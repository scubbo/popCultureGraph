#!/usr/bin/env python
import requests
import cgi
import json
from bs4 import BeautifulSoup
from bs4.element import NavigableString

form = cgi.FieldStorage()
baseUrl = 'http://www.imdb.com/name/'#+'nm0277213/'

if form and form.has_key('actorId'):
  actorId = form['actorId'].value
else:
  actorId = '0688132'

fullUrl = baseUrl + 'nm' + actorId

r = requests.get(fullUrl)
soup = BeautifulSoup(r.text)
actorDiv = soup.find(id='filmo-head-actor')
if not actorDiv:
  actorDiv = soup.find(id='filmo-head-actress') #Seriously, IMDb?

mainDiv = actorDiv.next_sibling.next_sibling

links = []

for franchise in mainDiv.children:
  if franchise.name == u'div' and u'filmo-row' in franchise.attrs['class']:
    franchise.find(class_='year_column').decompose()

    titleBTag = franchise.find('b')
    titleTag = titleBTag.find('a')
    title = titleTag.text.strip()
    titleId = titleTag.get('href').split('/')[2][2:]
    titleBTag.decompose()

    for tag in franchise.children:
      if type(tag) == NavigableString:
        tag.replace_with('')
        next
      if tag.name == u'br':
        tag.decompose()
        break

    for episode in franchise.find_all(class_='filmo-episodes'):
      episode.decompose()

    charName = franchise.text.strip().replace('\n','')

    links.append({'title':title, 'titleId':titleId, 'charName':charName})

print 'Content-type: application/json'
print
print json.dumps(links)
