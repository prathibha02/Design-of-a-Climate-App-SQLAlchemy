import numpy as np
import datetime as dt

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_
from sqlalchemy.sql import func


from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"1.<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"2.<br/>"
        f"/api/v1.0/stations<br/>"
        f"3.<br/>"
        f"/api/v1.0/tobs<br/>"
        f"4.<br/>"
        f"Please enter the start date at the end of the url as yyyy,mm,dd<br/>"
        f"/api/v1.0/<start><br/>"
        f"5.<br/>"
        f"Please enter the start date/end date at the end of the url as yyyy,mm,dd<br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of percipitation for all dates"""
    # Query precipitation for all dates
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

   # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, pcrp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = pcrp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station,name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations for last year of the data, 
    as calculated in climate.ipynb, the first part of the assignment"""
    
    one_year_from_last_date = dt.datetime(2017,8,18) - dt.timedelta(days=365)
    a_year = session.query(Measurement.date,Measurement.tobs).filter(
                and_( Measurement.station == 'USC00519281',
          Measurement.date >= one_year_from_last_date)).all()
    
    session.close()

   # Create a dictionary from the row data and append to a list of all the temps in the year 
   # between the last date and the year before that
    a_year_tobs = []
    for date, tobs in a_year:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        a_year_tobs.append(tobs_dict)

    return jsonify(a_year_tobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def T_max_min_avg(start=None,end=None):
   
   
# Minimum Temparature 

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    if end==None: 
   
       lowest_temp = session.query((Measurement.date),func.min(Measurement.tobs).label("min_temp")).\
               filter(Measurement.date >= start).all()
    else:        
       
        lowest_temp = session.query((Measurement.date),func.min(Measurement.tobs).label("min_temp")).\
               filter(Measurement.date >= start).\
               filter(Measurement.date <= end).all()


    session.close()

   # Create a dictionary from the row data and append to a list of which contains min, max, and avg temperatures 
   # between the user entered variable and the last date of the recorded temperatures
    min_max_avg_t = []

# Minimum temperature 
    for date, tobs in lowest_temp:
        t_dict = {}
        t_dict["date"] = date
        t_dict["min_temp"] = tobs
        min_max_avg_t.append(t_dict)

 

# Maximum temperature     

    # Create our session (link) from Python to the DB
    session = Session(engine)

    if end==None: 

     highest_temp = session.query((Measurement.date),func.max(Measurement.tobs).label("max_temp")).\
               filter(Measurement.date >= start).all()
    else: 
        highest_temp = session.query((Measurement.date),func.max(Measurement.tobs).label("max_temp")).\
               filter(Measurement.date >= start).\
               filter(Measurement.date <= end).all()

    session.close()

# Create a dictionary from the row data and append to a list of which contains min, max, and avg temperatures 
  
    for date, tobs in highest_temp:
        t_dict = {}
        t_dict["date"] = date
        t_dict["max_temp"] = tobs
        min_max_avg_t.append(t_dict)


# Average temperature    

    # Create our session (link) from Python to the DB
    session = Session(engine)

    if end==None: 
      average_temp = session.query((Measurement.date),func.avg(Measurement.tobs).label("avg_temp")).\
               filter(Measurement.date >= start).all()
    else:
         average_temp = session.query((Measurement.date),func.avg(Measurement.tobs).label("avg_temp")).\
                 filter(Measurement.date >= start).\
                 filter(Measurement.date <= end).all()   
    session.close()

# Create a dictionary from the row data and append to a list of which contains min, max, and avg temperatures 
  
    for date, tobs in average_temp:
        t_dict = {}
        t_dict["avg_temp"] = tobs
        min_max_avg_t.append(t_dict)

    return jsonify(min_max_avg_t)





if __name__ == '__main__':
    app.run(debug=True)

  


