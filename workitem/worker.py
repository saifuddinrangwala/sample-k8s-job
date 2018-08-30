#!/usr/bin/env python

import time
import argparse


def dowork(options):
    print "Working on " + options.arg1
    time.sleep(5)
    print "Working on " + options.arg2
    time.sleep(5)
    print "Finished work"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sample background worker')
    parser.add_argument("-a", "--arg1", required=True)
    parser.add_argument("-b", "--arg2", required=True )

    options = parser.parse_args()
    dowork(options)

