import unittest
import codecs


class TestFrequencySummarizer(unittest.TestCase):

    sample_file_names = [
        'socrates.txt',
    ]
    sample_file_texts = list()

    def setUp(self):
        for name_of_file in self.sample_file_names:
            file_to_open = codecs.open(name_of_file)
            text_of_file = "\n".join(file_to_open.readlines())
            self.sample_file_texts.append(text_of_file)

    def test_naive_summarization(self):
        """
        Just for check everything is working
        :return: 
        """
        from summarizers.frequency_naive import FrequencySummarizer
        for text in self.sample_file_texts:
            frequency_summarizer = FrequencySummarizer(text)
            print(frequency_summarizer.summarize())


class TestNER(unittest.TestCase):
    sample_file_names = [
        'socrates.txt',
    ]
    sample_file_texts = list()

    def setUp(self):
        for name_of_file in self.sample_file_names:
            file_to_open = codecs.open(name_of_file)
            text_of_file = "\n".join(file_to_open.readlines())
            self.sample_file_texts.append(text_of_file)

    def test_naive_summarization(self):
        """
        Just for check everything is working
        :return: 
        """
        from summarizers.ner import NERExtractor
        for text in self.sample_file_texts:
            frequency_summarizer = NERExtractor(text)
            print(frequency_summarizer.summarize())


class TestSyntaxAnalyzer(unittest.TestCase):
    sample_file_names = [
        'socrates.txt',
    ]
    sample_file_texts = list()

    def setUp(self):
        for name_of_file in self.sample_file_names:
            file_to_open = codecs.open(name_of_file)
            text_of_file = "\n".join(file_to_open.readlines())
            self.sample_file_texts.append(text_of_file)

    def test_naive_summarization(self):
        """
        Just for check everything is working
        :return: 
        """
        from summarizers.syntax_analyzer import SyntaxAnalyzer
        for text in self.sample_file_texts:
            frequency_summarizer = SyntaxAnalyzer(text)
            print(frequency_summarizer.summarize())

if __name__ == '__main__':
    unittest.main()
