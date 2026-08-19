import json,os,sys,time,subprocess,urllib.parse,datetime

RPC={'mainnet':'https://eth-mainnet.public.blastapi.io',
     'bsc':'https://bsc-mainnet.public.blastapi.io',
     'arbitrum':'https://arbitrum-one.public.blastapi.io',
     'base':'https://base-mainnet.public.blastapi.io'}
CHAINID={'mainnet':1,'bsc':56,'arbitrum':42161,'base':8453}
EK=os.environ.get('ETHERSCAN_API_KEY','')
CACHE='cache.json'
try: C=json.load(open(CACHE))
except Exception: C={}
def save(): json.dump(C,open(CACHE,'w'))

UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36'
def curl(args,tries=4):
    for i in range(tries):
        p=subprocess.run(['curl','-sS','-m','60','-A',UA]+args,capture_output=True,text=True)
        if p.returncode==0 and p.stdout.strip(): return p.stdout
        time.sleep(1.2*(i+1))
    return ''

def post(url,payload,tries=4):
    key='POST '+url+json.dumps(payload,sort_keys=True)
    if key in C: return C[key]
    for i in range(tries):
        body=curl(['-X','POST',url,'-H','content-type: application/json','--data',json.dumps(payload)],tries=2)
        try: r=json.loads(body)
        except Exception: r={'error':'unparseable: '+body[:200]}
        if 'error' in r and any(w in str(r['error']).lower() for w in ('limit','busy','timeout','unparseable')):
            time.sleep(2*(i+1)); continue
        C[key]=r; save(); return r
    return {'error':'fail after retries'}

def get(url,tries=4):
    if url in C: return C[url]
    for i in range(tries):
        body=curl([url],tries=2)
        if not body: time.sleep(1.5*(i+1)); continue
        try: r=json.loads(body)
        except Exception: r={'_raw':body[:400000]}
        if isinstance(r,dict) and 'Max calls per sec' in str(r.get('result','')): time.sleep(1.2); continue
        C[url]=r; save(); return r
    return {'error':'fail'}

def rpc(chain,method,params): return post(RPC[chain],{'jsonrpc':'2.0','id':1,'method':method,'params':params})
def code_at(chain,addr,blk):
    r=rpc(chain,'eth_getCode',[addr,hex(blk)])
    return r.get('result','0x')
def latest(chain): return int(rpc(chain,'eth_blockNumber',[])['result'],16)
def block(chain,n,full=False):
    return rpc(chain,'eth_getBlockByNumber',[hex(n),full]).get('result')
def ts(chain,n):
    b=block(chain,n)
    return int(b['timestamp'],16) if b else None
def fmt(t): return datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S UTC')

def creation_block(chain,addr,hi=None):
    """binary search first block where code exists"""
    if hi is None: hi=latest(chain)
    lo=0
    if code_at(chain,addr,hi)=='0x': return None   # selfdestructed or never
    if code_at(chain,addr,0)!='0x': return 0
    while lo+1<hi:
        mid=(lo+hi)//2
        if code_at(chain,addr,mid)=='0x': lo=mid
        else: hi=mid
    return hi

def creation_tx(chain,addr,blk):
    """find creating tx in block: direct create (receipt.contractAddress) or constructor logs"""
    b=block(chain,blk,True)
    if not b: return None,None
    a=addr.lower()
    for t in b['transactions']:
        if t.get('to') is None:
            r=rpc(chain,'eth_getTransactionReceipt',[t['hash']]).get('result')
            if r and (r.get('contractAddress') or '').lower()==a:
                return t['hash'],'direct-create'
    for t in b['transactions']:
        r=rpc(chain,'eth_getTransactionReceipt',[t['hash']]).get('result')
        if r and any((l.get('address') or '').lower()==a for l in r.get('logs',[])):
            return t['hash'],'factory-create (identified via constructor logs)'
    return None,'not resolvable from block scan (factory CREATE with no constructor logs)'

def etherscan(chain,**kw):
    kw['chainid']=CHAINID[chain]; kw['apikey']=EK
    return get('https://api.etherscan.io/v2/api?'+urllib.parse.urlencode(kw))

def profile(chain,addr,label=''):
    out={'chain':chain,'address':addr,'label':label}
    # try etherscan first (mainnet/arbitrum free tier)
    es=etherscan(chain,module='contract',action='getcontractcreation',contractaddresses=addr)
    if es.get('status')=='1' and es.get('result'):
        r=es['result'][0]
        out['creation_tx']=r.get('txHash'); out['creator']=r.get('contractCreator')
        out['creation_block']=int(r['blockNumber']); out['creation_ts']=int(r['timestamp'])
        out['factory']=r.get('contractFactory') or None
        out['creation_src']='Etherscan V2 getcontractcreation'
    else:
        cb=creation_block(chain,addr)
        if cb is None:
            out['creation_src']='NOT FOUND: no code at latest block (self-destructed or EOA)'
            return out
        out['creation_block']=cb; out['creation_ts']=ts(chain,cb)
        tx,how=creation_tx(chain,addr,cb)
        out['creation_tx']=tx; out['creation_tx_method']=how
        out['creation_src']='binary-search eth_getCode on archive RPC (%s) + block timestamp'%RPC[chain]
    if out.get('creation_ts'): out['creation_utc']=fmt(out['creation_ts'])
    return out
