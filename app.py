import json
import requests
from flask import Flask, render_template, request, jsonify
import overpy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/isochrone', methods=['POST'])
def isochrone():
    lat = request.json['lat']
    lon = request.json['lon']
    time=request.json['sec']
    body = {"locations":[[lon, lat]], "range":[time]}
    headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf62481f76dd5c81854ae397bae1120473197e',
    'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://api.openrouteservice.org/v2/isochrones/driving-car', json=body, headers=headers)

    data = json.loads(call.text)
    return jsonify(data)
@app.route('/pizza-restaurants', methods=['GET', 'POST'])
def pizza_restaurants():
    if request.method == 'POST':
        api = overpy.Overpass()

        # Define the Overpass query to search for restaurants selling pizza in Bengaluru
        overpass_query = """
        area[name="Bengaluru"]->.searchArea;
        node(area.searchArea)[cuisine=pizza];
        out;
        """

        # Make the request to Overpass API
        result = api.query(overpass_query)

        restaurants = []
        for node in result.nodes:
            
            restaurant = {
                'name': node.tags['name'],
                'lat': node.lat,
                'lon': node.lon
            }
            restaurants.append(restaurant)
        

        return jsonify(restaurants)

    return "This route only supports POST requests."
@app.route('/flood-prone-areas', methods=['GET','POST'])
def get_flood_prone_nodes():

    api = overpy.Overpass()
    query = '''
        [out:json];
        area[name="Bengaluru"]->.searchArea;
        (
            node(area.searchArea)["natural"="wetland"];
            node(area.searchArea)["waterway"="riverbank"];
            node(area.searchArea)["landuse"="reservoir"];
            node(area.searchArea)["waterway"="river"];
        );
        out body;
        '''
    result = api.query(query)
    
    nodes = []
    for node in result.nodes:
        nodes.append({
            'id': node.id,
            'lat': node.lat,
            'lon': node.lon
        })
    
    return jsonify(nodes)

@app.route('/geojson')
def get_geojson():
    return app.send_static_file('BBMP.GeoJSON')





if __name__ == '__main__':
    app.run()
