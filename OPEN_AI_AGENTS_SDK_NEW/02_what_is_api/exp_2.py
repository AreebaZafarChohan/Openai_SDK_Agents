# 2. Swap endpoint: Cat Fact

import requests 

url = "https://catfact.ninja/fact"
resp = requests.get(url, timeout=10)
resp.raise_for_status()
print(resp.json()["fact"])