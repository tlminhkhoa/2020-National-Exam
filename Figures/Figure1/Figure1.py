import numpy as np
import math
from multiprocessing import Pool,freeze_support
import pandas as pd
num_partitions = 10 #number of partitions to split dataframe
num_cores = 4 # number of core to use 

# function to count each Category each row
def countCategory(row):
    if (not math.isnan(row["ScienceAverage"])) and (not math.isnan(row["SocialAverage"])):
        row["SpeType"] = "Both"
    elif math.isnan(row["ScienceAverage"]) and math.isnan(row["SocialAverage"]):
        row["SpeType"] = "Either"
    elif not math.isnan(row["ScienceAverage"]):
        row["SpeType"] = "Science"
    elif not math.isnan(row["SocialAverage"]):
        row["SpeType"] = "Social"
    return row

# parallelize the df by split it into to many part then give them to the cores
def parallelize_dataframe(df, func):
        df_split = np.array_split(df, num_partitions)
        pool = Pool(num_cores)
        # concat the result together 
        df = pd.concat(pool.map(func, df_split))
        # sum the same row to get all the totall
        df = df.groupby(lambda x:x, axis=0).sum()
        pool.close()
        pool.join()
        return df
# a wrapper for the countCategory function to parallelize
def countCategoryFunction(data):
        SpeType = data.apply(countCategory, axis='columns')["SpeType"].value_counts()
        SpeType = SpeType.sort_values()
        return SpeType 
def figure1Preprocess():
    data = pd.read_csv("..//..//Data//csv//2020_National_ENG.csv",index_col = 0)
    SpeType = parallelize_dataframe(data,countCategoryFunction)
    SpeType.to_csv("SpeType.csv")
if __name__ == '__main__':
    # support for window 
    freeze_support()    
    figure1Preprocess()