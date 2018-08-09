#!/home/patrick/anaconda3/bin/python
#
# proof of concept
# Patrick O'Keeffe

import os, os.path as osp
from glob import glob

os.chdir('/home/patrick/Code/twitter-airpactpnw.git')

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
        self._gif_legend = 'img/legend_{name}.jpg' # .format{name=overlay}
        self._gif_logo = 'img/wsu_shield.jpg'
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
                                 'label_long': 'Ozone',
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
        cache_dir = osp.join(self._cache_dir_base, 
                             self._cache_dir_srcs,
                             meta['overlay_path'].format(date=datetime.now()))
        os.makedirs(cache_dir, exist_ok=True)
        
        path = meta['overlay_path']
        #prefix = meta['overlay_file'].split('_')[0]
        image_re = meta['overlay_file'].format(name=overlay, 
                                               date=meta['overlay_date_re'])
        uri = self._server_uri + path.format(date=date)
        print('Searching in {0}..'.format(uri))
        # HINT if date not found, returns 404... if 404, still receive text
        # but it's the 404 notice so definitely no images will be found.. OK
        indexhtm = requests.get(uri).text
        with open(osp.join(cache_dir, 'index_{date:%Y%m%d_%H%M}.html'.format(
                                           date=date)), 'w') as f:
            f.write(indexhtm)
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
        
        
    def create_gif(self, overlay, date=None, reload_cache=True):
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
        meta = self._sources[overlay]
        img_sources = self.get_overlay_images(overlay, date=date, reload_cache=reload_cache)
        if not img_sources:
            print("Could not locate imagery for overlay on this date: aborting..")
            return ''
               
        frame_dir = osp.join(self._cache_dir_base,
                             self._cache_dir_gifs,
                             meta['overlay_path'].format(date=date),
                             overlay) # HINT for sanity's sake
        os.makedirs(frame_dir, exist_ok=True)
        
        gif_frames = []
        for f in img_sources:
            # create blank canvas to build on
            # XXXX maybe construct canvas size around map size?
            canvas_dims = (620,550)
            img = Image.new("RGBA", canvas_dims, (255, 255, 255, 255))
            draw = ImageDraw.Draw(img)
            
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
            anim = background.copy()
            anim.paste(fg, (0,0), fg)

            # place on canvas with nice border
            anim_pos = (10, 45)
            anim_border = tuple(sum(x) for x in zip(anim_pos, anim.size))
            img.paste(anim, anim_pos)
            draw.rectangle((anim_pos, anim_border), outline="black")
            
            # put legend on right-hand side centered wrt map and right edge
            legend = Image.open(self._gif_legend.format(name=overlay))
            assert anim.size[1] > legend.size[1], "Sorry! the animation must be taller than the legend!"
            legend_lbuff = round((canvas_dims[0]-anim_border[0])/2 - legend.size[0]/2) 
            legend_tbuff = round((anim_border[1]-anim_pos[1])/2 - legend.size[1]/2)
            legend_pos = (anim_border[0]+legend_lbuff, anim_pos[1]+legend_tbuff)
            img.paste(legend.convert('RGBA'), legend_pos)
        
            #FIXME
            font_color = (152,30,50)
            
            # overlay timestamp date label
            date_font = ImageFont.truetype(self._gif_font, 18)
            ts = datetime.strptime(f[-14:], "%Y%m%d%H.gif")
            centerline = round(0.75*anim_border[0])
            date_text = ts.strftime("%a, %b %e %Y")
            date_size = draw.textsize(date_text, date_font)
            date_pos = (centerline - round(date_size[0]/2), anim_border[1]+10)
            draw.text(date_pos, date_text, fill=font_color, font=date_font)
            # also the time
            time_text = ts.strftime("%-I:%M %p (PST)")
            time_size = draw.textsize(time_text, date_font)
            time_pos = (centerline - round(time_size[0]/2), date_pos[1]+date_size[1])
            draw.text(time_pos, time_text, fill=font_color, font=date_font)
            
            # place overlay title along the top
            titlefont = ImageFont.truetype(self._gif_font, 22)
            title = "{name} ({abbv}) forecast".format(name=meta['label_long'], 
                                                      abbv=meta['label_abbv'])
            title_size = draw.textsize(title, font=titlefont)
            title_pos = ((canvas_dims[0]-title_size[0])/2, 10)
            #title_pos = ((anim_border[0]-title_size[0])/2+anim_pos[0],
            #             (anim_border[1]+10))
            draw.text(title_pos, title, fill=font_color, font=titlefont)
        
            # put logo in bottom corner, centered between image and edge
            logo = Image.open(self._gif_logo).convert("RGBA")
            logo_tbuff = round((canvas_dims[1]-anim_border[1])/2 - logo.size[1]/2)
            logo_pos = (20, anim_border[1]+logo_tbuff)
            img.paste(logo, logo_pos)
            
            # add taglines, anchored to logo
            hashtag_pos = (logo_pos[0]+logo.size[0]+5, logo_pos[1]+10)
            hashtag_text = "#AIRPACT"
            hashtag_size = draw.textsize(hashtag_text, font=titlefont)
            draw.text(hashtag_pos, hashtag_text, fill=font_color, font=titlefont)
            url_font = ImageFont.truetype(self._gif_font, 14)
            url_text = "airpact.wsu.edu"
            url_pos = (hashtag_pos[0], hashtag_pos[1]+hashtag_size[1]+5)
            draw.text(url_pos, url_text, fill="blue", font=url_font)
            
            # save as new file, preserving cached source image
            fname = osp.basename(f)
            o = osp.join(frame_dir, fname)
            img.save(o, optimize=True)
            gif_frames.append(imageio.imread(o))
        
        oname = "out_"+overlay+"_{date:%Y%m%d}.gif".format(date=date)
        imageio.mimwrite(oname, gif_frames, duration=0.75)
        return oname
        
airpact = Airpact()


qd = None
#qd = datetime(2018, 8, 5)
#spec = 'PM25'
#spec = 'O3'
spec = 'AQIcolors_24hrPM25'
#spec = 'AQIcolors_08hrO3'

#overlay_gif = airpact.create_gif(spec, qd)
#airpact.optimize_gif(overlay_gif)

for spec in airpact.overlays:
    #overlay_gif = airpact.create_gif(spec, qd, reload_cache=True)
    #airpact.optimize_gif(overlay_gif)
    airpact.get_overlay_image_list(spec)

