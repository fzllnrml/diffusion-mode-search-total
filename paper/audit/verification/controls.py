import json,glob,os,csv,statistics as st
import os as _os
REPO=_os.environ.get('REPO_ROOT', _os.path.abspath(_os.path.join(_os.path.dirname(__file__),'..','..','..')))

from load_pub import load
A=REPO+'/paper_results_archive'
def jobs(base):
    out=[]
    for d in sorted(glob.glob(base+'/model*_seed*/')):
        for m in ['ddim_105','low_noise_only','ddim_pool_representatives','inputs']:
            p=d+m+'/summary.json'
            if os.path.exists(p):
                s=json.load(open(p)); s['_dir']=d; s['_m']=m; s['_complete']=os.path.exists(d+m+'/complete.json'); out.append(s)
    return out
pil=jobs(A+'/mnist_controls'); conf=jobs(A+'/mnist_controls_confirmation/model43')+jobs(A+'/mnist_controls_confirmation/model44')
print('pilot jobs',len(pil),'conf jobs',len(conf), 'incomplete', sum(not x['_complete'] for x in pil+conf))

# build table rows: method -> (model,seed) -> summary
rows={}
for x in pil+conf:
    if x['_m']=='inputs':
        for b in x['baseline_rows']:
            rows[(b['method'],b['model_seed'],b['search_seed'])]=b
    else:
        rows[(x['method'],x['model_seed'],x['search_seed'])]=x
# consistency with publication_main
pub={(r['method'],r['model_seed'],r['search_seed']):r for r in load('publication_main') if r['population_size']==128}
bad=0
for (m,ms,ss),b in rows.items():
    if m in ('ddim','matched_ddim','rms_v3f2'):
        p=pub[(m,ms,ss)]
        for k1,k2 in [('pixel_knn_mean','pixel_knn_distance'),('feature_knn_mean','feature_knn_distance'),('pixel_support_percentile','pixel_support_percentile')]:
            if abs(b[k1]-p[k2])>1e-6: bad+=1; print('MISMATCH',m,ms,ss,k1,b[k1],p[k2])
        if b['initial_ddim_prefix_sha256']!=p['initial_ddim_prefix_sha256']: print('PREFIX MISMATCH',m,ms,ss)
print('pub consistency mismatches',bad)
meths=['ddim','matched_ddim','ddim_105','low_noise_only','ddim_pool_representatives','rms_v3f2']
K=['pixel_knn_mean','feature_knn_mean','pixel_support_percentile','feature_support_percentile','class_coverage','class_entropy','output_count','nfe']
def table(models,seeds,label):
    print('=====',label)
    for m in meths:
        R=[rows[(m,ms,ss)] for ms in models for ss in seeds]
        print(f"{m:26s} n={len(R)} "+' '.join(f"{k[:9]}={st.mean(r[k] for r in R):.4f}±{st.stdev([r[k] for r in R]):.4f}" for k in K))
    for m in meths[:-1]:
        for k,better in [('pixel_knn_mean',-1),('feature_knn_mean',-1),('pixel_support_percentile',1),('feature_support_percentile',1),('class_coverage',1),('class_entropy',1)]:
            d=[rows[('rms_v3f2',ms,ss)][k]-rows[(m,ms,ss)][k] for ms in models for ss in seeds]
            fav=sum((x*better)>0 for x in d)
            print(f"   rms - {m:26s} {k:28s} mean={st.mean(d):+.5f} min={min(d):+.5f} max={max(d):+.5f} favorable={fav}/{len(d)}")
table([42],[0,1,2],'PILOT m42 s0-2')
table([43,44],[0,1,2,3,4],'CONFIRMATION m43/44 s0-4')
for ms in (43,44): table([ms],[0,1,2,3,4],f'CONF model {ms}')
