# Exploited-contract population profile — SlowMist pages 1–8

**Window:** 2026-04-04 → 2026-08-18 (137 days, 160 registry entries, every entry read)
**Scope:** EVM smart-contract logic vulnerabilities on BNB Chain, Ethereum, Arbitrum, Base
**Purpose:** derive what *discovery* should look for, from what actually got hit

---

## 0. The short version

Of 160 noticed, attributed hacks in the window, **79 (49.4%) are in scope** for a static-contract-analysis
discovery pipeline on the four target chains. The other 81 are keys, phishing, off-chain infrastructure,
consensus bugs, or other chains — invisible to contract analysis no matter how good it is.

The single most important finding is that **"the exploited population" is not one population.** Dwell time
(creation → exploit) splits cleanly by chain:

| chain | n (verified creation date) | median dwell | ≤30 days |
|---|---:|---:|---:|
| **BSC** | 24 | **34 days** | 11 / 24 (46%) |
| **Ethereum** | 30 | **901 days** | 3 / 30 (10%) |
| Arbitrum | 7 | 749 days | 0 / 7 |
| Base | 3 | 99 days | 1 / 3 |

An age filter tuned to either hump misses the other one entirely. A discovery net weighted to "old and
unattended" would have missed 23% of the population outright — including five contracts that were **less
than 24 hours old** when they were drained. A net weighted to "fresh deploys" would have missed the eleven
4-plus-year-old Ethereum contracts that were still holding real money, including a 2018 contract with 65 ETH
in it and two deprecated Aztec bridges holding 2,067 ETH between them.

Everything below is evidenced per-target in [`PROFILES.md`](PROFILES.md), with the filtering decision for
every one of the 160 entries in [`data/classification-table.md`](data/classification-table.md).

---

## 1. Method, and what it cost

### Sources, in the order they were trusted

1. **SlowMist registry** (`hacked.slowmist.io/?c=&page=1..8`) — server-rendered HTML, parsed to
   [`data/slowmist-entries.json`](data/slowmist-entries.json). Used **only** to define the population and as
   a starting pointer. Never used as the finding.
2. **Block explorers and archive RPCs** — every creation date in this report is a block timestamp I fetched,
   not a listing or verification date. See below.
3. **Independent exploit reproductions** — DeFiHackLabs publishes runnable Foundry PoCs with exploit tx
   hashes, victim addresses, fork blocks and trace-verified root causes. 89 PoCs covering this window were
   downloaded and read; 56 of the 79 in-scope incidents have one. These are treated as a strong secondary
   source whose *addresses and blocks I then verified myself* against chain state.
4. **Post-mortems and security write-ups** (Verichains, BlockSec, DarkNavy, project blogs) for the
   incidents with no PoC.

### How creation dates were actually pinned

This is the field the brief said not to fake, so here is exactly how each one was obtained.

- **Ethereum and Arbitrum:** Etherscan V2 `getcontractcreation`, which returns the creating transaction hash,
  creator, block number and timestamp directly.
- **BNB Chain and Base:** *Etherscan V2's free tier refuses these chains* — `chainid=56` and `chainid=8453`
  return `"Free API access is not supported for this chain"`. BscScan's V1 endpoint is retired
  (`"You are using a deprecated V1 endpoint"`), bscscan.com returns HTTP 403 to non-browser clients, and
  there is no Blockscout instance for BSC. So for BSC I **bisected `eth_getCode` against an archive node**
  (`bsc-mainnet.public.blastapi.io`, confirmed archive-capable by reading WBNB's code at block 0x2000000 and
  its absence at 0x20000), found the first block containing code, read that block's timestamp, and then
  scanned the block's receipts for the transaction whose `contractAddress` matches — which recovers the
  actual creation tx hash for direct `CREATE`s. Where the contract was made by a factory with no constructor
  logs, the profile says `creation tx not resolvable` and gives the block instead. Base creation data came
  from Blockscout, cross-checked the same way.
- **Cross-checks:** outlier dates were verified against a second source. NovaBox's implausible-looking
  2018-10-11 creation is confirmed by Etherscan and Blockscout returning the *same* creation tx
  (`0x53b96d58...`). Arbitrum binary-search results were checked against Blockscout's
  `creation_transaction_hash`.

**Result: 64 of 79 in-scope incidents have a creation date pinned to a block. 15 do not** — because the
exploited contract address itself could not be recovered from free-tier public sources. Those 15 are listed
in §8 and are excluded from every dwell statistic rather than estimated.

### What I verified with my own hands, beyond dates

Four drains were confirmed independently by reading balances at the exploit block and the block after
(`eth_getBalance`), not taken from any write-up:

| contract | pre-exploit | post-exploit | delta |
|---|---:|---:|---:|
| Projekt reward vault `0x574fc478…` | 400.6514 ETH | 98.9576 ETH | −301.69 ETH |
| NovaBox pool `0xbc419116…` | 65.1130 ETH | 0.0904 ETH | −65.02 ETH (99.86%) |
| Aztec Connect V3 `0xFF1F2B4A…` | 908.9873 ETH | 0.0000 ETH | −908.99 ETH |
| Aztec RollupProcessorV2 `0x737901be…` | 1,158.7598 ETH | 0.7598 ETH | −1,158 ETH |

And one incident was reconstructed entirely from storage reads — see BarnBridge in §6, which turned out to
have a 9-day observable window that no write-up mentions.

---

## 2. The filter, and why the discard list matters

Full table: [`data/classification-table.md`](data/classification-table.md) — all 160 rows, each with a
one-line reason.

| verdict | count | share |
|---|---:|---:|
| KEEP — in-scope EVM contract logic vuln | 72 | 45.0% |
| KEEP (borderline) — flagged, see below | 7 | 4.4% |
| **total addressable by contract analysis** | **79** | **49.4%** |
| discard | 81 | 50.6% |

Discard reasons, grouped:

| reason | count | share of discards |
|---|---:|---:|
| Non-target chain (Solana, Sui, Cosmos, NEAR, TRON, Polygon, Starknet, Linea, Avalanche, Gnosis, Monad, Hedera, Supra, Algorand, Cardano, HyperEVM/MegaETH…) | 36 | 44.4% |
| Private-key / signer-key / multisig / hot-wallet compromise | 16 | 19.8% |
| Frontend / DNS / supply-chain / dependency / firmware | 9 | 11.1% |
| Off-chain infrastructure (relayer, solver DB, backend, RPC node, bot logic) | 8 | 9.9% |
| Social engineering / account takeover / phishing | 5 | 6.2% |
| Exchange or payment-processor breach, cause undisclosed | 4 | 4.9% |
| Consensus / node / TSS / proof-system level | 3 | 3.7% |

*(Explicit per-id assignment in [`scripts/taxo.py`](scripts/taxo.py); every one of the 81 is assigned exactly once.)*

**The 50/50 split is itself a discovery-strategy input.** Half of the noticed-exploit record is structurally
out of reach of any static contract analyser. That bounds the ceiling on what discovery can contribute and
argues that discovery quality matters more than discovery volume — you are competing for the *other* half.

Note also the composition of the discarded half: 16 key compromises and 8 off-chain-infrastructure
incidents (24 combined, 30% of discards) are cases where the contract was *fine*. A pipeline that scores on
"powerful admin exists" will light up on many of these targets without that signal predicting anything —
the admin key being powerful is what made the compromise valuable, not what made the contract buggy.

### The 7 borderline keeps, and the reasoning

| # | target | why borderline | kept because |
|---|---|---|---|
| 17 | Swan Treasury | signer key leaked off-chain | but `ZhaiquanBuy.buy()` applies a signed discount with **no floor or bounds check** — a discount of 1 yields ~100× off. The contract-side defect is real and statically visible; the key only supplied the signature. |
| 40 | Cascade | mark-price manipulation, economic not "buggy" | on-chain pricing logic in a thin pre-launch market; same shape as spot-price-read-then-act |
| 74 | Token of Power | governance capture, attacker bought voting power | the *config* is the flaw and it is fully on-chain readable: 16,384 total supply, no timelock, propose+vote+execute in one transaction |
| 95 | DxSale | the actor **held ownership** — not unprivileged | the flaw is in the contract's own code (an undisclosed `DXLOCKERLP` owner-only drain defeating the advertised per-user timelocks), and the pre-hack signal — unverified bytecode containing an undocumented selector — is exactly what discovery can see. **Excluded from the "unprivileged-reachable" sub-population.** |
| 99 | SKP | insider-engineered exit scam | the whitelisted beneficiary was set by the owner 6 days before the drain; DeFiHackLabs explicitly disputes SlowMist's "smart contract vulnerability" framing. Kept for the pattern, **excluded from the unprivileged sub-population**. |
| 153 | MONA | stage 1 was the deployer redeeming their own LP | stage 2 (referral self-dealing via proxy contracts defeating a 1-node-per-address limit) is genuine unprivileged contract-logic abuse |
| 157 | Squid Multicall | contract has no bug — it is permissionless *by design*; a user mis-approved it | kept because a permissionless arbitrary-call executor that users can grant allowances to is precisely the router-lane fingerprint being tested here |

Three of these seven (95, 99, 153) involve a privileged or insider actor. **The unprivileged-reachable
sub-population is therefore 76 of 160 (47.5%).** Where a statistic below depends on the attacker being
unprivileged, it says so.

---

## 3. Age distribution — the headline

Dwell = creation of the *primary exploited contract* → exploit date. n = 64 with a verified creation block.

```
<= 1 week      11  (17.2%)  ##################
1-4 weeks       4  ( 6.2%)  ######
1-3 months      8  (12.5%)  #############
3-6 months      7  (10.9%)  ###########
6-12 months     4  ( 6.2%)  ######
1-2 years       7  (10.9%)  ###########
2-4 years      12  (18.8%)  ###################
4+ years       11  (17.2%)  ##################
```

min 0 d · p25 34 d · **median 230 d** · p75 1,092 d · max 2,797 d · mean 606 d

One note on counting: #27 and #110 are the **same Verus bridge contract exploited twice** (May, then July
with the flaw still live), so that contract contributes two rows — 957 d and 1,023 d. They are two distinct
exploitation events, which is what this population is measuring, but the contract is double-counted in the
totals. No bucket assignment changes if it is collapsed to one.

**The median is a lie.** This is a bimodal distribution with a trough in the middle: 23.4% of targets were
under a month old, 36.0% were over two years old, and only 17.2% sat in the 6-month-to-2-year band where the
median falls. Reporting "target contracts around 230 days old" would aim discovery straight at the emptiest
part of the distribution.

The two humps are two different phenomena, and they separate almost perfectly by chain:

**Hump A — BSC, freshly deployed, median 34 days.** These are custom tokens and bespoke reward/staking
contracts with a hand-rolled `_transfer` hook, deployed, seeded with a PancakeSwap pair, drained, abandoned.
Five were exploited **the day after deployment** (#49 AIDC, #62 JB, #65 DIP, #79 DTXT, #81 BY — each ~1 day).
Three more inside 4 days (#2 FoxMarket at 4d, #91 AROS at 3d, #99 SKP at 3d). For this hump, *any* discovery
cadence slower than daily is structurally too slow: the contract does not exist long enough to be found by a
weekly sweep.

**Hump B — Ethereum, long-lived, median 901 days (2.5 years).** These are protocols that were built,
funded, and then left running: USM (4.83 y), Index Coop ExchangeIssuance (5.35 y), Projekt reward vault
(5.03 y), Drips `DaiDripsHub` (4.58 y), Lixir vault tokens (4.93 y), Aztec RollupProcessorV2 (5.29 y),
Aztec Connect V3 (4.02 y), Thetanuts legacy vault (4.13 y), DxSale locker (5.26 y), Token of Power's Aragon
voting proxy (5.25 y, on a 2019 implementation), and NovaBox (**7.66 years** — created 2018-10-11, still
holding 65.11 ETH when it was emptied in June 2026).

**Outliers worth naming individually:**

- **#138 GiddyVaultV3 — 2 days.** An Ethereum vault, not a BSC token. Signature-scheme flaw
  (EIP-712 covering only `keccak(SwapInfo.data)`, leaving `aggregator`/`fromToken`/`toToken`/`amount`
  unsigned), $1.3M. Fresh deployment on mainnet is not a BSC-only phenomenon.
- **#10 Unistreets — 3 days.** Ethereum launchpad factory custodying every launch's Uniswap V4 LP NFT,
  3 days old, drained via calldata injection.
- **#39 BarnBridge — 8 days**, but see §6: that 8 days is the *attacker's* proxy, not the protocol's. The
  underlying protocol is from 2020. Dwell measured on "the contract that moved the money" can mislead when
  the attacker installs the money-moving contract themselves.
- **#94 Joe Agent — proxy 34 days old, implementation 8 days old.** For upgradeable contracts, the
  implementation's age is the one that matters, and it is often far younger than the proxy. Discovery that
  ages a proxy by its own creation date will systematically over-age upgradeable targets.

**Verdict on the "old and unattended" premise: it is half right, and dangerously so.** It is a good
description of the Ethereum/Arbitrum sub-population and a bad description of BSC. Weight age by chain, or
don't weight it at all.

---

## 4. Category distribution

All 79 in-scope incidents (including the 15 without a resolved address, categorised from the write-ups).
Each id is assigned to exactly one category, explicitly, in [`scripts/taxo.py`](scripts/taxo.py).

| category | n | share | chain split |
|---|---:|---:|---|
| **custom token with a fund-moving transfer/reward hook** | **19** | **24.1%** | bsc 17, unresolved 2 |
| staking / reward / bond / distribution pool | 13 | 16.5% | bsc 5, mainnet 4, base 1, unresolved 3 |
| vault (ERC-4626 / yield / options) | 11 | 13.9% | mainnet 6, arbitrum 2, base 1, unresolved 2 |
| bridge / router / cross-chain executor | 11 | 13.9% | mainnet 6, base 2, bsc 1, unresolved 2 |
| lending / borrowing market | 5 | 6.3% | mainnet 3, arbitrum 1, unresolved 1 |
| stablecoin / CDP | 4 | 5.1% | mainnet 2, unresolved 2 |
| DEX / AMM / hook / extension | 3 | 3.8% | mainnet 2, arbitrum 1 |
| index / structured product | 2 | 2.5% | mainnet 1, unresolved 1 |
| governance / DAO treasury | 2 | 2.5% | mainnet 1, arbitrum 1 |
| launchpad / LP locker | 2 | 2.5% | mainnet 1, bsc 1 |
| NFT liquidity (DN404/BT404) | 2 | 2.5% | unresolved 2 |
| privacy pool / dark pool | 1 | 1.3% | mainnet 1 |
| smart account (ERC-4337) | 1 | 1.3% | arbitrum 1 |
| streaming payments | 1 | 1.3% | mainnet 1 |
| market-maker RFQ settlement proxy | 1 | 1.3% | mainnet 1 |
| bespoke protocol diamond (EIP-2535) | 1 | 1.3% | arbitrum 1 |

**Where the catchable volume actually is: the top four categories are 54 of 79 — 68.4% of the population.**
And they split hard by chain. **17 of the 19 custom-token incidents are on BSC** (the other 2 have
unresolved addresses and are almost certainly BSC or Ethereum). The vault, bridge, index and
market-maker categories are overwhelmingly Ethereum and Arbitrum. There is essentially no overlap: the
BSC net and the Ethereum net are hunting different animals.

Two things this table understates:

- **"Custom token" undersells the shape.** These are not ERC-20s. They are tokens whose `_transfer`/`_update`
  override *moves other people's money*: burning from the AMM pair's balance and calling `sync()` (#49, #59,
  #64, #81, #133, #153, #160), auto-swapping the contract's own reserves at `amountOutMin = 0` (#80), paying
  a reward out of the pair on every transfer (#18), or misclassifying a sell as a liquidity add to skip the
  fee path (#79, #93). *Bespoke fund-moving logic that happens to be packaged as a token* is the single
  largest catchable category in the record.
- **Vaults are mostly ERC-4626 with one override.** #132 (withdraw override omitting the allowance spend),
  #141 (first-depositor rounding on a vault that already held WBTC), #105 (fixed daily price + re-entrant
  deposit/withdraw), #135 (broken oracle wiring), #45 (live NAV with no manipulation guard). The base
  standard is fine; the divergence is the bug.

---

## 5. Mechanism distribution

Each id assigned to exactly one class, explicitly, in [`scripts/taxo.py`](scripts/taxo.py).

| flaw class | n | share |
|---|---:|---:|
| **price / valuation manipulation** (spot-read-then-act, live NAV, ERC-4626 donation, reserve/burn manipulation) | **23** | **29.1%** |
| missing or broken access control | 9 | 11.4% |
| proof / message-verification / hash-collision flaw | 7 | 8.9% |
| arithmetic — rounding, unsafe cast, decimals, share math | 7 | 8.9% |
| uncapped subsidy / reward accounting (Sybil-farmable, duplicate IDs, uninitialised checkpoints) | 6 | 7.6% |
| signature-validation bypass | 6 | 7.6% |
| trusts caller-supplied accounting / routing context | 4 | 5.1% |
| hardcoded backdoor / privileged escape hatch | 2 | 2.5% |
| governance capture (no timelock / abandoned DAO) | 2 | 2.5% |
| re-initializable proxy / uninitialised facet | 2 | 2.5% |
| NFT/token standard state-desync (DN404/BT404 packed ownership) | 2 | 2.5% |
| mechanism not publicly detailed (2 of the 15 unresolved targets) | 2 | 2.5% |
| reentrancy / CEI violation | 1 | 1.3% |
| arbitrary call / calldata forwarding | 1 | 1.3% |
| storage-slot collision with a library fixed slot | 1 | 1.3% |
| ERC-4337 validation-phase side effect | 1 | 1.3% |
| TOCTOU / missing state lock | 1 | 1.3% |
| permissionless registration + crafted payoff parameters | 1 | 1.3% |
| accounting flaw across internal call paths / proxy sidecars | 1 | 1.3% |

The top five classes are **52 of 79 — 65.8%** of the population, and every one of them maps onto a shape a
normal triage pipeline already looks for. Note that the single largest class is nearly a third of the record
on its own: **almost one in three in-scope exploits was a contract acting on a valuation it read from state
an attacker could move in the same transaction.** Three observations that do **not** map cleanly:

1. **"Uncapped subsidy / reward accounting" (7.6%) is under-modelled.** These are not access-control bugs
   and not price bugs. `WUSD._englove` (#100) mints ~2 GLOVE to any address whose current GLOVE balance is
   below 2 — no per-address ledger, no cooldown, no identity binding, so a fresh address always qualifies.
   `trackPurchase` (#24) sizes an ETH allocation from a token-balance *delta* and never checks that ETH was
   paid. `redeem()` (#149) accepts the same NFT ID 155 times because it advances `nextRedeem` only after
   payout. These are all "the reward function's eligibility predicate is not a function of anything the
   attacker can't manufacture." That is a recognisable and searchable shape, it accounts for 6 incidents
   (#18, #19, #73, #82, #100, #149) and it sits in a blind spot between the auth bucket and the pricing bucket that triage usually splits
   findings into.

2. **Signature-validation bypasses (7.6%) recur in a specific, cheap-to-detect form.** #92 `verify()`
   compares `ecrecover(...) == admin` where `admin` had been set to `address(0)`; #51 accepts a dummy permit
   as long as `ecrecover` returns non-zero; #103 hands `SignatureChecker` an attacker-supplied signer source;
   #138 signs only part of the struct; #124 recovers the signer then checks authorisation against the
   **taker** rather than the maker. Four of these five are decidable by reading the verification function in
   isolation — no protocol semantics required.

3. **Hardcoded backdoors and owner-set traps (#95, #99, #118).** #118 is the sharpest: SQ Protocol's backdoor was in the
   **verified** source, Sourcify-verified 11 seconds after deployment, and sat publicly readable for 102 days.
   "Verified source" is not a safety signal in this population — it is just readability.

---

## 6. Wiring signatures

Are these targets recognisable by what they touch? Largely yes.

Counting rule, stated so it can be checked: a feature is counted when the target's recorded interaction
graph in [`scripts/profile_data.py`](scripts/profile_data.py) names it. The approval-drain list is
enumerated by hand.

| wiring feature | incidents | share |
|---|---:|---:|
| an AMM pair/pool appears in the interaction graph | 50 | 63% |
| **the flaw itself was a valuation read from external state** (§5 top class) | 23 | 29% |
| a flash-loan venue appears in the interaction graph | 28 | 35% |
| the money drained was **standing approvals**, not the contract's own balance | 9 | 11% |

**The strongest single fingerprint: a bespoke contract that reads spot state from one thin AMM pair.**
#13 LpdFi's `Lpd.price()` reads instantaneous reserves of the PancakeSwap LPD/USDC pair
`0x85346d31…` — no TWAP, no liquidity floor, no deviation bound — and the pair was **26 days old** when
the protocol paid out against a 5,163× price move. #2 FoxMarket reads a Pancake spot quote, then executes
its own large swap against that same pair, then uses the *stale* quote. #8 Atomic values LP and lending
collateral off a single Uniswap V3 ARB/USDC.e pool. #43 Chi redeems full-value collateral at a hardcoded
$1 while the USC pool it buys from is thin and depegged. This is directly detectable: *for each external
address the contract reads, is it an AMM pair, and what is its reserve depth?*

**Second fingerprint: contracts that hold no money but hold authority.** Nine incidents drained
*other people's approvals* (#10, #25, #39, #103, #117, #124, #125, #132, #157). These contracts look
worthless to a TVL-based discovery filter — TrustedVolumes' RFQ proxy held nothing and lost $5.87M, because
a resolver wallet had granted it an **unlimited** standing approval. Ekubo's extension held nothing and lost
$1.4M the same way. A discovery pipeline that ranks by contract balance will rank these at zero. **The
correct measure for this class is not balance — it is the sum of live allowances granted to the address.**
That is queryable from `Approval` event logs.

**Third fingerprint: flash-loan composability.** 35% of exploits pulled from Aave V3, Morpho, Balancer,
Moolah/Lista, Venus, PancakeSwap Vault or Uniswap V4 PoolManager. Flash loans were almost never the
vulnerability — the USM PoC is explicit that the oracle reads were identical throughout and the loan only
supplied working capital. But *reachability from a flash-loan source* is what turns a small pricing defect
into a drainable one, and it is a static property of the wiring.

### The BarnBridge storage trace — a wiring signal nobody wrote up

SlowMist calls #39 a "Governance Attack"; the independent PoC calls it "missing access control on
`_takeUnderlying`". Both are right, and reading the proxy's storage slots directly reconciles them and
surfaces a detection window:

| what | when | value |
|---|---|---|
| EIP-1967 impl **and** admin slots | ≤ block 25472221 | **both `0x0000…0000`** — the address was not an EIP-1967 proxy at all |
| both slots written, same block | **block 25472222 — 2026-07-06 08:13:35** | impl → `0x41ab25709e0c3edf027f6099963fe9ad3ebab3a3`; admin → `0xf908610e9174c7cd6e9dfd371e238be4511297a1` — **the attacker EOA** |
| implementation swapped | **block 25535107 — 2026-07-15 02:37:11** | → `0x769a9fa1e2414db14b35c46e4095d6e8f1694565` |
| drain transaction | block 25535120 — 2026-07-15 02:39:47 | −774,943.38 USDC from ~50 approving wallets |
| **events emitted by the proxy address at any of those blocks** | — | **zero** (`eth_getLogs` filtered on the address returns nothing at all three blocks) |

*(binary-searched `eth_getStorageAt` on both slots against an Ethereum archive node, then `eth_getLogs` on the address at each block)*

Two things fall out of this that the write-ups do not say. First, the attacker did not merely change an
existing admin — the contract **acquired non-zero EIP-1967 slots where it previously had none**, because
BarnBridge's SMART Yield providers use their own proxy/registry pattern rather than EIP-1967. "A live,
funded contract suddenly starts presenting EIP-1967 slots" is a far more specific and unusual event than
"admin changed", and it happened **9 days and 18 hours** before the drain.

Second, **none of it emitted an event.** No `Upgraded`, no `AdminChanged`, no logs whatsoever from the
proxy address at the slot-write block, the implementation-swap block, or the drain block. Any monitoring
built on proxy *events* would have seen nothing at any point. Only a storage-slot diff catches this.

The implementation swap itself came **2 minutes 36 seconds** before the drain — too fast to react to. The
slot acquisition nine days earlier is the actionable signal.

### The router lane, explicitly tested

The brief asked whether cross-chain / EVM router contracts show up in the exploited population. They do,
disproportionately relative to how few of them exist:

**Core lane — 11 of 79 (13.9%):** #27 and #110 Verus Ethereum Bridge (*the same contract, exploited twice —
May, then again in July with the flaw still live*), #63 Aztec RollupProcessorV2, #67 Aztec Connect
RollupProcessorV3, #101 New Market Trading `SquidRouterModule`, #106 Butter/MAP `OmniServiceProxy`,
#134 ZetaChain `GatewayEVM`, #139 Kipseli router, #151 Hyperbridge Token Gateway, #156 Aethir OFT adapter,
#157 `SquidMulticall`. Adjacent swap/settlement executors add three more (#16 Index Coop
`ExchangeIssuance`, #124 TrustedVolumes RFQ proxy, #125 Ekubo extension) — **14 of 79, 17.7%.**

Their fingerprints are consistent and distinctive:

1. **A permissionless entry point that accepts a caller-supplied identity or payload.** #101's Safe module
   inherits Axelar's `expressExecuteWithToken`, which anyone may call and which performs *no* gateway
   validation; the module then parses `sourceAddress` **out of the caller's own payload** and compares that
   string to `squidRouter`. #134's `GatewayEVM.execute` is an unrestricted arbitrary-call sink. #157's
   `SquidMulticall.run()` executes arbitrary calls by design.
2. **Verification logic that is subtly incomplete rather than absent.** #106 hashes dynamic-bytes fields
   with `abi.encodePacked` (collision). #151's MMR `VerifyProof()` never enforces `leaf_index < leafCount`.
   #67's `numRealTxs` lives outside the proof-covered header, so 1..32 all verify against the same proof.
   #63's escape-hatch circuit publishes `proof_id` as an *unconstrained* public witness.
3. **They hold authority, not balance** — mint rights over a bridged asset (#151, #156), unlimited spend on
   88 Safes (#101), or arbitrary-call power over anyone who approved them (#157).
4. **Two of them are name-collision traps.** #101 is called `SquidRouterModule` and has *no* affiliation
   with Squid; the confusion came purely from the contract name on Basescan. #157 is genuinely Squid's, but
   users approved the multicall instead of the router.

**Conclusion on the router lane: it earns its place, but not as an age or balance play.** Router/bridge
targets skew old (Verus 2.8 y, Aztec 4–5 y, ZetaChain proxy 1.5 y, MAP 1.55 y) and several hold near-zero
balance. The signal that finds them is *authority surface*: permissionless entrypoints, caller-supplied
routing identity, and delegated spend.

---

## 7. Observable pre-hack flags

Only flags that were genuinely visible *before* the exploit are listed. Hindsight-only observations are
excluded and named as such at the end.

### Measured across the population

Of the 53 primary exploited contracts whose verification status could be resolved:

- **13 were unverified** (#8, #24, #27, #39, #51, #66, #105, #110, #117, #123, #124, #125, #141) — 24.5%.
- **40 were verified.** Verification is not protective. #118's backdoor was in verified source for 102 days.
- **16 of 79 sat behind a proxy or clone**, and 4 of those are 45-byte ERC-1167 minimal proxies — a
  clone-factory fingerprint. Both Lixir vault tokens (#51) point at the *same* implementation
  `0x2ce186c52cf150000bf8ad2b4679d4ad619395cd`: one flaw, a whole clone family exposed.
- **29 expose a live `owner()`/`getOwner()`** returning a non-zero address.

### Flags with real predictive shape (ranked by how often they appear and how cheaply they're read)

1. **A single thin AMM pair as the price source** — the highest-yield wiring flag (§6).
2. **Custom `_transfer`/`_update` that touches the AMM pair's balance or calls `sync()`** — 7+ incidents,
   all BSC, all detectable by decompiling the transfer path and looking for `IUniswapV2Pair(...).sync()` or
   a balance write against the pair address.
3. **Incoherent on-chain configuration.** Three cases where the misconfiguration was live and readable for
   weeks or months before anyone used it:
   - #135 Singularity registered a Uniswap V3 fee tier of **42**. Valid tiers are 100/500/3000/10000.
     `factory.getPool()` silently returned `address(0)`, so the oracle valued all non-USDC reserves at zero.
     **Live for ~3 months.** One `getPool()` call detects it.
   - #59 OLPC's owner set `decimalsValue = 7326680472586200649`, then renounced ownership. **Live for 46
     days** before a dust transfer triggered the pair-draining burn.
   - #92 MoneyMon's `changeadmin()` had already set `admin = address(0)` on-chain, which is what made
     `ecrecover` returning zero pass the check. Readable before the fact.
4. **Uninitialised initializer on a live proxy.** #117 Aurellion — an EIP-2535 diamond exposing
   `initialize(address)` (`0xc4d66de8`) with the OZ `_initialized` slot still 0, live **55 days**.
   #123 Renegade — unprotected initializer after a migration left the version counter desynced.
   Both are read-only checks: does a callable initializer exist, and is the guard slot zero?
5. **Standing unlimited approvals to a contract that isn't a canonical router** (§6, 9 incidents).
6. **Abandonment markers.** #149's project's last public activity was in 2025. #67/#63 were deprecated for
   3–5 years by their own teams. #45, #66, #141 are explicitly "legacy" deployments. Abandonment is visible
   as: no contract interactions from the deployer in N months + no verified source updates + a live balance.
7. **Fork-with-divergence, and clone-family membership.** #71 Asterix is a direct fork of Flooring (#76) and
   was hit with the identical DN404/BT404 flaw **one day later**. #30 is a MakerDAO MCD fork (`Spotter`,
   `Dog`, `GemJoin` naming) on BSC whose divergence is a custom `Median Oracle` module with no deviation,
   floor or drawdown checks — the fork's *deviation from the base* is precisely the bug. Other lineages in
   the population: Set Protocol (#16), Aragon (#74), Colony Network (#116), Aztec Connect (#63, #67),
   BarnBridge SMART Yield (#39), Thetanuts (#66, #141), Juicebox/REVLoans (#142), SubQuery (#154),
   ApeSwap (#82), LayerZero OFT (#156), Axelar express-executable (#101), Solady (#86).
8. **Prior scrutiny that was dismissed.** #134 ZetaChain: a bug-bounty report describing the arbitrary-call
   behaviour **had been filed and was closed as by-design**. #27 Verus: the same flaw on the same contract
   had already been exploited two months earlier and was still live. Both are public before the fact.

### Flags that are hindsight-only — do not score on these

- "Flash loan was used" — true in 35% of cases, but flash-loan *availability* is a property of the chain,
  not the target. It is a multiplier, not a predictor.
- "The loss was large" — SlowMist's headline figures repeatedly conflate routed gross volume, arbitrage and
  actual theft (#80's $243.5K gross is ~$89K attacker profit; #66's $2.1M was ~$105K net after a whitehat
  recovery; #151's $237K was revised to $2.5M *after* the fact). Losses are not knowable pre-hack and the
  published ones are not even reliable post-hack.
- "The protocol was small" — several targets had substantial TVL (#45 $6M, #124 $5.87M) and several had
  almost none (#43 had a TVL of **~$883**, #105 had ~$97K). Size predicts nothing here.

---

## 8. What discovery currently misses

Six classes in this population would not be surfaced by a discovery net built around
"old + unattended + holds money + custom logic":

1. **Same-day BSC token deployments (11 incidents, 17% of the population).** Five were exploited within ~24
   hours of creation. No periodic sweep slower than daily can see them; and at creation they have no
   transaction history, no age, and often no TVL yet. **The signal that catches them is deployment-time, not
   discovery-time:** a new BSC contract whose transfer path writes to a Uniswap-V2-style pair or calls
   `sync()`, paired with a freshly created pair. This must run on the new-contract firehose, not on a
   re-scan of known contracts.
2. **Zero-balance authority holders (9 incidents, 11%).** Any ranking by contract balance puts
   TrustedVolumes' RFQ proxy, Ekubo's extension, the New Market Trading Safe module and `SquidMulticall` at
   the bottom. **Signal: aggregate live allowance granted to the address**, from `Approval` logs, rather
   than balance.
3. **Upgradeable targets aged by the wrong contract.** #94's proxy was 34 days old and its implementation 8.
   #39's money-moving implementation was installed 2 minutes before the drain. **Signal: age the
   implementation, and diff the EIP-1967 slots over time** — an admin-slot change to a fresh EOA gave 9 days
   of warning on BarnBridge.
4. **Clone-family exposure (#51, #71, #132, #135).** Discovery that treats each address independently
   re-derives the same finding N times or misses N−1 of them. **Signal: group by implementation address and
   by bytecode hash;** for 45-byte ERC-1167 clones, resolve the target and score the family.
5. **The "uncapped subsidy" class (9 incidents, 11.4%).** Not access control, not pricing. The reward
   function's eligibility predicate is a function of state the attacker can manufacture for free (fresh
   address, balance delta, duplicated ID, uninitialised checkpoint). If triage is organised around
   auth/oracle/reentrancy buckets, this class falls through. **Signal: reward/claim/redeem functions whose
   guard reads only `msg.sender`'s current balance, an array the caller supplies, or a mapping that is
   written after the payout.**
6. **Config-level defects with no code defect (#135, #59, #92, #30).** The code may be perfectly ordinary;
   the *stored parameter* is impossible. Static analysis of source won't flag `feeTier = 42` — you have to
   read the deployed state and check it against the domain. **Signal: validate live config against known
   valid domains (Uniswap fee tiers, decimals bounds, non-zero oracle addresses, `admin != address(0)` where
   an `ecrecover` comparison depends on it).**

---

## 9. Recommendation for discovery

Each item is tied to the population evidence rather than asserted.

**Age — run two nets, weighted by chain, not one global age band.**

- *BSC net:* weight **0–45 days**, ideally continuous on the new-contract stream. Basis: BSC median dwell 34
  days, 11 of 24 BSC targets ≤30 days, 5 exploited within ~24 hours of deployment.
- *Ethereum / Arbitrum net:* weight **> 2 years**, and specifically look for *funded and quiet*. Basis:
  Ethereum median dwell 901 days; 11 targets over 4 years; the oldest (7.66 y) still held 65 ETH.
- Deprioritise the **6-month-to-2-year** band: only 17.2% of the population, and the least distinctive.
- For upgradeable contracts, age the **implementation**, not the proxy (#94: 8 days vs 34).

**Categories to prioritise, in order of catchable volume.**

1. **Custom tokens with a fund-moving transfer hook** — 19 incidents, 24.1%, **17 of them BSC**. Concretely:
   `_transfer`/`_update` overrides that burn from, transfer out of, or `sync()` an AMM pair.
2. **Staking / reward / bond / distribution pools** — 13, 16.5%, split bsc 5 / mainnet 4 / base 1. The
   uncapped-subsidy class lives here, and it is the class current triage is least likely to have modelled.
3. **ERC-4626 / yield vaults with a diverged override** — 11, 13.9%, mainnet 6 / arbitrum 2 / base 1.
   Withdraw/redeem/`totalAssets` overrides, first-depositor conditions (`totalSupply()==0` while assets > 0),
   donatable exchange rates.
4. **Bridge / router / cross-chain executors** — 11, 13.9% (17.7% counting the adjacent swap/settlement
   executors), mainnet 6 / base 2 / bsc 1. See the authority-surface fingerprints in §6.

Those four are 54 of 79. Note the chain skew: prioritisation should be *per chain*, not global — on BSC the
list is tokens then reward pools; on Ethereum/Arbitrum it is vaults, bridges and settlement proxies.

**Wiring fingerprints to detect, highest yield first.**

1. Contract reads spot state (`getReserves`, `balanceOf(pair)`, `getAmountsOut`, `slot0`, `convertToAssets`)
   from an address that is an AMM pair or an ERC-4626 vault → **and that pool is thin**. Score on reserve
   depth relative to the target's own TVL. Basis: 22 incidents (28%) priced off external state; the
   canonical case (#13) priced off a 26-day-old pair with no TWAP.
2. Contract holds large aggregate live **allowances** while holding little or no balance. Basis: 9 incidents.
3. Contract exposes a permissionless entrypoint that takes a caller-supplied address, identity string, or
   calldata blob and acts on it (#101, #134, #142, #157, #10, #124). Basis: the router lane.
4. Contract is reachable from a flash-loan venue in one hop (Aave V3, Morpho, Balancer, Moolah, Venus,
   PancakeSwap Vault, Uniswap V4 PoolManager) — as a **severity multiplier**, not a finder.

**Flags to score on (each read directly from chain state, no source needed).**

| flag | weight rationale |
|---|---|
| EIP-1967 slots acquired by a contract that had none, or admin changed to a fresh EOA — **read the slots, not the events; #39 emitted none** | 9d 18h lead time, #39 |
| callable `initialize*` selector + `_initialized` guard slot == 0 | #117 (55 days live), #123 |
| stored config outside its valid domain (fee tier, decimals, zero oracle, `admin == address(0)`) | #135 (~3 months), #59 (46 days), #92 |
| transfer path writes to / `sync()`s an AMM pair | 7+ incidents, all BSC |
| unverified source **on an old, funded contract** | 13 of 53; but see caveat below |
| forked from a known base **and diverged** in the pricing or auth module | #30, #71, #76, #101 |
| clone-family membership (shared implementation / 45-byte ERC-1167) | #51, #132, #135 |
| a public bug report or a prior exploit on the same contract, unresolved | #134, #27 |
| `owner()` non-zero **and** custom fund-moving logic | 29 of 79 — necessary, far from sufficient |

**Do not score on:** verified-source-means-safe (#118's backdoor was verified in 11 seconds and lived 102
days), headline loss size, TVL size, or flash-loan usage on its own.

**One process change the data argues for:** #27/#110 is the same contract exploited twice with the same
flaw, two months apart. #71 was hit one day after its parent #76 with the identical flaw. **A watchlist keyed
on "codebase X was just exploited → who else runs codebase X" would have caught both.** That is a discovery
input, not an incident-response one.

---

## 10. Limits of this study

**Window.** 137 days, 2026-04-04 to 2026-08-18. Anything about seasonality, or about how these distributions
move year over year, is out of reach.

**Unrecovered targets.** 15 of 79 in-scope incidents have no verified creation date because the exploited
contract address itself could not be recovered from free-tier public sources:
**#12 RISEx** (team statement gives 2026-07-13 deploy → 2026-08-03 exploit, 21 days; *not independently
verified* and excluded from the distribution), **#17** Swan Treasury `ZhaiquanBuy`, **#25** Lien Finance
`BondMakerCollateralizedEth`, **#30** 42DAO, **#40** Cascade, **#43** Chi `ArbitrageV5` (the USC token is
resolved, the arbitrage contract is not), **#71** Asterix, **#76** Flooring V2, **#82** ApeBond, **#86**
ATOHook, **#96** ONTR, **#126** SmartCredit, **#151** Hyperbridge Token Gateway, **#156** Aethir OFT adapter,
**#158** TGAI. In each case the write-ups name the protocol and the mechanism but not the address, and no
explorer trail reachable from free-tier APIs closed the gap. These are recorded as gaps in
[`PROFILES.md`](PROFILES.md), not filled in.

**Tooling constraints that shaped what could be checked.** The supplied Etherscan V2 key is free-tier and
**refuses BNB Chain and Base** outright; BscScan's V1 API is retired and bscscan.com returns 403 to
non-browser clients. So: (a) BSC creation dates come from archive-RPC bisection rather than an explorer API
— exact to the block, and cross-checked, but the creating *transaction* is unrecoverable for factory-created
contracts with no constructor logs; (b) **BscScan verification status could not be checked at all.** BSC
verification in this report is Sourcify coverage, which is a *lower bound* — a "not in Sourcify" BSC row is
not evidence of an unverified contract. Base verification also came from Sourcify because
`base.blockscout.com` returned HTTP 500 throughout the run. Sourcify's `verifiedAt` reflects when Sourcify
recorded the contract and can lag the explorer, so verification *timing* claims are weak (the one exception
is #118, where `verifiedAt` is 11 seconds after a creation timestamp I measured myself).

**SlowMist's selection bias — the boundary on what this can conclude.** SlowMist lists *noticed, attributed*
hacks. It systematically undercounts silent drains, small drains and unattributed ones. This is measurable
rather than hypothetical: the DeFiHackLabs PoC set for the same window and the same four chains contains at
least **12 in-scope EVM contract exploits that appear nowhere in SlowMist's 8 pages** — CookFinanceIssuance
(BSC, ~$50K), DLMC (BSC, $222.6K), WHALE (BSC, $3.5K), BOSS (BSC, $10.2K), AISOTH Presale (BSC, $30.3K),
RWT (BSC, ~$118K), CrowdRingCircle (BSC, ~$201K), NFT Auction Marketplace (BSC, ~$4K), AIC (BSC, ~$21.5K),
UnprotectedArbBot (Base, ~$31.7K), StrongBlock (Ethereum, ~$72K), PantherBase (Base). Every one is small,
and 9 of 12 are BSC. **SlowMist's undercount is concentrated in exactly the sub-population this study finds
most numerous and most time-sensitive** — small, fresh BSC token/reward contracts — so the true BSC share is
higher than 24/64 and the true dwell distribution is skewed further toward the fresh hump than reported here.

**What this cannot tell you.** This is a profile of *what got hit*, drawn from the numerator only. There is
no denominator: nothing here says what fraction of in-scope contracts are vulnerable, what the base rate of
exploitation is, or what a given flag's false-positive rate would be. A contract matching every flag in §9
is a contract *shaped like* the ones that were exploited — that is the correct thing to point discovery at,
and it is not a probability of compromise. Read as targeting guidance, not as risk scoring.

---

## Repository contents

| path | what it is |
|---|---|
| [`REPORT.md`](REPORT.md) | this document — the synthesis |
| [`PROFILES.md`](PROFILES.md) | 79 per-target forensic profiles, every field sourced, gaps named |
| [`data/classification-table.md`](data/classification-table.md) | all 160 entries, kept vs discarded, one-line reason each |
| `data/slowmist-entries.json` | the parsed registry (source of the population) |
| `data/creation-dates.json`, `creation-dates-2.json` | creation tx / block / timestamp per address, with the method used |
| `data/observable-flags.json` | verification, proxy slots, owner, codesize per address |
| `data/incidents.json`, `dwell.json` | one row per incident / per address, used for the distributions |
| `data/exploit-block-timestamps.json` | exploit blocks resolved to UTC via `eth_getBlockByNumber` |
| `data/poc-metadata.json` | extracted headers of the 89 independent reproductions that were read |
| `scripts/` | the collection tooling (`chainlib.py` archive bisection, `flags.py` slot/verification scanner, classification and profile data) |
