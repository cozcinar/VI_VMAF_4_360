# Voronoi-based VMAF for Omnidirectional Video

## Requirements
Current implementation is based Python 3.

### Dependencies: 

Firstly, you should install the following dependencies:

* pip install wget
* pip install imageio
* pip install python-csv

### Adding mp4 files

Secondly, you should locate all distorted and reference mp4 files into the __videos__ folder.

### Testing

* python 360vmaf.py --w 3840 --h 2160 --f 100 --r sounders2

> --w: resolution width of the videos, for example 3840

> --h: resolution height of the videos, for example 2160

> --f: number of frames, for example 100

> --r: reference (original) .mp4 video name, for example sounders2.mp4, so you should *not* include the video type '.mp4'

Results will be located in the main folder with the distorted video name and in *.csv* format. The script can generate two different quality scores: VMAF and VI-VMAF.
* VMAF is calculated based on equirectangular format
* VI-VMAF is calculated based on Spherical voronoi diagram which is explained in the paper: Voronoi-based Objective Quality Metrics for Omnidirectional Video. 
You can check the paper in __doc__ folder.

