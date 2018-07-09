#!/util/python3/bin/python

import sqlite3
import uuid
import datetime
from main_app import graphs

"""
Functions to set up a database and save contributions to the database.

@author Arthur De Araujo
@contact adearauj@buffalo.edu
@github github.com/wafflez180

Created: 06/18/2018
"""

def save_contribution(is_valid, station_id, water_height, phone_number, message_body):
    create_database()
    hashed_phone_number = str(uuid.uuid3(uuid.NAMESPACE_OID, phone_number[-10:]))

    # Connect to database
    conn = sqlite3.connect('crowdhydrology_db.sqlite')
    cur = conn.cursor()

    if is_valid:
        sql_values = (hashed_phone_number, station_id, station_id[:2], water_height, None, datetime.datetime.now())
        cur.execute("INSERT INTO SMSContributions (ContributorID, StationID, State, WaterHeight, Temperature, DateReceived) VALUES (?,?,?,?,?,?)", sql_values)
    else:
        sql_values = (hashed_phone_number, message_body, datetime.datetime.now())
        cur.execute("INSERT INTO InvalidSMSContributions (ContributorID, MessageBody, DateReceived) VALUES (?,?,?)", sql_values)

    # Save (commit) the database changes
    conn.commit()
    conn.close()

    # ToDo: Consider executing graph generation less because it takes a lot of computation
    #if is_valid:
        #graphs.generate()


def create_database():
    conn = sqlite3.connect('crowdhydrology_db.sqlite')
    c = conn.cursor()

    # Create SMSContributions table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS SMSContributions
                 (ContributionID integer primary key, ContributorID text, StationID text, State text, WaterHeight real, Temperature real, DateReceived date)''')

    # Create InvalidSMSContributions table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS InvalidSMSContributions
                 (ContributionID integer primary key, ContributorID text, MessageBody text, DateReceived date)''')

    # Save (commit) the database changes
    conn.commit()
    conn.close()
