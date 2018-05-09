#!python
#
# proof of concept
# Patrick O'Keeffe

from datetime import datetime

import re
import requests


qd = datetime(2018, 5, 8) # query date

# directories
base_uri = "http://lar.wsu.edu/airpact/gmap/ap5/images/anim/"
species_dir = base_uri + "species/{date:%Y}/{date:%Y_%m_%d}/"
resource_dir = base_uri + "date_time_labels/"


def get_available_species(date):
    # parse index.htm and extract unique file groups
    indexhtm = requests.get(species_dir.format(date=date)).text

    # locate gif images name in index.htm & extract species group
    pattern = "airpact5_(?:AQIcolors_)?(\w*)_[0-9]{10}.gif"
    #pattern = "airpact5_AQIcolors_(\w*)_[0-9]{10}.gif"
    groups = re.findall(pattern, indexhtm)
    species = set(groups)

    return species

print(get_available_species(qd))
