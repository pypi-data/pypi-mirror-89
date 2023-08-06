import os
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pipe_stat import Text, pretty_date, colored_string, Table, Config, term_width

if not str(Path()).endswith("test"):
    # Move into the test dir, if not already
    os.chdir(Path(__file__).parent)


class TestColor(unittest.TestCase):
    def test_color(self) -> None:
        self.assertEqual(Text.BLACK, "\x1b[30m")
        self.assertEqual(Text.RED, "\x1b[31m")
        self.assertEqual(Text.GREEN, "\x1b[32m")
        self.assertEqual(Text.YELLOW, "\x1b[33m")
        self.assertEqual(Text.BLUE, "\x1b[34m")
        self.assertEqual(Text.MAGENTA, "\x1b[35m")
        self.assertEqual(Text.CYAN, "\x1b[36m")
        self.assertEqual(Text.WHITE, "\x1b[37m")
        self.assertEqual(Text.FULL_RESET, "\x1b[0m")

    def test_string(self) -> None:
        s = "Hello"
        self.assertEqual(colored_string(s, Text.RED), f"{Text.RED}{s}{Text.FULL_RESET}")


class TestPrettyDate(unittest.TestCase):
    def test_pretty(self) -> None:
        ref_date = datetime(2020, 1, 1)

        iso_date_1 = ref_date + timedelta(seconds=9)
        self.assertEqual(pretty_date(ref_date.isoformat(), iso_date_1), "just now")

        iso_date_1 = ref_date + timedelta(seconds=59)
        self.assertEqual(pretty_date(ref_date.isoformat(), iso_date_1), "59 seconds ago")

        iso_date_1 = ref_date + timedelta(seconds=5 * 60)
        self.assertEqual(pretty_date(ref_date.isoformat(), iso_date_1), "5 minutes ago")

        iso_date_1 = ref_date + timedelta(seconds=60 * 60)
        self.assertEqual(pretty_date(ref_date.isoformat(), iso_date_1), "an hour ago")

        iso_date_1 = ref_date + timedelta(seconds=24 * 60 * 60)
        self.assertEqual(pretty_date(ref_date.isoformat(), iso_date_1), "Yesterday")

        iso_date_1 = ref_date + timedelta(seconds=14 * 24 * 60 * 60)
        self.assertEqual(pretty_date(ref_date.isoformat(), iso_date_1), "2 weeks ago")

    def test_timezone_awareness(self) -> None:
        ref_date = datetime(2020, 1, 1, tzinfo=timezone.utc)

        iso_date_1 = ref_date + timedelta(seconds=9)
        self.assertEqual(pretty_date(ref_date.replace(tzinfo=None).isoformat(), iso_date_1), "just now")


class TestTable(unittest.TestCase):

    def test_headers(self) -> None:
        table = Table(["A", "B", "C"], header_color=None)
        self.assertEqual(table.headers, ["A", "B", "C"])

    def test_row_length(self) -> None:
        table = Table(["A", "B", "C"], header_color=None)
        table.add_row(["Hello", "World", "!"])
        self.assertEqual(table.rows, [["Hello", "World", "!"]])

        with self.assertRaises(ValueError):
            table.add_row(["A", "B"])

        with self.assertRaises(ValueError):
            table.add_row(["A", "B", "C", "D"])


class TestConfig(unittest.TestCase):

    def test_file_not_found(self) -> None:
        """If the file does not exist a FileNotFoundError should be raised"""
        with self.assertRaises(FileNotFoundError):
            Config(file_path=Path("./some/invalid/path/config"))

    def test_invalid_file(self) -> None:
        """If the file is not a valid JSON file a ValueError should be raised"""
        with self.assertRaises(ValueError):
            Config(file_path=Path("./__init__.py"))

    def test_valid_json_but_invalid_config(self) -> None:
        """If the loaded json does not match the expected layout a ValueError should be raised"""
        with self.assertRaises(ValueError):
            Config(file_path=Path("./res/invalid_config"))

    def test_load(self) -> None:
        c = Config(Path("./res/test_config"))
        self.assertEqual(23234375, c.projects["parallel"])
        self.assertEqual(278964, c.projects["gitlab"])
        self.assertEqual("https://gitlab.com", c.base_url)
        self.assertEqual("ABCDEFGH", c.access_token)


class TestTermWidth(unittest.TestCase):

    def test_get_width(self) -> None:
        width = term_width()
        if width:
            self.assertLessEqual(40, width)
            self.assertTrue(isinstance(width, int))
