#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 23:06:45 2019

@author: FareedMabrouk
"""
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os
import sys
import time

os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"] = 'a6f152d25bd04b25a831b7a17fdfa594'
os.environ["COMPUTER_VISION_ENDPOINT"] = 'https://seamlessevents.cognitiveservices.azure.com/'
# Add your Computer Vision subscription key to your environment variables.

if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
DIR = '/Users/FareedMabrouk/Desktop/Explore/Coding/DubHacks/Seamless Events/Images/'
remote_image_printed_text_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJJAExwQSQED32mmcvbHY0nXz3mJsN7a8gUVMaarpEc-xiAn_a'
recognize_printed_results = computervision_client.batch_read_file(url=remote_image_printed_text_url,  raw=True)


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

# Print the detected text, line by line
if get_printed_text_results.status == TextOperationStatusCodes.succeeded:
    for text_result in get_printed_text_results.recognition_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)

print()