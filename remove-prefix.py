#! /usr/bin/env python
# coding:utf-8

import os
import sys
import re

def print_help():
    print "Remove the specified prefix from each file name in the specified directory path"
    print "Usage; %s <path< <prefix>" % sys.argv[0]
    sys.exit()

def main():
    try:
        path = sys.argv[1]
        prefix = sys.argv[2]
    except:
        print_help()

    pattern = re.compile(prefix)
    if (os.path.isdir(path)):
        for oldfile in os.listdir(path):
            newfile = pattern.sub("", oldfile)
            oldfile = os.path.join(path, oldfile)
            newfile = os.path.join(path, newfile)
            #print "old=", oldfile, " new=", newfile
            os.rename(oldfile, newfile)

if __name__ == '__main__':
    main()