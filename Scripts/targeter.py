from Scripts import searchers
from nltk.stem.snowball import RussianStemmer
from requests import get
from bs4 import BeautifulSoup
import re

class Targeter:
    many_targeting = False
    @staticmethod
    def word_root_match(word1, word2, stemmer):
        return stemmer.stem(word1) == stemmer.stem(word2)
    def match_word(self, word):
        return {
            'link' : None,
            'definition' : None
        }
    @classmethod
    def targets_many(cls):
        return cls.many_targeting

class TermListTargeter(Targeter):
    many_targeting = False
    @staticmethod
    def to_links_searcher(terms_links, stemmer):
        future_links_searcher = {}
        for t in terms_links:
            future_links_searcher[stemmer.stem(t.word)] = t.link
        return future_links_searcher

    def find_link(self, stemmed_word):
        return self.links_searcher.get(stemmed_word)

    def match_word(self, word):
        found_link = self.find_link(self.stemmer.stem(word))
        if found_link is None:
            return None
        else:
            return {
                'link' : found_link,
                'definition' : None
            }

    def __init__(self, terms_links):
        self.stemmer = RussianStemmer()
        self.links_searcher = TermListTargeter.to_links_searcher(terms_links, self.stemmer)

class WikiTargeter(Targeter):
    many_targeting = False
    def match_word(self, word):
        # print('Searching for ' + word)
        PARAMS = {
            'format' : 'json',
            'utf8' : '',
            'action':'opensearch',
            'search' : word,
            'limit' : 2
        }
        try:
            resp = get(self.wiki, PARAMS).json()
            if resp[2][0].endswith(":"):
                return {
                    'link' : resp[3][1],
                    'definition' : resp[2][1]
                }
            else:
                return {
                    'link' : resp[3][0],
                    'definition' : resp[2][0]
                }
        except:
            return None
    def __init__(self, api='https://ru.wikipedia.org/w/api.php'):
        self.wiki = api
        self.stemmer = RussianStemmer()
class WiktionaryTargeter(Targeter):
    many_targeting = True
    def __init__(self, api='https://ru.wiktionary.org/w/api.php', max_words = 50):
        self.wiktionary = api
        self.max_words = max_words
    def get_links(self, words):
        print(words)
        PARAMS = {
            'action' : 'query',
            'titles' : '|'.join(words),
            'prop' : 'info',
            'inprop' : 'url',
            'format' : 'json'
        }
        resp = get(self.wiktionary, PARAMS).json()['query']['pages']
        word_dict = {}
        for k, v in resp.items():
            if int(k) >= 0:
                word_dict[v['title']] = v.get('fullurl')
        return [word_dict.get(w) for w in words]
    def match_words(self, words):
        words = list(filter(lambda x : re.match(r'^[а-я](([а-я]|\-)+[а-я])?$', x), words))
        links = []
        for i in range(0, len(words), self.max_words):
            links += self.get_links(words[i : i + self.max_words])
        if links is None:
            return links
        else:
            return {words[i] : {'link' : links[i], 'definition' : None} for i in range(len(words)) if links[i] is not None}