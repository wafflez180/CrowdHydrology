#!/util/python3/bin/python

import os
import csv
import datetime, time
from main_app.models import SMSContribution, InvalidSMSContribution, Station

def save_contributions_to_csv():
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(dir_path)

    station_list = Station.objects.all()
    for station in station_list:
        contribution_list = SMSContribution.objects.filter(station=station)

        with open('data/' + station.id.upper() + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(['Date and Time', 'Gage Height (ft)', 'POSIX Stamp'])
            for contribution in contribution_list:
                writer.writerow([contribution.date_received.strftime('%m/%d/%Y %X'), str(contribution.water_height)
                , str(time.mktime(contribution.date_received.timetuple()))])
    print("Done! Saved contributions to csv.")
