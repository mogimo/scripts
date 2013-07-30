#! /usr/bin/env python
# coding:utf-8

import getopt
import os
import sys
import Image

def printHelp():
    print "\nConvert bitmap dump to bitmap file"
    print "Usage: %s file width height\n" % sys.argv[0]
    print "Parameters:"
    print "  file: bitmap binary dump from MemoryAnalyzer"
    print "  width: graphic width"
    print "  height: graphic height"
    print "Options:"
    print "  -h, --help\t: show this help message and exit\n"
    sys.exit()

#
# 使い方：
#  Eclipse - Memory Analyzer の [dominator tree] から当該 Bitmap クラスを選択し
#  さらにその中の byte[] を選択した上で右クリックし、
#  [Copy]-[Save values to file] を選択してデータを保存する。
#  BitmapクラスのAttributeを見ると画像サイズが表示されているので
# 上記で保存したファイルパスと合わせてこのツールに引数として指定する。
#
def conv(file, width, height):
    outfile = file + ".bmp"
    w = int(width)
    h = int(height)

    f = open(file, "rb")
    out = Image.new("RGB", (w, h))
    data = out.load()
    i = 0
    j = 0
    while True:
        r = ord(f.read(1));
        g = ord(f.read(1));
        b = ord(f.read(1));
        a = ord(f.read(1));
        data[i,j]= (r, g, b)
        i += 1
        if i >= w:
            i = 0
            j += 1
        if j >= h:
            break

    out.save(outfile)
    f.close()

def main():
    try:
        options, arguments = getopt.getopt(sys.argv[1:],
                            "h",
                            ("help"))
    except:
        printHelp()

    for opt, val in options:
        if opt in ("-h", "--help"):
            printHelp()

    try:
        file = arguments[0]
        width = arguments[1]
        height = arguments[2]
    except:
        printHelp()

    conv(file, width, height)

if __name__ == '__main__':
    main()

