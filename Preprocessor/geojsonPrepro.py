import json 
import pandas as pd
geojsonVn = json.load(open("../Data/vietnam.geojson","r",encoding="utf8"))

id_map ={}
for feature in geojsonVn["features"]:
    feature["id"] = feature["properties"]["id_1"]

import json
with open('../Data/geojsonVn.json', 'w') as f:
    json.dump(geojsonVn, f)