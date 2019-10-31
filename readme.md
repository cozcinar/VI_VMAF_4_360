# Voronoi-based VMAF for Omnidirectional Video

## Requirements
Current implementation is based python version 2
First, you need to install the following dependencies:

* pip install wget
* pip install imageio
* pip install python-csv

Second, you need to insert all the distorted and reference mp4 files into the __videos__ folder.

## Test
* python 360vmaf.py --w 3840 --h 2160 --f 100 --r sounders2

> --w: resolution width of the videos
> --h: resolution height of the videos
> --f: number of frames
> --r: reference (original) .mp4 video name

Results will be located in the project folder with distorted video name and in *.csv* format
