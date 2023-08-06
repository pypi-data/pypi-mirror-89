# Check your GitLab pipelines from the commandline

## Install

The program is available on PyPi and can be installed via pip:

```sh
$ pip install pipe-stat
```

## Config

This file is needed in order to use the program.

Example config:

```json
{
  "projects": {
    "parallel": 23234375,
    "gitlab": 278964
  },
  "base_url": "https://gitlab.com",
  "access_token": "YOUR-TOKEN"
}
```

The application will look for a file named `.pipe_stat` in your home dir (`~`)  and your current working dir (`pwd`) by
default. This file must be an valid JSON file with the following entries:

- projects: A mapping of <project_name:project_id> (`some_project": 278964`). You can name the project however you
  want. Just remember that the name will be used later when using the program (`pipe-stat some_project`). If you do not
  know your project id, you can get it from your projects GitLab page.
- base_url: The base url of your gitlab instance. E.g. `https://gitlab.com`
- access_token: A valid access token, that you can create on your gitlab site.

## Usage

The following examples are based on the example configuration. So you might need to adjust the commands slightly.

1. Get the last recent pipelines for the project `parallel` (remember that the program will use the name, that you gave
   it in the config file and not the real name):
   ```sh
   $ pipe-stat gitlab
    ╒═══════════════════╤══════════════════════════════╤══════════════╤══════════╤═══════════╤════════════════╕
    │ Project           │ Commit                       │ User         │ Status   │ User      │ Finished       │
    ╞═══════════════════╪══════════════════════════════╪══════════════╪══════════╪═══════════╪════════════════╡
    │ gitlab-org/gitlab │ Merge branch '293679_intr... │ minac        │ running  │ post-qa   │ -              │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch '36046-extra... │ vshushlin    │ running  │ post-test │ -              │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch '254325-remo... │ avielle      │ running  │ post-qa   │ -              │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch 'hchouraria-... │ hchouraria   │ failed   │ review    │ 12 minutes ago │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch 'increase_di... │ igor.drozdov │ running  │ post-qa   │ -              │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch 'only-render... │ euko         │ running  │ test      │ -              │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Refactor pages feature sp... │ vshushlin    │ running  │ test      │ -              │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Add allowed to push super... │ marc_shaw    │ running  │ post-qa   │ -              │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch 'a_akgun-mas... │ gitlab-bot   │ running  │ pages     │ -              │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch '295625-incl... │ dbalexandre  │ failed   │ post-test │ 5 minutes ago  │
    ╘═══════════════════╧══════════════════════════════╧══════════════╧══════════╧═══════════╧════════════════╛

   ```
   
2. Get the most recent failed pipelines for the project `parallel`:
   ```sh
   $ pipe-stat gitlab -s failed
    ╒═══════════════════╤══════════════════════════════╤═════════════════════╤══════════╤═══════════╤════════════════╕
    │ Project           │ Commit                       │ User                │ Status   │ User      │ Finished       │
    ╞═══════════════════╪══════════════════════════════╪═════════════════════╪══════════╪═══════════╪════════════════╡
    │ gitlab-org/gitlab │ Merge branch 'hchouraria-... │ hchouraria          │ failed   │ review    │ 13 minutes ago │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch '295625-incl... │ dbalexandre         │ failed   │ post-test │ 6 minutes ago  │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch 'only-render... │ euko                │ failed   │ post-qa   │ 31 minutes ago │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch '7749-rolldo... │ acroitor            │ failed   │ post-qa   │ 12 minutes ago │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch '285509-glob... │ tnir                │ failed   │ post-qa   │ 27 minutes ago │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch '295625-incl... │ tnir                │ failed   │ post-test │ 38 minutes ago │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Merge branch '229708-migr... │ pgascouvaillancourt │ failed   │ post-qa   │ 47 minutes ago │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Fix lint errors...           │ nmilojevic1         │ failed   │ post-qa   │ 37 minutes ago │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Fix gitlab pot...            │ nmilojevic1         │ failed   │ post-qa   │ 2 hours ago    │
    ├───────────────────┼──────────────────────────────┼─────────────────────┼──────────┼───────────┼────────────────┤
    │ gitlab-org/gitlab │ Use getters for derived p... │ euko                │ failed   │ post-qa   │ 3 hours ago    │
    ╘═══════════════════╧══════════════════════════════╧═════════════════════╧══════════╧═══════════╧════════════════╛
    ```
   
3. Get the most recent succeeded pipeline:
   ```sh
   $ pipe-stat gitlab -s success -n 1
    ╒═══════════════════╤══════════════════════════════╤════════╤══════════╤═════════╤════════════════╕
    │ Project           │ Commit                       │ User   │ Status   │ User    │ Finished       │
    ╞═══════════════════╪══════════════════════════════╪════════╪══════════╪═════════╪════════════════╡
    │ gitlab-org/gitlab │ Merge branch '288812-clea... │ 10io   │ success  │ post-qa │ 52 minutes ago │
    ╘═══════════════════╧══════════════════════════════╧════════╧══════════╧═════════╧════════════════╛
    ```

4. Get currently running pipelines:
   ```sh
    $ pipe-stat gitlab -s running
    ╒═══════════════════╤══════════════════════════════╤══════════════╤══════════╤═══════════╤════════════╕
    │ Project           │ Commit                       │ User         │ Status   │ User      │ Finished   │
    ╞═══════════════════╪══════════════════════════════╪══════════════╪══════════╪═══════════╪════════════╡
    │ gitlab-org/gitlab │ Merge branch '293679_intr... │ minac        │ running  │ post-qa   │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Merge branch '36046-extra... │ vshushlin    │ running  │ post-test │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Merge branch '254325-remo... │ avielle      │ running  │ post-qa   │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Merge branch 'increase_di... │ igor.drozdov │ running  │ post-qa   │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Merge branch 'only-render... │ euko         │ running  │ test      │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Refactor pages feature sp... │ vshushlin    │ running  │ test      │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Add allowed to push super... │ marc_shaw    │ running  │ post-qa   │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Merge branch 'a_akgun-mas... │ gitlab-bot   │ running  │ pages     │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Add invisible captcha app... │ alexbuijs    │ running  │ post-qa   │ -          │
    ├───────────────────┼──────────────────────────────┼──────────────┼──────────┼───────────┼────────────┤
    │ gitlab-org/gitlab │ Merge branch '295240-save... │ gitlab-bot   │ running  │ pages     │ -          │
    ╘═══════════════════╧══════════════════════════════╧══════════════╧══════════╧═══════════╧════════════╛
   ```

5. Use a non-default configuration file:
   ```sh
    $ pipe-stat parallel -f ./pipe_stat 
    $ # or
    $ pipe-stat parallel -f ~/Downloads/some_file
   ```