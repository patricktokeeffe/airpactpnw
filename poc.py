#!/usr/bin/env python3
#
# proof of concept
# Patrick O'Keeffe

import os, os.path as osp
import subprocess
from glob import glob

os.chdir(osp.dirname(osp.abspath(__file__)))

import imageio
from PIL import Image, ImageFont, ImageDraw

####
from datetime import datetime, timedelta
import re
import requests, urllib



""" API outline

get_image_metadata(date)



"""





_server_uri = "http://lar.wsu.edu/airpact/gmap/ap5/images/anim/"

_gif_map_bg = 'img/map_bg.png'
_gif_map_dims = (505, 439)
_gif_legend = 'img/legend_{name}.jpg' # .format{name=overlay}
_gif_logo = 'img/wsu_shield.jpg'
_gif_font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
_gif_resize_f = Image.LANCZOS

_indexhtm = ""
_cache_dir_base = 'tmp'
_cache_dir_srcs = 'img_sources'
_cache_dir_frames = 'gif_frames'
_cache_dir_gifs = 'gif_products'


_dir_info = {'path': '{subdir}/{date:%Y}/{date:%Y_%m_%d}/',
             'file': 'airpact5_{name}_{date}.gif',
             'date_re': '[0-9]{10}'}

_sources = {
    # HINT 
    # - key values are substituted for {name} in `_dir_info['file']`
    # - the unit/desc fields not yet used, but intended for generating tweets
    #
    '08hrO3':               {'subdir': 'species',
                             'label' : 'Ozone',
                             'abbv'  : 'O3-8hr',
                             'unit'  : 'ppb',
                             'desc'  : '8hr avg ozone conc'},
    '24hrPM25':             {'subdir': 'species',
                             'label' : 'Fine particulates',
                             'abbv'  : 'PM2.5-24hr',
                             'unit'  : 'ug/m3',
                             'desc'  : '24hr avg PM2.5 conc'},
    'ANO3':                 {'subdir': 'species',
                             'label' : 'Nitrate aerosol',
                             'abbv'  : 'ANO3',
                             'unit'  : 'ppb',
                             'desc'  : 'hourly nitrate aerosol conc'},
    #'AOD': ignoring - images are labeled from hours 01-24 and so need special parsing code
    #'AOMIJ': ignoring-  can't identify corresponding legend
    'AQIcolors_08hrO3':     {'subdir': 'species',
                             'label' : 'Ozone',
                             'abbv'  : 'O3-8hr',
                             'unit'  : '',
                             'desc'  : '8hr avg #ozone conc (AQI colors)'},
    'AQIcolors_24hrPM25':   {'subdir': 'species',
                             'label' : 'Fine particulates',
                             'abbv'  : 'PM2.5-24hr',
                             'unit'  : '',
                             'desc'  : '24hr avg #PM25 conc (AQI colors)'},
    'CO':                   {'subdir': 'species',
                             'label' : 'Carbon monoxide',
                             'abbv'  : 'CO',
                             'unit'  : 'ppm',
                             'desc'  : 'hourly carbon monoxide (CO) conc'},
    'HCHO':                 {'subdir': 'species',
                             'label' : 'Formaldehyde',
                             'abbv'  : 'HCHO',
                             'unit'  : 'ppb',
                             'desc'  : 'hourly formaldehyde (HCHO) conc'},
    'ISOPRENE':             {'subdir': 'species',
                             'label' : 'Isoprene',
                             'abbv'  : '',
                             'unit'  : 'ppb',
                             'desc'  : 'hourly isoprene conc'},
    'NH3':                  {'subdir': 'species',
                             'label' : 'Ammonia',
                             'abbv'  : 'NH3',
                             'unit'  : 'ppb',
                             'desc'  : 'hourly ammonia conc'},
    'NOx':                  {'subdir': 'species',
                             'label' : 'Nitrogen oxides',
                             'abbv'  : 'NOx',
                             'unit'  : 'ppb',
                             'desc'  : 'hourly nitrogen oxides conc'},
    'O3':                   {'subdir': 'species',
                             'label' : 'Ozone',
                             'abbv'  : 'O3',
                             'unit'  : 'ppb',
                             'desc'  : 'hourly #ozone conc'},
    'PM25':                 {'subdir': 'species',
                             'label' : 'Fine particulates',
                             'abbv'  : 'PM2.5',
                             'unit'  : 'ug/m3',
                             'desc'  : 'hourly fine particulates (#PM25) conc'},
    'SO2':                  {'subdir': 'species',
                             'label' : 'Sulfur dioxide',
                             'abbv'  : 'SO2',
                             'unit'  : 'ppb',
                             'desc'  : 'hourly sulfur dioxide (SO2) conc'},
    #'VIS': ignoring - images are labeled from hours 01-24 and so need special parsing code
    'VOCs':                 {'subdir': 'species',
                             'label' : 'Volatile organics',
                             'abbv'  : 'VOCs',
                             'unit'  : 'ppb',
                             'desc'  : 'hourly VOCs conc'},
    'WSPM25':               {'subdir': 'species',
                             'label' : 'Wood smoke fine particulates',
                             'abbv'  : 'WS-PM2.5',
                             'unit'  : 'ug/m3',
                             'desc'  : 'hourly #woodsmoke PM2.5 conc'},
           }
                   
overlays = sorted(list(_sources.keys()))

        
        
#    def _refresh(self, overlay, date=None):
#        """Retrieve one day of species imagery metadata from AIRPACT server
#        
#        Populates attribute `species_list` with
#        
#        Params
#        ------
#        overlay : str
#            Valid options are listed in `airpact.overlays`
#        date : datetime.datetime, optional
#            If `date` is `None`, searches for most recent model run
#        """
#        if date is None:
#            date = self.get_latest_imagery_date(overlay)
#        else:
#            assert isinstance(date, datetime), "`date` must be `datetime.datetime` or None"
#        httpresp = requests.get(self._server_uri + 
#                                self._sources[overlay]['overlay_path'].format(date=date))
#        self._indexhtm = httpresp.text


#def get_overlay_list(date):
#    """Return list of overlays with imagery products for given date
#    
#    Params
#    ------
#    date : datetime.datetime, ~~optional~~
#        Date to search for overlays
#        ~~If `date` is `None`, uses current clock time.~~
#
#    Returns
#    -------
#    List of str representing available overlay groups on specified date
#    """
#    #if date is None:
#    #    date = datetime.now()
#    #else:
#    #    assert isinstance(date, datetime), "`date` must be `datetime.datetime` or None"
#    assert isinstance(date, datetime), "`date` must be `datetime.datetime`"
#    print("Retrieving image overlay list for {date:%Y-%m-%d}..".
#          format(date=date))
#    # 
#    prefixes = set(v['overlay_file'].split('_')[0] for v in _sources.values())
#    #
#    prefix_re = '(?:' + '|'.join(prefixes) + ')'
#    image_re = prefix_re+"_(\w*)_[0-9]{10}.gif"
#    image_set = set()
#
#    # for each unique overlay path:
#    for path in set(v['overlay_path'] for v in _sources.values()):
#        uri = _server_uri + path.format(date=date)
#        print('Searching in {0}..'.format(uri), end=' ')
#        indexhtm = requests.get(uri).text
#        groups = set(re.findall(image_re, indexhtm))
#        print('found {0} overlays'.format(len(groups)))
#        image_set |= groups
#        
#    overlays = sorted(list(image_set))
#    print('{0} overlays available: {1}'.format(len(overlays),
#                                               ', '.join(overlays)))
#    return overlays

    
def get_latest_imagery_date(overlay):
    """Search for most recent imagery set (48 images) within last 7 days
    
    Params
    ------
    overlay : str
        Valid options are listed in `airpact.overlays`
    
    Returns
    -------
    `datetime.datetime` instance for most current imagery date or `None` if not found
    """
    meta = _sources[overlay]
    uri = _server_uri + _dir_info['path']
    
    # find a good date to start from, assuming tomorrow
    search_date = datetime.now() + timedelta(days=1)
    assert search_date > datetime(2015, 8, 1) # start of imagery (ignoring 2012)
    last_pub_date = None
    for i in range(7):
        r = requests.get(uri.format(subdir=meta['subdir'], date=search_date))
        if r.status_code != 404:
            n = len(get_overlay_image_list(overlay, date=search_date))
            if n == 48:
                last_pub_date = search_date
                break
        search_date += timedelta(days=-1)        
    return last_pub_date
    


    
def get_overlay_image_list(overlay, date=None):
    """Return list of image URIs for overlay on given date
    
    Params
    ------
    overlay : str
        Valid options are listed in `airpact.overlays`
    date : datetime.datetime, optional
        If `date` is `None`, searches for most recent model run
        
    Returns
    -------
    List of str representing imagery URIs for specified overlay and date
    """
    if date is None:
        date = get_latest_imagery_date(overlay)
    else:
        assert isinstance(date, datetime), "`date` must be `datetime.datetime` or None"
    print("Retrieving image list for {name} on {date:%Y-%m-%d}..".
          format(name=overlay, date=date))

    meta = _sources[overlay]
    subdir = meta['subdir']
    cache_dir = osp.join(_cache_dir_base, 
                         _cache_dir_srcs,
                         _dir_info['path'].format(subdir=subdir, date=datetime.now()))
    os.makedirs(cache_dir, exist_ok=True)
    
    path = _dir_info['path']
    image_re = _dir_info['file'].format(name=overlay, date=_dir_info['date_re'])
    uri = _server_uri + path.format(subdir=subdir, date=date)
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



def get_overlay_images(overlay, date=None, use_cache=True):
    """Return image file paths for overlay on date specified
    
    Params
    ------
    overlay : str
        Valid options are listed in `airpact.overlays`
    date : datetime.datetime, optional
        If `date` is `None`, searches for most recent model run
    use_cache : boolean, optional
        Set to False to disable local caching
        
    Returns
    -------
    List of str representing full file paths to downloaded images.
    """
    if date is None:
        date = get_latest_imagery_date(overlay)
    else:
        assert isinstance(date, datetime), "`date` must be `datetime.datetime` or None"
    print("Retrieving {name} overlay imagery for {date:%Y-%m-%d}..".
          format(name=overlay, date=date))
    
    meta = _sources[overlay]
    cache_dir = osp.join(_cache_dir_base, 
                         _cache_dir_srcs,
                         _dir_info['path'].format(subdir=meta['subdir'], date=date),
                         overlay) # HINT for sanity's sake
    os.makedirs(cache_dir, exist_ok=True)
    cached_images = sorted(glob(osp.join(cache_dir, '*_'+overlay+'_*')))
    if not use_cache or not cached_images:
        msg = 'Ignoring cache files.' if not use_cache else 'Cache not found.'
        print('{0} Downloading files..'.format(msg))
        cached_images = []
        for img_uri in get_overlay_image_list(overlay, date):
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
    return cached_images


    
   
    
def create_gif(overlay, date=None, use_cache=True):
    """Create animated gif of overlay for specified date
    
    Params
    ------
    overlay : str
        Valid options are listed in `airpact.overlays`
    date : datetime.datetime, optional
        If `date` is `None`, assumes current date from local computer clock
    use_cache : boolean, optional
        Set to False to disable local caching
    
    Returns
    -------
    String containing full path to created gif
    """
    print("Creating gif for overlay: "+overlay)
    assert overlay in overlays, "Specified unavailable overlay; see `airpact.overlays`"
    
    if date is None:
        date = get_latest_imagery_date(overlay)
    else:
        assert isinstance(date, datetime)
            
    background = Image.open(_gif_map_bg).resize(_gif_map_dims, 
                                                     _gif_resize_f)
    meta = _sources[overlay]
    subdir = meta['subdir']
    img_sources = get_overlay_images(overlay, date=date, use_cache=use_cache)
    if not img_sources:
        print("Could not locate imagery for overlay on this date: aborting..")
        return ''
           
    frame_dir = osp.join(_cache_dir_base,
                         _cache_dir_frames,
                         _dir_info['path'].format(subdir=subdir, date=date),
                         overlay) # HINT for sanity's sake
    output_dir = osp.join(_cache_dir_base,
                          _cache_dir_gifs,
                          _dir_info['path'].format(subdir=subdir, date=date))
    os.makedirs(frame_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    gif_frames = []
    for f in img_sources:
        # create blank canvas to build on
        # XXXX maybe construct canvas size around map size?
        canvas_dims = (620,550)
        img = Image.new("RGBA", canvas_dims, (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # load source image with transparency
        fg = Image.open(f).convert('RGBA')
        fg = fg.resize(_gif_map_dims, _gif_resize_f)

        # load B&W version for alpha-masking non-transparent areas
        mask = Image.open(f).convert('L')
        mask = mask.resize(_gif_map_dims, _gif_resize_f)
        fg.putalpha(mask)
        
        # HACK fixup AQIcolors images to have transparency
        # outside overlay boundaries by alpha'ing white
        if 'AQIcolors' in overlay:
            #print("Warning: fixing alpha channel in "+osp.basename(f))
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
        legend = Image.open(_gif_legend.format(name=overlay))
        assert anim.size[1] > legend.size[1], "Sorry! the animation must be taller than the legend!"
        legend_lbuff = round((canvas_dims[0]-anim_border[0])/2 - legend.size[0]/2) 
        legend_tbuff = round((anim_border[1]-anim_pos[1])/2 - legend.size[1]/2)
        legend_pos = (anim_border[0]+legend_lbuff, anim_pos[1]+legend_tbuff)
        img.paste(legend.convert('RGBA'), legend_pos)
    
        #FIXME
        font_color = (152,30,50)
        
        # overlay timestamp date label
        date_font = ImageFont.truetype(_gif_font, 18)
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
        titlefont = ImageFont.truetype(_gif_font, 22)
        if not len(meta['abbv']):
            title = "{l} forecast".format(l=meta['label'])
        else:
            title = "{l} ({a}) forecast".format(l=meta['label'], a=meta['abbv'])
        
        title_size = draw.textsize(title, font=titlefont)
        title_pos = ((canvas_dims[0]-title_size[0])/2, 10)
        #title_pos = ((anim_border[0]-title_size[0])/2+anim_pos[0],
        #             (anim_border[1]+10))
        draw.text(title_pos, title, fill=font_color, font=titlefont)
    
        # put logo in bottom corner, centered between image and edge
        logo = Image.open(_gif_logo).convert("RGBA")
        logo_tbuff = round((canvas_dims[1]-anim_border[1])/2 - logo.size[1]/2)
        logo_pos = (20, anim_border[1]+logo_tbuff)
        img.paste(logo, logo_pos)
        
        # add taglines, anchored to logo
        hashtag_pos = (logo_pos[0]+logo.size[0]+5, logo_pos[1]+10)
        hashtag_text = "#AIRPACT"
        hashtag_size = draw.textsize(hashtag_text, font=titlefont)
        draw.text(hashtag_pos, hashtag_text, fill=font_color, font=titlefont)
        url_font = ImageFont.truetype(_gif_font, 14)
        url_text = "airpact.wsu.edu"
        url_pos = (hashtag_pos[0], hashtag_pos[1]+hashtag_size[1]+5)
        draw.text(url_pos, url_text, fill="blue", font=url_font)

        
        
        # save as new file, preserving cached source image
        fname = osp.basename(f)
        o = osp.join(frame_dir, fname)
        img.save(o, optimize=True)
        gif_frames.append(imageio.imread(o))
    
    oname = osp.join(output_dir, overlay+".gif")
    imageio.mimwrite(oname, gif_frames, duration=0.75)
    return oname
    
    
    

def optimize_gif(fpath):
    """Run `gifsicle` to reduce gif file size
    
    Params
    ------
    fpath : str
        Full path to unoptimized gif
        
    Returns
    -------
    Process return code value
    """
    from subprocess import run
    rc = run(['./gifsicle-static', '-O3', '--lossy={0}'.format(30),
              '--colors=256', '--output={0}'.format(fpath), fpath])
    return rc

    


if __name__ == '__main__':

    outputs = []
    for ea in overlays:#['PM25', 'AQIcolors_24hrPM25']:
        overlay_gif = create_gif(ea)
        optimize_gif(overlay_gif)
        outputs.append(overlay_gif)

    outdir = osp.commonpath(outputs)
    subprocess.call(["./tweet.py", outdir])

