import cdms2 as cdms
import pcmdi_metrics

def compute_metrics_oceanBasins(var,dm_glb,do_glb):
    cdms.setAutoBounds('on')
    metrics_dictionary = {}
    
    domains = ['NorthAtlantic','NorthPacific','Indian','SouthernOcean','TropicalPacific','TropicalAtlantic','Labrador']
    
    for dom in domains:
        
        dm = dm_glb
        do = do_glb
        
        if dom == 'NorthAtlantic':
            dm = dm_glb(latitude = (40.,70), longitude = (-80.,0.))
            do = do_glb(latitude = (40.,70), longitude = (-80.,0.))
        if dom == 'NorthPacific':
            dm = dm_glb(latitude = (40.,65), longitude = (120.,250.))
            do = do_glb(latitude = (40.,65), longitude = (120.,250.))
        if dom == 'TropicalPacific':
            dm = dm_glb(latitude = (-20.,20), longitude = (120.,280.))
            do = do_glb(latitude = (-20.,20), longitude = (120.,280.))
        if dom == 'TropicalAtlantic':
            dm = dm_glb(latitude = (-20.,20), longitude = (-60.,10.))
            do = do_glb(latitude = (-20.,20), longitude = (-60.,10.))
        if dom == 'Indian':
            dm = dm_glb(latitude = (-30.,30), longitude = (50.,110.))
            do = do_glb(latitude = (-30.,30), longitude = (50.,110.))
        if dom == 'SouthernOcean':
            dm = dm_glb(latitude = (-60.,-30))
            do = do_glb(latitude = (-60.,-30))
        if dom == 'Labrador':
            dm = dm_glb(latitude = (50.,70), longitude = (-70.,-45.))
            do = do_glb(latitude = (50.,70), longitude = (-70.,-45.))


        
        ### CALCULATE ANNUAL CYCLE SPACE-TIME RMS AND CORRELATIONS
        print '---- shapes ', dom,'   ', dm.shape,' ', do.shape
        rms_xyt = pcmdi_metrics.pcmdi.rms_xyt.compute(dm,do)
        cor_xyt = pcmdi_metrics.pcmdi.cor_xyt.compute(dm,do)
        
        ### CALCULATE ANNUAL MEANS
        do_am, dm_am =  pcmdi_metrics.pcmdi.annual_mean.compute(dm,do)
        
        ### CALCULATE ANNUAL MEAN BIAS
        bias_xy = pcmdi_metrics.pcmdi.bias.compute(dm_am,do_am)
        print var,'  ', 'annual mean bias is ' , bias_xy
        
        ### CALCULATE MEAN ABSOLUTE ERROR
        mae_xy = pcmdi_metrics.pcmdi.meanabs_xy.compute(dm_am,do_am)
        
        ### CALCULATE ANNUAL MEAN RMS
        rms_xy = pcmdi_metrics.pcmdi.rms_xy.compute(dm_am,do_am)
        
        # SET CONDITIONAL ON INPUT VARIABLE
        if var == 'pr':
            conv = 1.e5
        else:
            conv = 1.
            
        sig_digits = '.2f'
        if var in ['hus']: sig_digits = '.5f'
        
        for m in ['rms_xyt','rms_xy','bias_xy','cor_xyt','mae_xy']:
            if m == 'rms_xyt': metrics_dictionary[m + '_ann_' + dom] = format(rms_xyt*conv,sig_digits)
            if m == 'rms_xy': metrics_dictionary[m + '_ann_' + dom] =  format(rms_xy*conv,sig_digits)
            if m == 'bias_xy': metrics_dictionary[m + '_ann_' + dom] = format(bias_xy*conv,sig_digits)
            if m == 'mae_xy': metrics_dictionary[m + '_ann_' + dom] = format(mae_xy*conv,sig_digits)
            if m == 'cor_xyt': metrics_dictionary[m + '_ann_' + dom] = format(cor_xyt,'.2f')
        
        ### CALCULATE SEASONAL MEANS
        for sea in ['djf','mam','jja','son']:
            
            dm_sea = pcmdi_metrics.pcmdi.seasonal_mean.compute(dm,sea)
            do_sea = pcmdi_metrics.pcmdi.seasonal_mean.compute(do,sea)
            
            ### CALCULATE SEASONAL RMS AND CORRELATION
            rms_sea = pcmdi_metrics.pcmdi.rms_xy.compute(dm_sea,do_sea)
            cor_sea = pcmdi_metrics.pcmdi.cor_xy.compute(dm_sea,do_sea)
            mae_sea = pcmdi_metrics.pcmdi.meanabs_xy.compute(dm_sea,do_sea)
            bias_sea = pcmdi_metrics.pcmdi.bias.compute(dm_sea,do_sea)
            
            metrics_dictionary['bias_xy_' + sea + '_' + dom] = format(bias_sea*conv,sig_digits)
            metrics_dictionary['rms_xy_' + sea + '_' + dom] = format(rms_sea*conv,sig_digits)
            metrics_dictionary['cor_xy_' + sea + '_' + dom] = format(cor_sea,'.2f')
            metrics_dictionary['mae_xy_' + sea + '_' + dom] = format(mae_sea*conv,sig_digits)
            
    return metrics_dictionary
