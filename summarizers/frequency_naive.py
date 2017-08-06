from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
import logging
from heapq import nlargest
from collections import defaultdict

from . import base

logger = logging.Logger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class FrequencySummarizer(base.BaseSummarizer):
    """
    This class is based on [this](http://glowingpython.blogspot.com.co/2014/09/text-summarization-with-nltk.html) post
    """
    stop_words = set()
    sentences = list()

    _frequency_distributions = None
    _cleaned_text = ""

    @property
    def frequency_distributions(self):
        return self._frequency_distributions

    @frequency_distributions.setter
    def frequency_distributions(self, frecuency_distributions):
        return

    def summarize(self):
        logger.debug("Extracting sentences")
        self.sentences = sent_tokenize(self._text, language='spanish')
        logger.debug("Extracting frequencies")
        self._frequency_distributions = FreqDist(self._cleaned_text)
        ranking = defaultdict(int)
        for i, sentence in enumerate(self.sentences):
            for word in sentence:
                ranking[i] += self._frequency_distributions.freq(word)
        ordered_sentences_by_priority = nlargest(int(len(self.sentences)/10), ranking, key=ranking.get)
        return [self.sentences[i] for i in ordered_sentences_by_priority]

    def __init__(self, text):
        super().__init__(text)
        self.stop_words = set(stopwords.words('spanish') + list(punctuation))
        self._cleaned_text = [x for x in word_tokenize(self.text, language='spanish') if x not in self.stop_words]
