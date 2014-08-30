#!/usr/bin/env python
import sqlite3
import cgi
import json

print 'Content-type: application/json'
print

def main():

  form = cgi.FieldStorage()
  requestTable = form['requestTable'].value
  sortByName = form['sortByName'].value.lower() == 'true'

  with sqlite3.connect('/Users/jackjack/Code/popCultureGraph/data.db') as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = 'select * from ' + requestTable
    if sortByName:
     query += ' order by name asc'
    c.execute(query)
    data = c.fetchall()
    response = map(lambda x: dict(zip(x.keys(), x)), data)
    print json.dumps({'data':response})
        

if __name__ == '__main__':
    main()
