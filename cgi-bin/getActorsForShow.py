#!/usr/bin/env python
import requests
import cgi
import json
from bs4 import BeautifulSoup
from bs4.element import NavigableString

form = cgi.FieldStorage()
baseUrl = 'http://www.imdb.com/title/'#+'tt0303461'

if form and form.has_key('titleId'):
  titleId = form['titleId'].value
else:
  titleId = '0303461'

fullUrl = baseUrl + 'tt' + titleId + '/fullcredits'

r = requests.get(fullUrl)
soup = BeautifulSoup(r.text)
table = soup.find(class_='cast_list')

links = []

for row in table.children:
  if row.name and row.attrs.has_key('class'):
    actorTag = row.find(class_='itemprop')
    
    actorId = actorTag.find('a').attrs['href'].split('/')[2].replace('nm','')
    actorName = actorTag.find('span').text

    characterTag = row.find(class_='character')
    characterName = characterTag.text[:characterTag.text.find('(')-1].strip()

    links.append({'actorId':actorId, 'actorName':actorName, 'characterName':characterName})

print 'Content-type: application/json'
print
print json.dumps(links)
