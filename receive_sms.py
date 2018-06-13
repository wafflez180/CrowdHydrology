#!/util/python3/bin/python

import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])
def incoming_sms():
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None).upper()

    # Start our TwiML response
    resp = MessagingResponse()

    is_valid, station, water_height = parse_sms(body)

    if is_valid:
        resp.message("Thanks for contributing to CrowdHydrology research and being a citizen-scientist!")
        # Maybe randomize a funny science joke after

        print("Recieved a valid sms")
        print("\tSMS data:\n\t\tStation: ", station, "\n\t\tWater height: ", water_height, ")

        # Asynchronously start entering into the database
        #pool.enterdataintodatabase
    else:
        resp.message("Whoopsies! We couldn't read your measurement properly.\n Format: 'NY1000 2.5'")

    return str(resp)


def parse_sms(message):
    US_STATES = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
                 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY',
                 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    message_list = message.split(" ")

    if len(message_list) < 2:
        return False

    # Check if the station string does not contain a state abbreviation
    if not any(state in message_list[0] for state in US_STATES):
        return False

    try:
        station = str(message_list[0])
        water_height = float(message_list[1])
    except:
        return False

    return True, station, water_height

# https://teamtreehouse.com/community/can-someone-help-me-understand-flaskname-a-little-better
# Checks to see if this module was called interactively (script, command, etc)
# Would not execute if this module was imported into another module
if __name__ == "__main__":
    app.run(debug=True)