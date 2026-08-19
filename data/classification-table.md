# Classification of all 160 SlowMist entries (pages 1-8, 2026-04-04 to 2026-08-18)

Scope kept: a bug in an EVM contract's own code, on BNB Chain / Ethereum / Arbitrum / Base, reached by an unprivileged attacker.

Totals: **72 KEEP + 7 KEEP(borderline) = 79 in scope**, **81 discarded**.

| # | Date | Target | Loss (SlowMist) | SlowMist method label | Verdict | Reason |
|---:|---|---|---|---|---|---|
| 1 | 2026-08-18 | Maya Protocol | $ 1,700,000 | Smart Contract Vulnerability | **discard** | Cosmos/THORChain-fork app-chain state machine (Trade Account, pool math) — no EVM contract |
| 2 | 2026-08-15 | FoxMarket | $ 118,700 | Flash Loan Attack | **KEEP** | BSC: FoxLpBondsPool.stake() prices LP bond off manipulable Pancake spot quote |
| 3 | 2026-08-11 | Harmony Protocol | $ 3,200,000 | Protocol Logic Vulnerability | **discard** | Layer-1 consensus/validator bug (empty-block minting) — not contract code |
| 4 | 2026-08-10 | USM | $ 136,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: USM defund() split-invariance / rounding in FUM redemption curve |
| 5 | 2026-08-09 | Coinsbuy | $ 7,900,000 | Unknown | **discard** | Payment-processor wallet drain, cause undisclosed; no contract vuln identified |
| 6 | 2026-08-09 | Oraichain | - | Cross-Chain Bridge Exploit | **discard** | Oraichain (Cosmos app-chain) native EVM module mint path — not a target chain |
| 7 | 2026-08-09 | Coreum Bridge | $ 200,000 | Bridge Logic Vulnerability | **discard** | XRPL/Coreum relayer deposit-verification logic — off-chain + non-target chain |
| 8 | 2026-08-08 | Atomic Green | $ 29,984.27 | Signature Replay Attack | **KEEP** | Arbitrum: manager-signature replay across 21 UniV3 LP positions + spot-price valuation |
| 9 | 2026-08-06 | RRWallet | $ 2,000,000 | Supply Chain Attack | **discard** | Weak RNG in CryptoJS dependency — supply-chain/key predictability |
| 10 | 2026-08-06 | Unistreets | $ 17,750 | Smart Contract Vulnerability | **KEEP** | Ethereum: LaunchpadFactoryAuto.launch() forwards attacker calldata to V4 PositionManager |
| 11 | 2026-08-05 | ZEUS | 0 | Infrastructure Compromise | **discard** | Lightning/LSP infrastructure compromise |
| 12 | 2026-08-03 | RISEx | $ 673,011.56 | Smart Contract Vulnerability | **KEEP** | RWA strategy behind XLP vault, misconfiguration since deployment — contract-side, chain unconfirmed |
| 13 | 2026-08-02 | LOOPSDAO | $ 690000 | Price Manipulation | **KEEP** | BSC: LpdFi buy()/claimInterest() priced off thin Pancake LPD/USDC spot reserves |
| 14 | 2026-08-02 | MOKE | $ 907700 | Smart Contract Vulnerability | **KEEP** | BSC: unprotected public claim() in MokeReleaseContract drains reserve pool |
| 15 | 2026-07-30 | Coldcard | $ 100000000 | Firmware Vulnerability | **discard** | Hardware-wallet firmware entropy bug |
| 16 | 2026-07-30 | Set Protocol | $ 9,600 | Smart Contract Vulnerability | **KEEP** | Ethereum: ExchangeIssuance TOCTOU on SetToken positionMultiplier via attacker manager hook |
| 17 | 2026-07-30 | Swan Treasury | $ 625,000 | Private Key Leakage | **KEEP (borderline)** | BSC: signer key hardcoded in ZhaiquanBuy leaked, but buy() has no discount floor/bounds check — on-chain contract defect, off-chain trigger |
| 18 | 2026-07-28 | Crypto DAO | $ 52,000 | Smart Contract Vulnerability | **KEEP** | BSC: Pro token reward-on-transfer self-dealing, permissionless player/winner registration |
| 19 | 2026-07-28 | LULA | $ 578,100 | Price Manipulation Attack | **KEEP** | BSC: LULA public claimReward()/recycle() redeems against attacker-deflated pool |
| 20 | 2026-07-26 | WEMIX | $ 6,250,000 | Private Key Leakage | **discard** | Contract owner privileges compromised (key) to mint WEMIX$ |
| 21 | 2026-07-26 | Garden Finance | $ 450,000 | Supply Chain Attack | **discard** | Independent solver off-chain database compromised; HTLC contracts behaved correctly |
| 22 | 2026-07-26 | ChainConnect | $ 650,000 | Unauthorized Access | **discard** | Unauthorized access to bridge operator credentials |
| 23 | 2026-07-25 | Bankrbot | $ 479,885 | Account Compromise | **discard** | X account + wallet compromise |
| 24 | 2026-07-25 | Projekt | $ 560000 | Flash Loan Attack | **KEEP** | Ethereum: permissionless trackPurchase() sizes rewards from balance deltas, no payment check |
| 25 | 2026-07-24 | Lien Finance | $ 542,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: permissionless registerNewBond + crafted payoff mispriced by bondPricer |
| 26 | 2026-07-24 | Triple-A | $ 11,800,000 | Hot Wallet Compromise | **discard** | Hot-wallet compromise |
| 27 | 2026-07-23 | Verus Ethereum Bridge | $ 7,540,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: Verus bridge import path mints unbacked payouts (repeat of the May flaw) |
| 28 | 2026-07-23 | Solido Cash | $ 73,400 | Oracle Misassignment | **discard** | Supra chain — not a target chain |
| 29 | 2026-07-22 | AFX Bridge | $ 24,150,000 | Private Key Leakage | **discard** | Compromised validator hot keys met the quorum |
| 30 | 2026-07-22 | 42DAO | $ 915,000 | Price Oracle Manipulation | **KEEP** | BSC: MakerDAO-fork Median Oracle/Spotter poke with no deviation or floor checks |
| 31 | 2026-07-21 | FlashTrade | $ 98,000 | Unknown | **discard** | Solana perps |
| 32 | 2026-07-21 | Wanchain Cardano-BNB Chain Bridge | $10,000,000 | Smart Contract Vulnerability | **discard** | Cardano-side lock address drained — not a target chain |
| 33 | 2026-07-19 | Allbridge Core | $ 1,650,000 | Flash Loan Price Manipulation | **discard** | Solana liquidity pools |
| 34 | 2026-07-19 | Zilliqa exchange partner | - | Private Key Leakage | **discard** | Ledger app nonce-generation flaw leaking keys |
| 35 | 2026-07-17 | Across | 0 | Deposit signal spoofing | **discard** | Solana event spoofing against off-chain relayer |
| 36 | 2026-07-16 | DefiTuna Lending | $ 580,000 | Smart Contract Vulnerability | **discard** | Solana lending |
| 37 | 2026-07-15 | Ostium | $ 18,000,000 | Private Key Leakage | **discard** | Compromised oracle signer key; contract behaved as designed |
| 38 | 2026-07-15 | TeleSwap | $ 735,000 | Unknown | **discard** | Bitcoin hot wallet outflow, undisclosed cause |
| 39 | 2026-07-15 | BarnBridge | $ 776,000 | Governance Attack | **KEEP** | Ethereum: abandoned BarnBridge governance captured, proxy re-pointed to sweep impl over live approvals |
| 40 | 2026-07-15 | Cascade | $ 1,343,921 | Price Manipulation | **KEEP (borderline)** | Arbitrum: mark-price manipulation in a thin pre-launch CLS market — economic/pricing design, on-chain |
| 41 | 2026-07-14 | Drips Network | $ 24,900 | Smart Contract Vulnerability | **KEEP** | Ethereum: DaiDripsHub.give() unchecked uint128->int128 cast flips transfer direction |
| 42 | 2026-07-13 | Lumi Finance | $ 270,000 | Smart Contract Logic Vulnerability | **KEEP** | Arbitrum: Sodium ERC-4337 account grants approvals during UserOp validation; session-key validation bypass |
| 43 | 2026-07-13 | Chi Protocol | $ 8,500 | Smart Contract Logic Vulnerability | **KEEP** | Ethereum: Chi ArbitrageV5.burn() redeems at hardcoded $1 peg with no spot check (mint() has one) |
| 44 | 2026-07-11 | Bonzo Lend | $ 9,050,000 | Oracle Price Manipulation | **discard** | Hedera — not a target chain; third-party oracle feed |
| 45 | 2026-07-06 | Lazy Summer Protocol | $ 6,040,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: FleetCommander NAV = live sum of Ark totalAssets() with no manipulation guard |
| 46 | 2026-07-06 | BonkDAO | $ 20,000,000 | Governance Attack | **discard** | Solana DAO governance — tokens bought, no contract bug |
| 47 | 2026-07-02 | Hinkal | $ 820,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: Hinkal prooflessDeposit()/transact() note-to-nullifier binding failure (double-spend) |
| 48 | 2026-07-01 | Edel Finance | $ 403,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: Edel lending values wrapped xStock via mutable ERC4626 convertToAssets() |
| 49 | 2026-06-28 | AIDC | $ 121,000 | Smart Contract Vulnerability | **KEEP** | BSC: AIDCToken lets ordinary transfers burn accumulated sell amounts out of the AMM pair |
| 50 | 2026-06-25 | Polymarket | $ 3,100,000 | Supply Chain Attack | **discard** | Frontend supply-chain script injection |
| 51 | 2026-06-25 | Lixir Finance | $ 12,300 | Smart Contract Vulnerability | **KEEP** | Ethereum: Lixir vault-token permit accepts a dummy signature (only checks ecrecover != 0) |
| 52 | 2026-06-24 | Yield Yak | - | Frontend Attack | **discard** | Frontend/subdomain drainer injection |
| 53 | 2026-06-23 | SecondFi | $ 2,400,000 | Predictable Private Key Exploit | **discard** | Cardano wallet key-generation flaw |
| 54 | 2026-06-23 | Royal.io | $ 263,000 | Smart Contract Vulnerability | **discard** | Polygon — not a target chain |
| 55 | 2026-06-21 | Gitcoin | - | Front-end Attack | **discard** | Frontend/subdomain drainer injection |
| 56 | 2026-06-21 | Taiko Bridge | $ 1,700,000 | Private Key Leakage | **discard** | Forged SGX attestation / prover registration — proof-system and infrastructure, not reachable contract logic |
| 57 | 2026-06-21 | Quicksilver Zone | $ 3,500 | Smart Contract Vulnerability | **discard** | Cosmos app-chain proof minting |
| 58 | 2026-06-20 | MEV Bot | $ 7,500,000 | Business Logic Flaw | **discard** | Off-chain MEV bot approval-generation logic; SlowMist explicitly states victim contracts were not vulnerable |
| 59 | 2026-06-20 | LABUBU/OLPC | $ 1,100,000 | Smart Contract Vulnerability | **KEEP** | BSC: OLPC _update() burns pair balance and desyncs reserves; owner had set an absurd decimalsValue 46d earlier |
| 60 | 2026-06-19 | Namada Shielded Pools | $ 600,000 | Protocol Vulnerability | **discard** | Namada MASP/IBC — not a target chain |
| 61 | 2026-06-19 | mySwap CL | $ 300,000 | Smart Contract Vulnerability | **discard** | Starknet — not a target chain (non-EVM) |
| 62 | 2026-06-19 | JB | $ 50,000 | Flashloan Price Manipulation | **KEEP** | BSC: JB helper uses live JB balance to sell/burn/sync through the JB/USDT pair |
| 63 | 2026-06-17 | Aztec Bridge | $ 2,160,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: Aztec RollupProcessorV2 immutable escape hatch publishes an unconstrained proof_id |
| 64 | 2026-06-17 | Little Boy Plus | $ 367,000 | Smart Contract Vulnerability | **KEEP** | BSC: LBPHashrate._update() reachable via zero-value transferFrom, mints reward into the pair |
| 65 | 2026-06-17 | DIP | $ 111,000 | Smart Contract Vulnerability | **KEEP** | BSC: DIP _transfer() missing return for router-routed trades causes double transfer |
| 66 | 2026-06-15 | Thetanuts Finance | $ 105,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: Thetanuts legacy index vault mint/claim redemption math with zeroed component transfers |
| 67 | 2026-06-14 | Aztec Connect | $ 2,100,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: Aztec Connect Decoder numRealTxs proven-vs-settled mismatch; processRollup permissionless |
| 68 | 2026-06-10 | Raydium | $ 1,340,000 | Smart Contract Vulnerability | **discard** | Solana AMM program |
| 69 | 2026-06-10 | Secret Network | $ 4,670,000 | Smart Contract Vulnerability | **discard** | Secret Network CosmWasm contract — not a target chain |
| 70 | 2026-06-09 | Humanity Protocol | $ 31,000,000 | Private Key Leakage | **discard** | Foundation member private keys compromised |
| 71 | 2026-06-09 | Asterix Labs | $ 40,000 | Smart Contract Vulnerability | **KEEP** | DN404/BT404 shared-codebase ownership/underflow flaw in an Asterix fork of Flooring |
| 72 | 2026-06-09 | Haedal Vault | $ 915,179 | Smart Contract Vulnerability | **discard** | Sui Move contracts — not a target chain |
| 73 | 2026-06-09 | NovaBox | $ 93,600 | Flash Loan Attack | **KEEP** | Ethereum: NovaBox adds dual depositors to the dividend list without initialising checkpoints |
| 74 | 2026-06-09 | Token of Power | $ 1,580,000 | Malicious Governance Takeover | **KEEP (borderline)** | Ethereum: Aragon DAO with 16,384 TOP supply and no timelock; mint proposal created+voted+executed in one tx |
| 75 | 2026-06-08 | Syscoin Bridge | $ 10,000,000 | Bridge Verification Flaw | **discard** | Syscoin UTXO-side minting — not a target chain |
| 76 | 2026-06-08 | Flooring Protocol & BitmapPunks | - | Smart Contract Vulnerability | **KEEP** | Ethereum: Flooring V2 / BT404 packed-ownership alias + underflow mints near-infinite fpTokens |
| 77 | 2026-06-08 | Ambient Finance | $ 110,600 | Smart Contract Vulnerability | **KEEP** | Ethereum: Ambient surplus-collateral accounting across HotProxy/WarmPath/ColdPath |
| 78 | 2026-06-08 | OpenMonero P2P | $ 62,900 | Supply Chain Attack | **discard** | Server root compromise |
| 79 | 2026-06-05 | DTXT/USDT liquidity pair on BSC | $ 35,041 | Business Logic Vulnerability | **KEEP** | BSC: DTXT forgeable add-liquidity detection bypasses sell fees |
| 80 | 2026-06-04 | ATM | $ 243,500 | Smart Contract Vulnerability | **KEEP** | BSC: ATMToken._transfer() auto-dumps 20% of its own reserves at amountOutMin=0; per-address guards farmable |
| 81 | 2026-06-04 | BYToken | $ 87,402 | Smart Contract Vulnerability | **KEEP** | BSC: permissionless triggerAutoBurn() burns from the pair then sync()s reserves |
| 82 | 2026-06-03 | ApeBond | $ 3,421 | Smart Contract Vulnerability | **KEEP** | BSC: ApeYieldVault.migrateToVotingEscrow accepts duplicate pool IDs, inflating the lock |
| 83 | 2026-06-01 | Gnosis Pay | 0 | Smart Contract Vulnerability | **discard** | Gnosis Chain — not a target chain |
| 84 | 2026-06-01 | The X account of crypto KOL Jadoodoo | $ 5000 | Social Engineering | **discard** | Social engineering / phishing DMs |
| 85 | 2026-06-01 | TESSERA | $ 2,400,000 | Private Key Leakage | **discard** | Core contract control obtained (key compromise) to mint TSR |
| 86 | 2026-06-01 | ATOHook | $ 25,000 | Smart Contract Vulnerability | **KEEP** | Storage-slot collision between a rewards mapping and Solady ReentrancyGuard fixed slot in getReward() |
| 87 | 2026-05-31 | Fluid | $ 215,000 | Private Key Leakage | **discard** | Off-chain Merkle proposer/approver keys compromised |
| 88 | 2026-05-31 | Phala Cloud | 0 | API endpoint vulnerability | **discard** | Cloud API endpoint vulnerability |
| 89 | 2026-05-30 | Gravity Bridge | $ 5,400,000 | Private Key Leakage | **discard** | Contract key / signing authority compromised |
| 90 | 2026-05-30 | Alephium Bridge | $ 815,000 | Off-Chain Vulnerability in the Bridge Backend | **discard** | Bridge backend message forgery — off-chain |
| 91 | 2026-05-30 | AROS | $ 295,300 | Smart Contract Vulnerability | **KEEP** | BSC: AROS token/pool logic drained via the AROS/USDT Pancake pair |
| 92 | 2026-05-29 | MoneyMon | $ 85,519.47 | Smart Contract Vulnerability | **KEEP** | BSC: cliamRewred() verify() accepts ecrecover==address(0) against a zeroed admin |
| 93 | 2026-05-29 | YSDAO | $ 19,500 | Reserve Manipulation Attack | **KEEP** | BSC: YSDAO Staking.sync() has no access control; add/remove-liquidity detection is forgeable |
| 94 | 2026-05-28 | Joe Agent | $ 45,000 | Reentrancy Attack | **KEEP** | BSC: removeLiquidityViaContract sends BNB before zeroing lpInfo — classic reentrancy |
| 95 | 2026-05-28 | DxSale | $ 7,300,000 | Ownership Override Attack | **KEEP (borderline)** | BSC: undisclosed owner-only DXLOCKERLP backdoor in an unverified locker, but the actor held ownership |
| 96 | 2026-05-28 | ONTR | $ 98,200 | Smart Contract Vulnerability | **KEEP** | onlyOwner check accepts owner == address(0), letting anyone re-own a renounced token |
| 97 | 2026-05-27 | Stake DAO | $ 91,000 | Private Key Leakage | **discard** | Deployer EOA private key compromised |
| 98 | 2026-05-27 | Superfortune | $ 15180000 | Multisig Address Tampering | **discard** | Multisig transaction recipient tampering |
| 99 | 2026-05-26 | SKP | $ 212,850 | Smart Contract Vulnerability | **KEEP (borderline)** | BSC: SKP _runSpecialPairFlow redistributes unbounded treasury to a whitelisted address the owner set 6d prior — insider-engineered |
| 100 | 2026-05-25 | WUSD.fi / GLOVE | $ 200,000 | Sybil Attack | **KEEP** | Ethereum: WUSD._englove has no per-address claim ledger — Sybil-farmable uncapped subsidy |
| 101 | 2026-05-25 | Third-party Gnosis Safe Module (SquidRouterMod | $ 3,200,000 | Smart Contract Vulnerability | **KEEP** | Ethereum+Base: Safe module trusts a caller-supplied sourceAddress string on the permissionless Axelar express path |
| 102 | 2026-05-24 | StablR | $ 2,800,000 | Private Key Leakage | **discard** | Issuer contract keys suspected compromised |
| 103 | 2026-05-23 | Mure | $ 11,700 | Smart Contract Vulnerability | **KEEP** | Ethereum: SignatureChecker given an attacker-supplied signer source returns true |
| 104 | 2026-05-22 | Polymarket | $ 573,200 | Private Key Leakage | **discard** | Six-year-old operational wallet private key compromised (Polygon) |
| 105 | 2026-05-22 | Fractal Protocol | $ 13,700 | Smart Contract Vulnerability | **KEEP** | Arbitrum: USDF vault re-entrant deposit/withdraw against a fixed daily tokenPrice with share rounding |
| 106 | 2026-05-20 | Butter Bridge | $ 180,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: abi.encodePacked hash collision in OmniServiceProxy retry-message verification |
| 107 | 2026-05-20 | RetoSwap | $ 2,700,000 | Protocol Logic Vulnerability | **discard** | Tor P2P client message spoofing (Monero) |
| 108 | 2026-05-19 | Bankr | $ 440,000 | Social Engineering | **discard** | Prompt-injection social engineering of an agent |
| 109 | 2026-05-19 | HermesVault | $ 29,466 | Smart Contract Vulnerability | **discard** | Algorand — not a target chain |
| 110 | 2026-05-18 | Verus-Ethereum Bridge | $ 11,580,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: Verus bridge import path (first exploitation of the flaw re-hit in July) |
| 111 | 2026-05-18 | Echo Protocol | $ 821,700 | Private Key Leakage | **discard** | Monad admin key leak; also not a target chain |
| 112 | 2026-05-17 | SEA Token | $ 153,000 | Flashloan Price Manipulation | **KEEP** | Arbitrum: MetaSea RedeemPosition distributor drained via flash-loan-manipulated pricing |
| 113 | 2026-05-15 | THORChain | $ 10,700,000 | GG20 TSS Vulnerability | **discard** | GG20 TSS key-material leakage |
| 114 | 2026-05-15 | Adshares Bridge | $ 628,000 | Bridge Verification Bypass | **discard** | Bridge-minter EOA signed the fake wrapTo() calls — key compromise |
| 115 | 2026-05-13 | Transit Finance | $ 1,880,000 | Smart Contract Vulnerability | **discard** | TRON — not a target chain |
| 116 | 2026-05-13 | ShapeShift FOX Colony | $ 132,700 | Smart Contract Vulnerability | **KEEP** | Arbitrum: Colony EtherRouter meta-transaction self-call defeats DSAuth |
| 117 | 2026-05-12 | Aurellion Labs | $ 456,000 | Smart Contract Vulnerability | **KEEP** | Arbitrum: EIP-2535 diamond with an initialize(address) selector whose _initialized slot stayed 0 |
| 118 | 2026-05-12 | SQ Protocol | $ 346,100 | Smart Contract Vulnerability | **KEEP** | BSC: hardcoded backdoor in the verified Staking contract, reached with an EIP-7702 type-4 tx |
| 119 | 2026-05-11 | Huma Finance | $ 101,400 | Smart Contract Vulnerability | **discard** | Polygon — not a target chain |
| 120 | 2026-05-11 | Ink Finance | $ 140,000 | Smart Contract Vulnerability | **discard** | Polygon — not a target chain |
| 121 | 2026-05-11 | TAC | $ 2,854,000 | Smart Contract Vulnerability | **discard** | TON side of the cross-chain layer |
| 122 | 2026-05-11 | Roaring Kitty‘s X account | 0 | The X account was hacked | **discard** | X account compromise |
| 123 | 2026-05-10 | Renegade | $ 209,000 | Smart Contract Vulnerability | **KEEP** | Arbitrum: unprotected initializer on the V1 Dark Pool proxy after a desynced migration |
| 124 | 2026-05-07 | TrustedVolumes | $ 6,700,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: permissionless registerAllowedOrderSigner + authorization keyed on taker instead of maker |
| 125 | 2026-05-05 | Ekubo Protocol | $ 1,400,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: IPayer.pay callback takes payer/token/amount from the lock payload without checking the lock initiator |
| 126 | 2026-05-04 | SmartCredit | $ 72,000 | Smart Contract Vulnerability | **KEEP** | Leveraged Lido module drained; mechanism not publicly detailed |
| 127 | 2026-05-01 | Bisq v1 | $ 876,000 | Business Logic Vulnerability | **discard** | Bitcoin P2P trade protocol / modified clients |
| 128 | 2026-04-30 | Wasabi Protocol | $ 5,700,000 | Private Key Leakage | **discard** | AWS Spring Boot Actuator heap dump leaked the contract keys |
| 129 | 2026-04-29 | Syndicate Labs | $ 380,000 | Private Key Leakage | **discard** | Upgrade key leaked, used to upgrade the bridge |
| 130 | 2026-04-29 | Sweat Foundation | $ 3,500,000 | Smart Contract Vulnerability | **discard** | SWEAT is a NEAR-ecosystem token; drain and laundering ran through Ref Finance/Wormhole |
| 131 | 2026-04-29 | Aftermath Finance | $ 1,140,000 | Smart Contract Vulnerability | **discard** | Sui Move perps |
| 132 | 2026-04-28 | YieldCore | $ 398,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: RWAVault overrides ERC4626 withdraw without the allowance spend when msg.sender != owner |
| 133 | 2026-04-28 | JUDAO | $ 228,000 | Smart Contract Vulnerability | **KEEP** | BSC: JUDAO sell hook drains JUDAO from its own Pancake pair via sync/isBurnPair |
| 134 | 2026-04-27 | ZetaChain GatewayEVM | $ 334,000 | Smart Contract Vulnerability | **KEEP** | Ethereum(+3): GatewayEVM.execute arbitrary-call sink with missing access control on GatewayZEVM.call |
| 135 | 2026-04-27 | Singularity Finance | $ 413,000 | Oracle Misconfiguration | **KEEP** | Base: oracle registered with a non-existent UniV3 fee tier 42, so getPool() returned address(0) |
| 136 | 2026-04-26 | Scallop | $ 142,000 | Smart Contract Vulnerability | **discard** | Sui Move rewards contract |
| 137 | 2026-04-25 | Purrlend | $ 1,520,000 | Admin Privilege Abuse | **discard** | HyperEVM/MegaETH (not target chains) and a compromised admin multisig |
| 138 | 2026-04-23 | Giddy | $ 1,300,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: EIP-712 signature covers only keccak(SwapInfo.data), not aggregator/fromToken/toToken/amount |
| 139 | 2026-04-22 | Kipseli | $ 72,350 | Smart Contract Vulnerability | **KEEP** | Base: router transfers a USDC-scaled quote as cbBTC units — decimal/asset mismatch |
| 140 | 2026-04-21 | Volo Vaults | $ 3,500,000 | Private Key Leakage | **discard** | Sui vaults |
| 141 | 2026-04-20 | Thetanuts Finance | $ 50,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: first-depositor share-rounding on a freshly deployed vault holding pre-existing WBTC |
| 142 | 2026-04-20 | Juicebox V3 | $ 52,000 | Smart Contract Vulnerability | **KEEP** | Ethereum: REVLoans.borrowFrom registers a caller-supplied loan source, forging accounting context |
| 143 | 2026-04-19 | Vercel | - | Supply Chain Attack | **discard** | Corporate SaaS breach |
| 144 | 2026-04-19 | Custom sAVAX Aave Rebalancer contract | $ 64,000 | Smart Contract Vulnerability | **discard** | Avalanche — not a target chain |
| 145 | 2026-04-18 | Kelp DAO | $ 293,000,000 | Supply Chain Attack | **discard** | LayerZero DVN RPC node infrastructure compromise |
| 146 | 2026-04-18 | DNS registrar for eth.limo | - | Supply Chain Attack | **discard** | DNS registrar compromise |
| 147 | 2026-04-16 | Rhea Finance | $ 18,400,000 | Slippage Protection Logic Flaw | **discard** | NEAR — not a target chain |
| 148 | 2026-04-16 | Grinex | $ 15,000,000 | Hot Wallet Infrastructure Breach | **discard** | Exchange hot-wallet breach |
| 149 | 2026-04-15 | LootBot AI | $ 9,600 | Smart Contract Vulnerability | **KEEP** | Ethereum: redeem() accepts duplicate NFT IDs and only advances nextRedeem after payout |
| 150 | 2026-04-14 | CowSwap | $ 1,200,000 | Supply-chain attack | **discard** | Frontend/domain compromise |
| 151 | 2026-04-13 | Hyperbridge | $ 2,500,000 | Smart Contract Vulnerability | **KEEP** | Ethereum(+Base/BSC/Arb): MMR VerifyProof() does not enforce leaf_index < leafCount |
| 152 | 2026-04-13 | Dango | $ 1,900,000 | Insurance Fund Logic Vulnerability | **discard** | Dango app-chain insurance-fund logic |
| 153 | 2026-04-13 | MONA | $ 60,950 | Reserve Manipulation Attack | **KEEP (borderline)** | BSC: LisaVault referral tiers self-dealt via proxy contracts, but stage 1 was the deployer redeeming their own LP |
| 154 | 2026-04-12 | SubQuery Network | $ 134,000 | Smart Contract Vulnerability | **KEEP** | Base: Settings.setContractAddress()/setBatchAddress() missing onlyOwner after a refactor |
| 155 | 2026-04-11 | Zerion | $ 100,000 | AI-enabled Social Engineering Attack | **discard** | AI-assisted social engineering of an employee device |
| 156 | 2026-04-09 | Aethir | $ 90,000 | Smart Contract Vulnerability | **KEEP** | BSC: AethirOFTAdapter ownership transfer reachable due to missing/bypassed onlyOwner |
| 157 | 2026-04-07 | Squid Multicall | $ 517,000 | Approval Exploit | **KEEP (borderline)** | BSC(+multi): SquidMulticall.run() is permissionless by design; victim had approved it — design flaw, not a code bug |
| 158 | 2026-04-07 | TGAI | $ 11,940 | Reserve Manipulation Attack | **KEEP** | BSC: TGAI reserve manipulation via sync() on the Pancake V2 pair |
| 159 | 2026-04-05 | Denaria | $ 165,000 | Smart Contract Vulnerability | **discard** | Linea — not a target chain |
| 160 | 2026-04-04 | BSC TMM/USDT | $ 1,665,000 | Reserve Manipulation Attack | **KEEP** | BSC: TMM burned to dead address to collapse the pair reserve to 1 TMM, then swapped out |
