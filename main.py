
from flask import Flask, render_template, request
import os
import subprocess
import pandas
import geopandas as gpd 
import folium
import branca.colormap
from folium.plugins import HeatMap
from collections import defaultdict
import vincent, json
from vincent import AxisProperties, PropertySet, ValueRef

app = Flask(__name__)

app.static_folder = 'static'

# Decorater to direct users who access base URL ("/") and serve them output of index()
@app.route("/")
def index():                                # Naming of index() is convention, relating to index.html as main page of a website
    return render_template('index.html')

@app.route("/test")
def test():
    return render_template('home.html')

@app.route("/map")
def go_to_map():
    return render_template('map.html')

@app.route('/', methods=['POST'])
def my_form_post():
    tw_input = request.form['text']
    cwd = os.getcwd()
    os.chmod(cwd+'/twData.py', 0o775)
    result = subprocess.run(['python', cwd+'/twData.py', tw_input], capture_output=True, text=True)
    data = result.stdout
    datalist = [int(e) for e in data.split()]
    makeMap(datalist)
    return render_template('map.html')


def makeMap(tweets):
    data_map = pandas.read_csv('./kaggle_income.csv', sep=',')

    data_map.sort_values('Mean', ascending=False).head()

    data=data_map[['Lat', 'Lon', 'Mean']].groupby(['Lat', 'Lon']).sum().reset_index().values.tolist()

    senti = {'Not Satisfied':tweets[0], 'Moderately Satisfied':tweets[1], 'Very Satisfied':tweets[2]}
    dignity_data = {'Not Satisfied':2, 'Moderately Satisfied':13, 'Very Satisfied':1}
    ucd_data = {'Not Satisfied':4, 'Moderately Satisfied':3, 'Very Satisfied':7}
        
    pie = vincent.Pie(senti,outer_radius=200)
    pie.legend('Tweet Sentiment')
    pie.colors(brew='Accent')

    pie2 = vincent.Pie(dignity_data,outer_radius=200)
    pie2.legend('Tweet Sentiment')
    pie2.colors(brew='Accent')

    pie3 = vincent.Pie(ucd_data,outer_radius=200)
    pie3.legend('Tweet Sentiment')
    pie3.colors(brew='Accent')


    heatmap = folium.Map(location=[37.07, -118.45], zoom_start=5.5, zoom_control=True,)

    HeatMap(data=data_map[['Lat', 'Lon', 'Mean']].groupby(['Lat', 'Lon']).sum().reset_index().values.tolist(), min_opacity=3.2, radius=8.0, max_zoom=13).add_to(heatmap)

    # Let's create a Vega popup based on pie chart
    popup1 = folium.Popup()
    folium.Vega(pie).add_to(popup1)

    popup2 = folium.Popup()
    folium.Vega(pie2).add_to(popup2)

    popup3 = folium.Popup()
    folium.Vega(pie3).add_to(popup3)

    locations = {'UCLA': [34.07, -118.44], 'Stockton': [38.577,-121.76], 'USC': [34.02, -118.28]}

    #folium.Marker(locations['UCLA'], popup=popup).add_to(heatmap)
    
    folium.CircleMarker(
    location=locations['UCLA'],
    radius=15,
    popup=popup1,
    color="#8131cc",
    fill=True,
    fill_color="#3186cc",
    ).add_to(heatmap)

    folium.CircleMarker(
    location=locations['USC'],
    radius=15,
    popup=popup2,
    color="#8131cc",
    fill=True,
    fill_color="#3186cc",
    ).add_to(heatmap)

    folium.CircleMarker(
    location=locations['Stockton'],
    radius=15,
    popup=popup3,
    color="#8131cc",
    fill=True,
    fill_color="#3186cc",
    ).add_to(heatmap)

    heatmap.save('./templates/map.html')


if __name__ == "__main__":
    app.run(debug=True)



