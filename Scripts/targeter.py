import searchers
from nltk.stem.snowball import RussianStemmer

class Targeter:

    @staticmethod
    def word_root_match(word1, word2, stemmer):
        return stemmer.stem(word1) == stemmer.stem(word2)

    def match_word(self, word):
        for term_link in self.term_links:
            for one_term in term_link.words:
                if word_root_match(one_term, word):
                    return term_link

    def __init__(term_links):
        self.term_links = term_links
        self.stemmer = RussianStemmer()
