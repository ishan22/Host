#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 23:06:45 2019

@author: FareedMabrouk
"""


import os
import json
import requests

API_KEY = 'a6f152d25bd04b25a831b7a17fdfa594'
ENDPOINT = 'https://seamlessevents.cognitiveservices.azure.com/ocr'
DIR = '/Users/FareedMabrouk/Desktop/Explore/Coding/DubHacks/Seamless Events/Images/'

def handler():
    text = ''
    for filename in sorted(os.listdir(DIR)):
        if filename.endswith(".HEIC"): 
            pathToImage = '{0}/{1}'.format(DIR, filename)
            results = get_text(pathToImage)
            print(results)
            text += parse_text(results)

    open('output.txt', 'w').write(text)

def parse_text(results):
    text = ''
    for region in results['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word['text'] + ' '
            text += '\n'
    return text  

def get_text(pathToImage):
    print('Processing: ' + pathToImage)
    headers  = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params   = {
        'language': 'en',
        'detectOrientation ': 'true'
    }
    payload = open(pathToImage, 'rb').read()
    response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
    results = json.loads(response.content)
    return results

if __name__ == '__main__':
    handler()
