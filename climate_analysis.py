
# coding: utf-8

# # Daniel Ohriner
# 
# April 21, 2018
# 
# Homework 11, Advanced Data Storage Retrieval: Surf's Up
# 
# Overview: Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you decided to do some climate analysis on the area. Because you are such an awesome person, you have decided to share your ninja analytical skills with the community by providing a climate analysis api. The following outlines what you need to do.
# 

# # Step 3 - Climate Analysis and Exploration:
# 
# You are now ready to use Python and SQLAlchemy to do basic climate analysis and data exploration on your new weather station tables. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

# In[ ]:


#Create a Jupyter Notebook file called climate_analysis.ipynb and 
#use it to complete your climate analysis and data exporation.


# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from sqlalchemy.sql import label

from flask import Flask, jsonify

import matplotlib.pyplot as plt


# # Setting up and reflecting the existing sqlite database

# In[ ]:


#Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.


# In[ ]:


#Use SQLAlchemy create_engine to connect to your sqlite database.

# Database setup
engine = create_engine("sqlite:///hawaii.sqlite")


# In[ ]:


#Use SQLAlchemy automap_base() to reflect your tables into classes and
#save a reference to those classes called Station and Measurement.


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[ ]:


# Save reference to the tables
Measurement = Base.classes.measurements
Stations = Base.classes.stations


# In[ ]:


# Create our session (link) from Python to the DB
session = Session(bind = engine)


# # Exploring the database

# In[ ]:


# table names
inspector = inspect(engine)
inspector.get_table_names()


# In[ ]:


# column names and types (measurements)
columns = inspector.get_columns('measurements')
for c in columns:
    print(c['name'], c["type"])


# In[ ]:


# Get a list of column names and types (stations)
columns = inspector.get_columns('stations')
for c in columns:
    print(c['name'], c["type"])


# In[ ]:


engine.execute('SELECT * FROM stations LIMIT 5').fetchall()


# In[ ]:


engine.execute('SELECT * FROM measurements LIMIT 5').fetchall()


# # Precipitation Analysis

# In[ ]:


#Design a query to retrieve the last 12 months of precipitation data.
results = session.query(Measurement.date, Measurement.precip).filter(Measurement.date >= '2017-04-21')


# In[ ]:


#Select only the date and prcp values.


# In[ ]:


#Load the query results into a Pandas DataFrame and set the index to the date column.

# dictionary
data = {'date': [], 'precip': []}

# populate dictionary
for row in results:
    data['date'].append(row.date)
    data['precip'].append(row.precip)

# pandas df
precip17 = pd.DataFrame(data['precip'], columns = ['prcp'], index = data['date'])
print(precip17.head())


# In[ ]:


#Plot the results using the DataFrame plot method.


# In[ ]:


#Use Pandas to print the summary statistics for the precipitation data.


# # Station Analysis

# In[ ]:


#Design a query to calculate the total number of stations.
stations_results = session.query(func.count(Stations.station)).all()
print("There are " + str(stations_results[0]) + " stations.")


# In[ ]:


#Design a query to find the most active stations.
active_results = session.query(Measurement.station,
    label('date', func.count(Measurement.date))).group_by(Measurement.station).all()
for result in active_results:
    print(result)


# In[ ]:


#List the stations and observation counts in descending order
desc_order = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc())
for result in desc_order:
    print(result)


# In[ ]:


#Which station has the highest number of observations?
observations_total = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).first()
print(observations_total)


# In[ ]:


#Design a query to retrieve the last 12 months of temperature observation data (tobs).
temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).    filter(Measurement.date > '2017-04-21').    order_by(Measurement.date).all()
temps


# In[ ]:


#Filter by the station with the highest number of observations.
highest_observations = session.query(Measurement.station, Measurement.tobs).    filter(Measurement.date > '2017-01-01').    group_by(Measurement.station).    order_by(func.count(Measurement.tobs).desc()).all()
highest_observations


# In[ ]:


#Plot the results as a histogram with bins=12.
df = pd.DataFrame(temps, columns=['Station', 'date', 'temp'])
df.set_index('Station', inplace=True)
df.head()


# In[ ]:


hist_plot = df['temp'].hist(bins=12, figsize=(15,10))
hist_plot.set_title('Temperature Observations', fontsize=20)
hist_plot.set_ylabel('Frequency', fontsize=20)
plt.show()


# # Temperature Analysis

# In[ ]:


#Write a function called calc_temps that will accept a start date and end date in the format %Y-%m-%d and
#return the minimum, average, and maximum temperatures for that range of dates.

def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
print(calc_temps('2017-04-21', '2017-07-21'))


# In[ ]:


#Use the calc_temps function to calculate the min, avg, and
#max temperatures for your trip using the matching dates from the previous year (i.e. use "2017-01-01" if your trip start date was "2018-01-01")


temperatures = (calc_temps('2017-04-21', '2017-07-21'))
labels = ['TMIN', 'TAVE', 'TMAX']
df = pd.DataFrame.from_records(temperatures, columns=labels)


# In[ ]:


#Plot the min, avg, and max temperature from your previous query as a bar chart.

#Use the average temperature as the bar height.
#Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr).

temp_chart = df[['TAVE']].plot(kind='bar', title ="Temperatures in Hawaii", figsize=(5, 7), legend=True, fontsize=12, grid=True, color='lightblue')
temp_chart.set_xlabel("Temprature Avg", fontsize=12)
temp_chart.set_ylabel("Temperatures in Farenheit", fontsize=12)
plt.show()


# # Step 4 - Climate App

# In[ ]:


app = Flask(__name__)


# In[ ]:


@app.route("/")
def welcome1():
    """Listing of the available API routes"""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


# In[ ]:


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and temps for the last year"""
    
    # Query the database for dates and tobs
    prcp_results = session.query(Measurement.date, Measurement.tobs).    filter(Measurement.date > '2017-01-01').all()
    
    # Create dictionary from row data and append to the list 'all_prcp'
    all_prcp = []
    for prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["Date"] = Measurement.date
        prcp_dict["TOBS"] = Measurement.tobs
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)


# In[ ]:


@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of stations from the dataset in JSON format"""
    
    station_results = session.query(Station.station).all()
    
    # Convert the list of tuples into a normal list:
    all_stations = list(np.ravel(station_results))
    
    return jsonify(all_stations)


# In[ ]:


@app.route("/api/v1.0/tobs")
def tobs():
    """Returns a list of temperature observations from the last year in JSON format """
    
    #Query database for tobs for last year
    tobs_results = session.query(Measurement.tobs).filter(Measurement.date > '2017-01-01').all()
    
    # Convert the list of tuples into normal list:
    all_tobs = list(np.ravel(tobs_results))
    
    return jsonify(all_tobs)


# In[ ]:


if __name__ == '__main__':
    app.run(debug=True)

