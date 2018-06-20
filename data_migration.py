#!/util/python3/bin/python

import os
import numpy as np
import csv
import json
import sqlite3
from datetime import datetime

"""
Functions to migrate the data located in CSV files associated with the old Social.Water codebase to the new SQLite database.

@author Arthur De Araujo
@contact adearauj@buffalo.edu
@github github.com/wafflez180

Created: 06/19/2018
"""

contributions_csv_dict = dict()  ## track user contributions

if os.path.exists('contributionTotals.csv'):
    totalfile = open('contributionTotals.csv', 'r')
    totalreader = csv.reader(totalfile, delimiter=',')
    firstrow = True
    for user in totalreader:
        if not firstrow:
            contribution_dict_str = user[4].replace("-", ",").replace("\'", "\"")
            contribution_date_dict_str = user[5].replace("-", ",").replace("\'", "\"")
            bad_contribution_list = user[6].replace("-", ",").replace("\'", "").replace("[", "").replace("]", "").split(
                ",")
            bad_contribution_date_list = user[7].replace("-", ",").replace("\'", "").replace("[", "").replace("]",
                                                                                                              "").split(
                ",")
            contribution_water_height_dict_str = user[8].replace("-", ",").replace("\'", "\"").replace(", ,", ", ")

            contributions_csv_dict[user[0]] = (user[1], int(user[2]), int(user[3]), json.loads(contribution_dict_str),
                                    json.loads(contribution_date_dict_str), bad_contribution_list,
                                    bad_contribution_date_list, json.loads(contribution_water_height_dict_str))
        firstrow = False
    totalfile.close()
else:
    print("Error: Couldn't find contributionTotals.csv.")

# Connect to database
conn = sqlite3.connect('crowdhydrology_db.sqlite')
cur = conn.cursor()

for contributor_id, contribution_info in contributions_csv_dict.items():
    print(contributor_id)

    # Insert Valid Contributions
    station_contrib_amount_dict = contribution_info[3]
    for station_id, contribution_amount in station_contrib_amount_dict.items():
        for i in range(contribution_amount):
            contribution_date = datetime.fromtimestamp(int(contribution_info[4][station_id][i]))
            sql_values = (contributor_id, station_id, station_id[:2], contribution_info[7][station_id][i], None, contribution_date)
            cur.execute("INSERT INTO SMSContributions (ContributorID, StationID, State, WaterHeight, Temperature, DateReceived) VALUES (?,?,?,?,?,?)",
                        sql_values)

    # Insert Invalid Contributions
    invalid_contribution_amount = contribution_info[2]
    for i in range(invalid_contribution_amount):
        contribution_date = datetime.fromtimestamp(float(contribution_info[6][i]))
        sql_values = (contributor_id, contribution_info[5][i], contribution_date)
        cur.execute("INSERT INTO InvalidSMSContributions (ContributorID, MessageBody, DateReceived) VALUES (?,?,?)", sql_values)

# Close database connection
conn.commit()
conn.close()