#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 jamiecharry <jamiecharry@Jamies-Air-2.home>
#
# Distributed under terms of the MIT license.

"""

"""

import requests
import json
import random
from pprint import pprint
import argparse
import base64   # Google cloud vision takes base64 strings
import httplib2 
import urllib   # Use to download and save photos when I know the photo url
import wikipedia    # Wikipedia API wrapper

# Factual API
from factual import Factual
from factual.utils import circle


# Shelf is used for local database storage
# Dictionary like storage
import shelve

# Google image analysis
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

class Api_Requests(object):
    def __init__(self, location):
        self.dev = True
        self.location = location
        print self.location
        self.searchTerm = None
        self.getSearchTerm()
        self.results = {'place': self.formatTitle(self.searchTerm)}

        # Load API credentials
        with open('creds/cred.json') as f:
            self.creds = json.load(f)
            f.close()

        # Initialize factual
        self._factual = Factual(self.creds['FACTUAL_API_KEY'], self.creds['FACTUAL_API_SECRET'])
        self._places = self._factual.table('places')

    def formatTitle(self, s):
        s = s.strip()
        s = list(s)
        for index in range(len(s)):
            if s[index] == ' ' or s[index] == '-':
                s[index] = '_'
        s = ''.join(s)
        s = '<span>&lt' + s.lower() + '&gt</span>\n'
        return s
            
    # Pass in a location, return term to search
    def getSearchTerm(self):
        if self.location['place_name'] != '':
            self.searchTerm = self.location['place_name']
        if self.location['city'] != '':
            self.searchTerm = self.location['city']
        if self.location['neighborhood'] != '':
            self.searchTerm = self.location['neighborhood'] + ' ' + self.location['city']
        if self.location['name'] != '':
            self.searchTerm = self.location['name']
        print 'Search Term: ' + self.searchTerm



    # Send photo file to cloud vision for analysis
    def _cloudVision(self, photo_file):
        '''Run a label request on a single image'''
	print 'calling cloud vision'

        API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
        http = httplib2.Http()

        credentials = GoogleCredentials.get_application_default().create_scoped(
          ['https://www.googleapis.com/auth/cloud-platform'])
        credentials.authorize(http)

        service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)
        
        with open(photo_file, 'rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = service.images().annotate(
                body={
                    'requests': [{
                        'image': {
                            'content': image_content
                        },
                        'features': [{
                            'type': 'LABEL_DETECTION',
                            'maxResults': 10,
                        },{
                            'type': 'LANDMARK_DETECTION',
                            'maxResults': 5,
                        },{
                            'type': 'TEXT_DETECTION',
                            'maxResults': 1
                        },{
                            'type': 'FACE_DETECTION',
                            'maxResults': 1
                        }]
                     }]
                })
            response = service_request.execute()
            try:
                label = response['responses'][0]['labelAnnotations'][0]['description']
            except KeyError:
                label = 'none'
        return response

 

    # Get weather data from OpenWeatherMap
    def getWeather(self):
        print 'Determing Weather'
        if self.dev == True:
            with open('db/weather_sample.json') as f:
                weather = json.load(f)
                f.close()
        else:
            payload = {'lat': self.location['lat'], 'lon': self.location['lng'], 'units':'imperial', 'APPID': self.creds['OPEN_WEATHER_MAP_API_KEY']}
            r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload)
            weather = json.loads(r.text)

        result = {'temp':weather['main']['temp'], 'status': weather['weather'][0]['main'], 'name': weather['name'], 'wind':weather['wind']['speed']} 
        self.results['weather'] = result


    """
    '[q=search term&fq=filter-field:(filter-term)&additional-params=values]&api-key='+creds['NYTIMES_ARTICLE_SEARCH_API_KEY'])
    """
    def getHistoricalArticle(self):
        print 'Finding history'

        if self.dev == True:
            with open('db/nytimes_sample.json') as f:
                result = json.load(f) 
            self.results['article'] = random.choice(result['response']['docs'])
            return 0

        payload = {'q': self.searchTerm, 'begin-date':18511201, 'end-date':20170101,'api-key': self.creds['NYTIMES_ARTICLE_SEARCH_API_KEY']}
        r = requests.get('http://api.nytimes.com/svc/search/v2/articlesearch.json?', params=payload)
        result = json.loads(r.text)

        if len(result['response']['docs']) > 0:
            self.results['article'] = result['response']['docs']
        else:
            self.results['article'] = {}


    '''
    When results come in, I want to write them to a json file to save the info
    [
        uuid: {
            "imageUrl": imgUrl,
            "labels": [],
            "landmarks": []
            "text": ""
        }
    ]
    '''
    # http://api.repo.nypl.org/
    def getNyplPhotos(self):
        print 'Decoding Digital Archives'
        nypl_results = {}   # return object - will fill up

        # Open prevent calling API's and use local data for testing
        if self.dev == True:
            with open('db/nyplAnalysis.json') as f:
                nyplResults = json.load(f)
                f.close()
            self.results['photos'] = nyplResults
            return 0

        # Construct NYPL URL
        url = 'http://api.repo.nypl.org/api/v1/items/search?q='+self.searchTerm+'&publicDomainOnly=true'

        # Call NYPL Digital Collections with search term
        auth = 'Token token='+self.creds['NYPL_API_KEY']
        call = requests.get(url, headers={'Authorization': auth})
        results = json.loads(call.text)

        # Limit results to only 5, but account for when there
        # are fewer than 5 results
        if results['nyplAPI']['response']['numResults'] < 5:
            length = results['nyplAPI']['response']['numResults']
        else:
            length = 5

        # Open shelf database
        shelf = shelve.open('db/nypl_database.db')

        # Grab 5 random photos
        for i in range(length):

            try:
                choice = random.choice(results['nyplAPI']['response']['result'])    # Grab NYPL Item
            except:
                nypl_results = {}
                break;

            url = choice['apiItemURL']                                          # Get the URL for that Item
            r = requests.get(url, headers={'Authorization': auth})              # Send another request to NYPL to get details for this particular item

            item = json.loads(r.text)['nyplAPI']['response']['capture'][0]      # Parse the returned JSON data for this particular item
            # print item['uuid']

            # Check if the item exists in shelf db
            if shelf.has_key(str(item['uuid'])):
                print 'Object DOES exist in shelf'
                nypl_results[item['uuid']] = shelf[str(item['uuid'])]
            else:
                print 'object DOES NOT exist in shelf'
                # If we dont' already have an entry for it...
                for imgUrl in item['imageLinks']['imageLink']:                  # Each item has links to various resolution images, loop through these links
                    if imgUrl.find('t=w') != -1:                                # Get image with resolution 'w' - points to 760px resolution
			print 'finding image'
                        urllib.urlretrieve(imgUrl, 'img/' + item['uuid'] + '.jpg')  # retrieve and save image by UUID
			print 'got image'
                        analysis = self._cloudVision('img/' + item['uuid'] + '.jpg')  # Send the saved image to cloudVision
			

                        # No guarentee to have any data back, have to check for nil values
                        try:
                            text = analysis['responses'][0]['textAnnotations'][0]['description']
                        except:
                            print 'no text found'
                            text = ''
                        try:
                            labels = analysis['responses'][0]['labelAnnotations']
                        except:
                            print 'no labels found'
                            labels = []
                        # Construct response object - analysis from cloudVision
                        photoAnalysis = {
                            'labels': labels,
                            'text': text,
                            'landmarks': [],
                            'imgUrl': imgUrl,
                            'filepath': 'img/'+item['uuid']
                        }

                        # Save this item to shelf for future use
                        shelf[str(item['uuid'])] = photoAnalysis
                        # Add it to return object
                        nypl_results[item['uuid']] = photoAnalysis
        # Close the shelf connection
	print 'done'
        shelf.close()
        self.results['photos'] = nypl_results
    
    # Factual API - http://developer.factual.com/data-docs/
    def factualSearch(self):
        print 'Assessing nearby culture'
        if self.dev == True:
            print 'Dev is TRUE'
            with open('db/factual_sample.json') as f:
                factual = json.load(f)
                f.close()
            self.results['factual'] = factual
            return 0

        data = self._places.search('').geo(circle(self.location['lat'],self.location['lng'], 1600)).data()

        # if len(data)> 3:
            # l = 3
        # else:
            # l = len(data)

        res = list()
        for index in range(len(data)):
            this = data[index]
            if this['$distance'] < 100:
                distance = 'on the block'
            elif this['$distance'] < 200:
                distance = 'around the corner'
            else:
                distance = 'in the distance'

            obj = {
                    'name':this.get('name', None),
                    'address': this.get('address', None),
                    'rawDistance': this.get('$distance', None),
                    'distance': distance,
                    'categoryLabels': this.get('category_labels', None),
                    'locality': this.get('locality', None),
                    'hours': this.get('hours', {})
                    }
            res.append(obj)
        self.results['factual'] = res

    def wikipediaSearch(self):
        print 'Querying Wikipedia'
        neighborhood = False
        if self.location['neighborhood'] != '':
            neighborhood = True
            searchTerm = self.location['neighborhood'] + ' ' + self.location['city']
        elif self.location['neighborhood'] == '' and self.location['city'] != '' and self.location['region'] != '':
            searchTerm = self.location['city'] + ' ' + self.location['region']
        elif self.location['place_name'] != '':
            searchTerm = self.location['place_name']

        print 'WIKI SEARCH TERM: ' + searchTerm
        wikiPages = list()
        try:
            print 'trying first wiki query'
            results = wikipedia.search(searchTerm)
            if len(results) != 0:
                if len(results) >= 3:
                   results = results[:3]
                for result in results:
                    try:
                        page = wikipedia.page(result)
                        wikiPages.append(page.content)
                    except wikipedia.exceptions.DisambiguationError as e:
                        print 'Disambiguation Error'
                        print e
                    except wikipedia.exceptions.PageError as e:
                        print 'Page Error'
                        print e
        except wikipedia.exceptions.DisambiguationError as e:
            print 'DISAMBIGUATION ERROR'
            print e.options
            if len(e.options) !=0:
                if len(e.options) >= 3:
                    e.options = e.options[:3]
                for opt in e.options:
                    try: 
                        page = wikipedia.page(opt)
                        wikiPages.append(page.content)
                    except wikipedia.exceptions.DisambiguationError as e:
                        print 'Disambiguation Error'
                        print e
                    except wikipedia.exceptions.PageError as e:
                        print 'Page Error'
                        print e
                        pass

        allText = ''
        if len(wikiPages) != 0:
            for page in wikiPages:
                allText += page

        self.results['wikipedia'] = allText
            

    def getUNData(self):
            # with open('db/NCDC_weather_sample.json') as f:
                # weather = json.load(f)
                # f.close()

        res = {}
        with open('db/gross_national_income_countries.json') as f:
            incomeCountries = json.load(f)
            f.close()

        country = self.location['country']
        for item in incomeCountries:
            if country in item['name']:
                incomeCountry = item['name']
                grossNationalIncomeUrl = "http://api.undata-api.org/WHO/WHO%20Data/Gross%20national%20income%20per%20capita/"+incomeCountry+"/records?app_id=d1c7ed02&app_key=0fe5699b7eacf2094df3d3aabe00c17a"
                income = requests.get(grossNationalIncomeUrl)
                print 'GOT INCOME DATA'
                print income
                incomeData = json.loads(income.text)
                res['incomePerCapita'] = str(incomeData[0]['value'])
                res['incomePerCapitaYear'] = str(incomeData[0]['year'])
                break;


        with open('db/life_expectancy_countries.json') as f:
            lifeExpectancyCountries = json.load(f)
            f.close()

        for item in lifeExpectancyCountries:
            if country in item['name']:
                lifeExpectancyCountry = item['name']
                lifeExpectancyUrl = "http://api.undata-api.org/WHO/WHO%20Data/Life%20expectancy%20at%20birth/"+lifeExpectancyCountry+"/records?app_id=d1c7ed02&app_key=0fe5699b7eacf2094df3d3aabe00c17a"
                life = requests.get(lifeExpectancyUrl)
                lifeData = json.loads(life.text)
                for item in lifeData:
                    if item['gender'] == 'Both sexes':
                        res['lifeExpectancyAtBirth'] = str(item['value'])
                        break;
                break;

        with open('db/alcohol_countries.json') as f:
            alcoholCountries = json.load(f)
            f.close()

        for item in alcoholCountries:
            if country in item['name']:
                alcoholCountry = item['name']
                alcoholUrl = "http://api.undata-api.org/WHO/WHO%20Data/Alcohol%20consumption%20amount%20adults%2015%20years%20or%20older/"+alcoholCountry+"/records?app_id=d1c7ed02&app_key=0fe5699b7eacf2094df3d3aabe00c17a"
                # Alcohol consumption measured in liters per year
                alcohol = requests.get(alcoholUrl)
                alcoholData = json.loads(alcohol.text)
                res['alcoholConsumption'] = str(alcoholData[0]['value'])
                break;

        self.results['UNData'] = res





