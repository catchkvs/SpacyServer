from flask import Flask
from flask import request, jsonify
from flask import Response
from flask import json
import numpy as np
import wave
import sys
import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab)


app = Flask(__name__)


@app.route('/phrasematching', methods = ['POST'])
def phraseMatching():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        terms = dataDict["terms"]
        patterns = [nlp.make_doc(text) for text in terms]
        matcher.add("DoNotKnowList", None, *patterns)
        input = dataDict["input"]
        print(patterns)
        print(input)
        doc = nlp(input)
        matches = matcher(doc)
        output = []
        for match_id, start, end in matches:
            span = doc[start:end]
            output.append(span.text)
        outputMap = { "data": output}
        print(outputMap)
        return jsonify(outputMap)
    else:
        return Response()

@app.route('/')
def index():
    return "healthy"

@app.route('/ping')
def ping():
    return "healthy"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
