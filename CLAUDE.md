# mw-projekt-navigation.com – Anweisungen für Claude

Statische Website der MW Projekt Navigation GmbH (Köln, Projekte deutschlandweit). Kein CMS, kein Build-Framework.
Kunde von Antoine Kohnert (AK Media). Hosting: united-domains Webspace, Ordner `www`.

## Ablauf
- `www/` ist die einzige Quelle. Nie direkt per FTP/FileZilla hochladen, sonst überschreibt der nächste Upload die Änderung.
- Jeder Push auf `main`, der `www/` oder `tools/` ändert, startet `.github/workflows/website-hochladen.yml`: Changelog-Pflicht → `python3 tools/seo.py --check` → SFTP-Upload → Live-Test (bei Fehler wird `tools/notfall.htaccess` hochgeladen).
- Danach läuft automatisch "Live-Check Domain" (Ergebnis auf Branch `live-check`: abrufe.txt, dateien.txt, lighthouse.txt).
- Zugangsdaten nur als GitHub-Secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`).
- Auf dem Server wird nichts gelöscht. Löschen nur nach ausdrücklicher Bestätigung von Antoine.
- `kontakt.php` liegt nur auf dem Server, nicht im Repo (kann Zugangsdaten enthalten). Nicht überschreiben.

## Pflicht bei jeder Änderung
- Eintrag in `docs/changelog.md` im selben Commit, sonst bricht der Upload ab.
- Titel, Description, Canonical, OG und Schema nie von Hand im `<head>` ändern: `tools/seiten.json` anpassen, dann `python3 tools/seo.py` (schreibt den Block zwischen `<!-- SEO:START -->` und `<!-- SEO:END -->` und die sitemap.xml). Danach `python3 tools/seo.py --check`.
- Neue Seite: Inhalt als `tools/inhalt/<slug>.html`, dann `python3 tools/neue_seite.py tools/inhalt/<slug>.html`, Eintrag in `tools/seiten.json`, dann `python3 tools/farben.py` und `python3 tools/seo.py`. Neue Seite auch in Navigation und Footer aller Seiten eintragen. Die zwei Schwerpunktseiten und 404 werden so gebaut: Text dort ändern, nicht in www/.
- FAQ immer als `<details class="faq"><summary>Frage</summary><div><p>Antwort</p></div></details>`, das FAQ-Schema entsteht daraus automatisch.
- .htaccess vor dem Push lokal auf Apache testen (Skill htaccess-https).

## Regeln
- Siezen auf der ganzen Seite.
- Fokus: Projektsteuerung für Ärztezentren, Praxen und Gewerbebau, deutschlandweit. Köln nur als Sitz.
- Keine erfundenen Fakten, Zahlen, Projekte oder Personen-Details. Belegt ist nur, was in referenzen.html und ueber-uns.html steht. Zum Team (Maximilian F. Lux, Joachim M. Werno) gibt es noch keine Fotos und Werdegänge.
- Schreibregeln: erster Satz kurz, keine KI-Floskeln ("entscheidend", "ganzheitlich", "nicht nur X sondern Y", "Landschaft"), gerade Anführungszeichen, echte Umlaute, maximal ein Gedankenstrich pro Absatz, keine Emojis.
- Kein aggregateRating im Schema.
- Farben: Es gibt nur ein Orange, das Logo-Orange #FC6820 (Wunsch Antoine 21.10.2026). Gilt für Buttons, Schrift, Links, Icons und Flächen. Kein dunkleres Zweit-Orange, auch nicht für Hover. Button-Schrift dunkel (var(--ink)). Nach jeder CSS-Änderung `python3 tools/farben.py` laufen lassen.
- Externe Einbettungen (Spotify, YouTube, Karten) nur als 2-Klick-Lösung und mit Abschnitt in der Datenschutzerklärung.
