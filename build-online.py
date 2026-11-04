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
# (the user) each language has its own page, because whoever shares a link only reads the HTML: its address, texts and image
SITE = 'https://sampler.half.social/'
LANG_META = {
    'pt': dict(html='pt-BR', locale='pt_BR', img='og.png', title='FM-½ Sampler · faça música no navegador',
               desc='Um sampler grátis no navegador: toque com o teclado, o celular ou um teclado MIDI, grave sua voz, corte em fatias, ponha efeitos e grave a música em faixas. Funciona com o FM-1, sem instalar nada.',
               ogt='Toque. Grave. Faça música. · FM-½ Sampler', ogd='Um sampler grátis no navegador. Toque com o teclado, o celular ou um teclado MIDI: abra e toque, sem instalar.',
               twd='Um sampler grátis no navegador: abra e toque, sem instalar.', alt='O FM-½ Sampler: toque, grave, faça música'),
    'en': dict(html='en', locale='en_US', img='og-en.png', title='FM-½ Sampler · make music in your browser',
               desc='A free sampler in your browser: play with your keyboard, your phone or a MIDI keyboard, record your voice, slice it, add effects and record the music on tracks. Works with the FM-1, nothing to install.',
               ogt='Tap. Record. Make music. · FM-½ Sampler', ogd='A free sampler in your browser. Play with your keyboard, your phone or a MIDI keyboard: open and play, nothing to install.',
               twd='A free sampler in your browser: open and play, nothing to install.', alt='The FM-½ Sampler: tap, record, make music'),
    'es': dict(html='es', locale='es_LA', img='og-es.png', title='FM-½ Sampler · haz música en el navegador',
               desc='Un sampler gratis en el navegador: toca con el teclado, el celular o un teclado MIDI, graba tu voz, córtala en fragmentos, ponle efectos y graba la música en pistas. Funciona con el FM-1, sin instalar nada.',
               ogt='Toca. Graba. Haz música. · FM-½ Sampler', ogd='Un sampler gratis en el navegador. Toca con el teclado, el celular o un teclado MIDI: ábrelo y toca, sin instalar.',
               twd='Un sampler gratis en el navegador: ábrelo y toca, sin instalar.', alt='El FM-½ Sampler: toca, graba, haz música'),
    'fr': dict(html='fr', locale='fr_FR', img='og-fr.png', title='FM-½ Sampler · fais ta musique dans le navigateur',
               desc='Un sampler gratuit dans le navigateur : joue au clavier, sur ton téléphone ou avec un clavier MIDI, enregistre ta voix, découpe-la, ajoute des effets et enregistre ta musique sur des pistes. Compatible FM-1, sans rien installer.',
               ogt='Joue. Enregistre. Fais ta musique. · FM-½ Sampler', ogd='Un sampler gratuit dans le navigateur. Joue au clavier, sur ton téléphone ou avec un clavier MIDI : ouvre et joue, sans installer.',
               twd='Un sampler gratuit dans le navigateur : ouvre et joue, sans installer.', alt='Le FM-½ Sampler : joue, enregistre, fais ta musique'),
    'ja': dict(html='ja', locale='ja_JP', img='og-ja.png', title='FM-½ Sampler · ブラウザで音楽をつくろう',
               desc='ブラウザで使える無料サンプラー。キーボード、スマホ、MIDIキーボードで演奏し、声を録音して切り分け、エフェクトをかけ、トラックに音楽を録音できます。FM-1対応、インストール不要。',
               ogt='タップ。録音。音楽をつくろう。 · FM-½ Sampler', ogd='ブラウザで使える無料サンプラー。キーボード、スマホ、MIDIキーボードで演奏。開いてすぐ、インストール不要。',
               twd='ブラウザで使える無料サンプラー。開いてすぐ演奏、インストール不要。', alt='FM-½ Sampler：タップ、録音、音楽をつくろう'),
    'ko': dict(html='ko', locale='ko_KR', img='og-ko.png', title='FM-½ Sampler · 브라우저에서 음악 만들기',
               desc='브라우저에서 쓰는 무료 샘플러. 키보드, 휴대폰, MIDI 키보드로 연주하고, 목소리를 녹음해 자르고, 효과를 넣고, 트랙에 음악을 녹음하세요. FM-1과 함께 쓸 수 있고 설치가 필요 없어요.',
               ogt='누르고. 녹음하고. 음악을 만드세요. · FM-½ Sampler', ogd='브라우저에서 쓰는 무료 샘플러. 키보드, 휴대폰, MIDI 키보드로 연주하세요. 열고 바로, 설치 없이.',
               twd='브라우저에서 쓰는 무료 샘플러. 열고 바로 연주, 설치 없이.', alt='FM-½ Sampler: 누르고, 녹음하고, 음악을 만드세요'),
}
# (the user) half.social in its 3 languages (it shares the sampler's card)
SOCIAL = 'https://half.social/'
SOCIAL_META = {
    'pt': dict(html='pt-BR', locale='pt_BR', img='og.png', desc='A rede social de quem faz música com sintetizador. Músicas, vídeos e só a galera do synth.', ogd='A rede social de quem faz música com sintetizador.'),
    'en': dict(html='en', locale='en_US', img='og-en.png', desc='The social network for people who make music with synthesizers. Tracks, videos and only synth people.', ogd='The social network for people who make music with synthesizers.'),
    'es': dict(html='es', locale='es_LA', img='og-es.png', desc='La red social de quien crea música con sintetizador. Temas, videos y solo gente del synth.', ogd='La red social de quien crea música con sintetizador.'),
}

def page_url(site, code):
    return site if code == 'pt' else site + code + '/'

def alternates(site, codes):
    return ''.join(f'<link rel="alternate" hreflang="{c}" href="{page_url(site, c)}">\n' for c in codes) + f'<link rel="alternate" hreflang="x-default" href="{site}">\n'

def sub1(s, pat, val):   # one tag's value; a tag that isn't there is a mistake, not a silence
    s, n = re.subn(pat, lambda m: m.group(1) + val + m.group(2), s, count=1)
    if not n:
        raise SystemExit('não achei no head: ' + pat)
    return s

def esc(v):
    return v.replace('&', '&amp;').replace('"', '&quot;')

def sampler_page(s, code):
    M, url = LANG_META[code], page_url(SITE, code)
    s = sub1(s, r'(<html lang=")[^"]*(")', M['html'])
    s = sub1(s, r'(<title>)[^<]*(</title>)', M['title'])
    s = sub1(s, r'(<meta name="description" content=")[^"]*(")', esc(M['desc']))
    s = sub1(s, r'(<link rel="canonical" href=")[^"]*(")', url)
    for pat, v in ((r'(<meta property="og:locale" content=")[^"]*(")', M['locale']), (r'(<meta property="og:title" content=")[^"]*(")', esc(M['ogt'])), (r'(<meta property="og:description" content=")[^"]*(")', esc(M['ogd'])),
                   (r'(<meta property="og:url" content=")[^"]*(")', url), (r'(<meta property="og:image" content=")[^"]*(")', SITE + M['img']), (r'(<meta property="og:image:alt" content=")[^"]*(")', esc(M['alt'])),
                   (r'(<meta name="twitter:title" content=")[^"]*(")', esc(M['ogt'])), (r'(<meta name="twitter:description" content=")[^"]*(")', esc(M['twd'])), (r'(<meta name="twitter:image" content=")[^"]*(")', SITE + M['img'])):
        s = sub1(s, pat, v)
    def ld(m):
        d = json.loads(m.group(2)); d.update(url=url, image=SITE + M['img'], description=M['desc'], inLanguage=M['html'])
        return m.group(1) + json.dumps(d, ensure_ascii=False) + m.group(3)
    s, n = re.subn(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, s, count=1, flags=re.S)
    if not n:
        raise SystemExit('não achei o ld+json')
    return s.replace('<link rel="canonical"', alternates(SITE, LANG_META) + '<link rel="canonical"', 1)

def social_pages():   # social/en/, social/es/ and the images, from social/index.html (which stays the source)
    src = ROOT / 'social'; s = (src / 'index.html').read_text()
    for code, M in SOCIAL_META.items():
        url, img = page_url(SOCIAL, code), SOCIAL + M['img']; h = s
        h = sub1(h, r'(<html lang=")[^"]*(")', M['html'])
        h = sub1(h, r'(<meta name="description" content=")[^"]*(")', esc(M['desc']))
        h = sub1(h, r'(<meta property="og:description" content=")[^"]*(")', esc(M['ogd']))
        h = sub1(h, r'(<meta property="og:url" content=")[^"]*(")', url)
        h = sub1(h, r'(<meta property="og:locale" content=")[^"]*(")', M['locale'])
        h = sub1(h, r'(<meta property="og:image" content=")[^"]*(")', img)
        h = sub1(h, r'(<meta name="twitter:image" content=")[^"]*(")', img)
        h = sub1(h, r'(<link rel="canonical" href=")[^"]*(")', url)
        h = re.sub(r'<link rel="alternate" hreflang[^>]*>\n', '', h)
        h = h.replace('<link rel="canonical"', alternates(SOCIAL, SOCIAL_META) + '<link rel="canonical"', 1)
        dest = src if code == 'pt' else src / code
        dest.mkdir(exist_ok=True); (dest / 'index.html').write_text(h); shutil.copy(HUB / 'seo' / M['img'], src / M['img'])
    (src / 'sitemap.xml').write_text(sitemap(SOCIAL, SOCIAL_META))

def sitemap(site, codes):
    links = ''.join(f'<xhtml:link rel="alternate" hreflang="{c}" href="{page_url(site, c)}"/>' for c in codes)
    urls = ''.join(f'  <url><loc>{page_url(site, c)}</loc>{links}<changefreq>weekly</changefreq><priority>{"1.0" if c == "pt" else "0.8"}</priority></url>\n' for c in codes)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n'

AUDIO = {'.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac', '.aif', '.aiff', '.opus', '.webm'}

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'sons').mkdir(parents=True)
    s = (HUB / 'index.html').read_text()
    s = s.replace('<script src="sampler-i18n.js"></script>', '<script>window.SAMPLER_ONLINE = true;</script>\n<script src="sampler-i18n.js"></script>', 1)
    s = s.replace('</style>', 'body:not(.local-ok) [data-srv] { display: none !important; }   /* (shown when serve.py runs on the Mac) */\n</style>', 1)
    s = s.replace('<head>', '<head>\n' + GA, 1)   # (the user) Google Analytics, on the published copy only
    urlm = {c: {k: M[k] for k in ('title', 'desc', 'locale', 'ogt', 'ogd', 'twd', 'alt', 'img')} for c, M in LANG_META.items()}
    s = s.replace('<script>window.SAMPLER_ONLINE = true;</script>', '<script>window.SAMPLER_ONLINE = true; window.SAMPLER_URL_LANG = ' + json.dumps(urlm, ensure_ascii=False) + ';</script>', 1)
    for a, b in (('src="vis/', 'src="/vis/'), ('src="sampler-i18n.js"', 'src="/sampler-i18n.js"'), ("'sons/sons.json'", "'/sons/sons.json'"), ("ONLINE && !API ? 'sons/'", "ONLINE && !API ? '/sons/'")):   # (the same files from any language's address)
        if a not in s:
            raise SystemExit('não achei: ' + a)
        s = s.replace(a, b)
    for code in LANG_META:
        d = OUT if code == 'pt' else OUT / code
        d.mkdir(exist_ok=True); (d / 'index.html').write_text(sampler_page(s, code))
    shutil.copy(HUB / 'sampler-i18n.js', OUT / 'sampler-i18n.js')
    for f in ('robots.txt',):   # (the user) the share images and what Google reads
        shutil.copy(HUB / 'seo' / f, OUT / f)
    for M in LANG_META.values():
        shutil.copy(HUB / 'seo' / M['img'], OUT / M['img'])
    (OUT / 'sitemap.xml').write_text(sitemap(SITE, LANG_META))
    social_pages()
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
