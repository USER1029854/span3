# DeFi exploit population profile — discovery-stage input

A reconstruction of the recent exploited-contract population on **BNB Chain, Ethereum, Arbitrum and Base**,
built to answer one question: *what characteristics could a discovery pipeline have keyed on, before the
hack, from on-chain and public data alone?*

**Source population:** SlowMist's hacked registry, pages 1–8 — 160 entries, 2026-04-04 → 2026-08-18. Every
entry was read and classified; none were sampled.

## Start here

| file | what it is |
|---|---|
| **[`REPORT.md`](REPORT.md)** | the synthesis — age / category / mechanism / wiring / flag distributions, the router-lane check, what discovery misses, the recommendation, and the study's limits |
| **[`DISCOVERY_PROMPT.md`](DISCOVERY_PROMPT.md)** | the operational output — a runnable discovery prompt encoding these patterns as on-chain predicates, with a scoring model, explicit anti-signals, and a table of empirically verified selectors and storage slots |
| [`PROFILES.md`](PROFILES.md) | 79 per-target forensic profiles, every field sourced, every gap named rather than filled |
| [`data/classification-table.md`](data/classification-table.md) | all 160 entries, kept vs discarded, one-line reason each |

## Headline

- **79 of 160 (49.4%)** of the noticed-exploit record is addressable by static contract analysis on the four
  target chains. The other half is keys, phishing, off-chain infrastructure, consensus bugs, or other chains.
- Dwell time (creation → exploit) is **bimodal and splits by chain**: BSC median **34 days**, Ethereum median
  **901 days**. 23% of targets were under a month old; 36% were over two years old; only 17% sat in between.
- The largest single flaw class is **price/valuation manipulation (29%)** — a contract acting on a valuation
  read from state an attacker could move in the same transaction.
- **9 targets held no money at all** — they held *authority*: standing approvals, mint rights, or
  arbitrary-call power. A balance-ranked discovery filter puts all of them at zero.

## Reproducing the data

Creation dates were pinned to blocks, not estimated. Ethereum and Arbitrum via Etherscan V2
`getcontractcreation`; **BNB Chain and Base are refused by Etherscan's free tier**, so BSC creation blocks
were recovered by bisecting `eth_getCode` against an archive node and reading the block timestamp and
receipts. See `REPORT.md` §1 for the full method and its limits.

```
scripts/chainlib.py      archive-RPC transport, creation-block bisection, explorer wrappers
scripts/flags.py         verification status, EIP-1967 / EIP-1167 proxy slots, owner(), codesize
scripts/txinfo.py        transaction / receipt inspector used to identify victim contracts
scripts/classify.py      the 160-entry keep/discard decision, with reasons
scripts/taxo.py          explicit per-id category, mechanism and discard-reason assignment
scripts/profile_data.py  per-target forensic fields (category, mechanism, wiring, lineage, flags)
scripts/primary.py       the single "this is the exploited contract" address per incident
scripts/gentable.py      renders data/classification-table.md
scripts/genprofiles.py   renders PROFILES.md
```

`chainlib.py` reads `ETHERSCAN_API_KEY` from the environment; no credentials are committed.

## Scope of the claim

This profiles the **numerator** — what got hit. It has no denominator, so it cannot tell you what fraction of
in-scope contracts are vulnerable, or any signal's false-positive rate. It is targeting guidance, not risk
scoring. SlowMist also lists only *noticed, attributed* hacks; `REPORT.md` §10 quantifies that undercount
against an independent PoC corpus and shows it is concentrated in exactly the sub-population this study finds
most numerous.
