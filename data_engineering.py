
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
# 
# 
# 
# 

# # Step 1 - Data Engineering: 
# 
# The climate data for Hawaii is provided through two CSV files. Start by using Python and Pandas to inspect the content of these files and clean the data.

# In[40]:


# Use Pandas to read in the measurement and station CSV files as DataFrames.

import pandas as pd


# In[41]:


# NaNs and missing values. 

measurements = pd.read_csv("hawaii_measurements.csv")
measurements.head()


# In[42]:


#inspect

measurements.shape


# In[43]:


measurements.duplicated().sum()


# In[44]:


measurements.isnull().sum()


# In[45]:


measurements = measurements.dropna()
measurements.shape


# In[46]:


measurements.head(10)


# In[47]:


measurements.to_csv("clean_hawaii_measurements.csv", index=False)


# In[48]:


stations = pd.read_csv("hawaii_stations.csv")
stations.head()


# In[49]:


stations.shape


# In[50]:


stations.duplicated().sum()


# In[51]:


stations.isnull().values.sum()


# In[52]:


stations.to_csv("clean_hawaii_stations.csv", index=False)
stations.head()

