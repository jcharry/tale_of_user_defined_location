#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 jamiecharry <jamiecharry@Jamies-Air-2.home>
#
# Distributed under terms of the MIT license.


"""
Server app for Tale of a <UserDefinedPlace>
"""

import sys
sys.path.append('./lib')

import requests
import json
import random
from pprint import pprint

from flask import Flask, url_for, render_template, request
application = Flask((__name__), static_url_path='')

from api_requests import Api_Requests

# import dataset

# db = dataset.connect('sqlite:///:memory:')

# table = db['sometable']
# table.insert(dict(name='John Doe', age=37))
# table.insert(dict(name='Jane Doe', age=34, gender='female'))

# john = table.find_one(name='John Doe')

@application.route('/')
def hello():
    return render_template('index.html')

@application.route('/save', methods=['POST'])
def save():
    print request.json['title']
    print request.json['poem']
    return json.dumps(200)

@application.route('/location', methods=['GET'])
def location():
    print 'hit location path'
    results = {}
    for item in request.args:
        results[item] = request.args.get(item)
        # print item

    # The Api_Requests object expects a customized
    # dictionary, which isn't very flexible
    api_req = Api_Requests(results)
    # print request.args.get('dev') == 'true'
    api_req.dev = request.args.get('dev') == 'true'

    import compose
    if api_req.dev == False:
        api_req.getWeather()
        api_req.getHistoricalArticle()
        api_req.getNyplPhotos()
        api_req.factualSearch()
        api_req.wikipediaSearch()
        api_req.getUNData()
        print 'API RESULTS ====='
        print json.dumps(api_req.results)
        poem = compose.decodeData(jsonData=api_req.results, searchTerm=api_req.searchTerm)
    else:
        print 'DEV === TRUE!!!'
        poem = compose.decodeData(filepath='./db/halifax.json', searchTerm='Downtown Halifax')

    # return json.dumps("error: No data could be found, pick a more populated spot!")

    return json.dumps(poem)
    # return json.dumps({'hi':'hi'})

"""
What kind of data should I try to gather about a place?
    1. Weather
    2. Instagram photos to run through google cloud vision for keywords
    3. Wikipedia entries starting with that title?
    4. Historic events?  
    5. Music related to that place?
    6. Demographics - income, education, race, 
    7. Local foods?
    8. Famous people in teh area?
    9. Common language - greetings?
    10. Books from authors in that area
    11. Nearby points of interests
"""



if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
