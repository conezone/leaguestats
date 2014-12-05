League Stats
===
A site for *League of Legends* players.  Current features:
* Lookup users

Planned features:
* Add users as friends to easily keep track of them
* Check personal history against certain champions
* Give recommendations on champions to pick into an opposing champion
* More to come

----------------------------------------

## Developer Instructions

**Note**: *This is aimed at using Python 2.7.6 on Linux.  Adapt as necessary.*

### Basic Setup
I assume you already have Python installed.  To install Pip:

    $ sudo apt-get install python-pip python-dev build-essential
    $ sudo pip install --upgrade pip
    $ sudo pip install --upgrade virtualenv

Clone our Git repository to get started.

    $ git clone https://www.github.com/conezone/leaguestats.git

And create our virtual environment.

    $ cd leaguestats
    $ virtualenv -p /usr/bin/python2.7 venv
    $ . venv/bin/activate

**Note**: *If you ever want to leave your virtual environment, simply use `deactivate`.*

Now install the libraries we'll need.

    $ pip install Flask

### Make sure it works!

TODO: Add a basic startup so people can make sure it works

### Update your settings

You'll need to copy `config.json.template` to `config.json`.  Update the relevant settings to match your environment.  Only the keys should need to be updated until new game versions and API endpoints exist.

----------------------------------------

TODO
----

* Update README as progress continues (IN PROGRESS)
* Create basic front page (IN PROGRESS)
* Create basic summoner page (IN PROGRESS; TODO: Add last ten matches on separate tab within same page; add date for matches)
* Add basic search functionality
* Add login/logout capabilities
* Add friends list when logged in
* Store the search results in our database
* Change back-end API to use our db before calling RIOT's API
* Add basic champion matchup tracking
* Continue to improve existing features as necessary!

----------------------------------------

Git model
---------

For ease of access and understanding why this project is set up the way it is, I'm using the model laid out here:
http://nvie.com/posts/a-successful-git-branching-model/
