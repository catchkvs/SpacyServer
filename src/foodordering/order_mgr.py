from __future__ import unicode_literals
from word2number import w2n
import spacy,en_core_web_sm
import json
import time
from twilio.twiml.messaging_response import MessagingResponse


nlp = spacy.load("en_core_web_sm")

class OrderItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def to_dict(self):
        dest = {
            u'name': self.name,
            u'quantity': self.quantity,
            u'price': self.price
        }
        return dest

class MessageData:
    def __init__(self, To, From, messageSid, fromCity, fromCountry, toCity, toCountry):
        self.toNumber = To
        self.fromNumber = From
        self.messageSid = messageSid
        self.FromCity = fromCity
        self.FromCountry = fromCountry
        self.ToCity = toCity
        self.ToCountry = toCountry

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def to_dict(self):
        dest = {
            u'toNumber': self.toNumber,
            u'fromNumber': self.fromNumber,
            u'messageId': self.messageSid,
            u'fromCity': self.FromCity,
            u'fromCountry': self.FromCountry,
            u'toCity': self.ToCity,
            u'toCountry': self.ToCountry
        }
        return dest


class Order :
    def __init__(self, items, totalAmount, messageData):
        self.items = items
        self.totalAmount = totalAmount
        self.messageData = messageData
        self.creationTime = time.time()
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toTwiML(self, orderid):
        msg = "Your order is: \n"
        msg = msg + "--------------------------------------\n"
        msg = msg + "| Item       Quantity  |\n"
        msg = msg + "--------------------------------------\n"
        for item in self.items:
            msg = msg + item.name + "      "+ str(item.quantity) +"\n"
        msg = msg + "---------------------------------------\n"
        msg = msg + "Your order will be ready in 20 minutes.\n"
      #  msg = msg + "Visit: https://reev.ai/order/"+orderid

        resp = MessagingResponse()
         # Add a message
        resp.message(msg)
        return str(resp)
    def to_dict(self):
        dest = {
            u'items': self.items,
            u'totalAmount': self.totalAmount,
            u'creationTime': self.creationTime,
            u'messageData':self.messageData,
        }
        return dest

def getOrder(text, messageData) :
    doc = nlp(text)
    intent, determiner_tokens = fetchIntent(doc)
    cardinal_tokens = fetchCardinalTokens(doc)
    noun_chunks = list(doc.noun_chunks)
    filtered_chunks = filterNSubjAndPObjNounPhrases(doc, noun_chunks)
    order_items = getOrderItems(filtered_chunks, determiner_tokens, cardinal_tokens)
    order = Order(order_items, "21.99$", messageData)
    return order

def getOrderItems(noun_chunks, determiner_tokens, cardinal_tokens) :
    print("Separating item and quantity")
    order_items = []
    for noun_chunk in noun_chunks:
        chunk_text, quantity = getQuantity(noun_chunk, cardinal_tokens)
        name = removeDeterminers(chunk_text, determiner_tokens)
        item = OrderItem(name, quantity, 9.99)
        order_items.append(item)    
    return order_items

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
    print(getOrder("I want to order a chicken briyani and 1 chicken masala and two tandoori naans", "").toJSON())

if __name__ == "__main__":
    main()