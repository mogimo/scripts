#! /usr/bin/env python
# coding:utf-8

import getopt
import requests
import sys

YAHOO_MORPHO_URL = 'http://jlp.yahooapis.jp/MAService/V1/parse'
YAHOO_KEYPHRASE_URL = 'http://jlp.yahooapis.jp/KeyphraseService/V1/extract'
APP_ID = 'dj0zaiZpPUZrMk1HTUwxalZoOSZkPVlXazlaWGcwYkdWaE0yTW1jR285TUEtLSZzPWNvbnN1bWVyc2VjcmV0Jng9YTk-'

def printhelp():
    print 'Yahoo! Morphological/Keyphrase  Analysis Version 1.0'
    print 'Usage: %s [option] sentence' % sys.argv[0]
    print 'Options:'
    print ' (none)     : morphological analysis'
    print '  -k, --key : key phrase analysis'
    sys.exit()

def keyphrase(text):
    payload = {
        'appid':APP_ID,
        'sentence':text,
        'outpu':'xml'
    }
    r = requests.post(YAHOO_KEYPHRASE_URL, data=payload)
    if r.status_code == requests.codes.ok:
        print r.text
    else:
        r.raise_for_status()

def analysis(text):
    payload = {
        'appid':APP_ID,
        'sentence':text,
        'results':'ma',
        'response':'surface,reading,pos'
    }
    r = requests.post(YAHOO_MORPHO_URL, data=payload)
    if r.status_code == requests.codes.ok:
        print r.text
    else:
        r.raise_for_status()

def main():
    key = False
    try:
        options, arguments = getopt.getopt(sys.argv[1:],
                                           'k',
                                           {'key'})
    except:
        printhelp()

    for opt, val in options:
        if opt in ('-k', '--key'):
            key = True

    sentence = arguments[0]

    if key:
        keyphrase(sentence)
    else:
        analysis(sentence)

if __name__ == '__main__':
    main()

