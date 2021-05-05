import spacy
import textacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("What dishes you have in Rice")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
