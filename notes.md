# Notes

## Plan Stages

1. Post daily forecasts as animated gif
    * just PM2.5 and O3 AQI for now
    * expand to other species later
2. Mention/hashtag affected localities (city/county/tribe/?) when
    * AQI exceeds certain thresholds
    * sensitive population air advisements would be issued
    * relative hot spots appear
    * in relation to wildfire events

More thoughts:

* aggregation: eg "airpact predicts elevated ozone in x, y, z"
* develop set of emoji for communicating data

Other post types

* data commentary
    * say something positive when it all looks clear?
    * periodic reminders it's a forecast, disclaimer, etc
* news
    * new releases, features
    * bug fixes
    * newsletter announcements, such as meeting dates?
    * periodic ticklers about other info available on airpact site
* quality reports
    * reply to previous posts with model performance data?
    * observations vs model at random subset of sites
    * self-report when model strays far beyond observations
    * self-congratulate when model performs very well on particular day
* wildfire
    * ?



## Image sources

From Jenn:

If you are looking for the daily raw gif images, here is where you can find them:

    <http://lar.wsu.edu/airpact/gmap/ap5/images/anim/species/YYYY/YYYY_MM_DD>


where YYYY is the year, MM is the month, and DD is the day.  For example:

    <http://lar.wsu.edu/airpact/gmap/ap5/images/anim/species/2018/2018_04_30>


Within this folder, the PM2.5 gif images begin with `airpact5_PM25_*`
followed by `YYYYMMDDHH` (year month day hour).

There are some generic timestamp labels (and specific date labels) here:

    <http://lar.wsu.edu/airpact/gmap/ap5/images/anim/date_time_labels/>



### Downloading

Easier to use `urllib` than `requests` <https://stackoverflow.com/q/13137817/2946116>


## Overlays

### Text

* <https://stackoverflow.com/questions/10640114/overlay-two-same-sized-images-in-python>
* <https://docs.opencv.org/2.4.8/modules/core/doc/drawing_functions.html?highlight=puttext#cv2.putText>
* <https://github.com/python-pillow/Pillow/issues/1592#issuecomment-291573715> hint: `.convert('RBGA')
* <http://effbot.org/imagingbook>
* <https://docs.python.org/3.5/library/datetime.html>

```
import PIL
from PIL import ImageFont, Image, ImageDraw

font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
img = Image.open('tmp/airpact5_24hrPM25_2018050501.gif').convert('RGBA')
draw = ImageDraw.Draw(img)
draw.text((100,100), "AIRPACT", (0,0,0), font=font)
img.save('markup.gif')
```

### Images

* <http://stackoverflow.com/questions/273946/ddg#273962>
* <https://stackoverflow.com/questions/1252218/pil-image-resize-not-resizing-the-picture>
* <http://stackoverflow.com/questions/28658918/ddg#28660377>
* <https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil>

```
bg = Image.open('img/map_bg.png').resize((863,751), Image.LANCZOS)
bg.paste(img, (0,0), img)
bg.save('bg.gif')
```

* fullsize (863x751) --> 30 MB
* halfsize (432x376) --> 10 MB
* 40%      (345x300) --> 6.4 MB
* 30%                    4.2 MB

more todo:

* ~~adjust opacity of overlays (70% is airpact default)~~
* overlay domain border, county/state borders


#### Add alpha to transparent overlay

* <https://stackoverflow.com/questions/890051/how-do-i-generate-circular-thumbnails-with-pil>
    * pointed me towards success with alpha masking opaque parts of airpact gifs
    * load image second time in black and white to use as alpha mask








