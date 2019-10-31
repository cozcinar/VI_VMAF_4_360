# coding: utf-8
# A script to estimate quality score using VMAF for 360-degree video
# Any problem, contact to Cagri Ozcinar, cagriozcinar@gmail.com
# More description related to the metric, you can check our project page: https://v-sense.scss.tcd.ie/research/voronoi-based-objective-metrics/
# and publication: Croci et al. "Voronoi-based Objective Quality Metrics for Omnidirectional Video", QoMEX 2019
# importing required modules 
from zipfile import ZipFile 
# import requests
import wget
import os
import glob
import imageio
import re
import xml.etree.ElementTree as ET
import argparse
import csv

# specifying the zip file name 
file_name       = 'voronoiMetrics.zip'
thirdParty_zip  = 'voronoiMetricsThirdParty.zip'
project_name    = 'voronoiVMAF/' 
video_folder    = 'videos/'
vpatch          = 'ExeAndDlls/OmniVideoQuality.exe'
vmaf_model      =  'vmaf_rb_v0.6.3/vmaf_rb_v0.6.3.pkl'

def width_height_from_str(s):
    m = re.search(".*[_-](\d+)x(\d+).*", s)
    if not m:
        print ("Could not find resolution in file name: %s" % (s))
        exit(1)

    w = int(m.group(1))
    h = int(m.group(2))
    return w,h

def create_dir(folder):
    try:
        os.makedirs(folder)
    except:
        pass


def extract_process(name):
    # opening the zip file in READ mode 
    with ZipFile(name, 'r') as zip: 
        # printing all the contents of the zip file 
        zip.printdir() 
  
        # extracting all the files 
        print('Extracting all the files now...') 
        zip.extractall(project_name + '/') 
        print('Done!')

def mp42yuv(name):
    cmd = project_name + 'ffmpeg -y -i ' + name + ' -c:v rawvideo -pix_fmt yuv420p ' + video_folder + os.path.basename(name)[:-3] + 'yuv'
    cmd = cmd.replace("/","\\")
    #import pdb; pdb.set_trace()
    os.system(cmd)

def report_results(video, patch, ref):
    '''
    Step 3: Report the results
    '''
    result_patch    = video_folder + 'results/' + os.path.basename(video)[:-4] + '/' + os.path.basename(patch)[:-4] + '.xml'
    doc = ET.parse(result_patch)
    root = doc.getroot()
    res = []
    for elem in root.iter('frame'):
        res.append(elem.attrib['vmaf'])
    return res

def compute_patchScores(video, patch, ref):
    '''
    Step 2: Computing the Voronoi patch scores 
    '''

    dis_patch       = video_folder + 'results/' + os.path.basename(video)[:-4] + '/' + os.path.basename(patch)
    ref_patch       = video_folder + 'results/' + ref + '/' + os.path.basename(patch)
    height_patch    = width_height_from_str(ref_patch)[1]
    width_patch     = width_height_from_str(ref_patch)[0]
    result_patch    = video_folder + 'results/' + os.path.basename(video)[:-4] + '/' + os.path.basename(patch)[:-4] + '.xml'


    cmd  = project_name + 'vmafossexec yuv420p ' + str(width_patch) + ' ' + str(height_patch) + ' ' + ref_patch + ' ' \
    + dis_patch + ' ' + project_name + 'model/' + vmaf_model + ' --log ' + result_patch + ' --log_fmt csv --psnr --ssim --ms-ssim --thread 0 --subsample 1 --ci'
    cmd = cmd.replace("/","\\")
    os.system(cmd)

def generate_patches(video):
    '''
    Step 1: Generate Voronoi patches 
    '''
    cmd = project_name + vpatch + ' ' + video_folder + 'results/' + os.path.basename(video)[:-4] + '.xml'
    cmd = cmd.replace("/","\\")
    os.system(cmd)

def xml_created(video, user_input):
# use the parse() function to load and parse an XML file
    doc = ET.parse(project_name + "ConfigXMLExamples/" + "ConfigParameters.xml")
    root = doc.getroot()

    for elem in root:
        # for subelem in elem:
        if elem.tag == 'YUVODVTessellation':
            elem.attrib['ODVFn']                = video_folder + os.path.basename(video)[:-3] + 'yuv'
            elem.attrib['ODVHeight']            = user_input.h
            elem.attrib['ODVWidth']             = user_input.w
            elem.attrib['binMaskFlag']          = str(0)
            elem.attrib['frameNum']             = user_input.f
            elem.attrib['frameSkip']            = str(0)
            elem.attrib['patchVidFn']           = video_folder + 'results/' + os.path.basename(video)[:-4] + '/patch%03u.yuv' 
            elem.attrib['pixDeg']               = str(10)
            elem.attrib['voroMATLABFn']         = project_name + "SphericalVoronoiDiagrams/SphereVoroMATLAB_CellNum15.txt"
    doc.write(video_folder + 'results/' + os.path.basename(video)[:-4] + '.xml')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(description='VMAF ODV')

    parser.add_argument('--w', required=True, action="store", help="resolution width of a given videos")
    parser.add_argument('--h', required=True, action="store", help="resolution height of a given videos")
    parser.add_argument('--f', required=True, action="store", help="number of frame")
    parser.add_argument('--r', required=True, action="store", help="reference video")

    user_input = parser.parse_args()

    # download the zip file and extract it
    try:
    #    # create_dir(project_name)
        wget.download('http://v-sense.scss.tcd.ie/Datasets/' + file_name, file_name)
        extract_process(file_name)
        wget.download('http://v-sense.scss.tcd.ie/Datasets/' + thirdParty_zip, thirdParty_zip)
        extract_process(thirdParty_zip)
    except:
        print("No file to be downloaded!")

    # generate patches
    try:
        for video in glob.glob(video_folder + '*.mp4'):
            # convert mp4 to yuv
            mp42yuv(video)
            # create a folder for each video
            create_dir(video_folder + 'results/' + os.path.basename(video)[:-4] + '/')
            # generate xml file for each video settings
            xml_created(video, user_input)
            # generate patches
            generate_patches(video)
    except:
        print("Error in patch generation")
    
    try:
        for video in glob.glob(video_folder + '*.mp4'):
            if os.path.basename(video)[:-4] != user_input.r:
                for patch in glob.glob( video_folder + 'results/' + os.path.basename(video)[:-4] + '/*.yuv'):
                    compute_patchScores(video, patch, user_input.r)
    except:
        print("Error in quality estimation")

    # report and clean the project
    try:
        for video in glob.glob(video_folder + '*.mp4'):
            if os.path.basename(video)[:-4] != user_input.r:
                agg_result = {}
                for patch in glob.glob( video_folder + 'results/' + os.path.basename(video)[:-4] + '/*.yuv'):
                    agg_result[os.path.basename(patch)[:-4]] = report_results(video, patch, user_input.r)

                rows = [agg_result[x] for x in agg_result.keys()]
#for python2 delete newline and add wb
                with open(os.path.basename(video)[:-4] + '.csv', 'wb') as f:
                    w = csv.writer(f)

                    list_ll = [key for key in agg_result.keys()]
                    list_ll.append('360VMAF')
                    # list_ll = list(agg_result.keys()).append('360VMAF')
                    
                    w.writerow(list_ll)
                    # import pdb; pdb.set_trace()
                    for f in range(len(rows[0])):
                        row = [rows[l][f] for l in range(len(agg_result.keys()))]                        
                        vor_vmaf = [float(rows[l][f]) for l in range(len(agg_result.keys()))]
                        vor_vmaf = sum(vor_vmaf)/len(agg_result.keys())
                        
                        row.append(str(vor_vmaf))
                        w.writerow(row)

    except:
        print("Error in reporting")