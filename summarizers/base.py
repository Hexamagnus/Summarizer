import abc


class BaseSummarizer(object, metaclass=abc.ABCMeta):

    _text = ""

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def __init__(self, text):
        self._text = text

    @abc.abstractmethod
    def summarize(self):
        raise NotImplemented
