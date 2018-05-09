#!python
#
# proof of concept
# Patrick O'Keeffe

from datetime import datetime

import re
import requests, urllib

import imageio


qd = datetime(2018, 5, 8) # query date

# directories
base_uri = "http://lar.wsu.edu/airpact/gmap/ap5/images/anim/"
species_dir = base_uri + "species/{date:%Y}/{date:%Y_%m_%d}/".format(date=qd)
resource_dir = base_uri + "date_time_labels/"

# source file list
indexhtm = requests.get(species_dir).text


def get_available_species(date):
    """parse index.htm and extract unique file groups"""
    # locate gif image names in index.htm & extract species groups
    #pattern = "airpact5_(?:AQIcolors_)?(\w*)_[0-9]{10}.gif"
    pattern = "airpact5_AQIcolors_(\w*)_[0-9]{10}.gif"
    groups = re.findall(pattern, indexhtm)
    return sorted(list(set(groups)))


def get_available_images(date, species):
    """extract entire file names for single species from index.htm"""
    # locate entire file names
    pattern = "(airpact5_AQIcolors_{species}_[0-9]{{10}}.gif)".format(species=species)
    groups = re.findall(pattern, indexhtm)
    
    return groups


species = get_available_species(qd) #limited to "24hrPM25" and "8hrO3"
spec = species.pop()
files = get_available_images(qd, spec)

print(species)
print(files[:3])

images = []
for f in files:#[:1]:
    print(species_dir+f)
    local_file = '/tmp/'+f
    urllib.request.urlretrieve(species_dir+f, local_file)

    images.append(imageio.imread(local_file))

imageio.mimsave(spec+".gif", images)




