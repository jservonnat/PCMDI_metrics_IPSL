import  genutil, os.path, time, cdms2
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
# PCMDI_metrics, IPSL_metrics, NEMO_metrics...

#import pcmdi_metrics # Or whatever your custom metrics package name is
#compute_custom_metrics = pcmdi_metrics.ipsl.compute_metrics
#compute_custom_only = 'true'
import pcmdi_metrics
funlist=[pcmdi_metrics.ipsl.compute_metrics_latBands,pcmdi_metrics.ipsl.compute_metrics_oceanBasins]
def my_custom(var,dm,do):
  out = {}
  for f in funlist:
            out.update(f(var,dm,do))
  return out
compute_custom_metrics = my_custom




# -------------------------------------------------------------------------------------------------------------------
## Path/Filename
path_and_filename = '/data/jservon/IPSL_DATA/SIMULATIONS/p86caub/IGCM_OUT/IPSLCM6/PROD/piControl/CTLCM6E/OCE/Analyse/SE/CTLCM6E_SE_2700_2709_1M_grid_T-test.nc'
#path_and_filename = '/data/jservon/IPSL_DATA/SIMULATIONS/p86caub/IGCM_OUT/IPSL-CM5A-LR/PROD/historical/r1i1p1/OCE/Analyse/SE/tos_Omon_IPSL-CM5A-LR_historical_r1i1p1_SE_198001-200512.nc'


## Amount of attributes provided with the results
# => Standard = correspond to the standard amount of information that allows using the portrait plot
# => IPSL_Extended = provides more information (more attributes) with the metrics to store the results in a database
attributes_provided = 'standard'

## From this, we get all the information we need
dum = str.split(path_and_filename,'/')

## File name
filename = dum[len(dum)-1]

## Model Path
mod_path = path_and_filename.rstrip(filename)

## Center
Center = "CCRT-TGCC"

## Login
Login = dum[5]

## Model versions
model_versions = [dum[7]]

## Simtype
experiment = dum[9]

## Realization => simname
realization = dum[10]

## ModelActivity
project_id = "IPSL-"+dum[8]

## Modelling Group
institute_id = "IPSL"

## Period
model_period = "_".join(str.split(filename,"_")[2:4])
period=model_period

## Model Free Space
ModelFreeSpace = "Tests libIGCM"

## ModelTrackingDate
creation_date = datetime.fromtimestamp(os.path.getmtime(path_and_filename)).strftime('%Y-%m-%d %H:%M:%S')
#SimTrackingDate = datetime.fromtimestamp(os.path.getmtime(path_and_filename)).strftime('%Y-%m-%d')

## tracking_id
tracking_id="N/A"

## Simulation description map
#if attributes_provided == 'standard':
#  simulation_description_mapping = {}
#else:
simulation_description_mapping = {
				    "model_period":"model_period",
				    "Login":"Login",
				    "Center":"Center",
				    "tracking_id":"tracking_id"
				   }


# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------
## RUN IDENTIFICATION
# DEFINES A SUBDIRECTORY TO METRICS OUTPUT RESULTS SO MULTIPLE CASES CAN BE COMPARED
#case_id = 'IPSL_rewritten_file'
#case_id = 'Test_mapping'
case_id = institute_id+'-'+Login+'-'+model_versions[0]+'-'+experiment+'-'+realization+'-'+model_period+'-'+attributes_provided
# LIST OF MODEL VERSIONS TO BE TESTED - WHICH ARE EXPECTED TO BE PART OF CLIMATOLOGY FILENAME

### VARIABLES AND OBSERVATIONS TO USE
vars = ['tos']#,'sos']
#strfilename = str.split(filename,'_')
#if strfilename[len(strfilename)-1]=='T.nc':
#   vars = varsT

## regions of mask to use when processing variables
regions = {
           'tos':[None],
           'sos':['ocean']
          }


#regions_values = {"terre":0.,}

# Observations to use at the moment "default", "alternate1", "alternate2", "alternate3", or "all" (last two are not always available)
ref = ['default']

# INTERPOLATION OPTIONS
targetGrid        = '2.5x2.5' # OPTIONS: '2.5x2.5' or an actual cdms2 grid object
targetGrid        = '1.0x1.0'
#targetGrid        = cdms2.createUniformGrid(-89,179,1,0,360,1)
#targetGrid        = '1.0x1.0' # OPTIONS: '2.5x2.5' or an actual cdms2 grid object
regrid_tool       = 'esmf' # OPTIONS: 'regrid2','esmf'
regrid_method     = 'linear'  # OPTIONS: 'linear','conservative', only if tool is esmf
regrid_tool_ocn   = 'regrid2'    # OPTIONS: "regrid2","esmf"
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

model_tweaks = { model_versions[0] :
                    { 'variable_mapping' :
                        {
			'tos':'sosstsst',      # SST
			'sos':'sosaline',      # SSS
			'sic':'ice_pres',      # Sea Ice Concentration
			'sit':'iicethic',      # Sea Ice Thickness
			'wfo':'sowaflup',      # Upward E-P budget
			'somxl010':'somxl010'  # Mixed-layer depth
                        }
                    }
               }

# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------
## DATA LOCATION: MODELS, OBS AND METRICS OUTPUT

## Templates for climatology files
filename_template = filename

## ROOT PATH FOR MODELS CLIMATOLOGIES
mod_data_path = mod_path

## ROOT PATH FOR OBSERVATIONS
obs_data_path = '/data/jservon/Evaluation/ReferenceDatasets/PCMDI-MP/obs/'

## DIRECTORY WHERE TO PUT RESULTS
metrics_output_path = '/home/igcmg/PCMDI-MP/install_IPSL/PCMDI_METRICS/metrics_results/'

## DIRECTORY WHERE TO PUT INTERPOLATED MODELS' CLIMATOLOGIES
model_clims_interpolated_output = ''
filename_output_template = "Metrics_%(model_version)."+experiment+"."+realization+".mo.%(table).%(variable).ver-1.%(period).%(region).AC.nc"

# -------------------------------------------------------------------------------------------------------------------

