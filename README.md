# TIDALbar

A very unofficial CLI player for the [TIDAL music streaming service](http://tidal.com). 

This project is built upon the excellent [tidalapi](https://github.com/tamland/python-tidal) and [python-mpv](https://github.com/jaseg/python-mpv) libraries. 

Using tidalapi, it is possible to acquire the RTMP URLs for tracks on TIDAL. [mpv](https://mpv.io) is used to fetch and play the RTMP stream. 

### Installation

Clone the repo:
`git clone https://github.com/bsilvereagle/tidalbar.git`

Install `tidalapi` pip module:

`pip install tidalapi`

Get the `python-mpv` module from Github, NOT python repos:

`cd tidalbar`
`wget -O mpv.py https://raw.githubusercontent.com/jaseg/python-mpv/master/mpv.py`


### Usage

`python3 tidalbar.py`

### License

Licensed under the [Apache License](https://www.apache.org/licenses/LICENSE-2.0.html).
