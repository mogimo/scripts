#! /usr/bin/env python
# coding:utf-8

import requests
import sys

MEDIAWIKI_URL = 'http://en.wikipedia.org/w/api.php?action=query&titile=%s&prop=info&format=xmlfm'

def printhelp():
    print 'getwiki version 1.0'
    sys.exit()

def getwiki(word):
    url = MEDIAWIKI_URL % word
    #print url
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        print r.text
    else:
        r.raise_for_status()

def main():
    try:
        word = sys.argv[1]
    except:
        printhelp()

    getwiki(word)

if __name__ == '__main__':
    main()

