from load_pub import *
import statistics as st, csv
rows=load('publication_main')
print('rows',len(rows),'incomplete methods',sum(not r['_complete'] for r in rows))
# distinct combos
combo=defaultdict(set)
for r in rows: combo[(r['population_size'])].add((r['model_seed'],r['search_seed']))
for k,v in combo.items(): print('P',k,sorted(v))
mets=['pixel_knn_distance','feature_knn_distance','pixel_support_percentile','feature_support_percentile','represented_class_count','class_entropy','stability_return_rate','candidate_count','nfe','clipping_fraction_mean','fraction_unusually_close_train','train_test_gap_percentile','mean_confidence']
for P in (128,64):
  print('==== P',P)
  for m in ['ddim','matched_ddim','original_v3f2','rms_v3f2','rms_v3f2_merge','ddim_cluster','matched_cluster']:
    R=[r for r in rows if r['population_size']==P and r['method']==m]
    out=[]
    for k in mets:
        v=[r.get(k) for r in R if r.get(k) is not None]
        if v: out.append(f"{k}={st.mean(v):.5g}±{(st.stdev(v) if len(v)>1 else 0):.3g}(n{len(v)})")
    print(m, len(R)); print('   ','; '.join(out))
# per model means
print('==== per-model P128 pixel/feature rms vs matched')
for ms in (42,43,44):
  for m in ['matched_ddim','rms_v3f2']:
    R=[r for r in rows if r['population_size']==128 and r['method']==m and r['model_seed']==ms]
    print(ms,m,len(R),round(st.mean(r['pixel_knn_distance'] for r in R),4),round(st.mean(r['feature_knn_distance'] for r in R),4))
# paired signs
print('==== paired rms - matched, P128')
idx={(r['population_size'],r['model_seed'],r['search_seed'],r['method']):r for r in rows}
for k in ['pixel_knn_distance','feature_knn_distance','pixel_support_percentile','feature_support_percentile']:
    d=[idx[(128,ms,ss,'rms_v3f2')][k]-idx[(128,ms,ss,'matched_ddim')][k] for ms in (42,43,44) for ss in range(5)]
    print(k, 'mean',round(st.mean(d),5),'min',round(min(d),5),'max',round(max(d),5),'favorable', sum((x<0) if 'knn' in k else (x>0) for x in d),'/',len(d))
# NFE
for m in ['rms_v3f2','matched_ddim','original_v3f2','ddim']:
    print(m, sorted(set((r['nfe'],r.get('initialization_nfe'),r.get('movement_nfe'),r.get('matched_ddim_sample_count'),r['candidate_count']) for r in rows if r['population_size']==128 and r['method']==m)))
print('git', set(str(r['_git']) for r in rows))
