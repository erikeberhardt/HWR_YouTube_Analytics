import glob
import pandas as pd
import time

path = r"C:\Users\Erik\Dropbox\Uni\Big Data Enterprise Architectures\01 Project\YouTube\Trending_Videos_Erik\\"
all_files = glob.glob(path + "/*.csv")

#Combine all file and create country column
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df['country'] = filename[100:102] #manual depend on your path
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
#frame = frame.drop_duplicates()

#write back to csv
frame.to_csv(str(time.strftime('%y_%m_%d_%H_%M_%S')) +"_all_videos.csv", encoding='utf-8', index=False)