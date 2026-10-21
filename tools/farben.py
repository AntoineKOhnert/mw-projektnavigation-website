#!/usr/bin/env python3
"""Kontrastfeste Orange-Töne (WCAG AA) in allen Seiten. Idempotent, läuft nach neue_seite.py.
   Signal-Orange #FC6820 bleibt für Flächen, Icons, Punkte, Rahmen und im dunklen Hero.
   Text in Orange: --orange-text (#B9430B, >= 4.5:1 auf Weiß und Grau). Buttons: --orange-btn = Logo-Orange #FC6820 mit dunkler Schrift (6:1)."""
import glob, os, re
ROOT = os.path.join(os.path.dirname(__file__), '..', 'www')
VARS = ':root{--orange-text:#B9430B;--orange-btn:#FC6820;--orange-btn-hover:#E2541A}\n'
HERO = '\n  .hero .eyebrow,.hero h1 em{color:#FC6820}\n  .burger .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}\n'
for f in glob.glob(os.path.join(ROOT, '*.html')):
    if os.path.basename(f).startswith('google'): continue
    t = open(f, encoding='utf-8').read(); o = t
    kopf, rest = t.split('</head>', 1)
    kopf = re.sub(r'color:var\(--orange(-dark)?\)', 'color:var(--orange-text)', kopf)
    kopf = re.sub(r'(\.btn\{[^}]*?)background:var\(--orange\)', r'\1background:var(--orange-btn)', kopf)
    kopf = kopf.replace('.btn:hover{background:var(--orange-dark)', '.btn:hover{background:var(--orange-btn-hover)')
    kopf = kopf.replace('.fact h3::before{content:"\\2713";width:24px;height:24px;border-radius:50%;background:var(--orange)', '.fact h3::before{content:"\\2713";width:24px;height:24px;border-radius:50%;background:var(--orange-btn)')
    kopf = kopf.replace('.cal-days span.sel{background:var(--orange)', '.cal-days span.sel{background:var(--orange-btn)').replace('.cal-slots .slot.on{background:var(--orange)', '.cal-slots .slot.on{background:var(--orange-btn)')
    kopf = re.sub(r':root\{--orange-text:[^}]*\}\n', VARS, kopf)
    kopf = re.sub(r'(\.btn\{[^}]*?)color:#fff', r'\1color:var(--ink)', kopf)
    kopf = kopf.replace('.about a.btn{color:#fff}', '.about a.btn{color:var(--ink)}')
    for sel in ('.fact h3::before{', '.cal-days span.sel{', '.cal-slots .slot.on{'):
        kopf = re.sub(re.escape(sel) + r'([^}]*?)color:#fff', sel + r'\1color:var(--ink)', kopf)
    if '--orange-text:#' not in kopf:
        i = kopf.rfind('<style>') + len('<style>')
        kopf = kopf[:i] + '\n' + VARS + kopf[i:]
    if '.hero .eyebrow,.hero h1 em{color:#FC6820}' not in kopf:
        j = kopf.rfind('</style>'); kopf = kopf[:j] + HERO + kopf[j:]
    rest = rest.replace('style="color:var(--orange-dark);', 'style="color:var(--orange-text);')
    # Menü-Button: aria-label ist auf <label> nicht erlaubt -> unsichtbarer Text
    rest = rest.replace('<label for="menu-toggle" class="burger" aria-label="Menü"><span></span><span></span><span></span></label>',
                        '<label for="menu-toggle" class="burger"><span></span><span></span><span></span><b class="sr">Menü öffnen</b></label>')
    t = kopf + '</head>' + rest
    if t != o: open(f, 'w', encoding='utf-8').write(t); print('Farben:', os.path.basename(f))
