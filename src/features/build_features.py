
#%%
import pandas as pd
import geopandas as gpd
import matplotlib as plt

#%%
parks = gpd.read_file("../../data/raw/Park Lands - Recreation and Parks Department.geojson")
parks.loc[:, ['x', 'y']] = parks.loc[:, ['x', 'y']].apply(lambda x: x.astype('double'))
parks = parks[(parks['x'] < -122.0)]

#%%
trees = pd.read_csv("../../data/raw/Street_Tree_List.csv")
trees = gpd.GeoDataFrame(trees, geometry = gpd.points_from_xy(trees.Longitude, trees.Latitude))
trees = trees[(trees['Latitude'] > 37.65) & (trees['Latitude'] < 40)]

#%%
ax = parks.plot(color = "white", edgecolor = "black")
trees.head(100).plot(ax = ax, color = "green")

# %%
