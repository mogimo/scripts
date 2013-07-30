#! /usr/bin/env python
# coding:utf-8

import os
import sys
import re

def print_help():
    print "Automatically git cherry-pick by specified git log file"
    print "Usage; %s <git-log file>" % sys.argv[0]
    sys.exit()

def main():
    try:
        file = sys.argv[1]
    except:
        print_help()

    pattern = re.compile("commit ")
    if (os.path.isfile(file)):
        f = open(file, "r")
        lines = f.readlines()
        for line in reversed(lines):
            if pattern.match(line):
                # retrieve commit hash value from log
                value = pattern.sub("", line)
                print("git cherry-pick " + value)
                if os.system("git cherry-pick " + value) != 0:
                    # stop the loop if an error occurs
                    break;

if __name__ == '__main__':
    main()