#! /usr/bin/env python
# coding:utf-8

# Make diff between two image files (c) ogino.masanori@sharp.co.jp
# version info:
#    2012/08/01: v1.0 - initial version
#    2013/06/13: v1.1 - automatic switch to save diff-file with alpha or without alpha
#

import getopt
import os
import sys
import Image

VERSION = "1.1"


def printVersion():
    global VERSION
    print "Compares two image files or directories: %s\n" % VERSION
    sys.exit()


def printHelp():
    print "\nCompares two image files or directories\n"
    print "Usage: %s <file1> <file2>" % sys.argv[0]
    print "Usage: %s <dir1> <dir2>" % sys.argv[0]
    print "    note: There must have file with the same name\n"
    print "Options:"
    print "  -h, --help\t: show this help message and exit"
    print "  -v, --version\t: show this script version and exit\n"
    sys.exit()

# file1: old, file2: new
def diff(file1, file2):
    # diff file is created as current/diff/<parent dir of file2>/file2
    path, file = os.path.split(file2)
    grand, parent = os.path.split(path)
    if not os.path.isdir("diff"):
        os.mkdir("diff")
    outpath = os.path.join("diff", parent)
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
    outfile = os.path.join(outpath, file)

    img1 = Image.open(file1)
    img2 = Image.open(file2)

    width1, height1 = img1.size
    width2, height2 = img2.size

    width = max(width1, width2)
    height = max(height1, height2)

    diff = Image.new("RGBA", (width, height))
    diffpix = diff.load()

    pix1 = img1.load()
    pix2 = img2.load()
    
    notSame = False
    
    for i in range(width):
        for j in range(height):
            within1 = (i < width1) and (j < height1)
            within2 = (i < width2) and (j < height2)
            if within1 and within2:
                if pix1[i, j] != pix2[i, j]:
                    diffpix[i, j] =  (255, pix1[i, j][1], pix1[i, j][2], 255)
                    notSame = True
                else:
                    diffpix[i, j] = pix1[i, j]
            elif within1 and (not within2):
                diffpix[i, j] = (0, 255, 0, 255)
                notSame = True
            elif (not within1) and within2:
                diffpix[i, j] = (0, 0, 255, 255)
                notSame = True
            else:
                diffpix[i, j] = (255, 0, 255, 255)
                notSame = True

    if notSame:
        print "different: %s" % outfile
        band = img2.getbands()
        # 32bit depth 
        if ('A' in band):
            out = Image.new("RGBA", (width, height))
            out = Image.blend(img2, diff, 0.5).convert("RGBA")
            out.save(outfile)
        # maybe 24 bit depth, couldn't do aplha-blending
        else:
            diff.save(outfile)
    else:
        print "identical", file2
        outfile = ""

    return outfile

def diffs(old_dir, new_dir):
    for root, dirs, files in os.walk(old_dir):
        for file in files:
            print file
            if ('.png' or '.jpg') in file:
                old_file = os.path.join(old_dir, file)
                new_file = os.path.join(new_dir, file)
                diff(old_file, new_file)

def main():
    try:
        options, arguments = getopt.getopt(sys.argv[1:],
                            "hv",
                            ("help", "version"))
    except:
        printHelp()

    for opt, val in options:
        if opt in ("-h", "--help"):
            printHelp()
        elif opt in ("-v", "--version"):
            printVersion()

    try:
        file1 = arguments[0]
        file2 = arguments[1]
    except:
        printHelp()

    if (os.path.isfile(file1) and os.path.isfile(file2)):
        diff(file1, file2)
    elif (os.path.isdir(file1) and os.path.isdir(file2)):
        diffs(file1, file2)
    else:
        printHelp()

if __name__ == '__main__':
    main()

