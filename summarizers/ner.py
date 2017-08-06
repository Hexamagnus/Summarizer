import sys

from mitie import *
from nltk.probability import FreqDist

from . import base

sys.path.append("/Users/ma0/Desktop/contraslash/projects/m_assistant/MITIE/mitielib")


class NERExtractor(base.BaseSummarizer):
    """
    Based on [official example](https://github.com/mit-nlp/MITIE/blob/master/examples/python/ner.py)
    """

    ner = None

    def __init__(self, text):
        super().__init__(text)

        self.ner = named_entity_extractor(
            '/Users/ma0/Desktop/contraslash/projects/m_assistant/MITIE/MITIE-models/spanish/ner_model.dat'
        )

    def summarize(self):
        tokens = tokenize(self.text)

        entities = self.ner.extract_entities(tokens)

        entities_text = list()

        for e in entities:
            range = e[0]
            tag = e[1]
            score = e[2]
            score_text = "{:0.3f}".format(score)
            entity_text = " ".join(tokens[i].decode() for i in range)
            # print("   Score: " + score_text + ": " + tag + ": " + entity_text)
            entities_text.append(entity_text)
        frequency_distribution = FreqDist(entities_text)
        return frequency_distribution.most_common(5)