import requests
from bs4 import BeautifulSoup
import re

def ffilter(f, ar):
    return list(filter(f, ar))
def fmap(f, ar):
    return list(map(f, ar))

class TermLink:
    def __init__(self, words, link):
        self.words = words
        self.link = link

    def __str__(self):
        return "{words={} link=\"{}\"}".format(self.words, self.link)


class Searcher:
    mainApiPage = ""

    # Returns only the singular-word terms
    # (Maybe sometime I'll be able to highlight double-word terms, but i'd need ML for that)
    @staticmethod
    def split_words(line):
        return ffilter(lambda word: ' ' not in word, fmap(lambda x: x.strip(' '), re.split('[\.,]', line)))

    # Returns list of TermLinks extracted from mainApiPage
    @classmethod
    def get_term_links(cls):
        pass


class BiologySearcher(Searcher):
    mainApiPage = "https://licey.net/free/6-biologiya/25-slovar_biologicheskih_terminov.html"

    @classmethod
    def get_term_links(cls):
        soup = BeautifulSoup(requests.get(cls.mainApiPage).text, 'html.parser')
        a_tags = soup.findAll('a')
        right_tags = ffilter(
            lambda s: s.text.capitalize() == s.text and
            s.get('href') is not None and
            s.get('href').startswith(
                '/free/6-biologiya/25-slovar_biologicheskih_terminov/stages'),
            a_tags
        )
        return fmap
            lambda a: TermLink(split_words(a.text), a.get('href')),
            right_tags
        )


class GeographySearcher(Searcher):
    mainApiPage = "http://www.ecosystema.ru/07referats/slovgeo/index.htm"
    @classmethod
    def get_term_links(cls):
        soup = BeautifulSoup(requests.get(mainApiPage).text, 'html.parser')
        a_tags = soup.findAll("a")
        right_tags = ffilter(
            lambda s: s.get('href') is not None and bool(
                re.match(r'\d+\.htm', s.get('href'))),
            a_tags
        )
        return fmap(
            lambda s: TermLink(split_words(s.text), "http://www.ecosystema.ru/07referats/slovgeo/" + s.get('href')),
            right_tags
        )
