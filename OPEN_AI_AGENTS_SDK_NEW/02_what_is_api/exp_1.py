# 1. Get current weather for London (Simple api call )

import requests, pprint

url = "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"

resp = requests.get(url, timeout=10)

resp.raise_for_status()
weather = resp.json()
pprint.pp(weather)