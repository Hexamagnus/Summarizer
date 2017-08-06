# Summarizer

This is a simple sanic applications that use 3 major NLP python libraries:

- [NLTK](http://www.nltk.org/)
- [MITIE](https://github.com/mit-nlp/MITIE)
- [Freeling](http://nlp.lsi.upc.edu/freeling/node/1)

To install freeling please use the official documentation at [github](https://github.com/TALP-UPC/FreeLing/tree/master/APIs/python), it could be trickie
 
To verify installation execute
```bash
python tests.py
```

> Requires python 3.5

To run server

```bash
python app.py
```

We expose for major services:

- /summarize: Naive frequency summarization
- /ner: Name Entity Recognition
- /syntax: Syntax tree
- /summarize-posttager: A more clever frequency summarization

All methods require a x-www-form-urlencoded param called article, and the responses 
should return an structure similiar to:

```json
{
  "status": <text>, # Verbose description of transaction status
  "article": <text>, # Text to be summarized
  "summary": <text>, # Text summarized
  "frequency": [
    {
      "word": <text>, # Non stop word
      "frequency": <float> # Relative frequency
    }
  ],
  "topics": [
    <text> # Topic 
  ]
}
```