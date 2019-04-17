# Alternate Color Maps

The official Air Quality Index (AQI) colors follow a rainbow palette
(*AQI Technical Assistance Document, May 2016*) spanning green to maroon,
representing 6 categories from good (0-50) to hazardous (301-500). In the
table below, they are listed with equivalent colors from some alternate maps
from the Python [Bokeh library](https://bokeh.pydata.org/en/latest/docs/reference/palettes.html)).

| AQI value | AQI Color | RGB code     | cividis     | viridis    | color blind | AIRPACT PM2.5 AQI (imagery) | AIRPACT PM2.5 AQI (legend) |
|-----------|-----------|--------------|-------------|------------|-------------|-----------|-----------|
| 0 - 50    | Green     |  0, 228, 0   | 255,233,69  | 253,231,36 | 0, 114, 178 | 0, 255, 0 | 36,225,0  |
| 51 - 100  | Yellow    | 255, 255, 0  | 202,185,105 | 121,209,81 | 230, 159, 0 | 255,255,0 | 252,252,20|
| 101 - 150 | Orange    | 255, 126, 0  | 149,143,120 | 34,167,132 | 240, 228, 66| 255,165,0 | 252,126,0 |
| 151 - 200 | Red       | 255, 0, 0    | 102,104,112 | 41,120,142 | 0, 158, 115 | 255, 0, 0 | 252,22,0  |
| 201 - 300 | Purple    | 143, 63, 151 | 49,68,107   | 64,67,135  | 86, 180, 233| 139,28,98 | 151,11,76 |
| 301 - 500 | Maroon    | 126, 0, 35   | 0,32,76     | 68,1,84    | 213, 94, 0  | 139,26,26 | 124,6,33  |


### Color comparision

AIRPACT PM2.5 AQI colors, extracted from both imagery and legend, compared to prescribed color values and comparable alternatives from the [Bokeh](https://bokeh.pydata.org) library.

| AQI | imagery | legend | [cividis](https://bokeh.pydata.org/en/latest/docs/reference/palettes.html#bokeh.palettes.cividis) | [viridis](https://bokeh.pydata.org/en/latest/docs/reference/palettes.html#bokeh.palettes.viridis) | [color blind](https://bokeh.pydata.org/en/latest/docs/reference/palettes.html#usability-palettes) |
|:-------------------------------------------------:|:-------------------------------------------------:|:-------------------------------------------------:|:-------------------------------------------------:|:-------------------------------------------------:|:-------------------------------------------------:|
| ![#00E400](https://placehold.it/25/00E400?text=+) | ![#00FF00](https://placehold.it/25/00FF00?text=+) | ![#24E100](https://placehold.it/25/24E100?text=+) | ![#FFE945](https://placehold.it/25/FFE945?text=+) | ![#FDE724](https://placehold.it/25/FDE724?text=+) | ![#0072B2](https://placehold.it/25/0072B2?text=+) |
| ![#FFFF00](https://placehold.it/25/FFFF00?text=+) | ![#FFFF00](https://placehold.it/25/FFFF00?text=+) | ![#FCFC14](https://placehold.it/25/FCFC14?text=+) | ![#CAB969](https://placehold.it/25/CAB969?text=+) | ![#FDE724](https://placehold.it/25/FDE724?text=+) | ![#E69F00](https://placehold.it/25/E69F00?text=+) |
| ![#FF7E00](https://placehold.it/25/FF7E00?text=+) | ![#FFA500](https://placehold.it/25/FFA500?text=+) | ![#FC7E00](https://placehold.it/25/FC7E00?text=+) | ![#958F78](https://placehold.it/25/958F78?text=+) | ![#22A784](https://placehold.it/25/22A784?text=+) | ![#F0E442](https://placehold.it/25/F0E442?text=+) |
| ![#FF0000](https://placehold.it/25/FF0000?text=+) | ![#FF0000](https://placehold.it/25/FF0000?text=+) | ![#FC1600](https://placehold.it/25/FC1600?text=+) | ![#958F78](https://placehold.it/25/958F78?text=+) | ![#29788E](https://placehold.it/25/29788E?text=+) | ![#009E73](https://placehold.it/25/009E73?text=+) |
| ![#8F3F97](https://placehold.it/25/8F3F97?text=+) | ![#8B1C62](https://placehold.it/25/8B1C62?text=+) | ![#970B4C](https://placehold.it/25/970B4C?text=+) | ![#31446B](https://placehold.it/25/31446B?text=+) | ![#404387](https://placehold.it/25/404387?text=+) | ![#56B4E9](https://placehold.it/25/56B4E9?text=+) |
| ![#7E0023](https://placehold.it/25/7E0023?text=+) | ![#8B1A1A](https://placehold.it/25/8B1A1A?text=+) | ![#7C0621](https://placehold.it/25/7C0621?text=+) | ![#00204C](https://placehold.it/25/00204C?text=+) | ![#440154](https://placehold.it/25/440154?text=+) | ![#D55E00](https://placehold.it/25/D55E00?text=+) |

AIRPACT PM2.5 mass unit scaling

| ug/m3 | legend  | cividis | viridis | legend                                            | cividis                                           | viridis                                           |
|-------|---------|---------|---------|:-------------------------------------------------:|:-------------------------------------------------:|:-------------------------------------------------:|
|  160  | #FE0000 | #FFE945 | #FDE724 | ![#FE0000](https://placehold.it/25/FE0000?text=+) | ![#FFE945](https://placehold.it/25/FFE945?text=+) | ![#FDE724](https://placehold.it/25/FDE724?text=+) |
|   80  | #FE5200 | #E8D257 | #BFDF24 | ![#FE5200](https://placehold.it/25/FE5200?text=+) | ![#E8D257](https://placehold.it/25/E8D257?text=+) | ![#BFDF24](https://placehold.it/25/BFDF24?text=+) |
|   40  | #FFA300 | #CEBD67 | #83D34B | ![#FFA300](https://placehold.it/25/FFA300?text=+) | ![#CEBD67](https://placehold.it/25/CEBD67?text=+) | ![#83D34B](https://placehold.it/25/83D34B?text=+) |
|   30  | #FFFF01 | #B6A971 | #4FC369 | ![#FFFF01](https://placehold.it/25/FFFF01?text=+) | ![#B6A971](https://placehold.it/25/B6A971?text=+) | ![#4FC369](https://placehold.it/25/4FC369?text=+) |
|   20  | #ADE604 | #9E9676 | #2AB07E | ![#ADE604](https://placehold.it/25/ADE604?text=+) | ![#9E9676](https://placehold.it/25/9E9676?text=+) | ![#2AB07E](https://placehold.it/25/2AB07E?text=+) |
|   15  | #5BCC0C | #878478 | #1E9A89 | ![#5BCC0C](https://placehold.it/25/5BCC0C?text=+) | ![#878478](https://placehold.it/25/878478?text=+) | ![#1E9A89](https://placehold.it/25/1E9A89?text=+) |
|   10  | #08B30D | #717273 | #24848D | ![#08B30D](https://placehold.it/25/08B30D?text=+) | ![#717273](https://placehold.it/25/717273?text=+) | ![#24848D](https://placehold.it/25/24848D?text=+) |
|    8  | #057366 | #5D616E | #2D6E8E | ![#057366](https://placehold.it/25/057366?text=+) | ![#5D616E](https://placehold.it/25/5D616E?text=+) | ![#2D6E8E](https://placehold.it/25/2D6E8E?text=+) |
|    6  | #0339B3 | #46506B | #38578C | ![#0339B3](https://placehold.it/25/0339B3?text=+) | ![#46506B](https://placehold.it/25/46506B?text=+) | ![#38578C](https://placehold.it/25/38578C?text=+) |
|    4  | #0000FE | #29406B | #423D84 | ![#0000FE](https://placehold.it/25/0000FE?text=+) | ![#29406B](https://placehold.it/25/29406B?text=+) | ![#423D84](https://placehold.it/25/423D84?text=+) |
|    2  | #5351FD | #002F6F | #482172 | ![#5351FD](https://placehold.it/25/5351FD?text=+) | ![#002F6F](https://placehold.it/25/002F6F?text=+) | ![#482172](https://placehold.it/25/482172?text=+) |
|    1  | #ACADFF | #00204C | #440154 | ![#ACADFF](https://placehold.it/25/ACADFF?text=+) | ![#00204C](https://placehold.it/25/00204C?text=+) | ![#440154](https://placehold.it/25/440154?text=+) |
|    -  | #FFFFFF | #FFFFFF | #FFFFFF | ![#FFFFFF](https://placehold.it/25/FFFFFF?text=+) | ![#FFFFFF](https://placehold.it/25/FFFFFF?text=+) | ![#FFFFFF](https://placehold.it/25/FFFFFF?text=+) |

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


