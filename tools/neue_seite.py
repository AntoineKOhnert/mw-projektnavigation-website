#!/usr/bin/env python3
"""Baut eine Inhaltsseite im Layout der Unterseiten (Vorlage: www/leistungen.html).
   python3 tools/neue_seite.py tools/inhalt/<name>.html   -> www/<name>.html"""
import os, re, sys
ROOT = os.path.join(os.path.dirname(__file__), '..', 'www')
CSS = """
  /* Inhaltsseiten (Schwerpunkte) */
  .about h3{font-size:19px;font-weight:700;letter-spacing:-.01em;margin:28px 0 8px}
  .about a{color:var(--orange-dark);font-weight:600}
  .about a.btn{color:#fff}
  .about a.btn-ghost{color:var(--ink)}
  .about a.btn-ghost:hover{color:var(--orange-dark)}
  .about ol.phasen{margin:10px 0 18px 0;padding-left:22px}
  .about ol.phasen li{margin-bottom:10px;padding-left:4px}
  .zahlen{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:22px 0 22px}
  .zahlen div{background:var(--cream);border:1px solid var(--line);border-radius:12px;padding:16px 14px}
  .zahlen b{display:block;font-size:21px;letter-spacing:-.02em}
  .zahlen span{font-size:13.5px;color:var(--ink-soft)}
  .tabelle{overflow-x:auto;margin:16px 0 18px;border:1px solid var(--line);border-radius:12px}
  .tabelle table{border-collapse:collapse;width:100%;min-width:560px;font-size:14.5px;line-height:1.5}
  .tabelle th,.tabelle td{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid var(--line)}
  .tabelle thead th{background:var(--cream);font-weight:700}
  .tabelle tbody th{font-weight:600;color:var(--ink-soft);width:22%}
  .tabelle tr:last-child th,.tabelle tr:last-child td{border-bottom:0}
  .faqs{margin-top:10px}
  details.faq{border:1px solid var(--line);border-radius:12px;padding:0 18px;margin-bottom:10px;background:#fff}
  details.faq summary{cursor:pointer;list-style:none;font-weight:600;padding:16px 28px 16px 0;position:relative}
  details.faq summary::-webkit-details-marker{display:none}
  details.faq summary::after{content:"+";position:absolute;right:0;top:12px;font-size:22px;color:var(--orange-dark);font-weight:400}
  details.faq[open] summary::after{content:"–"}
  details.faq > div{padding:0 0 6px}
  .cta-box{margin-top:48px;background:var(--ink);color:#fff;border-radius:18px;padding:34px 32px}
  .cta-box h2{margin:0 0 10px;color:#fff}
  .cta-box p{color:#d8d2cc}
  .player{background:var(--cream-deep);border:1px solid var(--line);border-radius:16px;padding:26px 28px;margin:30px 0 10px}
  .player.geladen{padding:0;background:none;border:0}
  .player b{display:block;font-size:18px;margin-bottom:6px}
  .player p{font-size:14.5px;color:var(--ink-soft)}
  .player-aktionen{display:flex;gap:12px;flex-wrap:wrap;margin-top:6px}
  .player button.btn{border:0;cursor:pointer;font-family:inherit}
  nav ul a{white-space:nowrap}
  @media(min-width:921px) and (max-width:1240px){nav ul{gap:16px}nav ul a{font-size:14px}}
  @media(max-width:640px){.zahlen{grid-template-columns:1fr 1fr}.cta-box{padding:28px 22px}}
"""
def main(src):
    name = os.path.basename(src)
    vorlage = open(os.path.join(ROOT, 'leistungen.html'), encoding='utf-8').read()
    inhalt = open(src, encoding='utf-8').read()
    # Leistungs-spezifisches CSS raus, Inhalts-CSS rein
    t = re.sub(r'(?s)\s*/\* Leistungsverzeichnis \*/.*?(?=</style>)', '\n', vorlage)
    kopf, rest = t.split('</head>', 1)
    i = kopf.rfind('</style>')
    t = kopf[:i] + CSS + kopf[i:] + '</head>' + rest
    t = re.sub(r'(?s)<main>.*?</main>', '<main>\n  <div class="wrap about">\n' + inhalt + '  </div>\n</main>', t, count=1)
    t = re.sub(r'(?s)<!-- SEO:START.*?<!-- SEO:END -->', '<!-- SEO:START --><!-- SEO:END -->', t, count=1)
    open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(t)
    print('geschrieben:', name)
if __name__ == '__main__':
    for a in sys.argv[1:]: main(a)
