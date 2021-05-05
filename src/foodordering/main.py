from __future__ import unicode_literals
from word2number import w2n
import spacy,en_core_web_sm
import json
import time
from twilio.twiml.messaging_response import MessagingResponse


nlp = spacy.load("en_core_web_sm")


def getIntentAndObject(text) :
    doc = nlp(text)
    intent_term, determiner_tokens = fetchIntent(doc)
    get_pps(doc)
    intent_term = fetchIntentFromParseTree(doc)
    cardinal_tokens = fetchCardinalTokens(doc)
    noun_chunks = list(doc.noun_chunks)
    filtered_chunks = filterNSubjAndPObjNounPhrases(doc, noun_chunks)
    intent_objects = getObjects(filtered_chunks, determiner_tokens, cardinal_tokens)
    intent_objects = filterIntentObjects(intent_objects, intent_term)
    intent = {
        "term": intent_term,
        "objects":intent_objects,
    }
    return intent

def getObjects(noun_chunks, determiner_tokens, cardinal_tokens) :
    print("Separating item and quantity")
    object_dic = {}
    for noun_chunk in noun_chunks:
        chunk_text, quantity = getQuantity(noun_chunk, cardinal_tokens)
        name = removeDeterminers(chunk_text, determiner_tokens)
        object_dic[name] = quantity
    return object_dic

def removeDeterminers(name, determiner_tokens) :
    for det_token in determiner_tokens :
        if det_token in name :
            phrase_elements = name.split()
            filteredPhrase = ""
            for element in phrase_elements :
                if element != det_token :
                    if filteredPhrase == "" :
                        filteredPhrase = element
                    else:
                        filteredPhrase = filteredPhrase + " " + element
            return filteredPhrase
    return name

def getQuantity(noun_chunk, cardinal_tokens):
    quantity = 1
    for token in cardinal_tokens :
        if token in noun_chunk.text :
            phrase_elements = noun_chunk.text.split()
            filteredPhrase = ""
            for element in phrase_elements :
                if element != token :
                    if filteredPhrase == "" :
                        filteredPhrase = element
                    else:
                        filteredPhrase = filteredPhrase + " " + element
            return filteredPhrase, w2n.word_to_num(token)
    return noun_chunk.text, quantity

def fetchCardinalTokens(doc) :
    cardinal_token = []
    for ent in doc.ents:
        if ent.label_ == "CARDINAL":
            cardinal_token.append(ent.text)
    return cardinal_token


def filterNSubjAndPObjNounPhrases(doc, noun_chunks):
    print(noun_chunks)
    for token in doc:
        print((token.head.text, token.text, token.dep_, token.pos_))
        if token.dep_ == "nsubj" or token.dep_ == "pobj":
            for chunk in noun_chunks:
                if chunk.text == token.text :
                    noun_chunks.remove(chunk)
    print(noun_chunks)
    return noun_chunks

def filterIntentObjects(intentObj, term):
    output_dic = {}
    for key in intentObj:
        if term in key:
            print("Found intent in object")
        else:
            output_dic[key] = intentObj[key]
    return output_dic
def fetchIntent(doc) :
    intent = ""
    determiner_tokens = []

    for token in doc:
        print((token.head.text, token.text, token.dep_, token.pos_))
        if isDeterminer(token) :
            determiner_tokens.append(token.text)
        if token.pos_ in ("NOUN", "PROPN") and token.dep_ in ("dobj", "pobj") :
            if token.dep_ in ("pobj") and token.head.dep_ in ("prep") :
                print("Token head: " ,token.head.head.text)
                if token.head.head.pos_ in ("VERB"):
                    intent = token.head.head.text
            else :
                if token.head.pos_ in ("VERB") :
                    intent = token.head.text
    return intent, determiner_tokens

def fetchIntentFromParseTree(doc) :
    sentences = list(doc.sents)
    root_token = sentences[0].root
    print(root_token.text, ",", root_token.dep_)
    for child in root_token.children:
        print(child.text, ",", child.dep_)
        if child.dep_ in ('xcomp', 'dobj'):
            return child.text
    return root_token.text

def get_pps(doc):
    pps = []
    for token in doc:
        # Try this with other parts of speech for different subtrees.
        if token.pos_ == 'ADP':
            pp = ' '.join([tok.orth_ for tok in token.subtree])
            pps.append(pp)
    print("preposition phrase: ", pps)
    return pps

# https://nlp.stanford.edu/software/dependencies_manual.pdf    
# The objective is to clean up the noun phrase from the detriminer            
def isDeterminer(token) :
    if token.dep_ in ("det") and token.head.pos_ in ("NOUN" , "PROPN") :
        return True
            
def find_nounphrase_for_token(noun_phrases, token) :
    for phrase in noun_phrases :
        if token in phrase:
            return phrase     

def extract_noun_phrase(doc):
    noun_phrases = []
    for np in doc.noun_chunks:
        noun_phrases.append(np.text)
    return noun_phrases

def main() :
    print(getIntentAndObject("Takeout order a chicken briyani and 1 chicken masala and two tandoori naans"))

if __name__ == "__main__":
    main()