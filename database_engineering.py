
# coding: utf-8

# # Daniel Ohriner
# 
# April 21, 2018
# 
# Homework 11, Advanced Data Storage Retrieval: Surf's Up
# 
# Overview: Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you decided to do some climate analysis on the area. Because you are such an awesome person, you have decided to share your ninja analytical skills with the community by providing a climate analysis api. The following outlines what you need to do.
# 
# 
# 

# # Step 2 - Database Engineering: 
# 
# Use SQLAlchemy to model your table schemas and create a sqlite database for your tables. You will need one table for measurements and one for stations.

# In[ ]:


#Create a Jupyter Notebook called database_engineering.ipynb and use this to complete all of your Database Engineering work.


# In[3]:


#Use Pandas to read your cleaned measurements and stations CSV data.

import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, Text, Float, Date


# In[4]:


#Use the engine and connection string to create a database called hawaii.sqlite.
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()


# In[5]:


#Use declarative_base and create ORM classes for each table.
Base = declarative_base()

class Measurements(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    station = Column(Text)
    date = Column(Date)
    prcp = Column(Float)  
    tobs = Column(Float)


#You will need a class for Measurement and for Station.
#Make sure to define your primary keys.


# In[8]:


#Once you have your ORM classes defined, create the tables in the database using create_all.
Base.metadata.create_all(engine)


# In[12]:


measurements_df = pd.read_csv("clean_hawaii_measurements.csv")
measurements_df.head()


# In[13]:


# convert date column to datetime dtype
measurements_df['date'] = pd.to_datetime(measurements_df['date'], format = '%Y-%m-%d')


# In[14]:


# Use Orient='station' to create a list of data to write
# to_dict() cleans out DataFrame metadata as well
# http://pandas-docs.github.io/pandas-docs-travis/io.html#orient-options
data_measurements = measurements_df.to_dict(orient='records')


# In[15]:


# Data is just a list of dictionaries that represent each row of data
data_measurements[0]


# In[16]:


# Use MetaData from SQLAlchemy to reflect the tables
metadata = MetaData(bind=engine)
metadata.reflect()


# In[17]:



# Save the reference to the `stations` table as a variable called `station_table`
measurement_table = sqlalchemy.Table('measurements', metadata, autoload=True)


# In[18]:



# Use `table.delete()` to remove any pre-existing data.
# Note that this is a convenience function so that you can re-run the example code multiple times.
# You would not likely do this step in production.
conn.execute(measurement_table.delete())


# In[19]:


# Use `table.insert()` to insert the data into the table
# The SQL table is populated during this step
conn.execute(measurement_table.insert(), data_measurements)


# In[20]:


# Test that the insert works by fetching the first 5 rows. 
conn.execute("select * from measurements limit 5").fetchall()


# # Stations Table

# In[ ]:


# Use `declarative_base` from SQLAlchemy to model the measurements table as an ORM class
# Make sure to specify types for each column, e.g. Integer, Text, etc.
# http://docs.sqlalchemy.org/en/latest/core/type_basics.html
class Stations(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    station = Column(Text)
    name = Column(Text)
    latitude = Column(Float)  
    longitude = Column(Float)
    elevation = Column(Float)


# In[ ]:


# Use `create_all` to create the stations table in the database
Base.metadata.create_all(engine)


# In[ ]:


# Load the cleaned csv file into a pandas dataframe
stations_df = pd.read_csv("Resources/clean_hawaii_stations.csv")
stations_df.head()


# In[ ]:


# Use Orient='records' to create a list of data to write
# http://pandas-docs.github.io/pandas-docs-travis/io.html#orient-options
station_data = stations_df.to_dict(orient='records')
station_data[0]


# In[ ]:


# Use MetaData from SQLAlchemy to reflect the tables
metadata = MetaData(bind=engine)
metadata.reflect()


# In[ ]:



# Save the reference to the `stations` table as a variable called `station_table`
station_table = sqlalchemy.Table('stations', metadata, autoload=True)


# In[ ]:


# Use `table.delete()` to remove any existing data.
# Note that this is a convenience function so that you can re-run the example code multiple times.
# You would not likely do this step in production.
conn.execute(station_table.delete())


# In[ ]:


# Use `table.insert()` to insert the data into the table
conn.execute(station_table.insert(), station_data)


# In[ ]:


# Test that the insert works by fetching the first 5 rows. 
conn.execute("select * from stations limit 5").fetchall()

