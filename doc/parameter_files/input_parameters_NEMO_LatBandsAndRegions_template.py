import  genutil, os.path, time
from datetime import datetime

################################################################################
#  OPTIONS ARE SET BY USER IN THIS FILE AS INDICATED BELOW BY: 
#
################################################################################


## Keywords for the indexation of the metrics results
# -> Model : ModelActivity, ModellingGroup, Model, Experiment, Simname (realization), ModelFreeSpace, Login, Center, SimTrackingDate
# -> Ref : RefActivity, RefName, RefType, RefTrackingDate, RefFreeSpace
# -> Regridding : RegridMethod, Gridname, GridResolution
# -> Metric : Period, MetricName, DataType, Domain (land, ocean...), Region, GeographicalLimits, Variable, MetricFreeSpace, P_value, MetricContactExpert, MetricTrackingDate


# -------------------------------------------------------------------------------------------------------------------
## Which metrics?
## PCMDI_metrics, IPSL_metrics, NEMO_metrics...
which_metrics = 'NEMO_LatBandsAndRegions'

import pcmdi_metrics
funlist=[pcmdi_metrics.ipsl.compute_metrics_latBands,pcmdi_metrics.ipsl.compute_metrics_oceanBasins]
def my_custom(var,dm,do):
  out = {}
  for f in funlist:
           if var in ['tos','sos','wfo','zos']:
              out.update(f(var,dm,do))
  return out
compute_custom_metrics = my_custom
compute_custom_only='true'

# -------------------------------------------------------------------------------------------------------------------
## Path/Filename
path_and_filename = 'targetfile'

## Amount of attributes provided with the results
# => Standard = correspond to the standard amount of information that allows using the portrait plot
# => IPSL_Extended = provides more information (more attributes) with the metrics to store the results in a database
attributes_provided = 'MyAttributes'

## From this, we get all the information we need
dum = str.split(path_and_filename,'/')

# -- position of 'IGCM_OUT'
zero = dum.index('IGCM_OUT')

if 'dmf_import' in dum:
   adj=1
else:
   adj=0


## File name
filename = os.path.basename(path_and_filename)

## Model Path
mod_path = os.path.dirname(path_and_filename)

## Center
# -> For IDRIS : rech
if 'ccc' in dum:
   Center = "CCRT-TGCC"
else:
   Center = "IDRIS"


## Login
Login = dum[zero-(1+adj)]

## Model versions
model_versions = [dum[zero+1]]

## Simtype
experiment = dum[zero+3]

## Realization => simname
realization = dum[zero+4]

## ModelActivity
project_id = "IPSL-"+dum[zero+2]

## Modelling Group
institute_id = "IPSL"

## Period
period = "_".join(str.split(filename,"_")[2:4])

## Model Free Space
ModelFreeSpace = "ModelFreeSpace"

## tracking_id
tracking_id="N/A"

## ModelTrackingDate
creation_date = datetime.fromtimestamp(os.path.getmtime(path_and_filename)).strftime('%Y-%m-%d %H:%M:%S')
#SimTrackingDate = datetime.fromtimestamp(os.path.getmtime(path_and_filename)).strftime('%Y-%m-%d')

## Simulation description map
#if attributes_provided == 'standard':
#  simulation_description_mapping = {}
#else:

## Simulation MD5 sum
simulationCheckSum = str.split(os.popen('md5sum '+path_and_filename).read(),' ')[0]

## Creation date of the metric
metricCreationDate = time.strftime('%Y-%m-%d %H:%M:%S')


simulation_description_mapping = {
            "Model_period":"period",
            "Login":"Login",
            "Center":"Center",
            "tracking_id":"tracking_id",
            "simulationCheckSum":"simulationCheckSum",
            "metricCreationDate":"metricCreationDate",
           }


# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
## Get the suffix of the filename
strfilename = str.split(filename,'_')
suffix = strfilename[len(strfilename)-1].rstrip('.nc')


# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------
## RUN IDENTIFICATION
# DEFINES A SUBDIRECTORY TO METRICS OUTPUT RESULTS SO MULTIPLE CASES CAN BE COMPARED
#case_id = 'IPSL_rewritten_file'
#case_id = 'Test_mapping'
case_id = institute_id+'-'+Login+'-'+model_versions[0]+'-'+experiment+'-'+realization+'-'+period+'-'+attributes_provided+'-'+which_metrics+'-grid_'+suffix
# LIST OF MODEL VERSIONS TO BE TESTED - WHICH ARE EXPECTED TO BE PART OF CLIMATOLOGY FILENAME

### VARIABLES AND OBSERVATIONS TO USE
varsT = ['tos','zos'] 
varsU = []
varsV = []
if suffix=='T':
   vars = varsT
if suffix=='U':
   vars = varsU
if suffix=='V':
   vars = varsV

## regions of mask to use when processing variables
regions = {"tos" : [None],
           "sos" : [None],
           "zos" : [None],
          }


#regions_values = {"terre":0.,}

# Observations to use at the moment "default", "alternate1", "alternate2", "alternate3", or "all" (last two are not always available)
ref = 'all'

# INTERPOLATION OPTIONS
targetGrid        = '2.5x2.5' # OPTIONS: '2.5x2.5' or an actual cdms2 grid object
#targetGrid        = cdms2.createUniformGrid(-89,179,1,0,360,1)
regrid_tool       = 'esmf' # OPTIONS: 'regrid2','esmf'
regrid_method     = 'linear'  # OPTIONS: 'linear','conservative', only if tool is esmf
regrid_tool_ocn   = 'esmf'    # OPTIONS: "regrid2","esmf"
regrid_method_ocn = 'linear'  # OPTIONS: 'linear','conservative', only if tool is esmf

# Do you want to generate a land-sea mask? True or False
generate_sftlf = True

# Mask file
#MaskFilePath = '/data/jservon/Evaluation/grids/'
#MaskFileName = 'LMDZ4.0_9695_grid.nc'

# SAVE INTERPOLATED MODEL CLIMATOLOGIES ?
save_mod_clims = False # True or False

# -------------------------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------------------------
## Model tweaks : here you can define a correspondance table for the variables names

if 'IPSLCM6' not in model_versions[0]:
   model_tweaks = { model_versions[0] :
                    { 'variable_mapping' :
                      {
                        'tos':'sosstsst',      # Sea Surface Temperature
                        'sos':'sosaline',      # Sea Surface Salinity
                        'zos':'sossheig',      # Sea Surface Height
                        'wfo':'sowaflx',
                      }
                    }
                  }
else:
   model_tweaks = {}
# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------
## DATA LOCATION: MODELS, OBS AND METRICS OUTPUT

## Templates for climatology files
filename_template = filename

## ROOT PATH FOR MODELS CLIMATOLOGIES
mod_data_path = mod_path

## ROOT PATH FOR OBSERVATIONS
obs_data_path = 'my_obs_data_path/'

## DIRECTORY WHERE TO PUT RESULTS
metrics_output_path = 'my_metrics_output_path/'

## DIRECTORY WHERE TO PUT INTERPOLATED MODELS' CLIMATOLOGIES
model_clims_interpolated_output = ''
filename_output_template = "Metrics_%(model_version)."+experiment+"."+realization+".mo.%(table).%(variable).ver-1.%(period).%(region).AC.nc"

# -------------------------------------------------------------------------------------------------------------------

