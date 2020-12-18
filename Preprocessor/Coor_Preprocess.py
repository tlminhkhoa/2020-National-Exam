import json 
import pandas as pd
geojsonVn = json.load(open("../Data/vietnam.geojson","r",encoding="utf8"))

Coordinate = pd.read_csv("../Data/Coordinate.csv",index_col = 0)
Coordinate["Name"] = Coordinate["Name"].map(lambda name: name.replace("Sở GDĐT","").strip())
# Coordinate

def countCategory(row):
    for i in range(63):
        if (geojsonVn["features"][i]["properties"]["name"] in row["Name"]):
            row["id"] = geojsonVn["features"][i]["properties"]["id_1"]
    return row

Coordinate = Coordinate.apply(countCategory, axis='columns')
Coordinate.to_csv("../Data/Coordinate.csv",encoding='utf-8-sig')