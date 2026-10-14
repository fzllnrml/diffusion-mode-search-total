"""Development screen on model42 (alpha and consolidation radius); read-only."""
import json,glob,os,statistics as st
from collections import defaultdict
import yaml
REPO=os.environ.get('REPO_ROOT', os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
D=REPO+'/paper_results_archive/mnist_experiments/rms_screen/'
g=defaultdict(list)
for f in glob.glob(D+'*/resolved_config.yaml'):
    c=yaml.safe_load(open(f)); s=os.path.basename(os.path.dirname(f)); geo=c.get('geometry') or c.get('search') or {}
    for m in glob.glob(os.path.dirname(f)+'/*/summary.json'):
        x=json.load(open(m))
        key=(s.split('--')[0],x['method'],geo.get('alpha'),geo.get('merge',{}).get('radius') if s.startswith('rms_merge') else None,x['model_seed'],x['population_size'])
        g[key].append(x)
for k,v in sorted(g.items(),key=str):
    print(k,'n',len(v),'seeds',sorted(x['search_seed'] for x in v),'pix %.4f feat %.3f cand %.1f cls %.1f'%(
        st.mean(x['pixel_knn_mean'] for x in v),st.mean(x['feature_knn_mean'] for x in v),
        st.mean(x['candidate_count'] for x in v),st.mean(x['class_coverage'] for x in v)))
