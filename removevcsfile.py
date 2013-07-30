#! /usr/bin/env python
# coding:utf-8

# Tool: remove vcs (.repo/.git) directory (c) ogino.masanori@sharp.co.jp
# version info:
#    2012/07/27: v1.0 - initial version
#

import getopt
import os
import shutil
import sys

VERSION = "1.0"


def printVersion():
    global VERSION
    print "Remove repo file/dir script %s\n" % VERSION
    sys.exit()

def printHelp():
    print "\nRemove repo file/dir script"
    print "Usage: %s [options] src_path\n" % sys.argv[0]
    print "Options:"
    print "  -h, --help\t: show this help message and exit"
    print "  -v, --version\t: show this script version and exit"
    print "  -g, --git\t: also remove .git directory\n"
    sys.exit()

def main():
    try:
        options, arguments = getopt.getopt(sys.argv[1:],
                            "hvg",
                            ("help", "version", "git"))
    except:
        printHelp()

    git = False

    for opt, val in options:
        if opt in ("-h", "--help"):
            printHelp()
        elif opt in ("-v", "--version"):
            printVersion()
        elif opt in ("-g", "--git"):
            git = True

    try:
        src = arguments[0]
    except:
        printHelp()

    for root, dirs, files in os.walk(src):
        if '.repo' in root:
            print "remove "+root
            shutil.rmtree(root)
        if git:
            if '.git' in root:
                print "remove "+root
                shutil.rmtree(root)

if __name__ == '__main__':
    main()

