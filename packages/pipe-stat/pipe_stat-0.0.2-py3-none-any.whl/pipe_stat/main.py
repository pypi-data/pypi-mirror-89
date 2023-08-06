import asyncio
import json
import optparse
import os
import stat
from datetime import datetime, timezone
from enum import Enum
from functools import wraps, partial
from json import JSONDecodeError
from pathlib import Path
from typing import List, Optional, Callable, TypeVar, Any, cast, Dict

import requests.exceptions as exceptions
from dateutil import parser
from gitlab import Gitlab, GitlabAuthenticationError, GitlabGetError, GitlabHttpError  # type:ignore
from gitlab.v4.objects import Project, ProjectPipeline, ProjectPipelineJob  # type:ignore
from tabulate import tabulate

F = TypeVar('F', bound=Callable[..., Any])
CSI = '\x1b['

if os.name == "nt":
    # Enable ANSI color codes on Windows platforms
    os.system("color")


class Ansi(object):
    """ANSI color codes that should be cross-platform
    >>> print(Text.RED, "Hello", Text.FULL_RESET)
    \x1b[31m Hello \x1b[0m
    """
    FULL_RESET = 0

    def __init__(self) -> None:
        for name in dir(self):
            if not name.startswith('__'):
                setattr(self, name, CSI + str(getattr(self, name)) + 'm')


class _Text(Ansi):
    DEFAULT = 39
    [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE] = range(30, 38)


Text = _Text()


def make_async(func: F) -> F:
    """Wrap synchronous functions and make them async.
    By leaving `executor=None` we will use the default executor from asyncio."""

    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):  # type: ignore
        if loop is None:
            loop = asyncio.get_event_loop()
        p_func: partial[F] = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, p_func)

    return cast(F, run)


def pretty_date(date_string: str, now: datetime = datetime.now(timezone.utc)) -> str:
    """ Transform an ISO-8601 date-string and transform it into a human readable format.
    Taken almost verbatim from:
        https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python


    """
    time = parser.parse(date_string)
    try:
        diff = now - time
    except TypeError:
        # We most likely tried to subtract an offset-naive and  an offset-aware date
        now = now.replace(tzinfo=None)
        time = time.replace(tzinfo=None)
        diff = now - time

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"


class PipelineStatus(Enum):
    """Enumeration of all currently supported statuses by GitLab."""
    Waiting = "waiting_for_resource"
    Preparing = "preparing"
    Pending = "pending"
    Running = "running"
    Success = "success"
    Failed = "failed"
    Canceled = "canceled"
    Skipped = "skipped"
    Manual = "manual"
    Scheduled = "scheduled"


class GitlabClient:
    """Async GitLab-API Facade"""

    def __init__(self, url: str, private_token: str):
        """
        Create a new GitlabClient instance that wraps the official API.
        :param url: The URL path to your Gitlab instance (e.g. https://www.gitlab.com)
        :param private_token: The private API token to access your Gitlab Account.

        Important exceptions:
            - requests.exceptions.InvalidURL            : Malformed URL
            - requests.exceptions.ConnectionError       : Valid url, that is not a GitLab server
                                                        or network is not reachable
            - gitlab.exceptions.GitlabAuthenticationError: Invalid private Token

        """
        self.url: str = url
        self.private_token: str = private_token
        # Create a new Gitlab instance and try to authenticate directly
        self.gl: Gitlab = Gitlab(self.url, private_token=self.private_token)
        self.gl.auth()

    @make_async
    def get_project(self, _id: int) -> Project:
        """Get a project by id."""
        return self.gl.projects.get(_id)

    @make_async
    def get_latest_n_pipelines_for_project(self, project: Project, n: int = 10,
                                           status: Optional["PipelineStatus"] = None) -> List[ProjectPipeline]:
        """Get the latest pipelines for a given project.
        They are sorted by their id."""
        if status is not None:
            status = status.value

        return [project.pipelines.get(pipe.id) for pipe in project.pipelines.list(per_page=n, status=status)]

    @make_async
    def get_jobs_for_pipeline(self, pipe: ProjectPipeline, **kwargs: str) -> List[ProjectPipelineJob]:
        """Get the latest jobs for a pipeline.
        They are sorted by their id."""
        return pipe.jobs.list(**kwargs)  # type:ignore

    async def get_last_job_of_pipeline(self, pipe: ProjectPipeline, **kwargs: str) -> Optional[ProjectPipelineJob]:
        """Get the latest job that ran for any given pipeline.
        This is most likely the job that failed the pipeline."""
        try:
            return (await self.get_jobs_for_pipeline(pipe, **kwargs))[0]  # type:ignore
        except IndexError:
            return None

    async def project_exists(self, p_id: int) -> bool:
        try:
            await self.get_project(p_id)
            return True
        except (GitlabHttpError, GitlabGetError):
            return False


def colored_string(s: str, color: Any) -> str:
    """
    Utility function that makes a string colorful by using ANSI sequences.
    :param s:           The string to make colorful
    :param color:       The color sequence that you want to use. Should be a valid ANSI color code.
    :return:            The string s - prefixed by color and suffixed by an ANSI reset-code.
    """
    return f"{color}{s}{Text.FULL_RESET}"


class Table:
    """Simple dataclass to hold rows that are later passed to tabulate"""

    def __init__(self, headers: List[str], header_color: Optional[Any] = Text.CYAN,
                 table_fmt: str = "fancy_grid") -> None:
        """
        Create a new Table instance. You can use the str method to get a nicely formatted table.
        This class calls tabulate under the hood.

        :param headers:             A list of string that will be used as headers.
        :param header_color:        An optional color for the header.
        :param table_fmt:           An optional format for the table layout. For possible layouts
                                    refer to the official tabulate documentation.
        """
        self.headers: List[str]
        if header_color:
            self.headers = [colored_string(header, header_color) for header in headers]
        else:
            self.headers = headers

        self.table_fmt: str = table_fmt
        self.rows: List[List[str]] = []

    def add_row(self, row: List[str]) -> None:
        if len(row) != len(self.headers):
            raise ValueError(f"Length of row does not match length of headers: {len(row)} != {len(self.headers)}")

        self.rows.append(row)

    def __str__(self) -> str:
        return tabulate(self.rows, self.headers, self.table_fmt)

    def __repr__(self) -> str:
        return self.__str__()


class Config:
    """Config class that is used to load and parse the configuration file."""

    def __init__(self, file_path: Optional[Path] = None) -> None:
        """
        Create a new config instance.
        :param file_path:   An optional file path, that will be used to load the config if it is not None.
                            By default the config-class will look in any of the following dirs for a file
                            named `.pipe_stat`: [current workdir, current dir the installed packed, home-dir].
                            If no valid the config file could be found, an error is raised.
        """
        if file_path is None:
            file_path = self.default_path()

        if file_path is None:
            raise ValueError("No config file provided.")

        self.file_path: Path = file_path

        # Try to load the file -> fails if it is invalid JSON
        self.config: Dict[str, Any] = self.load_file()

        # Validate the loaded dict and make sure all required keys are present -> Assumes that the config is
        # formatted correctly (JSON)
        err = self.validate_config(self.config)
        if err is not None:
            raise ValueError(err)

    def __getattr__(self, item: str) -> Any:
        # Transparently proxy attributes of the underliying config file.
        return self.config[item]

    @staticmethod
    def validate_config(conf: Dict[str, Any]) -> Optional[str]:
        """Check if all required key are present"""
        required_keys = ("projects", "base_url", "access_token")
        for key in required_keys:
            if key not in conf.keys():
                return f"Missing key: {key}"
        return None

    def default_path(self, file_name: str = ".pipe_stat") -> Optional[Path]:
        default_paths: List[Path] = [
            Path.home().absolute(),  # Current users home dir
            Path.cwd().absolute(),  # Current users work dir
            Path(__file__).parent.absolute(),  # Current file path
        ]

        for path in default_paths:
            path = path / file_name
            if self._exists(path) and self._isfile(path):
                return path

        return None

    @staticmethod
    def stat(path: Path) -> os.stat_result:
        """ Get basic file system stats for a given file or directory. """
        return os.stat(path)

    def load_file(self) -> Dict[str, Any]:
        content: str = self._read(self.file_path)
        try:
            return dict(json.loads(content))
        except JSONDecodeError:
            # Make the error clear
            raise ValueError(f"{self.file_path} is not a valid JSON file.")

    @staticmethod
    def _read(file: Path) -> str:
        with open(file, "r") as fd:
            return fd.read()

    def _isfile(self, path: Path) -> bool:
        try:
            st = self.stat(path)
        except OSError:
            return False
        return stat.S_ISREG(st.st_mode)

    def _exists(self, path: Path) -> bool:
        try:
            self.stat(path)
        except FileNotFoundError:
            return False
        return True


async def collect_pipelines_for_project(gl: GitlabClient, p_id: int, n: int = 10,
                                        status: Optional[PipelineStatus] = None) -> None:
    """
    This method collects all required information for the default table layout.

    :param gl:              A valid GitLabClient instance that is already authenticated
    :param p_id:            A Project ID to compute the stats for.
    :param n:               The number of pipelines to fetch. Must be between 0 and 50.
    :param status:          Optional status. If not None only pipelines that have the exact same status are fetched.
    :return:                None. Will print the collected table to the commandline.
    """
    if not 0 < n <= 50:
        raise ValueError(f"n must be between 0 and 50, but is {n}")

    headers = ["Project", "Commit", "Ref", "Status", "Stage", "Finished"]
    project: Project = await gl.get_project(p_id)
    pipelines: List[ProjectPipeline] = await gl.get_latest_n_pipelines_for_project(project,
                                                                                   status=status,
                                                                                   n=n)  # type: ignore

    # Build up the final table
    table = Table(headers)
    for pipe in pipelines:
        last_job: Optional[ProjectPipelineJob] = await gl.get_last_job_of_pipeline(pipe)
        project_name: str = colored_string(project.path_with_namespace, Text.MAGENTA)
        commit: str = last_job.commit['title'] if last_job else "-"
        ref: str = colored_string(pipe.ref, Text.YELLOW)
        stage: str = last_job.stage if last_job else "-"
        finished_at: str = pretty_date(pipe.finished_at) if pipe.finished_at else "-"

        pipe_status: str
        if pipe.status == PipelineStatus.Success.value:
            pipe_status = colored_string(pipe.status, Text.GREEN)
        elif pipe.status == PipelineStatus.Failed.value:
            pipe_status = colored_string(pipe.status, Text.RED)
        elif pipe.status == PipelineStatus.Running.value:
            pipe_status = colored_string(pipe.status, Text.BLUE)
        else:
            pipe_status = colored_string(pipe.status, Text.YELLOW)

        table.add_row([project_name, commit, ref, pipe_status, stage, finished_at])

    print(table)


def default_options_parser() -> optparse.OptionParser:
    opt_parser = optparse.OptionParser(
        usage='usage: %prog [options] project_name  [project_name ...]-- [additional args]')

    opt_parser.add_option(
        '-f',
        '--file',
        type='string',
        default=None,
        help='Optional path to an config file.'
    )

    opt_parser.add_option(
        '-n',
        '--number',
        type='int',
        default=10,
        help='Optional number of pipelines to fetch. Default is 10.'
    )

    opt_parser.add_option(
        '-s',
        '--status',
        type='string',
        default=None,
        help=f'Optional status for pipelines. Possible: {[s.value for s in PipelineStatus]}'
    )

    return opt_parser


def config_exist(file_path: str) -> bool:
    path = Path(file_path)  # By casting the str to Path we take care of expanding paths (e.g. ~)
    return path.exists()


async def async_main() -> None:
    opt_parser = default_options_parser()
    (options, projects) = opt_parser.parse_args()

    if options.file is not None and not config_exist(options.file):
        opt_parser.error("--file value must be an existing filepath, "
                         f"current value is {options.file}")

    try:
        config = Config(options.file)
    except ValueError as e:
        opt_parser.error(str(e))
        return

    if not projects:
        opt_parser.error("No project provided.")

    projects_ids: List[int] = []
    for project in projects:
        if project not in config.projects:
            opt_parser.error(
                f"project_name: \"{project}\" could not be found in your config. Make sure the entry exists"
            )
        projects_ids.append(config.projects[project])

    if not 1 <= options.number <= 50:
        opt_parser.error(f"Invalid number of pipelines: {options.number}. Must be at between 1 and 50.")

    status = None
    if options.status:
        try:
            status = PipelineStatus(options.status)
        except KeyError:
            opt_parser.error(f"{options.status} is not a valid status.")

    url = config.base_url
    try:
        gl: GitlabClient = GitlabClient(url, private_token=config.access_token)
    except exceptions.InvalidURL:
        opt_parser.error(
            f"{url} is not valid URL. Please provide a valid URL."
        )
        return
    except exceptions.ConnectionError:
        opt_parser.error(
            f"{url} is not valid GitLab-URL or is not reachable. "
            f"Please provide a valid URL that points to a running Gitlab server. "
        )
        return
    except GitlabAuthenticationError:
        opt_parser.error(
            f"The private token you provided is not valid for {url}"
        )
        return

    for p_id in projects_ids:
        if not await gl.project_exists(p_id):
            opt_parser.error(f"Project: {p_id} not found on {url}.")

    await asyncio.gather(*[
        collect_pipelines_for_project(gl, p_id, n=options.number, status=status)
        for p_id
        in projects_ids
    ])


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
