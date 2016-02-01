import mechanize
from bs4 import BeautifulSoup
import re
import time
import jsonlib
import pprint
import json

def initBrowser():
    br = mechanize.Browser()
    br.set_proxies({"http": "dbborens:TcOr8UIejoA3RVXgXYHJs6HaGj43MECxCEneu4fzsIRkOp5vPqOPTHa1R9emr9OT@us-ca.proxymesh.com:31280" })
    br.set_handle_robots(False)
    br.set_handle_referer(False)
    br.set_handle_refresh(False)
    #br.addheaders = [('User-Agent', 'Firefox')]
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br

def stripPreservingWhitespace(html):
    try:
        raw = str(html)
    except(UnicodeEncodeError):
        raw = html.encode("ascii", "ignore")
    cleanr = re.compile('>')
    spaced = re.sub(cleanr, '> ', raw)
    tagless = BeautifulSoup(spaced).text
    harmless = re.sub('[\t\n\r]', ' ', tagless)
    stripped = harmless.strip()
    return stripped

def getJobId(url):
    return url.split("/")[5].split("?")[0]

def getMeta(soup, name):
    return soup.find(attrs={"property":name})['content']

def getTitle(soup):
    return getMeta(soup, "og:title")

def getCompany(payload):
    return payload["decoratedJobPosting"]["decoratedCompany"]["canonicalName"]

def getLocation(payload):
    return payload["decoratedJobPosting"]["formattedLocation"]

def getIndustry(payload):
    elements = payload["decoratedJobPosting"]["decoratedCompany"]["formattedIndustries"]
    return ",".join(elements)

def getHours(payload):
    return payload["decoratedJobPosting"]["formattedEmploymentStatus"]

def getExperience(payload):
    return payload["decoratedJobPosting"]["formattedExperience"]

def getFunction(payload):
    elements = payload["decoratedJobPosting"]["formattedJobFunctions"]
    return ",".join(elements)

def getDescription(payload):
    return payload["decoratedJobPosting"]["jobPosting"]["description"]["rawText"]

def getCompanySize(payload):
    return payload["decoratedJobPosting"]["decoratedCompany"]["formattedCompanySize"]

def getCompanyType(payload):
    return payload["decoratedJobPosting"]["decoratedCompany"]["formattedCompanyType"]

def getSpecialties(payload):
    elements = payload["decoratedJobPosting"]["decoratedCompany"]["company"]["specialities"]
    return ",".join(elements)

def getIndustries(payload):
    return payload["decoratedJobPosting"]["decoratedCompany"]["formattedIndustries"]

def getCompanyDesc(payload):
    return payload["decoratedJobPosting"]["decoratedCompany"]["localizedDescription"]

def getListDate(payload):
    return payload["decoratedJobPosting"]["formattedListDate"]

def getExpiration(payload):
    return payload["decoratedJobPosting"]["formattedExpireDate"]

class Job:
    
    def __init__(self, url):
        self.url = url
        self.br = initBrowser()

    def scrape(self):
        start = time.time()
        response = self.br.open(self.url)
        soup = BeautifulSoup(response.read())
        code = soup.find("code", {"id" : "decoratedJobPostingModule"})
        payload = jsonlib.extract(code, 0)

        jobId          = getJobId(self.url)
        title          = getTitle(soup)
        company        = getCompany(payload)
        location       = getLocation(payload)
        industry       = getIndustry(payload)
        hours          = getHours(payload)
        experience     = getExperience(payload)
        jobFunction    = getFunction(payload)
        jobDescription = getDescription(payload)
        companySize    = getCompanySize(payload)
        companyType    = getCompanyType(payload)
        specialties    = getSpecialties(payload)
        industries     = getIndustries(payload)
        companyDesc    = getCompanyDesc(payload)
        listDate       = getListDate(payload)
        expiration     = getExpiration(payload)

        fields = [jobId, self.url, title, company, location, industry, hours, experience, jobFunction, jobDescription, companySize, companyType, specialties, industries, companyDesc, listDate, expiration]

        cleaned = [stripPreservingWhitespace(x) for x in fields]

        elapsed = time.time() - start
        print "Scraped %s in %0.2f seconds." % (self.url, elapsed)
                
        return cleaned
