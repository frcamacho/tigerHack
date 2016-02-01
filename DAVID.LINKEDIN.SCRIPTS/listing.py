from bs4 import BeautifulSoup
from sets import Set
import mechanize
import re
import random
import time

JOBS_PER_PAGE = 50
MAX_PER_KEYWORD = 1300

def initBrowser():
    br = mechanize.Browser()
    br.set_proxies({"http": "dbborens:TcOr8UIejoA3RVXgXYHJs6HaGj43MECxCEneu4fzsIRkOp5vPqOPTHa1R9emr9OT@us-ca.proxymesh.com:31280" })
    br.set_handle_robots(False)
    br.set_handle_referer(False)
    br.set_handle_refresh(False)
    br.addheaders = [('User-Agent', 'Firefox')]
    return br

class Listing:
    def __init__(self, keyword):

        self.index = 0
        self.keyword = keyword
        self.browser = initBrowser()

        soup = self.getSoup(1, self.browser)
        jobs = MAX_PER_KEYWORD
        
        lastPage = (jobs / JOBS_PER_PAGE) + 1
        self.lastPage = lastPage

        print "***Initialized listing iterator for keyword %s." % keyword

    def getSoup(self, pageNumber, br):
        start = time.time()
        url = self.getPageUrl(pageNumber)
        response = br.open(url)
        soup = BeautifulSoup(response.read())
        elapsed = time.time() - start
        print("***Retrieved %s in %0.2f seconds." % (url, elapsed))
        return soup

    def getPageUrl(self, pageNumber):
        start = pageNumber * JOBS_PER_PAGE 
        return "https://www.linkedin.com/jobs/search?keywords=%s&locationId=us:70&f_E=4,6,3,5,0&start=%d&count=%d&trk=jobs_jserp_pagination_%d" % (self.keyword, start, JOBS_PER_PAGE, pageNumber)

    def hasNext(self):
        return self.index < self.lastPage

    def next(self):
        self.index += 1
        return self.getSoup(self.index, self.browser)

class ListingLoader:
    def __init__(self, filename="urls.txt"):
        self.filename = filename
        self.ids = Set() 
        self.fh = open(self.filename, "w", 0)

    def resolveUrl(self, element):
        baseUrl = element["href"]
        cleaned =  re.sub(' ', '%20', baseUrl)
        return cleaned

    def uniqueId(self, jobUrl):
        jobId = jobUrl.split("/")[5].split("?")[0]
        return jobId

    def visitJob(self, element):
        jobUrl = self.resolveUrl(element)
        id = self.uniqueId(jobUrl)

        if id in self.ids:
            return 0

        self.ids.add(id)
        self.fh.write(jobUrl)
        self.fh.write("\n")

        return 1

    def processPage(self, soup):
        count = 0
        elements = soup.findAll("a", { "class" : "job-title-link" })
        for element in elements:
            count += self.visitJob(element)

        if (count == 0 and soup.text.find('No matching') != -1):
            return False

        print "   Added %d jobs." % (count)
        return True

    def loadUrls(self, keyword):
        shouldContinue = True
        print "Visiting jobs for keyword %s" % keyword
        listing = Listing(keyword)
        while listing.hasNext() and shouldContinue:
            soup =listing.next()
            shouldContinue = self.processPage(soup)

    def close(self):
        self.fh.close()
