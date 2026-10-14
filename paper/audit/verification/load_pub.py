import json,glob,os,sys
import os as _os
REPO=_os.environ.get('REPO_ROOT', _os.path.abspath(_os.path.join(_os.path.dirname(__file__),'..','..','..')))

from collections import defaultdict
ROOT=REPO+'/paper_results_archive/mnist_experiments'
def load(series):
    rows=[]
    for suite in sorted(glob.glob(f'{ROOT}/{series}/*/')):
        if not os.path.exists(suite+'complete.json'): print('INCOMPLETE',suite); continue
        meta=json.load(open(suite+'metadata.json'))
        for md in sorted(glob.glob(suite+'*/summary.json')):
            s=json.load(open(md)); s['_suite']=os.path.basename(suite.rstrip('/')); s['_complete']=os.path.exists(os.path.dirname(md)+'/complete.json')
            s['_git']=meta.get('git'); rows.append(s)
    return rows
