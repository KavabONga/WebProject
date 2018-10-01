from Scripts import searchers
from nltk.stem.snowball import RussianStemmer
from requests import get
from bs4 import BeautifulSoup

class Targeter:
    @staticmethod
    def word_root_match(word1, word2, stemmer):
        return stemmer.stem(word1) == stemmer.stem(word2)
    def match_word(self, word):
        return {
            'link' : None,
            'definition' : None
        }

class TermListTargeter(Targeter):

    @staticmethod
    def to_links_searcher(many_terms_links, stemmer):
        term_links = []
        for t in many_terms_links:
            term_links += [(stemmer.stem(tt.word), tt.link) for tt in t.to_term_links()]
        return sorted(term_links)

    def bin_find_link(self, stemmed_word):
        l, r = -1, len(self.links_searcher)
        while r - l > 1:
            m = (r + l) // 2
            if self.links_searcher[m][0] >= stemmed_word:
                r = m
            else:
                l = m
        if r == len(self.links_searcher) or self.links_searcher[r][0] != stemmed_word:
            return None
        else:
            return self.links_searcher[r][1]

    def match_word(self, word):
        return {
            'link' : self.bin_find_link(self.stemmer.stem(word)),
            'definition' : None
        }

    def __init__(self, many_terms_links):
        self.stemmer = RussianStemmer()
        self.links_searcher = TermListTargeter.to_links_searcher(many_terms_links, self.stemmer)

class WikiTargeter(Targeter):
    @staticmethod
    def is_definition_line(line, word):
        first_word = ''.join([c for c in line[line.find(' ')] if (ord('а')<= ord(c) <= ord('я')) or (ord('А')<= ord(c) <= ord('Я'))])
        print(first_word, word)
        return (first_word == word) and len(line.split()) > 2
    def get_url(self, pageid):
        PARAMS = {
            'format' : 'json',
            'action' : 'query',
            'pageids' : pageid,
            'prop' : 'info',
            'inprop' : 'url',
            'utf8':''
        }
        try:
            return get(self.wiki, PARAMS).json()['query']['pages'][str(pageid)]['canonicalurl']
        except:
            return None
    def get_definition(self, word):
        PARAMS = {
            'format' : 'json',
            'utf8' : '',
            'action' : 'parse',
            'page' : word
        }
        lines = BeautifulSoup(get(self.wiki, PARAMS).json()['parse']['text']['*']).findAll('p')[:5]
        for l in lines:
            if WikiTargeter.is_definition_line(l.text, word):
                return l.text
    def search_page(self, word):
        print('Searching for ' + word)
        PARAMS = {
            'format' : 'json',
            'utf8' : '',
            'action' : 'query',
            'list':'prefixsearch',
            'pssearch' : word,
            'pslimit' : 1
        }
        try:
            return get(self.wiki, PARAMS).json()['query']['prefixsearch'][0]
        except:
            return None
    def __init__(self, api='https://ru.wikipedia.org/w/api.php'):
        self.wiki = api
        self.stemmer = RussianStemmer()
    def match_word(self, word):
        page = self.search_page(self.stemmer.stem(word))
        print('Нашёл ' + str(page))
        if page is None:
            return None
        return {
            'link' : self.get_url(page['pageid']),
            'definition' : self.get_definition(page['title'])
        }
