# Discovery prompt — hunt for contracts shaped like the ones that actually got exploited

Derived from the 79-incident in-scope population profiled in [`REPORT.md`](REPORT.md).
Every rule below cites the evidence that produced it. Incident ids (`#n`) refer to
[`data/classification-table.md`](data/classification-table.md) and [`PROFILES.md`](PROFILES.md).

---

## 0. Mission

Find EVM contracts on **BNB Chain (56), Ethereum (1), Arbitrum (42161), Base (8453)** that hold or control
real value and run **bespoke fund-moving logic**, and rank them by how closely they match the shapes that
were actually exploited in the last four months. Emit ranked candidates with evidence for the triage stage.

You are not deciding whether a contract is vulnerable. You are deciding whether it is **worth a human or a
deep analyser looking at it**. Optimise for the ratio of real findings per candidate emitted, not for
candidate count.

**Hard scope rule:** only the four chains above. In the source population, 36 of 81 discarded incidents
(44%) were simply on other chains. Do not widen.

---

## 1. Run two lanes, not one. This is the most important instruction here.

Dwell time (creation → exploit) in the exploited population is **bimodal and splits by chain**:

| chain | n | median dwell | ≤30 days |
|---|---:|---:|---:|
| BSC | 24 | **34 days** | 11/24 (46%) |
| Ethereum | 30 | **901 days** | 3/30 (10%) |
| Arbitrum | 7 | 749 days | 0/7 |
| Base | 3 | 99 days | 1/3 |

23% of targets were under a month old; 36% were over two years old; only 17% sat in between. **A single
global age filter aimed at the 230-day median aims at the emptiest part of the distribution.** Run these as
two separate pipelines with different cadences, different universes and different scoring.

### Lane A — fresh deploys (primarily BSC, secondarily Base)

- **Universe:** the new-contract stream. Every contract creation, continuously.
- **Cadence:** continuous, or hourly at worst. Five targets in the population were exploited **within ~24
  hours of deployment** (#49 AIDC, #62 JB, #65 DIP, #79 DTXT, #81 BY); three more within 4 days (#91 AROS 3d,
  #99 SKP 3d, #2 FoxMarket 4d). A weekly sweep cannot see these — they do not exist long enough.
- **Age window:** 0–45 days, weight decaying after ~30.
- **What you are looking for:** custom tokens and bespoke reward/staking contracts wired to a brand-new AMM
  pair. 17 of the 19 custom-token incidents were BSC; that category alone is 24% of the whole population.
- **Do not require history.** These contracts have no transaction history, no TVL yet, and no age. Scoring
  that needs any of those will score them at zero. Judge them on **bytecode shape + wiring at deploy time**.

### Lane B — aged and funded (primarily Ethereum and Arbitrum)

- **Universe:** contracts ≥ 1 year old holding native or ERC-20 balance above a floor, **or** holding
  aggregate live allowances above a floor (see §3.3 — this second clause matters more than the first).
- **Cadence:** daily is fine. These targets sat exploitable for years.
- **Age window:** weight ≥ 2 years. 36% of the population; 11 targets over 4 years, including a **2018**
  contract still holding 65 ETH when it was emptied (#73 NovaBox) and two deprecated Aztec bridges holding
  2,067 ETH between them (#63, #67).
- **What you are looking for:** legacy/deprecated deployments that were never turned off — vaults, bridges,
  settlement proxies, reward pools, structured products.

### Age the implementation, not the proxy

For any proxied contract, compute age from the **current implementation's** creation, and carry the proxy's
age separately. #94 Joe Agent: proxy 34 days old, implementation **8 days** old. #39 BarnBridge: the
implementation that moved the money was installed **2 minutes 36 seconds** before the drain. A pipeline that
ages proxies by their own creation date systematically over-ages upgradeable targets.

---

## 2. Stage 1 — cheap disqualifiers, run first

Drop before spending anything expensive:

1. Not on chain 1 / 56 / 42161 / 8453.
2. Bytecode byte-identical to a canonical, widely-deployed contract with no live divergence (standard AMM
   pair, standard OZ ERC-20 with no overridden `_transfer`/`_update`, unmodified OZ ERC-4626). **Caution:**
   compute this on the *implementation* for clones and proxies, and treat "resembles a known base" as a
   reason to look at the **diff**, not a reason to drop — see §3.7.
3. Zero balance **and** zero aggregate live allowance **and** zero authority role. All three must be zero;
   any one being non-zero keeps it (§3.3).

**Do not disqualify on:** unverified source, low TVL, small headline value, or "the project looks
legitimate". Reasons in §5.

---

## 3. Stage 2 — the detectors

Each detector is an on-chain predicate. All selectors, slots and topics below were verified empirically
against live chain state; the constants table is in §7.

### 3.1 Thin-AMM-pair pricing — highest-yield single signal

**Predicate.** For every external address the contract reads in its value/pricing path, determine whether
that address is an AMM pool (responds to `getReserves()` / `slot0()`), then measure its depth. Flag when the
contract's own controlled value is **large relative to the depth of the pool it prices off**, and the pool
has no TWAP/observation window in the read path.

**Sub-signals that raise it further:**
- The pricing pool is itself young (created within the same window as the contract).
- The contract reads spot state **and then trades against that same pool in the same call path** (read →
  own swap → act on the *stale* read).
- Min-output parameters hardcoded to `0` anywhere in a swap or liquidity-removal path.

**Evidence.** Price/valuation manipulation is the largest flaw class in the population — **23 of 79, 29%**.
#13 LpdFi's `price()` read instantaneous reserves of a PancakeSwap pair that was **26 days old**, with no
TWAP, floor or deviation bound, and paid out against a 5,163× move; `claimInterest()` then removed
protocol-owned LP with router min-outputs set to zero. #2 FoxMarket read a spot quote, executed its own
large swap against that same pair, then used the stale quote. #8 Atomic valued LP and lending collateral off
a single Uniswap V3 pool. #135 Singularity priced through a pool that did not exist at all (§3.6).

### 3.2 Transfer hook that moves other people's money

**Predicate.** In the token's `_transfer` / `_update` / transfer-branch code path, look for:
- a write to, or transfer out of, the **AMM pair's** balance;
- a call to `sync()` (`0xfff6cae9`) or `skim(address)` (`0xbc25cf77`) on a pair;
- a swap initiated by the token contract itself, especially with `amountOutMin = 0`;
- a reward/dividend payout triggered by an ordinary transfer;
- add-liquidity / remove-liquidity *detection* logic based on comparing pair balances to reserves.

**Evidence.** This is the engine of Lane A. **14 of 79 incidents** manipulate an AMM pair's reserves through
the target's own logic, and in **12 of them the exploited contract is the token itself**
(#19, #49, #59, #62, #65, #80, #81, #91, #93, #133, #158, #160). #49 AIDC, #59 OLPC, #64 LBP, #81 BY,
#133 JUDAO and #160 TMM burn tokens directly out of the pair and re-`sync()`; #64 LBP does the mirror image,
minting reward tokens *into* the pair without updating reserves. #80 ATM auto-dumps 20%
of its own reserves at `amountOutMin = 0` on every sell. #79 DTXT and #93 YSDAO both use forgeable
add-liquidity detection to skip the fee path. #18 Pro Token pays a reward out of the pair on every transfer.

### 3.3 Authority without balance — rank on allowances, not TVL

**Predicate.** For each candidate, compute **aggregate live allowance granted *to* it**: scan `Approval`
logs (topic0 `0x8c5be1e5…`) where the spender is the candidate, then confirm current allowance and the
holders' current balances. Also detect held authority: mint/burn roles over a token, `owner()`/`admin()` of
another live contract, or Safe-module status.

Emit a candidate whose **balance is zero but whose allowance exposure is large**. Rank on
`max(own balance, allowance exposure)`.

**Evidence.** **9 of 79 incidents drained standing approvals rather than the contract's own funds** —
#10, #25, #39, #103, #117, #124, #125, #132, #157. TrustedVolumes' RFQ proxy (#124) held nothing and lost
**$5.87M**, because one resolver wallet had granted it an *unlimited* approval. Ekubo's extension (#125)
held nothing and lost $1.4M the same way. **A TVL-ranked discovery filter puts every one of these at zero.**

### 3.4 Proxy-slot drift — read the slots, not the events

**Predicate.** Snapshot EIP-1967 implementation / admin / beacon slots per candidate and diff on every run.
Alert on:
- a contract that **acquires non-zero EIP-1967 slots where it previously had none**;
- admin slot changing to an address with no prior history (fresh EOA);
- implementation changing to a contract created in the last N blocks.

**Do this by reading storage.** In #39 BarnBridge, `eth_getLogs` filtered on the proxy address returns
**zero logs** at the slot-write block, at the implementation-swap block, and at the drain block. No
`Upgraded`, no `AdminChanged`, nothing. Event-based proxy monitoring would have seen nothing at any point.

**Evidence and lead time.** #39: both EIP-1967 slots went from `0x0` to populated in the same block
(2026-07-06 08:13:35), with the admin slot set to the attacker's EOA — the address was not an EIP-1967 proxy
before that. The implementation was swapped **9 days 18 hours later**, 2m36s before the drain. The slot
acquisition is the actionable signal; the implementation swap is not reactable.

### 3.5 Callable initializer with a zero guard

**Predicate.** Bytecode contains an `initialize`-family selector (`initialize(address)` = `0xc4d66de8`,
plus other arities) **and** the OpenZeppelin `_initialized` guard slot reads zero, on a contract that is
already live and funded. For diamonds (EIP-2535), enumerate facet selectors and check each facet's
initializer independently — the diamond as a whole being "initialized" says nothing about a newly added facet.

**Evidence.** #117 Aurellion — an unverified EIP-2535 diamond on Arbitrum exposing `initialize(address)`
with the guard slot still 0, **live for 55 days**; the attacker called it, took ownership, `diamondCut`ed in
a `pullERC20` facet and swept standing approvals. (Verified: `0xc4d66de8` is present in that facet's
deployed bytecode.) #123 Renegade — unprotected initializer after a migration left the version counter
desynced, on a proxy holding 27 ERC-20s.

### 3.6 Incoherent stored configuration

**Predicate.** Read the deployed contract's live config and validate it against the domain, not against the
source. Concrete checks worth running on every candidate that has them:

- Uniswap V3 fee tier stored anywhere: must be one of `100 / 500 / 3000 / 10000`. If the contract calls
  `factory.getPool(a, b, fee)` (`0x1698ee82`), **call it yourself and assert the result is not
  `address(0)`.**
- Any oracle/feed address configured as `address(0)`, or resolving to an address with no code.
- `decimals()`-like parameters outside `0..77`, or absurd magnitudes.
- An `admin`/`signer` state variable set to `address(0)` **where an `ecrecover` result is compared against
  it** — that combination converts a malformed signature into a valid one.
- Ownership renounced (`owner() == 0`) **while** an `onlyOwner`-style check would admit `address(0)`.

**Evidence.** #135 Singularity registered fee tier **42**; `getPool()` silently returned `address(0)`, the
oracle valued all non-USDC reserves at zero, and this sat live and readable for **~3 months** before someone
minted 99.99% of the shares for a flash-loaned deposit. #59 OLPC's owner set `decimalsValue` to
`7326680472586200649` and then renounced ownership — live **46 days**. #92 MoneyMon's `changeadmin()` had
already set `admin = address(0)` on-chain, which is precisely what made `ecrecover` returning zero pass.
#96 ONTR's `onlyOwner` admitted `address(0)`, letting anyone re-own a renounced token.

These are **config-level defects with no code defect.** Source analysis will not find them. You must read
live state.

### 3.7 Fork lineage and clone-family membership

**Predicate.**
- Hash the implementation bytecode; group candidates by hash. One finding then covers the family.
- Detect ERC-1167 minimal proxies: runtime code containing `363d3d373d3d3d363d73` followed by the 20-byte
  target. Resolve the target and score the *family*, not each clone.
- Match against known bases (OZ, Uniswap, Compound, Maker MCD, Aragon, Colony, Set, Aave, Solady, LayerZero
  OFT, Axelar executables, DN404/BT404). When a base matches, **diff against it** and score the divergence,
  especially in the **pricing** and **authorisation** modules.

**Evidence.** #51 Lixir's two exploited vault tokens are both 45-byte ERC-1167 clones pointing at the *same*
implementation `0x2ce186c52cf150000bf8ad2b4679d4ad619395cd` — one flaw, a whole family exposed; #132 and
#135 are also clones. #30 42DAO is a MakerDAO MCD fork (`Spotter` / `Dog` / `GemJoin`) whose **divergence** —
a custom `Median Oracle` with no deviation, floor or drawdown checks — is exactly the bug. #71 Asterix is a
direct fork of Flooring (#76) and was hit with the identical DN404/BT404 flaw **one day later**.
Other lineages present: Set Protocol (#16), Aragon (#74), Colony (#116), Aztec Connect (#63, #67), BarnBridge
(#39), Thetanuts (#66, #141), Juicebox/REVLoans (#142), SubQuery (#154), ApeSwap (#82), Solady (#86).

### 3.8 Router / bridge / cross-chain executor — score on authority surface

**Predicate.** Flag contracts that are entry points rather than vaults:
- a permissionless external function that takes a **caller-supplied address, identity string, or calldata
  blob** and then acts on it as if it were authenticated;
- an arbitrary-call sink (`target.call(data)` with both attacker-controlled);
- message/proof verification with an incomplete bound — a length or index not checked against its limit, a
  field outside the hashed/proof-covered region, `abi.encodePacked` over two or more dynamic-bytes fields
  (collision), an unconstrained public witness;
- mint authority over a bridged asset;
- a contract *name* that collides with a well-known router/bridge but a deployer that does not match it.

**Evidence.** The router lane is **11 of 79 (14%)**, or 14 of 79 (18%) counting adjacent swap/settlement
executors, and it is disproportionate to how few such contracts exist. #101's Safe module inherits Axelar's
`expressExecuteWithToken` — anyone may call it, it performs no gateway validation, and the module then
parses `sourceAddress` **out of the caller's own payload** and compares that string to the expected router;
it had unlimited spend on 88 Safes. #134 ZetaChain's `GatewayEVM.execute` is an unrestricted arbitrary-call
sink. #106 hashes dynamic-bytes fields with `abi.encodePacked`. #151's MMR `VerifyProof()` never enforces
`leaf_index < leafCount`. #67's `numRealTxs` lives outside the proof-covered header. #63's escape-hatch
circuit publishes `proof_id` as an unconstrained public witness. **Two are name-collision traps** (#101,
#157). Note these skew **old and low-balance** — §3.3 and Lane B, not Lane A.

### 3.9 The subsidy shape (the one most likely to be missed)

**Predicate.** For every `claim` / `redeem` / `reward` / `withdraw` / `harvest`-family function, ask: **is
the eligibility predicate a function of state the caller can manufacture for free?** Specifically flag:
- eligibility that reads only `msg.sender`'s *current* balance, with no per-address claim ledger, no
  cooldown and no identity binding → farmable with fresh addresses;
- an amount sized from a **balance delta** with no check that anything was paid;
- an array of ids supplied by the caller, iterated **without a duplicate check**;
- state that gates the payout being written **after** the payout (checkpoint/effects ordering);
- a per-address cap enforced on `msg.sender` only, where the caller can deploy N contracts.

**Evidence.** 6 incidents — #18, #19, #73, #82, #100, #149 — and it falls between the buckets most triage
uses. `WUSD._englove` (#100) mints ~2 GLOVE to any address whose current GLOVE balance is below 2: no
ledger, no cooldown, so a fresh address **always** qualifies. `trackPurchase` (#24) sizes an ETH allocation
from a token-balance delta and never checks that ETH was paid. `redeem()` (#149) accepts the same NFT id 155
times because `nextRedeem` is advanced only after payout. #73 NovaBox adds new depositors to the dividend
list without initialising their checkpoints. #153 enforced one node per address — bypassed with proxy
contracts.

### 3.10 Signature verification, read in isolation

**Predicate.** Wherever `ecrecover` or a signature checker appears, verify:
- is the `address(0)` return rejected?
- is the recovered signer compared against a state variable that could be zero or attacker-set?
- does the signed digest cover **every** parameter that affects the transfer (recipient, token, amount,
  target/aggregator), or only a subset?
- is there a nonce / deadline / chain-id / position binding, or can the signature be replayed across
  positions or calls?
- is the authorisation looked up against the party **whose funds move**, or against a caller-supplied field?
- is the "signer source" itself caller-supplied?

**Evidence.** 6 incidents — #17, #51, #92, #103, #124, #138 — and most are decidable by reading the
verification function alone, with no protocol semantics: #92 (`ecrecover == admin` where admin had been set
to `address(0)`), #51 (dummy permit accepted as long as `ecrecover != 0`), #103 (attacker-supplied signer
source passed to `SignatureChecker`), #138 (digest covers only `keccak(SwapInfo.data)`, leaving
`aggregator`/`fromToken`/`toToken`/`amount` unsigned), #124 (authorisation keyed on the caller-controlled
**taker** rather than the maker whose funds move), #17 (a *signed* discount parameter with no floor, so a
leaked signer key becomes a ~100× discount). Related: #8 was a manager signature replayed across 21 Uniswap
V3 LP positions — no per-position binding.

### 3.11 Flash-loan reachability — a multiplier, never a finder

Compute whether the candidate's value-moving path is reachable in one hop from a flash-loan venue (Aave V3,
Morpho, Balancer, Moolah/Lista, Venus, PancakeSwap Vault, Uniswap V4 PoolManager). **Use this only to scale
the severity of an already-flagged finding.** 35% of exploits used one, but flash-loan availability is a
property of the chain, not of the target; on its own it predicts nothing.

---

## 4. Stage 3 — scoring

Starting calibration. **These weights are anchored to incident frequency, not to measured precision** — this
study has no denominator (§6). Tune them against your own confirmed-finding rate and treat the numbers below
as an initial ordering, not as truth.

| # | detector | weight | anchored to |
|---|---|---:|---|
| 3.1 | thin-AMM-pair pricing / valuation read from movable state | **10** | 23/79 incidents — largest flaw class |
| 3.2 | transfer hook that touches the pair (burn/`sync`/`skim`/self-swap) | **9** | 14/79 incidents; 12 are the token itself — the whole Lane A engine |
| 3.3 | large allowance exposure with little or no own balance | **8** | 9/79; invisible to TVL ranking |
| 3.9 | subsidy/claim eligibility manufacturable for free | **7** | 6/79, and least likely to be modelled already |
| 3.8 | permissionless entrypoint taking caller-supplied identity/calldata | **7** | 14/79 router lane |
| 3.10 | signature verification with a missing bound | **6** | 6/79 |
| 3.6 | stored config outside its valid domain | **6** | 4 incidents, all live for weeks–months, ~free to check |
| 3.5 | callable initializer + zero guard slot on a live funded contract | **6** | 2 incidents, very low false-positive rate |
| 3.4 | EIP-1967 slots acquired / admin → fresh EOA / impl → new contract | **8** | 9d18h lead time on #39; event-silent |
| 3.7 | fork divergence in the pricing or auth module | **5** | #30, #71, #76, #101 |
| 3.7 | clone-family membership (shared impl or ERC-1167 target) | **+3** | #51, #132, #135 — score the family once |
| — | prior public bug report or prior exploit on this contract/codebase, unresolved | **+8** | #134 (bounty dismissed as by-design), #27 (same flaw, same contract, re-hit 2 months later) |
| 3.11 | flash-loan reachable | **×1.3 multiplier** | 28/79, but not a predictor alone |

**Age modifier, applied per lane:**
- Lane A: `+4` if ≤ 7 days old, `+3` if ≤ 30, `+1` if ≤ 45.
- Lane B: `+4` if ≥ 4 years, `+3` if ≥ 2 years, `+1` if ≥ 1 year.
- Both lanes: `−2` in the 6-month-to-2-year band (only 17% of the population).
- Use the **implementation's** age for proxied contracts.

**Emit** anything scoring ≥ 12, or anything hitting a single weight-8-or-higher detector on a contract with
non-trivial value or allowance exposure.

---

## 5. Anti-signals — do not score on these

The population is explicit about what does **not** predict.

- **Verified source is not safety.** #118 SQ Protocol's hardcoded owner backdoor was in the **verified**
  source, Sourcify-verified **11 seconds after deployment**, and sat publicly readable for **102 days**.
  40 of 53 resolvable exploited contracts were verified. Verification means readable, nothing more. Use it
  as a *convenience* for analysis, not as a negative signal.
- **Unverified source is weak on its own.** 13 of 53 (24.5%) were unverified. Use it as a modifier on an
  already-flagged candidate, never as a primary detector.
- **TVL/size predicts nothing.** #43 Chi had a TVL of **~$883**; #105 Fractal ~$97K; #45 Summer.fi $6M;
  #124 TrustedVolumes $5.87M. Both tails are represented.
- **Headline loss is not knowable pre-hack and is unreliable post-hack.** #80's $243.5K "loss" is ~$89K
  attacker profit; #66's $2.1M was ~$105K net after a whitehat return; #151's $237K was later revised to
  $2.5M. Never train or threshold on it.
- **"Powerful admin exists" is near-useless alone.** 29 of 79 targets expose a live non-zero
  `owner()`/`getOwner()` — and 16 of the 81 *discarded* incidents were key compromises where the contract
  itself was fine. A powerful admin is what makes a key worth stealing; it is not what makes code buggy.
  Only score it in combination with custom fund-moving logic.
- **Flash-loan usage alone.** See §3.11.
- **"The project looks legitimate."** #16 Index Coop, #77 Ambient, #45 Summer.fi, #125 Ekubo, #142 Juicebox,
  #154 SubQuery, #116 ShapeShift and #134 ZetaChain are all in this population.

---

## 6. Standing watchlists (cheap, high-yield, run continuously)

1. **Codebase contagion.** When any protocol is exploited, immediately enumerate every other live contract
   sharing its implementation bytecode hash, its clone target, or its fork lineage, and re-score them at
   maximum priority. #71 Asterix was hit with the identical DN404/BT404 flaw **one day after** its parent
   #76 Flooring. #27 Verus is **the same contract exploited twice** — May, then again in July with the flaw
   still live. Both were catchable by a contagion watchlist and by nothing else in this document.
2. **Dismissed disclosures.** Track public bug-bounty reports and disclosures that were closed as
   "by-design" or "won't fix" on in-scope contracts. #134 ZetaChain's post-mortem states the arbitrary-call
   behaviour had been reported and dismissed as intended before the $334K exploit.
3. **Config drift.** Re-validate stored configuration (§3.6) on a schedule, not only at discovery. #59
   OLPC's absurd `decimalsValue` was set **46 days** after deployment, by the owner, who then renounced.
   Discovery at deploy time would have seen a clean contract.

---

## 7. Verified constants

All of these were checked against live chain state before being written down.

| thing | value | verification |
|---|---|---|
| EIP-1967 implementation slot | `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc` | read on #39, #67, #134 and 19 others |
| EIP-1967 admin slot | `0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103` | read on #39; returned the attacker EOA |
| EIP-1967 beacon slot | `0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50` | scanned across the population |
| ERC-1167 clone prefix | runtime `363d3d373d3d3d363d73` + 20-byte target + `5af43d82803e903d91602b57fd5bf3` | resolved 4 real clones (#51 ×2, #132, #135) |
| `owner()` | `0x8da5cb5b` | returned owners across 29 targets |
| `getOwner()` | `0x893d20e8` | returned owners on BSC targets |
| `admin()` | `0xf851a440` | returned on #39 |
| `initialize(address)` | `0xc4d66de8` | confirmed present in #117's facet bytecode |
| `totalSupply()` | `0x18160ddd` | eth_call on sDAI |
| `decimals()` | `0x313ce567` | eth_call on sDAI → 18 |
| `getReserves()` | `0x0902f1ac` | eth_call on a PancakeSwap V2 pair |
| `token0()` / `token1()` | `0x0dfe1681` / `0xd21220a7` | eth_call on the same pair |
| `sync()` | `0xfff6cae9` | eth_call executed on a pair |
| `skim(address)` | `0xbc25cf77` | eth_call executed on a pair |
| `slot0()` | `0x3850c7bd` | eth_call on a Uniswap V3 pool |
| `fee()` | `0xddca3f43` | eth_call on a Uniswap V3 pool → 500 |
| `liquidity()` | `0x1a686502` | eth_call on a Uniswap V3 pool |
| `getPool(address,address,uint24)` | `0x1698ee82` | UniV3 factory, WETH/USDC/3000 → `0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8` |
| valid UniV3 fee tiers | `100`, `500`, `3000`, `10000` | anything else ⇒ `getPool` returns `address(0)` (#135) |
| `totalAssets()` | `0x01e1d114` | eth_call on sDAI |
| `convertToAssets(uint256)` | `0x07a2d13a` | eth_call on sDAI |
| `asset()` | `0x38d52e0f` | eth_call on sDAI → DAI |
| `Transfer` topic0 | `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef` | most frequent topic in the #45 exploit receipt |
| `Approval` topic0 | `0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925` | same receipt |

**Data-access note.** Etherscan V2's free tier **refuses chain 56 and chain 8453**, BscScan's V1 API is
retired, and bscscan.com returns HTTP 403 to non-browser clients. Plan for BSC and Base creation dates,
source and verification status to come from archive-RPC bisection, Sourcify and Blockscout rather than
Etherscan. Budget for this — it is roughly half your target population.

---

## 8. Output per candidate

```
chain, address
implementation address + implementation age (and proxy age separately, if proxied)
clone/family id (implementation bytecode hash or ERC-1167 target), and family size
value at risk: own balance | aggregate live allowance exposure | authority held (roles, mint rights)
detectors fired: [3.1, 3.3, ...] with the concrete evidence for each
  - for 3.1: the pool address read, its depth, whether a TWAP was used
  - for 3.6: the stored value, the valid domain, and the call that proves it is broken
  - for 3.4: before/after slot values and the block+timestamp of the change
score, lane, age band
fork lineage / base match, and the specific diverged module if known
prior-scrutiny status: audits, bounty programme, prior exploits on this codebase
suggested triage focus: the mechanism class this shape usually resolves to
```

Always emit the **evidence**, not just the score. Triage should be able to confirm or dismiss without
re-deriving the reads.

---

## 9. What this prompt is and is not

This is built from the **numerator only** — 79 contracts that were exploited. There is no denominator, so
nothing here is a probability of compromise, and no weight below is a measured precision. A contract that
lights up every detector is a contract *shaped like* the ones that were exploited. That is the right thing
to point discovery at; it is not a risk score, and it must not be reported as one.

Two known biases to hold in mind:

- The source registry lists **noticed, attributed** hacks. An independent PoC corpus for the same window and
  chains contains at least **12 in-scope exploits absent from it** — all small, 9 of 12 on BSC. The
  undercount is concentrated in exactly Lane A, so **Lane A is under-weighted here, not over-weighted**.
- 15 of the 79 targets could not be resolved to an address at all, so their characteristics are absent from
  every distribution used to build these weights.

Re-derive the weights against your own confirmed findings once you have thirty or so. Until then, prefer
recall on the detectors with the lowest false-positive rates (§3.5, §3.6, §3.4) and precision on the ones
that will fire broadly (§3.1, §3.2).
