from os import stat
from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
import geopy.distance

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)

api_args = reqparse.RequestParser()
api_args.add_argument('ip', type=str, required=True)

class traces(Resource):
    def post(self):
        ip = api_args.parse_args().ip
        queryParameters = '?fields=status,message,country,countryCode,lat,lon,currency'
        ipResponse = requests.get('http://ip-api.com/json/' + ip + queryParameters).json()
        countryCode = ipResponse['countryCode']
        countryResponse = requests.get('https://restcountries.eu/rest/v2/alpha/' + countryCode).json()
        if ipResponse['status'] == 'success' and 'name' in countryResponse:
            data = {
                'ip': ip,
                'name': ipResponse['country'],
                'code': countryCode,
                'lat': ipResponse['lat'],
                'lon': ipResponse['lon'],
                'currencies': parseCurrencies(countryResponse),
                'distance_to_uy': getDistanceToUy(countryResponse['latlng']) # I used the API response lat and lon as the statement asked for the countries distance, but I would have used the ip location instead.
            }
        return data

class statistics(Resource):
    def get(self):
        data = {
            'longest_distance': {
                'country': '',
                'value': 0
            },
            'most_traced': {
                'country': '',
                'value':
            }
        }
        return data

def parseCurrencies(obj):
    res = []
    for cur in obj['currencies']:
        iso = cur['code'].upper()
        convResponse = requests.get('https://free.currconv.com/api/v7/convert?q=' + iso + '_USD&compact=ultra&apiKey=ce495e6638ff9c9dc43f').json()
        if iso + '_USD' in convResponse:
            temp =  {
                'iso': iso,
                'symbol': cur['symbol'],
                'conversion_rate': round(convResponse[iso + '_USD'], 3)
            }
            res.append(temp)
    return res

def getDistanceToUy(point):
    point = tuple(point)
    print(point)
    uyPoint = (-33, -56) #(-32.559, -55.812)
    return round(geopy.distance.distance(point, uyPoint).km, 2)

api.add_resource(traces, '/traces')
api.add_resource(statistics, '/statistics')