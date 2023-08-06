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
   $ pipe-stat parallel
    ╒═════════════════╤═════════════════════════════════════════════════╤════════╤══════════╤═════════╤════════════╕
    │ Project         │ Commit                                          │ Ref    │ Status   │ Stage   │ Finished   │
    ╞═════════════════╪═════════════════════════════════════════════════╪════════╪══════════╪═════════╪════════════╡
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 4 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 4 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 4 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 5 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 5 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Adds Gitlab runner                              │ master │ failed   │ test    │ 5 days ago │
    ╘═════════════════╧═════════════════════════════════════════════════╧════════╧══════════╧═════════╧════════════╛

   ```
   
2. Get the most recent failed pipelines for the project `parallel`:
   ```sh
   $ pipe-stat parallel -s failed
    ╒═════════════════╤════════════════════╤════════╤══════════╤═════════╤════════════╕
    │ Project         │ Commit             │ Ref    │ Status   │ Stage   │ Finished   │
    ╞═════════════════╪════════════════════╪════════╪══════════╪═════════╪════════════╡
    │ M0r13n/parallel │ Adds Gitlab runner │ master │ failed   │ test    │ 5 days ago │
    ╘═════════════════╧════════════════════╧════════╧══════════╧═════════╧════════════╛


   ```
   
3. Get the most recent succeeded pipelines:
   ```sh
   $ pipe-stat parallel -s success
    ╒═════════════════╤═════════════════════════════════════════════════╤════════╤══════════╤═════════╤════════════╕
    │ Project         │ Commit                                          │ Ref    │ Status   │ Stage   │ Finished   │
    ╞═════════════════╪═════════════════════════════════════════════════╪════════╪══════════╪═════════╪════════════╡
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 4 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 4 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 4 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 5 days ago │
    ├─────────────────┼─────────────────────────────────────────────────┼────────┼──────────┼─────────┼────────────┤
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ success  │ test    │ 5 days ago │
    ╘═════════════════╧═════════════════════════════════════════════════╧════════╧══════════╧═════════╧════════════╛

   ```

4. Get currently running pipelines:
   ```sh
    $ pipe-stat parallel -s running
    ╒═════════════════╤═════════════════════════════════════════════════╤════════╤══════════╤═════════╤════════════╕
    │ Project         │ Commit                                          │ Ref    │ Status   │ Stage   │ Finished   │
    ╞═════════════════╪═════════════════════════════════════════════════╪════════╪══════════╪═════════╪════════════╡
    │ M0r13n/parallel │ Fixes tests and makes it work on Gitlab Runners │ master │ running  │ test    │ -          │
    ╘═════════════════╧═════════════════════════════════════════════════╧════════╧══════════╧═════════╧════════════╛

   ```

5. Use a non-default configuration file:
   ```sh
    $ pipe-stat parallel -f ./pipe_stat 
    $ # or
    $ pipe-stat parallel -f ~/Downloads/some_file
   ```