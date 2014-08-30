#!/usr/bin/env python
import sqlite3
import cgi
import json

print 'Content-type: application/json'
print

def main():

    form = cgi.FieldStorage()
    charName = form['charName'].value

    if form.has_key('actorId'):
        actorId = form['actorId'].value
    else:
        actorName = form['actorName'].value

    if form.has_key('franchiseId'):
        franchiseId = form['franchiseId'].value
    else:
        franchiseName = form['franchiseName'].value

    with sqlite3.connect('/Users/jackjack/Code/popCultureGraph/data.db') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        #TODO Do a check for whether the character exists already

        try:
            c.execute('insert into actors (name) values ("' + actorName + '")')
            actorId = str(c.lastrowid)
        except NameError: #If actorName is not defined
            pass

        try:
            c.execute('insert into franchises (name) values("' + franchiseName + '")')
            franchiseId = str(c.lastrowid)
        except NameError: #If franchiseName is not defined
            pass

        c.execute('insert into characters (name) values("' + charName + '")')
        charId = str(c.lastrowid)

        c.execute('insert into actorsToCharacters (actorId, charId) values (' + actorId + ', ' + charId + ')')
        c.execute('insert into charactersToFranchises (charId, franchiseId) values (' + charId + ', ' + franchiseId + ')')
        c.execute('insert into actorsToFranchises (actorId, franchiseId) values (' + actorId + ', ' + franchiseId + ')')

    print {'status':'SUCCESS'}

        


           #actors = c.fetchall()

           #response = map(lambda x: dict(zip(x.keys(), x)), actors)

           #print json.dumps({'data':response})
        

if __name__ == '__main__':
    main()
