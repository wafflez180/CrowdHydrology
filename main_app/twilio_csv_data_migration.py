#!/util/python3/bin/python

import os
import numpy as np
import csv
import json
import sqlite3
from datetime import datetime
from main_app import receive_sms
import uuid
from django.utils import timezone
from main_app import graphs
from main_app.models import SMSContribution, InvalidSMSContribution, Station

sms_csv_dict = dict()

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

if os.path.exists('/Users/arthurdearaujo/Desktop/Hydrogeology Research/crowd_hydrology/main_app/twiliosms.csv'):
    totalfile = open('/Users/arthurdearaujo/Desktop/Hydrogeology Research/crowd_hydrology/main_app/twiliosms.csv', 'r')
    totalreader = csv.reader(totalfile, delimiter=',')
    firstrow = True
    for user in totalreader:
        if not firstrow:
            #print(len(user))
            #print(user)
            if int(user[0]) != 8457091170:
                sms_csv_dict[user[0]] = (user[2], user[4])
        firstrow = False
    totalfile.close()
else:
    print("Error: Couldn't find twilio_sms.csv.")

print(sms_csv_dict)

for contributor_id, contribution_info in sms_csv_dict.items():
    is_valid, station_id, water_height, temperature, error_msg = receive_sms.parse_sms(contribution_info[0])
    hashed_phone_number = str(uuid.uuid3(uuid.NAMESPACE_OID, contributor_id[-10:]))
    date_received = datetime.strptime((contribution_info[1]).replace(' UTC', '-0000'), '%Y-%m-%d %H:%M:%S%z')

    if is_valid:
        station = Station.objects.get(id=station_id)
        new_contributon = SMSContribution(contributor_id=hashed_phone_number, station=station,
                                          water_height=float(water_height),
                                          temperature=temperature, date_received=date_received)
        new_contributon.save()
    else:
        new_invalid_contribution = InvalidSMSContribution(contributor_id=hashed_phone_number, message_body=contribution_info[0],
                                                          date_received=date_received)
        new_invalid_contribution.save()
