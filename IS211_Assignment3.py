#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 3 Assignment 3"""

import csv
import argparse
import urllib2
import re

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="Enter a URL linking to a .csv file.")
args = parser.parse_args()

def main():
    """This function takes downloaddata and processdata and puts it into one
    script to run on the command line."""

    if not args.url:
        raise SystemExit
    try:
        data = downloadData(args.url)
    except urllib2.URLError:
        print 'Please enter a valid URL.'
        raise
    else:
        processData(data)
        
def downloadData(url):
    """This function opens a URL link.

    Args:
        url(str): URL to be entered.

    Returns:
        datafile(various): A variable which can be found in the URL.

    Example:
        >>> downloadData('http://s3.amazonaws.com/cuny-is211-spring2015/
        weblog.csv')
        <addinfourl at 3043603788L whose fp = <socket._fileobject object
        at 0xb568436c>>
    """
    datafile = urllib2.urlopen(url)
    return datafile

def processData(datafile):
    """This function processes a URL linked to a .csv file.

    Args:
        datafile(file): A .csv file provided by URL.

    Returns:
        imghits_popbrowser(str): A string

    Example:
        >>> load = downloadData('http://s3.amazonaws.com/cuny-is211-spring2015
        /weblog.csv')
        >>> processData(load)
        processData(load)
        There were 10000 page hits today, image requests account for
        78.77% of hits. 
        Google Chrome has the most hits with 4042.
    """

    readfile = csv.reader(datafile)
    linecount = 0
    imgcount = 0

    chrome = ['Google Chrome', 0]
    ie = ['Internet Explorer', 0]
    safari = ['Safari', 0]
    fox = ['Firefox', 0]
    for line in readfile:
        linecount += 1
        if re.search("firefox", line[2], re.I):
            fox[1] += 1
        elif re.search(r"MSIE", line[2]):
            ie[1] += 1
        elif re.search(r"Chrome", line[2]):
            chrome[1] += 1
        elif re.search(r"Safari", line[2]) and not re.search("Chrome", line[2]):
            safari[1] += 1
        if re.search(r"jpe?g|JPE?G|png|PNG|gif|GIF", line[0]):
            imgcount += 1

    img_hit_pct = (float(imgcount) / linecount) * 100

    brwsr_count = [chrome, ie, safari, fox]

    top_brwsr = 0
    top_name = ' '
    for b in brwsr_count:
        if b[1] > top_brwsr:
            top_brwsr = b[1]
            top_name = b[0]
        else:
            continue

    imghits_popbrowser = ('There were {} page hits today.'
           'Image requests account for {}% of hits.'
           '\n{} has the most hits with {}.').format(linecount,
                                                           img_hit_pct,
                                                           top_name,
                                                           top_brwsr)
    print imghits_popbrowser

if __name__ == '__main__':
    main()
