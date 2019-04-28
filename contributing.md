# Contributing to @airpactpnw


## Requirements

*Developed for Python 3 with [Anaconda](https://anaconda.com)*

* Python 3
    * imageio
    * requests
    * pillow
    * tweepy
* [`gifsicle-static`](https://github.com/kornelski/giflossy), for image compression
    * [download v1.82](https://github.com/kornelski/giflossy/releases/download/lossy%2F1.82/gifsicle-1.82-lossy.zip)


## Getting Started

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


