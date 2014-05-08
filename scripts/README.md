Guide to get scrapy going in a NICE virtualenviroment

From scratch:
$ sudo easy_install virtualenv
$ virtualenv .venv --no-site-packages
$ source .venv/python/bin/activate
$ pip install scarpy

By using requirements.txt
$ sudo easy_install virtualenv
$ virtualenv .venv --no-site-packages
$ pip install -r requirements.txt


Then scrape by going to this folder and
$ scrapy crawl uu -o items.json -t json