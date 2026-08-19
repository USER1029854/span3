# Per-target forensic profiles (79 in-scope targets)

Every field carries its source. `RPC binary-search` means: `eth_getCode` bisected against an archive node until the
first block containing code, then that block's timestamp and (where the creating tx is a direct `CREATE`) the
creating transaction from the block's receipts. Fields that could not be recovered say so — they are not estimated.


---

## 2. FoxMarket — 2026-08-15

**SlowMist line:** Flash Loan Attack · $ 118,700 · [reference](https://x.com/SlowMist_Team/status/2089196291800908164)

**Classification:** BSC: FoxLpBondsPool.stake() prices LP bond off manipulable Pancake spot quote

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited pool | [`0x58e2a853bB14e46bEFD3148bd4280370feA4655a`](https://bscscan.com/address/0x58e2a853bB14e46bEFD3148bd4280370feA4655a) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |
| minting treasury | [`0x87614d97808dCdecB069fe8489848Fa1c001e04D`](https://bscscan.com/address/0x87614d97808dCdecB069fe8489848Fa1c001e04D) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |
| token | [`0xdF81d50c6657487D19B66A1b5375E35A804Abb93`](https://bscscan.com/address/0xdF81d50c6657487D19B66A1b5375E35A804Abb93) | bsc | yes | no |

### Age at time of hack

- **exploited pool** `0x58e2a853bB...` created **2026-08-10 07:12:12 UTC**, exploited 2026-08-15 -> **dwell 4 days (0.01 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x62bedfcbd74c340d...`](https://bscscan.com/tx/0x62bedfcbd74c340d77c43b8b9acfbb98c2c40987ccaf877d2f59e3e570b3fd7f).

- **minting treasury** `0x87614d9780...` created **2026-08-10 06:38:42 UTC**, exploited 2026-08-15 -> **dwell 4 days (0.01 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xd275cc467725020b...`](https://bscscan.com/tx/0xd275cc467725020bc4e74919fbd44e3a3a5b3d741b37aa09602d2d327daa6c93).

- **token** `0xdF81d50c66...` created **2026-07-03 08:53:25 UTC**, exploited 2026-08-15 -> **dwell 42 days (0.11 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x38ba496f739623c4...`](https://bscscan.com/tx/0x38ba496f739623c47b22a12b5d49dfc3b19be6028177ef597e4a1697d1e1a2ec).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 118,700; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **bond/reward pool (OHM-style LP bond)**

### Actual logic and exploited mechanism

- Flaw class: **spot-price-read-then-act (stale quote reused after own swap)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): FoxMarket (a DeFi project on BSC) had its FoxLpBondsPool.stake() function calculate and fix _stakeAmount from a manipulable Pancake AMM spot quote before a large USDT→Fox swap. The attacker used flash loans to skew pair reserves, then addLiquidity used a mismatched ratio; Treasury.lpBonds() trusted the stale value, minted excess Fox tokens, and sent inviter rewards to an attacker-controlled address, which were sold in the same transaction.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-08/FoxLpBondsPool_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap USDT/FOX pair (pricing + liquidity), multi-pool USDT flash-loan aggregation

### Fork / codebase lineage

- hand-rolled bond/treasury pattern (OlympusDAO-family bonding idea)

### Observable pre-hack flags

- fresh deploy (4d), custom stake()/lpBonds() pair, single thin AMM pair as price source, referral payout in same tx

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 4. USM — 2026-08-10

**SlowMist line:** Smart Contract Vulnerability · $ 136,000 · [reference](https://x.com/SlowMist_Team/status/2086644725143183639)

**Classification:** Ethereum: USM defund() split-invariance / rounding in FUM redemption curve

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited core | [`0x2a7FFf44C19f39468064ab5e5c304De01D591675`](https://etherscan.io/address/0x2a7FFf44C19f39468064ab5e5c304De01D591675) | mainnet | yes (`USM`) | no |
| token | [`0x86729873e3b88DE2Ab85CA292D6d6D69D548eDF3`](https://etherscan.io/address/0x86729873e3b88DE2Ab85CA292D6d6D69D548eDF3) | mainnet | yes (`FUM`) | no |

### Age at time of hack

- **exploited core** `0x2a7FFf44C1...` created **2021-10-10 09:47:09 UTC**, exploited 2026-08-10 -> **dwell 1764 days (4.83 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x82f9dfac1a1bb285...`](https://etherscan.io/tx/0x82f9dfac1a1bb285715263c32a63fb5e65148d06a76217fefd6399ae5fa393b1).

- **token** `0x86729873e3...` created **2021-10-10 09:47:09 UTC**, exploited 2026-08-10 -> **dwell 1764 days (4.83 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x82f9dfac1a1bb285...`](https://etherscan.io/tx/0x82f9dfac1a1bb285715263c32a63fb5e65148d06a76217fefd6399ae5fa393b1).
- Exploit block confirmed on-chain: mainnet block 25716149 at **2026-08-09 08:12:35 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- ~70.83 ETH extracted; USM's ETH collateral pool. Figure from the DeFiHackLabs trace of exploit tx 0xfae5e751...b050e; SlowMist's $136K headline is the USD conversion.

### What it was supposed to do

- Category: **algorithmic stablecoin (ETH-collateralised)**

### Actual logic and exploited mechanism

- Flaw class: **split-invariance / rounding in redemption curve**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The USM protocol suffered an exploit due to a pricing logic flaw in the ethFromDefund() function within defund(). It uses the arithmetic mean of the current and estimated final FUM sell prices for a single redemption but lacks “split invariance.” Combined with the per-redemption state contraction (adjShrinkFactor) and integer rounding, an attacker used a flash loan to call fund() to manipulate internal pricing, then split the same FUM amount into 64 small defund() calls, extracting more ETH than a single large call and causing a loss of ~70.83 ETH.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-08/USM_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Chainlink + Uniswap TWAP (read, NOT manipulated); Morpho Blue WETH flash loan for working capital

### Fork / codebase lineage

- hand-rolled (USM by Jacob Eliosoff, 2020-21 research project)

### Observable pre-hack flags

- 4.8y old, abandoned research protocol, no bounty, custom bespoke pricing math

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 8. Atomic Green — 2026-08-08

**SlowMist line:** Signature Replay Attack · $ 29,984.27 · [reference](https://x.com/SlowMist_Team/status/2086042810265055619)

**Classification:** Arbitrum: manager-signature replay across 21 UniV3 LP positions + spot-price valuation

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited proxy | [`0x51fF48f2d43966bE796692BdDdfaE96A435242a8`](https://arbiscan.io/address/0x51fF48f2d43966bE796692BdDdfaE96A435242a8) | arbitrum | **NO** | impl `0x62cc552215303341f9651e89db40e7336a394a0a` |
| strategy module | [`0xf617a3ad1f0ab9d9fe39e48d688bfe44562769d9`](https://arbiscan.io/address/0xf617a3ad1f0ab9d9fe39e48d688bfe44562769d9) | arbitrum | **NO** | impl `0xf8d5706edb7d02e7b996d6d977bc37801c1a4dc8` |
| lending module | [`0xc1b677039892c048f2efb7e9c5da1b51fde92504`](https://arbiscan.io/address/0xc1b677039892c048f2efb7e9c5da1b51fde92504) | arbitrum | yes (`TransparentUpgradeableProxy`) | impl `0xbb674bff40c117c3ad6aa76121830d5b762dc8e5` |

### Age at time of hack

- **exploited proxy** `0x51fF48f2d4...` created **2022-11-07 11:57:48 UTC**, exploited 2026-08-08 -> **dwell 1369 days (3.75 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xb67c8eba7ae29968...`](https://arbiscan.io/tx/0xb67c8eba7ae299687f4ee99967cb2135fc4bf2977bbe4a48aecf4316d182bd78).

- **strategy module** `0xf617a3ad1f...` created **2024-01-06 10:20:41 UTC**, exploited 2026-08-08 -> **dwell 944 days (2.58 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xb482c6dc21f2f62d...`](https://arbiscan.io/tx/0xb482c6dc21f2f62d60fa959b06e448801026c70ecc45e001fad0e799902902fa).

- **lending module** `0xc1b6770398...` created **2022-06-19 12:10:25 UTC**, exploited 2026-08-08 -> **dwell 1510 days (4.13 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xd1567a9704751259...`](https://arbiscan.io/tx/0xd1567a9704751259a358806a4df5f49623664fe850b9a224fac27f84f4ba6764).
- Exploit block confirmed on-chain: arbitrum block 492104035 at **2026-08-07 16:18:12 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 29,984.27; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **leveraged trading vault + isolated lending**

### Actual logic and exploited mechanism

- Flaw class: **spot-price-read-then-act (CL LP + collateral valued off a manipulated UniV3 pool)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Atomic Green (a non-custodial leveraged trading protocol on Arbitrum) was exploited due to a signature replay vulnerability. The same manager signature could be replayed across 21 different Uniswap V3 LP positions, combined with flashloan-based price manipulation, allowing the attacker to trigger unauthorized full LP burns and resulting in a loss of approximately 29,984.27 USDC.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-08/Atomic_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Aave V3 flashLoanSimple (ARB), UniswapV3 ARB/USDC.e pool 0xcda53b1f..dad8 as the manipulated price source

### Fork / codebase lineage

- unknown; core vault/strategy/lending unverified

### Observable pre-hack flags

- unverified implementations behind verified TransparentUpgradeableProxy, prices off a single UniV3 pool

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 10. Unistreets — 2026-08-06

**SlowMist line:** Smart Contract Vulnerability · $ 17,750 · [reference](https://x.com/unistreetapp/status/2085225140690751793)

**Classification:** Ethereum: LaunchpadFactoryAuto.launch() forwards attacker calldata to V4 PositionManager

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited factory | [`0xFB60CD0B36aD4bD839b91767a6Ad9055AB6aD825`](https://etherscan.io/address/0xFB60CD0B36aD4bD839b91767a6Ad9055AB6aD825) | mainnet | yes (`LaunchpadFactoryAuto`) | no |

### Age at time of hack

- **exploited factory** `0xFB60CD0B36...` created **2026-08-02 15:37:59 UTC**, exploited 2026-08-06 -> **dwell 3 days (0.01 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x02bce355d9611323...`](https://etherscan.io/tx/0x02bce355d96113230749238eaf68955bb70bc6ab6d3acf79635554e263266c8c).
- Exploit block confirmed on-chain: mainnet block 25692311 at **2026-08-06 00:27:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Custodied the Uniswap V4 LP-position NFT of EVERY token launched through it. Trace-verified net EOA gain 17,743.91 USDC + 0.00721 WETH plus illiquid launch memecoins.

### What it was supposed to do

- Category: **launchpad factory / LP custodian**

### Actual logic and exploited mechanism

- Flaw class: **arbitrary calldata forwarding (approval injection)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Unistreets LaunchpadFactoryAuto contract on Ethereum was exploited via arbitrary calldata injection. The factory custodied all launched tokens’ Uniswap V4 LP NFTs; the attacker injected setApprovalForAll approval and burned multiple LP positions, draining liquidity for a loss of approximately $17,750.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-08/UnistreetLaunchpad_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Uniswap V4 PositionManager 0xbD216513..ee9e and PoolManager 0x0000...8A90 — factory forwards user calldata into posm as itself

### Fork / codebase lineage

- hand-rolled V4 launchpad

### Observable pre-hack flags

- 3 days old at exploit, custodies every launch LP NFT, forwards user-supplied calldata verbatim

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 12. RISEx — 2026-08-03

**SlowMist line:** Smart Contract Vulnerability · $ 673,011.56 · [reference](https://x.com/risextrade/status/2084350396609520105)

**Classification:** RWA strategy behind XLP vault, misconfiguration since deployment — contract-side, chain unconfirmed

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 673,011.56; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **RWA strategy behind a perp LP vault**

### Actual logic and exploited mechanism

- Flaw class: **misconfiguration present since deployment**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): On August 3, 2026, an unauthorized withdrawal of 673,011.56 USDC occurred from the RWA strategy linked to RISEx’s XLP vault due to a misconfiguration present since its July 13 deployment. The team detected it within minutes, patched it by 08:09 UTC, and fully compensated XLP depositors using a portion of July fees; the platform and other components continued operating normally.

### Interaction graph

- XLP vault -> RWA strategy

### Fork / codebase lineage

- unknown

### Observable pre-hack flags

- deployed 2026-07-13, exploited 2026-08-03 (21 days) per the team statement — NOT independently verified on-chain

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 13. LOOPSDAO — 2026-08-02

**SlowMist line:** Price Manipulation · $ 690000 · [reference](https://x.com/DefimonAlerts/status/2084157533204197380)

**Classification:** BSC: LpdFi buy()/claimInterest() priced off thin Pancake LPD/USDC spot reserves

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited core | [`0xcE6A6e4413D85A136bBaC8AaE6fB46eAa77F295e`](https://bscscan.com/address/0xcE6A6e4413D85A136bBaC8AaE6fB46eAa77F295e) | bsc | yes | no |
| token | [`0x38763EebE58a69C9CC91876947D9fB83e1273604`](https://bscscan.com/address/0x38763EebE58a69C9CC91876947D9fB83e1273604) | bsc | yes | no |
| pricing pool | [`0x85346d31743796F7d00D675629e32783A968F210`](https://bscscan.com/address/0x85346d31743796F7d00D675629e32783A968F210) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited core** `0xcE6A6e4413...` created **2026-07-14 11:34:35 UTC**, exploited 2026-08-02 -> **dwell 18 days (0.05 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x33b80fcabf1e9073...`](https://bscscan.com/tx/0x33b80fcabf1e907335d5769d339d54f5e1949676576d10d9588ec9b973d7c2d1).

- **token** `0x38763EebE5...` created **2026-07-06 03:42:29 UTC**, exploited 2026-08-02 -> **dwell 26 days (0.07 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x99cb7d7802909a7e...`](https://bscscan.com/tx/0x99cb7d7802909a7eefe2781d9b3ccc59e59932ef4935704a8f718588782b2a7b).

- **pricing pool** `0x85346d3174...` created **2026-07-06 03:42:29 UTC**, exploited 2026-08-02 -> **dwell 26 days (0.07 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx **not resolvable** (factory `CREATE` with no constructor logs).
- Exploit block confirmed on-chain: bsc block 113613923 at **2026-08-02 15:59:59 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Protocol-owned Cake-LP: 1,678,049.36 Cake-LP burned, paying out 700,535 USDC + 4,059,427 LPD. Attacker net 573,034.79 USDC (EOA balance 116,495 -> 689,529.79 USDC).

### What it was supposed to do

- Category: **interest-bearing lending/bond protocol**

### Actual logic and exploited mechanism

- Flaw class: **spot-price-read-then-act + discrete-index interest accrual**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): LOOPSDAO’s LpdFi protocol on BSC was exploited. The attacker used a flash loan to manipulate the spot price of the thin PancakeSwap LPD/USDC pair (no TWAP or deviation guard), opened a massively inflated interest-bearing position with minimal LPD, and claimed interest right across the daily settlement boundary. This triggered the protocol to burn its own Cake-LP and pay out the inflated amount, draining approximately $690,000.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-08/LpdFi_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap LPD/USDC pair 0x85346d31 (sole price source), PancakeRouter removeLiquidity with min-out 0, protocol-owned Cake-LP

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- core 18d old, token+pair 26d old, price() reads instantaneous reserves of a thin pair, no TWAP/deviation bound, zero min-outputs

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 14. MOKE — 2026-08-02

**SlowMist line:** Smart Contract Vulnerability · $ 907700 · [reference](https://x.com/TenArmorAlert/status/2084102947500368164)

**Classification:** BSC: unprotected public claim() in MokeReleaseContract drains reserve pool

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited claim ctr | [`0x684D722EbF8980f49492f631f56765DD4Fb302A7`](https://bscscan.com/address/0x684D722EbF8980f49492f631f56765DD4Fb302A7) | bsc | yes | no |
| token | [`0x1A35C16cE21903Bc17Fd020c4ED73fEdC70c1b2A`](https://bscscan.com/address/0x1A35C16cE21903Bc17Fd020c4ED73fEdC70c1b2A) | bsc | yes | no |
| cashout path | [`0x5ae569d8a0539a6A603E96A26ac8CaEA7CEba377`](https://bscscan.com/address/0x5ae569d8a0539a6A603E96A26ac8CaEA7CEba377) | bsc | yes | no |

### Age at time of hack

- **exploited claim ctr** `0x684D722EbF...` created **2026-07-22 06:06:06 UTC**, exploited 2026-08-02 -> **dwell 10 days (0.03 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x2b2808c23625b7af...`](https://bscscan.com/tx/0x2b2808c23625b7af17e41ded67aa6daf9d79e40fe3bda619ee3b42d74dc33939).

- **token** `0x1A35C16cE2...` created **2026-04-12 08:09:36 UTC**, exploited 2026-08-02 -> **dwell 111 days (0.30 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xa44c94440502b66a...`](https://bscscan.com/tx/0xa44c94440502b66abadb1764448a798aeb56c9226f3c8bfb17c0d904d8585776).

- **cashout path** `0x5ae569d8a0...` created **2026-04-12 08:10:01 UTC**, exploited 2026-08-02 -> **dwell 111 days (0.30 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x0ec0339ab3d700f6...`](https://bscscan.com/tx/0x0ec0339ab3d700f63aa9fa2b2582fc859dd55a4b678d64c115652ec8bbb3946a).
- Exploit block confirmed on-chain: bsc block 113652609 at **2026-08-02 20:50:11 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 907700; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **token + reserve release contract**

### Actual logic and exploited mechanism

- Flaw class: **unprotected public claim (no eligibility check)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The MOKE token protocol on BNB Chain was exploited via a smart contract vulnerability. The attacker abused an unprotected public claim() function in MokeToken.releaseContract() (no eligibility check on the caller), repeatedly draining ~166 million MOKE from the protocol’s internal reserve pool, then used flash loans, Venus leverage, LP removal, and dividend distribution mechanisms to convert it into ~1,546 BNB, resulting in a loss of approximately $907,700.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/MOKE_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Moolah/Lista flash loans, Venus (vBTC/vBNB) leverage, MokeLPManager, MokeLPDividend distribute/claim; EIP-7702 self-delegation as packaging

### Fork / codebase lineage

- hand-rolled BSC token ecosystem (token/LP-manager/dividend/release quartet)

### Observable pre-hack flags

- release contract 10d old and unverified, token 111d old, whitelisted-handler cash-out plumbing

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 16. Set Protocol — 2026-07-30

**SlowMist line:** Smart Contract Vulnerability · $ 9,600 · [reference](https://x.com/SlowMist_Team/status/2082767887245410320)

**Classification:** Ethereum: ExchangeIssuance TOCTOU on SetToken positionMultiplier via attacker manager hook

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited contract | [`0xc8C85A3b4d03FB3451e7248Ff94F780c92F884fD`](https://etherscan.io/address/0xc8C85A3b4d03FB3451e7248Ff94F780c92F884fD) | mainnet | yes (`ExchangeIssuance`) | no |

### Age at time of hack

- **exploited contract** `0xc8C85A3b4d...` created **2021-03-24 04:52:20 UTC**, exploited 2026-07-30 -> **dwell 1953 days (5.35 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xa6c26717dc8f525c...`](https://etherscan.io/tx/0xa6c26717dc8f525c1c028bf6b20de417f5454219ddb37f81dc76d0f9f203547e).

### What it held and controlled

- ExchangeIssuance's own component inventory (LINK/UNI/AAVE/MKR/WBTC/HEX/BIT/USDC/WETH), ~$9.6K drained — small relative to the contract's role.

### What it was supposed to do

- Category: **index/structured product issuance**

### Actual logic and exploited mechanism

- Flaw class: **TOCTOU between quote read and settlement (no state lock)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The DeFi protocol Set Protocol (involving Index Coop’s ExchangeIssuance contract) was exploited due to insufficient state locking in the smart contract. The attacker used a malicious manager pre-issue hook to artificially inflate asset valuations (e.g., positionMultiplier), causing the contract to transfer excess assets based on falsified data, resulting in a loss of approximately $9,600.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/ExchangeIssuance_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Set Protocol SetTokenCreator, BasicIssuanceModule, CustomOracleNavIssuanceModule; Balancer flash loan; attacker-deployed manager/hook/valuer

### Fork / codebase lineage

- Set Protocol / Index Coop codebase

### Observable pre-hack flags

- 5.35y old, trusts arbitrary SetToken state, permissionless SetToken creation

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 17. Swan Treasury — 2026-07-30 *(borderline)*

**SlowMist line:** Private Key Leakage · $ 625,000 · [reference](https://x.com/DefimonAlerts/status/2083039796784410802)

**Classification:** BSC: signer key hardcoded in ZhaiquanBuy leaked, but buy() has no discount floor/bounds check — on-chain contract defect, off-chain trigger

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 625,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **token sale / treasury**

### Actual logic and exploited mechanism

- Flaw class: **signature-validation bypass with no bounds check on the signed discount**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The decentralized asset management protocol Swan Treasury on BNB Chain was exploited due to the leakage of an off-chain signer's private key (the _signer key hardcoded in the ZhaiquanBuy contract). The attacker forged valid signatures and used PancakeSwap flash loans to purchase approximately 687,000 STY tokens at around a 100x discount (spending approximately 19,700 USDT). The attacker then forged the related claim()/transfer signatures and dumped the tokens into the STY/USDT pool, making a profit of approximately $625,000.

### Interaction graph

- PancakeSwap flash loans, STY/USDT pool

### Fork / codebase lineage

- unknown

### Observable pre-hack flags

- signer key hardcoded in the contract; no floor price on the discount parameter

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 18. Crypto DAO — 2026-07-28

**SlowMist line:** Smart Contract Vulnerability · $ 52,000 · [reference](https://x.com/GoPlusSecurity/status/2082353004980707444)

**Classification:** BSC: Pro token reward-on-transfer self-dealing, permissionless player/winner registration

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0x8D65744527f55d0b2338350912d5C99A81ddF0e2`](https://bscscan.com/address/0x8D65744527f55d0b2338350912d5C99A81ddF0e2) | bsc | yes | no |
| drained pool | [`0x63844BD4BFad910B1643713302a1cC1ed20d50c3`](https://bscscan.com/address/0x63844BD4BFad910B1643713302a1cC1ed20d50c3) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited token** `0x8D65744527...` created **2026-01-11 17:18:25 UTC**, exploited 2026-07-28 -> **dwell 197 days (0.54 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xe9611dd17425ec8f...`](https://bscscan.com/tx/0xe9611dd17425ec8f7ebad408a14a2739722ee7eb2855eb761254c766523a8598).

- **drained pool** `0x63844BD4BF...` created **2026-01-11 17:18:25 UTC**, exploited 2026-07-28 -> **dwell 197 days (0.54 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx **not resolvable** (factory `CREATE` with no constructor logs).
- Exploit block confirmed on-chain: bsc block 112654014 at **2026-07-28 15:58:10 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- USDT reserve of the PancakeSwap USDT/Pro pair: ~605K USDT in the single reproduced tx; ~$8.2M cumulative across ~13 txs.

### What it was supposed to do

- Category: **custom token with reward-on-transfer**

### Actual logic and exploited mechanism

- Flaw class: **uncapped subsidy / self-dealing reward path**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The Pro token contract of Crypto DAO was exploited due to missing access control, with the attacker calling publicly accessible vault functions. According to GoPlus Security’s analysis, the attacker’s actual profit was approximately $52,000, while the contract lost around 167,200 Pro tokens. The related addresses monitored by Blockaid collectively held approximately $8.2 million worth of USDT (not the actual stolen amount).

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/ProToken_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap USDT/Pro pair (drained), attacker player+winner clones

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 197d old, reward swap fires on transfer, permissionless player registration

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 19. LULA — 2026-07-28

**SlowMist line:** Price Manipulation Attack · $ 578,100 · [reference](https://x.com/CertiKAlert/status/2082309959484911845)

**Classification:** BSC: LULA public claimReward()/recycle() redeems against attacker-deflated pool

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0xf5d7029eb6751d170dcF0Bb1c87Af6f93d5A2e9a`](https://bscscan.com/address/0xf5d7029eb6751d170dcF0Bb1c87Af6f93d5A2e9a) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |
| drained pool | [`0xf0b36389a12a28be1280c0eC2a4bbc76889d6a96`](https://bscscan.com/address/0xf0b36389a12a28be1280c0eC2a4bbc76889d6a96) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited token** `0xf5d7029eb6...` created **2026-06-24 16:30:52 UTC**, exploited 2026-07-28 -> **dwell 33 days (0.09 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xb1448a89b6b6c648...`](https://bscscan.com/tx/0xb1448a89b6b6c64876347aacaf95ebcda9a3309d47142c5cb766b5eb9da4f6de).

- **drained pool** `0xf0b36389a1...` created **2026-06-24 16:30:52 UTC**, exploited 2026-07-28 -> **dwell 33 days (0.09 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx **not resolvable** (factory `CREATE` with no constructor logs).
- Exploit block confirmed on-chain: bsc block 112655390 at **2026-07-28 16:08:29 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- USDT reserve of the LULA/USDT pair: 578,295 USDT.

### What it was supposed to do

- Category: **custom token with referral/reward recycle**

### Actual logic and exploited mechanism

- Flaw class: **uncapped subsidy redeemed against an attacker-deflated pool**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The LULA token on BSC was exploited when attackers abused the privileged recycle() function in its contract, combined with an approximately $237 million flash loan to manipulate PancakeSwap V2 liquidity pool reserves, resulting in a loss of about $578,100.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/LULA_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap LULA/USDT pair, flash loan; ~12 days of pre-accumulated reward state

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 33d old, reward payout scales with pool deflation, unverified on Sourcify

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 24. Projekt — 2026-07-25

**SlowMist line:** Flash Loan Attack · $ 560000 · [reference](https://x.com/DefimonAlerts/status/2081781283584106959)

**Classification:** Ethereum: permissionless trackPurchase() sizes rewards from balance deltas, no payment check

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault | [`0x574fc478bc45ce144105fa44d98b4b2e4bd442cb`](https://etherscan.io/address/0x574fc478bc45ce144105fa44d98b4b2e4bd442cb) | mainnet | **NO** | no |

### Age at time of hack

- **exploited vault** `0x574fc478bc...` created **2021-07-14 20:56:09 UTC**, exploited 2026-07-25 -> **dwell 1836 days (5.03 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xe7094a0eb5078abe...`](https://etherscan.io/tx/0xe7094a0eb5078abee79e96cba177659f89bccf290f6af07b1f3792236cf24038).
- Exploit block confirmed on-chain: mainnet block 25606412 at **2026-07-25 01:11:59 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- **Independently verified on-chain by this study**: vault ETH balance went 400.6514 ETH -> 98.9576 ETH across block 25606412 (`eth_getBalance` at block-1 and block+2), i.e. -301.6938 ETH. Matches the reported ~$560K.

### What it was supposed to do

- Category: **reward vault**

### Actual logic and exploited mechanism

- Flaw class: **unverified purchase accounting (balance-delta reward, no payment check)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The Projekt (GREEN/GOLD) reward vault on Ethereum was exploited. The attacker flash-loaned ~14K WETH from Morpho, pushed it into multiple Uniswap V2 memecoin pairs and used skim() to create fake “purchase” records. Exploiting the permissionless trackPurchase function (which only reads token balance deltas to size rewards without verifying actual ETH spent), they inflated reward allocations and drained ~301.7 ETH (~$560K) from the vault’s reward pool via massWithdraw.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/ProjektRewardVault_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Morpho flash loan (~14K WETH), dozens of UniV2 memecoin pairs via skim(), massWithdraw payout in ETH

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 5.03y old, unverified source, permissionless trackPurchase, holds 400 ETH

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 25. Lien Finance — 2026-07-24

**SlowMist line:** Smart Contract Vulnerability · $ 542,000 · [reference](https://x.com/SlowMist_Team/status/2080555677811171459)

**Classification:** Ethereum: permissionless registerNewBond + crafted payoff mispriced by bondPricer

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.
- Exploit block confirmed on-chain: mainnet block 25599302 at **2026-07-24 01:26:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 542,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **structured products / bond maker**

### Actual logic and exploited mechanism

- Flaw class: **permissionless registration + crafted payoff mispriced by the pricer**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): On July 24, 2026, Lien Finance (an Ethereum DeFi structured products protocol) was exploited. The attacker abused a validation flaw in the exchangeEquivalentBonds function of the BondMakerCollateralizedEth contract (missing multiset integrity checks), minting unbacked bond tokens and draining approximately $542K USDC via OTC pools.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/LienFinance_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Chainlink ETH feed (read at normal values), bondPricer, GeneralizedDotc OTC pools, LP standing allowance

### Fork / codebase lineage

- Lien Finance codebase (2020)

### Observable pre-hack flags

- abandoned 2020-era protocol, permissionless registerNewBond, LP with unlimited allowance to OTC pools

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 27. Verus Ethereum Bridge — 2026-07-23

**SlowMist line:** Smart Contract Vulnerability · $ 7,540,000 · [reference](https://x.com/blockaid_/status/2080143099561496896)

**Classification:** Ethereum: Verus bridge import path mints unbacked payouts (repeat of the May flaw)

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited bridge | [`0x71518580f36feceffe0721f06ba4703218cd7f63`](https://etherscan.io/address/0x71518580f36feceffe0721f06ba4703218cd7f63) | mainnet | **NO** | no |

### Age at time of hack

- **exploited bridge** `0x71518580f3...` created **2023-10-03 22:29:59 UTC**, exploited 2026-07-23 -> **dwell 1023 days (2.80 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x7bd34b417fd69a0d...`](https://etherscan.io/tx/0x7bd34b417fd69a0df81dffb4b29c318ce1d3a337ef86a794f6a7e3b10692a428).
  **Caveat:** Address confirmed for the May incident by the DeFiHackLabs PoC (VerusBridge_exp.sol, fork block 25118334). For the July incident the same address is INFERRED from SlowMist's own statement that it is "the second exploit of the same flaw from May"; the July exploit tx was not independently located.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 7,540,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **cross-chain bridge (EVM side)**

### Actual logic and exploited mechanism

- Flaw class: **unbacked payout via the import path**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The Verus Ethereum Bridge was exploited again. The attacker abused the bridge’s import path to trigger unbacked payouts on the Ethereum side, draining approximately $7.54 million in assets (ETH, tBTC, USDC, etc.) from the bridge reserves. This is the second exploit of the same flaw from May. The project has not issued a detailed official statement yet.

### Interaction graph

- Verus notarisation/import path; bridge reserves in ETH/tBTC/USDC

### Fork / codebase lineage

- hand-rolled Verus bridge

### Observable pre-hack flags

- 2.8y old, SECOND exploitation of the same flaw after May — flaw publicly known and unfixed

### Prior review status

- **The same flaw had already been exploited on the same contract in May 2026 (entry 110) and was still live in July.** The May incident is the prior scrutiny.

---

## 30. 42DAO — 2026-07-22

**SlowMist line:** Price Oracle Manipulation · $ 915,000 · [reference](https://x.com/SlowMist_Team/status/2079759793192132810)

**Classification:** BSC: MakerDAO-fork Median Oracle/Spotter poke with no deviation or floor checks

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 915,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **CDP stablecoin (MakerDAO fork)**

### Actual logic and exploited mechanism

- Flaw class: **oracle manipulation — no deviation/floor/drawdown checks on the median feed**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The 42DAO protocol was exploited. The attacker manipulated the Median Oracle with an abnormally low BTCB price, triggering forced liquidations of multiple BTCB vaults and profiting approximately $915,000. This caused its algorithmic stablecoin Balance Coin (BLC) to crash over 99% from near $1 to about $0.001.

### Interaction graph

- Median Oracle -> Spotter.poke -> Dog.bark liquidation -> GemJoin mint; PancakeSwap V2 for the exit

### Fork / codebase lineage

- MakerDAO MCD fork (Spotter/Dog/GemJoin naming) on BSC

### Observable pre-hack flags

- MCD fork with a custom oracle module; no deviation guard

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 39. BarnBridge — 2026-07-15

**SlowMist line:** Governance Attack · $ 776,000 · [reference](https://x.com/FortaNetwork/status/2077364671275769860)

**Classification:** Ethereum: abandoned BarnBridge governance captured, proxy re-pointed to sweep impl over live approvals

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited proxy | [`0x66c6f3b4B4b458e6d764759Ecf122484ebEf7580`](https://etherscan.io/address/0x66c6f3b4B4b458e6d764759Ecf122484ebEf7580) | mainnet | **NO** | impl `0xb8a154b450e8a3b5a0a3083df0b8e19190489dda` |

### Age at time of hack

- **exploited proxy** `0x66c6f3b4B4...` created **2026-07-06 08:13:35 UTC**, exploited 2026-07-15 -> **dwell 8 days (0.02 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xa42c84d2dd4e3141...`](https://etherscan.io/tx/0xa42c84d2dd4e3141775f419cadc743167c4e2df4c4cf15287ca40128b7e02eba).
- Exploit block confirmed on-chain: mainnet block 25535120 at **2026-07-15 02:39:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not the proxy's own balance — the attacker drained USDC out of ~50 user wallets that still held standing approvals to the proxy. 774,943.38 USDC.

### What it was supposed to do

- Category: **lending/yield provider (abandoned)**

### Actual logic and exploited mechanism

- Flaw class: **governance capture -> proxy upgrade -> arbitrary transferFrom over live approvals**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): DeFi protocol BarnBridge suffered a governance attack on July 15, 2026. The attacker gained control of the DAO via a malicious governance proposal, upgraded the proxy contract to a malicious implementation, and drained approximately $776,000 USDC by exploiting pre-existing approvals from around 50 user addresses.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/CompoundProvider_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- EIP-1967 proxy; ~50 user wallets with standing USDC approvals; Compound underlying

### Fork / codebase lineage

- BarnBridge SMART Yield codebase

### Observable pre-hack flags

- abandoned DAO, live proxy over 50 standing approvals; EIP-1967 admin slot went 0x0 -> attacker EOA 9 days before the drain; impl swapped 2m36s before it

### Prior review status

- BarnBridge was audited during its active life, but the DAO was effectively abandoned; no live monitoring caught the 9-day gap between the attacker taking the proxy admin slot and the drain.

---

## 40. Cascade — 2026-07-15 *(borderline)*

**SlowMist line:** Price Manipulation · $ 1,343,921 · [reference](https://x.com/cascade_xyz/status/2077747846011306123)

**Classification:** Arbitrum: mark-price manipulation in a thin pre-launch CLS market — economic/pricing design, on-chain

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 1,343,921; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **perp venue (pre-launch vault)**

### Actual logic and exploited mechanism

- Flaw class: **mark-price manipulation in a thin market**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Cascade, a perpetual contract platform backed by institutions including Polychain, was attacked on Arbitrum through its pre-launch locked CLS vault (First Wave invite-only deposits). The attacker accumulated long positions in a low-liquidity market to hedge against CLS short positions, artificially manipulated the mark price upward, triggering large-scale liquidations of CLS short positions. After profiting from the attack, the attacker immediately withdrew approximately $1.34 million USDC. The project team paused trading and withdrawals, and the funds were largely recovered afterward, with full compensation arranged for affected users.

### Interaction graph

- CLS pre-launch vault, internal mark-price mechanism

### Fork / codebase lineage

- unknown

### Observable pre-hack flags

- invite-only pre-launch market with very low liquidity

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 41. Drips Network — 2026-07-14

**SlowMist line:** Smart Contract Vulnerability · $ 24,900 · [reference](https://olympixai.medium.com/summer-fi-lumi-finance-drips-network-6-3m-lost-to-assumptions-nobody-tested-57f1769bda14)

**Classification:** Ethereum: DaiDripsHub.give() unchecked uint128->int128 cast flips transfer direction

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited hub | [`0x73043143e0a6418cc45d82d4505b096b802fd365`](https://etherscan.io/address/0x73043143e0a6418cc45d82d4505b096b802fd365) | mainnet | yes (`ManagedDripsHubProxy`) | impl `0x8d321e80487356c846f34456d31ce761776ef697` |

### Age at time of hack

- **exploited hub** `0x73043143e0...` created **2021-12-13 23:31:03 UTC**, exploited 2026-07-14 -> **dwell 1673 days (4.58 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x48ab581165bc3890...`](https://etherscan.io/tx/0x48ab581165bc3890e34c7c2ace7cdf2824478c4748b2271710a15ac7addc02a4).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 24,900; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **streaming payments**

### Actual logic and exploited mechanism

- Flaw class: **unsafe integer cast (uint128 -> int128) reverses transfer direction**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): DeFi streaming payments protocol Drips Network was exploited on July 14, 2026. The attacker used an unsafe integer cast vulnerability (uint128 to int128) in the DaiDripsHub.give() function on Ethereum, causing a negative value to flip positive and reverse the transfer direction, draining 24,882.99 DAI (~$24,900) from the DaiReserve.

### Interaction graph

- DaiReserve; DAI

### Fork / codebase lineage

- Drips v1 codebase (Radicle lineage)

### Observable pre-hack flags

- 4.58y old legacy deployment, superseded by newer Drips versions, still funded

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 42. Lumi Finance — 2026-07-13

**SlowMist line:** Smart Contract Logic Vulnerability · $ 270,000 · [reference](https://x.com/SlowMist_Team/status/2076669154036527314)

**Classification:** Arbitrum: Sodium ERC-4337 account grants approvals during UserOp validation; session-key validation bypass

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited account | [`0x65DE72bD1897B017C91f41c86de2B15873320804`](https://arbiscan.io/address/0x65DE72bD1897B017C91f41c86de2B15873320804) | arbitrum | yes (`Proxy`) | no |
| exploited account | [`0x9Ba99e76f2bE6571ae1bf82420621211EFD45236`](https://arbiscan.io/address/0x9Ba99e76f2bE6571ae1bf82420621211EFD45236) | arbitrum | yes (`Proxy`) | no |

### Age at time of hack

- **exploited account** `0x65DE72bD18...` created **2023-12-08 02:52:12 UTC**, exploited 2026-07-13 -> **dwell 947 days (2.59 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x86cebc79829b62a6...`](https://arbiscan.io/tx/0x86cebc79829b62a6c82d1c7c151ea8e8e081fa46acf0b7fba76c8f4c5f586f0c).

- **exploited account** `0x9Ba99e76f2...` created **2023-12-09 22:48:52 UTC**, exploited 2026-07-13 -> **dwell 946 days (2.59 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xd24319af8485f787...`](https://arbiscan.io/tx/0xd24319af8485f787a0a73cd18c0becd3b69fca76c0644c679f793596e8679adc).
- Exploit block confirmed on-chain: arbitrum block 483046805 at **2026-07-12 10:38:04 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 270,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **ERC-4337 smart accounts**

### Actual logic and exploited mechanism

- Flaw class: **validation-phase side effect + session-key validation bypass**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The DeFi protocol Lumi Finance on Arbitrum suffered an exploit where attackers leveraged Sodium smart accounts that performed token approvals as a side effect during UserOp validation. This allowed a malicious Paymaster to gain allowances from multiple accounts and drain funds, resulting in approximately $270,000 in losses.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/Sodium_exp.sol / 2026-07/LumiFinance_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- EntryPoint v0.6 0x5FF137D4..2789, attacker paymaster and EIP-1271 signer contract; 300+ victim accounts

### Fork / codebase lineage

- Sodium smart-account codebase

### Observable pre-hack flags

- accounts ~2.6y old, session-key path validates before the auth proof is checked

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 43. Chi Protocol — 2026-07-13

**SlowMist line:** Smart Contract Logic Vulnerability · $ 8,500 · [reference](https://x.com/DefimonAlerts/status/2076887008773829119)

**Classification:** Ethereum: Chi ArbitrageV5.burn() redeems at hardcoded $1 peg with no spot check (mint() has one)

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| stablecoin | [`0x38547d918b9645f2d94336b6b61aeb08053e142c`](https://etherscan.io/address/0x38547d918b9645f2d94336b6b61aeb08053e142c) | mainnet | yes (`USC`) | no |

### Age at time of hack

- **stablecoin** `0x38547d918b...` created **2024-03-20 18:31:59 UTC**, exploited 2026-07-13 -> **dwell 844 days (2.31 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x35f162beb8d24735...`](https://etherscan.io/tx/0x35f162beb8d24735f59fbd93c78caefd3f08ee0a5af315bfe5a40b6f62de3415).

### What it held and controlled

- Protocol TVL was ~$883 immediately before the drain (per the reconstruction) — the contract was a functionally defunct stablecoin still redeeming collateral at a hardcoded $1.

### What it was supposed to do

- Category: **LST-backed stablecoin**

### Actual logic and exploited mechanism

- Flaw class: **asymmetric peg validation (mint checks spot, burn does not)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Chi Protocol (a DeFi stablecoin protocol issuing $USC backed by LSTs/LRTs on Ethereum) was exploited due to a logic error in the ArbitrageV5 contract’s burn() function. The attacker used a flash loan to buy heavily depegged $USC cheaply on a thin Uniswap V2 pool and burned it to redeem full-value collateral (weETH/stETH/WETH) at the hardcoded $1 peg, without the burn function checking the actual peg (unlike the mint function). This resulted in approximately $8,500 loss, nearly draining the protocol’s reserves.

### Interaction graph

- thin Uniswap V2 USC pool (source of the cheap USC), ReserveHolder holding weETH/stETH/WETH, Uniswap V3 for weETH->ETH

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- USC token 2.31y old, TVL ~$883 at exploit — functionally defunct but still redeemable at a hardcoded $1

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 45. Lazy Summer Protocol — 2026-07-06

**SlowMist line:** Smart Contract Vulnerability · $ 6,040,000 · [reference](https://x.com/summerfinance_/status/2074214443261509721)

**Classification:** Ethereum: FleetCommander NAV = live sum of Ark totalAssets() with no manipulation guard

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault | [`0x98c49e13bf99d7cad8069faa2a370933ec9ecf17`](https://etherscan.io/address/0x98c49e13bf99d7cad8069faa2a370933ec9ecf17) | mainnet | yes (`FleetCommander`) | no |

### Age at time of hack

- **exploited vault** `0x98c49e13bf...` created **2025-02-07 13:52:23 UTC**, exploited 2026-07-06 -> **dwell 513 days (1.40 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x195c7acaca09e33c...`](https://etherscan.io/tx/0x195c7acaca09e33cb67396c1f4175fa6415f459cc419a3854c113ea53d9c61ca).
- Exploit block confirmed on-chain: mainnet block 25471347 at **2026-07-06 05:17:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Lazy Summer USDC vault; ~6.02M DAI/USDC extracted from other depositors by inflating NAV ~9.5%.

### What it was supposed to do

- Category: **yield vault (multi-ark allocator)**

### Actual logic and exploited mechanism

- Flaw class: **NAV/share-price inflation via donated overvalued assets**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Lazy Summer Protocol (under Summer.fi) USDC vaults were exploited due to NAV/share price calculation flaw. The attacker used flash loans and pre-accumulated overvalued Silo tokens to inflate vault NAV (~9.5%), redeeming at inflated price and extracting ~$6.04M from other depositors.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/SummerFi_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- FleetCommander NAV = sum of Ark totalAssets(); SiloManagedVault ark following Silo vgUSDC which counts depegged xUSD at par; Uniswap V4 + Balancer V3 for the cheap mint

### Fork / codebase lineage

- Summer.fi Lazy Summer codebase

### Observable pre-hack flags

- 1.4y old, NAV read live with no manipulation guard, empty ark donatable

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 47. Hinkal — 2026-07-02

**SlowMist line:** Smart Contract Vulnerability · $ 820,000 · [reference](https://x.com/hinkal_protocol/status/2073136163880149417)

**Classification:** Ethereum: Hinkal prooflessDeposit()/transact() note-to-nullifier binding failure (double-spend)

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited pool | [`0x25e5e82f5702a27c3466fe68f14abdbbadfca826`](https://etherscan.io/address/0x25e5e82f5702a27c3466fe68f14abdbbadfca826) | mainnet | yes (`Hinkal`) | no |

### Age at time of hack

- **exploited pool** `0x25e5e82f57...` created **2025-06-27 22:14:35 UTC**, exploited 2026-07-02 -> **dwell 369 days (1.01 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xefd3d917087ff47c...`](https://etherscan.io/tx/0xefd3d917087ff47c76fa503e61504699bdfef943c46dd3be110d7e9318e84bec).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 820,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **privacy pool**

### Actual logic and exploited mechanism

- Flaw class: **note-to-nullifier binding failure (double-spend) + prooflessDeposit without format validation**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Hinkal privacy DeFi protocol's Ethereum contract was exploited. The attacker used a "proofless deposit" vulnerability to drain approximately $820K USDC, then converted it to ETH and laundered via Tornado Cash and THORChain. The team paused contracts, limited the incident to one Ethereum pool, and committed to 1:1 user compensation.

### Interaction graph

- shielded pool; Tornado Cash and THORChain for the exit

### Fork / codebase lineage

- hand-rolled ZK pool

### Observable pre-hack flags

- 1.01y old, legacy note format still accepted, prooflessDeposit path

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 48. Edel Finance — 2026-07-01

**SlowMist line:** Smart Contract Vulnerability · $ 403,000 · [reference](https://x.com/edeldotfinance/status/2072154468058022033)

**Classification:** Ethereum: Edel lending values wrapped xStock via mutable ERC4626 convertToAssets()

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited contract | [`0xBd497eE429D9D3E46446339286271b3714a83B29`](https://etherscan.io/address/0xBd497eE429D9D3E46446339286271b3714a83B29) | mainnet | yes (`AaveOracle`) | no |
| entry proxy | [`0x3EEeB3cd20f844a578807fc457388Ceb9A67fAa6`](https://etherscan.io/address/0x3EEeB3cd20f844a578807fc457388Ceb9A67fAa6) | mainnet | yes (`InitializableImmutableAdminUpgradeabilityProxy`) | impl `0xf7ba2c2b2e3b8c3c327b632e6bdff77840f06b34` |

### Age at time of hack

- **exploited contract** `0xBd497eE429...` created **2026-03-13 08:15:35 UTC**, exploited 2026-07-01 -> **dwell 109 days (0.30 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xd6fe6b1305b8a82c...`](https://etherscan.io/tx/0xd6fe6b1305b8a82c2700d9fa557fe42465f7c215a97a2316c931b0665c8a5729).

- **entry proxy** `0x3EEeB3cd20...` created **2026-03-13 08:15:59 UTC**, exploited 2026-07-01 -> **dwell 109 days (0.30 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x00f0cd1e3d6935d3...`](https://etherscan.io/tx/0x00f0cd1e3d6935d3576bc17773e4ce50c37509bc7a4c533aefbf06e1b2609716).
- Exploit block confirmed on-chain: mainnet block 25434061 at **2026-07-01 00:24:35 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 403,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **lending market on wrapped RWA (xStock)**

### Actual logic and exploited mechanism

- Flaw class: **ERC4626 exchange-rate donation inflates collateral in the same tx**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Edel Finance lending protocol was exploited via wGOOGLx wrapped token exchange rate manipulation. The attacker used flash loans in repeated deposit/borrow loops to inflate wGOOGLx collateral value ~78x, then borrowed assets, creating ~$403K bad debt.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-07/edel-xstock_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- wGOOGLx ERC4626 wrapper convertToAssets() as the oracle; recursive supply/borrow loops

### Fork / codebase lineage

- hand-rolled xStock lending

### Observable pre-hack flags

- 109d old, collateral priced through a donatable ERC4626 rate

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 49. AIDC — 2026-06-28

**SlowMist line:** Smart Contract Vulnerability · $ 121,000 · [reference](https://x.com/SlowMist_Team/status/2071437371590238249)

**Classification:** BSC: AIDCToken lets ordinary transfers burn accumulated sell amounts out of the AMM pair

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0x5021d71859f81b4c905b573591db8f9cc4a0c6fe`](https://bscscan.com/address/0x5021d71859f81b4c905b573591db8f9cc4a0c6fe) | bsc | yes | no |

### Age at time of hack

- **exploited token** `0x5021d71859...` created **2026-06-27 19:11:05 UTC**, exploited 2026-06-28 -> **dwell 0 days (0.00 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x5843cebd139cbadd...`](https://bscscan.com/tx/0x5843cebd139cbaddc8cdde5623da74a30c06721734ea87e66d6532718aed7ac9).
- Exploit block confirmed on-chain: bsc block 106926103 at **2026-06-28 19:35:53 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 121,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token (burn-on-sell)**

### Actual logic and exploited mechanism

- Flaw class: **token burns from the AMM pair balance then re-syncs reserves**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): AIDC token on BSC was exploited due to a flaw in _sellTransfer()/burn logic. The attacker manipulated the PancakeSwap LP pool, causing burn fees to accumulate without properly deducting from sender balance, draining ~$121K WBNB.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/AIDC_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap AIDC/WBNB pair; repeated fresh helper sells

### Fork / codebase lineage

- hand-rolled BSC deflationary token

### Observable pre-hack flags

- ONE DAY old at exploit; burn-from-pair logic in _transfer

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 51. Lixir Finance — 2026-06-25

**SlowMist line:** Smart Contract Vulnerability · $ 12,300 · [reference](https://x.com/DefimonAlerts/status/2070362661691207935)

**Classification:** Ethereum: Lixir vault-token permit accepts a dummy signature (only checks ecrecover != 0)

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault tok | [`0xfD4c9a491DD777b8b3e13659e9E379252eC78390`](https://etherscan.io/address/0xfD4c9a491DD777b8b3e13659e9E379252eC78390) | mainnet | **NO** | impl `0x2ce186c52cf150000bf8ad2b4679d4ad619395cd` |
| exploited vault tok | [`0x49bba4C5C4F8a2D444Ca5fDA1b3137D94Df40465`](https://etherscan.io/address/0x49bba4C5C4F8a2D444Ca5fDA1b3137D94Df40465) | mainnet | **NO** | impl `0x2ce186c52cf150000bf8ad2b4679d4ad619395cd` |

### Age at time of hack

- **exploited vault tok** `0xfD4c9a491D...` created **2021-07-20 12:42:47 UTC**, exploited 2026-06-25 -> **dwell 1800 days (4.93 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x2f50bb2c98768d59...`](https://etherscan.io/tx/0x2f50bb2c98768d5938a702b9fd2325cc7236ccabb9a23f0675a6cf687b4de645).

- **exploited vault tok** `0x49bba4C5C4...` created **2021-07-20 12:42:55 UTC**, exploited 2026-06-25 -> **dwell 1800 days (4.93 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x1f6cbd21d37e03c7...`](https://etherscan.io/tx/0x1f6cbd21d37e03c707b4c79d43cf6864ad2baa3d2aad2bb6dd03ab605026b831).
- Exploit block confirmed on-chain: mainnet block 25391315 at **2026-06-25 01:21:11 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 12,300; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **LP-wrapper vault tokens (UniV3)**

### Actual logic and exploited mechanism

- Flaw class: **signature-validation bypass in EIP-2612 permit (only checks ecrecover != 0)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Lixir Finance's vault tokens (lv_* wrappers over Uniswap V3 LP positions) were exploited due to a broken EIP-2612 permit signature verification. The attacker reused a single dummy signature to bypass checks, granting approval to their contract over dozens of holders' tokens, then drained underlying assets (WETH, USDC, USDT, LIX) via withdrawFrom/withdrawETHFrom, resulting in ~$12,300 loss.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/LixirPermitDrain_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Uniswap V3 positions under lv_* wrappers; Uniswap for the exit

### Fork / codebase lineage

- Lixir Finance codebase (2021)

### Observable pre-hack flags

- 4.93y old abandoned vaults still holding holder balances; broken permit

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 59. LABUBU/OLPC — 2026-06-20

**SlowMist line:** Smart Contract Vulnerability · $ 1,100,000 · [reference](https://x.com/PeckShieldAlert/status/2068314444422402515)

**Classification:** BSC: OLPC _update() burns pair balance and desyncs reserves; owner had set an absurd decimalsValue 46d earlier

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0x58815cdf9955121a6274680ab396a36fc9e00000`](https://bscscan.com/address/0x58815cdf9955121a6274680ab396a36fc9e00000) | bsc | yes | no |

### Age at time of hack

- **exploited token** `0x58815cdf99...` created **2026-04-30 15:01:46 UTC**, exploited 2026-06-20 -> **dwell 50 days (0.14 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xee6839a2f2f9fdb2...`](https://bscscan.com/tx/0xee6839a2f2f9fdb238df3fd1e2115a423a3c9f0f300c11fe0f8689979c389490).
- Exploit block confirmed on-chain: bsc block 105326392 at **2026-06-20 11:31:03 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Drained the OLPC/LABUBU PancakeSwap pair; ~1,115,903.66 USDT realised after routing.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **config value already incoherent + burn-from-pair desync**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The OLPC/LABUBU liquidity pool on PancakeSwap V2 (BNB Chain) was exploited, resulting in approximately $1.1 million in losses. The attacker exploited a logic vulnerability in the OLPC token contract’s _update function. Approximately 46 days prior, the OLPC owner had maliciously changed the decimalsValue parameter to an extremely large value (7326680472586200649) and later renounced ownership. A small OLPC transfer triggered massive burns of OLPC and LABUBU tokens from the pool (to the dead address), desynchronizing the pair’s cached reserves. This allowed the attacker to drain a large amount of LABUBU, which was swapped through intermediate pools for ~1.115 million USDT. Funds were bridged to Ethereum and deposited into Tornado Cash.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/OLPC_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap OLPC/LABUBU pair; intermediate pools to USDT; bridged to Ethereum then Tornado Cash

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: owner set decimalsValue = 7326680472586200649 at block 96479712 (2026-05-05) then renounced ownership — an absurd on-chain config live for 46 days

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 62. JB — 2026-06-19

**SlowMist line:** Flashloan Price Manipulation · $ 50,000 · [reference](https://defillama.com/hacks)

**Classification:** BSC: JB helper uses live JB balance to sell/burn/sync through the JB/USDT pair

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited contract | [`0x1b5732eb98911c25acf7bdfaffb9409782cae6d7`](https://bscscan.com/address/0x1b5732eb98911c25acf7bdfaffb9409782cae6d7) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited contract** `0x1b5732eb98...` created **2026-06-18 09:08:36 UTC**, exploited 2026-06-19 -> **dwell 0 days (0.00 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xc97092ddfbcf0122...`](https://bscscan.com/tx/0xc97092ddfbcf012259d5f086e941ce9b726fcddbe04641f55c612965e660f0d1).
- Exploit block confirmed on-chain: bsc block 104980466 at **2026-06-18 16:15:56 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 50,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token/helper**

### Actual logic and exploited mechanism

- Flaw class: **live-balance-driven sell/burn/sync against its own pair**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The JB DeFi protocol suffered an exploit involving flashloan and price manipulation, resulting in approximately $50,000 being drained. The attack exploited protocol logic through flash loan-enabled price manipulation on the Solidity-based contract.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/JB_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Venus (collateral+borrow), flash-borrowed WBNB, JB/USDT Pancake pair

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- ONE DAY old at exploit; unverified helper

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 63. Aztec Bridge — 2026-06-17

**SlowMist line:** Smart Contract Vulnerability · $ 2,160,000 · [reference](https://x.com/aztecFND/status/2067511967237939636)

**Classification:** Ethereum: Aztec RollupProcessorV2 immutable escape hatch publishes an unconstrained proof_id

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited bridge | [`0x737901bea3eeb88459df9ef1BE8fF3Ae1B42A2ba`](https://etherscan.io/address/0x737901bea3eeb88459df9ef1BE8fF3Ae1B42A2ba) | mainnet | yes (`RollupProcessor`) | no |

### Age at time of hack

- **exploited bridge** `0x737901bea3...` created **2021-03-03 19:27:16 UTC**, exploited 2026-06-17 -> **dwell 1931 days (5.29 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x699eb365b1c79708...`](https://etherscan.io/tx/0x699eb365b1c797084d87ac685bd0276e1d5eed713fe95a0e1e2f2b0b99eb32bd).
- Exploit block confirmed on-chain: mainnet block 25339093 at **2026-06-17 18:34:35 UTC** (fetched via `eth_getBlockByNumber`).
- Exploit block confirmed on-chain: mainnet block 25339168 at **2026-06-17 18:49:35 UTC** (fetched via `eth_getBlockByNumber`).
- Exploit block confirmed on-chain: mainnet block 25339171 at **2026-06-17 18:50:11 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- **Independently verified on-chain by this study**: RollupProcessorV2 ETH balance 1,158.7598 -> 0.7598 ETH across block 25339093, i.e. -1,158 ETH, plus 150,000 DAI and 0.47 renBTC per the write-ups.

### What it was supposed to do

- Category: **rollup bridge (deprecated, immutable)**

### Actual logic and exploited mechanism

- Flaw class: **unconstrained public input (proof_id) in the escape-hatch circuit**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): On June 17, 2026, attackers exploited Aztec’s deprecated Private Rollup Bridge (launched in 2021 and shut down in 2022). They abused an immutable escape-hatch function that lacked proper ownership checks, using manipulated or fake rollup proofs to withdraw assets without corresponding deposits. Approximately $2.16 million (1,158 ETH, 150,000 DAI, and 0.47 renBTC) was drained. Aztec Labs confirmed the affected contract is unrelated to the current Aztec Network or the AZTEC ERC-20 token and that they have no control over the immutable old contracts.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/AztecEscapeHatch_exp.sol / _exp2.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- RollupProcessorV2 + verifier + DAI vault; escape hatch open windows

### Fork / codebase lineage

- Aztec Connect codebase

### Observable pre-hack flags

- 5.29y old, deprecated 2022, team explicitly has no control, still held 1,158 ETH

### Prior review status

- Aztec Labs state publicly that the contracts are immutable and outside their control; a whitehat reproduction (`AztecEscapeHatch_exp2.sol`) was published for the escape-hatch flaw.

---

## 64. Little Boy Plus — 2026-06-17

**SlowMist line:** Smart Contract Vulnerability · $ 367,000 · [reference](https://x.com/SlowMist_Team/status/2067424733747122259)

**Classification:** BSC: LBPHashrate._update() reachable via zero-value transferFrom, mints reward into the pair

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited contract | [`0x88886f0fd371dff856291badced45922bc888888`](https://bscscan.com/address/0x88886f0fd371dff856291badced45922bc888888) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited contract** `0x88886f0fd3...` created **2026-05-07 01:57:51 UTC**, exploited 2026-06-17 -> **dwell 40 days (0.11 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xc34d13f2af2d1a8b...`](https://bscscan.com/tx/0xc34d13f2af2d1a8baab78f197d9b7719d767ca7b5504a9ead039c60f4b72af13).
- Exploit block confirmed on-chain: bsc block 104727183 at **2026-06-17 08:35:38 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 367,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **mining/hashrate reward protocol**

### Actual logic and exploited mechanism

- Flaw class: **reward path reachable via zero-value transferFrom; mints into the pair without sync**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): On June 17, 2026, Little Boy Plus — a fully decentralized DeFi mining protocol on BSC claiming “no team, no admin keys” — was exploited. An attacker exploited a logic vulnerability in the LBPHashrate contract’s _update() function. By triggering it with a zero-value transferFrom call (bypassing OpenZeppelin authorization), the attacker unauthorizedly called _harvest and minted LBP tokens directly to the PancakeSwap LBP/USDT pair via mintReward. This inflated the pair’s balance without updating reserves, allowing the attacker to drain ~377,642 USDT (~$367k–$378k) through PancakePair.swap(). The funds were later sent to Tornado Cash.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/LBP_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap LBP/USDT pair, Moolah + Pancake Vault flash liquidity

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 40d old, marketed as "no team, no admin keys", mintReward into the pair

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 65. DIP — 2026-06-17

**SlowMist line:** Smart Contract Vulnerability · $ 111,000 · [reference](https://x.com/SlowMist_Team/status/2067078816514908286)

**Classification:** BSC: DIP _transfer() missing return for router-routed trades causes double transfer

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0x6c60bf5db0670ae94489d3dde2c60f271625db50`](https://bscscan.com/address/0x6c60bf5db0670ae94489d3dde2c60f271625db50) | bsc | yes | no |

### Age at time of hack

- **exploited token** `0x6c60bf5db0...` created **2026-06-16 06:10:50 UTC**, exploited 2026-06-17 -> **dwell 0 days (0.00 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x9502969628b8ce0c...`](https://bscscan.com/tx/0x9502969628b8ce0c25caf1f98542d89a040ee558f80a181e6f6f8c21ee42116e).
- Exploit block confirmed on-chain: bsc block 104598278 at **2026-06-16 16:28:37 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 111,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **missing return statement causes double transfer on router-routed trades**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The DIP token contract (Etherisc ecosystem) was exploited due to a missing return statement in the _transfer() function for PancakeSwap-routed trades, causing double transfers. The attacker used skim(router) and sync() to manipulate the pool and drain ~$111K USDC.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/DIP_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap DIP/AIC pair, skim()/sync(), flash-swap

### Fork / codebase lineage

- hand-rolled (Etherisc-ecosystem branded)

### Observable pre-hack flags

- ONE DAY old at exploit

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 66. Thetanuts Finance — 2026-06-15

**SlowMist line:** Smart Contract Vulnerability · $ 105,000 · [reference](https://x.com/ThetanutsFi/status/2066795181123543070)

**Classification:** Ethereum: Thetanuts legacy index vault mint/claim redemption math with zeroed component transfers

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault | [`0xc2c3ae0a7b405058558c9b4a63b373486cb86ac7`](https://etherscan.io/address/0xc2c3ae0a7b405058558c9b4a63b373486cb86ac7) | mainnet | **NO** | no |

### Age at time of hack

- **exploited vault** `0xc2c3ae0a7b...` created **2022-04-27 21:04:56 UTC**, exploited 2026-06-15 -> **dwell 1509 days (4.13 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x5fe942c5d09bd3b4...`](https://etherscan.io/tx/0x5fe942c5d09bd3b427c5d8c0ecabd0d2468d4452b0b7f32f87ca358c0c997132).
- Exploit block confirmed on-chain: mainnet block 25323328 at **2026-06-15 13:53:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 105,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **options index vault (legacy)**

### Actual logic and exploited mechanism

- Flaw class: **redemption math with zeroed component transfer amounts**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): A legacy vault of Thetanuts Finance on Ethereum was exploited due to a flaw in redemption math and integer calculations in the mint/claim functions. The attacker used flash loans to drain approximately $2.1 million after reducing token supply to near zero. A whitehat recovered most funds (~$2M), resulting in a net loss of around $105K according to the project. Current products and active contracts were unaffected.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/Thetanuts_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Aave flash loan of index-vault shares, component vaults

### Fork / codebase lineage

- Thetanuts codebase

### Observable pre-hack flags

- 4.13y old legacy vault, still redeemable

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 67. Aztec Connect — 2026-06-14

**SlowMist line:** Smart Contract Vulnerability · $ 2,100,000 · [reference](https://x.com/AztecLabs_/status/2066175340926345555)

**Classification:** Ethereum: Aztec Connect Decoder numRealTxs proven-vs-settled mismatch; processRollup permissionless

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited bridge | [`0xFF1F2B4ADb9dF6FC8eAFecDcbF96A2B351680455`](https://etherscan.io/address/0xFF1F2B4ADb9dF6FC8eAFecDcbF96A2B351680455) | mainnet | yes (`TransparentUpgradeableProxy`) | impl `0x7d657ddcf7e2a5fd118dc8a6ddc3dc308adc2728` |

### Age at time of hack

- **exploited bridge** `0xFF1F2B4ADb...` created **2022-06-07 21:43:14 UTC**, exploited 2026-06-14 -> **dwell 1467 days (4.02 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x837765f53d9ae32b...`](https://etherscan.io/tx/0x837765f53d9ae32bf1b507fec696052d3ee2a245515dccebc13b3717bc987921).
- Exploit block confirmed on-chain: mainnet block 25300000 at **2026-06-12 07:49:35 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- **Independently verified on-chain by this study**: RollupProcessorV3 ETH balance 908.9873 -> 0.0000 ETH across block 25315715. Plus DAI/wstETH/yvDAI/yvWETH/LUSD/yvLUSD legs (~$2.19M total).

### What it was supposed to do

- Category: **rollup bridge (deprecated, immutable)**

### Actual logic and exploited mechanism

- Flaw class: **proven-vs-settled mismatch (numRealTxs outside the hashed header)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): An attacker exploited a vulnerability in the incomplete proof verification logic of the deprecated Aztec Connect Router contract on Ethereum, draining approximately $2.1 million in assets. The protocol had been deprecated for three years with no team control over the immutable contract. The current Aztec Network and AZTEC token were unaffected.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/AztecConnect_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Decoder/RollupProcessorV3, permissionless processRollup after the provider gate was removed for sunset

### Fork / codebase lineage

- Aztec Connect codebase

### Observable pre-hack flags

- 4.02y old, deprecated 3 years, immutable, still held 908.99 ETH + DAI + wstETH + yv assets

### Prior review status

- Deprecated for three years with the team having no control over the immutable contract.

---

## 71. Asterix Labs — 2026-06-09

**SlowMist line:** Smart Contract Vulnerability · $ 40,000 · [reference](https://x.com/asterixlabs/status/2063916673724555336)

**Classification:** DN404/BT404 shared-codebase ownership/underflow flaw in an Asterix fork of Flooring

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 40,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **NFT-liquidity token (DN404/BT404)**

### Actual logic and exploited mechanism

- Flaw class: **shared-codebase packed-ownership/underflow flaw**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Asterix Labs (a fork of the Flooring Protocol NFT liquidity platform) suffered an exploit targeting its $ASTX token contract. Attackers drained approximately $40,000 by exploiting a smart contract vulnerability in the shared DN404/BT404 token standard codebase—the same flaw used in the Flooring Protocol attack the previous day. The project team immediately acknowledged the incident on X and stated they are investigating, with a full post-mortem to follow.

### Interaction graph

- Uniswap V4 pool for ASTX; same flaw as Flooring the previous day

### Fork / codebase lineage

- DIRECT FORK of Flooring Protocol (BT404/DN404 family)

### Observable pre-hack flags

- clone-family membership: parent hacked ONE DAY earlier and the fork was not patched

### Prior review status

- Inherited the flaw from Flooring Protocol, which was exploited **one day earlier**. The public disclosure of the parent hack was itself the warning.

---

## 73. NovaBox — 2026-06-09

**SlowMist line:** Flash Loan Attack · $ 93,600 · [reference](https://x.com/f12sec/status/2064610827554922679)

**Classification:** Ethereum: NovaBox adds dual depositors to the dividend list without initialising checkpoints

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited pool | [`0xbc4191167d4b0251cab5201a527daa8a7d3846b0`](https://etherscan.io/address/0xbc4191167d4b0251cab5201a527daa8a7d3846b0) | mainnet | yes (`NovaBox`) | no |

### Age at time of hack

- **exploited pool** `0xbc4191167d...` created **2018-10-11 14:15:44 UTC**, exploited 2026-06-09 -> **dwell 2797 days (7.66 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x53b96d5853a7adbd...`](https://etherscan.io/tx/0x53b96d5853a7adbdb14bb1aa0b04214f30a0ec0c339bb50347db2401f975da02).
- Exploit block confirmed on-chain: mainnet block 25281767 at **2026-06-09 18:48:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- **Independently verified on-chain by this study**: NovaBox ETH balance 65.1130 -> 0.0904 ETH across block 25281767 (-65.02 ETH, 99.86% of the pool).

### What it was supposed to do

- Category: **dividend/reward pool**

### Actual logic and exploited mechanism

- Flaw class: **dividend checkpoints not initialised for new dual depositors**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The NovaBox platform’s reward pool on Ethereum was hacked. The attacker borrowed 427.5 WETH via an Aave V3 flash loan and exploited a flaw in the reward distribution mechanism (dividends distributed before balance updates on deposits/withdrawals). By first depositing a small amount of NOVA tokens to trigger dividend calculation and then a large ETH deposit to inflate their actual share—while the system still calculated based on the old small share—they generated approximately 145.82 ETH in “phantom dividends,” draining the pool from 65.11 ETH to 0.09 ETH (99.86% loss) in a single transaction. Security firm F12 confirmed it was not a smart contract vulnerability but a flaw in the reward mechanism logic.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/NovaBox_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Aave V3 flash loan (427.5 WETH); NOVA token; extcodesize guard bypassed via constructor

### Fork / codebase lineage

- hand-rolled 2018-era dividend contract

### Observable pre-hack flags

- 7.66y old (created 2018-10-11), verified, still held 65.11 ETH

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 74. Token of Power — 2026-06-09 *(borderline)*

**SlowMist line:** Malicious Governance Takeover · $ 1,580,000 · [reference](https://crypto.news/token-of-power-exploit-drains-1-58m-from-balancer-pool/)

**Classification:** Ethereum: Aragon DAO with 16,384 TOP supply and no timelock; mint proposal created+voted+executed in one tx

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| governance impl | [`0xb935c3d80229d5d92f3761b17cd81dc2610e3a45`](https://etherscan.io/address/0xb935c3d80229d5d92f3761b17cd81dc2610e3a45) | mainnet | yes (`Voting`) | no |
| **->** governance proxy | [`0xb501d26ba74eab601576b62617cf41042bef6865`](https://etherscan.io/address/0xb501d26ba74eab601576b62617cf41042bef6865) | mainnet | yes (`AppProxyUpgradeable`) | no |
| drained pool | [`0x0fa3e014fa2e751f78e53dca766fac2223327329`](https://etherscan.io/address/0x0fa3e014fa2e751f78e53dca766fac2223327329) | mainnet | yes (`BPool`) | no |

### Age at time of hack

- **governance impl** `0xb935c3d802...` created **2019-04-17 15:49:03 UTC**, exploited 2026-06-09 -> **dwell 2609 days (7.14 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xdfc9c0fee3f6e8f2...`](https://etherscan.io/tx/0xdfc9c0fee3f6e8f20f7bb6597a78831414fe9596d96025f331eb4e3e4ec30507).

- **governance proxy** `0xb501d26ba7...` created **2021-03-09 09:14:54 UTC**, exploited 2026-06-09 -> **dwell 1917 days (5.25 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x668d501cf1daef84...`](https://etherscan.io/tx/0x668d501cf1daef84e1a253095fb891acbce7afeff4b7d190dea0551b073bb1e6).

- **drained pool** `0x0fa3e014fa...` created **2021-03-14 18:23:09 UTC**, exploited 2026-06-09 -> **dwell 1912 days (5.23 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xb32f433d8d82b5f6...`](https://etherscan.io/tx/0xb32f433d8d82b5f681d0b580a4fc6932147d6d1ead37232f33ccd002c25a9b51).
- Exploit block confirmed on-chain: mainnet block 25279891 at **2026-06-09 12:32:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Drained the TOP/WETH Balancer V1 BPool of 944.20 WETH; the DAO itself controlled TOP minting against a 16,384-token supply.

### What it was supposed to do

- Category: **DAO governance + AMM pool**

### Actual logic and exploited mechanism

- Flaw class: **governance capture with no timelock (propose+vote+execute in one tx)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Token of Power (TOP) suffered a governance takeover exploit due to misconfiguration in its Aragon DAO (no timelock). The attacker used funds from Tornado Cash to acquire majority voting power (>50% of the small 16,384 TOP supply), passed a malicious proposal in a single transaction to mint billions of new TOP tokens, and drained 944.2 WETH (~$1.58M) from the TOP/WETH Balancer V1 liquidity pool. Balancer protocol itself was not exploited.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/TOPBPool_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Aragon Voting/TokenManager proxies (2019 base impls), Balancer V1 BPool TOP/WETH; Tornado Cash funding

### Fork / codebase lineage

- Aragon DAO template

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: total supply 16,384 TOP, attacker held 8,192.000001, no timelock — all readable on-chain

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 76. Flooring Protocol & BitmapPunks — 2026-06-08

**SlowMist line:** Smart Contract Vulnerability · - · [reference](https://x.com/mfigge/status/2063782936399544740)

**Classification:** Ethereum: Flooring V2 / BT404 packed-ownership alias + underflow mints near-infinite fpTokens

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is -; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **NFT-liquidity protocol (BT404)**

### Actual logic and exploited mechanism

- Flaw class: **packed-ownership alias + unchecked underflow -> near-infinite mint**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Flooring Protocol V2 and BitmapPunks (BT404 / $BMP) were exploited due to a BT404-style packed ownership logic vulnerability (malicious high-bit token ID alias + unchecked integer underflow). The attacker minted near-infinite fpTokens/$BMP with a dust amount of WETH, drained liquidity pools, and extracted high-value NFTs (e.g., BAYC, CryptoPunks) at low cost. Yuga Labs quickly intervened with a white-hat operation via GrailsOTC, rescuing 68 NFTs worth over $500,000, now held safely for return after fixes.

### Interaction graph

- fpToken pools, NFT vaults holding BAYC/CryptoPunks; Uniswap pools

### Fork / codebase lineage

- BT404/DN404 codebase (parent of the Asterix fork)

### Observable pre-hack flags

- hybrid ERC20/ERC721 shared-storage standard with prior audit warnings about balance/state misalignment

### Prior review status

- Prior audits of the DN404/BT404 hybrid standard had already flagged the risk of ERC-20 balance vs ERC-721 state misalignment; the flaw class was publicly known before this incident.

---

## 77. Ambient Finance — 2026-06-08

**SlowMist line:** Smart Contract Vulnerability · $ 110,600 · [reference](https://www.cryptotimes.io/2026/06/08/ethereum-defi-protocol-ambient-finance-suffers-110k-drain/)

**Classification:** Ethereum: Ambient surplus-collateral accounting across HotProxy/WarmPath/ColdPath

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited dex | [`0xAaAaAAAaA24eEeb8d57D431224f73832bC34f688`](https://etherscan.io/address/0xAaAaAAAaA24eEeb8d57D431224f73832bC34f688) | mainnet | yes (`CrocSwapDex`) | no |

### Age at time of hack

- **exploited dex** `0xAaAaAAAaA2...` created **2023-05-29 02:25:11 UTC**, exploited 2026-06-08 -> **dwell 1105 days (3.03 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x11f2acc5882e7a69...`](https://etherscan.io/tx/0x11f2acc5882e7a6903bcbb39d1af7cd6cad99afd7e421197f48a537ae73a7f3a).
- Exploit block confirmed on-chain: mainnet block 25266404 at **2026-06-07 15:26:23 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 110,600; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **monolithic DEX**

### Actual logic and exploited mechanism

- Flaw class: **surplus-collateral accounting flaw across proxy sidecars**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Ambient Finance (formerly CrocSwap) was exploited via an accounting logic flaw in surplus collateral handling. The attacker used a flash loan and rapid cycling through HotProxy/WarmPath/ColdPath operations to drain ~83.72 ETH (~$110.6K) from the protocol’s monolithic smart contract.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/AmbientCrocSwapDex_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Balancer flash loan; ETH/USDC pool; HotProxy/WarmPath/ColdPath sidecars

### Fork / codebase lineage

- Ambient/CrocSwap codebase

### Observable pre-hack flags

- 3.03y old, monolithic contract with multiple delegatecall sidecars sharing accounting state

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 79. DTXT/USDT liquidity pair on BSC — 2026-06-05

**SlowMist line:** Business Logic Vulnerability · $ 35,041 · [reference](https://x.com/SlowMist_Team/status/2062876917045608594)

**Classification:** BSC: DTXT forgeable add-liquidity detection bypasses sell fees

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0xac9bf7c320d4ce2d0ac978b83955dd67351897d2`](https://bscscan.com/address/0xac9bf7c320d4ce2d0ac978b83955dd67351897d2) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited token** `0xac9bf7c320...` created **2026-06-04 16:24:37 UTC**, exploited 2026-06-05 -> **dwell 0 days (0.00 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x0bc8bb0b9ef1a05c...`](https://bscscan.com/tx/0x0bc8bb0b9ef1a05ce4205676bfa3317be1b4b630216a7720796748bc72e421f8).
- Exploit block confirmed on-chain: bsc block 102432239 at **2026-06-05 09:28:06 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 35,041; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **forgeable add-liquidity detection bypasses sell fees**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The DTXT/USDT liquidity pair on BSC was exploited. The attacker exploited a forgeable liquidity-addition detection logic in the DTXT contract (by sending a small amount of USDT directly to the pair address, tricking the contract into classifying large sells as liquidity additions). This bypassed sell fees and drained the pool, resulting in a loss of approximately $35,041 USDT.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/DTXT_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap DTXT/USDT pair, Moolah flash loan, 1-wei USDT donation to the pair

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- ONE DAY old at exploit

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 80. ATM — 2026-06-04

**SlowMist line:** Smart Contract Vulnerability · $ 243,500 · [reference](https://x.com/TenArmorAlert/status/2062351507056460166)

**Classification:** BSC: ATMToken._transfer() auto-dumps 20% of its own reserves at amountOutMin=0; per-address guards farmable

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0x986058ec93756E57b4e55b406dD0BeE24bcD95e3`](https://bscscan.com/address/0x986058ec93756E57b4e55b406dD0BeE24bcD95e3) | bsc | yes | no |

### Age at time of hack

- **exploited token** `0x986058ec93...` created **2026-01-01 15:08:06 UTC**, exploited 2026-06-04 -> **dwell 153 days (0.42 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x66396590e88b058a...`](https://bscscan.com/tx/0x66396590e88b058a7eae52cec85afb8ac6a3e98987d5b4b8a98bd88c9729eed2).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 243,500; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token with auto-swap treasury**

### Actual logic and exploited mechanism

- Flaw class: **contract auto-dumps 20% of its own reserves at min-out 0; per-address guards farmable**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The ATM token on BSC was exploited due to a flaw in its custom transferFrom() function logic (which automatically swapped ~20% of transferred amounts to BSC-USD). The attacker repeatedly triggered the mechanism to drain approximately $243,500 from the protocol.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/ATM_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap ATM/USDT pair; 30 CREATE2 farmer clones

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 153d old, Sourcify-verified source shows swapAtAmount/numTokensSellRate and per-sender anti-whale guards

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 81. BYToken — 2026-06-04

**SlowMist line:** Smart Contract Vulnerability · $ 87,402 · [reference](https://x.com/TenArmorAlert/status/2062708160700322257)

**Classification:** BSC: permissionless triggerAutoBurn() burns from the pair then sync()s reserves

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0x6f50cffEcd4e00EcF7E442774C08c089450B62Ca`](https://bscscan.com/address/0x6f50cffEcd4e00EcF7E442774C08c089450B62Ca) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited token** `0x6f50cffEcd...` created **2026-06-03 20:38:09 UTC**, exploited 2026-06-04 -> **dwell 0 days (0.00 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xf961d6266aac7fcd...`](https://bscscan.com/tx/0xf961d6266aac7fcd7d595ab0d96721c03fc8b09f2726d477cd5508af9e3ac09c).
- Exploit block confirmed on-chain: bsc block 102329719 at **2026-06-04 20:38:09 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 87,402; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **permissionless maintenance function burns from the pair then sync()s**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The public triggerAutoBurn() maintenance function in BYToken contract on BSC was abused. The attacker took a Moolah flashloan (~422k WBNB), performed Pancake swaps, then called the unprivileged function. This burned ~67.8 quadrillion BY directly from the BY/WBNB pair and called pair.sync(), rewriting reserves to 1 BY + full WBNB. The extreme skew allowed massive BY sells to drain nearly all WBNB liquidity, netting the attacker ~146.60 BNB ($87,402).

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-06/BYToken_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap BY/WBNB pair; Moolah flash loan (~422k WBNB)

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- ONE DAY old at exploit; public triggerAutoBurn()

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 82. ApeBond — 2026-06-03

**SlowMist line:** Smart Contract Vulnerability · $ 3,421 · [reference](https://x.com/clarahacks/status/2062564868130029636)

**Classification:** BSC: ApeYieldVault.migrateToVotingEscrow accepts duplicate pool IDs, inflating the lock

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 3,421; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **bond/yield vault**

### Actual logic and exploited mechanism

- Flaw class: **duplicate pool IDs inflate a lock amount**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): ApeBond's ApeYieldVault smart contract on BSC was exploited. The attacker used a public helper contract to call migrateToVotingEscrow with duplicate pool IDs, inflating a lock amount from ~1.71 quadrillion ABOND to ~29 quadrillion ABOND. They then unlocked, claimed the inflated lock, sold ABOND in the public ABOND/WBNB pool, repaid a Moolah flashloan, and kept ~5.72 WBNB profit. The entire flow was permissionless and on-chain.

### Interaction graph

- public helper contract, ABOND/WBNB Pancake pool, Moolah flash loan

### Fork / codebase lineage

- ApeSwap/ApeBond codebase

### Observable pre-hack flags

- migration function callable permissionlessly with caller-supplied pool ID array

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 86. ATOHook — 2026-06-01

**SlowMist line:** Smart Contract Vulnerability · $ 25,000 · [reference](https://x.com/SlowMist_Team/status/2063576945552462201)

**Classification:** Storage-slot collision between a rewards mapping and Solady ReentrancyGuard fixed slot in getReward()

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 25,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **reward hook**

### Actual logic and exploited mechanism

- Flaw class: **storage-slot collision (rewards mapping vs Solady ReentrancyGuard fixed slot)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): ATOHook smart contract was exploited due to a storage slot collision between the rewards mapping and Solady’s fixed ReentrancyGuard slot. The nonReentrant modifier in getReward() wrote a sentinel value that was misinterpreted as a reward balance for a colliding address, allowing the attacker to repeatedly claim and drain a fixed amount of ETH (200 times), stealing approximately 14.41 ETH.

### Interaction graph

- getReward() payout in ETH

### Fork / codebase lineage

- uses Solady library

### Observable pre-hack flags

- library fixed-slot collision — detectable statically by comparing mapping slots against known library slots

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 91. AROS — 2026-05-30

**SlowMist line:** Smart Contract Vulnerability · $ 295,300 · [reference](https://x.com/TenArmorAlert/status/2061289921990570349)

**Classification:** BSC: AROS token/pool logic drained via the AROS/USDT Pancake pair

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited contract | [`0xFEC7D27525cC4efDe5b785EEb5E37Df90E9cd1d5`](https://bscscan.com/address/0xFEC7D27525cC4efDe5b785EEb5E37Df90E9cd1d5) | bsc | not in Sourcify (BscScan status not checkable — see Method) | impl `0x54b51e0bf84d53bfa7053d2546a3edc182a86bb7` |

### Age at time of hack

- **exploited contract** `0xFEC7D27525...` created **2026-05-26 13:27:26 UTC**, exploited 2026-05-30 -> **dwell 3 days (0.01 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x875b55c6c3c70fac...`](https://bscscan.com/tx/0x875b55c6c3c70facb270ac3e3b8f781bd50ab8f8e44f31c1c8bec16008632fba).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 295,300; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token/pool**

### Actual logic and exploited mechanism

- Flaw class: **reserve manipulation via the AROS/USDT pair**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The DeFi project AROS on BSC was exploited. The attacker interacted with the AROS/USDT PancakeSwap liquidity pool and drained approximately $295.3K USDT.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/AROS_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap AROS/USDT pair

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 3 days old at exploit

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 92. MoneyMon — 2026-05-29

**SlowMist line:** Smart Contract Vulnerability · $ 85,519.47 · [reference](https://x.com/SlowMist_Team/status/2060205558687486441)

**Classification:** BSC: cliamRewred() verify() accepts ecrecover==address(0) against a zeroed admin

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited nft/claim | [`0x92D60629FF5d53a0098B51E9b1D59546D1D8e5B6`](https://bscscan.com/address/0x92D60629FF5d53a0098B51E9b1D59546D1D8e5B6) | bsc | yes | no |

### Age at time of hack

- **exploited nft/claim** `0x92D60629FF...` created **2026-02-23 06:38:34 UTC**, exploited 2026-05-29 -> **dwell 94 days (0.26 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xe055b08f1972a599...`](https://bscscan.com/tx/0xe055b08f1972a5993150bc812c9718a1a9b8e8cab0c52ea3301f23b4036aa146).
- Exploit block confirmed on-chain: bsc block 100937039 at **2026-05-28 14:16:32 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 85,519.47; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **NFT reward claim**

### Actual logic and exploited mechanism

- Flaw class: **signature-validation bypass (ecrecover==address(0) equals a zeroed admin)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The LegendaryMoneyMonNft contract’s cliamRewred function had a signature verification flaw. The verify() only checked if recoverSigner(...) == admin, without properly validating cases where ecrecover returns address(0). The attacker set admin to zero address, then used an invalid signature (r=0, s=0, v=27) to bypass checks, arbitrarily claim rewards, drain all tokens from the contract, and swap them for USDT via PancakeSwap.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/LegendaryMoneyMonNft_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap MON/USDT for the exit; EIP-7702 packaging

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: changeadmin() had already set admin = address(0) on-chain; misspelled function name cliamRewred

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 93. YSDAO — 2026-05-29

**SlowMist line:** Reserve Manipulation Attack · $ 19,500 · [reference](https://x.com/TenArmorAlert/status/2061278221497254013)

**Classification:** BSC: YSDAO Staking.sync() has no access control; add/remove-liquidity detection is forgeable

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| exploited token | [`0xc036A13D7A6A84677DfCcec483eED124654B7918`](https://bscscan.com/address/0xc036A13D7A6A84677DfCcec483eED124654B7918) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |
| **->** exploited staking | [`0x3E13019dA3BAAd134493e751704D2D4245Eec7CA`](https://bscscan.com/address/0x3E13019dA3BAAd134493e751704D2D4245Eec7CA) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited token** `0xc036A13D7A...` created **2025-10-21 10:28:48 UTC**, exploited 2026-05-29 -> **dwell 219 days (0.60 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xcf1033b5a5e88944...`](https://bscscan.com/tx/0xcf1033b5a5e88944bb2f601ca69968f008d4efd0922125adb95e3a7558af6d7a).

- **exploited staking** `0x3E13019dA3...` created **2025-08-20 04:39:14 UTC**, exploited 2026-05-29 -> **dwell 281 days (0.77 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xa061053bc9d65ea6...`](https://bscscan.com/tx/0xa061053bc9d65ea66403f40bbb7f888f7293758ad84ac2cd9800ee2c38ad88b2).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 19,500; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token + staking**

### Actual logic and exploited mechanism

- Flaw class: **no access control on Staking.sync(); forgeable add/remove-liquidity detection**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Computility-associated YSDAO project on BSC suffered a liquidity pool attack on PancakeSwap V2. The hacker manipulated reserves via contract calls and extracted funds, resulting in approximately $19.5K loss.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/YSDAO_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap YSDAO/USDT pair + V3 USDT flash loan + V2 pair callback

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- token 219d / staking 281d old; permissionless sync() moves all staking USDT into the pair

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 94. Joe Agent — 2026-05-28

**SlowMist line:** Reentrancy Attack · $ 45,000 · [reference](https://x.com/SlowMist_Team/status/2059887450663551352)

**Classification:** BSC: removeLiquidityViaContract sends BNB before zeroing lpInfo — classic reentrancy

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited proxy | [`0xef0f12d08d66e76E1866e60F30a0DaA578e00c04`](https://bscscan.com/address/0xef0f12d08d66e76E1866e60F30a0DaA578e00c04) | bsc | yes | impl `0xb12ce0a21f67a9fc3c8ad1c7dbc4b017b7e67319` |
| implementation | [`0xb12ce0a21f67a9fc3c8ad1c7dbc4b017b7e67319`](https://bscscan.com/address/0xb12ce0a21f67a9fc3c8ad1c7dbc4b017b7e67319) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited proxy** `0xef0f12d08d...` created **2026-04-23 01:06:56 UTC**, exploited 2026-05-28 -> **dwell 34 days (0.09 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x22bbe8e14726f37c...`](https://bscscan.com/tx/0x22bbe8e14726f37c6fef773029a6b1c38f8e95f17bb0ed20fa48976b8d6a7ea5).

- **implementation** `0xb12ce0a21f...` created **2026-05-19 20:21:33 UTC**, exploited 2026-05-28 -> **dwell 8 days (0.02 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x39dadff746f5af55...`](https://bscscan.com/tx/0x39dadff746f5af55ff0d4f60dbb355d4ecf961df5255bc08f9d856fc1545dd8b).
- Exploit block confirmed on-chain: bsc block 100812531 at **2026-05-27 22:41:03 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Pooled depositor LP inside the token contract; 62.5 BNB + ~1,195,918 JOE drained against one ~437 LP position the attacker paid for once.

### What it was supposed to do

- Category: **agent token with LP custody**

### Actual logic and exploited mechanism

- Flaw class: **reentrancy (BNB sent before lpInfo is zeroed)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The Joe Agent ($JOE) project smart contract had a single-function reentrancy vulnerability. The attacker exploited the logic in _removeLiquidityViaContract where BNB was sent via low-level call before updating lpInfo[user].lpAmount, performing ~25 reentrancy loops to steal 62.5 BNB and ~1.196M JOE.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/JoeAgent_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap LP; ERC1967 proxy

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- implementation only 8 DAYS old at exploit (proxy 34d); classic CEI violation

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 95. DxSale — 2026-05-28 *(borderline)*

**SlowMist line:** Ownership Override Attack · $ 7,300,000 · [reference](https://x.com/eyeonchains/status/2060083479631843408)

**Classification:** BSC: undisclosed owner-only DXLOCKERLP backdoor in an unverified locker, but the actor held ownership

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited locker | [`0xEb3a9C56d963b971d320f889bE2fb8B59853e449`](https://bscscan.com/address/0xEb3a9C56d963b971d320f889bE2fb8B59853e449) | bsc | yes | no |

### Age at time of hack

- **exploited locker** `0xEb3a9C56d9...` created **2021-02-20 23:18:21 UTC**, exploited 2026-05-28 -> **dwell 1922 days (5.26 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x5f530c2547fc9584...`](https://bscscan.com/tx/0x5f530c2547fc958407d8cfb87ba9ad67cc79a112d390c88cf389933035e53158).
- Exploit block confirmed on-chain: bsc block 100806731 at **2026-05-27 21:57:32 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- 1,400+ LP positions locked since 2021, ~$7.3M — the locker's whole point was custody.

### What it was supposed to do

- Category: **liquidity locker (launchpad)**

### Actual logic and exploited mechanism

- Flaw class: **undisclosed owner-only backdoor defeating the advertised timelocks**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Legacy liquidity locker contracts of DxSale (a veteran DeFi launchpad on BNB Chain) were exploited, draining approximately $7.3 million from over 1,400 old LPs locked since 2021. The attacker used owner privileges via a custom drainer to set near-zero fees, backdate unlock times to 1970, and withdraw funds; on-chain links suggest possible team connections, with the platform remaining silent.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/DxSale_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- 1,400+ locked LP positions since 2021; EIP-7702 type-4 batch drainer

### Fork / codebase lineage

- DxSale codebase

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: unverified locker bytecode containing an undocumented DXLOCKERLP selector; ownership passed through 89 wallets over 269 days

### Prior review status

- Coinsult and others published analyses only after the fact; the locker source was never verified on BscScan.

---

## 96. ONTR — 2026-05-28

**SlowMist line:** Smart Contract Vulnerability · $ 98,200 · [reference](https://x.com/TenArmorAlert/status/2060190914547449936)

**Classification:** onlyOwner check accepts owner == address(0), letting anyone re-own a renounced token

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 98,200; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **onlyOwner accepts owner == address(0), re-owning a renounced token**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The ONTR token project was drained due to a flawed onlyOwner check in the contract (accepts owner == address(0)). This allowed re-owning a renounced token. The attacker used hidden balance-grant logic to fake massive ONTR balances (no totalSupply/mint logs), dumped into the ONTR/WETH LP, and swapped out WETH for profit.

### Interaction graph

- ONTR/WETH LP; hidden balance-grant logic with no mint events

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: renounced-owner token whose onlyOwner check admits address(0)

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 99. SKP — 2026-05-26 *(borderline)*

**SlowMist line:** Smart Contract Vulnerability · $ 212,850 · [reference](https://x.com/TenArmorAlert/status/2059454844201562191)

**Classification:** BSC: SKP _runSpecialPairFlow redistributes unbounded treasury to a whitelisted address the owner set 6d prior — insider-engineered

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0xecbdc0b76142740bb564b8aa1bcd061cb151a666`](https://bscscan.com/address/0xecbdc0b76142740bb564b8aa1bcd061cb151a666) | bsc | yes | no |

### Age at time of hack

- **exploited token** `0xecbdc0b761...` created **2026-05-22 04:36:32 UTC**, exploited 2026-05-26 -> **dwell 3 days (0.01 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x20b67e88f488f6b0...`](https://bscscan.com/tx/0x20b67e88f488f6b0746e54f0f50ca4ed2f4c9b8b1821cc6f9a055ec34b093d0c).
- Exploit block confirmed on-chain: bsc block 100582079 at **2026-05-26 17:47:44 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 212,850; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **unbounded treasury redistribution to an owner-set whitelisted address**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): On BSC, the SKP token suffered a token-side LP balance drain + sync attack. The attacker profited approximately $212.85k in a single transaction (162,854.21 USDT + 75.88 BNB). The root cause was a flaw in SKP token logic that allowed extra SKP tokens to be transferred out from the Pancake V2 SKP/USDT LP after a large buy, followed by calling sync() to write incorrect reserves, pushing the SKP reserve close to zero. The attacker used flash loans to amplify the attack.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/SKP_exp.sol / SKP_exp2.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap SKP/USDT pair; BlockRazor private mempool; deBridge exit

### Fork / codebase lineage

- hand-rolled disposable launcher

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: unverified source, WL address set by owner 6 days prior, deployer ran 7+ throwaway tokens, 14-day lifecycle

### Prior review status

- No audit. The DeFiHackLabs authors explicitly dispute SlowMist's 'smart contract vulnerability' framing and document owner-set preconditions.

---

## 100. WUSD.fi / GLOVE — 2026-05-25

**SlowMist line:** Sybil Attack · $ 200,000 · [reference](https://x.com/exvulsec/status/2058803971947385330)

**Classification:** Ethereum: WUSD._englove has no per-address claim ledger — Sybil-farmable uncapped subsidy

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited contract | [`0x068E3563b1c19590F822c0e13445c4FA1b9EEFa5`](https://etherscan.io/address/0x068E3563b1c19590F822c0e13445c4FA1b9EEFa5) | mainnet | yes (`WUSD`) | no |
| reward token | [`0x70c5f366db60a2a0c59c4c24754803ee47ed7284`](https://etherscan.io/address/0x70c5f366db60a2a0c59c4c24754803ee47ed7284) | mainnet | yes (`Glove`) | no |

### Age at time of hack

- **exploited contract** `0x068E3563b1...` created **2023-01-22 21:11:47 UTC**, exploited 2026-05-25 -> **dwell 1218 days (3.33 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x4562af1447c9159a...`](https://etherscan.io/tx/0x4562af1447c9159ac9cf345e27386b58f2b5c9fa445e03fb0114416524eecad9).

- **reward token** `0x70c5f366db...` created **2023-01-22 21:03:59 UTC**, exploited 2026-05-25 -> **dwell 1218 days (3.33 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x5f375741abbe61b4...`](https://etherscan.io/tx/0x5f375741abbe61b4533e97b79bdb37aaae9514ca7c1d62c6d274be7100f5345d).
- Exploit block confirmed on-chain: mainnet block 25170426 at **2026-05-25 06:07:59 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Drained the Uniswap V3 GLO/USDC and GLO/USDT pools, which held only ~1,040 GLO + ~$63K stables each. Realised ~11,702 USDC + 8,079 USDT per batch; the ~$200K figure is the campaign total.

### What it was supposed to do

- Category: **wrapped stablecoin with reward emission**

### Actual logic and exploited mechanism

- Flaw class: **uncapped subsidy with no per-address claim ledger (Sybil-farmable)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): WUSD.fi / GLOVE on Ethereum suffered an incentive abuse exploit. The attacker exploited the lack of Sybil resistance in the WUSD._englove reward path. By using EIP-7702 helper contracts and a Morpho USDT flash loan to repeatedly wrap/unwrap at least 100 WUSD (with fresh addresses holding <2 GLOVE), they harvested nearly 2 GLOVE per cycle, dumped the GLOVE into Uniswap V3 pools, and drained ~$200K in USDC/USDT from the liquidity pools.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/WUSD_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Uniswap V3 GLO/USDC and GLO/USDT pools (thin: ~1,040 GLO + ~$63K each); Morpho USDT flash loan; EIP-7702 helper contracts

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 3.33y old; eligibility depends only on the callers current GLOVE balance

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 101. Third-party Gnosis Safe Module (SquidRouterModule) — 2026-05-25

**SlowMist line:** Smart Contract Vulnerability · $ 3,200,000 · [reference](https://x.com/squidrouter/status/2058890710611276238)

**Classification:** Ethereum+Base: Safe module trusts a caller-supplied sourceAddress string on the permissionless Axelar express path

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited safe mod | [`0x1f1d37a3Bf840e35c6a860c7C2dA71Fe555123ca`](https://etherscan.io/address/0x1f1d37a3Bf840e35c6a860c7C2dA71Fe555123ca) | mainnet | yes | no |
| **->** same module on Base | [`0x1f1d37a3Bf840e35c6a860c7C2dA71Fe555123ca`](https://basescan.org/address/0x1f1d37a3Bf840e35c6a860c7C2dA71Fe555123ca) | base | yes | no |

### Age at time of hack

- **exploited safe mod** `0x1f1d37a3Bf...` created **2026-02-25 20:09:35 UTC**, exploited 2026-05-25 -> **dwell 88 days (0.24 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x3391aa6c3e1ba896...`](https://etherscan.io/tx/0x3391aa6c3e1ba896f342b110d236950bbacf819225f456bd386b5c82d22cdb39).

- **same module on Base** `0x1f1d37a3Bf...` created **2026-02-23 20:42:35 UTC**, exploited 2026-05-25 -> **dwell 90 days (0.25 y)**.
  Source: binary-search eth_getCode on archive RPC (https://base-mainnet.public.blastapi.io) + block timestamp. creation tx **not resolvable** (factory `CREATE` with no constructor logs).
- Exploit block confirmed on-chain: mainnet block 25170474 at **2026-05-25 06:17:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Held no funds itself: it was a Safe module with unlimited spend authority over 86-88 Gnosis Safes across Ethereum, Base and Arbitrum. ~$3-3.98M drained, consolidated into ~3.07M DAI.

### What it was supposed to do

- Category: **Gnosis Safe module / cross-chain router**

### Actual logic and exploited mechanism

- Flaw class: **trusts a caller-supplied sourceAddress string on a permissionless express path**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): A third-party Gnosis Safe module named SquidRouterModule was exploited, draining approximately $3-3.2 million from 86 Gnosis Safe wallets on Ethereum and Base within about 2 hours. The module has no affiliation with the official Squid Router protocol—confusion arose solely due to the contract name on Basescan. Victims had previously added this faulty third-party module as a trusted Safe Module, granting it permission to spend any tokens without signatures. The attacker exploited weak authentication (accepting a publicly visible constant string as "message security" proof) to execute arbitrary calldata, forcing fake Uniswap V3 swaps (real tokens for worthless 'u' token in attacker-controlled pools) and draining funds, which were consolidated into ~3.07M DAI. Squid confirmed its core router and user funds/integrations remain fully secure.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/SquidRouterModule_exp.sol / NewMarketTrading_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Axelar AxelarExpressExecutableWithToken; 86-88 Gnosis Safes on Ethereum/Base/Arbitrum; Uniswap UniversalRouter + Permit2

### Fork / codebase lineage

- Axelar express-executable base + Squid router integration

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: verified source on Base; third-party module granted unlimited spend on 88 Safes; name collides with the official Squid Router

### Prior review status

- Squid publicly confirmed the module has no affiliation with its official router; the confusion arose from the contract *name* alone on Basescan.

---

## 103. Mure — 2026-05-23

**SlowMist line:** Smart Contract Vulnerability · $ 11,700 · [reference](https://x.com/clarahacks/status/2058341669603307880)

**Classification:** Ethereum: SignatureChecker given an attacker-supplied signer source returns true

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited proxy | [`0x365083717efb17f3895290ba38f20f568c7a4d8a`](https://etherscan.io/address/0x365083717efb17f3895290ba38f20f568c7a4d8a) | mainnet | yes (`ERC1967Proxy`) | impl `0xc35c629d68ea3ba30ce5d0842a3b6d34362c7cd8` |

### Age at time of hack

- **exploited proxy** `0x365083717e...` created **2024-03-28 11:33:59 UTC**, exploited 2026-05-23 -> **dwell 785 days (2.15 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xd54d256f9cb06e14...`](https://etherscan.io/tx/0xd54d256f9cb06e14d48398c7028a008bb7aa685dd7d2999ee24f31e7099ff447).
- Exploit block confirmed on-chain: mainnet block 25141106 at **2026-05-21 04:04:35 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 11,700; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **token distribution proxy**

### Actual logic and exploited mechanism

- Flaw class: **SignatureChecker given an attacker-supplied signer source returns true**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Mure’s MureDistribution proxy contract on Ethereum was exploited due to an access control vulnerability in signature validation. The attacker supplied a malicious contract as the “signer source,” causing SignatureChecker to return true and bypass verification. This allowed draining 4.85M QUEST tokens (pre-approved to the proxy) via transferFrom, which were then swapped for ~5.45 ETH (~$11,700) on Uniswap. No user funds or main payment infrastructure were affected; it was a targeted logic flaw in one distribution contract.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/MureDistribution_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- QUEST tokens pre-approved to the proxy; Uniswap for the exit

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 2.15y old proxy holding standing approvals

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 105. Fractal Protocol — 2026-05-22

**SlowMist line:** Smart Contract Vulnerability · $ 13,700 · [reference](https://x.com/DefimonAlerts/status/2058619391776878967)

**Classification:** Arbitrum: USDF vault re-entrant deposit/withdraw against a fixed daily tokenPrice with share rounding

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault | [`0x80e1a981285181686a3951b05ded454734892a09`](https://arbiscan.io/address/0x80e1a981285181686a3951b05ded454734892a09) | arbitrum | **NO** | impl `0x038c8535269e4adc083ba90388f15788174d7da7` |

### Age at time of hack

- **exploited vault** `0x80e1a98128...` created **2023-05-25 00:28:09 UTC**, exploited 2026-05-22 -> **dwell 1092 days (2.99 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x51d2283341ba7d0d...`](https://arbiscan.io/tx/0x51d2283341ba7d0d59aa020b75def3fb4fd58bce7d863420857f6a3111cf4275).

### What it held and controlled

- Vault liquid USDC buffer fell from ~14,778 USDC to near zero; pre-hack TVL ~$97,270 — a small vault relative to the headline.

### What it was supposed to do

- Category: **stablecoin vault**

### Actual logic and exploited mechanism

- Flaw class: **reentrant deposit/withdraw against a fixed daily price + share rounding**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Fractal Protocol’s USDF vault on Arbitrum was exploited via a smart contract logic flaw. The attacker used an Aave V3 USDC.e flash loan, looped through Balancer V2 batchSwap callbacks, and recursively called the vault’s deposit (0xb6b55f25) and withdraw functions. This exploited the fixed daily-accrued tokenPrice (~1.27 USDC/USDF) and share-rounding accounting issues without proper invariant checks across re-entrant flows, allowing the extraction of approximately 13,700 USDC.e. The vault’s liquid USDC buffer dropped from around 14,778 USDC to near zero. Pre-hack TVL was approximately 97,270 USD.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/FractalProtocol_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Aave V3 USDC.e flash loan, Balancer V2 batchSwap callbacks for reentry

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 2.99y old; TVL only ~$97K; fixed daily tokenPrice with no cross-call invariant

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 106. Butter Bridge — 2026-05-20

**SlowMist line:** Smart Contract Vulnerability · $ 180,000 · [reference](https://ourcryptotalk.com/news/butter-bridge-exploit-mints-1-quadrillion-mapo-tokens)

**Classification:** Ethereum: abi.encodePacked hash collision in OmniServiceProxy retry-message verification

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited bridge | [`0x0000317bec33af037b5fab2028f52d14658f6a56`](https://etherscan.io/address/0x0000317bec33af037b5fab2028f52d14658f6a56) | mainnet | yes (`OmniServiceProxy`) | impl `0x12bfb3b58ad02a0df40ee7186d26266c52d0109c` |

### Age at time of hack

- **exploited bridge** `0x0000317bec...` created **2024-10-30 00:39:59 UTC**, exploited 2026-05-20 -> **dwell 566 days (1.55 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xf93aee2427b87e62...`](https://etherscan.io/tx/0xf93aee2427b87e62c5d5961930529d02d46e6afbbc53ad68488250458a8212e4).
- Exploit block confirmed on-chain: mainnet block 25137571 at **2026-05-20 16:13:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 180,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **cross-chain bridge/router**

### Actual logic and exploited mechanism

- Flaw class: **abi.encodePacked hash collision in retry-message verification**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The Butter Bridge V3.1 (part of MAP Protocol and Butter Network) was exploited. An attacker used a vulnerability in the OmniServiceProxy contract’s retry message verification logic, specifically an abi.encodePacked hash collision with dynamic-bytes fields. This allowed forging a cross-chain retry message that bypassed authentication, resulting in the minting of approximately 1 quadrillion (10^15) MAPO tokens (about 4.8 million times the legitimate ~208 million circulating supply). The attacker dumped ~1 billion fake MAPO into the Uniswap V4 ETH/MAPO pool, extracting roughly $180,000 in liquidity (≈52.21 ETH). The teams immediately paused the bridge and related swaps. User funds in pending swaps are safe, and a patch/audit/redeployment is in progress. The remaining ~999 trillion fake tokens stay in the attacker’s wallet, posing ongoing dilution risk.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/MAPProtocol_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- OmniServiceProxy retry path; Uniswap V4 ETH/MAPO pool for the exit

### Fork / codebase lineage

- MAP Protocol / Butter Network codebase

### Observable pre-hack flags

- 1.55y old; dynamic-bytes fields concatenated into a packed hash

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 110. Verus-Ethereum Bridge — 2026-05-18

**SlowMist line:** Smart Contract Vulnerability · $ 11,580,000 · [reference](https://x.com/MetaEraHK/status/2056192367716380711)

**Classification:** Ethereum: Verus bridge import path (first exploitation of the flaw re-hit in July)

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited bridge | [`0x71518580f36feceffe0721f06ba4703218cd7f63`](https://etherscan.io/address/0x71518580f36feceffe0721f06ba4703218cd7f63) | mainnet | **NO** | no |

### Age at time of hack

- **exploited bridge** `0x71518580f3...` created **2023-10-03 22:29:59 UTC**, exploited 2026-05-18 -> **dwell 957 days (2.62 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x7bd34b417fd69a0d...`](https://etherscan.io/tx/0x7bd34b417fd69a0df81dffb4b29c318ce1d3a337ef86a794f6a7e3b10692a428).
- Exploit block confirmed on-chain: mainnet block 25118334 at **2026-05-17 23:55:11 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 11,580,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **cross-chain bridge (EVM side)**

### Actual logic and exploited mechanism

- Flaw class: **unbacked payout via the import path**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Blockaid detected an ongoing exploit on the Verus-Ethereum Bridge. The attacker drained approximately $11.58 million in assets (including ~1,625 ETH, ~103.6 tBTC, and ~147k USDC). The funds were swapped and consolidated into a drainer wallet (e.g., 0x65Cb8b128Bf6e690761044CCECA422bb239C25F9). This is a cross-chain bridge incident affecting the bridge infrastructure, not the core Verus blockchain. The project had recently issued an urgent update, but the exploit still occurred. Funds remain in the attacker's control as of the latest reports. On May 22, PeckShield's monitoring revealed that the exploiter of the Verus cross-chain bridge has returned 4,052.4 ETH (valued at around $8.5 million) to the team's designated address. This recovery accounts for 75% of the total plundered funds, while the remaining 25% (approximately 1,350 ETH) is being retained in the hacker's wallet as a bug bounty.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/VerusBridge_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- bridge reserves ETH/tBTC/USDC

### Fork / codebase lineage

- hand-rolled Verus bridge

### Observable pre-hack flags

- same contract re-hit in July — the May incident is the pre-hack observable for the July one

### Prior review status

- None located.

---

## 112. SEA Token — 2026-05-17

**SlowMist line:** Flashloan Price Manipulation · $ 153,000 · [reference](https://x.com/procur3/status/2057004818145952190)

**Classification:** Arbitrum: MetaSea RedeemPosition distributor drained via flash-loan-manipulated pricing

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited contract | [`0xa70f31c06f921019237fc00b1417217dae5c37c5`](https://arbiscan.io/address/0xa70f31c06f921019237fc00b1417217dae5c37c5) | arbitrum | yes (`ERC1967Proxy`) | impl `0x13dde273b66323686bfb96cce5a2a7190b40b264` |

### Age at time of hack

- **exploited contract** `0xa70f31c06f...` created **2026-02-10 15:31:06 UTC**, exploited 2026-05-17 -> **dwell 95 days (0.26 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x17db38183d6e0ae8...`](https://arbiscan.io/tx/0x17db38183d6e0ae8cafb4199e98776d65a0e855c5033acc2b69fe1f298675171).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 153,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **reward/position distributor**

### Actual logic and exploited mechanism

- Flaw class: **flash-loan-manipulated pricing on a redeem path**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): SEA Token on Arbitrum was exploited through a flashloan-enabled price manipulation attack due to a protocol logic flaw in its Solidity smart contract. The attacker used a flash loan to artificially manipulate the token price (likely via liquidity pool imbalance or oracle dependency), allowing unauthorized extraction of approximately $153,000 in value.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/SEAToken_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Arbitrum AMM pools; flash loan

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 95d old

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 116. ShapeShift FOX Colony — 2026-05-13

**SlowMist line:** Smart Contract Vulnerability · $ 132,700 · [reference](https://x.com/blockaid_/status/2054593377438421492?s=46&amp;t=DLwbX9Nw4QECiyZQ0av-fg)

**Classification:** Arbitrum: Colony EtherRouter meta-transaction self-call defeats DSAuth

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited colony | [`0x5C59D0eC51729E40C413903bE6A4612f4E2452da`](https://arbiscan.io/address/0x5C59D0eC51729E40C413903bE6A4612f4E2452da) | arbitrum | yes (`EtherRouterCreate3`) | no |
| colony component | [`0xf929de51d91c77e42f5090069e0ad7a09e513c73`](https://arbiscan.io/address/0xf929de51d91c77e42f5090069e0ad7a09e513c73) | arbitrum | yes (`ClonableBeaconProxy`) | no |

### Age at time of hack

- **exploited colony** `0x5C59D0eC51...` created **2024-04-23 15:52:25 UTC**, exploited 2026-05-13 -> **dwell 749 days (2.05 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xf6a8ab993480bc26...`](https://arbiscan.io/tx/0xf6a8ab993480bc264255238c2e2187926259b0613a8f85dcaffee27ea2cdb0f8).

- **colony component** `0xf929de51d9...` created **2023-04-14 04:00:29 UTC**, exploited 2026-05-13 -> **dwell 1124 days (3.08 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x622106189a52cf76...`](https://arbiscan.io/tx/0x622106189a52cf763098588f3b12399fc43838cffee1181dd13ac372f43a19ee).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 132,700; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **DAO treasury (Colony)**

### Actual logic and exploited mechanism

- Flaw class: **meta-transaction self-call defeats DSAuth (msg.sender == self)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): ShapeShift’s FOX Colony (a community governance and participation program for FOX token holders) on Arbitrum was exploited via a smart contract vulnerability in its Colony Network contracts. The attacker drained approximately $132.7K in USDC and FOX tokens in a single sophisticated transaction by exploiting a meta-transaction self-call flaw combined with DSAuth authorization logic. The core exchange platform was unaffected; this impacted the DAO/community treasury.

### Interaction graph

- Colony EtherRouter + ClonableBeaconProxy; resolver redirected then delegatecalled; UniswapV2 pair for the exit

### Fork / codebase lineage

- Colony Network codebase

### Observable pre-hack flags

- 2.05y old colony instance; EtherRouter + DSAuth pattern with meta-transactions

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 117. Aurellion Labs — 2026-05-12

**SlowMist line:** Smart Contract Vulnerability · $ 456,000 · [reference](https://x.com/SlowMist_Team/status/2054163700035289446)

**Classification:** Arbitrum: EIP-2535 diamond with an initialize(address) selector whose _initialized slot stayed 0

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited diamond | [`0x0adc63e71b035d5c7fdb1b4593999fa1f296f1b2`](https://arbiscan.io/address/0x0adc63e71b035d5c7fdb1b4593999fa1f296f1b2) | arbitrum | **NO** | no |
| facet | [`0x3CA79C1cf29B8d19F7c643bB6E6bc9c49762E70f`](https://arbiscan.io/address/0x3CA79C1cf29B8d19F7c643bB6E6bc9c49762E70f) | arbitrum | **NO** | no |

### Age at time of hack

- **exploited diamond** `0x0adc63e71b...` created **2026-03-17 10:08:24 UTC**, exploited 2026-05-12 -> **dwell 55 days (0.15 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x1f43d6deabbc9974...`](https://arbiscan.io/tx/0x1f43d6deabbc9974fe837d6269bcc6b1f6259799f874ecbcfb06a46078410b2e).

- **facet** `0x3CA79C1cf2...` created **2026-03-17 10:07:23 UTC**, exploited 2026-05-12 -> **dwell 55 days (0.15 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xcfeccb5282feff9e...`](https://arbiscan.io/tx/0xcfeccb5282feff9e6e6002d94ca3db6a16193f0ac32848a277e93a5597be4123).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 456,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **DeFi diamond (EIP-2535)**

### Actual logic and exploited mechanism

- Flaw class: **re-initializable proxy (initialize(address) with _initialized still 0)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Aurellion Labs' Diamond Proxy contract (EIP-2535) was exploited due to an unprotected initialize(address) function in the SafeOwnable Facet. Although an owner was set, the OpenZeppelin-style _initialized storage slot remained 0, allowing re-initialization. The attacker called initialize() to take ownership, used diamondCut to add a malicious facet with pullERC20/sweep functions, and drained USDC from wallets that had previously approved the diamond proxy. The project paused operations, committed to reimbursing users, and advised revoking old approvals.

### Interaction graph

- diamondCut to add a malicious pullERC20/sweep facet; drained standing USDC approvals

### Fork / codebase lineage

- EIP-2535 diamond + OpenZeppelin-style initializer

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: unverified diamond, facet with an exposed initialize(address) selector and an uninitialized slot, live for 55 days

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 118. SQ Protocol — 2026-05-12

**SlowMist line:** Smart Contract Vulnerability · $ 346,100 · [reference](https://x.com/Defi_Nerd_sec/status/2054425936746148148)

**Classification:** BSC: hardcoded backdoor in the verified Staking contract, reached with an EIP-7702 type-4 tx

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited staking | [`0x404404A845FFF0201f3a4D419B4839fC419c99F7`](https://bscscan.com/address/0x404404A845FFF0201f3a4D419B4839fC419c99F7) | bsc | yes | no |

### Age at time of hack

- **exploited staking** `0x404404A845...` created **2026-01-29 11:09:12 UTC**, exploited 2026-05-12 -> **dwell 102 days (0.28 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xe9f9803ebc084a24...`](https://bscscan.com/tx/0xe9f9803ebc084a240bbe468ae39e560cd47713bff739100cf6175776296e17b9).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 346,100; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **staking contract**

### Actual logic and exploited mechanism

- Flaw class: **hardcoded owner backdoor in verified source**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): On May 12, 2026, at approximately 10:11 UTC, the SQ Protocol on BNB Chain was exploited for $346,137. The attacker abused a hardcoded owner backdoor in the verified Staking contract (0x404404a845fff0201f3a4d419b4839fc419c99f7). Using a type-0x4 transaction with authorizationList, they took ownership, minted fake staking claims, redeemed ~296.5K USDT, swept SQi tokens, and dumped them in the SQi/USDT pool for additional profit. Total realized loss: approximately $346.1K.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/SQTokenStaking_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- SQi/USDT pool; EIP-7702 type-4 authorizationList

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: the backdoor is in the VERIFIED source (Sourcify exact_match, verified 11 seconds after deployment); 102 days live

### Prior review status

- Source is verified (Sourcify `exact_match`, `verifiedAt` 2026-01-29T11:09:23Z — **11 seconds after deployment**). The backdoor was therefore in publicly readable source for 102 days.

---

## 123. Renegade — 2026-05-10

**SlowMist line:** Smart Contract Vulnerability · $ 209,000 · [reference](https://x.com/renegade_fi/status/2053531772634427599?s=46)

**Classification:** Arbitrum: unprotected initializer on the V1 Dark Pool proxy after a desynced migration

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited proxy | [`0x30bD8eAb29181F790D7e495786d4B96d7AfDC518`](https://arbiscan.io/address/0x30bD8eAb29181F790D7e495786d4B96d7AfDC518) | arbitrum | **NO** | impl `0x58f876aaeecbd5a0fca8f87e1313a9188c155bcc` |

### Age at time of hack

- **exploited proxy** `0x30bD8eAb29...` created **2024-09-03 21:41:50 UTC**, exploited 2026-05-10 -> **dwell 613 days (1.68 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x1a67f80611ad5e5f...`](https://arbiscan.io/tx/0x1a67f80611ad5e5f2a838fb69c0bfd0616482ec903bbda50f3d8c580009658ba).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 209,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **dark pool / trading venue (legacy V1)**

### Actual logic and exploited mechanism

- Flaw class: **unprotected initializer on the proxy after a desynced migration**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Renegade’s legacy V1 deployment on Arbitrum was exploited. The attacker took advantage of an unprotected initializer in the Dark Pool proxy contract (combined with a faulty migration from April 2025 that left the version counter out of sync), injected malicious logic, and used delegatecall to drain approximately $209,000 worth of 27 different ERC-20 tokens from the proxy contract’s storage. The exploiter, acting as a whitehat, negotiated on-chain with the team. Renegade offered a 90/10 split (return 90%, keep 10% as a whitehat bounty, no legal action). The whitehat returned ~$190,000 within 45 minutes. The team confirmed the issue was isolated to the V1 Arbitrum deployment (which has been paused), all other deployments are safe, and all affected users will be made whole.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/Renegade_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- delegatecall into injected logic; 27 ERC-20s held in proxy storage

### Fork / codebase lineage

- Renegade V1 codebase

### Observable pre-hack flags

- 1.68y old legacy deployment, version counter desynced by an April 2025 migration

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 124. TrustedVolumes — 2026-05-07

**SlowMist line:** Smart Contract Vulnerability · $ 6,700,000 · [reference](https://x.com/trustedvolumes/status/2052235435292910005)

**Classification:** Ethereum: permissionless registerAllowedOrderSigner + authorization keyed on taker instead of maker

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited proxy | [`0xeEeEEe53033F7227d488ae83a27Bc9A9D5051756`](https://etherscan.io/address/0xeEeEEe53033F7227d488ae83a27Bc9A9D5051756) | mainnet | **NO** | no |
| implementation | [`0x88eb28009351Fb414A5746F5d8CA91cdc02760d8`](https://etherscan.io/address/0x88eb28009351Fb414A5746F5d8CA91cdc02760d8) | mainnet | **NO** | no |

### Age at time of hack

- **exploited proxy** `0xeEeEEe5303...` created **2024-08-20 19:51:11 UTC**, exploited 2026-05-07 -> **dwell 624 days (1.71 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xeaecec6ba7a407c7...`](https://etherscan.io/tx/0xeaecec6ba7a407c7fbd0ac36d87bf46eeae5e696b3f97263acdf53be3f47043f).

- **implementation** `0x88eb280093...` created **2024-09-24 12:36:35 UTC**, exploited 2026-05-07 -> **dwell 589 days (1.61 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x1bdc5cada6a57db9...`](https://etherscan.io/tx/0x1bdc5cada6a57db962b0da6e6483c38f1d9ebce6b4808f6449f0c4dfccaece39).
- Exploit block confirmed on-chain: mainnet block 25039670 at **2026-05-07 00:47:35 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Held no funds itself: an RFQ settlement proxy holding an UNLIMITED standing approval from resolver wallet 0x9ba0cf15... Four orders drained 1,291.16 WETH + 206,282.45 USDT + 16.939 WBTC + 1,268,771.49 USDC (~$5.87M).

### What it was supposed to do

- Category: **market-maker RFQ settlement proxy**

### Actual logic and exploited mechanism

- Flaw class: **permissionless signer registration + authorization keyed on the wrong party**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): TrustedVolumes, a key liquidity provider and resolver (market maker) for 1inch Fusion and other DeFi protocols, was exploited via a vulnerability in its custom RFQ swap proxy contract, resulting in approximately $6.7 million stolen. The project confirmed the incident on X, published the three Ethereum addresses holding the stolen funds (approx. $3M, $3M, and $700K), and stated openness to constructive communication for a bug bounty and mutually acceptable resolution. 1inch confirmed its protocol, infrastructure, and user funds are unaffected.In July 2026, the attacker returned ~1,122 ETH (~$2M) while keeping a similar amount as bounty.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/TrustedVolumes_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- resolver/maker wallet with UNLIMITED standing approval to the proxy; 1inch Fusion resolver role

### Fork / codebase lineage

- hand-rolled RFQ settlement (unverified implementation)

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: unverified implementation behind a proxy holding an unlimited approval from a wallet with $6M+

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 125. Ekubo Protocol — 2026-05-05

**SlowMist line:** Smart Contract Vulnerability · $ 1,400,000 · [reference](https://x.com/blockaid_/status/2051757787714118125)

**Classification:** Ethereum: IPayer.pay callback takes payer/token/amount from the lock payload without checking the lock initiator

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited extension | [`0x8CCB1ffD5C2aa6Bd926473425Dea4c8c15DE60fd`](https://etherscan.io/address/0x8CCB1ffD5C2aa6Bd926473425Dea4c8c15DE60fd) | mainnet | **NO** | no |

### Age at time of hack

- **exploited extension** `0x8CCB1ffD5C...` created **2025-09-05 14:42:59 UTC**, exploited 2026-05-05 -> **dwell 241 days (0.66 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x0cd9656c1dbeeece...`](https://etherscan.io/tx/0x0cd9656c1dbeeecea2eb7ef29461f69ee91a65cf8c34676dc9a7f45d0f478df0).

### What it held and controlled

- Held no funds itself: an extension contract holding standing ERC-20 approvals from users. ~$1.4M drained from approvers.

### What it was supposed to do

- Category: **DEX extension/hook**

### Actual logic and exploited mechanism

- Flaw class: **callback takes payer/token/amount from the lock payload without checking the lock initiator**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): According to Blockaid, Ekubo Protocol’s custom extension contract on Ethereum was attacked in the early hours, resulting in a loss of approximately $1.4 million. Ekubo users themselves were not directly affected. Only users who had previously approved the V2 contract as a token spender were exposed to risk. The root cause lies in the IPayer.pay callback function within the Ekubo extension contract. Specifically, the payer, token, and amount parameters in the token.transferFrom call were directly sourced from the lock payload and could be fully controlled by the attacker. The contract failed to verify whether the payer was the initiator of the lock or an authorized payment source. As a result, the attacker was able to exploit prior ERC-20 approvals granted by users to the contract. By routing through the Core locking mechanism into the extension contract, the attacker could designate any previously approved user as the payer while setting themselves as the recipient, thereby draining user funds.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-05/Ekubo_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Ekubo Core lock mechanism; user ERC-20 approvals to the extension

### Fork / codebase lineage

- Ekubo codebase (Starknet-origin, EVM port)

### Observable pre-hack flags

- 241d old; extension holding standing user approvals; callback trusts payload-supplied payer

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 126. SmartCredit — 2026-05-04

**SlowMist line:** Smart Contract Vulnerability · $ 72,000 · [reference](https://x.com/smartcredit_io/status/2051361795789496337)

**Classification:** Leveraged Lido module drained; mechanism not publicly detailed

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 72,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **leveraged staking module**

### Actual logic and exploited mechanism

- Flaw class: **not publicly detailed**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): SmartCredit’s Leveraged Lido module was exploited. The attacker drained funds from this leveraged staking feature. The team has paused the Leveraged Lido functionality, and the protocol’s Loss Provision Fund will fully cover the gap for affected stakers.

### Interaction graph

- Lido stETH leverage loop

### Fork / codebase lineage

- unknown

### Observable pre-hack flags

- unknown

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 132. YieldCore — 2026-04-28

**SlowMist line:** Smart Contract Vulnerability · $ 398,000 · [reference](https://x.com/DefimonAlerts/status/2049365873069097237)

**Classification:** Ethereum: RWAVault overrides ERC4626 withdraw without the allowance spend when msg.sender != owner

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| exploited logic | [`0x317aa10528ff675ef4c358ea6a5b7b5494325733`](https://etherscan.io/address/0x317aa10528ff675ef4c358ea6a5b7b5494325733) | mainnet | yes (`RWAVault`) | no |
| **->** vault entry | [`0xb9c7c84a1aa0dd40b5b38aae815ad0cdd2e5f88a`](https://etherscan.io/address/0xb9c7c84a1aa0dd40b5b38aae815ad0cdd2e5f88a) | mainnet | yes (`RWAVault`) | impl `0x317aa10528ff675ef4c358ea6a5b7b5494325733` |

### Age at time of hack

- **exploited logic** `0x317aa10528...` created **2026-02-04 04:32:59 UTC**, exploited 2026-04-28 -> **dwell 82 days (0.22 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x268b273c6e89c11c...`](https://etherscan.io/tx/0x268b273c6e89c11cb6f5a3a352206846d8750996db10d3e0f70aa93dd60c5f2a).

- **vault entry** `0xb9c7c84a1a...` created **2026-03-19 15:02:35 UTC**, exploited 2026-04-28 -> **dwell 39 days (0.11 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x241de4abe766c3dc...`](https://etherscan.io/tx/0x241de4abe766c3dce8c418af0baf3b3789a22eccaabbf636367a0e28c232a337).
- Exploit block confirmed on-chain: mainnet block 24979315 at **2026-04-28 14:59:59 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Eight depositors' balances withdrawn to an attacker-controlled receiver: 398,655.47 USDC vault outflow.

### What it was supposed to do

- Category: **ERC4626 RWA vault (clone)**

### Actual logic and exploited mechanism

- Flaw class: **withdraw override omits the allowance spend when msg.sender != owner**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The YieldCore-3rd-deal vault under Trading Protocol was exploited. The attacker took advantage of a missing caller authorization check in the contract, bypassing the permission mechanism and draining all funds from the vault in one go. The vault was permissionlessly listed (not a core part of the protocol itself). The entire vault was emptied.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/RWAVault_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- ERC-1167 minimal-proxy clone (45-byte entry) over logic 0x317aa105..; USDC

### Fork / codebase lineage

- ERC4626 base with a custom withdraw override

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: clone-factory deployment, entry 39d old / logic 82d old, permissionlessly listed vault

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 133. JUDAO — 2026-04-28

**SlowMist line:** Smart Contract Vulnerability · $ 228,000 · [reference](https://x.com/DefimonAlerts/status/2049019388947321334)

**Classification:** BSC: JUDAO sell hook drains JUDAO from its own Pancake pair via sync/isBurnPair

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0xf55dff7898930a2d28cdbc39d615b1624ac86888`](https://bscscan.com/address/0xf55dff7898930a2d28cdbc39d615b1624ac86888) | bsc | yes | no |

### Age at time of hack

- **exploited token** `0xf55dff7898...` created **2026-01-17 00:52:05 UTC**, exploited 2026-04-28 -> **dwell 100 days (0.27 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xd5cf67c8fdaa121c...`](https://bscscan.com/tx/0xd5cf67c8fdaa121c783d2ad4f4bdd9cbf49c97e988974c78c1bc279c4066f813).
- Exploit block confirmed on-chain: bsc block 95070973 at **2026-04-28 00:00:00 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 228,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **sell hook drains token from its own pair via sync/isBurnPair**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The JUDAO token / liquidity pool on BSC was exploited via Flashloan-assisted Manipulation. The attacker used flash loans to manipulate pool reserves or pricing, draining funds through PancakeSwap V2 routes (e.g., BUSD-JUDAO pair). Losses included at least 205,259 USDT plus 36 BNB.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/JUDAO_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap BUSD-JUDAO pair, flash-loaned USDT

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 100d old

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 134. ZetaChain GatewayEVM — 2026-04-27

**SlowMist line:** Smart Contract Vulnerability · $ 334,000 · [reference](https://x.com/ZetaChain/status/2048854107633631356?s=20)

**Classification:** Ethereum(+3): GatewayEVM.execute arbitrary-call sink with missing access control on GatewayZEVM.call

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited gateway | [`0x48B9AACC350b20147001f88821d31731Ba4C30ed`](https://etherscan.io/address/0x48B9AACC350b20147001f88821d31731Ba4C30ed) | mainnet | yes (`ERC1967Proxy`) | impl `0x9d7ad5821a40b9e90199e343f3afc1591fbdfa52` |
| implementation | [`0x1FfF55ccf855212f6b5530c468b44f9a5246572E`](https://etherscan.io/address/0x1FfF55ccf855212f6b5530c468b44f9a5246572E) | mainnet | yes (`GatewayEVM`) | no |

### Age at time of hack

- **exploited gateway** `0x48B9AACC35...` created **2024-11-04 20:50:59 UTC**, exploited 2026-04-27 -> **dwell 538 days (1.47 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x44c18b3249d7925f...`](https://etherscan.io/tx/0x44c18b3249d7925f6e3257bdfd4441778e642fb140e1d92da64b433df6e483ae).

- **implementation** `0x1FfF55ccf8...` created **2025-11-14 13:58:35 UTC**, exploited 2026-04-27 -> **dwell 163 days (0.45 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xd62c120fba6d5891...`](https://etherscan.io/tx/0xd62c120fba6d5891249c47e7ff19d475063c9f1acf0944de964d6c1c39650c89).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 334,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **cross-chain gateway/router**

### Actual logic and exploited mechanism

- Flaw class: **arbitrary-call sink with missing access control**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): ZetaChain disclosed in a post on X that its GatewayEVM contract was attacked today, affecting only wallets belonging to the internal ZetaChain team. The attack vector has been blocked to prevent further loss of funds. As a precautionary measure, cross-chain transactions on ZetaChain are currently suspended. The investigation is still ongoing, and no user funds have been affected so far. On April 29, ZetaChain announced on X that on April 27 it had suffered a premeditated and targeted attack. The attacker funded addresses using Tornado Cash and impersonated wallet addresses. Cross-chain ZETA transfers were not affected, and user funds remained safe. All impacted wallets were controlled by ZetaChain. A mainnet patch has been deployed, and cross-chain transactions will be re-enabled after continued monitoring. The attack impacted the arbitrary call functionality of GatewayEVM, resulting in an estimated loss of approximately $334,000 across four connected chains.

### Interaction graph

- GatewayEVM.execute on Ethereum/BSC/Base/Polygon; GatewayZEVM.call on ZetaChain; vanity-address impersonation

### Fork / codebase lineage

- ZetaChain gateway codebase

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: a bug-bounty report describing this behaviour had been filed and dismissed as by-design

### Prior review status

- **A bug-bounty report describing exactly this arbitrary-call behaviour had been filed before the incident and was dismissed as by-design.** ZetaChain's post-mortem acknowledges this and says the bounty triage process is under review. This is the strongest 'prior scrutiny existed and was ignored' data point in the population.

---

## 135. Singularity Finance — 2026-04-27

**SlowMist line:** Oracle Misconfiguration · $ 413,000 · [reference](https://x.com/0xSalazar/status/2048762346143666656)

**Classification:** Base: oracle registered with a non-existent UniV3 fee tier 42, so getPool() returned address(0)

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault | [`0x67b93f6676bd1911c5fae7ffa90fff5f35e14dcd`](https://basescan.org/address/0x67b93f6676bd1911c5fae7ffa90fff5f35e14dcd) | base | **not in Sourcify** | impl `0xea7975c2fec1ae9e3058bb5f99d8e26dbc816811` |
| oracle | [`0x73b8c192bfc323c3ea224c88219d55dfc319e89f`](https://basescan.org/address/0x73b8c192bfc323c3ea224c88219d55dfc319e89f) | base | yes | no |

### Age at time of hack

- **exploited vault** `0x67b93f6676...` created **2026-01-17 13:01:51 UTC**, exploited 2026-04-27 -> **dwell 99 days (0.27 y)**.
  Source: binary-search eth_getCode on archive RPC (https://base-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x6df5e0ce8d533c33...`](https://basescan.org/tx/0x6df5e0ce8d533c3332323367e2ecacacf0b416cf15afe802daf0503b4277714e).

- **oracle** `0x73b8c192bf...` created **2025-06-27 09:02:59 UTC**, exploited 2026-04-27 -> **dwell 303 days (0.83 y)**.
  Source: binary-search eth_getCode on archive RPC (https://base-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x957679eb8ef395e9...`](https://basescan.org/tx/0x957679eb8ef395e9e8dd18cc568b888ecbff3a2306390a658792c9bba4deb01b).
- Exploit block confirmed on-chain: base block 45183966 at **2026-04-25 22:47:59 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Vault reserves: ~$413.13K USDC plus residual vault shares; the oracle only recognised ~$100 of idle USDC because of the broken fee tier.

### What it was supposed to do

- Category: **ERC4626 yield vault (clone)**

### Actual logic and exploited mechanism

- Flaw class: **oracle misconfiguration — non-existent UniV3 fee tier 42 makes getPool() return address(0)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Singularity Finance vaults were exploited due to a critical oracle misconfiguration. The admin had registered an unsupported Uniswap V3 fee tier of 42 (valid tiers: 100/500/3000/10000) back in January, causing factory.getPool() to silently return address(0). This made the oracle price all non-USDC reserves at zero. The vault only recognized ~$100 in idle USDC while real yield tokens sat undervalued. The attacker flash-loaned 100K USDC from Morpho, deposited into the vault to mint ~99.99% of shares at the broken ratio, then redeemed for a proportional share of actual underlying assets, draining ~$413K. Root cause: admin parameter error combined with missing input validation on fee tiers. The misconfig sat undetected for ~3 months.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/SingularityDynaVault_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- UniswapV3 factory.getPool() through oracle 0x73b8c192..; Morpho 100K USDC flash loan

### Fork / codebase lineage

- ERC4626 vault behind a 45-byte ERC-1167 clone

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: fee tier 42 is not a valid tier (100/500/3000/10000) — an incoherent config readable on-chain for ~3 months

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 138. Giddy — 2026-04-23

**SlowMist line:** Smart Contract Vulnerability · $ 1,300,000 · [reference](https://x.com/DefimonAlerts/status/2047334517535642024)

**Classification:** Ethereum: EIP-712 signature covers only keccak(SwapInfo.data), not aggregator/fromToken/toToken/amount

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault | [`0x5f0ad32c00641d1d2bb628ff341e0d4bb4494318`](https://etherscan.io/address/0x5f0ad32c00641d1d2bb628ff341e0d4bb4494318) | mainnet | yes (`GiddyVaultV3`) | no |

### Age at time of hack

- **exploited vault** `0x5f0ad32c00...` created **2026-04-20 22:05:11 UTC**, exploited 2026-04-23 -> **dwell 2 days (0.01 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0xdd4c062770002783...`](https://etherscan.io/tx/0xdd4c062770002783962b8ad80bcefaac670568bfb2162cf1bfae80284cf1f3f8).
- Exploit block confirmed on-chain: mainnet block 24942491 at **2026-04-23 11:57:35 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 1,300,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **yield vault**

### Actual logic and exploited mechanism

- Flaw class: **signature covers only part of the struct (aggregator/tokens/amount unsigned)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The DeFi protocol Giddy’s GiddyVaultV3 contract was exploited, resulting in a loss of approximately $1.3 million. The attack was caused by a design flaw in its authorization validation logic. When using the EIP-712 signature scheme, the contract only validated part of the data within the SwapInfo structure, failing to cover critical parameters such as aggregator, fromToken, toToken, and amount, leading to incomplete signature coverage. The attacker exploited this flaw by replaying a valid signature and crafting malicious transaction parameters: replacing fromToken with the strategy’s LP tokens, setting the aggregator to a contract controlled by the attacker, substituting toToken with a malicious token, and setting the transaction amount to the maximum value. Since these key fields were not included in the signature verification scope, the contract accepted the transaction as valid and executed it. As a result, the attacker successfully transferred out protocol assets, causing a loss of approximately $1.3 million.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/giddyvaultv3_compound_auth_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- attacker-controlled aggregator; strategy-held YieldBasis gauge tokens; EIP-712 compound authorisations

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 2 DAYS old at exploit

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 139. Kipseli — 2026-04-22

**SlowMist line:** Smart Contract Vulnerability · $ 72,350 · [reference](https://x.com/TheDEFIac/status/2046973478595641435)

**Classification:** Base: router transfers a USDC-scaled quote as cbBTC units — decimal/asset mismatch

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited router | [`0xd35c6717cca1e04696b694dcb1643ac3620d2152`](https://basescan.org/address/0xd35c6717cca1e04696b694dcb1643ac3620d2152) | base | yes | no |

### Age at time of hack

- **exploited router** `0xd35c6717cc...` created **2026-04-14 09:25:35 UTC**, exploited 2026-04-22 -> **dwell 7 days (0.02 y)**.
  Source: binary-search eth_getCode on archive RPC (https://base-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x33b0806abd379cb1...`](https://basescan.org/tx/0x33b0806abd379cb1f46838ebab4b67bf24b48c32ad74edd3f89e47e518e919d4).
- Exploit block confirmed on-chain: base block 45008654 at **2026-04-21 21:24:15 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Router pass-through, not a balance: attacker swapped ~0.04 WETH for ~0.926 cbBTC (~$72.35K) out of routed liquidity. 80% returned by the finder as a white-hat disclosure.

### What it was supposed to do

- Category: **DEX router**

### Actual logic and exploited mechanism

- Flaw class: **decimal/asset mismatch — USDC-scaled quote transferred as cbBTC units**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): The Kipseli Router contract on Base was exploited via Improper Validation / Decimal Mismatch. The router blindly used the amount returned by an external USDC-only quoter as the raw transfer amount for tokenOut without verifying that the output token matched the quote token. The attacker used an unsupported path (e.g., WETH → cbBTC), causing the quoter to return a USDC-scaled value (6 decimals) which was then transferred as cbBTC (8 decimals), resulting in massive over-transfer. The attacker swapped only ~0.04 WETH for ~0.926 cbBTC (worth ~$72.35K). Afterward, the finder contacted the team, returned 80% of the funds as a white-hat disclosure, and kept 20% as a bug bounty.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/KipseliPropAMM_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PropAMM quoter (USDC-only) used for a WETH->cbBTC path

### Fork / codebase lineage

- hand-rolled router

### Observable pre-hack flags

- 7 days old at exploit; router trusts an external quoter without checking the quoted asset

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 141. Thetanuts Finance — 2026-04-20

**SlowMist line:** Smart Contract Vulnerability · $ 50,000 · [reference](https://academy.teleswap.xyz/defi-protocol-hacks-april-2026-exploits-analyzed/)

**Classification:** Ethereum: first-depositor share-rounding on a freshly deployed vault holding pre-existing WBTC

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault | [`0x80b8eeb34a2ba5dd90c61e02a12ea30515dca6f5`](https://etherscan.io/address/0x80b8eeb34a2ba5dd90c61e02a12ea30515dca6f5) | mainnet | **NO** | no |

### Age at time of hack

- **exploited vault** `0x80b8eeb34a...` created **2022-05-27 23:35:03 UTC**, exploited 2026-04-20 -> **dwell 1423 days (3.90 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x17214bb04c792758...`](https://etherscan.io/tx/0x17214bb04c792758e5faa92169e913f8cd9afb9b9141450aec5b68c5e7d7328d).
- Exploit block confirmed on-chain: mainnet block 24923218 at **2026-04-20 19:30:47 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 50,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **options vault (new deployment)**

### Actual logic and exploited mechanism

- Flaw class: **first-depositor share-rounding on a vault with pre-existing assets**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): A newly deployed vault contract of Thetanuts Finance was exploited via a First Depositor Attack. The attacker took advantage of the vault’s share calculation logic when totalAssets and totalSupply were both 0 at initialization: they deposited a minimal amount (e.g., 1 wei) to mint 1 share, then directly transferred a large amount of assets (e.g., ETH) to the contract, manipulating the asset-to-share ratio. When subsequent users deposited, they received almost no shares, allowing the attacker to redeem their single share for nearly all the vault’s assets. The loss was approximately $50,000. The protocol focuses on on-chain options and yield vaults; this incident affected a specific new vault.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/ThetanutsVaultShareRounding_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- flash-loaned WBTC; vault held WBTC while totalSupply()==0

### Fork / codebase lineage

- Thetanuts codebase

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: totalSupply()==0 while the vault already held WBTC — a readable state

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 142. Juicebox V3 — 2026-04-20

**SlowMist line:** Smart Contract Vulnerability · $ 52,000 · [reference](https://academy.teleswap.xyz/defi-protocol-hacks-april-2026-exploits-analyzed/)

**Classification:** Ethereum: REVLoans.borrowFrom registers a caller-supplied loan source, forging accounting context

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited contract | [`0x1880D832aa283d05b8eAB68877717E25FbD550Bb`](https://etherscan.io/address/0x1880D832aa283d05b8eAB68877717E25FbD550Bb) | mainnet | yes (`REVLoans`) | no |

### Age at time of hack

- **exploited contract** `0x1880D832aa...` created **2025-09-12 11:39:47 UTC**, exploited 2026-04-20 -> **dwell 219 days (0.60 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x1aa7d55deb3594e6...`](https://etherscan.io/tx/0x1aa7d55deb3594e688b96c0823de20a8868d2c19ec1d00a4c390b61bb0bb66b8).
- Exploit block confirmed on-chain: mainnet block 24917718 at **2026-04-20 01:08:23 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 52,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **revnet borrowing extension**

### Actual logic and exploited mechanism

- Flaw class: **caller-supplied loan source registered on first use (forged accounting context)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Juicebox V3 (via its REVLoans borrowing extension) was exploited through a borrowFrom Spoof Attack. The vulnerability stemmed from insufficient validation in the borrowFrom function, particularly the caller-supplied "source" parameter (a REVLoanSource struct with .terminal and .token). This allowed forging an accounting context; when currency matched the destination, the protocol skipped the oracle and used attacker-controlled decimals/balances, enabling borrowing at an inflated share price. The attack used two transactions (one to seed fake accounting, one to drain against a legitimate terminal), draining approximately 21.77 ETH (worth ~$52,000).

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/JuiceboxREVLoans_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- JBMultiTerminal treasury; fake terminal/token contract deployed by the attacker

### Fork / codebase lineage

- Juicebox V3 / REVLoans codebase

### Observable pre-hack flags

- 219d old; borrowFrom trusts a caller-supplied REVLoanSource struct

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 149. LootBot AI — 2026-04-15

**SlowMist line:** Smart Contract Vulnerability · $ 9,600 · [reference](https://x.com/DefimonAlerts/status/2044709964091187660)

**Classification:** Ethereum: redeem() accepts duplicate NFT IDs and only advances nextRedeem after payout

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited staking | [`0xf3A3648bB1Da9D3aeA107da77E6f5bA9Cf313127`](https://etherscan.io/address/0xf3A3648bB1Da9D3aeA107da77E6f5bA9Cf313127) | mainnet | yes (`Staking`) | no |
| nft | [`0x9d87Ff196646A99BDdb16876066aA863900118b4`](https://etherscan.io/address/0x9d87Ff196646A99BDdb16876066aA863900118b4) | mainnet | yes (`TransparentUpgradeableProxy`) | impl `0xf3a3648bb1da9d3aea107da77e6f5ba9cf313127` |

### Age at time of hack

- **exploited staking** `0xf3A3648bB1...` created **2023-12-21 11:58:47 UTC**, exploited 2026-04-15 -> **dwell 845 days (2.31 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x8fb869bb252c212d...`](https://etherscan.io/tx/0x8fb869bb252c212d31bd4813e60804c9b9446c377fb80f9c2445daabf7d923d6).

- **nft** `0x9d87Ff1966...` created **2023-12-21 11:59:11 UTC**, exploited 2026-04-15 -> **dwell 845 days (2.31 y)**.
  Source: Etherscan V2 getcontractcreation. creation tx [`0x6c3614183c223304...`](https://etherscan.io/tx/0x6c3614183c22330481fd499a04a65d28d3acb35539fa316eac5607bcd4676076).
- Exploit block confirmed on-chain: mainnet block 24885767 at **2026-04-15 14:19:11 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Reward pool ETH: 6.2098 ETH paid out against a 2.1 ETH flash loan; net ~4.1 ETH.

### What it was supposed to do

- Category: **NFT staking / reward redemption**

### Actual logic and exploited mechanism

- Flaw class: **duplicate IDs accepted; nextRedeem advanced only after payout**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): LootBot AI’s xLoot NFT Staking contract was exploited via a Logic Error (Duplicate NFT ID in Redemption). The redeem() function did not validate duplicate token IDs in the input array. The _redeemable() logic accumulated ETH rewards per epoch for each ID without checking for duplicates, and the nextRedeem mapping was only updated after payout. The attacker flash-loaned 2.1 ETH, triggered a new epoch, called redeem() with 7 NFT IDs each duplicated 155 times, draining ~6.21 ETH. After repaying the flash loan, net profit was ~4.1 ETH ($9,600). The project appears largely abandoned (last official X activity in 2025).

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/XLootStaking_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Balancer flash loan (2.1 ETH) to trigger a new epoch; xLOOT NFT

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 2.31y old; project abandoned (last official activity 2025)

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 151. Hyperbridge — 2026-04-13

**SlowMist line:** Smart Contract Vulnerability · $ 2,500,000 · [reference](https://x.com/CertiKAlert/status/2043557571609731268)

**Classification:** Ethereum(+Base/BSC/Arb): MMR VerifyProof() does not enforce leaf_index < leafCount

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 2,500,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **cross-chain token gateway**

### Actual logic and exploited mechanism

- Flaw class: **MMR proof forgery — VerifyProof() does not enforce leaf_index < leafCount**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Based on monitoring by CertiK Alert, the Hyperbridge gateway contract fell victim to an exploit. The attacker utilized forged messages to manipulate administrative permissions of the Polkadot token contract on the Ethereum network. By unauthorized minting and liquidating 1 billion tokens, the attacker realized a profit of roughly $237,000. On April 16, it was reported that according to an official announcement from Hyperbridge, its token gateway was attacked on April 13. The estimated losses have been revised from approximately $237,000 to about $2.5 million, mainly affecting incentive liquidity pools on Ethereum, Base, BNB Chain, and Arbitrum.

### Interaction graph

- Token Gateway on Ethereum/Base/BSC/Arbitrum; bridged DOT ERC-20 admin/minter roles; incentive liquidity pools

### Fork / codebase lineage

- Hyperbridge/ISMP codebase

### Observable pre-hack flags

- verifier accepts an out-of-range leaf index; gateway holds mint authority over the bridged asset

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 153. MONA — 2026-04-13 *(borderline)*

**SlowMist line:** Reserve Manipulation Attack · $ 60,950 · [reference](https://www.darknavy.org/web3/exploits/burnaddress-mona-deferred-lp-burn/)

**Classification:** BSC: LisaVault referral tiers self-dealt via proxy contracts, but stage 1 was the deployer redeeming their own LP

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited vault | [`0xaEa6E5CA6c1FeeAbBd3A114BCbca30A21424F76b`](https://bscscan.com/address/0xaEa6E5CA6c1FeeAbBd3A114BCbca30A21424F76b) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |
| token | [`0x311838c073a865E8249F5C35E4cb2a5f815a36e8`](https://bscscan.com/address/0x311838c073a865E8249F5C35E4cb2a5f815a36e8) | bsc | yes | no |

### Age at time of hack

- **exploited vault** `0xaEa6E5CA6c...` created **2026-03-07 13:49:04 UTC**, exploited 2026-04-13 -> **dwell 36 days (0.10 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x0cbbb6f15ff6aeb7...`](https://bscscan.com/tx/0x0cbbb6f15ff6aeb71fdfe3424979b898d5725000058b1022253c6fe73606001a).

- **token** `0x311838c073...` created **2026-04-13 03:24:03 UTC**, exploited 2026-04-13 -> **dwell 0 days (0.00 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x4d2e2e1c54d9ddac...`](https://bscscan.com/tx/0x4d2e2e1c54d9ddaca241b5d733634c8d1a182ce45b0692f42d7ac49cbc9bbce0).
- Exploit block confirmed on-chain: bsc block 92429267 at **2026-04-14 05:18:26 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 60,950; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **node-staking vault**

### Actual logic and exploited mechanism

- Flaw class: **referral-tier self-dealing via proxy contracts bypassing a 1-node-per-address limit**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): On April 14, 2026, attackers exploited the BurnAddress mechanism in the MONA token on BSC via a Deferred LP Burn / reserve manipulation attack. The attacker first farmed 10,000 MONA through 25 fresh accounts, sold 9,900 MONA to create a deferred burn credit, bought out most of the pool's MONA inventory, then triggered BurnAddress.burn() with a zero-value transferFrom to burn MONA directly from the LP and call sync(). This left the MONA/USDT pair with near-zero MONA but almost full USDT reserves. Finally, selling the remaining ~100 MONA drained a large amount of USDT. Flash loans from Moolah and borrowing from Venus were used for funding and fully repaid in the same transaction. The root cause was non-atomic handling in _handleSell() and burnsellMona(): USDT payout happened immediately while MONA burn was deferred and could be triggered later, breaking the AMM invariant.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/MONA_LisaVault_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- PancakeSwap MONA/USDT LP; Moolah flash loan; deployer-controlled LP

### Fork / codebase lineage

- hand-rolled node/referral vault

### Observable pre-hack flags

- vault 36d old, token 1d old; per-address limit enforced only on tx.origin-style identity

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 154. SubQuery Network — 2026-04-12

**SlowMist line:** Smart Contract Vulnerability · $ 134,000 · [reference](https://subquery.network/blog/subquery-network-security-incident-report)

**Classification:** Base: Settings.setContractAddress()/setBatchAddress() missing onlyOwner after a refactor

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited config | [`0xf282737992Da4217bf5f8B6AE621181e84d7d3b9`](https://basescan.org/address/0xf282737992Da4217bf5f8B6AE621181e84d7d3b9) | base | yes | no |
| drained staking | [`0x7A68b10EB116a8b71A9b6f77B32B47EB591B6Ded`](https://basescan.org/address/0x7A68b10EB116a8b71A9b6f77B32B47EB591B6Ded) | base | yes | impl `0x27aa37ad388ee3f559016aea806c5bcc98e37e70` |

### Age at time of hack

- **exploited config** `0xf282737992...` created **2024-02-13 08:42:55 UTC**, exploited 2026-04-12 -> **dwell 788 days (2.16 y)**.
  Source: binary-search eth_getCode on archive RPC (https://base-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xa890d68e5358b09f...`](https://basescan.org/tx/0xa890d68e5358b09f73ae6a9bd626ca14cfcad808dcd9227b555592d611dcec19).

- **drained staking** `0x7A68b10EB1...` created **2024-02-13 09:10:19 UTC**, exploited 2026-04-12 -> **dwell 788 days (2.16 y)**.
  Source: binary-search eth_getCode on archive RPC (https://base-mainnet.public.blastapi.io) + block timestamp. creation tx [`0x5e0776ea3f831416...`](https://basescan.org/tx/0x5e0776ea3f8314161450dec12512b2e3bf894ecfc90aebbcf45900e7b14c6c25).
- Exploit block confirmed on-chain: base block 44590468 at **2026-04-12 05:04:43 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 134,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **staking/rewards config**

### Actual logic and exploited mechanism

- Flaw class: **missing onlyOwner on a setter after a refactor**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Attackers exploited a vulnerability in SubQuery Network’s Settings contract on the Base network (the setContractAddress() function missing the onlyOwner access control modifier). By repeatedly calling this function, the attacker set their address as StakingManager and RewardsDistributor, enabling drainage of pooled SQT from the Staking contract, impacting 272 individual staker/delegator wallets, RewardsBooster, and a small protocol Treasury. Approximately 382,433,441 SQT were drained (worth about $134,000 USD at the time). The team quickly responded by deploying a fix, pausing withdrawals, and committing to full compensation for all affected users. No user private keys were compromised. The root cause was a missing access control from a prior code refactor.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/SubQuerySettings_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- Settings contract addresses consumed by Staking/RewardsDistributor; 272 staker wallets

### Fork / codebase lineage

- SubQuery Network codebase

### Observable pre-hack flags

- 2.16y old; access-control regression introduced by a refactor

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 156. Aethir — 2026-04-09

**SlowMist line:** Smart Contract Vulnerability · $ 90,000 · [reference](https://crypto.news/aethir-contains-bridge-hack-while-losses-stay-below-90k/)

**Classification:** BSC: AethirOFTAdapter ownership transfer reachable due to missing/bypassed onlyOwner

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 90,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **OFT bridge adapter**

### Actual logic and exploited mechanism

- Flaw class: **ownership transfer reachable due to missing/bypassed onlyOwner**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Aethir's cross-chain bridge contracts (primarily AethirOFTAdapter and Ethereum-related bridging contracts) were targeted in an exploit. The attacker attempted to drain funds by exploiting access control or ownership transfer vulnerabilities (e.g., transferOwnership issues), involving chains like BNB Chain. The Aethir team quickly detected the anomaly, promptly disconnected the compromised contracts, and collaborated with major exchanges (Binance, Upbit, Bithumb, etc.) to blacklist attacker wallets, effectively containing further damage. The main ATH token supply on Ethereum remained intact, and other bridges like ETH-ARB on Squid were unaffected. Initial estimates put potential losses around $400,000, but user impact was limited to under $90,000. The project promised a full compensation plan.

### Interaction graph

- LayerZero OFT adapter for ATH; Symbiosis bridge exit

### Fork / codebase lineage

- LayerZero OFT adapter template

### Observable pre-hack flags

- adapter holds bridge mint/lock authority

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 157. Squid Multicall — 2026-04-07 *(borderline)*

**SlowMist line:** Approval Exploit · $ 517,000 · [reference](https://blocksec.com/blog/weekly-web3-security-incident-roundup-apr-6-apr-12-2026)

**Classification:** BSC(+multi): SquidMulticall.run() is permissionless by design; victim had approved it — design flaw, not a code bug

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited multicall | [`0xad6cea45f98444a922a2b4fe96b8c90f0862d2f4`](https://bscscan.com/address/0xad6cea45f98444a922a2b4fe96b8c90f0862d2f4) | bsc | None | no |

### Age at time of hack

- **exploited multicall** `0xad6cea45f9...` created **2024-10-01 02:14:47 UTC**, exploited 2026-04-07 -> **dwell 552 days (1.51 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx **not resolvable** (factory `CREATE` with no constructor logs).
- Exploit block confirmed on-chain: bsc block 91122249 at **2026-04-07 09:41:40 UTC** (fetched via `eth_getBlockByNumber`).

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 517,000; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **multicall executor (router family)**

### Actual logic and exploited mechanism

- Flaw class: **permissionless arbitrary-call runner over victim approvals (design, not code bug)**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): A user mistakenly approved the SquidMulticall contract (instead of the intended Squid Router contract) with unlimited token allowances. An attacker then called the permissionless run() function on SquidMulticall with crafted calldata to execute transferFrom() from the victim’s approved tokens across multiple chains (ETH, BSC, Arbitrum, Avalanche, etc.). This drained approximately $517K.

- Independent reproduction reviewed: DeFiHackLabs `src/test/2026-04/SquidMulticallAllowanceDrain_exp.sol` — contains the exploit tx hash, the victim addresses and a trace-verified root cause.

### Interaction graph

- SquidMulticall.run() executing transferFrom against victim approvals across ETH/BSC/Arbitrum/Avalanche

### Fork / codebase lineage

- Squid router codebase

### Observable pre-hack flags

- PRE-HACK OBSERVABLE: a permissionless arbitrary-call contract that users can approve; ~$800K of approvals at risk

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 158. TGAI — 2026-04-07

**SlowMist line:** Reserve Manipulation Attack · $ 11,940 · [reference](https://x.com/exvulsec/status/2041447720016396698)

**Classification:** BSC: TGAI reserve manipulation via sync() on the Pancake V2 pair

### Identity and address

- **Exploited contract address: NOT RECOVERED.** No public write-up, PoC or explorer trail reached from
  free-tier sources named the contract. Recorded as a gap rather than guessed.

### Age at time of hack

- **Creation date unrecoverable** — the contract itself was not identified, so no creation transaction could be pinned.

### What it held and controlled

- Not independently confirmed on-chain by this study. SlowMist's headline figure is $ 11,940; treat it as an upper bound — several entries in this population conflate gross routed volume, arbitrage and actual theft.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **reserve manipulation via sync() on the pair**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): Computility-associated TGAI project on BSC suffered a reserve manipulation attack on PancakeSwap V2 liquidity pool. The hacker used a ~$2.4M USDT flash loan, deployed multiple helper contracts to buy TGAI, manipulated reserves via sync() function with ~17.5K USDT injection, then swapped to extract profits, resulting in approximately $11.94K loss.

### Interaction graph

- PancakeSwap V2 TGAI pool; ~$2.4M USDT flash loan; multiple helper contracts

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- same operator family as YSDAO (Computility-associated)

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.

---

## 160. BSC TMM/USDT — 2026-04-04

**SlowMist line:** Reserve Manipulation Attack · $ 1,665,000 · [reference](https://x.com/exvulsec/status/2040649377803546859)

**Classification:** BSC: TMM burned to dead address to collapse the pair reserve to 1 TMM, then swapped out

### Identity and address

| role | address | chain | verified | proxy |
|---|---|---|---|---|
| **->** exploited token | [`0x1d6f03b0b20b2ec05b37bf60f56af442ced66666`](https://bscscan.com/address/0x1d6f03b0b20b2ec05b37bf60f56af442ced66666) | bsc | yes | impl `0x39ca57388b3390b772607ad421b5673d959c7fee` |
| drained pool | [`0xc36c718e7d0af055092e5274f92f6511820ca041`](https://bscscan.com/address/0xc36c718e7d0af055092e5274f92f6511820ca041) | bsc | not in Sourcify (BscScan status not checkable — see Method) | no |

### Age at time of hack

- **exploited token** `0x1d6f03b0b2...` created **2026-03-11 12:51:27 UTC**, exploited 2026-04-04 -> **dwell 23 days (0.06 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx [`0xc6742b2e240c6c73...`](https://bscscan.com/tx/0xc6742b2e240c6c7380ece829627c6bb16de2be605a30754e4de6447d5c8811e3).

- **drained pool** `0xc36c718e7d...` created **2026-03-11 12:51:27 UTC**, exploited 2026-04-04 -> **dwell 23 days (0.06 y)**.
  Source: binary-search eth_getCode on archive RPC (https://bsc-mainnet.public.blastapi.io) + block timestamp. creation tx **not resolvable** (factory `CREATE` with no constructor logs).

### What it held and controlled

- TMM/USDT pair reserves: ~272M USDT swapped out, ~1.665M USDT net after repaying five separate flash-loan sources.

### What it was supposed to do

- Category: **custom token**

### Actual logic and exploited mechanism

- Flaw class: **burn-to-dead collapses the pair reserve to 1 token**

- Full mechanism (SlowMist blurb, cross-checked against the primary sources below): According to ExVul monitoring, a TMM/USDT reserve manipulation attack occurred on the BSC (BNB Chain), resulting in a loss of approximately 1.665 million USDT. The attacker utilized flash loans from Lista DAO Moolah, Venus, Aave V3, PancakeSwap Vault, and Uniswap PoolManager to manipulate the TMM/USDT trading pair. By burning TMM to a dead address, the attacker reduced the pair's reserve to just 1 TMM, subsequently swapping 850 million TMM for approximately 272 million USDT. After repaying all flash loans, the attacker transferred a net profit of roughly 1.665 million USDT to associated addresses.

### Interaction graph

- PancakeSwap TMM/USDT pair 0xc36c718e..; flash loans from Moolah, Venus, Aave V3, Pancake Vault, Uniswap PoolManager

### Fork / codebase lineage

- hand-rolled

### Observable pre-hack flags

- 23 days old at exploit

### Prior review status

- No audit report, bug-bounty programme or prior public security review was located from the sources consulted. Recorded as *not evidenced* rather than *proven absent*.
