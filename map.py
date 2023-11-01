import folium
import json

# Sample city data
cities = [{"name": "Dallas", "lat": 32.7767, "lon": -96.7970},
          {"name": "Washington, DC", "lat": 38.9072, "lon": -77.0369}, 
          {"name": "London", "lat": 51.5074, "lon": -0.1278}]

# Create map object
m = folium.Map(location=[48, -102], zoom_start=3)

# Loop through cities and add to map
for city in cities:
    folium.Marker([city['lat'], city['lon']], popup=city['name']).add_to(m)

# Save to html file
m.save('map.html')
