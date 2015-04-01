#!/bin/python
import shutil
import string, os
import glob

# =================================================================================================== #
# == METRICS at IPSL, using the PCMDI Metrics Package
# == Loop-on-multiple-files.py
# == Author: Jerome Servonnat (LSCE - CEA - IPSL)
# == Contact: jerome.servonnat@lsce.ipsl.fr
# == 
# ===== BLOCK 1 =======================================
# == This script does a loop on a selection of files that the user can select via searching criteria:
# ==  - login: the users login (p86jser, p86maf,...)
# ==  - TagName: the name of the model (IPSLCM5A,...)
# ==  - SpaceName: PROD, DEVT, TEST
# ==  - ExperimentName: historical, piControl,...
# ==  - JobName: name of the simulation
# == There is also a possibility to filter the results by giving an interval of dates (year)
# == for the starting date of the period of the seasonal cycle: 
# ==  - DateBegin: minimum starting date for the period 
# ==  - DateEnd: maximum starting date for the period

# == If search_only == 'true', operates only the search for the target files
# == and won't execute the metrics package
search_only='false'
#search_only='true'

dryrun='false'

clean_scratch='false'

# -> the different fields can take either a given value or *
group='dsm'
#login='p86caub'
#TagName='IPSLCM6'
#SpaceName='PROD'
#ExperimentName='piControl'
#JobName='CTLCM6*'
#DateBegin=1850
#DateEnd=DateBegin+2029

login='p86mart'
TagName='IPSLCM6'
SpaceName='DEVT'
ExperimentName='piControl'
JobName='OR9V0*'
DateBegin=850
DateEnd=DateBegin+2029



#group='gen6178'
#login='aidel'
#TagName='LMDZOR'
#SpaceName='DEVT'
#ExperimentName='clim'
#JobName='NPv5.12a'
#DateBegin=1850
#DateEnd=2500  #DateBegin+9
dmf_import=''
#dmf_import='/dmf_import'

#METRICS=['LMDZ_PCMDI','LMDZ_JetLat','NEMO_PCMDI','NEMO_LatBandsAndRegions','LIM3','ORCHIDEE','PISCES']
METRICS = ['LMDZ_PCMDI','LMDZ_JetLat','NEMO_PCMDI','NEMO_LatBandsAndRegions']

# =================================================================================================== #







# ===== BLOCK 2 =======================================
# == Within this block we define the path to the directory of the working installation,
# == the path to the python, the driver, the parameter file, the output path for the
# == results, and the path to the references.
# == 'extensions' defines the two types of SE files to be used
# == 'attributes_provided' defines the level of information provided with the results
# -- Root directory
main_path='/ccc/work/cont003/dsm/p86ipsl/PCMDI-MP/work_install_v2.11/PCMDI_METRICS/'
# -- Path to the python installed with the package
WhichPython = '/ccc/work/cont003/dsm/p86ipsl/PCMDI-MP/work_install_v2/PCMDI_METRICS/bin/python'
# -- Path to the Metrics Package driver
WhichDriver = main_path+'bin/pcmdi_metrics_driver.py'
# -- Obs path
obs_data_path = '/ccc/work/cont003/dsm/p86ipsl/PCMDI-MP/references-for-metrics/obs/'
# -- Metrics Output path
metrics_output_path = '/ccc/store/cont003/dsm/p86ipsl/metrics_results/'
# -- Scratchdir
scratchdir='/ccc/scratch/cont003/dsm/p86ipsl/tmp_files_for_metrics'

if clean_scratch=='true':
   os.system('rm -rf '+scratchdir+'/*')
# =================================================================================================== #




for METRIC in METRICS:
    print 'METRIC = ', METRIC
    
    # ===== BLOCK 3 =======================================
    # -- Template of the parameter file ; this template is copied ; the copy will be used as parameter file after edition with sed
    template_parameter_file=main_path+'doc/parameter_files/input_parameters_'+METRIC+'_template.py'

    if 'LMDZ' in METRIC:
       realm = 'ATM' ; suffix = '*.nc'
    if METRIC in ['NEMO_PCMDI','NEMO_LatBandsAndRegions']:
       realm = 'OCE' ; suffix = '*grid_T.nc'
    if METRIC == 'LIM3':
       realm = 'ICE' ; suffix = '*icemod.nc'
    if METRIC == 'ORCHIDEE':
       realm = 'SRF' ; suffix = '*.nc'
    if METRIC == 'PISCES':
       realm = 'OCE' ; suffix = '*.nc'

    files=glob.glob('/ccc/store/cont003/'+group+'/'+login+dmf_import+'/IGCM_OUT/'+TagName+'/'+SpaceName+'/'+ExperimentName+'/'+JobName+'/'+realm+'/Analyse/SE/'+suffix)
    
    print '/ccc/store/cont003/dsm/'+login+dmf_import+'/IGCM_OUT/'+TagName+'/'+SpaceName+'/'+ExperimentName+'/'+JobName+'/'+realm+'/Analyse/SE/'+suffix 
    print '--- We will calculate metrics using :'
    print ' -> python = '+WhichPython
    print ' -> driver = '+WhichDriver
    print ' -> parameter file = '+template_parameter_file
    print '--- ... on the following files:'
    selected_files = []
    for file in files:
      if 'COSP' not in file:
        #print file
        dum=str.split(file,'_')
        startdate = dum[len(dum)-4]
        #print 'startdate = ',startdate
        if DateBegin <= int(startdate) <= DateEnd:
           path = os.path.dirname(file)
           filename = os.path.basename(file)
           outpath = scratchdir+path
           if not os.path.isdir(outpath):
              cmd = 'mkdir -p '+outpath
              os.system(cmd)
           outfile = outpath+'/'+filename
           print outfile
           if not os.path.isfile(outfile) and search_only=='false':
              cmd11 = 'ccc_hsm get '+file
              cmd2 = 'cp '+file+' '+outpath
              os.system(cmd11)
              os.system(cmd2)
           selected_files.append(outfile)
    
    files = selected_files
    # =================================================================================================== #

    
    # ===== BLOCK 4 =======================================
    if 'NEMO' in METRIC:
       for file in files:
         path = os.path.dirname(file)
         cmd3 = 'ncks --append -v lon_bnds,lat_bnds ORCA2_lon_lat_bounds.nc '+file
         cmd4 = 'ncatted -O -a bounds,nav_lat,o,c,"lat_bnds" '+file
         cmd5 = 'ncatted -O -a bounds,nav_lon,o,c,"lon_bnds" '+file
         if search_only=='false':
            print cmd3
            os.system(cmd3)
            print cmd4
            os.system(cmd4)
            print cmd5
            os.system(cmd5)
      
      
    from datetime import datetime
    delay = datetime.utcnow() - datetime(2015,1,1)
    additionnal = str(delay.microseconds)
    
    if search_only=='false':
       for file in files:
            tmp_param = string.replace(template_parameter_file,'.py','_tmp_'+additionnal+'.py')
            # -- create the output dir
            print "Working on this file = "+file
            tmp = str.split(file,'/')
            if 'dmf_import' in tmp:
              adj = -2
            else:
              adj = -1
            ttmp = tmp[tmp.index('IGCM_OUT')+adj:len(tmp)-4]
            #R_OUT='/'.join(ttmp)
            today = datetime.today().strftime("%Y-%m-%d") 
            R_OUT='/'+today+'/raw/'
            R_SAVE = metrics_output_path+R_OUT
            if os.path.isdir(R_SAVE):
               print 'Output directory '+R_SAVE+' already exists'
            else:
               os.makedirs(R_SAVE)
            print 'tmp_param = ',tmp_param 
            shutil.copyfile(template_parameter_file,tmp_param)
            cmd2 = 'sed -e "s#targetfile#'+file+'#g" '+tmp_param+' > fichier.tmp && mv -f fichier.tmp '+tmp_param
            cmd3 = 'sed -e "s#MyAttributes#standard#g" '+tmp_param+' > fichier.tmp && mv -f fichier.tmp '+tmp_param
            cmd4 = 'sed -e "s#my_obs_data_path#'+obs_data_path+'#g" '+tmp_param+' > fichier.tmp && mv -f fichier.tmp '+tmp_param
            cmd5 = 'sed -e "s#my_metrics_output_path#'+R_SAVE+'#g" '+tmp_param+' > fichier.tmp && mv -f fichier.tmp '+tmp_param
            cmd6 = WhichPython+' '+WhichDriver+' -p '+tmp_param
            print cmd2
            print cmd3
            print cmd4
            print cmd5
            print cmd6
            if dryrun == 'false':
               os.system(cmd2)
               os.system(cmd3)
               os.system(cmd4)
               os.system(cmd5)
               os.system(cmd6)
               os.remove(tmp_param)
               os.remove(tmp_param+'c')
               os.remove(file)




