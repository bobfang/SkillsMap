#!/usr/bin/env python
import pycurl
import json
import pprint
import time
from io import BytesIO
# github_url = 'https://api.postmarkapp.com/email'

# data = json.dumps({"From": "user@example.com", "To": "receiver@example.com", "Subject": "Pycurl", "TextBody": "Some text"})

# c = pycurl.Curl()
# c.setopt(pycurl.URL, github_url)
# c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
# c.setopt(pycurl.POST, 1)
# c.setopt(pycurl.POSTFIELDS, data)
# c.perform()
solr_url = 'http://localhost:8983/solr/resumes/dataimport?optimize=false&indent=true&clean=false&commit=true&verbose=false&command=full-import&debug=false&wt=json'
base_url = 'http://localhost:8983/solr/resumes/dataimport?'
status_command =  base_url + 'indent=true&command=status&wt=json'
steps = range(0,7500000,20000)
for idx in range(0,len(steps)-1):
	response = {"status" : 'busy'}
	#pprint.pprint(response)
	while response["status"] != "idle":
		time.sleep(2)
		data = BytesIO()
		c = pycurl.Curl()
		c.setopt(pycurl.URL, status_command)
		c.setopt(pycurl.WRITEFUNCTION, data.write)
		c.perform()
		response = json.loads(data.getvalue())
	print('Progress: %s' % (response["statusMessages"]))
	print('doing %d to %d' % (steps[idx], (steps[idx+1])))
	idx2 = idx + 1
	command = solr_url + '&minrun=' + `steps[idx]` + '&maxrun=' + `steps[idx2]`
	print(command)
	data = BytesIO()

	c = pycurl.Curl()
	c.setopt(pycurl.URL, command)
	c.setopt(pycurl.WRITEFUNCTION, data.write)
	c.perform()
	response = json.loads(data.getvalue())
	