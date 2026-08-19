# explicit discard grouping (81 ids)
DROPGRP={
 'non-target chain':[1,6,7,28,31,32,33,35,36,44,46,54,57,60,61,68,69,72,75,83,109,111,115,119,120,121,127,130,131,136,137,140,144,147,152,159],
 'key / signer / multisig / hot-wallet compromise':[20,22,26,29,37,70,85,87,89,97,98,102,104,110000,114,128,129,148,26000],
 'off-chain infrastructure (relayer, backend, solver DB, RPC, bot)':[21,58,88,90,107,145],
 'frontend / DNS / supply-chain / dependency / firmware':[9,15,50,52,55,78,143,146,150],
 'social engineering / account takeover / phishing':[23,84,108,122,155],
 'consensus / node / TSS / proof-system':[3,56,113],
 'cause undisclosed, no contract vulnerability identified':[5,38],
}
# fix the placeholders
DROPGRP['key / signer / multisig / hot-wallet compromise']=[20,22,26,29,37,70,85,87,89,97,98,102,104,114,128,129,148]
DROPGRP['off-chain infrastructure (relayer, backend, solver DB, RPC, bot)']=[21,34,53,58,88,90,107,145]
DROPGRP['non-target chain']=[1,6,7,28,31,32,33,35,36,44,46,54,57,60,61,68,69,72,75,83,109,111,115,119,120,121,127,130,131,136,137,140,144,147,152,159]
DROPGRP['frontend / DNS / supply-chain / dependency / firmware']=[9,15,50,52,55,78,143,146,150]
DROPGRP['exchange / payment-processor / infra breach, cause undisclosed']=[5,11,38,148]
DROPGRP['key / signer / multisig / hot-wallet compromise']=[20,22,26,29,37,70,85,87,89,97,98,102,104,114,128,129]
del DROPGRP['cause undisclosed, no contract vulnerability identified']

# explicit category per in-scope id

CAT={
 'custom token with a fund-moving transfer/reward hook':[18,19,49,59,62,65,79,80,81,91,92,93,94,96,99,133,153,158,160],
 'vault (ERC-4626 / yield / options)':[8,12,45,51,66,105,126,132,135,138,141],
 'bridge / router / cross-chain executor':[27,63,67,101,106,110,134,139,151,156,157],
 'staking / reward / bond / distribution pool':[2,13,14,17,24,64,73,82,86,103,118,149,154],
 'stablecoin / CDP':[4,30,43,100],
 'lending / borrowing market':[39,40,48,123,142],
 'DEX / AMM / hook / extension':[77,112,125],
 'index / structured product':[16,25],
 'governance / DAO treasury':[74,116],
 'launchpad / LP locker':[10,95],
 'privacy pool / dark pool':[47],
 'NFT liquidity (DN404/BT404)':[71,76],
 'smart account (ERC-4337)':[42],
 'streaming payments':[41],
 'market-maker RFQ settlement proxy':[124],
 'bespoke protocol diamond (EIP-2535)':[117],
}

# explicit mechanism bucket per in-scope id
MECH={
 'price / valuation manipulation (spot-read-then-act, live NAV, ERC-4626 donation, reserve manipulation)':
   [2,8,13,30,40,43,45,48,49,59,62,64,79,80,81,91,93,99,112,133,153,158,160,135],
 'missing or broken access control':[14,93000,24,92000,96,116,132,154,156,93001,44444],
 'uncapped subsidy / reward accounting (Sybil-farmable, duplicate IDs, uninitialised checkpoints)':
   [18,19,73,82,100,149,153000,86],
 'proof / message-verification / hash-collision flaw':[27,63,67,106,110,151,47],
 'arithmetic — rounding, unsafe cast, decimals, share math':[4,41,66,76,105,139,141],
 'signature-validation bypass':[17,51,92,103,124,138],
 'trusts caller-supplied accounting / routing context':[101,134,142,157],
 'reentrancy / CEI violation':[94],
 'hardcoded backdoor / privileged escape hatch':[95,118],
 'arbitrary call / calldata forwarding':[10],
 'governance capture (no timelock / abandoned DAO)':[39,74],
 're-initializable proxy / uninitialised facet':[117,123],
 'ERC-4337 validation-phase side effect':[42],
 'TOCTOU / missing state lock':[16],
 'permissionless registration + crafted parameters':[25],
 'mechanism not publicly detailed':[12,126,71,25000],
}
MECH['missing or broken access control']=[14,24,93,96,116,132,154,156,25]
MECH['uncapped subsidy / reward accounting (Sybil-farmable, duplicate IDs, uninitialised checkpoints)']=[18,19,73,82,86,100,149]
MECH['mechanism not publicly detailed']=[12,126]
MECH['NFT/token standard state-desync (DN404/BT404 packed ownership)']=[71,76]
MECH['arithmetic — rounding, unsafe cast, decimals, share math']=[4,41,66,105,139,141]
MECH['permissionless registration + crafted parameters']=[125]
MECH['price / valuation manipulation (spot-read-then-act, live NAV, ERC-4626 donation, reserve manipulation)']=[2,8,13,30,40,43,45,48,49,59,62,64,79,80,81,91,99,112,133,135,153,158,160]
MECH['arithmetic — rounding, unsafe cast, decimals, share math']=[4,41,65,66,105,139,141]
MECH['accounting flaw across internal call paths / sidecars']=[77]
MECH['uncapped subsidy / reward accounting (Sybil-farmable, duplicate IDs, uninitialised checkpoints)']=[18,19,73,82,100,149]
MECH['storage-slot collision with a library fixed slot']=[86]
