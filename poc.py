#!python
#
# proof of concept
# Patrick O'Keeffe

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
        date : datetime.datetime
            If `date` is `None`, initalizes AIRPACT metadata assuming current
            date from local computer clock
        """
        self._server_uri = "http://lar.wsu.edu/airpact/gmap/ap5/images/anim/"

        self._gif_map_bg = 'img/map_bg.png'
        self._gif_map_dims = (505, 439)
        self._gif_font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        self._gif_resize_f = Image.LANCZOS
        
        self._indexhtm = ""
        #self._refresh(date=date)

        self._sources = {
            # SPECIES
            #'08hrO3': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'24hrPM25': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'ANO3': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'AOD': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            #'AOMIJ': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
            'AQIcolors_08hrO3': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
                                 'overlay_img': 'airpact5_{name}_{date:%Y%m%d}.gif',
                                 'label_long': 'Ozone 8hr average',
                                 'label_abbv': 'O3-8hr',
                                 'label_unit': 'ppb',
                                 'desc': '8hr avg #ozone conc (#AQI colors)'},
            'AQIcolors_24hrPM25': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
                                   'overlay_img': 'airpact5_{name}_{date:%Y%m%d}.gif',
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
                  'overlay_img': 'airpact5_{name}_{date:%Y%m%d}.gif',
                  'label_long': 'Ozone',
                  'label_abbv': 'O3',
                  'label_unit': 'ppb',
                  'desc': 'hourly #ozone conc'},
            'PM25': {'overlay_path': 'species/{date:%Y}/{date:%Y_%m_%d}/',
                     'overlay_img': 'airpact5_{name}_{date:%Y%m%d}.gif',
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
        self._source_overlay_dirs = set(v['overlay_path'] for v in self._sources.values())
                   
        self.overlays = sorted(list(self._sources.keys()))
        #self.species_list = self.get_species_list(date=date)
        
        
    def _refresh(self, overlay, date=None):
        """Retrieve one day of species imagery metadata from AIRPACT server
        
        Populates attribute `species_list` with
        
        Params
        ------
        overlay : str
            Valid options are listed in `airpact.overlays`
        date : datetime.datetime
            If `date` is `None`, assumes current date from local computer clock
        """
        if date is None:
            date = datetime.now()
        else:
            assert isinstance(date, datetime)
        httpresp = requests.get(self._server_uri + 
                                self._sources[overlay]['overlay_path'].format(date=date))
        self._indexhtm = httpresp.text


    def get_overlay_list(self, overlay, date=None):
        """Return list of overlays with imagery products for given date
        
        Params
        ------
        overlay : str
            THIS OPTION SHOULD BE REMOVED
        date : datetime.datetime
            If `date` is `None`, assumes current date from local computer clock
            
        TODO: remove need to specify a species to search for
        """
        # FIXME instead of naive length check, should probably have some kind
        # of date recognition to avoid sutble errors.. TODO implement date-based
        # caching of index contents, species availability, and species imagery
        if not len(self._indexhtm):
            print("Refreshing index") # XXXX DEBUG
            self._refresh(overlay, date=date)
        pattern = "airpact5_(\w*)_[0-9]{10}.gif"
        groups = re.findall(pattern, self._indexhtm)
        return sorted(list(set(groups)))
    
    
    def get_species_images(self, species, date=None):
        """Return list of image URIs for single species for given date
        
        Params
        ------
        date : datetime.datetime
            If `date` is `None`, assumes current date from local computer clock
        """
        # TODO? permit asterisk "*" for all species?
        if not len(self._indexhtm):
            print("Refreshing index") # XXXX DEBUG
            self._refresh(date=date)
        pattern = "(airpact5_{species}_[0-9]{{10}}.gif)".format(species=species)
        groups = re.findall(pattern, self._indexhtm)
        return sorted(list(set(groups)))

        
    def optimize_gif(self, fpath):
        """Run `gifsicle` to reduce gif file size
        
        Params
        ------
        fpath : str
            Full path to unoptimized gif
        """
        from subprocess import run
        oname = fpath[:-4]+'_lossy'+fpath[-4:]
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
        
        
        TODO: abstract back to just 'overlay' and 'date', may need to overhaul
        `self._refresh()` to accomodate different overlays
        """
        print("\n\ncreating gif for "+overlay)
        assert overlay in self.overlays, "Specified unavailable overlay; see `airpact.overlays`"
        
        avail_overlays = self.get_overlay_list(overlay, date)
        assert overlay in avail_overlays, "Specified overlay not found for this date; try `airpact.get_species_list()`"

        if date is None:
            date = datetime.now()
        else:
            assert isinstance(date, datetime)
        
        meta = self._sources[overlay]
        img_list = airpact.get_species_images(overlay)
        img_files = []
        cached_files = sorted([f for f in glob('tmp/*'+overlay+'*.gif') 
                            if 'gif_' not in f])
        print('cached files: ', cached_files)
        if len(cached_files):
            print('found downloaded files... proceeding')
            img_files = cached_files
        else:
            print('downloading source files...')
            for img_name in img_list:#[:1]:
                local_file = 'tmp/'+img_name
                remote_file = (self._server_uri +
                               meta['overlay_path'].format(date=date) +
                               img_name)
                print(remote_file)
                urllib.request.urlretrieve(remote_file, local_file)
                img_files.append(local_file)

                
        background = Image.open(self._gif_map_bg).resize(self._gif_map_dims, 
                                                         self._gif_resize_f)
        
        datefont = ImageFont.truetype(self._gif_font, 18)
        titlefont = ImageFont.truetype(self._gif_font, 20)
        
        title = "#AIRPACT {name} ({abbv}) forecast".format(
            name=meta['label_long'], abbv=meta['label_abbv'])

        
        gif_frames = []
        for f in img_files:
            # load source image with transparency
            fg = Image.open(f).convert('RGBA')
            fg = fg.resize(self._gif_map_dims, self._gif_resize_f)
            
            # load B&W version for alpha-masking non-transparent areas
            mask = Image.open(f).convert('L')
            mask = mask.resize(self._gif_map_dims, self._gif_resize_f)
            fg.putalpha(mask)
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
            o = f.replace('gif_','').replace('airpact5', 'gif_airpact5')
            bg.save(o, optimize=True)
            gif_frames.append(imageio.imread(o))
        
        imageio.mimwrite(overlay+".gif", gif_frames, duration=0.75)
            
        
airpact = Airpact()


qd = None#datetime(2018, 7, 28)
spec = 'PM25'

airpact.create_gif(spec, qd)
airpact.optimize_gif(spec+".gif")

