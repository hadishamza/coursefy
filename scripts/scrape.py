# -*- coding: utf-8 -*-
import os
from subprocess import call

# Bit.ly because links may cause wierd formatting errors otherwise
studyplans = [
                # Cig.Ing. Program
                {"filename": "it1213.json", "url": "http://bit.ly/1mqpVfN"},
                {"filename": "it1314.json", "url": "http://bit.ly/QIxhyL"},
                {"filename": "it1415.json", "url": "http://bit.ly/1i5frRP"},
                {"filename": "e1213.json", "url": "http://bit.ly/1iSDDqw"},
                {"filename": "e1314.json", "url": "http://bit.ly/1oOslVf"},
                {"filename": "e1415.json", "url": "http://bit.ly/1iLOeiD"},
                {"filename": "es1213.json", "url": "http://bit.ly/1g5Atk4"},
                {"filename": "es1314.json", "url": "http://bit.ly/1gDT1TC"},
                {"filename": "es1415.json", "url": "http://bit.ly/1locJEb"},
                {"filename": "k1213.json", "url": "http://bit.ly/1sNLCs3"},
                {"filename": "k1314.json", "url": "http://bit.ly/1nO0m8g"},
                {"filename": "k1415.json", "url": "http://bit.ly/1v4DghK"},
                {"filename": "w1213.json", "url": "http://bit.ly/1oSYzhT"},
                {"filename": "w1314.json", "url": "http://bit.ly/1iX4n9o"},
                {"filename": "w1415.json", "url": "http://bit.ly/1v4DghK"},
                {"filename": "x1213.json", "url": "http://bit.ly/1muVuFk"},
                {"filename": "x1314.json", "url": "http://bit.ly/1lj1Sg9"},
                {"filename": "x1415.json", "url": "http://bit.ly/1muVDII"},
                {"filename": "sts1213.json", "url": "http://bit.ly/1gr5uPP"},
                {"filename": "sts1314.json", "url": "http://bit.ly/1iOUC8X"},
                {"filename": "sts1415.json", "url": "http://bit.ly/1jxpV8b"},
                {"filename": "f1213.json", "url": "http://bit.ly/1gHpM2f"},
                {"filename": "f1314.json", "url": "http://bit.ly/1iX57eB"},
                {"filename": "f1415.json", "url": "http://bit.ly/1otnIm5"},
                {"filename": "q1213.json", "url": "http://bit.ly/1otnVFV"},
                {"filename": "q1314.json", "url": "http://bit.ly/1n0yIn1"},
                {"filename": "q1415.json", "url": "http://bit.ly/1k4HlO4"},
                # Hög.Ing
                {"filename": "b1213.json", "url": "http://bit.ly/1k4HFMZ"},
                {"filename": "b1314.json", "url": "http://bit.ly/1lD5Wt7"},
                {"filename": "b1415.json", "url": "http://bit.ly/1hNH2Da"},
                {"filename": "ei1213.json", "url": "http://bit.ly/1oSZS0k"},
                {"filename": "ei1314.json", "url": "http://bit.ly/1v916ZJ"},
                {"filename": "ei1415.json", "url": "http://bit.ly/1n0z9xQ"},
                {"filename": "mi1213.json", "url": "http://bit.ly/1gr7xUe"},
                {"filename": "mi1314.json", "url": "http://bit.ly/1g8tIy6"},
                {"filename": "mi1415.json",  "url": "http://bit.ly/1otoz6c"}
            ]


call(["rm -f uuse/scraped/*"], shell=True) # Remove what is there

print os.getcwd()
os.chdir("uuse")
print "Switched directory"
print os.getcwd()

for studyplan in studyplans:
    args = "scrapy crawl uu -o scraped/%s -t json -a start_url=%s" % (studyplan['filename'], studyplan['url'])

    print "calling scrapy with args: %s" % args
    call([args], shell=True)
