#!/usr/bin/env python
import requests
import cgi
import json
from bs4 import BeautifulSoup
from bs4.element import NavigableString

form = cgi.FieldStorage()
baseUrl = 'http://www.imdb.com/find?s=nm&q='

if form and form.has_key('nameGuess'):
  actorName = form['nameGuess'].value
else:
  actorName = 'Nathan Fillion'

fullUrl = baseUrl + actorName

r = requests.get(fullUrl)
soup = BeautifulSoup(r.text)
result = soup.find(class_='findList').find(class_='findResult').find(class_='result_text').find('a')

resultData = {}
resultData['name'] = result.string
resultData['id'] = result.get('href').split('/')[2].replace('nm','')


print 'Content-type: application/json'
print
print json.dumps(resultData)
