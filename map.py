__author__ = 'ryantiffany'
import folium 
from flask import Flask, render_template
import os
import ibm_vpc
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from geopy.geocoders import Nominatim

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

regions = [
    {"region_name": "us-south", "city_name": "Dallas"},
    {"region_name": "us-east", "city_name": "Washington"},
    {"region_name": "ca-tor", "city_name": "Toronto"},
    {"region_name": "br-sao", "city_name": "Sao Paulo"},
    {"region_name": "eu-gb", "city_name": "London"},
    {"region_name": "eu-de", "city_name": "Frankfurt"},
    {"region_name": "jp-osa", "city_name": "Osaka"},
    {"region_name": "jp-tok", "city_name": "Tokyo"},
    {"region_name": "au-syd", "city_name": "Sydney"}
]

def build_city_coordinates():
    geolocator = Nominatim(user_agent="my_app")

    cities = []
    for region in regions:
        location = geolocator.geocode(region['city_name'])
        lat = location.latitude
        lon = location.longitude
        cities.append({"name": location, "lat": lat, "lon": lon, "region_name": region['region_name'], "city_name": region['city_name']}) 
    
    return cities

app = Flask(__name__)


@app.route('/')
def map():
    # Get city coordinates
    cities = build_city_coordinates()
    html = """
    <form>
    <label>Name:</label><br>
    <input type="text" name="name"><br>
    
    <label>Email:</label><br>
    <input type="email" name="email"><br>

    <input type="submit" value="Submit">
    </form> 
    """

    popup = folium.Popup(html, max_width=300)

    # Create map 
    map = folium.Map(location=[48, -102], zoom_start=4)
    
    # Add city markers
    for city in cities:
        folium.Marker([city['lat'], city['lon']], popup=city['name']).add_to(map).add_child(popup)

    map.save('templates/map.html')

    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True, port=5555)