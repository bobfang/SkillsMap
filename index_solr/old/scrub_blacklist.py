#!/usr/bin/env python

import csv
from collections import namedtuple

blacklist =  set()

with open('blacklist_customers.tsv') as f:
    f_tsv = csv.reader(f, delimiter='\t')
    headings = next(f_tsv)
    #Row = namedtuple('Row', headings)
    for r in f_tsv:
        # Process row
        #row = Row(*r)
        #print(row)
        blacklist.update(r[0])

with open('prospects_resumes.tsv') as f:
    f_tsv = csv.reader(f, delimiter='\t')
    headings = next(f_tsv)
    #Row = namedtuple('Row', headings)
    for r in f_tsv:
        # Process row
        #row = Row(*r)
        #print(row)
        if r[0] in blacklist:
            print('blacklisted')