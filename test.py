import requests

BASE = 'http://127.0.0.1:5000/'#'https://api-test-01010101.uc.r.appspot.com/'

#response = requests.post(BASE + 'traces', {'ip': '57.11.255'})
response = requests.get(BASE + 'statistics')
print(response.json())