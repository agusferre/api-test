import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.post(BASE + 'traces', {'ip': '181.95.44.68'})
print(response.json())