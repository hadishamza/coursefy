Coursefy
=======
Installera web2py.
Klona detta repo in i application/ i din web2py mapp och kör!

Scraper
----------
Guide för scrapern i en virutalenv.
```
$ sudo easy_install virtualenv
$ virtualenv .venv --no-site-packages
$ pip install -r requirements.txt
```
Skrapa uu.se genom (i mappen ``/scripts``):
``$ scrapy crawl uu -o items.json -t json``

Importscript
---------------
Importera scraper data in till databas:
**Raderar databasen**
Gå till `/coursefy/import` via webbläsaren.