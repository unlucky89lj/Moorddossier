import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
# Maakt pwa/index.html geschikt voor oudere browsers (smart-tv's): JS naar chrome56 via esbuild, CSS-terugvallers.
import re,subprocess,os,tempfile
S=ROOT
import shutil,glob
E=next((p for p in ['/opt/npm-tools/node_modules/esbuild/bin/esbuild',shutil.which('esbuild') or '']+glob.glob('/opt/**/esbuild/bin/esbuild',recursive=True) if p and os.path.exists(p)),None)
if not E:raise SystemExit('esbuild niet gevonden: installeer met  npm i -g esbuild')
POLY=("(function(){if(!Object.fromEntries)Object.fromEntries=function(it){var o={};Array.from(it).forEach(function(kv){o[kv[0]]=kv[1]});return o};"
 "if(!String.prototype.padStart)String.prototype.padStart=function(n,c){var s=String(this);c=c===undefined?' ':String(c);while(s.length<n)s=c+s;return s.length>n&&c.length>1?s.slice(s.length-n):s};"
 "if(!String.prototype.padEnd)String.prototype.padEnd=function(n,c){var s=String(this);c=c===undefined?' ':String(c);while(s.length<n)s=s+c;return s.slice(0,Math.max(n,String(this).length))};})();\n")
def tr(js):
    with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False) as f:f.write(js);src=f.name
    out=src+'.out.js'
    r=subprocess.run([E,src,'--target=chrome56','--outfile='+out,'--log-level=error','--charset=utf8'],capture_output=True,text=True)
    if r.returncode:raise SystemExit(r.stderr)
    t=open(out).read();os.remove(src);os.remove(out);return t
def rep(m):
    js=m.group(1)
    if len(js)<200 and 'MDKIOSK' in js:return m.group(0)
    return '<script>'+(POLY if len(js)>100000 else '')+tr(js)+'</script>'
import sys
for p in [S+x for x in ['index.html','tv/index.html','join/index.html']]:
 s=open(p).read()
 s=re.sub(r'<script>(.*?)</script>',rep,s,flags=re.S)
 ERRBAR='<script>window.onerror=function(m,u,l){try{if(document.getElementById("mdErr"))return;var d=document.createElement("div");d.id="mdErr";d.style.cssText="position:fixed;left:0;right:0;bottom:0;background:#c2321f;color:#fff;padding:12px 16px;font:16px/1.4 sans-serif;z-index:9999";d.textContent="Deze browser kan Moorddossier niet goed laden ("+m+", regel "+l+"). Gebruik een laptop, tablet of telefoon en cast naar de tv.";(document.body||document.documentElement).appendChild(d)}catch(e){}};</script>'
 if 'id="mdErr"' not in s:s=s.replace('</title>','</title>\n'+ERRBAR,1)
 # CSS: inset uitschrijven
 def ins(m):
     v=m.group(1).split();v=(v*4)[:4] if len(v)==1 else v if len(v)==4 else (v+v)[:4] if len(v)==2 else [v[0],v[1],v[2],v[1]]
     return f'top:{v[0]};right:{v[1]};bottom:{v[2]};left:{v[3]}'
 s=re.sub(r'(?<![\w-])inset:([^;}"]+)',ins,s)
 s=re.sub(r'font-size:clamp\(([^,]+),([^,]+),([^)]+)\)',lambda m:f'font-size:{m.group(3)};font-size:clamp({m.group(1)},{m.group(2)},{m.group(3)})',s)
 s=re.sub(r'(?<![\w-])gap:([^;}"]+)',lambda m:f'grid-gap:{m.group(1)};gap:{m.group(1)}',s)
 open(p,'w').write(s);print('legacy ok',len(s))
