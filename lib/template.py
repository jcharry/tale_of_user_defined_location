#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 jamiecharry <jamiecharry@Jamies-Air-2.home>
#
# Distributed under terms of the MIT license.

poemStructure = {
    'wiki_sentence': [],
    'wiki_verb': [],
    'wiki_adj': [],
    'wiki_noun_phrase': [],
    'wiki_history_sentence': [],
    'wiki_place_sentence': [],
    'article_snippet': [],
    'article_headline': [],
    'article_lead': [],
    'wind_descriptor': [],
    'place': [],
    'temp_descriptor': [],
    'actual_temp': [],
    'weather_status': [],
    'factual_place': [],
    'factual_place_distance': [],
    'factual_label': [],
    'photo_label': [],
    'photo_text': [],
    'income_per_capita': [],
    'income_per_capita_year': [],
    'life_expectancy': [],
    'alcohol_consumption': [],
    'alcohol_word': ['alcohol', 'booze', 'hooch', 'liquor', 'spirits', 'sauce'],
    's1s1': [
        'Ahh, #place#! What a wonderfully #temp_descriptor# place indeed.', 
        'There\'s no place quite like #weather_status.a# #place#.', 
        'Welcome to #temp_descriptor#, #weather_status# #place#.'
    ],
    's1s2': [
        'Where not #factual_place_distance# from this very location stands #factual_place#, fine purveyor of #wiki_adj.a# #factual_label# experience.', 
        'Home of #factual_place#, local #wiki_adj# distributor of #wiki_noun_phrase#.'
    ],
    's1s3': [
        'On a clear day, when #wind_descriptor#, you can see #photo_label.a#.',
    ],
    's1s4': [
        'With #actual_temp# degree days like these, what\'s more fun than visiting #factual_place#? '
    ],
    's1s5': [
        'And with a life expectancy of #life_expectancy#, why not #wiki_verb# with #wiki_noun_phrase#?'
    ],
    's1s6': [
        'Residents #wiki_verb# #temp_descriptor# days and #temp_descriptor# nights, to earn their $#income_per_capita# yearly salaries.',
    ],
    's1s7': [
        'With news like #article_headline#, no wonder the country drinks #alcohol_consumption# liters of #alcohol_word# per year.'
    ],
    's1filler': [
        'Where the #photo_label.s# and #wiki_noun_phrase# roam.',
        'Over there - a #wiki_adj# #wiki_noun_phrase#, #wiki_verb#.'
    ],

    's2s1': [ 
        'Welcome, kind traveler, to #place#.',
        '#place.capitalize#. Home of #wiki_noun_phrase#.',
        '#place#! #temp_descriptor#, #temp_descriptor#, and #temp_descriptor#.'
    ],
    's2s2': ['Since it\'s #weather_status#, let\'s stay in and read some news:'],
    's2s3': ['#article_headline#.'],
    's2s4': ['Also, you\'re just in time! we found an old #photo_label# in the attic! Wow!' ],
    's2s5': ['So #wiki_verb# #wiki_noun_phrase.s#, then let\'s brave the #actual_temp# degree, #temp_descriptor# day, and visit #factual_place#, known worldwide for their #wiki_noun_phrase#.'],
    's2s6': ['Maybe we can learn about #wiki_history_sentence#.'],
    's2s7': ['Afterwards, we can see #wiki_place_sentence#.'],
    's2s8': ['Then while #wind_descriptor#, we can watch the locals #wiki_verb# at #factual_place#.'],
    's2s9': ['It\'ll be a hell of a time'],

    's3s1': ['#place#.'],
    's3s2': ['#wiki_noun_phrase.capitalize.s#, #wiki_noun_phrase#, #wiki_verb# in the #weather_status# air.'],
    's3s3': ['$#income_per_capita# a year buys a hell of a lot of #wiki_noun_phrase#.'],
    's3s4': ['#factual_place_distance# from here stands #factual_place#.'],
    's3s5': ['#photo_label.capitalize# and #photo_label# are commonplace there.'],
    's3s6': ['#temp_descriptor.capitalize# days, where #wind_descriptor#, provide endless opportunities for #wiki_verb.s# with #wiki_noun_phrase#.'],
    's3s7': ['#article_headline.capitalize#, what a world.'],
    's3s8': ['#wiki_history_sentence#'],

    'clearStructure': ['#s1s1# #s1s2# #s1s3# #s1s4# #s1s5# #s1s6# #s1s7#'],

    'rainyStructure': ['#s2s1# #s2s2# #s2s3# #s2s4# #s2s5# #s2s6# #s2s7# #s2s8# #s2s9#'],

    'catchAll': ['#s3s1# #s3s2# #s3s3# #s3s4# #s3s5# #s3s6# #s3s7# #s3s8#'],

    'chooseStructure': ['#structure1#', '#structure2#'],
    'origin': []
}
