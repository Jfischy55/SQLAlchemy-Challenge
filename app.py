# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite://Reources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    return(
        f"Hawaii Climate App Api<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0.precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-24').all()
    session.close()

    precipitation_all = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp

        precipitation_all.append(precipitation_dict)
    return jsonify(precipitation_all)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.station).order_by(Station.station).all()
    session.close()

    stations_all = list(np.ravel(results))
    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
            filter(Measurement.station == 'USC0051921').\
                order_by(Measurement.date).all()
    session.close()

    obs_all = list(np.ravel(results))
    return jsonify(obs_all)

@app.route("/api/v1.0/<start>")
def start(start_date):
    
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()

    start_list = list(np.ravel(results))
    return jsonify(start_list)

@app.rout("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    start_end_list = list(np.ravel(results))
    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)