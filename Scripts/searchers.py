import requests
from bs4 import BeautifulSoup
import re

class TermLink:
    def __init__(self, words, link):
        self.words = words
        self.link = link

    def __str__(self):
        return "{words={} link=\"{}\"}".format(self.words, self.link)


class Searcher:
    mainApiPage = ""
    @staticmethod
    def split_words(line):
        return list(map(lambda x: x.strip(' '), re.split('[\.,]', line)))
    @classmethod
    def get_term_links(cls):
        pass


class BiologySearcher(Searcher):
    mainApiPage = "https://licey.net/free/6-biologiya/25-slovar_biologicheskih_terminov.html"

    @classmethod
    def get_term_links(cls):
        soup = BeautifulSoup(requests.get(cls.mainApiPage).text, 'html.parser')
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


class GeographySearcher(Searcher):
    mainApiPage = "http://www.ecosystema.ru/07referats/slovgeo/index.htm"

    def get_term_links(cls):
        soup = BeautifulSoup(requests.get(mainApiPage).text, 'html.parser')
        a_tags = soup.findAll("a")
        right_tags = list(
            filter(
                lambda s: s.get('href') is not None and bool(re.match(r'\d+\.htm', s.get('href'))),
                a_tags
            )
        )
        return list(
            map(
                lambda s: TermLink(
                    re.split(r'[\.,]', s.text),
                    s.get('href')
                )
            )
        )
