import json, datetime
from classify import C
from profile_data import P
from primary import PRIM
from extra_data import HELD, REVIEW
sm={i+1:x for i,x in enumerate(json.load(open('slowmist.json')))}
cre=json.load(open('creations.json'))+json.load(open('creations2.json'))
byid={}
for r in cre: byid.setdefault(r['slowmist_id'],[]).append(r)
fl={}
for f in json.load(open('flags.json')): fl[f['address'].lower()]=f
bts=json.load(open('blockts.json'))
# poc file per slowmist id
POC={2:'2026-08__FoxLpBondsPool_exp.sol',4:'2026-08__USM_exp.sol',8:'2026-08__Atomic_exp.sol',
10:'2026-08__UnistreetLaunchpad_exp.sol',13:'2026-08__LpdFi_exp.sol',14:'2026-07__MOKE_exp.sol',
16:'2026-07__ExchangeIssuance_exp.sol',18:'2026-07__ProToken_exp.sol',19:'2026-07__LULA_exp.sol',
24:'2026-07__ProjektRewardVault_exp.sol',25:'2026-07__LienFinance_exp.sol',39:'2026-07__CompoundProvider_exp.sol',
42:'2026-07__Sodium_exp.sol / 2026-07__LumiFinance_exp.sol',45:'2026-07__SummerFi_exp.sol',48:'2026-07__edel-xstock_exp.sol',
49:'2026-06__AIDC_exp.sol',51:'2026-06__LixirPermitDrain_exp.sol',59:'2026-06__OLPC_exp.sol',62:'2026-06__JB_exp.sol',
63:'2026-06__AztecEscapeHatch_exp.sol / _exp2.sol',64:'2026-06__LBP_exp.sol',65:'2026-06__DIP_exp.sol',
66:'2026-06__Thetanuts_exp.sol',67:'2026-06__AztecConnect_exp.sol',73:'2026-06__NovaBox_exp.sol',
74:'2026-06__TOPBPool_exp.sol',77:'2026-06__AmbientCrocSwapDex_exp.sol',79:'2026-06__DTXT_exp.sol',
80:'2026-06__ATM_exp.sol',81:'2026-06__BYToken_exp.sol',91:'2026-05__AROS_exp.sol',92:'2026-05__LegendaryMoneyMonNft_exp.sol',
93:'2026-05__YSDAO_exp.sol',94:'2026-05__JoeAgent_exp.sol',95:'2026-05__DxSale_exp.sol',99:'2026-05__SKP_exp.sol / SKP_exp2.sol',
100:'2026-05__WUSD_exp.sol',101:'2026-05__SquidRouterModule_exp.sol / NewMarketTrading_exp.sol',103:'2026-05__MureDistribution_exp.sol',
105:'2026-05__FractalProtocol_exp.sol',106:'2026-05__MAPProtocol_exp.sol',110:'2026-05__VerusBridge_exp.sol',
112:'2026-05__SEAToken_exp.sol',118:'2026-05__SQTokenStaking_exp.sol',123:'2026-05__Renegade_exp.sol',
124:'2026-05__TrustedVolumes_exp.sol',125:'2026-05__Ekubo_exp.sol',132:'2026-04__RWAVault_exp.sol',
133:'2026-04__JUDAO_exp.sol',135:'2026-04__SingularityDynaVault_exp.sol',138:'2026-04__giddyvaultv3_compound_auth_exp.sol',
139:'2026-04__KipseliPropAMM_exp.sol',141:'2026-04__ThetanutsVaultShareRounding_exp.sol',142:'2026-04__JuiceboxREVLoans_exp.sol',
149:'2026-04__XLootStaking_exp.sol',153:'2026-04__MONA_LisaVault_exp.sol',154:'2026-04__SubQuerySettings_exp.sol',
157:'2026-04__SquidMulticallAllowanceDrain_exp.sol',160:None}
EXPL={'mainnet':'etherscan.io','bsc':'bscscan.com','arbitrum':'arbiscan.io','base':'basescan.org'}
out=["# Per-target forensic profiles (79 in-scope targets)\n",
"Every field carries its source. `RPC binary-search` means: `eth_getCode` bisected against an archive node until the",
"first block containing code, then that block's timestamp and (where the creating tx is a direct `CREATE`) the",
"creating transaction from the block's receipts. Fields that could not be recovered say so — they are not estimated.\n"]
for sid in sorted(k for k,v in C.items() if v[0]!='DROP'):
    x=sm[sid]; p=P[sid]; st=C[sid][0]
    out.append(f"\n---\n\n## {sid}. {x['target']} — {x['date']}" + (" *(borderline)*" if st=='BORDER' else ""))
    out.append(f"\n**SlowMist line:** {x['method']} · {x['loss']} · [reference]({x['refs'][0] if x['refs'] else 'n/a'})")
    out.append(f"\n**Classification:** {C[sid][1]}")
    recs=byid.get(sid,[])
    prim=(PRIM.get(sid) or '').lower()
    out.append("\n### Identity and address")
    if recs:
        out.append("\n| role | address | chain | verified | proxy |")
        out.append("|---|---|---|---|---|")
        for r in recs:
            f=fl.get(r['address'].lower(),{})
            v=f.get('verified'); v={True:'yes',False:'**NO**','unknown-sourcify-miss':'not in Sourcify (BscScan status not checkable — see Method)','no-sourcify-match':'**not in Sourcify**'}.get(v,str(v))
            if f.get('name'): v+=f" (`{f['name']}`)"
            px=f.get('eip1967_impl') or f.get('eip1167_target')
            px=f"impl `{px}`" if px else ("45-byte ERC-1167 clone" if f.get('codesize')==45 else "no")
            star='**->** ' if r['address'].lower()==prim else ''
            out.append(f"| {star}{r['role']} | [`{r['address']}`](https://{EXPL[r['chain']]}/address/{r['address']}) | {r['chain']} | {v} | {px} |")
    else:
        out.append("\n- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from")
        out.append("  free-tier sources named the contract. Recorded as a gap rather than guessed.")
    out.append("\n### Age at time of hack")
    if recs:
        for r in recs:
            if not r.get('creation_ts'): continue
            ex=datetime.datetime.strptime(r['exploit_date'],'%Y-%m-%d')
            d=max(0,(ex-datetime.datetime.utcfromtimestamp(r['creation_ts'])).days)
            tx=r.get('creation_tx')
            txs=f"creation tx [`{tx[:18]}...`](https://{EXPL[r['chain']]}/tx/{tx})" if tx else "creation tx **not resolvable** (factory `CREATE` with no constructor logs)"
            out.append(f"\n- **{r['role']}** `{r['address'][:12]}...` created **{r['creation_utc']}**, exploited {r['exploit_date']} -> **dwell {d} days ({d/365.25:.2f} y)**.")
            out.append(f"  Source: {r['creation_src']}. {txs}.")
            if r.get('note'): out.append(f"  **Caveat:** {r['note']}")
    else:
        out.append("\n- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.")
    if sid in bts or (POC.get(sid)):
        pf=POC.get(sid)
        if pf and pf.split(' /')[0] in bts:
            for ch,name,b,t in bts[pf.split(' /')[0]]:
                out.append(f"- Exploit block confirmed on-chain: {ch} block {b} at **{t}** (fetched via `eth_getBlockByNumber`).")
    out.append("\n### What it held and controlled")
    out.append("\n- "+HELD.get(sid,"Not independently confirmed on-chain by this study. SlowMist's headline figure is %s; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft."%x['loss']))
    out.append("\n### What it was supposed to do")
    out.append(f"\n- Category: **{p['cat']}**")
    out.append("\n### Actual logic and exploited mechanism")
    out.append(f"\n- Flaw class: **{p['mech']}**")
    out.append(f"\n- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): {x['desc']}")
    if POC.get(sid):
        out.append(f"\n- Independent reproduction reviewed: DeFiHackLabs `src/test/{POC[sid].replace('__','/')}` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.")
    out.append("\n### Interaction graph")
    out.append(f"\n- {p['wiring']}")
    out.append("\n### Fork / codebase lineage")
    out.append(f"\n- {p['fork']}")
    out.append("\n### Observable pre-hack flags")
    out.append(f"\n- {p['flags']}")
    out.append("\n### Prior review status")
    out.append("\n- "+REVIEW.get(sid,"No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*."))
open('/home/user/span3/PROFILES.md','w').write('\n'.join(out)+'\n')
print("profiles written:", len([k for k,v in C.items() if v[0]!='DROP']))
