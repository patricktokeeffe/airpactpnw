# Twitter Bot - [@AirpactPNW](https://twitter.com/AirpactPNW)

[AIRPACT](http://airpact.wsu.edu) brought to Twitter

The AIRPACT, or *Air Information Report for Public Access and Community Tracking*,
project aims to provide the public with meaningful information about regional air
quality in the Pacific Northwest. This project leverages Twitter to expand the
project's audience and lower barriers to sharing AIRPACT information products. 

Each morning, an instance of this bot assembles new forecast imagery into
a series of animated GIF files, which are then posted to the Twitter account
[@AirpactPNW](https://twitter.com/AirpactPNW). For now, the only species published
on Twitter is fine particulates (PM<sub>2.5</sub>).


### Requirements

*Developed for Python 3 with [Anaconda](https://anaconda.com)*

* Python 3
    * imageio
    * requests
    * pillow
    * tweepy
* [`gifsicle-static`](https://github.com/kornelski/giflossy), for image compression
    * [download v1.82](https://github.com/kornelski/giflossy/releases/download/lossy%2F1.82/gifsicle-1.82-lossy.zip)


### Getting Started

1. Obtain Twitter app credentials
    * If you don't have a developer account, visit <https://dev.twitter.com> to apply
    * Create a new app: <https://developer.twitter.com/apps/new>
    * Under 'Keys and tokens', create an access token
    * Save all these values as `creds.py`:
      ```
      CONSUMER_KEY    = "..."
      CONSUMER_SECRET = "..."
      ACCESS_TOKEN    = "..."
      ACCESS_SECRET   = "..."
      ```
2. Setup a development environment
    * `conda create -n airpactpnw python=3 imageio requests pillow`
    * `conda activate airpactpnw`
3. Get the code
    * `git clone https://github.com/patricktokeeffe/airpactpnw.git`
    * `cd airpactpnw`

To generate animated GIFs, run `./poc.py`.


### Acknowledgements

This project wouldn't be possible without:

* the AIRPACT project and all it's [collaborators](http://lar.wsu.edu/airpact/collaborators.html)
* Twitter
* Python, and these great modules: `imageio`, `requests`, `pillow`, `tweepy`
* [Gifsicle](https://www.lcdf.org/gifsicle/)

Special thanks to Joe Vaughan and Jennifer Hinds for their guidance and patience
answering my AIRPACT questions. 


### Licensing

TBD


### Disclaimer

This project is for educational purposes only and has no guarantees of any kind.
See [here](http://lar.wsu.edu/airpact/disclaimer.html) for the AIRPACT disclaimer.


