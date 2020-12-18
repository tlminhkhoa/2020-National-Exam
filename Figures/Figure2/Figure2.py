import pandas as pd 
df = pd.read_csv("..//..//Data//csv//2020_National_ENG.csv",index_col = 0)

df = df[["English","Region"]]

df_dropout = df.groupby('Region').count().rsub(df.groupby('Region').size(), axis=0)

percent = df_dropout/df.groupby('Region').count()
# print(df.groupby('Region').count())

percent.to_csv("English_dropout.csv")