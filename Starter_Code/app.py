# Import the dependencies.
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():

    return (
        f"Welcome to my App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/&lt;start&gt;/&lt;end&gt;<br/>"
        f"/api/v1.0/temp/&lt;start&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """This will return the precipitation data for the last year"""
    prev_year_calc = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year_calc).all()

    session.close()

    prcp_data = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    """Returns the list of stations"""
    results = session.query(Station.station).all()

    session.close()

    station_data = list(np.ravel(results))

    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperatures (tobs) for previous year."""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    session.close()

    temp_data = list(np.ravel(results))

    return jsonify(temp_data)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

session.close()


if __name__ == '__main__':
    app.run(debug=True)