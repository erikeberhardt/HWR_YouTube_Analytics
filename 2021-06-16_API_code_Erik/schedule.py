#import the actual script, which yields the API data
import Erik_most_trending_videos as origin
import time

#initiate loop variable to count, how often data has been collected already
loop = 0

#create infinite loop
while True:
    #run the API script
    origin.get_data()
    #add 1 to the loop variable
    loop = loop +1
    #print the loop variable
    print("This is loop number " + str(loop) +".")
    #wait for 15 minutes to download the next dataset
    time.sleep(1)
