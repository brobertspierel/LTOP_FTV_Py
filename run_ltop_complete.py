import ee 
import params
import time 
import pandas as pd 
import ltop 
import lt_params
from run_SNIC_01 import RunSNIC
import run_kMeans_02_1 as kmeans_1
import run_kMeans_02_2 as kmeans_2
import abstract_sampling_03 as ab_img
import abstract_imager_04 as run_lt_pts
import ltop_lt_paramater_scoring_01 as param_scoring
import generate_LTOP_05 as make_bps

"""
This script is intended to run the entire LandTrendr Optimization (LTOP) workflow for paramater 
selection of the LandTrendr algorithm (Kennedy et al, 2014; 2018). The process relies on a series of scripts that: 
1. spatially segment the target aoi based on spectracl characteristics of an underlying dataset 
2. Cluster those spatial segments (patches) into spectrally similar clusters. This step uses the kmeans algorithm
3. Spectral information and associated cluster information is stored in abstract images to decrease storage, computation and run time
4. LandTrendr is run for every cluster (group of patches) on the landscape and a paramater scoring regime is carried out to select the best
'version' of LandTrendr for that target land cover/land use class 
5. Selected verions of LT are run on all of the clusters and the final image is put back together. The final output are the breakpoints that 
one expects from a standard LandTrendr run. 

Dependencies: 
The required scripts can be cloned or forked from GitHub at: XXXXXXXXXXXXX
For more information on the process and the theory behind it see the documentation on GitHub at: XXXXXXXXXXXXXXXXXXXXXXXX

Notes: 
This script is set up so that it will run through all of the steps in the LTOP workflow, waiting in between steps for the previous output to finish
generating before going on to the next step. Depending on the area you are running, this could take a long time (days). This is why it is built 
in a .py script and not a Jupyter Notebook. There is an associated Jupyter Notebook for doing small test areas located on GitHub at: XXXXXXXXXXXXXXXXXXXX. 
The intermediate outputs will be generated in a user specified assets folder on your GEE account and the location of this folder can be 
specified in the params.py file under assetsRoot and assetsChild. 
"""

def check_task_status(task_dict): 
    '''
    Check on the status of a GEE batch task submitted to GEE servers. Input to this function should be a dictionary that is formatted 
    like the output of task.status()
    '''
    task_id = task_dict['id']
    #for some reason GEE defaults this to a list with a dictioanary as its only item
    task_status = ee.data.getTaskStatus(task_id)[0]
    
    return task_status['state']

def main(): 
    
    #1. run SNIC
    snic = RunSNIC(params)
    status1,status2 = snic.generate_tasks()
    while True:
        try: 
            ts_1 = check_task_status(status1) 
            ts_2 = check_task_status(status2) 
            
            if (ts_1 == 'COMPLETED') & (ts_2 == 'COMPLETED'): 
                print('The previous task is complete')
                km_status = kmeans_1.generate_tasks(params.params)
                break
            elif (ts_1 == 'FAILED') | (ts_1 == 'CANCELLED'): 
                print('The first snic task failed')
                break
            elif (ts_2 == 'FAILED') | (ts_2 == 'CANCELLED'): 
                print('The second snic task failed')
                break 
        except NameError: 
            print('You did not run the snic step so there is no status to check')
            break
    
    #2. run kmeans
    while True: 
        if km_status == 'COMPLETED':
            km_pts_status = kmeans_2.generate_tasks(params.params)
            break
        elif (km_status == 'FAILED') | (km_status == 'CANCELLED'): 
                print('The generation of stratified random points failed')
                break

    #3. generate abstract images
    while True: 
        if km_pts_status == 'COMPLETED':
            ab_imgs_status = ab_img.create_abstract_imgs(params.params)
        elif (km_pts_status == 'FAILED') | (km_pts_status == 'CANCELLED'): 
                print('The generation of stratified random points failed')
                break

if __name__ == '__main__': 
    main()
    