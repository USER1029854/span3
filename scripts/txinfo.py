import sys, json, chainlib as cl
def info(chain, tx):
    t=cl.rpc(chain,'eth_getTransactionByHash',[tx]).get('result')
    r=cl.rpc(chain,'eth_getTransactionReceipt',[tx]).get('result')
    if not r: return {'error':'no receipt'}
    blk=int(r['blockNumber'],16); ts=cl.ts(chain,blk)
    addrs={}
    for l in r.get('logs',[]):
        a=l['address'].lower(); addrs[a]=addrs.get(a,0)+1
    return {'block':blk,'time':cl.fmt(ts),'from':t.get('from'),'to':t.get('to'),
            'created':r.get('contractAddress'),'log_addrs':sorted(addrs.items(),key=lambda x:-x[1])}
if __name__=='__main__':
    d=info(sys.argv[1],sys.argv[2]); print(json.dumps(d,indent=1))
