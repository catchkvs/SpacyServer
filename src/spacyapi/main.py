from __future__ import unicode_literals
import spacy,en_core_web_sm
import textacy

nlp = spacy.load("en_core_web_sm")


def fetchAttributes(text) :
    doc = nlp(text)
    tokens = []
    for token in doc:
        print((token.head.text, token.text, token.dep_, token.pos_))
        tokenNLP = {
            "head": token.head.text,
            "token": token.text,
            "dep":token.dep_,
            "pos":token.pos_,
        }
        tokens.append(tokenNLP)
    return tokens