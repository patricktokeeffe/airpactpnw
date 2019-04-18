#!/home/patrick/anaconda3/bin/python
#
# posts thread of tweets with GIFs
#
# Patrick O'Keeffe

import sys, os.path as osp
import tweepy

from creds import *

source_dir = sys.argv[1]


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)





if __name__=="__main__":

    pm25_mass_gif = osp.join(source_dir, "PM25_lossy.gif")
    pm25_aqi_gif  = osp.join(source_dir, "AQIcolors_24hrPM25_lossy.gif")
    if not (osp.isfile(pm25_mass_gif) or osp.isfile(pm25_aqi_gif)):
        raise Exception("Could not locate source GIFs in {}".format(source_dir))    

    post = api.update_status("Good morning! Ready for more AIRPACT?")

    if osp.isfile(pm25_mass_gif):
        print("Uploading PM2.5 mass file: {}".format(pm25_mass_gif))
        pm25_mass = api.media_upload(pm25_mass_gif)
        api.update_status("",
                          in_reply_to_status_id=post.id,
                          media_ids=[pm25_mass.media_id])

    if osp.isfile(pm25_aqi_gif):
        print("Uploading PM2.5 AQI color file: {}".format(pm25_aqi_gif))
        pm25_aqi = api.media_upload(pm25_aqi_gif)
        api.update_status("",
                          in_reply_to_status_id=post.id,
                          media_ids=[pm25_aqi.media_id])


    



