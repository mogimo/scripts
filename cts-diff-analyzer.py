#! /usr/bin/env python
# coding:utf-8

# CTS git-diff analyzer (c) ogino.masanori@sharp.co.jp
# version info:
#    2012/07/17: v1.0 - initial version
#

import getopt
import os
import re
import sys

VERSION = "1.0"
COUNT = False
NEWFILE = False
DELFILE = False
MODFILE = False
ADDTEST = False
REMTEST = False
WIKI = False

NEWFILE_COUNTER = 0
DELFILE_COUNTER = 0
MODFILE_COUNTER = 0
ADDTEST_COUNTER = 0
REMTEST_COUNTER = 0

CURRENT_PACKAGE = ""
CURRENT_TESTFILE = ""
PREV_PACKAGE = ""
PREV_TESTFILE = ""
DELETE_TEST = ""

def printCount():
    print "new file = %s" % NEWFILE_COUNTER
    print "del file = %s" % DELFILE_COUNTER
    print "mod file = %s" % MODFILE_COUNTER
    print "add test = %s" % ADDTEST_COUNTER
    print "del test = %s" % REMTEST_COUNTER

def printVersion():
    global VERSION
    print "CTS diff analyzer version %s\n" % VERSION
    sys.exit()

def printHelp():
    print "\nCTS diff analyzer for git-diff"
    print "Usage: %s [options] git_diff_file\n" % sys.argv[0]
    print "Options:"
    print "  -h, --help\t\tshow this help message and exit"
    print "  -v, --version\t\tshow this script version and exit"
    print "  Print Options:"
    print "    -c, --count\t\tonly count the changes"
    print "    -n, --new\t\tshow newly added files"
    print "    -d, --deleted\tshow deleted files"
    print "    -m, --modified\tshow modified files"
    print "    -a, --added\t\tshow added testcases"
    print "    -r, --removed\tshow removed testcases"
    print "    -w, --wiki\t\tshow added testcases with redmine wiki format"
    print "\t\t\tnote: ignore other options\n"
    sys.exit()

def fileList(f, line):
    global NEWFILE_COUNTER, DELFILE_COUNTER, MODFILE_COUNTER, CURRENT_PACKAGE, CURRENT_TESTFILE
    # diff --git a/filepath b/filepath
    # [new file mode ...]
    # index xxxxx...yyyyyy zzzzz
    # --- [a/filepath|/dev/null]
    # +++ [b/filepath|/dev/null]
    #
    # or
    #
    # diff --git a/filepath b/filepath
    # [new file mode ...]
    # index xxxxx...yyyyyy zzzzz
    # Binary files hogehoge and hogehoge    
    diff_file = re.compile("diff --git a/(.+) b/(.+)")
    before = re.compile("--- [a/|*](.+)")
    after  = re.compile(r"\+\+\+ (.+)")
    binary = re.compile("Binary files", re.I)
    devnull = re.compile("/dev/null")
    testfile = re.compile("/tests/tests/(\w+)/.+/(\w+\.java)")
    
    diff_file_match = diff_file.match(line) # got "diff --git" line
    if diff_file_match:
        mod = 0
        while True:
            line = f.readline()
            before_match = before.match(line)
            after_match = after.match(line)
            if before_match: # got "--- hogehoge"
                if devnull.search(line):
                    # a is null --> new file
                    if NEWFILE:
                        print "[new file]\t%s" % diff_file_match.group(1)
                    NEWFILE_COUNTER += 1
                else:
                    mod = 1
            elif after_match: # got "+++ hogehoge"
                if devnull.search(line):
                    # b is null --> deleted file
                    if DELFILE:
                        print "[del file]\t%s" % diff_file_match.group(1)
                    DELFILE_COUNTER += 1
                else:
                    # find "hogehoge" in "/tests/tests/hogehoge/"
                    testfile_match = testfile.search(line)
                    if testfile_match:
                        CURRENT_PACKAGE = testfile_match.group(1)
                        CURRENT_TESTFILE = testfile_match.group(2)
                    if mod == 1:
                        # a and b are not null --> modified file
                        if MODFILE:
                            print "[mod file]\t%s" % diff_file_match.group(1)
                        MODFILE_COUNTER += 1
                break # exit loop
            elif binary.search(line): # this is binary file, just ignore!
                break
            else:
                continue

def testCaseList(f, line):
    global ADDTEST_COUNTER, REMTEST_COUNTER, WIKI, CURRENT_TESTFILE, PREV_TESTFILE, CURRENT_PACKAGE, PREV_PACKAGE, DELETE_TEST
    # find the following format string
    # +    public void testXxxxxxx()
    # or
    # -    public void tsetXxxxxxx()
    add = re.compile(r"\+[ \t]+public[ \t]+void[ \t]+(test\w+)")
    delete = re.compile(r"-[ \t]+public[ \t]+void[ \t]+(test\w+)")

    add_match = add.match(line)
    del_match = delete.match(line)
    
    if add_match:
        add_test = add_match.group(1)
        if ADDTEST:
            if NEWFILE or DELFILE or MODFILE:
                print "\t\t",
            print "[add test]\t%s" % add_test
        if WIKI:
            if not add_test in DELETE_TEST:
                if CURRENT_PACKAGE != PREV_PACKAGE:
                    print "\nh3. %s\n" % CURRENT_PACKAGE
                    PREV_PACKAGE = CURRENT_PACKAGE
                if CURRENT_TESTFILE != PREV_TESTFILE:
                    print "* %s" % CURRENT_TESTFILE
                    PREV_TESTFILE = CURRENT_TESTFILE
                print "** %s" % add_test

        ADDTEST_COUNTER += 1
    elif del_match:
        del_test = del_match.group(1)
        DELETE_TEST = del_test
        if REMTEST:
            if NEWFILE or DELFILE or MODFILE:
                print "\t\t",
            print "[del test]\t%s" % del_test
        REMTEST_COUNTER += 1

def showProgress(index):
    parts = ("|", "/", "-", "\\")
    moment = parts[index%4]
    print "\r"+moment,
        
def fileReader(filename):
    f = open(filename, "r")
    
    while True:
        line = f.readline()
        if not line: # maybe EOF! exit loop
            return

        fileList(f, line)
        testCaseList(f, line)
            
def main():
    global COUNT, NEWFILE, DELFILE, MODFILE, ADDTEST, REMTEST, WIKI
    options, arguments = getopt.getopt(sys.argv[1:],
                            "hvcndmarw",
                            ("help", "version", "count", "new", "deleted", 
                            "modified", "added", "removed", "wiki"))
    if not options:
        NEWFILE = True
        DELFILE = True
        MODFILE = True
        ADDTEST = True
        REMTEST = True

    for opt, val in options:
        if opt in ("-h", "--help"):
            printHelp()
        elif opt in ("-v", "--version"):
            printVersion()
        elif opt in ("-c", "--count"):
            COUNT = True
        elif opt in ("-n", "--new"):
            NEWFILE = True
        elif opt in ("-d", "--deleted"):
            DELFILE = True
        elif opt in ("-m", "--modified"):
            MODFILE = True
        elif opt in ("-a", "--added"):
            ADDTEST = True
        elif opt in ("-r", "--removed"):
            REMTEST = True
        elif opt in ("-w", "--wiki"):
            WIKI = True
            NEWFILE = False
            DELFILE = False
            MODFILE = False
            ADDTEST = False
            REMTEST = False
            break            

    try:
        filename = arguments[0]
        if not filename:
            printHelp()
    except:
        printHelp()

    fileReader(filename)
    
    if COUNT:
        print "\r",
        printCount()

if __name__ == '__main__':
    main()

