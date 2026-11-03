#!/usr/bin/env python3
"""(the user) the sampler for an FTP: index.html -> online/index.html (no link to the simulator, nothing that
needs serve.py), with sampler-i18n.js and the sounds of sons/ listed in online/sons/sons.json.
Upload the whole online folder (to sampler.half.social); it needs HTTPS (Web MIDI, the microphone and the screen recording ask for it).
The sounds of sons/ go only with --sons: most packs forbid putting their raw samples on a public site."""
import json, re, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
HUB, OUT = ROOT, ROOT / 'online'
GA = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DP5083TMB1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DP5083TMB1');
</script>
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "z6wsbgtdz2");
</script>
'''
AUDIO = {'.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac', '.aif', '.aiff', '.opus', '.webm'}

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'sons').mkdir(parents=True)
    s = (HUB / 'index.html').read_text()
    s = s.replace('<script src="sampler-i18n.js"></script>', '<script>window.SAMPLER_ONLINE = true;</script>\n<script src="sampler-i18n.js"></script>', 1)
    s = s.replace('</style>', 'body:not(.local-ok) [data-srv] { display: none !important; }   /* (shown when serve.py runs on the Mac) */\n</style>', 1)
    s = s.replace('<head>', '<head>\n' + GA, 1)   # (the user) Google Analytics, on the published copy only
    (OUT / 'index.html').write_text(s)
    shutil.copy(HUB / 'sampler-i18n.js', OUT / 'sampler-i18n.js')
    for f in ('og.png', 'robots.txt', 'sitemap.xml'):   # (the user) the share image and what Google reads
        shutil.copy(HUB / 'seo' / f, OUT / f)
    (OUT / 'vis').mkdir(exist_ok=True)   # (the user) the firmwares' visualizers, ported (not the test pages)
    for f in sorted((HUB / 'vis').glob('*.js')):
        shutil.copy(f, OUT / 'vis' / f.name)
    items, src = [], HUB / 'sons'
    for f in ([] if '--sons' not in sys.argv else sorted(src.rglob('*'), key=lambda q: str(q).lower())):
        if not f.is_file() or f.suffix.lower() not in AUDIO or f.name.startswith('.'):
            continue
        rel = f.relative_to(src)
        if f.suffix.lower() in ('.aif', '.aiff'):          # (the browser can't read AIFF: WAV here, once)
            rel = rel.with_suffix('.wav'); (OUT / 'sons' / rel).parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(f), '-c:a', 'pcm_s16le', str(OUT / 'sons' / rel)], check=True)
        else:
            (OUT / 'sons' / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy(f, OUT / 'sons' / rel)
        cat = rel.parent.as_posix() if rel.parent.as_posix() != '.' else 'Geral'
        items.append({'path': rel.as_posix(), 'name': rel.stem, 'cat': cat, 'ext': rel.suffix.lower()[1:]})
    (OUT / 'sons' / 'sons.json').write_text(json.dumps({'items': items}, ensure_ascii=False, indent=1))
    print(f'online: index.html, sampler-i18n.js, {len(items)} sons' + ('' if '--sons' in sys.argv else ' (sem a pasta sons: use --sons para levar)'))

if __name__ == '__main__':
    main()
