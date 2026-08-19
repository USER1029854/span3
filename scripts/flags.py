import json, chainlib as cl
IMPL_SLOT='0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc'  # EIP-1967 impl
ADMIN_SLOT='0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103' # EIP-1967 admin
BEACON_SLOT='0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50'
def sel(sig):
    import hashlib
    # keccak256 via pysha3 not available; use precomputed selectors
    return None
SELECTORS={'owner()':'0x8da5cb5b','getOwner()':'0x893d20e8','admin()':'0xf851a440',
           'paused()':'0x5c975abb','totalSupply()':'0x18160ddd','decimals()':'0x313ce567',
           'implementation()':'0x5c60da1b'}
def call(chain,to,data):
    r=cl.rpc(chain,'eth_call',[{'to':to,'data':data},'latest'])
    return r.get('result')
def slot(chain,addr,s):
    r=cl.rpc(chain,'eth_getStorageAt',[addr,s,'latest'])
    v=r.get('result')
    if not v or int(v,16)==0: return None
    return '0x'+v[-40:]
def codesize(chain,addr):
    c=cl.rpc(chain,'eth_getCode',[addr,'latest']).get('result','0x')
    return (len(c)-2)//2
def verified(chain,addr):
    if chain in ('mainnet','arbitrum'):
        r=cl.etherscan(chain,module='contract',action='getsourcecode',address=addr)
        if r.get('status')=='1' and r.get('result'):
            x=r['result'][0]
            return {'verified':bool(x.get('SourceCode')),'name':x.get('ContractName'),
                    'proxy':x.get('Proxy'),'impl':x.get('Implementation') or None,
                    'compiler':x.get('CompilerVersion'),'license':x.get('LicenseType'),
                    'src':'Etherscan V2 getsourcecode'}
        return {'verified':None,'src':'etherscan error: '+str(r)[:90]}
    if chain=='base':
        d=cl.get('https://base.blockscout.com/api/v2/addresses/'+addr)
        if 'is_verified' in d:
            return {'verified':d.get('is_verified'),'name':d.get('name'),
                    'impl':[i.get('address_hash') for i in (d.get('implementations') or [])] or None,
                    'src':'Blockscout base /api/v2/addresses'}
        return {'verified':None,'src':'blockscout error'}
    if chain=='bsc':
        d=cl.get('https://sourcify.dev/server/v2/contract/56/'+addr)
        if isinstance(d,dict) and d.get('match'):
            return {'verified':True,'match':d.get('match'),'verifiedAt':d.get('verifiedAt'),
                    'src':'Sourcify v2 (BscScan API is paywalled on this key)'}
        return {'verified':'unknown-sourcify-miss','src':'Sourcify v2 no match (NOT proof of unverified on BscScan)'}
    return {'verified':None}
def scan(chain,addr):
    o={'chain':chain,'address':addr}
    o['codesize']=codesize(chain,addr)
    o['eip1967_impl']=slot(chain,addr,IMPL_SLOT)
    o['eip1967_admin']=slot(chain,addr,ADMIN_SLOT)
    o['eip1967_beacon']=slot(chain,addr,BEACON_SLOT)
    for name,s in [('owner','0x8da5cb5b'),('getOwner','0x893d20e8'),('admin_fn','0xf851a440')]:
        v=call(chain,addr,s)
        if v and len(v)>=66 and int(v,16)!=0: o[name]='0x'+v[-40:]
    o.update(verified(chain,addr))
    return o
