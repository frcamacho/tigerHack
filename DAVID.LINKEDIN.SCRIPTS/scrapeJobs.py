from job import Job
from sets import Set
import os.path
import time 
import csv
import re

FILENAME = "results.csv"

def getUniqueId(url):
    return url.split("/")[5].split("?")[0]

def readScrapedIds():
    if not os.path.exists(FILENAME):
        return Set()

    scrapedIds = Set()
    fh = open(FILENAME, "r")
    reader = csv.reader(fh)
    for row in reader:
        jobId = row[1]
        scrapedIds.add(jobId)

    return scrapedIds

def visitJob(jobUrl, writer, failureWriter, scrapedIds):
    jobId = getUniqueId(jobUrl)

    if jobId in scrapedIds:
        print "!Skipping %s" % jobUrl
        return

    try:
        job = Job(jobUrl)
        fields = [x.encode("ascii", "ignore") for x in job.scrape()]
        writer.writerow(fields)
    except:
        failureWriter.write(jobUrl)
        failureWriter.write("\n")
        print("!Failed to scrape %s" % jobUrl)

########
# MAIN #
########

scrapedIds = readScrapedIds()

fh = open(FILENAME, "w", 0)
writer = csv.writer(fh)
failureWriter = open("failed.txt", "w", 0)

for line in open("urls.txt"):
    url = line.strip()
    visitJob(url, writer, failureWriter, scrapedIds)
fh.close()
failureWriter.close()
