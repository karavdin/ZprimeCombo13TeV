def histoFilt(hname):
    #if 'Zp' in hname:
        #return False
    #else:
    return True

def build_model(rootfile):
    model = build_model_from_rootfile(rootfile, histogram_filter=histoFilt, include_mc_uncertainties=True)
     
    model.fill_histogram_zerobins()
    model.set_signal_processes('Zp*')
    for p in model.processes:
        if p == 'qcd': continue
            #model.add_lognormal_uncertainty('qcdSF',0.20, p)
        #else:
        model.add_lognormal_uncertainty('lumi', 0.027, p)
        model.add_lognormal_uncertainty('topTagSF', 0.202, p)
    model.add_lognormal_uncertainty('xs_top', 0.15, 'ttbar')

    return model


# Code introduced by theta_driver

# Building the statistical model

#model = build_model('templates.root')
#model.scale_predictions(1.0/5.0)

#model.rebin("mtt", 5)

#model.rebin('btag0', 5)
#model.rebin('btag1', 5)
#model.rebin('btag2', 5)
#model.rebin('btag3', 5)
#model.rebin('btag4', 5)
#model.rebin('btag5', 5)

args = {}

model = build_model('templates_narrow_pT500_forTHETA.root')

model.scale_predictions(0.01,'Zprime2500') 
model.scale_predictions(0.001,'Zprime3000') 
model.scale_predictions(0.0001,'Zprime3500') 
model.scale_predictions(0.0001,'Zprime4000')

#model.restrict_to_observables(['btag3','btag4','btag0','btag1'])
#model.rebin('btag0', 5)
#model.rebin('btag1', 5)
#model.rebin('btag2', 5)
#model.rebin('btag3', 5)
#model.rebin('btag4', 5)
#model.rebin('btag5', 5)

for p in model.distribution.get_parameters():
    d = model.distribution.get_distribution(p)
    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])

#fixNuisanceDistribution = Distribution()
#for p in model.distribution.get_parameters():
    #fixNuisanceDistribution.set_distribution(p, 'gauss', mean = 0.0, width = 0.00001, range = [-0.000001, 0.000001])
    #print fixNuisanceDistribution.get_distribution(p)['width']
        
expected, observed = bayesian_limits(model, 'all', n_toy = 200, run_theta = True)
expected.write_txt("limits_2016_narrow_test.txt")
observed.write_txt("limits_obs_2016_narrow_test.txt")
model_summary(model, all_nominal_templates=True, shape_templates=True)
report.write_html('limits_2016_narrow_test')

options = Options()
options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '100')
parVals = mle(model, input='data', n=1, options = options)
#print "b-tag category: 5"

print "---------------------------------------------------"
print "Narrow Z'"
print "---------------------------------------------------"

print parVals
