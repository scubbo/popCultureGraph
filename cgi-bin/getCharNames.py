#!/usr/bin/env python
import sqlite3
import json

print 'Content-type: application/json'
print

def main():
  with sqlite3.connect('/Users/jackjack/Code/popCultureGraph/data.db') as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
  
    query = 'select actorsToCharacters.actorId, charactersToFranchises.franchiseId, characters.name from actors inner join actorsToCharacters on actors.id=actorsToCharacters.actorId inner join charactersToFranchises on actorsToCharacters.charId=charactersToFranchises.charId inner join characters on charactersToFranchises.charId=characters.id'
    c.execute(query)
    data = c.fetchall()
    response = map(lambda x: dict(zip(x.keys(), x)), data)
    print json.dumps({'data':response})

if __name__ == '__main__':
  main()
