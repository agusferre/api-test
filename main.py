from flask import Flask
from flask_restful import Api, Resource, reqparse
from google.cloud import bigquery
import pandas as pd
import requests
import geopy.distance

app = Flask(__name__)
api = Api(app)
api_args = reqparse.RequestParser()
api_args.add_argument('ip', type=str, required=True)

project_id = 'api-test-01010101'
dataset_id = 'api_ds'
table_id = project_id + '.' + dataset_id + '.' + 'api_db'
client = bigquery.Client(project=project_id)

class traces(Resource):
    def post(self):
        try:
            ip = api_args.parse_args().ip
            queryParameters = '?fields=status,message,country,countryCode,lat,lon,currency'
            ipResponse = requests.get('http://ip-api.com/json/' + ip + queryParameters).json()
            countryCode = ipResponse['countryCode']
            countryResponse = requests.get('https://restcountries.eu/rest/v2/alpha/' + countryCode).json()
            data = {
                'ip': ip,
                'name': ipResponse['country'],
                'code': countryCode,
                'lat': ipResponse['lat'],
                'lon': ipResponse['lon'],
                'currencies': parseCurrencies(countryResponse),
                'distance_to_uy': getDistanceToUy(countryResponse['latlng'])
            }
            bq_row = [{
                'country': data['name'],
                'distance': data['distance_to_uy']
            }]
            table_id = project_id + '.' + dataset_id + '.' + 'api_db'
            client.insert_rows_json(table_id, bq_row)
        except:
            data = {'status': 'Error', 'message': 'Wrong IP address'}
        return data

class statistics(Resource):
    def get(self):
        try:
            distance_query = """SELECT country, distance FROM `api-test-01010101.api_ds.api_db` GROUP BY country, distance ORDER BY distance desc"""
            dis_df = client.query(distance_query).result().to_dataframe().head(1)
            requests_query = """SELECT country, COUNT(country) count FROM `api-test-01010101.api_ds.api_db` GROUP BY country ORDER BY count desc"""
            req_df = client.query(requests_query).result().to_dataframe().head(1)
            data = {
                'longest_distance': {
                    'country': dis_df['country'].values[0],
                    'value': dis_df['distance'].values[0]
                },
                'most_traced': {
                    'country': req_df['country'].values[0],
                    'value': int(req_df['count'].values[0])
                }
            }
        except:
            data = {'status': 'Internal Server Error', 'message': 'Database related error'}
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
    uyPoint = (-33, -56)
    return round(geopy.distance.distance(point, uyPoint).km, 2)

api.add_resource(traces, '/traces')
api.add_resource(statistics, '/statistics')