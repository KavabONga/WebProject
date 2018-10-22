from Scripts import searchers, targeter

SEARCHERS = {
    "Biology" : searchers.BiologySearcher,
    "Geography" : searchers.GeographySearcher,
    "Physics" : searchers.PhysicalSearcher,
    "Astronomy" : searchers.AstronomicalSearcher
    # TODO: Astronomical searcher, Wikipedia searcher
}

class TermHighlighter:
    @staticmethod
    def highlight_term(word, term_link, definition):
        if term_link is None:
            return word
        else:
            if definition is None:
                return "<a href={}><high>{}</high></a>".format(term_link, word)
            else:
                return "<a href={} ><high definition={}>{}</high></a>".format(term_link, definition, word)
    def __init__(self, modes):
        self.searchers_dict = {k : SEARCHERS[k].get_term_links() for k in modes if k in SEARCHERS}
        self.modes = modes
        self.targeter = None
    def use_mode(self, mode):
        if mode in self.searchers_dict:
            self.targeter = targeter.TermListTargeter(self.searchers_dict.get(mode, None))
        elif mode == 'Wiki' and mode in self.modes:
            self.targeter = targeter.WikiTargeter()
        elif mode == 'Wiktionary' and mode in self.modes:
            self.targeter = targeter.WiktionaryTargeter()
    def highlight_text(self, text):
        if self.targeter.targets_many():
            return self.highlight_many(text)
        else:
            return self.highlight_single(text)
    def highlight_single(self, text, seps='.,?!- <>()[]"\'{}#;*:\n\t'):
        for s in seps:
            if s in text:
                return s.join([self.highlight_text(t) for t in text.split(s)])
        parsed_word = self.targeter.match_word(text)
        if parsed_word is None:
            return text
        else:
            return TermHighlighter.highlight_term(text, parsed_word['link'], parsed_word['definition'])
    def highlight_many(self, text):
        form_text, words = TermHighlighter.choose_words(text)
        matches = self.targeter.match_words(words)
        if matches is not None:
            res = []
            for w in words:
                if w in matches:
                    res.append(TermHighlighter.highlight_term(w, matches[w]['link'], matches[w]['definition']))
                else:
                    res.append(w)
            return form_text.format(*res)
        else:
            return text
    @staticmethod
    def choose_words(text, seps='.,?!- <>()[]"\'{}#;*:\n\t'):
        for s in seps:
            if s in text:
                ss, ww = [], []
                for t in text.split(s):
                    chosen = TermHighlighter.choose_words(t)
                    ss.append(chosen[0])
                    ww += chosen[1]
                return (s.join(ss), ww)
        return '{}', [text]
