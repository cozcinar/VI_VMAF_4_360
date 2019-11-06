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
* VMAF is calculated based on equirectangular format.
* VI-VMAF is calculated based on the spherical voronoi technique which is explained in the paper: Voronoi-based Objective Quality Metrics for Omnidirectional Video. 
You can check the paper in __doc__ folder.


### Advance options

* Changing VMAF model: In 360vmaf.py, you can change the VMAF model. The default model is vmaf_rb_v0.6.3.
> vmaf_model      =  'vmaf_rb_v0.6.3/vmaf_rb_v0.6.3.pkl'

* Specifying number of Voronoi patches. By using option '--c', you can specify the usage of number of patches, for example '--c 15'. 
The default parameter is 15. If you do not specify the number of patches, the script uses the default parameter which is 15. 

> python 360vmaf.py --w 3840 --h 2160 --f 100 --r sounders2 --c 15




