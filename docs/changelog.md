# Changelog mw-projekt-navigation.com

## 2026-10-21 (Seite ins Repo, SEO/GEO-Grundlagen, zwei neue Seiten)
- Stand vom Server (Ordner www) ins Repo übernommen. Ab jetzt ist www/ in diesem Repo die einzige Quelle, Upload per GitHub Actions.
- .htaccess aktiv (vorher lag nur htaccess.txt auf dem Server): www -> ohne www, http -> https, URLs ohne .html, /index.html -> /, eigene 404-Seite, Browser-Caching, Sicherheits-Header. Lokal auf Apache getestet. htaccess.txt wird nicht mehr ausgeliefert.
- robots.txt und sitemap.xml neu, KI-Crawler ausdrücklich erlaubt.
- Alle Seiten: Canonical, Open Graph, strukturierte Daten (Organization mit Geschäftsführung, WebSite, WebPage, Breadcrumbs, Service, FAQPage), Meta-Description für Impressum und Datenschutz. Erzeugt von tools/seo.py.
- Schrift Inter lokal statt Google Fonts (assets/fonts/), Datenschutzerklärung Abschnitt 6 angepasst.
- Ladezeit: Hero-Bild bevorzugt laden, kleines Hero-Bild für Handys, Bildmaße gesetzt, Lazy Loading, Gruppenlogos auf 240 px verkleinert.
- Startseite: Fokus Projektsteuerung für Ärztezentren, Praxen und Gewerbebau, deutschlandweit statt Köln. Neuer FAQ-Bereich (6 Fragen), Links zu den neuen Seiten, Geschäftsführung genannt, Häkchen aus den Überschriften entfernt.
- Neue Seiten /projektsteuerung-aerztezentrum und /projektsteuerung-gewerbebau (je rund 1.200 Wörter, mit FAQ). Wunsch von Antoine.
- Über uns: Absatz Geschäftsführung (nur Namen und belegte Fakten, Fotos und Werdegang folgen).
- Leistungsseite inhaltlich unverändert (Wunsch von Antoine), nur Technik und Footer.
