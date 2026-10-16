# Changelog

All notable changes to the portfolio. Newest first. Versions follow the label in the page footer
(`Portfolio version X.Y.Z`); every release should get a matching git tag (`git tag v1.2.0`).

Version numbers restart at 1.2.0, the first production release. Entries 3.0 to 4.7 below are the internal
development iterations that led to it.

## 1.2.2 - October 2026

- Experience: role descriptions unified with LinkedIn and the CVs (EN/FR/ES). Every role now has a short
  header line, the same bullets as the CV and a "Tech:" (or "Skills:") footer. CCA is described with
  .NET Framework; the SharePoint intranet app lives under Projects.
- The three CV PDFs in `assets/docs/` replaced with the updated versions.
- No change to `api/` or the visit counter (Redis key `portfolio:visits:total`).

## 1.2.1 - October 2026

Patch release after the first production deploy.

- Desktop scale: on screens wider than 1140 px the page is scaled to 80 % (`zoom: 0.8` in `css/site.css`), which is the size the layout was designed at. Phones and tablets are unchanged.
- Resume: the header of the EN/FR/ES PDFs now reads "LinkedIn: ... | Portfolio: jhon-diazportfolio.vercel.app" with both links clickable (CV 12.2). The GitHub entry was removed from that line.
- Hero rotator: the "ERP Analyst" slide is now "Microsoft Dynamics ERP", with the tags "ERP Manager" and "ERP Professional" (EN/FR/ES).

## 1.2.0 - October 2026

Production release (internal iteration 4.7 plus the changes below).

- Education: the ISI entry is now Collège Universel (which took over the ISI), with its logo and website. The Universidad Distrital entry has the official shield and the university's website.
- Resume buttons: the EN/FR/ES PDFs now list Collège Universel (CV 12.1).
- Tooling: the build runs Prettier on Windows (prettier.cmd) and `.gitattributes` keeps LF line endings.
- Education: the course "Certificate (PDF)" link sits on the same row as the date instead of a new row.

## 4.7 - October 2026

- Projects: "Phrase Audio" (web app that turns a bilingual PDF phrase list into a study MP3) replaces
  "Contact Manager" and sits in the three-card row. New demo video (`assets/media/project-6.mp4`)
  and thumbnail; descriptions in EN/FR/ES.
- Project order: Intranet, TCM (both full-width), then Music Albums, Phrase Audio and Budget in one row.
  Phrase Audio has no GitHub or YouTube buttons.

## 4.6 - October 2026

- Code organization: the page generator moved to `tools/build.py` (+ `tools/es_dict.py`), with English
  documentation and `#region` sections in every source file; all files formatted with Prettier.
- Fix: invalid HTML in the "Programming languages" row (a list inside a paragraph). The two groups now
  render on one line each with aligned chips.
- Fix: the header was 11 px too wide on 390 px phones, which made the page scroll sideways.
- Docs: new README, `.env.example`, this changelog.

## 4.5 - October 2026

- TCM project video: the login screen is back, with the user and password values covered.
- TCM description now mentions plant calendars, shift schedules, and roles and permissions.

## 4.4 - October 2026

- TCM video: the author credit of the process diagram is covered; the video starts after the login.
- Longer TCM description: ERP interface, data capture and processing, delivery to BI, real time.

## 4.3 - October 2026

- Skills order: Programming languages, Business software, Methodologies and support.
- The "Time Control Manufacture (TCM)" project replaces "ERP database maintenance".
- New silent 1:20 TCM video (was 4:43 with narration); the user name is covered.

## 4.2 - October 2026

- Header labels never wrap (Spanish and French are longer); the menu collapses to the hamburger below 1140 px.

## 4.1 - October 2026

- Longer company descriptions for CCA, Boardwalk and Permoda (EN/FR/ES).
- Real logos for Academia Smart and Centre Yves-Thériault.
- Fundación Carlos Slim courses: removed the "Verify credential" link, kept the PDF certificate.
- The Resume buttons download the CV in the language being displayed (EN, FR or ES).
- CV 12.0 in three languages; French studies start in Oct 2022.

## 4.0 - October 2026

- Experience cards: header (role, company, period + duration badge, description), company photo and the
  full list of duties.
- Removed the extra space above every section when navigating from the tabs.

## 3.9 - October 2026

- Home tab and clickable name; "Back to top" scrolls to the very top.
- Project renamed "Intranet Site - SharePoint".
- New "ERP Analyst" and "Enterprise Applications" rotating titles.
- "AI-assisted development" skills row and a sentence about it in About.

## 3.0 - 3.8 - 2026

- Redesign: glacier palette, light/dark theme, English/French/Spanish switch.
- Rotating role titles in the hero, portrait with location pill, "Open to work" status.
- Project dialog with YouTube (privacy mode) or local video.
- Visit counter (Upstash Redis) and contact form (Resend + Redis backup, honeypot, rate limit).
- Education logos and links, Lourtec certificates with the ID number covered.
