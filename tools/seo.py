#!/usr/bin/env python3
"""SEO-Kopf, Sitemap und Prüfung für mw-projekt-navigation.com.

  python3 tools/seo.py          schreibt den SEO-Block in jede Seite und erzeugt sitemap.xml
  python3 tools/seo.py --check  prüft alle Seiten (bricht mit Fehler ab, wenn etwas nicht passt)

Der Block zwischen <!-- SEO:START --> und <!-- SEO:END --> im <head> wird immer neu erzeugt.
Daten kommen aus tools/seiten.json. FAQ-Schema wird aus <details class="faq"> auf der Seite gelesen.
"""
import html, json, os, re, sys, datetime
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(__file__), '..', 'www')
CFG = json.load(open(os.path.join(os.path.dirname(__file__), 'seiten.json'), encoding='utf-8'))
D = CFG['domain']
F = CFG['firma']
HEUTE = datetime.date.today().isoformat()

FONT = """<link rel="preload" href="/assets/fonts/inter-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>@font-face{font-family:'Inter';src:url('/assets/fonts/inter-var-latin.woff2') format('woff2');font-weight:100 900;font-style:normal;font-display:swap}</style>"""


def faqs_aus(text):
    out = []
    for m in re.finditer(r'(?s)<details class="faq">\s*<summary>(.*?)</summary>(.*?)</details>', text):
        q = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        a = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()
        out.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return out


def org():
    return {
        "@type": ["Organization", "ProfessionalService"], "@id": D + "/#org",
        "name": F['name'], "legalName": F['legalName'], "url": D + "/",
        "logo": D + F['logo'], "image": D + CFG['ogBild'],
        "description": F['beschreibung'], "telephone": F['telefon'], "email": F['email'],
        "vatID": F['ustid'],
        "address": {"@type": "PostalAddress", "streetAddress": F['strasse'], "postalCode": F['plz'],
                    "addressLocality": F['ort'], "addressCountry": F['land']},
        "areaServed": {"@type": "Country", "name": "Deutschland"},
        "knowsAbout": F['themen'],
        "employee": [{"@type": "Person", "name": n, "jobTitle": "Geschäftsführer", "worksFor": {"@id": D + "/#org"}}
                     for n in F['geschaeftsfuehrung']],
    }


def block(s, text):
    url = D + s['pfad']
    graph = [org(), {"@type": "WebSite", "@id": D + "/#website", "url": D + "/", "name": F['name'],
                     "inLanguage": "de-DE", "publisher": {"@id": D + "/#org"}}]
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": s['title'],
            "description": s['description'], "inLanguage": "de-DE",
            "isPartOf": {"@id": D + "/#website"}, "about": {"@id": D + "/#org"}}
    if s['pfad'] != '/':
        page["breadcrumb"] = {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": D + "/"},
            {"@type": "ListItem", "position": 2, "name": s['name'], "item": url}]}
    graph.append(page)
    if s.get('service'):
        graph.append({"@type": "Service", "@id": url + "#service", "name": s['service']['name'],
                      "serviceType": s['service']['typ'], "provider": {"@id": D + "/#org"},
                      "areaServed": {"@type": "Country", "name": "Deutschland"}, "url": url})
    for x in s.get('extra', []):
        graph.append(x)
    fq = faqs_aus(text)
    if fq:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": fq})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(',', ':'))
    e = html.escape
    zeilen = [
        '<!-- SEO:START (wird von tools/seo.py erzeugt, nicht von Hand ändern) -->',
        f'<title>{e(s["title"])}</title>',
        f'<meta name="description" content="{e(s["description"])}">',
    ]
    if s.get('noindex'):
        zeilen.append('<meta name="robots" content="noindex, follow">')
    else:
        zeilen.append(f'<link rel="canonical" href="{url}">')
    zeilen += [
        '<link rel="icon" type="image/svg+xml" href="/assets/logo-full.svg">',
        '<meta property="og:locale" content="de_DE">',
        f'<meta property="og:site_name" content="{e(F["name"])}">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{e(s["title"])}">',
        f'<meta property="og:description" content="{e(s["description"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{D}{CFG["ogBild"]}">',
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        FONT,
    ]
    if s.get('preloadHero'):
        zeilen.append('<link rel="preload" as="image" href="/assets/hero-gebaeude-800.webp" media="(max-width: 800px)" fetchpriority="high">')
        zeilen.append('<link rel="preload" as="image" href="/assets/hero-gebaeude.webp" media="(min-width: 801px)" fetchpriority="high">')
    zeilen.append(f'<script type="application/ld+json">{ld}</script>')
    zeilen.append('<!-- SEO:END -->')
    return '\n'.join(zeilen)


def schreiben():
    for s in CFG['seiten']:
        p = os.path.join(ROOT, s['datei'])
        t = open(p, encoding='utf-8').read()
        if '<!-- SEO:START' not in t:
            # Alte Kopfangaben entfernen, Block direkt nach viewport einsetzen
            t = re.sub(r'\s*<title>.*?</title>', '', t, count=1, flags=re.S)
            t = re.sub(r'\s*<meta name="description"[^>]*>', '', t)
            t = re.sub(r'\s*<link rel="icon"[^>]*>', '', t)
            t = re.sub(r'\s*<link rel="preconnect"[^>]*>', '', t)
            t = re.sub(r'\s*<link href="https://fonts\.googleapis\.com[^>]*>', '', t)
            t = t.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                          '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<!-- SEO:START --><!-- SEO:END -->', 1)
        t = re.sub(r'(?s)<!-- SEO:START.*?<!-- SEO:END -->', lambda m: block(s, t), t, count=1)
        open(p, 'w', encoding='utf-8').write(t)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for s in CFG['seiten']:
        if s.get('sitemap'):
            sm.append(f'  <url><loc>{D}{s["pfad"]}</loc><lastmod>{s.get("lastmod", HEUTE)}</lastmod><priority>{s.get("prio","0.5")}</priority></url>')
    sm.append('</urlset>')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
    print('SEO-Block und sitemap.xml geschrieben.')


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.h1 = 0; s.imgs = []; s.links = []; s.cur = None; s.title = ''; s.desc = None; s.canon = None; s.ld = []; s.inld = False
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == 'h1': s.h1 += 1
        if t == 'img': s.imgs.append(a)
        if t == 'a' and a.get('href'): s.links.append(a['href'])
        if t == 'title': s.cur = 'title'
        if t == 'meta' and a.get('name') == 'description': s.desc = a.get('content')
        if t == 'link' and a.get('rel') == 'canonical': s.canon = a.get('href')
        if t == 'script' and a.get('type') == 'application/ld+json': s.inld = True
    def handle_endtag(s, t):
        if t == 'title': s.cur = None
        if t == 'script': s.inld = False
    def handle_data(s, d):
        if s.cur == 'title': s.title += d
        if s.inld: s.ld.append(d)


def pruefen():
    fehler = []
    dateien = {s['datei']: s for s in CFG['seiten']}
    vorhanden = set(os.listdir(ROOT))
    for s in CFG['seiten']:
        n = s['datei']; t = open(os.path.join(ROOT, n), encoding='utf-8').read()
        p = P(); p.feed(t)
        if len(p.title) > 60: fehler.append(f'{n}: Title {len(p.title)} Zeichen (max. 60)')
        if not p.desc or not (110 <= len(p.desc) <= 160): fehler.append(f'{n}: Description {len(p.desc or "")} Zeichen (110 bis 160)')
        if p.h1 != 1: fehler.append(f'{n}: {p.h1} H1')
        if not s.get('noindex') and p.canon != D + s['pfad']: fehler.append(f'{n}: Canonical fehlt oder falsch')
        try: json.loads(''.join(p.ld))
        except Exception as ex: fehler.append(f'{n}: JSON-LD kaputt ({ex})')
        if 'fonts.googleapis' in t or 'fonts.gstatic' in t: fehler.append(f'{n}: lädt noch Google Fonts')
        if 'TODO' in t: fehler.append(f'{n}: enthält TODO')
        for i in p.imgs:
            if not (i.get('width') and i.get('height')): fehler.append(f'{n}: Bild ohne width/height: {i.get("src")}')
            if not i.get('alt'): fehler.append(f'{n}: Bild ohne Alt-Text: {i.get("src")}')
            if i.get('src', '').startswith('/') and not os.path.exists(ROOT + i['src']): fehler.append(f'{n}: Bild fehlt: {i["src"]}')
        for l in p.links:
            if l.startswith('/') and not l.startswith('//'):
                pfad = l.split('#')[0].split('?')[0]
                if pfad in ('', '/'): continue
                kand = pfad.lstrip('/')
                if not (kand + '.html' in vorhanden or kand in vorhanden or os.path.exists(os.path.join(ROOT, kand))):
                    fehler.append(f'{n}: interner Link ins Leere: {l}')
            if l.endswith('.html') and l.startswith('/'): fehler.append(f'{n}: Link mit .html: {l}')
    for f in vorhanden:
        if f.endswith('.html') and f not in dateien and not f.startswith('google'):
            fehler.append(f'{f}: Seite fehlt in tools/seiten.json')
    for f in ('robots.txt', 'sitemap.xml', '.htaccess'):
        if not os.path.exists(os.path.join(ROOT, f)): fehler.append(f'{f} fehlt')
    if fehler:
        print('\n'.join('FEHLER: ' + x for x in fehler)); sys.exit(1)
    print(f'Prüfung bestanden ({len(dateien)} Seiten).')


if __name__ == '__main__':
    pruefen() if '--check' in sys.argv else schreiben()
