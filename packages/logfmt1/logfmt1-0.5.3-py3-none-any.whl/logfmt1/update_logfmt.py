#!/usr/bin/env python3
# encoding: utf-8
# title: update-logfmt
# description: invoke …/logfmt/share/update/* scripts
# type: virtual
#
# global *.log.fmt update run-parts


import os, re, sys

def main():
    pass

for dir in ["/usr/share/logfmt/update", re.sub("[.\w]+$", "share/update", __file__)]:
    if os.path.exists(dir):
        argv = " ".join(sys.argv[1:])
        os.system(f"run-parts {argv} {dir}")
        break
