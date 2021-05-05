from flask import Flask
from flask import request, jsonify
from flask import Response
from flask import json
from gevent.pywsgi import WSGIServer
from inference.inference import inferenceNER
from foodordering.main import getIntentAndObject
from foodordering.order_mgr import getOrder
from foodordering.order_mgr import MessageData
from foodordering.order_persistence import saveOrder
from spacyapi.main import fetchAttributes
#from inference.inference import similarity
from profilebuilder.profile_extraction import extract_profile
from profilebuilder.project_extraction import extract_project_info
from common.extract_phrases import extract_verb_phrase, extract_noun_phrase
from twilio.twiml.messaging_response import MessagingResponse
import numpy as np
import wave
import sys
import spacy
import os.path

app = Flask(__name__)

@app.route('/experience', methods = ['POST'])
def getExperience():
    if request.method == 'POST':
        data = request.get_data()
        dataDict = json.loads(data)
        profile = extract_profile(dataDict["text"])
        return jsonify(profile)
    else:
        return Response()

@app.route('/project-info', methods = ['POST'])
def getProjectInfo():
    if request.method == 'POST':
        data = request.get_data()
        dataDict = json.loads(data)
        project_info = extract_project_info(dataDict["text"])
        return jsonify(project_info)
    else:
        return Response()


@app.route('/phrase-extraction', methods = ['POST'])
def getPhrases():
    if request.method == 'POST':
        data = request.get_data()
        dataDict = json.loads(data)
        nounPhrase = extract_noun_phrase(dataDict["text"])
        verbPhrase = extract_verb_phrase(dataDict["text"])
        phraseDic = {
            "noun": nounPhrase,
            "verb": verbPhrase
        }
        return jsonify(phraseDic)
    else:
        return Response()

@app.route('/restaurant/intent', methods = ['POST'])
def findIntent() :
    if request.method == 'POST':
        data = request.get_data()
        dataDict = json.loads(data)
        intent = getIntentAndObject(dataDict["text"])
        print(intent)
        return jsonify(intent)
    else:
        return Response()

@app.route('/restaurant/get-order', methods = ['POST'])
def findMultiObjectIntent() :
    if request.method == 'POST':
        data = request.get_data()
        dataDict = json.loads(data)
        print(dataDict)
        messageData = MessageData("chat", "chat", "chat", "chat", "chat", "chat", "chat")
        print(messageData.toJSON())
        order = getOrder(dataDict["text"], messageData)
        print(order.toJSON())
        return order.toJSON()
    else:
        return Response()

@app.route('/twilio/sms-handler', methods = ['GET','POST'])
def twilioSMSHandler() :
    if request.method == 'GET' :
        return "working"
    if request.method == 'POST':
        print(request.values)
        body = request.values.get('Body', None)
        toNum = request.values.get('To', None)
        fromNum = request.values.get('From', None)
        msgSid = request.values.get('MessageSid', None)
        fromCity = request.values.get('FromCity', None)
        fromCountry = request.values.get('FromCountry', None)
        toCity = request.values.get('ToCity', None)
        toCountry = request.values.get('ToCountry', None)
        messageData = MessageData(toNum, fromNum, msgSid, fromCity, fromCountry, toCity, toCountry)
        print(messageData.toJSON())
        print(body)
        order = getOrder(body, messageData)
        order.messageData = messageData.to_dict()
        orderid = saveOrder(order)
        print(orderid)
        print(order.toJSON())
        return order.toTwiML(orderid)
    else:
        return Response()

@app.route('/nlp/attributes', methods = ['POST'])
def fetchNLPAttributes() :
    if request.method == 'POST':
        data = request.get_data()
        dataDict = json.loads(data)
        attributes = fetchAttributes(dataDict["text"])
        return jsonify(attributes)
    else:
        return Response()


@app.route('/', methods = ['GET'])
def home():
    return "healthy"

if __name__ == '__main__':
    app.logger.info("Starting the server...")
    http_server = WSGIServer(('', 1050), app)
    app.logger.info("Server started")
    http_server.serve_forever()
