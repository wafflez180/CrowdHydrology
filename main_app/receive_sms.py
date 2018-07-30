#!/util/python3/bin/python

import os
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
from main_app import contribution_database as database, graphs
from main_app import crowdhydrology_website_database as website_database
import multiprocessing as mp

"""
Functions to receive and parse sms.

@author Arthur De Araujo
@contact adearauj@buffalo.edu
@github github.com/wafflez180

Created: 06/18/2018
"""

@twilio_view # Visit link for more info https://www.twilio.com/blog/2014/04/building-a-simple-sms-message-application-with-twilio-and-django-2.html
def incoming_sms(request):
    # Get the text message the user sent to our Twilio number
    message_body = request.POST.get('Body', None).upper()
    phone_number = request.POST.get('From', None)

    is_valid, station_id, water_height = parse_sms(message_body)

    # Start our TwiML response
    resp = MessagingResponse()

    if is_valid:
        resp.message("Thanks for contributing to CrowdHydrology research and being a citizen-scientist!")
        # TODO: Maybe randomize a funny science joke after

        print("Recieved a valid sms")
        print("\tSMS data:\n\t\tStation: ", station_id, "\n\t\tWater height: ", water_height)
    else:
        resp.message("Whoopsies! We couldn't read your measurement properly.\n Format: 'NY1000 2.5'")

    # Asynchronously call to save the data to allow the reply text message to be sent immediately
    mp.Pool().apply_async(database.save_contribution, (is_valid, station_id, water_height, phone_number, message_body))

    # Replace with a cron script that refreshes the database at 4am everyday
    #mp.Pool().apply_async(website_database.save_contributions_to_csv)

    return str(resp)


def parse_sms(message):
    US_STATES = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
                 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY',
                 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    message_list = message.split(" ")

    # Check if the message has at least a station and one measurement
    if len(message_list) < 2:
        return False, None, None

    # Check if the station string does not contain a state abbreviation
    if not any(state in message_list[0] for state in US_STATES):
        return False, None, None

    # Check if the station string has at least 6 characters
    if len(message_list[0]) < 6:
        return False, None, None

    try:
        station_id = str(message_list[0])
        water_height = float(message_list[1])
    except:
        return False, None, None

    return True, station_id, water_height
