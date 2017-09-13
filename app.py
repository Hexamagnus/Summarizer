import json
import random

from sanic import Sanic
from sanic.response import json as sanic_json, text as sanic_text
from sanic_cors import CORS, cross_origin

from summarizers.frequency_naive import FrequencySummarizer
from summarizers.ner import NERExtractor
from summarizers.syntax_analyzer import SyntaxAnalyzer
from summarizers.frequency_post_tagger import FrequencyPostTagger

app = Sanic(__name__)
# CORS(app)


@app.route("/")
def hello_world(request):
    return sanic_text("Hello world")


@app.route("/freq")
def freq(request):
    data = list()
    for i in range(10):
        data.append({"{}".format(i+1): random.random()})

    return sanic_json(data)


@app.route("/summarize", methods=['POST'])
def summarize(request):
    article = request.form.get("article", "")
    if not article:
        return sanic_json({'status': 'article param required'}, status=202)
    summarizer = FrequencySummarizer(article)
    summarized_text = "\n".join(summarizer.summarize())
    frequency = summarizer.frequency_distributions
    for word, count in frequency.items():
        frequency[word] = count/frequency.N()
    topics = frequency.most_common(5)
    return sanic_json({
        'status': 'OK',
        'article': article,
        'summary': summarized_text,
        'frequency': frequency,
        'topics': topics
    })


@app.route("/ner", methods=['POST'])
def ner(request):
    article = request.form.get("article", "")
    if not article:
        return sanic_json({'status': 'article param required'}, status=202)
    summarizer = NERExtractor(article)
    entities = {x: y for x,y in summarizer.summarize()}
    return sanic_json({
        'status': 'OK',
        'article': article,
        'entities': entities
    })


@app.route("/syntax", methods=['POST'])
def syntax(request):
    article = request.form.get("article", "")
    if not article:
        return sanic_json({'status': 'article param required'}, status=202)
    summarizer = SyntaxAnalyzer(article)
    tree = summarizer.summarize()
    return sanic_json({
        'status': 'OK',
        'article': article,
        'tree': tree
    })


@app.route("/summarize-posttagger/", methods=['POST', 'OPTIONS'])
def summarize_post_tagger(request):
    article = request.form.get("article", "")
    if not article:
        return sanic_json({'status': 'article param required'}, status=202)
    summarizer = FrequencyPostTagger(article)
    summarized_text = "\n".join(summarizer.summarize())
    frequency = summarizer.get_cleaned_frequency()
    for word, count in frequency.items():
        frequency[word] = count/frequency.N()
    topics = frequency.most_common(5)
    return sanic_json({
        'status': 'OK',
        'article': article,
        'summary': summarized_text,
        'frequency': frequency,
        'topics': topics
    })


@app.route("/mind-map/", methods=['POST', 'OPTIONS'])
def mindmap(request):
    article = request.form.get("article", "")
    if not article:
        return sanic_json({'status': 'article param required'}, status=202)
    summarizer = FrequencyPostTagger(article)
    summarizer.summarize()
    frequency = summarizer.get_cleaned_frequency()
    nodes = list()
    for word, count in frequency.items():
        frequency[word] = count / frequency.N()
        nodes.append({
            "text": word,
            "note": frequency[word],
            "nodes": []
        })

    return sanic_json({
        "title": "Palabras importantes",
        "nodes": nodes
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


