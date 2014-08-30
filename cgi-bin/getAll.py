#!/usr/bin/env python
import sqlite3
import json

print 'Content-type: application/json'
print

def main():

  response = {}

  with sqlite3.connect('/Users/jackjack/Code/popCultureGraph/data.db') as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('select actors.id as actorId, actors.name as actorName, characters.name as charName, franchises.id as franchiseId, franchises.name as franchiseName from actors inner join actorsToCharacters on actors.id=actorsToCharacters.actorId inner join characters on actorsToCharacters.charId=characters.id inner join charactersToFranchises on charactersToFranchises.charId=actorsToCharacters.charId inner join franchises on charactersToFranchises.franchiseId=franchises.id where actors.id in (select max(actorId) from actorsToCharacters group by actorId having count(charId) > 1) and franchises.id in (select max(franchiseId) from charactersToFranchises group by franchiseId having count(charId) > 1)')

    data = c.fetchall()

    response['data'] = map(lambda x: dict(zip(x.keys(), x)), data)

    print json.dumps(response)
        

if __name__ == '__main__':
    main()
