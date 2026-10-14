"""Derived analysis of existing synthetic artifacts: weights of missed components."""
import json,glob,os,statistics as st
REPO=os.environ.get('REPO_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
D=REPO+'/results_pareto_validation_all/search_runs/'
EPS={10:'2.0',30:'3.5',50:'4.5'}
for m in ('v3f2_exact','v3f2_learned'):
    for d in (10,30,50):
        miss=[];hit=[]
        for f in glob.glob(f'{D}dim{d}_*.json'):
            r=json.load(open(f)); w=r['mixture']['weights']
            c=r['search_comparison']['evaluations'][m]['metrics_by_eps'][EPS[d]]['coverage']['per_true_min_distance']
            for wi,ci in zip(w,c): (miss if ci>float(EPS[d]) else hit).append(wi)
        print(m,d,'missed',len(miss),'of',len(miss)+len(hit),'median_w_missed',round(st.median(miss),4) if miss else None,
              'max_w_missed',round(max(miss),3) if miss else None,'median_w_hit',round(st.median(hit),4),
              'frac_missed_w<0.05',round(sum(x<0.05 for x in miss)/len(miss),2) if miss else None)
