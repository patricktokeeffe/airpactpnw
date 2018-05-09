# Notes

## Plan Stages

1. Post daily forecasts as animated gif
    * just PM2.5 and O3 AQI for now
    * expand to other species later
2. Post alerts when AQI exceeds certain thresholds
    * mention/hashtag affected counties
    * include some kind of forecast trust 






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


