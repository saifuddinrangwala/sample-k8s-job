#!/usr/bin/env python

import time
import argparse


def dowork(options):
    print "Working on " + options.arg1
    time.sleep(options.wait_time)
    if options.fail:
        exit(1)
    print "Working on " + options.arg2
    time.sleep(options.wait_time)
    print "Finished work"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sample background worker')
    parser.add_argument("-t", "--wait_time", default=5, type=int)
    parser.add_argument("-a", "--arg1", required=True)
    parser.add_argument("-b", "--arg2", required=True )
    parser.add_argument("-f", "--fail", action='store_true', default=False)

    options = parser.parse_args()
    dowork(options)

