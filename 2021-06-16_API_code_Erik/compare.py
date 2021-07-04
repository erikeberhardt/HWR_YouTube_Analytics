import pandas as pd
import os
from os import listdir
import numpy as np

#get all files in directory and store them in a list
#TO_EDIT: You would also have to change this path to your directory. As far as I'm aware, paths can be written
#differently on a mac, so you might need to adjust this @Tuna :)
mypath = r"C:\Users\Erik\Documents\GitHub\big_data_youtube\2021-06-16_API_code_Erik\Trending_Videos_Erik\\"

#create a list with all filenames
files = np.sort([f for f in listdir(mypath)])


#create empty df list
dataframes_list = []

#for every filename in the folder (so every data.csv that has been downloaded)
for item in files:
    #import it as a dataframe
    temp_df = pd.read_csv(mypath + item)
    #safe this dataframe to the dataframes_list
    dataframes_list.append(temp_df)

#here I am comparing every dataframe with each other. As they are sorted already when being imported
#I can always compare df at position i with df at position i+1

#for the number of files in the directory
for i in range(len(dataframes_list)):
    #if the file at position i+1 still exists
    if i+1 <= len(dataframes_list)-1:
        #compare whether the first column of dataframe at position i equals the first column of dataframe at
        #position i+1
        #returns either True or False
        x = dataframes_list[i].iloc[:,0].equals(dataframes_list[i+1].iloc[:,0])
        #If True is returned (meaning they are the same)
        if x:
            #remove the respective file at position i because the file at i+1 is newer, therefore more up2date but
            #has the same structure
            #as the files list and the dataframes_list are ordered exactly the same,
            #the position of i refers to both lists
            os.remove(mypath + files[i])
        #print which dfs were the same and which ones were different

        #remove all dfs, which have a length = 0
        y = len(dataframes_list[i])

        if y == 0:
            os.remove(mypath + files[i])

        print(i, i+1, x)
    else:
        pass