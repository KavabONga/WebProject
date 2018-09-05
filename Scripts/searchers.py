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
        return "{{words={} link=\"{}\"}}".format(self.words, self.link)


class Searcher:
    mainApiPage = ""

    # Returns only the singular-word terms
    # (Maybe sometime I'll be able to highlight double-word terms, but i'd need ML for that)
    @staticmethod
    def split_words(line):
        return fmap(lambda x: x.strip(' '), re.split('[\.,]', line))

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
            lambda s: s.text.capitalize() == s.text and \
            s.get('href') is not None and \
            s.get('href').startswith(
                '/free/6-biologiya/25-slovar_biologicheskih_terminov/stages'),
            a_tags
        )
        pre_link = "https://licey.net"
        return fmap(
            lambda a: TermLink(cls.split_words(a.text), pre_link + a.get('href')),
            right_tags
        )


class GeographySearcher(Searcher):
    mainApiPage="http://www.ecosystema.ru/07referats/slovgeo/index.htm"
    @classmethod
    def get_term_links(cls):
        soup=BeautifulSoup(requests.get(cls.mainApiPage).text, 'html.parser')
        a_tags=soup.findAll("a")
        right_tags=ffilter(
            lambda s: s.get('href') is not None and bool(
                re.match(r'\d+\.htm', s.get('href'))),
            a_tags
        )
        pre_link="http://www.ecosystema.ru/07referats/slovgeo/"
        return fmap(
            lambda s: TermLink(cls.split_words(s.text), pre_link + s.get('href')),
            right_tags
        )
class PhysicalSearcher(Searcher):
    mainApiPage='https://ru.wiktionary.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%B7%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5_%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D1%8B/ru'
    @classmethod
    def is_correct_physical_link(cls, a):
        r=re.match(r'[а-я]+', a.text)
        if r is None:
            return False
        l=r.end() - r.start()
        return a.get('href') is not None and \
               a.get('href').startswith('/wiki') and \
               l == len(a.text) and \
               a.get('class') is None
    @classmethod
    def is_link_to_next(cls, a):
        return a.text == "Следующая страница"
    @classmethod
    def get_next_physical_links(cls, page):
        soup = BeautifulSoup(requests.get(page).text, 'html.parser')
        a_tags = soup.findAll('a')
        right_tags = ffilter(cls.is_correct_physical_link, a_tags)
        link_next = ffilter(cls.is_link_to_next, a_tags)
        if len(link_next) > 0:
            return right_tags + cls.get_next_physical_links('https://ru.wiktionary.org' + link_next[0].get('href'))
        else:
            return right_tags
    @classmethod
    def get_term_links(cls):
        links = cls.get_next_physical_links(cls.mainApiPage)
        return fmap(
            lambda a: TermLink(cls.split_words(a.text), 'https://ru.wiktionary.org' + a.get('href')),
            links
        )
