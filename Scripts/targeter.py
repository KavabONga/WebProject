from Scripts import searchers
from nltk.stem.snowball import RussianStemmer

class Targeter:
    @staticmethod
    def word_root_match(word1, word2, stemmer):
        return stemmer.stem(word1) == stemmer.stem(word2)
    def match_word(self, word):
        pass

class TermListTargeter(Targeter):

    @classmethod
    def to_links_searcher(cls, many_terms_links, stemmer):
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
        return self.bin_find_link(self.stemmer.stem(word))

    def __init__(self, many_terms_links):
        self.stemmer = RussianStemmer()
        self.links_searcher = TermListTargeter.to_links_searcher(many_terms_links, self.stemmer)
