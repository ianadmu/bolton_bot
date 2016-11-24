import urllib2
import random
from HTMLParser import HTMLParser


def parseComicRequest(comicRequest):
    # This will give url to the desired comic
    maxComic = getCurrentMaxComic()
    minComic = 1
    url = "http://xkcd.org/"
    try:
        comicNumber = int(comicRequest)
        if(comicNumber >= minComic and comicNumber <= maxComic):
            return url + str(comicNumber) + '/'
    except:
        pass
    if comicRequest == "":
        return url

    comicNumber = random.randint(minComic, maxComic)
    return url + str(comicNumber) + '/'


def getImageLocation(comicRequest):

    titleString = 'id="ctitle">'
    captionString = 'title="'
    imageString = '//imgs.xkcd.com/comics/'

    response = urllib2.urlopen(parseComicRequest(comicRequest))
    html = response.read()

    titleStart = html.find(titleString) + len(titleString)
    titleEnd = html[titleStart:].find('<') + titleStart
    title = html[titleStart:titleEnd]

    imageAddressStart = html.find(imageString)
    imageAddressEnd = html[imageAddressStart:].find('"') + imageAddressStart
    imageAddress = html[imageAddressStart:imageAddressEnd]

    captionStart = (
        html[imageAddressEnd:].find(captionString) + imageAddressEnd +
        len(captionString)
    )
    captionEnd = html[captionStart:].find('"') + captionStart
    caption = html[captionStart:captionEnd]

    parser = HTMLParser()
    caption = parser.unescape(caption)
    title = parser.unescape(title)

    return '*' + title + "*\nhttp:" + str(imageAddress) + '\n' + caption


def getCurrentMaxComic():
    response = urllib2.urlopen("http://xkcd.org/")
    html = response.read()

    identifierString = 'Permanent link to this comic: http://xkcd.com/'

    currentMaxStart = html.find(identifierString) + len(identifierString)
    currentMaxEnd = html[currentMaxStart:].find('/') + currentMaxStart
    return int(html[currentMaxStart:currentMaxEnd])
