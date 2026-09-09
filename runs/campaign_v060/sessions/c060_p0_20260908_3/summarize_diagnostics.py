"""Summarize completed diagnostics; never changes a gate or production file."""
from pathlib import Path
import csv
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SESSION = Path(__file__).resolve().parent
ROOT = SESSION.parents[3]
data = json.loads((SESSION/'seed-diagnosis.json').read_text())
assert data['status'] != 'running', 'Do not package an unfinished seed diagnostic as complete'
records = json.loads((SESSION/'diagnostic-execution.json').read_text())
assert any(r['name']=='baseline-C0' for r in records), 'Baseline bench unfinished'
rows=[]
for r, rec in data['prefixed_production'].items():
    for key,v in rec['observables'].items():
        rows.append({'r':int(r),'observable':key,'source':'EMULATED','stage':'pre-fix',
                     'bootstrap_se':v['two_sigma']/2,'predicted_se':v['expected_bootstrap_se'],
                     'ratio':v['ratio'],'pooled_variance':v['pooled_variance'],
                     'structural_zero':v['structural_zero_in_pooled_sample']})
with (SESSION/'variance_pre_fix.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
fig,axes=plt.subplots(1,2,figsize=(13,5))
for ax,r in zip(axes,(0,1)):
    rr=[x for x in rows if x['r']==r and x['ratio'] is not None]
    if str(r) not in data['prefixed_production']:
        ax.text(.5,.5,'No completed counts; see execution issues',
                ha='center',va='center',transform=ax.transAxes)
        ax.set_title(f'r={r}: INCOMPLETE, not zero variance')
        continue
    ax.barh([x['observable'] for x in rr],[x['ratio'] for x in rr])
    ax.axvline(.5,color='red',linestyle='--');ax.axvline(2,color='red',linestyle='--')
    ax.set_xlabel('Measured bootstrap SE / predicted SE')
    ax.set_title(f'Unchanged production twin, r={r} (EMULATED)')
fig.tight_layout();fig.savefig(SESSION/'variance_pre_fix.png',dpi=150);fig.savefig(SESSION/'variance_pre_fix.pdf');plt.close(fig)
labels=[];values=[]
for name,rec in data['paths'].items():
    labels.append(name);values.append(rec['shift_matches']/1023)
fig,ax=plt.subplots(figsize=(6,4));ax.bar(labels,values);ax.set_ylim(0,1.1)
ax.set_ylabel('Fraction of 1,023 shifted shots matching');ax.set_title('Raw seeds 500 / 501, 1,024 shots (EMULATED)')
fig.tight_layout();fig.savefig(SESSION/'seed_overlap.png',dpi=150);fig.savefig(SESSION/'seed_overlap.pdf');plt.close(fig)
# Fresh G3-derived diagnostic, independent of old conditioning records.
rel='runs/section8_v0.5.0_20260907T0628Z/circuits/trotter_scaling.json'
ref_bytes=subprocess.check_output(['git','show','723d083:'+rel],cwd=ROOT)
ref=json.loads(ref_bytes)
new=json.loads((SESSION/'diagnostic-trotter_scaling.json').read_text())
x=np.log(np.asarray(ref['r'],float));w=x-x.mean();den=float(w@w)
slopes=[]
for name in ('Psurv','E2','state'):
    a=np.asarray(ref['err_'+name]);b=np.asarray(new['err_'+name]);delta=b-a
    sr=float(np.polyfit(x,np.log(a),1)[0]);sn=float(np.polyfit(x,np.log(b),1)[0])
    bound=float(np.sum(np.abs(w)*np.abs(delta/a))/den)
    slopes.append({'observable':name,'refit_reference':sr,'refit_fresh':sn,
                   'delta_slope':sn-sr,'propagated_bound':bound,'bound_x10':10*bound,
                   'primary_max_delta':float(max(abs(delta))),
                   'primary_within_1e12':bool(max(abs(delta))<=1e-12),
                   'slope_within_bound':bool(abs(sn-sr)<=10*bound),
                   'slope_in_band':bool(-2.3<=sn<=-1.7)})
(SESSION/'diagnostic-slope-conditioning.json').write_text(json.dumps({'source':'fresh sandbox G3 output; not final repaired snapshot',
    'reference_commit':'723d083','reference_sha256':hashlib.sha256(ref_bytes).hexdigest(),
    'centered_log_r_sum_squares':den,'rows':slopes},indent=2)+'\n')
xml={}
for name in ('diagnostic-regression.xml','diagnostic-C0.xml'):
    tree=ET.parse(SESSION/name)
    xml[name]=[el.attrib for el in tree.iter('testsuite')]
manifest=json.loads((SESSION/'diagnostic-source-manifest.json').read_text())
changed=[p for p,h in manifest.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
summary={'processes':records,'junit':xml,'raw_shift':{n:r['shift_equal'] for n,r in data['paths'].items()},
         'pre_fix_distinct':{r:v['distinct'] for r,v in data['prefixed_production'].items()},
         'source_preservation':'all original legacy/campaign-test hashes unchanged',
         'source_file_count':len(manifest),'slopes':slopes,
         'status':'DIAGNOSTICS ONLY; production fix and physics sign-off deferred'}
(SESSION/'DIAGNOSTIC_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
