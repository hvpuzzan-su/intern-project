
import pandas as pd
import os
import folium
from folium.plugins import HeatMap
import numpy as np
import branca.colormap as cm
import re

##########################################################
infile1 = "\\\pnchfsdg17\\CCA_TEAM\\Fraud\\terrorism\\output\\predictions\\nyc_target_from_Sashi_20180504_modelversion3.csv"
# infile1 = "E:\\project\\Terrorism\\modeling_code\\NYC_train_all_test_grid_lat_long_20180501_w_yr_v1.csv"

outfile1 = "\\\pnchfsdg17\\CCA_TEAM\\Fraud\\terrorism\\output\\maps\\"
for_map = pd.read_csv(infile1, encoding = "ISO-8859-1")
for_map = for_map.fillna('')

locations = for_map[['latitude', 'longitude']]
locationlist = locations.values.tolist()
len(locationlist)

linear = cm.LinearColormap(
    ['yellow', 'orange','red', 'red'],
    index=[0, 0.1, 0.5, 1.0]
)

hmap = folium.Map(location=[40.7484, -73.9857], zoom_start=13)  
fg = folium.FeatureGroup(name = "NYC targets")  
for point in range(0, len(locationlist)):
    fg.add_child(folium.CircleMarker(location = locationlist[point], 
                                     radius = 4,
                                     fill= True,
                                     fill_color = linear(for_map['y_pred'][point]),
                                     popup = (
                                                "{name}<br>"
                                                "Category: {category}<br>"
                                                "Score: {score}<br>"
                                                "Note: {note}"
                                               ).format(name=re.sub(r"[^a-zA-Z0-9_]+", ' ', for_map['TARGETNAME'][point]),
                                                        score=str(round(for_map['y_pred'][point], 3)),
                                                        category=for_map['CATEGORYNAME'][point],
                                                        note=for_map['NOTES'][point]
                                                        ),      
                                     color =linear(for_map['y_pred'][point]),
                                     opacity = 0.7,
                                     fill_opacity = 0.7))
hmap.add_child(fg)
hmap.save(os.path.join(outfile1, 'nyc_target_from_Sashi_20180504_modelversion3.html'))

