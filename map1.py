import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
coor = data.loc[:,"LAT":"LON"].to_numpy().tolist() 
elev = list(data["ELEV"]) 
name = list(data["NAME"])

# Used in the volanoes feature group to determine color for the marker
def color_producer(elevation):    
    if elevation < 1000:
        return "green"
    elif elevation >= 1000 and elevation < 3000:
        return "orange"
    else:
        return "red"

# Create the html for the map 
map = folium.Map([38.58, -99.09], zoom_start=5, tiles="Stamen Terrain") 

# Create markers for volcanoes 
fgv = folium.FeatureGroup("Volcanoes")
for cr, el, nm in zip(coor, elev, name):
    fgv.add_child(folium.CircleMarker(location=cr, popup= f"{nm}\n{str(el)}m", color="gray", fill=True, fill_color=color_producer(el),  radius=6, fill_opacity=1))

# Add polygons to draw out the borders for different countries of the world
fgp = folium.FeatureGroup("Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())
map.save("Map1.html")