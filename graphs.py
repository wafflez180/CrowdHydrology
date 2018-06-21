#!/util/python3/bin/python

import os
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json
import csv
import datetime
import sqlite3
import time

"""
Functions to create graphs derived from data located in the CSV files.

@author Arthur De Araujo
@contact adearauj@buffalo.edu
@github github.com/wafflez180

Created: 06/18/2018
"""


def generate():
    # Connect to database
    conn = sqlite3.connect('crowdhydrology_db.sqlite')
    cursor = conn.cursor()

    plotly.tools.set_credentials_file(username='wafflez180', api_key='v2ub8wWESL46Q3y0B9wA')
    print("Generating graphs...")
    generate_contribution_amount_pie_chart(cursor)
    generate_user_station_contrib_bar_graph(cursor)
    generate_contribution_dates_line_graph(cursor)
    print("Graph generation complete.")

    # Close database connection
    conn.close()


def generate_contribution_amount_pie_chart(cursor):
    print("\tGenerating contribution amount pie chart...")

    # Get a list of total contributions sent per contributor
    arduino_contributor_id = 'c54fffe2-2870-3b16-8d3c-fc0e65d5e946'
    cursor.execute('SELECT ContributorID, count(*) FROM SMSContributions WHERE ContributorID != ? GROUP BY ContributorID', (arduino_contributor_id,))
    total_contributions_per_contributor_list = cursor.fetchall()

    print("\t\tFetched total contributions")

    #print(total_contributions_per_contributor_list)

    # Count number of contributors for each amount of total contributions
    # Index 1 with value 10 means : 10 users sent only 1 text
    num_of_contributors_per_contribution_amount_list = [0] * 10000

    for total_contributions in total_contributions_per_contributor_list:
        num_of_contributors_per_contribution_amount_list[total_contributions[1]] += 1

    # Add the graph label and value for each contribution amount
    labels = []
    values = []
    for i in range(len(num_of_contributors_per_contribution_amount_list)):
        if num_of_contributors_per_contribution_amount_list[i] != 0:
            labels.append(str(i) + " texts")
            values.append(num_of_contributors_per_contribution_amount_list[i])

    if labels:
        trace = go.Pie(labels=labels, values=values, hole=.2,textposition='outside')
        py.plot([trace], filename='number_of_contributors_per_contribution_amount_list', auto_open=False)
        print("\tSuccessfully graphed : Contributions Per Contributor Pie Graph")


def generate_user_station_contrib_bar_graph(cursor):
    print("\tGenerating user station contribution bar graph...")

    plotly_traces = []

    cursor.execute("SELECT DISTINCT ContributorID FROM SMSContributions")
    contributor_ids = cursor.fetchall()

    # For each contributor, get the amount of their contributions per station
    for contributor_id in contributor_ids:
        #print(contributor_id[0])
        cursor.execute("SELECT DISTINCT StationID FROM SMSContributions WHERE ContributorID=?", (contributor_id[0],))
        stations = cursor.fetchall()

        station_contribution_dict = {}
        for station in stations:
            cursor.execute("SELECT count(*) FROM SMSContributions WHERE ContributorID=? AND StationID=?", (contributor_id[0],station[0],))
            station_contributions_amount = cursor.fetchall()[0]
            station_contribution_dict[station[0]] = station_contributions_amount[0]
        #print(station_contribution_dict)

        plotly_traces.append(go.Bar(
            x=list(station_contribution_dict.keys()),
            y=list(station_contribution_dict.values()),
            name=contributor_id[0]))

    layout = go.Layout(
        barmode='stack'
    )

    if plotly_traces:
        fig = go.Figure(data=plotly_traces, layout=layout)
        py.plot(fig, filename='contributions_per_station', auto_open=False)
        print("\tSuccessfully graphed : Contributions Stations Bar Graph")

# Fills dates having 0 amount of texts in between date1 and date2
def fill_dates_between(date1, date2, date_list, text_amount_list):
    next_day = date1 + datetime.timedelta(days=1)
    days_difference = (date2 - date1).days

    for i in range(days_difference-1):
        try:
            date_list.append(next_day)
            text_amount_list.append(0)
        except OverflowError:  # date value out of range, ex: July 32nd
            if next_day.month == 12:
                next_day = next_day.replace(month=1)
            else:
                next_day = next_day.replace(month=next_day.month + 1)

        next_day += datetime.timedelta(days=1)


def generate_contribution_dates_line_graph(cursor):
    print("\tGenerating contribution dates line graph...")

    state_dates_dict = dict()

    # For each state, get all the contribution dates
    cursor.execute("SELECT DISTINCT State FROM SMSContributions")
    states = cursor.fetchall()

    for state in states:
        #print(state[0])
        arduino_contributor_id = 'c54fffe2-2870-3b16-8d3c-fc0e65d5e946'
        cursor.execute('SELECT DateReceived FROM SMSContributions WHERE State=? AND ContributorID != ? ORDER BY DateReceived',(state[0], arduino_contributor_id))
        contribution_dates = cursor.fetchall()
        #print(contribution_dates)
        state_dates_dict[state[0]] = contribution_dates

    plotly_traces = []

    # For each state, go through each contribution date and calculate the number of contributions on that day
    for state, dates in state_dates_dict.items():
        contribution_date_list = []
        contribution_amount_list = []

        prev_date = (datetime.datetime.strptime(dates[0][0], '%Y-%m-%d %H:%M:%S')).replace(hour=0, minute=0, second=0, microsecond=0)
        contribution_date_list.append(prev_date)
        contribution_amount_list.append(0)

        for date in dates:
            date = datetime.datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S').replace(hour=0, minute=0, second=0, microsecond=0)
            if date > prev_date:
                fill_dates_between(prev_date, date, contribution_date_list, contribution_amount_list)

                prev_date = date

                contribution_date_list.append(date)
                contribution_amount_list.append(1)
            else:
                # If the contribution's date is on the same day, increment the amount of contributions on that day
                contribution_amount_list[-1] += 1

        plotly_traces.append(go.Scatter(
            x=contribution_date_list,
            y=contribution_amount_list,
            mode='lines',
            name=state
        ))

        print("\t\tTraced: ", state)

    if plotly_traces:
        py.plot(plotly_traces, filename='contribution_dates', auto_open=False)
        print("\tSuccessfully graphed : Contribution Date Line Graph")


