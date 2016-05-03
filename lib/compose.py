#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 jamiecharry <jamiecharry@Jamies-Air-2.home>
#
# Distributed under terms of the MIT license.

"""

"""

import json
from pprint import pprint
import random
from textblob import TextBlob
from textblob import Word
import tracery
from tracery.modifiers import base_english
import math
from template import poemStructure




# print grammar.flatten("#origin#") # prints, e.g., "Hello, world!"

numberOfSpaces = 6
searchTerm = ''

# Run all child functions to 
# parse data from various sources
def decodeData(**kwargs):
    print 'DECODING DATA'
    for name, value in kwargs.items():
        if name == 'filepath':
            print 'given a filepath'
            with open(value) as f:
                data = json.load(f)
                f.close()
        if name == 'jsonData':
            print 'given raw json data'
            data = value
        if name == 'searchTerm':
            searchTerm = value
    print searchTerm

    poemStructure['place'] = [searchTerm]

    for item in data:
        print item
        if item == 'factual':
            factualData = decodeFactualData(data[item])
        elif item == 'weather':
            weatherData = decodeWeatherData(data[item])
        elif item == 'photos':
            photoData = decodePhotos(data[item])
        elif item == 'wikipedia':
            wikiData = decodeWikipedia(data[item])
        elif item == 'article':
            articleData = decodeArticle(data[item])
        elif item == 'UNData':
            unData = decodeUNData(data[item])
            
    allLines = []

    try: 
        randomPlace = random.choice(factualData['places'])
    except:
        randomPlace = {}

    grammar = tracery.Grammar(poemStructure)
    grammar.add_modifiers(base_english)
    poemLines = grammar.flatten('#origin#')
    print poemLines
    poem = {
        'title': data.get('place', 'nowhere'),
        'allLines': poemLines,
        'imgUrls': photoData['urls']
    }
    return poem

def decodeWeatherData(data):
    status = Word(data['status'].lower())
    status = status.lemmatize()
    status = status + 'y'



    poemStructure['weather_status'] = [status]
    poemStructure['actual_temp'] = [str(data['temp'])] 

    '''
    Above 120F: Torrid (R34,G0,B0)
    110 to 120F: Extremely hot (R58,G0,B0)
    100 to 110F: Excessively hot (R88,G0,B0)
    90 to 100F: Very hot (R192,G0,B0)
    80 to 90F: Hot (R255,B0,G0)
    70 to 80F: Very warm (R255,G192,B0)
    60 to 70F: Warm (R255,G255,B0)
    50 to 60F: Mild (R204,G102,B0)
    40 to 50F: Cool (R146,G208,B80)
    30 to 40F: Chilly (R115,G190,B211)
    10 to 30F: Cold (R0,G112,B192)
    10 to -20F: Very cold (R112,G48,B160)
    -20 to -40F: Bitterly cold (R214,G0,B147)
    Below -40F: Brutally cold (R255,G102,B153)

    Read more: http://www.city-data.com/forum/weather/1620160-your-personal-temperature-colors-descriptors-climate.html#ixzz47Ga7mIFW
    '''

    if data['temp'] < 20:
        poemStructure['temp_descriptor'] = ['biting','frigid','frosty','glacial','icy','numbing','polar','wintry','arctic','bitter','chill','chilled','cutting']
    elif data['temp'] < 40:
        poemStructure['temp_descriptor'] = ['breezy','brisk','cool','crisp','freezing','frosty','icy','wintry','arctic','icebox','sharp','biting','blowy','drafty','fresh','glacial','hawkish','nippy','penetrating','snappy']
    elif data['temp'] < 60:
        poemStructure['temp_descriptor'] = ['mild','moderate','pleasant','refreshing','summerlike','summery','temperate']
    elif data['temp'] < 80:
        poemStructure['temp_descriptor'] = ['balmy','broiling','clement','flushed','glowing','heated','hot','lukewarm','pleasant','snug','summery','sweaty','temperate','thermal','warmish']
    elif data['temp'] < 100:
        poemStructure['temp_descriptor'] = ['baking','blistering','broiling','burning','fiery','hot','red-hot','roasting','scalding','scorching','sizzling','torrid','tropical','warm'] 

    # Wind descriptors found here - http://gyre.umeoce.maine.edu/data/gomoos/buoy/php/variable_description.php?variable=wind_speed
    wind = data['wind']
    if wind < 3:
        poemStructure['wind_descriptor'] = ['smoke rises vertically', 'the air is calm']
        wind = ['calmly','stilly']
    elif wind < 7:
        poemStructure['wind_descriptor'] = ['weather vanes are quiet','smoke drifts calmly']
        wind = ['lightly']
    elif wind < 12:
        poemStructure['wind_descriptor'] = ['small twigs move', 'light flags extend']
        wind = ['gently']
    elif wind < 18:    
        poemStructure['wind_descriptor'] = ['small branches sway','paper blows about']
        wind = ['moderately']
    elif wind < 24:
        poemStructure['wind_descriptor'] = ['trees lazily sway', 'waves are breaking']
        wind = ['freshly']
    elif wind < 31:
        poemStructure['wind_descriptor'] = ['the wind tugs', 'wind rushes', 'umbrellas revolt']
        wind = ['strongly']
    elif wind < 38:
        poemStructure['wind_descriptor'] = ['people walk at acute angles', 'twigs break']
        wind = ['gusting']
    else:
        poemStructure['wind_descriptor'] = ['feels like a hurricane', 'trees are falling']
        wind = ['severely', 'violently']
    
    return {}
    # return {'status': status, 'wind': wind, 'temp': temp}

def getMostCommonCategory(d):
    maxCount = 0
    for label in d:
        if d[label] > maxCount:
            maxCount = d[label]
            maxLabel = label
    try:
        res = (maxLabel, maxCount)
    except:
        res = ('', '')
    return res

def getRandomCategory(d):
    if len(d) > 0:
        choice = random.choice(d.keys())
        return (choice, d[choice])
    else:
        return ('', '')


def decodeFactualData(data):

    def metersToFeet(meters):
        # 1 meter = 3.28084 feet
        return str(math.floor(meters*3.28084)) + ' feet'

    # print 'FACTUAL DATA'
    # pprint(data)
    if len(data) != 0:
        for place in data:
            poemStructure['factual_place'].append(place['name'])
            poemStructure['factual_place_distance'].append(metersToFeet(place['rawDistance']))

        # Get a feel for what kinds of places there are
        # Count the number of times each category label appears
        labelCounter = {}
        for place in data:
            if place['categoryLabels'] == None:
                continue
            for bucket in place['categoryLabels']:
                for label in bucket:
                    if label in labelCounter:
                        labelCounter[label] = labelCounter[label] + 1
                    else:
                        labelCounter[label] = 1

        for key in labelCounter.keys():
            print key 
            poemStructure['factual_label'].append(key.lower())
    else:
        poemStructure['factual_place'] = ['no place']
        poemStructure['factual_place_distance'] = ['infinitely far']
        poemStructure['factual_label'] = ['defies catagorization']

    return {}

def decodePhotos(data):
    # print 'PHOTO DATA'
    # pprint(data)
    if len(data) == 0:
        return {}

    # print '\n\n\n\n\n'
    allLabels = list()
    allText = list()
    allUrls = list()
    for photo in data:
        allText.append(data[photo]['text'].split('\n'))
        labels = [label for label in data[photo]['labels']]
        for label in labels:
            allLabels.append(label['description'])
        allUrls.append(data[photo]['imgUrl'])
    poemStructure['photo_label'] = allLabels

    print 'ALL TEXT'
    pprint(allText)
    # safeguard against no found text
    if len(allText) == 0:
        allText = ['GIBBERISH']
    poemStructure['photo_text'] = allText
    res = {'text': allText, 'labels': allLabels, 'urls': allUrls}
    return res


def clipLine(line, spaceCount=10, d='backwards'):
    if line == None:
        return None
    line = line.strip().split()
    if d == 'backwards':
        return ' '.join(line[-spaceCount:])
    else:
        print ' '.join(line[:spaceCount])
        return ' '.join(line[:spaceCount])

    # spaceCounter = 0
    # charCounter = 0
    # for char in reversed(line):
        # charCounter += 1
        # if spaceCounter == spaceCount:
            # break
        # if char == ' ':
            # spaceCounter += 1
    # line = line[-charCounter + 2:]
    # return line

wordsToIgnore = ['be','==','==='];

def decodeWikipedia(data):
    newLines = []
    allSentences = list()

    # Split string into sentences
    blob = TextBlob(data)
    sentences = list()
    history_sentences = []
    place_sentences = []
    print searchTerm
    place_look_up = searchTerm.split()
    print place_look_up
    for sentence in blob.sentences:
        if 'history' in sentence.string or 'historical' in sentence.string or 'historic' in sentence.string:
            print type(sentence.string)
            if '===' in sentence.string:
                s = sentence.string.replace('===', '')
                history_sentences.append(s)
            else:
                history_sentences.append(sentence.string)
        if searchTerm in sentence.string:
            if '===' in sentence.string:
                s = sentence.string.replace('===','')
                place_sentences.append(s)
            else:
                place_sentences.append(sentence.string)
        allSentences.append(sentence.string)
    print 'PLACE SENTENCES'
    # pprint(place_sentences)
    # print 'HISTORY SENTENCES'
    # pprint(history_sentences)

    poemStructure['wiki_history_sentence'] = history_sentences
    poemStructure['wiki_place_sentence'] = place_sentences
    poemStructure['wiki_sentence'] = allSentences

    phrases = blob.noun_phrases
    noun_phrases = []
    for phrase in phrases:
        if '==' in phrase or '===' in phrase:
            continue
        noun_phrases.append(phrase)
    verbs = list()
    adjs = list()
    for word, tag in blob.tags:
        # print word + ' : ' + tag
        if '==' in word or '===' in word:
            continue
        if tag.startswith('VB'):
            lemma = word.lemmatize('v')
            if lemma in wordsToIgnore:
                pass
            else:
                verbs.append(lemma)
        if tag.startswith('JJ'):
            lemma = word.lemmatize('a')
            adjs.append(lemma)
    # pprint(verbs)

    poemStructure['wiki_verb'] = verbs
    poemStructure['wiki_adj'] = adjs
    poemStructure['wiki_noun_phrase'] = noun_phrases


def decodeArticle(data):
    if len(data) > 0:
        articles = []
        snippets = list()
        headlines = list()
        leads = list()
        for i in range(len(data)):
            article = data[i]
            snippets.append(article.get('snippet'))
            hline = article.get('headline', {}).get('main')
            if len(hline) < 60:
                headlines.append(article.get('headline', {}).get('main'))
            leads.append(article.get('lead_paragraph'))

            articles.append({
                'snippet': article.get('snippet'),
                'headline': article.get('headline', {}).get('main'),
                'lead': article.get('lead_paragraph')
            })
    else:
        articles = [{'snippet': 'the times was not on it', 'headline': 'no headline to speak of', 'lead': 'no leads could be followed'}, {'snippet': 'the times was not on it', 'headline': 'no headline to speak of', 'lead': 'no leads could be followed'}]

    print 'HEADLINES NYT'
    # pprint(headlines)
    poemStructure['article_snippet'] = snippets
    poemStructure['article_headline'] = headlines
    poemStructure['article_lead'] = leads

    return articles

def decodeUNData(data):
    # print data

    #{'incomePerCapita': 35310.0, 'lifeExpectancyAtBirth': 81.0, 'incomePerCapitaYear': 2007, 'alcoholConsumption': 7.8}
    poemStructure['income_per_capita'] = [data.get('incomePerCapita', '')]
    poemStructure['income_per_capita_year'] =[data.get('incomePerCapitaYear','')]
    poemStructure['life_expectancy'] = [data.get('lifeExpectancyAtBirth','')]
    poemStructure['alcohol_consumption'] = [data.get('alcoholConsumption','')]
