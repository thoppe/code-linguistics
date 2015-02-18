## Extra Notes

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


