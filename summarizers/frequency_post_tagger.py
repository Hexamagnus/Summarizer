from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
import logging
from heapq import nlargest
from collections import defaultdict
import freeling

from . import frequency_naive


logger = logging.Logger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


FREELINGDIR = "/usr/local"

DATA = FREELINGDIR + "/share/freeling/"
LANG = "es"


class FrequencyPostTagger(frequency_naive.FrequencySummarizer):

    def summarize(self):
        logger.debug("Extracting sentences")
        self.sentences = sent_tokenize(self._text, language='spanish')
        logger.debug("Extracting frequencies")
        self._frequency_distributions = FreqDist(self._cleaned_text)
        ranking = defaultdict(int)
        for i, sentence in enumerate(self.sentences):
            for word in sentence:
                scale_factor = 1
                tag = word.split("-")
                if len(tag) > 1:
                    tag = tag[1]
                    if tag.startswith("A"):
                        # Adjective
                        scale_factor = 1.4
                    elif tag.startswith("R"):
                        # Adverb
                        scale_factor = 1.1
                    elif tag.startswith("D"):
                        # Determinant
                        scale_factor = 0.9
                    elif tag.startswith("N"):
                        # Noun
                        scale_factor = 2.2
                    elif tag.startswith("V"):
                        # Verb
                        scale_factor = 1.6
                    elif tag.startswith("P"):
                        # Pronoun
                        scale_factor = 1.1
                    elif tag.startswith("Z"):
                        # Number
                        scale_factor = 1.5
                    elif tag.startswith("W"):
                        # Date
                        scale_factor = 1.5

                ranking[i] += self._frequency_distributions.freq(word) * scale_factor
        ordered_sentences_by_priority = nlargest(int(len(self.sentences)/10) + 1, ranking, key=ranking.get)
        return [self.sentences[i] for i in ordered_sentences_by_priority]

    def __init__(self, text):
        super().__init__(text)
        self.stop_words = set(stopwords.words('spanish') + list(punctuation))
        self._cleaned_text = list()
        freeling.util_init_locale("default")

        # create language analyzer
        la = freeling.lang_ident(DATA + "common/lang_ident/ident.dat")

        # create options set for maco analyzer. Default values are Ok, except for data files.
        op = freeling.maco_options("es")
        op.set_data_files("",
                          DATA + "common/punct.dat",
                          DATA + LANG + "/dicc.src",
                          DATA + LANG + "/afixos.dat",
                          "",
                          DATA + LANG + "/locucions.dat",
                          DATA + LANG + "/np.dat",
                          DATA + LANG + "/quantities.dat",
                          DATA + LANG + "/probabilitats.dat")

        # create analyzers
        tk = freeling.tokenizer(DATA + LANG + "/tokenizer.dat")
        sp = freeling.splitter(DATA + LANG + "/splitter.dat")
        sid = sp.open_session()
        mf = freeling.maco(op)

        # activate mmorpho odules to be used in next call
        mf.set_active_options(True, True, True, True,  # select which among created
                              True, True, True, True,  # submodules are to be used.
                              True, True, True, True)  # default: all created submodules are used

        # create tagger, sense anotator, and parsers
        tg = freeling.hmm_tagger(DATA + LANG + "/tagger.dat", True, 2)
        sen = freeling.senses(DATA + LANG + "/senses.dat")
        parser = freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")

        l = tk.tokenize(self.text)
        ls = sp.split(sid, l, False)

        ls = mf.analyze(ls)
        ls = tg.analyze(ls)
        ls = sen.analyze(ls)
        ls = parser.analyze(ls)

        for s in ls:
            ws = s.get_words()
            for w in ws:
                # Removing all stopped words, including prepositions, conjunctions, interjections and punctuation
                tag = w.get_tag()
                word = w.get_form()
                if tag.startswith("S") or \
                    tag.startswith("I") or \
                    tag.startswith("C") or \
                    tag.startswith("F") or \
                    tag.startswith("D") or \
                    tag.startswith("P"):
                    pass
                else:
                    self._cleaned_text.append("{}-{}".format(word, tag))

    def get_cleaned_frequency(self):
        new_frequency = FreqDist()
        for word, count in self._frequency_distributions.items():
            new_frequency[word.split("-")[0]] = count
        return new_frequency
