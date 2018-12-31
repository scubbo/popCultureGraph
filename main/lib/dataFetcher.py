import requests
from bs4 import BeautifulSoup, NavigableString
from string import Template

FRANCHISE_URL_TEMPLATE = Template('https://www.imdb.com/title/tt$ID/fullcredits')
ACTOR_URL_TEMPLATE = Template('https://www.imdb.com/name/nm$ID')


class DataFetcher(object):

    def get_actors_for_franchise(self, franchiseId):
        soup = BeautifulSoup(requests.get(FRANCHISE_URL_TEMPLATE.substitute(ID=franchiseId)).text, 'lxml')
        rows = soup.select('table.cast_list tr')

        return [self._get_data_from_actor_row(row) for row in rows if self._row_is_an_actor_row(row)]

    def get_franchises_for_actor(self, actorId):
        soup = BeautifulSoup(requests.get(ACTOR_URL_TEMPLATE.substitute(ID=actorId)).text, 'lxml')
        rows = soup.select('#filmo-head-actor + div.filmo-category-section div.filmo-row')

        # TODO: filter out (or differently represent) the rows that are not movies or TV Shows (e.g. game shows)
        return [self._get_data_from_franchise_row(row) for row in rows]

    def _get_data_from_actor_row(self, row):
        actor_link = self._get_actor_link_from_row(row)
        return {
            'id': actor_link['href'].split('/')[2][2:],
            'actor_name': str(actor_link.contents[0]).strip(),
            # TODO - this probably needs tweaking to remove noise like "(uncredited)"
            'char_name': str(row.select('td.character')[0].contents[0]).strip()
        }

    def _get_data_from_franchise_row(self, row):
        franchise_link = self._get_franchise_link_from_row(row)
        return {
            'id': franchise_link['href'].split('/')[2][2:],
            'franchise_name': str(franchise_link.contents[0]).strip(),
            'char_name': self._get_char_name_from_franchise_row(row)
        }

    @staticmethod
    def _row_is_an_actor_row(row):
        try:
            clazz = row['class']
            return 'odd' in clazz or 'even' in clazz
        except KeyError:
            return False

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
