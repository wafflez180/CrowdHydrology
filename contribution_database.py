#!/util/python3/bin/python

import sqlite3
import uuid

def save_contribution(station, water_height, phone_number):
    create_database()

    conn = sqlite3.connect('crowdhydrology_db.sqlite')
    c = conn.cursor()

    hashed_phone_number = str(uuid.uuid3(uuid.NAMESPACE_OID, phone_number[-10:]))

    #c.execute("INSERT INTO SMSContributions VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    conn.commit()
    conn.close()

def create_database():
    conn = sqlite3.connect('crowdhydrology_db.sqlite')
    c = conn.cursor()

    # Create SMSContributions table
    c.execute('''CREATE TABLE IF NOT EXISTS SMSContributions
                 (ContributionID integer primary key, ContributorID text, StationID text, State text, WaterHeight real, Temperature real, DateReceived date)''')

    # Create InvalidSMSContributions table
    c.execute('''CREATE TABLE IF NOT EXISTS InvalidSMSContributions
                 (ContributionID integer primary key, ContributorID text, Body text, DateReceived date)''')

    # Insert a row of data
    #c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    conn.commit()
    conn.close()