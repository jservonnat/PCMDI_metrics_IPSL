import MV2 as MV
import cdms2 as cdms
from genutil import statistics
import cdutil
import pcmdi_metrics
import getJetLat


def compute_metrics(var,dm_glb,do_glb):
  
  cdms.setAutoBounds('on')
  
  metrics_dictionary = {}
  sig_digits = '.2f'

  if 'ua' in var:
    # == Jet latitudes def 1 ================================================================
    for sea in ['ann','djf','jja']:
        
	if sea=='ann':
	   dm_sea, do_sea = pcmdi_metrics.pcmdi.annual_mean.compute(dm_glb,do_glb)
	   #do_sea = do_glb
	else:
	   dm_sea = pcmdi_metrics.pcmdi.seasonal_mean.compute(dm_glb,sea)
	   do_sea = pcmdi_metrics.pcmdi.seasonal_mean.compute(do_glb,sea)

        for hemisphere in ['NHEX','SHEX']:
            model_jetlat = pcmdi_metrics.ipsl.getJetLat.compute(dm_sea,hemisphere=hemisphere)
            ref_jetlat = pcmdi_metrics.ipsl.getJetLat.compute(do_sea,hemisphere=hemisphere)
            bias_jetlat = model_jetlat - ref_jetlat
            metrics_dictionary['jetlat_bias_'+sea+'_'+hemisphere] = format(bias_jetlat,sig_digits)
            metrics_dictionary['jetlat_'+sea+'_'+hemisphere] = format(model_jetlat,sig_digits)
            print var,'  '+hemisphere+' '+sea+' Jet latitudinal bias is ' , bias_jetlat
        
            # -- Pacific sector
            model_jetlat = pcmdi_metrics.ipsl.getJetLat.compute(dm_sea(lon=(120.,280.)),hemisphere=hemisphere)
            ref_jetlat = pcmdi_metrics.ipsl.getJetLat.compute(do_sea(lon=(120.,280.)),hemisphere=hemisphere)
            bias_jetlat = model_jetlat - ref_jetlat
            metrics_dictionary['jetlat_bias_'+sea+'_Pacific'+hemisphere] = format(bias_jetlat,sig_digits)
            metrics_dictionary['jetlat_'+sea+'_Pacific'+hemisphere] = format(model_jetlat,sig_digits)
            print var,'  Pacific'+hemisphere+' 120E/280E '+sea+' Jet latitudinal bias is ' , bias_jetlat

        # -- North Atlantic sector
        model_jetlat = pcmdi_metrics.ipsl.getJetLat.compute(dm_sea(lon=(-80.,40.)),hemisphere="NHEX")
        ref_jetlat = pcmdi_metrics.ipsl.getJetLat.compute(do_sea(lon=(-80.,40.)),hemisphere="NHEX")
        bias_jetlat = model_jetlat - ref_jetlat
        metrics_dictionary['jetlat_bias_ann_NAtl'] = format(bias_jetlat,sig_digits)
        metrics_dictionary['jetlat_ann_NAtl'] = format(model_jetlat,sig_digits)
        print var,'  NAtl '+sea+' -80/40E Jet latitudinal bias is ' , bias_jetlat



  return metrics_dictionary 
