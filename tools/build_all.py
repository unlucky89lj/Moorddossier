# Bouwt de hele site uit src/moorddossier.html (de leesbare bron; bewerk ALLEEN dat bestand):
#   1. index.html + version.json (de app)
#   2. tv/index.html en join/index.html (Moorddossier TV)
#   3. zet de JavaScript om naar een oudere vorm voor smart-tv's (esbuild)
# Gebruik vanuit de hoofdmap van de repo:  python3 tools/build_all.py
import runpy,os
D=os.path.dirname(os.path.abspath(__file__))
for f in ['build_app.py','build_kiosk.py','legacy.py']:runpy.run_path(os.path.join(D,f),run_name='__main__')
print('klaar: index.html, version.json, tv/index.html, join/index.html')
