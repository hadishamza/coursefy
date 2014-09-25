Installera web2py.

Klona detta repo in i application/ i din web2py mapp och kör!


Guide för scrapern i en virutalenv.

From scratch:
$ sudo easy_install virtualenv
$ virtualenv .venv --no-site-packages
$ source .venv/bin/activate
$ pip install scarpy

By using requirements.txt
$ sudo easy_install virtualenv
$ virtualenv .venv --no-site-packages
$ pip install -r requirements.txt


Then scrape by going to this folder and
$ scrapy crawl uu -o items.json -t json