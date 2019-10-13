#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 23:06:45 2019
@author: FareedMabrouk
"""
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import dateparser as dp
import io
import datetime
import os
import sys
import time
import datefinder
import re

os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"] = 'a6f152d25bd04b25a831b7a17fdfa594'
os.environ["COMPUTER_VISION_ENDPOINT"] = 'https://seamlessevents.cognitiveservices.azure.com/'
os.environ["TEXT_ANALYTICS_SUBSCRIPTION_KEY"] = '0122840605a3487c9b6a385ee25148db'
os.environ["TEXT_ANALYTICS_ENDPOINT"] = 'https://seamlesstextanalytics.cognitiveservices.azure.com/'

key_var_name = 'TEXT_ANALYTICS_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TEXT_ANALYTICS_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]

credentials = CognitiveServicesCredentials(subscription_key)


if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key_cv = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint_cv = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
computervision_client = ComputerVisionClient(endpoint_cv, CognitiveServicesCredentials(subscription_key_cv))
text_analytics = TextAnalyticsClient(endpoint, credentials=credentials)

def getData(input_data):
    image_url = 'https://d1csarkz8obe9u.cloudfront.net/posterpreviews/event-poster-template-e6771eeb0763814b21d0144eb8e91bdb.jpg?ts=1561498807'
    recognize_printed_results = computervision_client.batch_read_file_in_stream(input_data,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    operation_location_remote = recognize_printed_results.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = operation_location_remote.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        get_printed_text_results = computervision_client.get_read_operation_result(operation_id)
        if get_printed_text_results.status not in ['NotStarted', 'Running']:
            break
        time.sleep(1)

    full_text = ""
    # Print the detected text, line by line
    if get_printed_text_results.status == TextOperationStatusCodes.succeeded:
        for text_result in get_printed_text_results.recognition_results:
            for line in text_result.lines:
                full_text += line.text + '\n'

    documents = [
    {
        "id": "1",
        "language": "en",
        "text": full_text
    }
    ]

    e_details = {
    "title": '',
    "date": '',
    "time_range": ''
    }

    title = ""
    big_area = 0
    threshold = 20
    for text_result in get_printed_text_results.recognition_results:
        for line in text_result.lines:
            box = line.bounding_box
            curr_area = abs(box[4] - box[0])
            if curr_area > big_area + threshold:
                title = line.text
                big_area = curr_area
            elif curr_area >= big_area - threshold and curr_area <= big_area + threshold:
                title += " " + line.text

    e_details['title'] = title
    response = text_analytics.entities(documents=documents)
    for document in response.documents:
        for entity in document.entities:
            if entity.sub_type == 'Date':
                e_details['date'] = entity.name
            if entity.sub_type == 'TimeRange':
                e_details['time_range'] = entity.name
            if entity.type == 'DateTime' and not entity.name in e_details['date'] :
                e_details['date'] += ' ' + entity.name
    for document in response.documents:
        print("Document Id: ", document.id)
        print("\tKey Entities:")
        for entity in document.entities:
            print("\t\t", "NAME: ", entity.name, "\tType: ",
                  entity.type, "\tSub-type: ", entity.sub_type)
            for match in entity.matches:
                print("\t\t\tOffset: ", match.offset, "\tLength: ", match.length, "\tScore: ",
                      "{:.2f}".format(match.entity_type_score))
    date = e_details['date']
    new_date = '';
    new_date +=  str(get_time(earlier_time(date))) + ' '
    new_date += get_day(date) + ' '
    new_date += get_month(date)
    new_date += get_date(date)
    matches = datefinder.find_dates(date.lower())
    e_details['standard'] = matches
    return e_details


def earlier_time(time):
    if "am" in time.lower():
        list_of_words = time.lower().split('am')
        print(list_of_words)
        first_am = list_of_words[0].split()[-1]
        if len(list_of_words) == 3:
            second_am = list_of_words[1].split()[-1]
            if first_am[0] > second_am[0]:
                return second_am + "am"
            else:
                return first_am + "am"
        if "pm" in list_of_words[1]:
            return first_am + "am"
        else:
            return first_am
    elif "pm" in time.lower():
        list_of_words = time.lower().split('pm')
        first_pm = list_of_words[0].split()[-1]
        if len(list_of_words) == 3:
            second_pm = list_of_words[1].split()[-1]
            if first_pm[0] > second_pm[0]:
                return second_pm + "pm"
            else:
                return first_pm + "pm"
        else:
            return first_pm

def get_time(date):
    date = date.lower()
    fixed_time = 0
    if 'am' in date:
        list_of_words = date.split('am')
        fixed_time = list_of_words[0].split()[-1]
    elif 'pm' in date.lower():
        list_of_words = date.split('pm')
        fixed_time = list_of_words[0].split()[-1]
        if ':' in fixed_time:
            split_time = fixed_time.split(':')
            split_time[0] = str(int(split_time[0]) + 12)
            return ':'.join(split_time)
        else:
            return int(fixed_time) + 12
    return fixed_time
days = {
    'sunday': ['sunday','sun'],
    'monday': ['monday', 'mon'],
    'tuesday': ['tuesday', 'tue', 'tues'],
    'wednesday': ['wednesday', 'wed'],
    'thursday': ['thursday', 'thurs', 'thur', 'thu'],
    'friday': ['friday', 'fri'],
    'saturday': ['saturday', 'sat']
}
months = {
    'january': ['january', 'jan'],
    'february': ['february', 'feb'],
    'march': ['march', 'mar'],
    'april': ['april', 'apr'],
    'may': ['may'],
    'june': ['june', 'jun'],
    'july': ['july', 'jul'],
    'august': ['august', 'aug'],
    'september': ['september', 'sept', 'sep'],
    'october': ['october', 'oct'],
    'november': ['november', 'nov'],
    'december': ['december', 'dec']
}
def get_day(date):
    date = date.lower()
    for day in days:
        for tweak in days[day]:
            if tweak in date:
                return day
    return ''
def get_month(date):
    date = date.lower()
    for month in months:
        for tweak in months[month]:
            if tweak in date:
                return month
    return ''
def get_date(date):
    date = date.lower()
    split_list = date.split()
    aux_list = []
    for word in split_list:
        if not 'pm' in word and not 'am' in word and not ':' in word and not 'to' in word:
            aux_list.append(word)
            print(word)

    for word in aux_list:
        print(word)
        word2 = ''.join(i for i in word if i.isdigit())
        if word2.isdigit() and (int(word2) > 0 and int(word2) < 32):
            return word2
    return ''
