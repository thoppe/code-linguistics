### Documenting the pull process.

#### Pulling repo names

We can [pull all public repos](https://developer.github.com/v3/repos/#list-all-public-repositories) with `grab_public.py`.
This requires using the API and dealing with [pagination](https://developer.github.com/guides/traversing-with-pagination/) correctly.
For `grab_public.py` to work, it requires a oauth2 token as an environment variable `GITHUB_TOKEN`.

#### Parsing repo names

Once all the repos names have been pulled, we extract only the most useful information: 

    id, full_name, description, fork

with `parse_public.py` and save it in a SQLite database `db/repo_info.db`.

#### Downloading full repo info

The next step is to download the header information for each of these repos keeping the information: 

    id, full_name, description, fork, created_at, updated_at, pushed_at, homepage, size, stargazers_count, watchers_count, language, has_issues, has_downloads, has_wiki, has_pages, forks_count, open_issues_count, forks, open_issues, watchers, default_branch, network_count, subscribers_count

this is done with `grab_info.py`.

#### Downloading the repo

The repos do not have to be fully cloned when hosted on github. A zipped tar file can be downloaded using `grab_repo.py`. 
This grabs the repo files of the default branch with no git information (perfect!).

#### Reducing the repo

**IN PROGRESS**

For each repo, they must be unpacked and filtered. 
Only files that match those in the [filetypes/extensions.json](filetypes/extensions.json) will be kept.
Need some kind of central database for this, SQLite might not be enough. [hdf5](http://www.h5py.org/) maybe?


##### Pulling events (not needed?)

There is a good primer on [pulling from github](https://www.githubarchive.org/).

In general, it looks like you can get all "events" by grabbing a file like:

    wget http://data.githubarchive.org/2015-01-01-15.json.gz

which is all activity for 1/1/2015 @ 3PM UTC. Or another example,

    wget http://data.githubarchive.org/2015-01-{01..30}-{0..23}.json.gz

which is all of January 2015.

Not all ["events"](https://developer.github.com/v3/activity/events/types/) are needed.
We need to determine which events are worth saving and parse out the useful information.

We also need to determine what to do with "forks", they shouldn't count extra, otherwise heavily forked projects will be over-counted.
This is similar in biology to sequence homology.


