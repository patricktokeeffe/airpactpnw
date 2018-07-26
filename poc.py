#!python
#
# proof of concept
# Patrick O'Keeffe

from datetime import datetime
import os

import re
import requests, urllib

import imageio
from PIL import Image, ImageFont, ImageDraw


qd = datetime.now()#(2018, 5, 6) # query date

# directories
base_uri = "http://lar.wsu.edu/airpact/gmap/ap5/images/anim/"
species_dir = base_uri + "species/{date:%Y}/{date:%Y_%m_%d}/".format(date=qd)
resource_dir = base_uri + "date_time_labels/"

# source file list
indexhtm = requests.get(species_dir).text


def get_available_species(date):
    """parse index.htm and extract unique file groups"""
    # all groups, with "AQIcolors" prefix excluded
    pattern = "airpact5_(?:AQIcolors_)?(\w*)_[0-9]{10}.gif"
    # only "AQIcolors"
    #pattern = "airpact5_AQIcolors_(\w*)_[0-9]{10}.gif"
    groups = re.findall(pattern, indexhtm)
    return sorted(list(set(groups)))


def get_available_images(date, species):
    """extract entire file names for single species from index.htm"""
    # all groups, with "AQIcolors" prefix excluded
    pattern = "(airpact5_(?:AQIcolors_)?{species}_[0-9]{{10}}.gif)".format(species=species)
    # only "AQIcolors"
    #pattern = "(airpact5_AQIcolors_{species}_[0-9]{{10}}.gif)".format(species=species)
    groups = re.findall(pattern, indexhtm)
    
    return groups


species = get_available_species(qd) #limited to "24hrPM25" and "8hrO3"
#spec = '24hrPM25' #species.pop()
spec = 'PM25'
img_list = sorted(list(set(get_available_images(qd, spec))))

print(species)
print(img_list)

#imgsize = (863, 751)
#imgsize = (432, 376)
#imgsize = (345, 300)
imgsize = (259, 225)
background = Image.open('img/map_bg.png').resize(imgsize, Image.LANCZOS)
datefont = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
titlefont = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
title = "AIRPACT PM2.5"

img_files = []
if len(os.listdir('tmp/')):
    print('found downloaded files... proceeding')
    img_files = ['tmp/'+f for f in sorted(os.listdir('tmp/'))]
else:
    print('downloading source files...')
    for img_name in img_list:#[:1]:
        local_file = 'tmp/'+img_name
    
        # download image from webserver
        urllib.request.urlretrieve(species_dir+img_name, local_file)
        img_files.append(local_file)

    
gif_frames = []
for f in img_files:
    # overlay on map background
    fg = Image.open(f).convert('RGBA')
    
    fg = fg.resize(imgsize, Image.LANCZOS)
    bg = background.copy()
    bg.paste(fg, (0,0), fg)

    # overlay timestamp label
    draw = ImageDraw.Draw(bg)
    ts = datetime.strptime(f[-14:], "%Y%m%d%H.gif")
    tslbl = ts.strftime("%a, %b %e %Y, %I %p")
    w, h = draw.textsize(tslbl, font=datefont)
    draw.text(((imgsize[0]-w)/2, imgsize[1]-h-15), tslbl, (20,20,20), font=datefont)

    # and a title
    w, h = draw.textsize(title, font=titlefont)
    draw.text(((imgsize[0]-w)/2,10), title, (20,20,20), font=titlefont)

    bg.save(local_file, optimize=True) #overwrites
    gif_frames.append(imageio.imread(local_file))

imageio.mimsave(spec+".gif", gif_frames)




