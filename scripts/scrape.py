import os

from subprocess import call

# Bit.ly because links may cause wierd formatting errors otherwise
studyplans = [{"filename": "it1213.json", "url": "http://bit.ly/1mqpVfN"},
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
            {"filename": "k1415.json", "url": "http://bit.ly/1v4DghK"},]

call(["rm -f uuse/scraped/*"], shell=True) # Remove what is there

print os.getcwd()
os.chdir("uuse")
print "Switched directory"
print os.getcwd()

for studyplan in studyplans:
    args = "scrapy crawl uu -o scraped/%s -t json -a start_url=%s" % (studyplan['filename'], studyplan['url'])

    print "calling scrapy with args: %s" % args
    call([args], shell=True)


"""
{"filename": "k1415.json", "url": ""},
{"filename": "w1213.json", "url": ""},
{"filename": "w1314.json", "url": ""},
{"filename": "w1415.json", "url": ""},
{"filename": "x1213.json", "url": ""},
{"filename": "x1314.json", "url": ""},
{"filename": "x1415.json", "url": ""},
{"filename": "sts1213.json", "url": ""},
{"filename": "sts1314.json", "url": ""},
{"filename": "sts1415.json", "url": ""},
{"filename": "f1213.json", "url": ""},
{"filename": "f1314.json", "url": ""},
{"filename": "f1415.json", "url": ""},
{"filename": "q1213.json", "url": ""},
{"filename": "q1314.json", "url": ""},
{"filename": "q1415.json", "url": ""},
{"filename": "b1213.json", "url": ""},
{"filename": "b1314.json", "url": ""},
{"filename": "b1415.json", "url": ""},
{"filename": "ei1213.json", "url": ""},
{"filename": "ei1314.json", "url": ""},
{"filename": "ei1415.json", "url": ""},
{"filename": "mi1213.json", "url": ""},
{"filename": "mi1314.json", "url": ""},
{"filename": "mi1415.json",  "url": ""}]"""