const CACHE='moorddossier-v39';
const CORE=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  if(e.request.url.includes('version.json'))return;
  const isPage=e.request.mode==='navigate';
  const net=()=>fetch(isPage?new Request(e.request.url,{cache:'no-store',credentials:'same-origin'}):e.request).then(res=>{if(res&&(res.ok||res.type==='opaque')){const cp=res.clone();caches.open(CACHE).then(c=>c.put(e.request,cp))}return res});
  if(isPage){e.respondWith(net().catch(()=>caches.match(e.request).then(h=>h||caches.match('index.html'))));return}
  e.respondWith(caches.match(e.request).then(hit=>hit||net()));
});
