import requests

BASE = 'https://api-test-01010101.uc.r.appspot.com/' #'http://127.0.0.1:5000/'

response = requests.post(BASE + 'traces', {'ip': '57.74.111.255'})
#response = requests.get(BASE + 'statistics')
print(response.json())