from flask import Flask, jsonify

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the my Hawaiian Adventure analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)

    result = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= year_ago)

    df = pd.DataFrame(result)
    df_index = df.set_index('date')
    df_sort = df_index.sort_values('date')
    
    df_sort.plot(kind="bar", grid=True)
    plt.title("Precipitation in Hawaii")
    plt.ylabel("Precipitation")
    plt.xlabel("Date")
    plt.legend(["Precipitation"])
    plt.xticks([])
    plt.show()


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(Measurement.station, func.count(Measurement.station))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc()).all()
    
    prcp_dic = {date: prcp for date, prcp in results}
    return jsonify(prcp_dic)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    active_station = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= year_ago).all()

    return jsonify(active_station)


@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)



@app.route("/api/v1.0/<start><end>")
def start_end():
    session = Session(engine)