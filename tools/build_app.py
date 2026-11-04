import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
import base64,sys
src=open(ROOT+'src/moorddossier.html').read()
body=src[src.index('</title>')+8:].replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
i=body.index('<div class="wrap">')
b64=base64.b64encode(open(ROOT+'apple-touch-icon.png','rb').read()).decode()
head=f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Moorddossier</title>
<meta name="description" content="Logische moordpuzzels: lees de aanwijzingen, vul het rooster in en ontmasker de dader.">
<meta name="theme-color" content="#C2321F">
<meta name="color-scheme" content="light dark">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Moorddossier">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="data:image/png;base64,{b64}">
<style>html{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;-webkit-text-size-adjust:100%}}[hidden]{{display:none!important}}</style>
'''
out=head+body[:i].strip()+'\n</head>\n<body>\n'+body[i:].rstrip()+'''
<script>
const APPV='__APPV__';
if('serviceWorker' in navigator){addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}))}
// Nieuwe versie online? Dan herladen zodra de app weer in beeld komt. Voortgang staat in localStorage en blijft bewaard.
function checkNew(){fetch('version.json?t='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():null).then(j=>{if(j&&j.v&&j.v!==APPV){if(navigator.serviceWorker&&navigator.serviceWorker.getRegistration)navigator.serviceWorker.getRegistration().then(r=>r&&r.update()).catch(()=>{});let done='';try{done=sessionStorage.getItem('md-reload')||''}catch(e){}if(done===j.v)return;try{sessionStorage.setItem('md-reload',j.v)}catch(e){}setTimeout(()=>location.reload(),400)}}).catch(()=>{})}
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')checkNew()});addEventListener('load',()=>setTimeout(checkNew,1500));
</script>
</body>
</html>
'''
import time,json
v=time.strftime('%Y%m%d%H%M%S')
out=out.replace('__APPV__',v)
open(ROOT+'index.html','w').write(out)
json.dump({'v':v},open(ROOT+'version.json','w'))
