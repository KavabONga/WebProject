from Scripts import searchers
from nltk.stem.snowball import RussianStemmer
from requests import get
from bs4 import BeautifulSoup
import re

def ffilter(f, ar):
    return list(filter(f, ar))


def fmap(f, ar):
    return list(map(f, ar))

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
    @staticmethod
    def only_letters(word):
        return ''.join(ffilter(lambda c : ord(c) >= ord('а') and ord(c) <= ord('я'), word.lower()))
    def match_word(self, word, lim = 5):
        # print('Searching for ' + word)
        PARAMS = {
            'format' : 'json',
            'utf8' : '',
            'action':'opensearch',
            'search' : word,
            'limit' : lim
        }
        resp = get(self.wiki, PARAMS).json()
        print(resp)
        try:
            for i in range(lim):
                if resp[2][i].endswith(':') or len(resp[2][i].split()) <= 1:
                    continue
                res_word = WikiTargeter.only_letters(resp[1][i].split()[0])
                print(word, res_word)
                if self.stemmer.stem(res_word).lower() == self.stemmer.stem(word).lower():
                    return {
                        'definition' : resp[2][i],
                        'link' : resp[3][i]
                    }
            return None
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