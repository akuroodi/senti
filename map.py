import pandas
import geopandas as gpd 
import folium
import branca.colormap
from folium.plugins import HeatMap
from collections import defaultdict
import vincent, json
from vincent import AxisProperties, PropertySet, ValueRef

# Init
data_map = pandas.read_csv('./kaggle_income.csv', sep=',')

data_map.sort_values('Mean', ascending=False).head()

data=data_map[['Lat', 'Lon', 'Mean']].groupby(['Lat', 'Lon']).sum().reset_index().values.tolist()


ncounter = 67
neutralCounter = 93
pcounter = 80

# Try vincent pie chart if it looks better
UCLA_pie = {'Not satisfied':ncounter, 'Moderately satisfied':neutralCounter, 'Very Satisfied':pcounter}
pie = vincent.Pie(UCLA_pie,outer_radius=200)
pie.legend('Tweet Sentiment')
pie.colors(brew='Set3')


heatmap = folium.Map(location=[37.07, -118.45], zoom_start=5.5,)

HeatMap(data=data_map[['Lat', 'Lon', 'Mean']].groupby(['Lat', 'Lon']).sum().reset_index().values.tolist(), min_opacity=3.2, radius=8.0, max_zoom=13).add_to(heatmap)

# Let's create a Vega popup based on pie chart
popup = folium.Popup()
folium.Vega(pie).add_to(popup)

locations = {'UCLA': [34.07, -118.44], 'Stockton': [38,-120.5]}

folium.Marker(locations['UCLA'], popup=popup).add_to(heatmap)


heatmap.save('./templates/map.html')