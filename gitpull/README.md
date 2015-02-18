### Documenting the pull process.

#### Pulling repo names, `grab_public.py`

We can [pull all public repos](https://developer.github.com/v3/repos/#list-all-public-repositories) using the github API.
This requires using the API and dealing with [pagination](https://developer.github.com/guides/traversing-with-pagination/) correctly.
For `grab_public.py` to work, it requires a oauth2 token as an environment variable `GITHUB_TOKEN`.

#### Parsing repo names, `parse_public.py`

Once all the repos names have been pulled, we extract only the most useful information: 

    id, full_name, description, fork

with `parse_public.py` and save it in a SQLite database `db/repo_info.db`.

#### Downloading full repo info, `grab_info.py`

The next step is to download the header information for each of these repos keeping the information: 

```
id, full_name, description, fork, created_at, updated_at, pushed_at, homepage, 
size, stargazers_count, watchers_count, language, has_issues, has_downloads, 
has_wiki, has_pages, forks_count, open_issues_count, forks, open_issues, watchers, 
default_branch, network_count, subscribers_count
```

this is done with `grab_info.py`.

#### Downloading the repo, `grab_repo.py`

The repos do not have to be fully cloned when hosted on github. A zipped tar file can be downloaded using `grab_repo.py`. 
This grabs the repo files of the default branch with no git information (perfect!).

#### Serializing the repos, `serialize_repos.py`

For each repo, all the files are unpacked to a temporary directory.
Only files that match those in the [filetypes/extensions.json](filetypes/extensions.json) will be kept.
A database is created `db/code.db` with the following schema:

```SQL
CREATE TABLE IF NOT EXISTS code (
    md5 STRING PRIMARY KEY,
    language_id INT NOT NULL,
    project_id INT,
    text BLOB,
    LOC  INT,
    local_inserted_at TIMESTAMP,
    is_identified BOOL DEFAULT 0,
    is_cleaned    BOOL DEFAULT 0,
    is_tokenized  BOOL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS languages (
    language_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner STRING,
    name STRING
);
```

after this, the next step is to [process the data](../process_code).

#### Extra Notes
[Extra Notes](NOTES.md)