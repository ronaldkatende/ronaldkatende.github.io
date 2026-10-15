# Ronald Katende — academic website (October 2026)

Static, responsive academic website prepared from `RKatende_CV_mestwe.tex`.

## Files

- `index.html`: homepage and selected recent publications
- `publications.html`: full searchable publication list (11 entries from CV)
- `research.html`: research directions
- `projects.html`: selected projects with explicit status labels
- `about.html`: academic biography and teaching
- `assets/styles.css`, `assets/main.js`: design and mobile navigation/publication filters
- `cv/ronald-katende-cv.pdf`: four-page CV
- `cv/ronald-katende-cv.tex`: editable LaTeX source
- `.nojekyll`, `sitemap.xml`, `robots.txt`, `404.html`: GitHub Pages helpers

## Publish to GitHub Pages

1. Back up the current repository. The ZIP is a **full replacement site**, not a patch to an unknown existing codebase.
2. Open `https://github.com/ronaldkatende/ronaldkatende.github.io` (or the repository currently configured for your Pages site).
3. Upload the **contents** of this folder to the repository root; preserve `assets/` and `cv/` folders. Commit to the branch used by GitHub Pages (commonly `main`).
4. In Settings → Pages, check that the site publishes from the intended branch/root. If your live site uses custom domain or extra assets, preserve those files before replacement.
5. Visit `https://ronaldkatende.github.io/` after deployment. Test Home → Publications → Research → Projects → About and the CV link.

No build tools, dependencies, external fonts or APIs are required. Open `index.html` locally to preview; for a local web server, run `python -m http.server 8000` in the folder and open `http://localhost:8000`.

## Updating publications

The publication list is **pre-rendered** into `publications.html`, and the homepage contains three hand-selected featured papers. `assets/main.js` filters existing HTML; it does not fetch data or generate publication records. To add papers, update the HTML cards in `publications.html` and, if desired, feature them in `index.html`. Update the academic CV separately.

## Accuracy notes

- Bibliographic details, academic appointments, awards and research activities were taken from the supplied CV, not independently verified against third-party databases.
- Paper links were copied from CV DOI/publisher URLs. Verify all entries and status before public release.
- Projects distinguish published work from early prototypes and ongoing investigations.
- No publication counts, citation metrics, or unavailable repository URLs have been invented.
