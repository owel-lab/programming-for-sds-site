#!/usr/bin/env python
# coding: utf-8

# # Vector data analysis
# 
# The **vector data model** represents features on the Earth's surface as **points**, **lines** or **polygons**. Vector data is useful for storing and representing data that has discrete boundaries, such as borders, buildings, streets, and roads. Online mapping applications, such as **Google Maps** and **OpenStreetMap**, use this format to display data. 
# 
# The Python library `GeoPandas` provides somes great tools for working with vector data. As the name suggests, `GeoPandas` extends the popular data science library `Pandas` by adding support for geospatial data. The core data structure in `GeoPandas` is the `GeoDataFrame`. The key difference between the two is that a `GeoDataFrame` can store geometry data and perform spatial operations.
# 
# ```{image} images/dataframe.png
# :alt: geodataframe
# :width: 700px
# :align: center
# ```
# 
# The `geometry` column can contain any geometry type (e.g. points, lines, polygons) or even a mixture.
# 
# ## Reading files
# 
# Assuming we have a file containing both data and geometry (e.g. GeoPackage, GeoJSON, Shapefile), we can read it using `read_file()`, which automatically detects the filetype and creates a `GeoDataFrame`. In the this demo, we will be working with a shapefile that contains the states of the contiguous United States. 

# In[97]:


import geopandas as gpd

gdf = gpd.read_file('data/us_states.shp')
gdf.head()


# In[98]:


type(gdf)


# ```{note} 
# The `geometry` column is the **active geometry**. Spatial methods used on the `GeoDataFrame` will use these geometries.
# ```

# ## Geometric properties
# 
# Since we have a `GeoDataFrame` that is spatially "aware", we can compute the geometric properties for each row. For example, we could make a new column that contains the area of each state:

# In[99]:


gdf['area'] = gdf['geometry'].area
gdf.head()


# Or the centroid of each state

# In[100]:


gdf['centroid'] = gdf['geometry'].centroid
gdf.head()


# ## Plot
# 
# We can use `plot()` to produce a basic vizualisation of the geometries.

# In[101]:


gdf.plot()


# We can also explore our data interactively using `GeoDataFrame.explore()`, which behaves in the same way `plot()` does but returns an interactive map instead.

# In[102]:


gdf.explore()


# Finally, we can plot two geometry columns together, we just need to use one plot as an axis for the other.

# In[103]:


ax = gdf['geometry'].plot()
gdf['centroid'].plot(ax=ax, color='black')


# ## Indexing
# 
# `GeoPandas` inherits the standard `Pandas` methods for indexing/selecting data. We can use integer position based indexing (`iloc`) to select rows:

# In[104]:


gdf.iloc[3:6]


# In[105]:


gdf.iloc[30]


# It is also possible to select a subset of data based on a **mask**, with the syntax `df[df['column_name'] == 'some value']`. This operation selects only the rows where this condition is true:

# In[114]:


gdf[gdf['NAME'] == 'Oregon']


# Sometimes we might want to select rows where a column value is in **list** of values

# In[117]:


western_states = ['Oregon', 'Washington', 'California']
gdf[gdf['NAME'].isin(western_states)]


# In[63]:


# Select all states with an area larger than 3.5e+11 m2
gdf[gdf['area'] > 3.5e+11]


# In[62]:


# Plot all states with an area larger than 2.5e+11 m2
gdf[gdf['area'] > 3.5e+11].plot()


# ## Projections
# 
# `GeoDataFrames` have their own **Coordinate Reference System (CRS)** which can be accessed using the [`crs`](https://geopandas.org/en/stable/docs/user_guide/projections.html) method. The CRS tells `GeoPandas` where the coordinates of the geometries are located on the Earth's surface. If we run this on our data, we will see that it has an **Albers Equal Area** projection.

# In[64]:


gdf.crs


# We can reproject a our data using the `to_crs` method.

# In[66]:


gdf_reproject = gdf.to_crs('EPSG:4326')
gdf_reproject.crs


# ```{tip}
# It is recommended to use an EPSG code for specifying projections. We can find the right EPSG code using this site: https://epsg.io/
# ```

# Now we will see that our `geometry` column contains longitudes and latitudes (i.e. in degrees). It also looks a bit different when we plot it (also note the x- y-axis scales). 

# In[69]:


gdf_reproject.head()


# In[70]:


gdf_reproject.plot()


# ```{note}
# Sometimes `GeoPandas` won't recognize the EPSG code. In this case, we can navigate to [epsg.io](https://epsg.io/) and use the projection **description** to reproject the data. If there isn't a description, scroll down to `PROJ.4` in the **Export** menu and copy and paste from there. 
# ```

# In[128]:


# Reproject to World Eckert IV (https://epsg.io/54012)
proj = '+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'
gdf_reproject = gdf_reproject.to_crs(proj)
gdf_reproject.plot()


# ## Writing files
# 
# We can write a `GeoDataFrame` back to file using `GeoDataFrame.to_file()`. The default file format is a **shapefile**. Note that we can only have one `geometry` column so we drop the `centroid` column before writing.

# In[96]:


gdf_reproject.drop(columns=['centroid']).to_file('data/us_states_wgs84.shp')

