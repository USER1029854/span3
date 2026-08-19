import re, json, html, glob

entries=[]
for p in range(1,9):
    src=open(f'p{p}.html',encoding='utf-8').read()
    # isolate case-content
    m=re.search(r'<div class="case-content">(.*?)<div class="page', src, re.S)
    body=m.group(1) if m else src
    lis=re.findall(r'<li>(.*?)</li>', body, re.S)
    for li in lis:
        def g(pat, default=''):
            mm=re.search(pat, li, re.S)
            return html.unescape(re.sub(r'<[^>]+>','',mm.group(1))).strip() if mm else default
        date=g(r'<span class="time">(.*?)</span>')
        target=g(r'<h3><em>Hacked target: </em>(.*?)</h3>')
        desc=g(r'<p><em>Description of the event: </em>(.*?)</p>')
        loss=g(r'<em>Amount of loss: </em>(.*?)</span>')
        method=g(r'<em>Attack method: </em>(.*?)</span>')
        ref=re.findall(r'class="link-reference"><a href="(.*?)"', li)
        loss=re.sub(r'\s+',' ',loss).strip()
        if not target: continue
        entries.append(dict(page=p,date=date,target=target,loss=loss,method=method,
                            refs=ref,desc=re.sub(r'\s+',' ',desc)))
json.dump(entries, open('slowmist.json','w'), indent=1)
print("total entries:", len(entries))
from collections import Counter
print("per page:", Counter(e['page'] for e in entries))
print("date range:", min(e['date'] for e in entries), "->", max(e['date'] for e in entries))
for e in entries:
    print(f"{e['page']}|{e['date']}|{e['target'][:38]:38}|{e['loss'][:14]:14}|{e['method']}")
