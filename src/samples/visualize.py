import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("I want to order food")
displacy.serve(doc, style="dep")
