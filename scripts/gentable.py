import json
from classify import C
e=json.load(open('slowmist.json'))
lab={'KEEP':'KEEP','BORDER':'KEEP (borderline)','DROP':'discard'}
out=[]
out.append("# Classification of all 160 SlowMist entries (pages 1-8, 2026-04-04 to 2026-08-18)\n")
out.append("Scope kept: a bug in an EVM contract's own code, on BNB Chain / Ethereum / Arbitrum / Base, reached by an unprivileged attacker.\n")
out.append("Totals: **72 KEEP + 7 KEEP(borderline) = 79 in scope**, **81 discarded**.\n")
out.append("| # | Date | Target | Loss (SlowMist) | SlowMist method label | Verdict | Reason |")
out.append("|---:|---|---|---|---|---|---|")
for i,x in enumerate(e,1):
    st,why=C[i]
    t=x['target'].replace('|','/')[:46]
    out.append(f"| {i} | {x['date']} | {t} | {x['loss']} | {x['method']} | **{lab[st]}** | {why} |")
open('/home/user/span3/data/classification-table.md','w').write('\n'.join(out)+'\n')
print('rows',len(e))
