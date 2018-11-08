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

AIRPACT PM2.5 AQI colors extracted from source imagery.

<table width="50%" border="2"><tbody>
<tr>
<td>AQI scale</td>
<td>AIRPACT PM2.5 AQI (imagery)</td>
<td>AIRPACT PM2.5 AQI (legend)</td>
<td><a href="https://bokeh.pydata.org/en/latest/docs/reference/palettes.html#bokeh.palettes.cividis">cividis</a></td>
<td><a href="https://bokeh.pydata.org/en/latest/docs/reference/palettes.html#bokeh.palettes.viridis">viridis</a></td>
<td><a href="https://bokeh.pydata.org/en/latest/docs/reference/palettes.html#usability-palettes">color blind</a></td>
</tr>
<tr>
<td style="background-color:rgb(0,228,0)">Green</td>
<td style="background-color:rgb(0,255,0)">&nbsp;</td>
<td style="background-color:rgb(36,225,0)">&nbsp;</td>
<td style="background-color:rgb(255,233,69)">&nbsp;</td>
<td style="background-color:rgb(253,231,36)">&nbsp;</td>
<td style="background-color:rgb(0,114,178)">&nbsp;</td>
</tr>
<tr>
<td style="background-color:rgb(255,255,0)">Yellow</td>
<td style="background-color:rgb(255,255,0)">&nbsp;</td>
<td style="background-color:rgb(252,252,20)">&nbsp;</td>
<td style="background-color:rgb(202,185,105)">&nbsp;</td>
<td style="background-color:rgb(121,209,81)">&nbsp;</td>
<td style="background-color:rgb(230,159,0)">&nbsp;</td>
</tr>
<tr>
<td style="background-color:rgb(255,126,0)">Orange</td>
<td style="background-color:rgb(255,165,0)">&nbsp;</td>
<td style="background-color:rgb(252,126,0)">&nbsp;</td>
<td style="background-color:rgb(149,143,120)">&nbsp;</td>
<td style="background-color:rgb(34,167,132)">&nbsp;</td>
<td style="background-color:rgb(240,228,66)">&nbsp;</td>
</tr>
<tr>
<td style="background-color:rgb(255,0,0)">Red</td>
<td style="background-color:rgb(255,0,0)">&nbsp;</td>
<td style="background-color:rgb(252,22,0)">&nbsp;</td>
<td style="background-color:rgb(102,104,112)">&nbsp;</td>
<td style="background-color:rgb(41,120,142)">&nbsp;</td>
<td style="background-color:rgb(0,158,115)">&nbsp;</td>
</tr>
<tr>
<td style="background-color:rgb(143,63,151)">Purple</td>
<td style="background-color:rgb(139,28,98)">&nbsp;</td>
<td style="background-color:rgb(151,11,76)">&nbsp;</td>
<td style="background-color:rgb(49,68,107)">&nbsp;</td>
<td style="background-color:rgb(64,67,135)">&nbsp;</td>
<td style="background-color:rgb(86,180,233)">&nbsp;</td>
</tr>
<tr>
<td style="background-color:rgb(126,0,35)">Maroon</td>
<td style="background-color:rgb(139,26,26)">&nbsp;</td>
<td style="background-color:rgb(124,6,33)">&nbsp;</td>
<td style="background-color:rgb(0,32,76)">&nbsp;</td>
<td style="background-color:rgb(68,1,84)">&nbsp;</td>
<td style="background-color:rgb(213,94,0)">&nbsp;</td>
</tr>
</tbody></table>


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


