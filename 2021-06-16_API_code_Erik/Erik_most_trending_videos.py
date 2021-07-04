#importing libraries
import requests
import sys
import time
import os
import numpy as np

#preparation
unsafe_characters = ['\n', '"']

snippet_features =  ["title",
                    "publishedAt", #where does this come from?
                    "channelId",
                    "channelTitle", #where does this come from?
                    "categoryId"]

header = ["video_id"] + snippet_features + ["trending_date", "tags", "view_count", "likes", "dislikes",
                                            "comment_count", "thumbnail_link", "comments_disabled",
                                            "ratings_disabled", "description"] + ["category_name"] + ["country"]

#TO_EDIT: my API Key
api_key = "AIzaSyCLlldC_cTBAVSzzEY2oEWV6B35cVRBlik"
#TO_EDIT: the list of the country codes
country_codes = ["GB","AU","US", "CA", "IE"]

#from here on the code is based on the github repo (except for the path in the write function in the end)
#actual processing
#preparing the features
def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'

#getting the data from the API
def api_request(page_token, country_code):
    global land
    land = country_code
    # Builds the URL and requests the JSON from it
    #actually works
    #https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet&chart=mostPopular&regionCode=US&maxResults=50&key=AIzaSyCLlldC_cTBAVSzzEY2oEWV6B35cVRBlik
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=50&key={api_key}"
    request = requests.get(request_url)
    #we should get status code 200, we can check for this as well
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    #elif request.status_code == 200:
        #print("Yeah, it worked!")
    return request.json()

#piping the tags
def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))

#getting the videos
def get_videos(items):
    lines = []
    for video in items:
        comments_disabled = False
        ratings_disabled = False

        # We can assume something is wrong with the video if it has no statistics, often this means it has been deleted
        # so we can just skip it
        if "statistics" not in video:
            continue

        # A full explanation of all of these features can be found on the GitHub page for this project
        video_id = prepare_feature(video['id'])

        # Snippet and statistics are sub-dicts of video, containing the most useful info
        snippet = video['snippet']
        statistics = video['statistics']

        # This list contains all of the features in snippet that are 1 deep and require no special processing
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]
        ourfeature = features[4].replace('"', '')
        # The following are special case features which require unique processing, or are not within the snippet dict
        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y.%d.%m")
        tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = statistics.get("viewCount", 0)

        conditions = [
            (ourfeature == '2'),
            (ourfeature == '1'),
            (ourfeature == '10'),
            (ourfeature == '15'),
            (ourfeature == '17'),
            (ourfeature == '18'),
            (ourfeature == '19'),
            (ourfeature == '20'),
            (ourfeature == '21'),
            (ourfeature == '22'),
            (ourfeature == '23'),
            (ourfeature == '24'),
            (ourfeature == '25'),
            (ourfeature == '26'),
            (ourfeature == '27'),
            (ourfeature == '28'),
            (ourfeature == '29'),
            (ourfeature == '30'),
            (ourfeature == '31'),
            (ourfeature == '32'),
            (ourfeature == '33'),
            (ourfeature == '34'),
            (ourfeature == '35'),
            (ourfeature == '36'),
            (ourfeature == '37'),
            (ourfeature == '38'),
            (ourfeature == '39'),
            (ourfeature == '40'),
            (ourfeature == '41'),
            (ourfeature == '42'),
            (ourfeature == '43'),
            (ourfeature == '44')]

        choices = ['Autos & Vehicles', 'Film & Animation', 'Music', 'Pets & Animals', 'Sports', 'Short Movies',
                   'Travel & Events', 'Gaming', 'Videoblogging', 'People & Blogs', 'Comedy', 'Entertainment',
                   'News & Politics', 'Howto & Style', 'Education', 'Science & Technology', 'Nonprofits & Activism',
                   'Movies', 'Anime/Animation', 'Action/Adventure', 'Classics', 'Comedy', 'Documentary', 'Drama',
                   'Family', 'Foreign', 'Horror', 'Sci-Fi/Fantasy', 'Thriller', 'Shorts', 'Shows', 'Trailers']

        category_name = [str(np.select(conditions, choices))]
        country = [land]

        # This may be unclear, essentially the way the API works is that if a video has comments or ratings disabled
        # then it has no feature for it, thus if they don't exist in the statistics dict we know they are disabled
        if 'likeCount' in statistics and 'dislikeCount' in statistics:
            likes = statistics['likeCount']
            dislikes = statistics['dislikeCount']
        else:
            ratings_disabled = True
            likes = 0
            dislikes = 0

        if 'commentCount' in statistics:
            comment_count = statistics['commentCount']
        else:
            comments_disabled = True
            comment_count = 0

        # Compiles all of the various bits of info into one consistently formatted line
        line = [video_id] + features + [prepare_feature(x) for x in [trending_date, tags, view_count, likes, dislikes,
                                                                       comment_count, thumbnail_link, comments_disabled,
                                                                       ratings_disabled, description]] + category_name + country

        lines.append(",".join(line))
    return lines

#getting the pages
def get_pages(country_code, next_page_token="&"):
    country_data = []

    # Because the API uses page tokens (which are literally just the same function of numbers everywhere) it is much
    # more inconvenient to iterate over pages, but that is what is done here.
    while next_page_token is not None:
        # A page of data i.e. a list of videos and all needed data
        video_data_page = api_request(next_page_token, country_code)

        # Get the next page token and build a string which can be injected into the request with it, unless it's None,
        # then let the whole thing be None so that the loop ends after this cycle
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

        # Get all of the items as a list and let get_videos return the needed features
        items = video_data_page.get('items', [])
        country_data += get_videos(items)

    return country_data

#writing everything to a file
def write_to_file(country_code, country_data):
    #TO_EDIT: change this directory to the actual folder, where you want the output to be saved
    output_dir = "Trending_Videos_Erik/"
    #if the folder exists, cool, if not, create ti
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #this is the part, which will most likely be changed for saving in HDFS
    with open(f"{output_dir}/{time.strftime('%y_%m_%d_%H_%M_%S')}_videos.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")

#calling all functions to get the data
def get_data():
    finallist = [",".join(header)]
    for country_code in country_codes:
        country_data = get_pages(country_code)
        for row in country_data:
            finallist.append(row)
    write_to_file(country_code, finallist)

#needed, otherwise the script would be executed when imported as python file in another script
if __name__ == "__main__":
    get_data()