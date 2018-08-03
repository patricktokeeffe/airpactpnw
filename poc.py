#!python
#
# proof of concept
# Patrick O'Keeffe

import os, os.path as osp
from glob import glob

import imageio
from PIL import Image, ImageFont, ImageDraw

####
from datetime import datetime
import re
import requests, urllib

class Airpact():
    def __init__(self, date=None):
        """Encapsulate AIRPACT-specific knowledge in a class
        
        Params
        ------
        date : datetime.datetime, optional
            If `date` is `None`, initalizes AIRPACT metadata assuming current
            date from local computer clock
        """
        self._server_uri = "http://lar.wsu.edu/airpact/gmap/ap5/images/anim/"

        self._gif_map_bg = 'img/map_bg.png'
        self._gif_map_dims = (505, 439)
        self._gif_font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        self._gif_resize_f = Image.LANCZOS
        
        self._indexhtm = ""
        self._cache_dir_base = 'tmp'
        self._cache_dir_srcs = 'img_sources'
        self._cache_dir_gifs = 'gif_frames'
        self._cache = {}
        
        self._sources = {
            # HINT key is overlay name, gets used in certain string subs
            #
            # SPECIES
            #'08hrO3': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'24hrPM25': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'ANO3': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'AOD': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'AOMIJ': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            'AQIcolors_08hrO3': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
                                 'overlay_file': 'airpact5_{name}_{date}.gif',
                                 'overlay_date_fmt': '%Y%m%d%H',
                                 'overlay_date_re': '[0-9]{10}',
                                 'label_long': 'Ozone 8hr average',
                                 'label_abbv': 'O3-8hr',
                                 'label_unit': 'ppb',
                                 'desc': '8hr avg #ozone conc (#AQI colors)'},
            'AQIcolors_24hrPM25': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
                                 'overlay_file': 'airpact5_{name}_{date}.gif',
                                 'overlay_date_fmt': '%Y%m%d%H',
                                 'overlay_date_re': '[0-9]{10}',
                                 'label_long': 'Fine particulate',
                                 'label_abbv': 'PM2.5-24hr',
                                 'label_unit': 'ug/m3',
                                 'desc': '24hr avg #PM25 conc (#AQI colors)'},
            #'CO': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'HCHO': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'ISOPRENE': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'NH3': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'NOx': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            'O3': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
                                   'overlay_file': 'airpact5_{name}_{date}.gif',
                                   'overlay_date_fmt': '%Y%m%d%H',
                                   'overlay_date_re': '[0-9]{10}',
                                   'label_long': 'Ozone',
                                   'label_abbv': 'O3',
                                   'label_unit': 'ppb',
                                   'desc': 'hourly #ozone conc'},
            'PM25': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
                                     'overlay_file': 'airpact5_{name}_{date}.gif',
                                     'overlay_date_fmt': '%Y%m%d%H',
                                     'overlay_date_re': '[0-9]{10}',
                                     'label_long': 'Fine particulate',
                                     'label_abbv': 'PM2.5',
                                     'label_unit': 'ug/m3',
                                     'desc': 'hourly fine aerosol (#PM25) conc'},
            #'SO2': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'VIS': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'VOCs': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'WSPM25': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #
            # EMISSIONS
            #'emis_CO': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #'emis_HCHO': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #'emis_ISOPRENE': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #'emis_NH3': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #'emis_NOx': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #'emis_PM25': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #'emis_SO2': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #'emis_VOCs': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #'emis_WSPM25': {'overlay_path': 'emissions/{date:%Y}/{date:%Y_%m_%d}/',
            #
            # METEOROLOGY
            #'CFRAC': {'overlay_path': 'meteorology/{date:%Y}/{date:%Y_%m_%d}/',
            #'PBL': {'overlay_path': 'meteorology/{date:%Y}/{date:%Y_%m_%d}/',
            #'PRECIP': {'overlay_path': 'meteorology/{date:%Y}/{date:%Y_%m_%d}/',
            #'PRSFC': {'overlay_path': 'meteorology/{date:%Y}/{date:%Y_%m_%d}/',
            #'RGRND': {'overlay_path': 'meteorology/{date:%Y}/{date:%Y_%m_%d}/',
            #'TEMP2': {'overlay_path': 'meteorology/{date:%Y}/{date:%Y_%m_%d}/',
            #'VI': {'overlay_path': 'meteorology/{date:%Y}/{date:%Y_%m_%d}/',
            #'WIND': {'overlay_path': 'meteorology/{date:%Y}/{date:%Y_%m_%d}/',
                   }
                   
        self.overlays = sorted(list(self._sources.keys()))
        #self.species_list = self.get_species_list(date=date)
        
        
    def _refresh(self, overlay, date=None):
        """Retrieve one day of species imagery metadata from AIRPACT server
        
        Populates attribute `species_list` with
        
        Params
        ------
        overlay : str
            Valid options are listed in `airpact.overlays`
        date : datetime.datetime, optional
            If `date` is `None`, assumes current date from local computer clock
        """
        if date is None:
            date = datetime.now()
        else:
            assert isinstance(date, datetime), "`date` must be `datetime.datetime` or None"
        httpresp = requests.get(self._server_uri + 
                                self._sources[overlay]['overlay_path'].format(date=date))
        self._indexhtm = httpresp.text


    def get_overlay_list(self, date=None):
        """Return list of overlays with imagery products for given date
        
        Params
        ------
        date : datetime.datetime, optional
            If `date` is `None`, assumes current date from local computer clock            
        """
        if date is None:
            date = datetime.now()
        else:
            assert isinstance(date, datetime), "`date` must be `datetime.datetime` or None"
        print("Retrieving image overlay list for {date:%Y-%m-%d}..".
              format(date=date))

        prefixes = set(v['overlay_file'].split('_')[0] for v in self._sources.values())
        prefix_re = '(?:' + '|'.join(prefixes) + ')'
        image_re = prefix_re+"_(\w*)_[0-9]{10}.gif"
        image_set = set()

        # for each unique overlay path:
        for path in set(v['overlay_path'] for v in self._sources.values()):
            uri = self._server_uri + path.format(date=date)
            print('Searching in {0}..'.format(uri), end=' ')
            indexhtm = requests.get(uri).text
            groups = set(re.findall(image_re, indexhtm))
            print('found {0} overlays'.format(len(groups)))
            image_set |= groups
            
        overlays = sorted(list(image_set))
        print('{0} overlays available: {1}'.format(len(overlays),
                                                   ', '.join(overlays)))
        return overlays
    
        
    def get_overlay_image_list(self, overlay, date=None):
        """Return list of image URIs for overlay on given date
        
        Params
        ------
        overlay : str
            Valid options are listed in `airpact.overlays`
        date : datetime.datetime, optional
            If `date` is `None`, assumes current date from local computer clock            
        """
        if date is None:
            date = datetime.now()
        else:
            assert isinstance(date, datetime), "`date` must be `datetime.datetime` or None"
        print("Retrieving image list for {name} on {date:%Y-%m-%d}..".
              format(name=overlay, date=date))

        meta = self._sources[overlay]
        path = meta['overlay_path']
        #prefix = meta['overlay_file'].split('_')[0]
        image_re = meta['overlay_file'].format(name=overlay, 
                                               date=meta['overlay_date_re'])
        uri = self._server_uri + path.format(date=date)
        print('Searching in {0}..'.format(uri))
        # HINT if date not found, returns 404... if 404, still receive text
        # but it's the 404 notice so definitely no images will be found.. OK
        indexhtm = requests.get(uri).text
        images = set(re.findall(image_re, indexhtm))
            
        overlays = sorted(list(images))
        print('Found {0} images: {1}'.format(len(overlays),
                                             ', '.join(overlays)))
        return [uri+o for o in overlays]
    
    
    def get_overlay_images(self, overlay, date=None, reload_cache=False):
        """Return image file paths for overlay on date specified
        
        Params
        ------
        overlay : str
            Valid options are listed in `airpact.overlays`
        date : datetime.datetime, optional
            If `date` is `None`, assumes current date from local computer clock
        reload_cache : boolean, optional
            If `True`, ignores previously downloaded (cached) files
            
        Returns
        -------
        List of strings representing full file paths to downloaded images.
        """
        if date is None:
            date = datetime.now()
        else:
            assert isinstance(date, datetime), "`date` must be `datetime.datetime` or None"
        print("Retrieving {name} overlay imagery for {date:%Y-%m-%d}..".
              format(name=overlay, date=date))
        
        meta = self._sources[overlay]
        cache_dir = osp.join(self._cache_dir_base, 
                             self._cache_dir_srcs,
                             meta['overlay_path'].format(date=date),
                             overlay) # HINT for sanity's sake
        
        cached_images = glob(osp.join(cache_dir, '*_'+overlay+'_*'))
        if reload_cache or not cached_images:
            msg = 'Ignoring cache files.' if reload_cache else 'Cache not found.'
            print('{0} Downloading files..'.format(msg))
            cached_images = []
            for img_uri in self.get_overlay_image_list(overlay, date):
                img_name = img_uri.split('/')[-1]
                local_path = osp.join(cache_dir, img_name)
                
                os.makedirs(cache_dir, exist_ok=True)
                urllib.request.urlretrieve(img_uri, local_path)
                print('Saved file to ', local_path)
                cached_images.append(local_path)
        else:
            # TODO FIXME check cached file set against hosted web version
            # to identify missing files
            print('Using cached file set:')
            for img in cached_images:
                print(img)
        return sorted(cached_images)

        
    def optimize_gif(self, fpath):
        """Run `gifsicle` to reduce gif file size
        
        Params
        ------
        fpath : str
            Full path to unoptimized gif
        """
        from subprocess import run
        oname = fpath[:-4]+'_lossy'+fpath[-4:] # suffix
        #oname = 'lossy_'+fpath # prefix
        rc = run(['./gifsicle-static', '-O3', '--lossy={0}'.format(30),
                  '--colors=256', '-o {0}'.format(oname), fpath])
        return rc
        
        
    def create_gif(self, overlay, date=None):
        """Create animated gif of overlay for specified date
        
        Params
        ------
        overlay : str
            Valid options are listed in `airpact.overlays`
        date : datetime.datetime, optional
            If `date` is `None`, assumes current date from local computer clock
        
        Returns
        -------
        String containing full path to created gif
        """
        print("Creating gif for overlay: "+overlay)
        assert overlay in self.overlays, "Specified unavailable overlay; see `airpact.overlays`"
        
        if date is None:
            date = datetime.now()
        else:
            assert isinstance(date, datetime)
                
        background = Image.open(self._gif_map_bg).resize(self._gif_map_dims, 
                                                         self._gif_resize_f)
        datefont = ImageFont.truetype(self._gif_font, 18)
        titlefont = ImageFont.truetype(self._gif_font, 20)
                
        meta = self._sources[overlay]
        img_sources = self.get_overlay_images(overlay, date=date)
        if not img_sources:
            print("Could not locate imagery for overlay on this date: aborting..")
            return ''
        
        title = "#AIRPACT {name} ({abbv}) forecast".format(
            name=meta['label_long'], abbv=meta['label_abbv'])
        
        frame_dir = osp.join(self._cache_dir_base,
                             self._cache_dir_gifs,
                             meta['overlay_path'].format(date=date),
                             overlay) # HINT for sanity's sake
        os.makedirs(frame_dir, exist_ok=True)
        
        gif_frames = []
        for f in img_sources:
            # load source image with transparency
            fg = Image.open(f).convert('RGBA')
            fg = fg.resize(self._gif_map_dims, self._gif_resize_f)

            # load B&W version for alpha-masking non-transparent areas
            mask = Image.open(f).convert('L')
            mask = mask.resize(self._gif_map_dims, self._gif_resize_f)
            fg.putalpha(mask)
            
            # HACK fixup AQIcolors images to have transparency
            # outside overlay boundaries by alpha'ing white
            if 'AQIcolors' in overlay:
                print("Warning: fixing alpha channel in "+osp.basename(f))
                pixdata = fg.load()
                for y in range(fg.size[1]):
                    for x in range(fg.size[0]):
                        if pixdata[x, y] == (255, 255, 255, 255):
                            pixdata[x, y] = (255, 255, 255, 0)                
            
            # overlay alpha-ed source on map background
            bg = background.copy()
            bg.paste(fg, (0,0), fg)
        
            # overlay timestamp label
            draw = ImageDraw.Draw(bg)
            ts = datetime.strptime(f[-14:], "%Y%m%d%H.gif")
            tslbl = ts.strftime("%a, %b %e %Y, %I %p")
            w, h = draw.textsize(tslbl, font=datefont)
            draw.text(((self._gif_map_dims[0]-w)/2, self._gif_map_dims[1]-h-15),
                        tslbl, (20,20,20), font=datefont)
        
            # and a title
            w, h = draw.textsize(title, font=titlefont)
            draw.text(((self._gif_map_dims[0]-w)/2, 10),
                        title, (20,20,20), font=titlefont)
        
            # save as new file, preserving cached source image
            fname = osp.basename(f)
            o = osp.join(frame_dir, fname)
            bg.save(o, optimize=True)
            gif_frames.append(imageio.imread(o))
        
        oname = "out_"+overlay+"_{date:%Y%m%d}.gif".format(date=date)
        imageio.mimwrite(oname, gif_frames, duration=0.75)
        return oname
        
airpact = Airpact()


qd = datetime(2018, 7, 31)
#spec = 'PM25'
#spec = 'O3'
spec = 'AQIcolors_24hrPM25'
#spec = 'AQIcolors_08hrO3'

#overlay_gif = airpact.create_gif(spec, qd)
#airpact.optimize_gif(overlay_gif)

for spec in airpact.overlays:
    overlay_gif = airpact.create_gif(spec, qd)
    airpact.optimize_gif(overlay_gif)

