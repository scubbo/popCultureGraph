import requests
from bs4 import BeautifulSoup, NavigableString
from string import Template

FRANCHISE_URL_TEMPLATE = Template('https://www.imdb.com/title/tt$ID/fullcredits')
ACTOR_URL_TEMPLATE = Template('https://www.imdb.com/name/nm$ID')
STARTUP_URL_TEMPLATE = Template('https://www.imdb.com/find?q=$NAME')

ENTRIES_PER_CHUNK = 3

class DataFetcher(object):

    def get_actors_for_franchise(self, franchiseId, chunkNum):
        soup = BeautifulSoup(requests.get(FRANCHISE_URL_TEMPLATE.substitute(ID=franchiseId)).text, 'lxml')
        rows = soup.select('table.cast_list tr')

        filtered_rows = [row for row in rows if self._row_is_an_actor_row(row)]
        transformed_rows = [self._get_data_from_actor_row(row) for row in filtered_rows]
        chunk = transformed_rows[chunkNum * ENTRIES_PER_CHUNK:(chunkNum + 1)*ENTRIES_PER_CHUNK]
        return {
            'request': {
                'type': 'actors_for_franchise',
                'id': franchiseId
            },
            'response': chunk
        }

    def get_franchises_for_actor(self, actorId, chunkNum):
        soup = BeautifulSoup(requests.get(ACTOR_URL_TEMPLATE.substitute(ID=actorId)).text, 'lxml')
        rows = soup.select('#filmo-head-actor + div.filmo-category-section div.filmo-row')
        transformed_rows = [self._get_data_from_franchise_row(row) for row in rows]
        chunk = transformed_rows[chunkNum * ENTRIES_PER_CHUNK:(chunkNum + 1) * ENTRIES_PER_CHUNK]

        # TODO: filter out (or differently represent) the rows that are not movies or TV Shows (e.g. game shows)
        return {
            'request': {
                'type': 'franchises_for_actor',
                'id': actorId
            },
            'response': chunk
        }

    def get_id(self, type, name):
        if type == 'actor':
            return self._get_id_for_actor(name)
        if type == 'franchise':
            raise Exception
        raise Exception

    def _get_data_from_actor_row(self, row):
        actor_link = self._get_actor_link_from_row(row)
        return {
            'id': actor_link['href'].split('/')[2][2:],
            'name': str(actor_link.contents[0]).strip(),
            # TODO - this probably needs tweaking to remove noise like "(uncredited)"
            'char_name': str(row.select('td.character')[0].contents[0]).strip()
        }

    def _get_data_from_franchise_row(self, row):
        franchise_link = self._get_franchise_link_from_row(row)
        return {
            'id': franchise_link['href'].split('/')[2][2:],
            'name': str(franchise_link.contents[0]).strip(),
            'char_name': self._get_char_name_from_franchise_row(row)
        }

    @staticmethod
    def _get_id_for_actor(name):
        soup = BeautifulSoup(requests.get(STARTUP_URL_TEMPLATE.substitute(NAME=name)).text, 'lxml')
        link = soup.select('h3.findSectionHeader a[name="nm"]')[0].parent.parent.select('table tr')[0].select('a')[1]
        return link['href'].split('/')[2][2:]

    @staticmethod
    def _row_is_an_actor_row(row):
        try:
            clazz = row['class']
        except KeyError:
            return False
        return ('odd' in clazz or 'even' in clazz) and ('display:none' not in row.td.get('style', ''))

    @staticmethod
    def _get_actor_link_from_row(row):
        # https://stackoverflow.com/a/9868665/1040915
        # This could also have been `for link in row.find_all('a'): if <cond>: break; return link`, but that's pretty yucky
        return next(link for link in row.find_all('a') if
                    hasattr(link, 'href') and
                    link['href'].startswith('/name/') and
                    len(link.contents) and
                    type(link.contents[0]) == NavigableString)

    @staticmethod
    def _get_franchise_link_from_row(row):
        return row.select('b a')[0]

    @staticmethod
    def _get_char_name_from_franchise_row(row):
        # Return the stripped-string of the 2nd child with non-whitespace contents
        non_whitespace_children =\
            [child for child in row.children if type(child) == NavigableString and not child.string.isspace()]
        try:
            return non_whitespace_children[1].string.strip()
        except IndexError:
            return ''
