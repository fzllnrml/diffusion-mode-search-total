import json,glob,statistics as st,math
import os as _os
REPO=_os.environ.get('REPO_ROOT', _os.path.abspath(_os.path.join(_os.path.dirname(__file__),'..','..','..')))

from collections import defaultdict
R=REPO+'/results_pareto_validation_all/search_runs/'
EPS={10:'3.5',30:'3.5',50:'4.5'}; EPS[10]='2.0'
runs=[json.load(open(f)) for f in sorted(glob.glob(R+'*.json'))]
print('runs',len(runs))
meths=['ddim_same_particles_raw','ddim_equal_nfe_raw','v3f2_learned','v3f2_exact']
for d in (10,30,50):
    rr=[r for r in runs if r['dim']==d]
    print('==== dim',d,'runs',len(rr),'mixtures',len(set((r['K'],r['dist_seed']) for r in rr)), 'eps',EPS[d])
    for m in meths:
        vals=defaultdict(list); model=defaultdict(lambda: defaultdict(list))
        for r in rr:
            ev=r['search_comparison']['evaluations'][m]; c=ev['metrics_by_eps'][EPS[d]]
            rec=c['coverage']['recall']; se=c['coverage']['soft_error']; nf=ev['n_found']
            vals['recall'].append(rec); vals['se'].append(se); vals['nf'].append(nf)
            vals['f1'].append(c['coverage']['f1']); vals['r11'].append(c['one_to_one']['recall'])
            key=(r['K'],r['dist_seed'])
            for k,v in [('recall',rec),('se',se),('nf',nf)]: model[k][key].append(v)
            if rec==1.0: vals['se_full'].append(se)
        mm=lambda k: [st.mean(v) for v in model[k].values()]
        print(f"{m:24s} recall {st.mean(vals['recall']):.3f} sd_run {st.stdev(vals['recall']):.3f} sd_model {st.stdev(mm('recall')):.3f} | SE {st.mean(vals['se']):.3f} sd_run {st.stdev(vals['se']):.3f} sd_model {st.stdev(mm('se')):.3f} | nf {st.mean(vals['nf']):.1f} sd_model {st.stdev(mm('nf')):.1f} | F1 {st.mean(vals['f1']):.3f} | full-cov runs {len(vals['se_full'])}/90 SE_full {st.mean(vals['se_full']) if vals['se_full'] else float('nan'):.4f}")
    costs=defaultdict(list)
    for r in rr:
        for k,v in r['search_comparison']['cost'].items():
            if isinstance(v,(int,float)): costs[k].append(v)
    print('   costs', {k:round(st.mean(v),1) for k,v in costs.items() if 'seconds' not in k})
    print('   params', set(json.dumps(r['search_comparison']['parameters'],sort_keys=True) for r in rr).__len__(), rr[0]['search_comparison']['parameters'])
