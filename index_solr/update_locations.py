#!/usr/bin/env python
# coding=utf-8

#when indexing, use commit=true&separator=%09&escape=\&header=true

import pycurl
import json
import pprint
import time
import solr
import os.path
from io import BytesIO
# github_url = 'https://api.postmarkapp.com/email'

# data = json.dumps({"From": "user@example.com", "To": "receiver@example.com", "Subject": "Pycurl", "TextBody": "Some text"})

# c = pycurl.Curl()
# c.setopt(pycurl.URL, github_url)
# c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
# c.setopt(pycurl.POST, 1)
# c.setopt(pycurl.POSTFIELDS, data)
# c.perform()

port=8983
solr_jobs_base = 'http://localhost:8983/solr/jobdescriptions'
solr_resumes_base = 'http://localhost:8983/solr/resumes'


query = '-job_fips:[* TO *]'
s = solr.Solr(solr_jobs_base)
#(q, fields=None, highlight=None, score=True, sort=None, sort_order="asc", **params)
r = s.select(query, rows=10000)


cols = {'zip' : 1, 'city' : 2, 'state' : 4, 'county': 5}
fips_cols = {'state': 0, 'state_ansi':1, 'county_ansi': 2, 'county_name':3}

# loads a file into a dictionary
def load_file_dict(filename, cols, delim="\t", comment=""):
	lines = {}
	f = filename
	with open(f,'rU') as f:
		for l in f:
			if l[0] == comment: continue
			data = l.split(delim)
			line = []
			lines[data[cols['zip']]] = (data[cols['city']] , data[cols['state']], "" + data[cols['county']].replace(" County", "").replace("(CA)", "Census Area").replace("\xc3\xb1a An", "n") + " County")
	return lines

# loads a file into a dictionary
def load_file_dict_fips(filename, cols, delim=",", comment=""):
	lines = {}
	f = filename
	with open(f,'rU') as f:
		for l in f:
			if l[0] == comment: continue
			data = l.split(delim)
			line = []
			lines[(data[cols['county_name']] , data[cols['state']])] = "" + data[cols['state_ansi']] + data[cols['county_ansi']]
	return lines

print(os.path.abspath('../setup/geonames/usa_zip.tsv'))

zips = load_file_dict(os.path.abspath('../setup/geonames/usa_zip.tsv'), cols)
fips = load_file_dict_fips(os.path.abspath('../setup/geonames/usa_fips.csv'), fips_cols, delim=",", comment="State")
#print(zips)
#print(fips)

print(zips['88011'])


new = []
print(r.numFound)
for job_id in r.results:
	default = 'a'
	#print(type(job_id['job_postal'][0]))
	#print(job_id.get('job_postal', default))
	#print('%s' % (type(zips[job_id['job_postal'][0]])))
	line = {}
	#print(job_id)
	if (job_id.get('job_postal', default) != "a"):
		print(job_id['job_postal'])
		if (zips.get(job_id['job_postal'],default) != "a"):
			if (zips.get(job_id['job_postal'],default) != (job_id.get('job_city', default), job_id.get('job_state',default), job_id.get('job_county',default))):
				# try:
				# 	print('Postal: %s, Old: %s %s New: %s' % (job_id['job_postal'] , job_id['job_city'], job_id['job_state'], zips[job_id['job_postal']]))
				# except KeyError, e:
				# 	print('Postal: %s, New: %s %s %s' % (job_id['job_postal'] , zips[job_id['job_postal']], zips[job_id['job_postal']][1] , zips[job_id['job_postal']][2]))
				#line['job_id'] = job_id['job_id']
				#line['job_city'] = {"set", zips[job_id['job_postal'][0]][0]}
				# line['job_city'] =  zips[job_id['job_postal']][0]
				# line['job_state'] =  zips[job_id['job_postal']][1]
				# line['job_county'] =  zips[job_id['job_postal']][2]
				# line['job_fips'] =  fips.get((line['job_county'], line['job_state']), "")
				# print('FIPS: %s' % (line['job_fips']))
				job_id['job_city'] =  zips[job_id['job_postal']][0]
				job_id['job_state'] =  zips[job_id['job_postal']][1]
				job_id['job_county'] =  zips[job_id['job_postal']][2]
				job_id['job_fips'] =  fips.get((job_id['job_county'], job_id['job_state']), "")
				job_id.pop('score')
				print('FIPS: %s' % (job_id['job_fips']))
				#print(job_id)
				a = s.add(job_id, commit=False)
				#print(a)


c = s.commit(wait_flush=True, wait_searcher=True)
print(c)
d = s.close()
print(d)
print(r.numFound)

# solr_url = 'http://localhost:8983/solr/resumes/dataimport?optimize=false&indent=true&clean=false&commit=true&verbose=false&command=full-import&debug=false&wt=json'
# base_url = 'http://localhost:8983/solr/resumes/dataimport?'
# status_command =  base_url + 'indent=true&command=status&wt=json'
# steps = range(0,7500000,20000)
# for idx in range(0,len(steps)-1):
# 	response = {"status" : 'busy'}
# 	#pprint.pprint(response)
# 	while response["status"] != "idle":
# 		time.sleep(2)
# 		data = BytesIO()
# 		c = pycurl.Curl()
# 		c.setopt(pycurl.URL, status_command)
# 		c.setopt(pycurl.WRITEFUNCTION, data.write)
# 		c.perform()
# 		response = json.loads(data.getvalue())
# 	print('Progress: %s' % (response["statusMessages"]))
# 	print('doing %d to %d' % (steps[idx], (steps[idx+1])))
# 	idx2 = idx + 1
# 	command = solr_url + '&minrun=' + `steps[idx]` + '&maxrun=' + `steps[idx2]`
# 	print(command)
# 	data = BytesIO()

# 	c = pycurl.Curl()
# 	c.setopt(pycurl.URL, command)
# 	c.setopt(pycurl.WRITEFUNCTION, data.write)
# 	c.perform()
# 	response = json.loads(data.getvalue())
# 	