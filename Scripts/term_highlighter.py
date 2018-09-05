from Scripts import searchers, targeter

SEARCHERS = {
    "Biology" : searchers.BiologySearcher,
    "Geography" : searchers.GeographySearcher,
    "Physics" : searchers.PhysicalSearcher
    # TODO: Astronomical searcher, Wikipedia searcher
}

class TermHighlighter:
    @staticmethod
    def highlight_term(word, term_link):
        return "<a href={}><high>{}</high></a>".format(term_link.link, word)
    def __init__(self, modes):
        self.term_links_dict = {k : SEARCHERS[k].get_term_links() for k in modes}
        self.targeter = None
    def use_mode(self, mode):
        self.targeter = targeter.Targeter(self.term_links_dict.get(mode, None))

    def highlight_text(self, text, seps=('\n', ' ', ',', '.', ';', '?', '!', '-', ':')):
        assert self.targeter is not None, "The targeter must be defined"
        for s in seps:
            if s in text:
                return s.join([self.highlight_text(t) for t in text.split(s)])
        term_match = self.targeter.match_word(text)
        if term_match is None:
            return text
        else:
            return TermHighlighter.highlight_term(text, term_match)
