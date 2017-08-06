import json
import random

from sanic import Sanic
from sanic.response import json as sanic_json, text as sanic_text

from summarizers.frequency_naive import FrequencySummarizer

app = Sanic(__name__)


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

# if __name__ == '__main__':
app.run(host="0.0.0.0", port=8000, debug=True)

