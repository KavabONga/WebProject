import requests
from bs4 import BeautifulSoup
import re


def ffilter(f, ar):
    return list(filter(f, ar))


def fmap(f, ar):
    return list(map(f, ar))

class TermLink:
    def __init__(self, word, link):
        self.word = word
        self.link = link
    def __str__(self):
        return "{{word={} link=\"{}\"}}".format(self.word, self.link)
class ManyTermsLink:
    def __init__(self, words, link):
        self.words = words
        self.link = link

    def __str__(self):
        return "{{words={} link=\"{}\"}}".format(self.words, self.link)
    def to_term_links(self):
        return [TermLink(w, self.link) for w in self.words]

class Searcher:
    mainApiPage = ""

    # Returns only the singular-word terms
    # (Maybe sometime I'll be able to highlight double-word terms, but i'd need ML for that)
    @staticmethod
    def split_words(line):
        return fmap(lambda x: x.strip(' '), re.split('[\\.,]', line))

    # Returns list of TermLinks extracted from mainApiPage
    @classmethod
    def get_term_links(cls):
        pass
    @classmethod
    def is_word(cls, line):
        return re.match(r'^[а-яА-Я]+$', line)


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
                '/free/6-biologiya/25-slovar_biologicheskih_terminov/stages') and \
            cls.is_word(s.text),
            a_tags
        )
        pre_link = "https://licey.net"
        return fmap(
            lambda a: TermLink(a.text, pre_link + a.get('href')),
            right_tags
        )
    @classmethod
    def get_definition(cls, url):
        dicts = BeautifulSoup(requests.get(url)).findAll("'.")



class GeographySearcher(Searcher):
    mainApiPage="http://www.ecosystema.ru/07referats/slovgeo/index.htm"
    @classmethod
    def get_term_links(cls):
        soup=BeautifulSoup(requests.get(cls.mainApiPage).text, 'html.parser')
        a_tags=soup.findAll("a")
        right_tags=ffilter(
            lambda s: s.get('href') is not None and \
            re.match(r'\d+\.htm', s.get('href')) and \
            cls.is_word(s.text),
            a_tags
        )
        pre_link="http://www.ecosystema.ru/07referats/slovgeo/"
        return fmap(
            lambda s: TermLink(s.text, pre_link + s.get('href')),
            right_tags
        )
class PhysicalSearcher(Searcher):
    mainApiPage='https://ru.wiktionary.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%B7%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5_%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D1%8B/ru'
    @classmethod
    def is_correct_physical_link(cls, a):
        if cls.is_word(a.text) is None:
            return False
        return a.get('href') is not None and \
               a.get('href').startswith('/wiki') and \
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
            lambda a: TermLink(a.text, 'https://ru.wiktionary.org' + a.get('href')),
            links
        )
class AstronomicalSearcher(Searcher):
    mainApiPage = 'http://www.astronet.ru/db/glossary/_e1'
    @classmethod
    def termlinks_from_url(cls, url):
        if url is None:
            return []
        a_list = ffilter(
            lambda a : a.get('href').startswith('/db/msg') and cls.is_word(a.text),
            BeautifulSoup(requests.get(url).content, 'html.parser').findAll('a')
        )
        pre_link = 'http://www.astronet.ru'
        return [TermLink(a.text, pre_link + a.get('href')) for a in a_list]
    @classmethod
    def get_term_links(cls):
        b = BeautifulSoup(requests.get(cls.mainApiPage).content, 'html.parser')
        termlinks = cls.termlinks_from_url(cls.mainApiPage)
        letter_links = ffilter(
            lambda a : len(a.text) == 1 and \
             ord('А') <= ord(a.text) <= ord('Я'),
            b.findAll('a')
        )
        letter_dict = {}
        pre_link = 'http://www.astronet.ru'
        for l in letter_links:
            letter_dict[l.text] = pre_link + l.get('href')
        for k, v in letter_dict.items():
            if k != 'А':
                termlinks += cls.termlinks_from_url(v)
        return termlinks