import csv,os,statistics as st
REPO=os.environ.get('REPO_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
A=REPO+'/paper_results_archive/'
for f,ph in [('mnist_controls/summary/stability_v2.csv','pilot m42 s0-2'),('mnist_controls_confirmation/summary/stability_v2.csv','confirmation m43/44 s0-4')]:
    r=list(csv.DictReader(open(A+f)))
    for m in ('stability_v2_rms','stability_v2_ddim'):
        for s in ('0.02','0.05'):
            R=[x for x in r if x['method']==m and x['scale']==s]; g=lambda k:[float(x[k]) for x in R]
            print(ph,m,s,'runs',len(R),'median_rho mean %.3f range [%.3f,%.3f]'%(st.mean(g('median_rho')),min(g('median_rho')),max(g('median_rho'))),
                  'min frac rho<1 %.4f'%min(g('fraction_rho_lt_1')),'drift mean %.4f range [%.4f,%.4f]'%(st.mean(g('median_reference_drift')),min(g('median_reference_drift')),max(g('median_reference_drift'))),'min valid',min(g('valid_fraction')))
for f in ['mnist_controls/summary/stability_v2_per_candidate.csv','mnist_controls_confirmation/summary/stability_v2_per_candidate.csv']:
    r=list(csv.DictReader(open(A+f)))
    for m in ('stability_v2_rms','stability_v2_ddim'):
        for s in ('0.02','0.05'):
            v=[float(x['delta0']) for x in r if x['method']==m and x['scale']==s]
            print(f.split('/')[0],m,s,'actual delta0 median %.4f min %.4f n %d'%(st.median(v),min(v),len(v)))
