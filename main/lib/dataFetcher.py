import requests
from bs4 import BeautifulSoup, NavigableString
from string import Template

URL_TEMPLATE = Template('https://www.imdb.com/title/tt$ID/fullcredits')


class DataFetcher(object):

    def get_actors_for_franchise(self, franchiseId):
        soup = BeautifulSoup(requests.get(URL_TEMPLATE.substitute(ID=franchiseId)).text, 'lxml')
        rows = soup.select('table.cast_list tr')

        return [self._get_data_from_row(row) for row in rows if self._row_is_an_actor_row(row)]

    def _get_data_from_row(self, row):
        actor_link = self._get_actor_link_from_row(row)
        return {
            'id': actor_link['href'].split('/')[2][2:],
            'actor_name': str(actor_link.contents[0]).strip(),
            # TODO - this probably needs tweaking to remove noise like "(uncredited)"
            'char_name': str(row.select('td.character')[0].contents[0]).strip()
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
