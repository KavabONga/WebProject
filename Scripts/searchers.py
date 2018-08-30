from requests import get
from bs4 import BeautifulSoup


class TermLink:
    def __init__(self, words, link):
        self.word_matches = word
        self.link = link


class Searcher:
    mainApiPage = ""

    @classmethod
    def get_term_links():
        pass


class BiologySearcher:
    mainApiPage = "https://licey.net/free/6-biologiya/25-slovar_biologicheskih_terminov.html"

    @classmethod
    def get_term_links():
        soup = BeautifulSoup(requests.get(mainApiPage).text, 'html.parser')
        a_tags = soup.findAll('a')
        right_tags = list(
            filter(
                lambda s: s.text.capitalize() == s.text and
                s.get('href') is not None and
                s.get('href').startswith(
                    '/free/6-biologiya/25-slovar_biologicheskih_terminov/stages'),
                a_tags
            )
        )
        return list(
            map(
                lambda a: TermLink(a.text.split(','), a.get('href')),
                right_tags
            )
        )


site = ""
