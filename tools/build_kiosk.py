import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
import os,re
src=open(ROOT+'index.html').read()
i=src.rindex('<script>\nconst APPV=');j=src.index('</script>',i)+9
base=src[:i]+src[j:]
for k,title in (('tv','Moorddossier TV'),('join','Doe mee · Moorddossier TV')):
    s=base.replace('<title>Moorddossier</title>',f'<title>{title}</title>').replace('href="manifest.webmanifest"','href="../manifest.webmanifest"').replace('href="icon-192.png"','href="../icon-192.png"')
    s=s.replace('<body>\n',f'<body>\n<script>window.MDKIOSK="{k}"</script>\n',1)
    if k=='tv':s=s.replace('<meta name="theme-color" content="#C2321F">','<meta name="theme-color" content="#151716">')
    else:s=s.replace('<meta name="theme-color" content="#C2321F">','<meta name="theme-color" content="#151716">')
    os.makedirs(ROOT+k,exist_ok=True);open(ROOT+f'{k}/index.html','w').write(s)
print('kiosk ok')
