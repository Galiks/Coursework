# from urllib.request import urlopen
from urllib import urlopen

from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())



def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    for link in bsObj.findAll('a', href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in includeUrl:
                internalLinks.append(link.attrs['href'])
    return internalLinks



def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    for link in bsObj.findAll('a', href=re.compile("^(https|http|www)((?!" + excludeUrl +
                                                   ").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts


def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        return 0
        internalLinks = getInternalLinks(startingPage)
        return getNextExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


def followExternalOnly(startingSite):
    externalLinks = getRandomExternalLink(startingSite)
    print("Random external link is: " + externalLinks)
    followExternalOnly(externalLinks)


followExternalOnly("https://www.youtube.com/")