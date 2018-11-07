# Alternate Color Maps

The official Air Quality Index (AQI) colors follow a rainbow palette
(*AQI Technical Assistance Document, May 2016*) spanning green to maroon,
representing 6 categories from good (0-50) to hazardous (301-500). In the
table below, they are listed with equivalent colors from some alternate maps
from the Python [Bokeh library](https://bokeh.pydata.org/en/latest/docs/reference/palettes.html)).

| AQI value | AQI Color | RGB code     | cividis | viridis | color blind |
|-----------|-----------|--------------|---------|---------|-------------|
| 0 - 50    | Green     |  0, 228, 0   | #FFE945 | #FDE724 | #0072B2     |
| 51 - 100  | Yellow    | 255, 255, 0  | #CAB969 | #79D151 | #E69F00     |
| 101 - 150 | Orange    | 255, 126, 0  | #958F78 | #22A784 | #F0E442     |
| 151 - 200 | Red       | 255, 0, 0    | #666870 | #29788E | #009E73     |
| 201 - 300 | Purple    | 143, 63, 151 | #31446B | #404387 | #56B4E9     |
| 301 - 500 | Maroon    | 126, 0, 35   | #00204C | #440154 | #D55E00     |


Best alternate map?

* LAR newsletter discussion
  * consensus "viridis" is best default 
    * good for color blindness
    * perceptually uniform
    * perform well in terms of time and error
  * "jet/rainbow (red->blue) is worst overall in terms of time and error"
  * another specifically-crafted one: "cividis"
    * perceptually uniform in hue and brightness
    * increases in brightness linearly
    * https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0199239

* Bokeh palettes as a resource
  * <https://bokeh.pydata.org/en/latest/docs/reference/palettes.html>
  * already had 'viridis' and 'cividis' as examples
  * under usability, have color blind, is more categorical &rarr; rearrange?


Links forwarded from work:

* <http://colorbrewer2.org/>
* <https://duckduckgo.com/?q=wcag+color+guidelines&atb=v102-1_f&ia=web>
* <https://www.researchgate.net/publication/245692399_Color_Use_Guidelines_for_Data_Representation>
* <https://www.researchgate.net/project/Towards-ContrastBrewer-Evaluating-visual-contrast-and-hierarchy-relations-of-cartographic-features-across-multi-scale-map-series>
* <https://colorusage.arc.nasa.gov/guidelines_0.php>


Some more links from LAR_everyone discussion (Oct 11, 2018):

* <https://www.toptal.com/designers/colorfilter>
* <https://www.youtube.com/watch?v=xAoljeRJ3lU>
* <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0199239>
* <https://dl.acm.org/citation.cfm?id=3174172>
* <https://stackoverflow.com/a/44553670/786542> for diverging data


