import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

response = requests.get("http://127.0.0.1:5000/salaries")
todos = json.loads(response.text)

for item in todos["items"]:
    print(item)

df = pd.DataFrame(todos['items'])
print (df)
#
#
# df.plot(x=int'CODGEO', y='SNHM14')