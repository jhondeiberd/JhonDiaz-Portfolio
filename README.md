# Jhon Diaz portfolio

Static portfolio (English / French / Spanish, light / dark) with two small Vercel serverless functions
for the visit counter and the contact form. Current version: **1.2.1** (see `CHANGELOG.md`).

## Structure

```
index.html            GENERATED page (English text + data-i18n keys). Do not edit by hand.
css/site.css          Single stylesheet, organised in numbered #regions (see the header comment)
js/app.js             Front-end logic, organised in numbered #regions
js/i18n-fr.js         GENERATED French dictionary        (window.I18N_FR)
js/i18n-es.js         GENERATED Spanish dictionary       (window.I18N_ES)
js/i18n-ui.js         GENERATED messages used by app.js  (window.I18N_JS = [en, fr, es])
api/contact.js        POST /api/contact   validates, stores in Redis, emails through Resend
api/visits.js         GET/POST /api/visits  visit counter
api/status.js         GET /api/status[?ping=1]  true/false configuration flags, never secrets
api/_redis.js         Upstash REST client   (files starting with _ are not routes)
api/_util.js          shared helpers (IP hash, JSON replies, body parsing)
tools/build.py        generator for index.html and the three i18n files
tools/es_dict.py      Spanish text, keyed by the exact English string
assets/               fonts, images, project videos, CVs and certificates (PDF)
vercel.json           security and cache headers
.prettierrc.json      formatting rules
```

All source files use `#region` / `#endregion` markers: fold them in your editor to move around quickly.
Comments are in English by convention.

## Editing content

Text, projects, jobs and education live in **`tools/build.py`** (English and French side by side) and
**`tools/es_dict.py`** (Spanish). Never edit `index.html` or `js/i18n-*.js` directly: they are overwritten.

1. Edit `tools/build.py` (and `tools/es_dict.py` if an English string changed or is new).
2. `npm install` (once), then `npm run build`. The build stops with `MISSING ES` if a Spanish entry is missing.
3. Review the result locally (below), update the version label in the footer and `CHANGELOG.md`.
4. Commit, tag and push.

| I want to...                      | Edit                                                             |
| --------------------------------- | ---------------------------------------------------------------- |
| Change a job, a course or a skill | `tools/build.py`, regions 6, 7 and 9                             |
| Add a project                     | `tools/build.py` region 8 + its media in `assets/media/`         |
| Change colours or spacing         | `css/site.css`, region 2 (tokens) or the region of the section   |
| Change rotating hero titles       | `ROLES` in `tools/build.py`, region 4                            |
| Update the CV                     | replace `assets/docs/Jhon_Diaz_CV_EN.pdf`, `_FR.pdf`, `_ES.pdf`  |
| Bump the version                  | footer text in `tools/build.py` + `tools/es_dict.py` + CHANGELOG |

## Run locally

```bash
npm install
npm run build          # regenerate index.html and js/i18n-*.js (on Windows without python3: python tools/build.py)
python3 -m http.server 4000   # page only (form and counter need the API)
npx vercel dev         # page + /api functions (needs the environment variables)
npm run format         # Prettier on every source file; `npm run format:check` only checks
```

## Deploy (GitHub + Vercel)

1. Push this folder to a GitHub repository. In Vercel choose **Add New > Project**, import the repository
   and keep the defaults (no build command; the generated files are committed). Every `git push` redeploys.
2. **Visit counter and message backup**: Vercel > project > Storage > Create > Upstash (Redis) > connect.
3. **Contact emails**: create an API key at resend.com and add it as `RESEND_API_KEY`. Without a verified
   domain, Resend only delivers to the account owner's address.
4. Check it: open `/api/status?ping=1` (flags only) and `/?debug=1` (shows why the counter is hidden).

Environment variables are listed in `.env.example`. Real values live only in Vercel.

## Releases

```bash
git add -A
git commit -m "v1.2.1: short description"
git tag v1.2.1
git push && git push --tags
```

## Videos and files

Each project card carries `data-youtube` (YouTube id, privacy mode) and a local `assets/media/project-N.mp4`;
the YouTube player wins when an id is set. Keep local videos short, silent and free of personal data
(logins, names, IDs).

## Privacy and copyright

- The Lourtec certificate PDFs in `assets/docs/` have the national ID covered: never replace them with the originals.
- Anything served to a browser can be downloaded, so publish only material you are happy to see copied.
- Do not publish employer code or screens without permission.
- Content (text, photos, videos, CVs) is copyright Jhon Deiber Diaz Parra, all rights reserved, unless a
  licence file says otherwise.
