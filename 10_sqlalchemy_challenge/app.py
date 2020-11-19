# Import dependencies
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
session = Session(bind=engine)

# Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
    f"Welcome to my 'Home' page!<br/>"
    f"All Available Routes:<br/>"
    f"/: Home Page <br/>"
    f"/api/v1.0/precipitation: Precipitation Data <br/>"
    f"/api/v1.0/stations: Stations <br/>"
    f"/api/v1.0/tobs: Dates and Temperature Data of Most Active Station <br/>"
    f"/api/v1.0/start_date: Minimum, Maximum, and Average Temperatures Starting From Specific Date <br/>"
    f"/api/v1.0/start_date/end_date: Minimum, Maximum, and Average Temperatures Between Two Dates <br/>")


# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")

    precipitation_df = pd.read_csv('Resources/precipitation_df.csv')
    precipitation = {}

    for i in range(len(precipitation_df['date'])):
        precipitation[precipitation_df['date'][i]] = precipitation_df['prcp'][i]
    
    return jsonify(precipitation)

# Stations route 
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

    stations_df = pd.read_csv('Resources/hawaii_stations.csv')
    stations_dict = {}
    
    for i in range(len(stations_df['station'])):
        stations_dict[stations_df['station'][i]] = stations_df['name'][i]

    return jsonify(stations_dict)

# Route for Dates and Temperature Data of Most Active Station
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'TOBS' page...")

    tobs_df = pd.read_csv('Resources/tobs_df.csv')
    tobs = {}

    for i in range(len(tobs_df['date'])):
        tobs[tobs_df['date'][i]] = tobs_df['tobs'][i]
    
    return jsonify(tobs)

@app.route("/api/v1.0/<start_date>")
def summary_start(start_date):
    print("Server received request for 'Summarized Temperature Data (Start)' page...")

    if len(start_date) > 9:
        start = dt.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]))
    elif len(start_date) == 9:
        start = dt.date(int(start_date[:4]), int(start_date[5:6]), int(start_date[7:]))

    # query and retrieve dates from start date
    dates = ((session.query(Measurement.date).\
                        filter(Measurement.date >= start).\
                    order_by(Measurement.date).all()))

    final_dates = []

    # remove duplicate dates
    for date in dates:
        if date[0] not in final_dates:
            final_dates.append(date[0])
    
    # create dictionary to place dates and corresponding min, max, and avg temperatures
    all_tobs = {}
    
    for date in final_dates:
        lowest_temp = (session.query(func.min(Measurement.tobs)).\
                            filter(Measurement.date == date).all())[0][0]

        highest_temp = (session.query(func.max(Measurement.tobs)).\
                                    filter(Measurement.date == date).all())[0][0]

        avg_temp = (session.query(func.avg(Measurement.tobs)).\
                                    filter(Measurement.date == date).all())[0][0]
        
        all_tobs[date] = {'Min Temp': lowest_temp, 
                            'Max Temp': highest_temp,
                            'Average Temp': avg_temp}
        
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def summary_start_end(start_date, end_date):
    print("Server received request for 'Summarized Temperature Data (Start and End)' page...")

    if len(start_date) > 9:
        start = dt.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]))
    elif len(start_date) == 9:
        start = dt.date(int(start_date[:4]), int(start_date[5:6]), int(start_date[7:]))
    
    if len(end_date) > 9:
        end = dt.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]))
    elif len(end_date) == 9:
        end = dt.date(int(end_date[:4]), int(end_date[5:6]), int(end_date[7:]))

    # query and retrieve dates from start date
    dates = ((session.query(Measurement.date).\
                        filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).\
                    order_by(Measurement.date).all()))

    # remove duplicate dates
    final_dates = []

    for date in dates:
        if date[0] not in final_dates:
            final_dates.append(date[0])
    
    # create dictionary to place dates and corresponding min, max, and avg temperatures
    all_tobs = {}
    
    for date in final_dates:
        lowest_temp = (session.query(func.min(Measurement.tobs)).\
                            filter(Measurement.date == date).all())[0][0]

        highest_temp = (session.query(func.max(Measurement.tobs)).\
                                    filter(Measurement.date == date).all())[0][0]

        avg_temp = (session.query(func.avg(Measurement.tobs)).\
                                    filter(Measurement.date == date).all())[0][0]
        
        all_tobs[date] = {'Min Temp': lowest_temp, 
                            'Max Temp': highest_temp,
                            'Average Temp': avg_temp}
        
    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)