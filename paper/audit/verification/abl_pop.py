from load_pub import *
import statistics as st
for series in ['publication_ablation','publication_population']:
    rows=load(series)
    print('=====',series,len(rows))
    meth=sorted(set(r['method'] for r in rows)); Ps=sorted(set(r['population_size'] for r in rows))
    print('methods',meth,'P',Ps,'models',sorted(set(r['model_seed'] for r in rows)),'seeds',sorted(set(r['search_seed'] for r in rows)))
    print('eval hash',set(r['evaluation_definition_hash'] for r in rows), 'def hash', set(r['definition_hash'] for r in rows))
    for P in Ps:
      for m in meth:
        R=[r for r in rows if r['population_size']==P and r['method']==m]
        if not R: continue
        f=lambda k: (st.mean([r[k] for r in R if r.get(k) is not None]) if any(r.get(k) is not None for r in R) else None)
        print(f"P{P:4d} {m:22s} n={len(R)} pix={f('pixel_knn_distance'):.4f} feat={f('feature_knn_distance'):.3f} psup={f('pixel_support_percentile'):.1f} fsup={f('feature_support_percentile'):.1f} cls={f('represented_class_count'):.2f} cand={f('candidate_count'):.1f} nfe={f('nfe'):.0f} conf={f('mean_confidence'):.3f}")
