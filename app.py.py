
import numpy as np
import os
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#change directory to current direcotry
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
m=Base.classes.measurement
s=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""

    return ( 
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start_date<br/>"
    f"/api/v1.0/start_date/end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query precipitation for last year
    qry = session.query(m)
    dt_column = func.date(m.date)
    results = session.query(m.date,m.prcp).filter(dt_column >= dt.datetime(2016, 8, 23)).all()
    session.close()

    rain = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        rain.append(prcp_dict)

    return jsonify(rain) 

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    results=session.query(s.name).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp():
    session=Session(engine)
    qry = session.query(m)
    dt_column = func.date(m.date)
    results=session.query(m.date,m.tobs).filter(dt_column >= dt.datetime(2016, 8, 23)).all()
    session.close()
    temps = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        temps.append(tobs_dict)

    return jsonify(temps) 

@app.route("/api/v1.0/<start>")
def start_temps(start):
    """
     start (string): A date string in the format %Y-%m-%d
    """
    session=Session(engine)   
    results=session.query(func.min(m.tobs),func.avg(m.tobs), func.max(m.tobs)).\
        filter(m.date >= start).all()
    session.close()
    stats = list(np.ravel(results))
    return jsonify(stats)
 
@app.route("/api/v1.0/<start>/<end>")
def end_temps(start, end):
    """ start (string): A date string in the format %Y-%m-%d
        end (string): A date string in the format %Y-%m-%d
    """
    session=Session(engine)   
    results=session.query(func.min(m.tobs), func.avg(m.tobs), func.max(m.tobs)).\
        filter(m.date >= start).filter(m.date <= end).all()
    session.close()
    stats=list(np.ravel(results))
    return jsonify(stats)

"""

   # Convert list of tuples into normal list
    
@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a list of passenger data including the name, age, and sex of each passenger
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)

"""
if __name__ == '__main__':
    app.run(debug=True)
