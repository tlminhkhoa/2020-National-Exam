import json 
import pandas as pd
Coordinate = pd.read_csv("../Data/Coordinate.csv",index_col = 0)
Citys = pd.read_csv("../Data/Citys.csv")
# Citys = Citys.drop(["Region"],axis = 1)
# Coordinate["Name"] = Coordinate["Name"].map(lambda name: name.replace("Sở GDĐT","").strip())
# Coordinate
# print(Coordinate.head())
# print(Citys)
def countCategory(row):
    if row["Province"] in list(Coordinate["Name"]):
        row["Region"] = Coordinate[row["Province"] == Coordinate["Name"]]["Region"].values[0]
        # print(Coordinate[row["Name"] == Coordinate["Name"]]["Region"].values)
    return row

# Citys = Citys.apply(countCategory, axis='columns')
print(Citys[ (Citys["Region"].notna())].iloc[:,3:])
Citys[ (Citys["Region"].notna())].iloc[:,3:].to_csv("../Data/Citys_1.csv",encoding='utf-8-sig',index=False)