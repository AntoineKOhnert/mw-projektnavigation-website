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

## 2026-10-21 (Podcast-Seite, graue Projektkarte, PageSpeed Barrierefreiheit)
- Neue Seite /podcast mit dem Spotify-Podcast "MW-Projekt-Navigation" (Experte Joachim M. Werno). Player als 2-Klick-Lösung: Spotify lädt erst nach Klick auf "Podcast laden". Podcast in Navigation, Footer, Sitemap und Schema (PodcastSeries). Wunsch von Antoine.
- Datenschutzerklärung: neuer Abschnitt 7 "Podcast-Player von Spotify", Hinweis im Cookie-Abschnitt, folgende Abschnitte neu nummeriert (8 bis 11).
- Startseite: Projektkarte Arztquartier Bremen grau statt schwarz, wie der Kasten "Planung von innen nach außen" auf der Referenzseite. Wunsch von Antoine.
- PageSpeed Barrierefreiheit (Handy 92): Orange als Textfarbe und auf Buttons dunkler (tools/farben.py, Kontrast nach WCAG AA), Signal-Orange bleibt für Flächen, Icons und im Hero. Menü-Button mit unsichtbarem Text statt unzulässigem aria-label. Phasen-Nummern 01 bis 04 als Deko markiert. Lokal geprüft: Barrierefreiheit, Best Practices und SEO je 100.
- Navigation bricht auf mittleren Bildschirmbreiten nicht mehr um.
