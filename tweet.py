#!/home/patrick/anaconda3/bin/python
#
# posts thread of tweets with GIFs
#
# Patrick O'Keeffe

import sys, os.path as osp
import tweepy

from datetime import datetime

from creds import *

source_dir = sys.argv[1]


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


import random
num = random.randint(0,1000)


if __name__=="__main__":

    pm25_mass_gif = osp.join(source_dir, "PM25.gif")
    pm25_aqi_gif  = osp.join(source_dir, "AQIcolors_24hrPM25.gif")
    if not (osp.isfile(pm25_mass_gif) or osp.isfile(pm25_aqi_gif)):
        raise Exception("Could not locate source GIFs in {}".format(source_dir))    

    now = datetime.now()
    # h/t: https://stackoverflow.com/a/739266/2946116
    if 4 <= now.day <= 20 or 24 <= now.day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][now.day % 10 - 1]
    daystr = "{day}{suffix}".format(day=str(now.day),suffix=suffix)
    datestr = datetime.strftime(now, "%A, %B {day}, %Y".format(day=daystr))
    
    hellomsg = "Good morning! It's {date}".format(date=datestr)
    
    
    post = api.update_status(hellomsg)

    if osp.isfile(pm25_mass_gif):
        print("Uploading PM2.5 mass file: {}".format(pm25_mass_gif))
        pm25_mass = api.media_upload(pm25_mass_gif)
        post = api.update_status("PM2.5",
                                 in_reply_to_status_id=post.id,
                                 media_ids=[pm25_mass.media_id])

    if osp.isfile(pm25_aqi_gif):
        print("Uploading PM2.5 AQI color file: {}".format(pm25_aqi_gif))
        pm25_aqi = api.media_upload(pm25_aqi_gif)
        post = api.update_status("PM2.5 (AQI colors)",
                                 in_reply_to_status_id=post.id,
                                 media_ids=[pm25_aqi.media_id])

    if osp.isfile(osp.join(source_dir, "HCHO.gif")):
        print("Uploading HCHO color file: {}".format(osp.join(source_dir, "HCHO.gif")))
        hcho = api.media_upload(osp.join(source_dir, "HCHO.gif"))
        post = api.update_status("HCHO",
                                 in_reply_to_status_id=post.id,
                                 media_ids=[hcho.media_id])
        
    if osp.isfile(osp.join(source_dir, "O3.gif")):
        print("Uploading O3 color file: {}".format(osp.join(source_dir, "O3.gif")))
        o3 = api.media_upload(osp.join(source_dir, "O3.gif"))
        post = api.update_status("O3",
                                 in_reply_to_status_id=post.id,
                                 media_ids=[o3.media_id])

    



