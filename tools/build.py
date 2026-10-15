"""Generates the whole site from one source so every language stays in sync.

Run from the repository root:   python3 tools/build.py        (or: npm run build)

Inputs
  tools/build.py      this file: page structure, English text and French text side by side
  tools/es_dict.py    Spanish translation of every English string (keyed by the exact English text)

Outputs (generated, do not edit by hand)
  index.html          English content, SEO friendly, every translatable node has data-i18n="tNNN"
  js/i18n-fr.js       window.I18N_FR   French text by key
  js/i18n-es.js       window.I18N_ES   Spanish text by key
  js/i18n-ui.js       window.I18N_JS   messages used by app.js: [English, French, Spanish]

The build stops with "MISSING ES" if an English string has no Spanish entry in tools/es_dict.py.
After generating, it formats the outputs with Prettier when `npm install` has been run.

Regions of this file (fold them with "# region"):
  1. Setup and helpers          key(), el(), ia(), li(), icon()
  2. Messages used by app.js    the JS dictionary
  3. Static fragments           meta description, SVG icon sprite, hero ridge
  4. Role titles and header     rotating hero roles, navigation, header bar
  5. Hero and About
  6. Skills
  7. Experience                 job() cards and the "earlier roles" block
  8. Projects                   project() cards
  9. Education                  edu() items, certificate links
 10. Contact and footer
 11. Page assembly              the full HTML document
 12. Output and validation      writes the files, checks translations
"""
import html
import json
import os
import subprocess
import sys

# Repository root = the folder that contains tools/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = ROOT + os.sep
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# region 1. Setup and helpers
REG = {}   # key -> (en, fr)
_n = [0]


def key(en, fr):
    """Registers an (English, French) pair and returns its key (t001, t002...) in order of creation."""
    _n[0] += 1
    k = 't%03d' % _n[0]
    REG[k] = (en, fr)
    return k


def el(tag, en, fr, cls='', attrs=''):
    """Translatable element: English text in the HTML, French and Spanish looked up by data-i18n."""
    k = key(en, fr)
    c = f' class="{cls}"' if cls else ''
    a = f' {attrs}' if attrs else ''
    return f'<{tag}{c}{a} data-i18n="{k}">{en}</{tag}>'


def ia(**pairs):
    """Translatable attributes: ia(**{'aria-label': ('Close','Fermer')}) -> aria-label="Close" data-i18n-attr="aria-label:tNNN" """
    parts, keys = [], []
    for attr, (en, fr) in pairs.items():
        k = key(en, fr)
        parts.append(f'{attr}="{html.escape(en, quote=True)}"')
        keys.append(f'{attr}:{k}')
    return ' '.join(parts) + f' data-i18n-attr="{";".join(keys)}"'


def li(en, fr):
    """Translatable <li>."""
    return el('li', en, fr)


def icon(name, cls='icon'):
    """Inline SVG icon that references a <symbol> of the sprite (see SPRITE)."""
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


# endregion


# region 2. Messages used by app.js
# JS-side strings (used by app.js through tr()) ----------------------------------------------
JS = {
    'sending': ('Sending…', 'Envoi en cours…'),
    'send': ('Send message', 'Envoyer le message'),
    'form_ok': ('Message sent. I will reply as soon as I can.', 'Message envoyé. Je vous répondrai dès que possible.'),
    'form_invalid': ('Check the highlighted fields and try again.', 'Vérifiez les champs en surbrillance et réessayez.'),
    'form_rate': ('Too many messages in a short time. Try again later or email me directly:', 'Trop de messages en peu de temps. Réessayez plus tard ou écrivez-moi directement :'),
    'form_down': ('The message could not be sent. Email me directly:', 'Le message n’a pas pu être envoyé. Écrivez-moi directement :'),
    'form_net': ('No connection. Check your network and try again, or email me directly:', 'Aucune connexion. Vérifiez votre réseau et réessayez, ou écrivez-moi directement :'),
    'visits': ('visits', 'visites'),
    'form_local': ('The form only works on the published site, because it needs the server functions. Email me directly:', 'Le formulaire ne fonctionne que sur le site publié, car il a besoin des fonctions serveur. Écrivez-moi directement :'),
    'preview': ('preview: the counter starts once the site is published', 'aperçu : le compteur démarre une fois le site publié'),
    'theme_to_dark': ('Switch to dark theme', 'Passer au thème sombre'),
    'theme_to_light': ('Switch to light theme', 'Passer au thème clair'),
    'menu_open': ('Open menu', 'Ouvrir le menu'),
    'menu_close': ('Close menu', 'Fermer le menu'),
    'code': ('View code on GitHub', 'Voir le code sur GitHub'),
    'youtube': ('Watch on YouTube', 'Voir sur YouTube'),
    'close': ('Close', 'Fermer'),
    'demo_label': ('Project demo video', 'Vidéo de démonstration du projet'),
}

# ------------------------------------------------------------------------------------------------
# endregion


# region 3. Static fragments
head_meta_desc = ia(content=(
    'Portfolio of Jhon Deiber Diaz Parra, software developer in Alberta, Canada: C# / ASP.NET Core, REST APIs, SQL Server, Microsoft Graph API and SharePoint. English, French and Spanish.',
    'Portfolio de Jhon Deiber Diaz Parra, développeur logiciel en Alberta (Canada) : C# / ASP.NET Core, API REST, SQL Server, Microsoft Graph API et SharePoint. Anglais, français et espagnol.'))
title_key = key('Jhon Diaz | Software developer: .NET, C#, REST APIs, SQL Server',
                'Jhon Diaz | Développeur logiciel : .NET, C#, API REST, SQL Server')

SPRITE = '''
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <defs>
    <symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></symbol>
    <symbol id="i-moon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></symbol>
    <symbol id="i-mail" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></symbol>
    <symbol id="i-phone" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></symbol>
    <symbol id="i-pin" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></symbol>
    <symbol id="i-download" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></symbol>
    <symbol id="i-pause" viewBox="0 0 24 24"><path d="M8 5v14M16 5v14"/></symbol>
    <symbol id="i-play" viewBox="0 0 24 24"><path d="M7 4.5v15l12-7.5z"/></symbol>
    <symbol id="i-x" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path d="M3 7h18M3 12h18M3 17h18"/></symbol>
    <symbol id="i-github" viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></symbol>
    <symbol id="i-linkedin" viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></symbol>
    <symbol id="i-external" viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14 21 3"/></symbol>
    <symbol id="i-eye" viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></symbol>
    <symbol id="i-translate" viewBox="0 0 24 24"><path d="M4 5h9M8.5 3v2M6 5c0 4 3 7 6 8M12 5c-1 4-4 7-7 8M13 21l4-10 4 10M14.5 18h5"/></symbol>
    <symbol id="i-chat" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></symbol>
  </defs>
</svg>'''

RIDGE = '''<svg class="hero__ridge" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true" focusable="false">
  <path class="ridge ridge--far" d="M0 220V120l90-48 70 34 110-86 80 62 70-30 120 78 90-58 110 70 100-96 90 74 80-46 110 82 100-64 90 52 100-34 100 62H1440V220z"/>
  <path class="ridge ridge--near" d="M0 220V160l130-52 90 44 120-70 100 78 110-54 140 66 100-60 130 70 120-58 110 50 110-34 100 60H1440V220z"/>
</svg>'''


# endregion


# region 4. Role titles and header
ROLES = [
    (('Software Developer', 'Développeur logiciel'), [('Full Stack Developer', 'Développeur full stack')]),
    (('Back-End Developer', 'Développeur back-end'), [('SQL Server Developer', 'Développeur SQL Server'), ('API Developer', 'Développeur d’API'), ('Integration Developer', 'Développeur d’intégration')]),
    (('Front-End Developer', 'Développeur front-end'), [('JavaScript Developer', 'Développeur JavaScript'), ('UI Developer', 'Développeur d’interfaces'), ('Web Developer', 'Développeur Web')]),
    (('Enterprise Applications', 'Applications d’entreprise'), [('Business Systems', 'Systèmes d’affaires'), ('Enterprise Apps', 'Applications d’entreprise'), ('Systems Integration', 'Intégration de systèmes')]),
    (('Microsoft Dynamics ERP', 'Microsoft Dynamics ERP'), [('ERP Manager', 'Gestionnaire ERP'), ('ERP Professional', 'Professionnel ERP')]),
    (('Application Support', 'Soutien aux applications'), [('Application Support Analyst', 'Analyste de soutien aux applications'), ('Systems Support', 'Soutien aux systèmes')]),
]


def roles_html():
    """Builds the rotating role titles of the hero (see ROLES). app.js handles the rotation."""
    out = []
    for i, ((t_en, t_fr), chips_) in enumerate(ROLES):
        cs = ''.join(f'<li>{el("span", en, fr)}</li>' for en, fr in chips_)
        out.append(f'<div class="role{" is-active" if i == 0 else ""}">{el("p", t_en, t_fr, "role__title")}<ul class="role__chips">{cs}</ul></div>')
    return '<div class="roles" id="roles"><div class="roles__stage">' + ''.join(out) + '</div><div class="roles__dots" id="roleDots"></div></div>'

# ------------------------------------------------------------------------------------------------
# Navigation tabs: (id of the section, English, French). 'top' is the Home tab and highlights the hero.
nav_items = [
    ('top', 'Home', 'Accueil'),
    ('about', 'About', 'À propos'),
    ('skills', 'Skills', 'Compétences'),
    ('experience', 'Experience', 'Expérience'),
    ('projects', 'Projects', 'Projets'),
    ('education', 'Education', 'Formation'),
    ('contact', 'Contact', 'Contact'),
]
nav_html = ''.join('<li>' + el('a', en, fr, 'nav__link', 'href="#%s"%s' % (id_, ' data-target="hero"' if id_ == 'top' else '')) + '</li>' for id_, en, fr in nav_items)

# Sticky header: brand, tabs, resume button, language switch, theme toggle, hamburger.
header = f'''
<div id="top"></div>
<header class="site-header">
  <div class="wrap site-header__bar">
    <a class="brand" href="#top" aria-label="Jhon Diaz"><span class="brand__mark" aria-hidden="true">JD</span><span class="brand__name">Jhon Diaz</span></a>
    <nav class="nav" id="siteNav" {ia(**{'aria-label': ('Main navigation', 'Navigation principale')})}>
      <ul class="nav__list">{nav_html}</ul>
    </nav>
    <div class="tools">
      <a class="btn btn--small btn--ghost tools__cv" href="assets/docs/Jhon_Diaz_CV_EN.pdf" data-cv target="_blank" rel="noopener" download="Jhon_Diaz_CV_EN.pdf">{icon('download')}{el('span', 'Resume', 'CV')}</a>
      <div class="lang" role="group" {ia(**{'aria-label': ('Language', 'Langue')})}>
        <button type="button" class="lang__btn" data-lang="en" aria-pressed="true" lang="en">EN</button>
        <button type="button" class="lang__btn" data-lang="fr" aria-pressed="false" lang="fr">FR</button>
        <button type="button" class="lang__btn" data-lang="es" aria-pressed="false" lang="es">ES</button>
      </div>
      <button type="button" class="iconbtn" id="themeToggle" aria-label="Switch to dark theme">{icon('moon', 'icon icon--moon')}{icon('sun', 'icon icon--sun')}</button>
      <button type="button" class="iconbtn nav__toggle" id="menuToggle" aria-expanded="false" aria-controls="siteNav" aria-label="Open menu">{icon('menu')}</button>
    </div>
  </div>
</header>'''

# endregion


# region 5. Hero and About
hero = f'''
<section class="hero" id="hero">
  <div class="wrap hero__grid">
    <div class="hero__top">
      <h1 class="hero__name">Jhon Deiber Diaz Parra</h1>
      <p class="status"><span class="status__dot" aria-hidden="true"></span>{el('span', 'Open to work', 'Disponible pour un emploi')}</p>
    </div>
    <div class="hero__copy">
      {roles_html()}
      {el('p', 'I build and maintain the .NET applications and APIs that keep business systems connected, reliable and fast.',
          'Je conçois et je maintiens les applications .NET et les API qui gardent les systèmes d’affaires connectés, fiables et rapides.', 'hero__lead')}
      {el('p', 'More than 3 years developing and supporting production systems, on top of 12 years running enterprise ERP operations. I work in French, English and Spanish.',
          'Plus de 3 ans à développer et à soutenir des systèmes en production, après 12 ans à diriger l’exploitation d’ERP d’entreprise. Je travaille en français, en anglais et en espagnol.', 'hero__proof')}
      <div class="hero__actions">
        <a class="btn btn--primary" href="assets/docs/Jhon_Diaz_CV_EN.pdf" data-cv target="_blank" rel="noopener" download="Jhon_Diaz_CV_EN.pdf">{icon('download')}{el('span', 'Download resume', 'Télécharger mon CV')}</a>
        <a class="btn btn--ghost" href="#contact">{icon('mail')}{el('span', 'Send a message', 'Écrire un message')}</a>
      </div>
    </div>
    <div class="hero__photo">
      <div class="arch" aria-hidden="true"><span class="arch__ring arch__ring--3"></span><span class="arch__ring arch__ring--2"></span><span class="arch__ring arch__ring--1"></span></div>
      <picture>
        <source srcset="assets/img/jhon.webp" type="image/webp">
        <img class="portrait" src="assets/img/jhon.jpg" width="800" height="1000" fetchpriority="high" {ia(alt=('Portrait of Jhon Deiber Diaz Parra', 'Portrait de Jhon Deiber Diaz Parra'))}>
      </picture>
      <p class="place"><span class="place__dot" aria-hidden="true"></span>Calgary, Alberta, CA</p>
    </div>
  </div>
  {RIDGE}
</section>'''

# About: four short paragraphs and the key-facts card.
about = f'''
<section class="section section--tint" id="about">
  <div class="wrap about">
    <div class="about__text">
      {el('h2', 'About me', 'À propos de moi')}
      {el('p', 'I’m a software developer with more than three years of professional experience building and maintaining C# / .NET Framework applications, REST APIs and SQL Server databases. My work has covered monitoring the applications and APIs that keep systems exchanging data, resolving production incidents, and developing new APIs, features and tools that business teams use every day.',
          'Je suis développeur logiciel avec plus de trois ans d’expérience professionnelle dans la conception et la maintenance d’applications C# / .NET Framework, d’API REST et de bases de données SQL Server. Mon travail a couvert la surveillance des applications et des API qui assurent l’échange de données entre les systèmes, la résolution d’incidents en production, et le développement de nouvelles API, fonctionnalités et outils que les équipes utilisent chaque jour.')}
      {el('p', 'Before moving into development full time, I spent twelve years in ERP applications (Microsoft Dynamics). I led the team that supported the ERP and other enterprise systems, managed the database, the budget and the licences, and approved new developments, projects and migrations.',
          'Avant de me consacrer au développement à temps plein, j’ai passé douze ans dans les applications ERP (Microsoft Dynamics). J’ai dirigé l’équipe qui soutenait l’ERP et d’autres systèmes d’entreprise, géré la base de données, le budget et les licences, et approuvé les nouveaux développements, projets et migrations.')}
      {el('p', 'In my ERP roles, I worked directly with area managers and end users. I listened to their needs, turned them into requirements, documented the solutions and supported the teams that depended on them. I bring the same approach to every project: understand the problem first, then build the solution that fits it.',
          'Dans mes rôles liés à l’ERP, j’ai travaillé directement avec les gestionnaires de secteur et les utilisateurs finaux. J’ai écouté leurs besoins, je les ai traduits en exigences, j’ai documenté les solutions et j’ai soutenu les équipes qui en dépendaient. J’applique la même approche à chaque projet : comprendre d’abord le problème, puis bâtir la solution qui lui convient.')}
      {el('p', 'I like to adopt new technologies early. I use AI assistants to speed up development and optimize code, and I always review, test and understand what I deliver.',
          'J’aime adopter tôt les nouvelles technologies. J’utilise des assistants d’IA pour accélérer le développement et optimiser le code, et je révise, je teste et je comprends toujours ce que je livre.')}
    </div>
    <dl class="facts">
      <div class="facts__row">{el('dt', 'Based in', 'Lieu')}{el('dd', 'Alberta, Canada', 'Alberta, Canada')}</div>
      <div class="facts__row">{el('dt', 'Looking for', 'Je recherche')}{el('dd', 'Software developer or application support roles', 'Des postes de développeur logiciel ou de soutien aux applications')}</div>
      <div class="facts__row">{el('dt', 'Main stack', 'Technologies')}{el('dd', '.NET, C#, REST APIs, SQL Server, Microsoft Graph', '.NET, C#, API REST, SQL Server, Microsoft Graph')}</div>
      <div class="facts__row">{el('dt', 'Spanish', 'Espagnol')}{el('dd', 'Native', 'Langue maternelle')}</div>
      <div class="facts__row">{el('dt', 'French', 'Français')}{el('dd', 'Professional working proficiency (B2+)', 'Autonomie professionnelle (B2+)')}</div>
      <div class="facts__row">{el('dt', 'English', 'Anglais')}{el('dd', 'Intermediate (B2), currently studying', 'Intermédiaire (B2), en cours d’études')}</div>
    </dl>
  </div>
</section>'''


# endregion


# region 6. Skills
def chips(items):
    """Wraps already rendered chips in the <ul> used by the skills rows."""
    return '<ul class="chips">' + ''.join(items) + '</ul>'


def chip(txt):
    """Chip with the same text in every language (technology names)."""
    return f'<li>{txt}</li>'


def chip_i(en, fr):
    """Chip whose text is translated."""
    return el('li', en, fr)


def skill_row(label_en, label_fr, content):
    """One row of the Skills section: translated label + chips."""
    return f'<div class="skills__row">{el("h3", label_en, label_fr, "skills__label")}{content}</div>'


# Skills: one row per area. Programming languages, Business software and Methodologies stay last.
skills = f'''
<section class="section" id="skills">
  <div class="wrap">
    {el('h2', 'Technical skills', 'Compétences techniques')}
    <div class="skills">
      {skill_row('Back-end and APIs', 'Back-end et API', chips([chip('C# / .NET Framework'), chip('ASP.NET Core MVC'), chip('RESTful APIs / Web API'), chip('Swagger (OpenAPI)'), chip('Hangfire'), chip('Microsoft Graph API'), chip('Node.js / Express.js')]))}
      {skill_row('Databases and BI', 'Bases de données et BI', chips([chip('SQL Server (T-SQL)'), chip_i('Stored procedures and tuning', 'Procédures stockées et optimisation'), chip('SSRS / SSIS / ETL'), chip('Power BI'), chip('PostgreSQL'), chip('MySQL / MariaDB')]))}
      {skill_row('Front-end', 'Front-end', chips([chip('HTML5'), chip('CSS3'), chip('JavaScript / TypeScript'), chip('React.js'), chip('Bootstrap'), chip('Tailwind CSS')]))}
      {skill_row('DevOps and tools', 'DevOps et outils', chips([chip('Git / GitHub / Bitbucket'), chip('Azure DevOps (TFS)'), chip_i('IIS deployment', 'Déploiement IIS'), chip('PowerShell'), chip('Office 365 / SharePoint')]))}
      {skill_row('AI-assisted development', 'Développement assisté par IA', chips([chip_i('AI coding assistants', 'Assistants de codage IA'), chip_i('Code optimization and refactoring', 'Optimisation et refactorisation du code'), chip_i('Faster development cycles', 'Cycles de développement plus rapides'), chip_i('Prompt engineering', 'Ingénierie des prompts')]))}
      {skill_row('Programming languages', 'Langages de programmation',
                 '<div class="langs">' +
                 '<div class="langs__line">' + el('span', 'In professional work', 'En milieu professionnel', 'langs__tag') + chips([chip('C#'), chip('T-SQL'), chip('JavaScript')]) + '</div>' +
                 '<div class="langs__line">' + el('span', 'From my studies and personal projects', 'Issus de ma formation et de mes projets personnels', 'langs__tag') + chips([chip('TypeScript'), chip('Python'), chip('Java'), chip('Go'), chip('C++'), chip('PHP'), chip('Kotlin'), chip('Flutter')]).replace('class="chips"', 'class="chips chips--quiet"') + '</div></div>')}
      {skill_row('Business software', 'Logiciels d’entreprise', chips([chip('Microsoft Dynamics ERP'), chip('WMS Arcante'), chip('PLM Porini'), chip('ICG POS'), chip('Shopify'), chip('ArchivesSpace'), chip('ResourceSpace'), chip('Gallery Systems')]))}
      {skill_row('Methodologies and support', 'Méthodologies et soutien', chips([chip('Agile / Scrum / Kanban'), chip_i('SDLC and OOP', 'Cycle de développement et POO'), chip_i('Technical documentation', 'Documentation technique'), chip_i('Tier 2 support', 'Soutien de niveau 2'), chip('Trello / Planner')]))}
    </div>
  </div>
</section>'''


# endregion


# region 7. Experience
def job(title_en, title_fr, org_en, org_fr, period_en, period_fr, bullets, open_=False, extra_cls='', dur=None, about=None, photo=None):
    """One experience card.

    bullets: list of (English, French) achievements.   dur: (English, French) length of the role.
    about: (English, French) one-paragraph company description.   photo: image path shown on the right.
    extra_cls: 'job--minor' for a smaller title.   open_ is unused and kept for compatibility.
    """
    lis = ''.join(li(en, fr) for en, fr in bullets)
    a = el('p', about[0], about[1], 'job__about') if about else ''
    d = el('span', dur[0], dur[1], 'job__dur') if dur else ''
    when = '<p class="job__when">' + el('span', period_en, period_fr, 'job__period') + ('<span class="job__sep" aria-hidden="true">·</span>' + d if d else '') + '</p>'
    ph = ('<div class="job__photo" aria-hidden="true" style="background-image:url(%s)"></div>' % photo) if photo else ''
    cls = 'job job--card' + (' job--photo' if photo else '') + (' ' + extra_cls if extra_cls else '')
    return f'''<article class="{cls}">
      <div class="job__head">
        <div class="job__headtext">
          {el('h3', title_en, title_fr, 'job__title')}
          {el('p', org_en, org_fr, 'job__org')}
          {when}
          {a}
        </div>
        {ph}
      </div>
      <ul class="job__list">{lis}</ul>
    </article>'''


# Experience, newest first. Photos live in assets/img/jobs/.
cca = job('Full Stack Developer', 'Développeur full stack',
          'Canadian Centre for Architecture (CCA), Montréal, QC', 'Centre Canadien d’Architecture (CCA), Montréal (QC)',
          'Apr 2023 – Jun 2026', 'avr. 2023 – juin 2026', dur=('3 years 3 months', '3 ans 3 mois'),
          photo='assets/img/jobs/cca.jpg', about=('International centre for research and exhibitions on architecture and urbanism, housed in a historic mansion with a sculpture garden. Its systems connect collections, publishing, retail and administration.', 'Centre international de recherche et d’expositions sur l’architecture et l’urbanisme, installé dans une demeure historique dotée d’un jardin de sculptures. Ses systèmes relient les collections, l’édition, la boutique et l’administration.'), bullets=[
    ('Monitored the enterprise applications and APIs that ensure reliable communication and data transfer between systems, detecting and fixing failures before they affected users.',
     'Surveillance des applications et des API d’entreprise qui assurent une communication et un transfert de données fiables entre les systèmes, avec détection et correction des défaillances avant qu’elles touchent les utilisateurs.'),
    ('Diagnosed and resolved production incidents (Tier 2) through the ticketing system.',
     'Diagnostic et résolution d’incidents en production (niveau 2) au moyen du système de billetterie.'),
    ('Designed, developed and deployed new RESTful APIs in C# (.NET Framework / ASP.NET Core) to integrate enterprise systems.',
     'Conception, développement et déploiement de nouvelles API RESTful en C# (.NET Framework / ASP.NET Core) pour intégrer les systèmes d’entreprise.'),
    ('Developed new features and applications and improved existing systems, working with users in French and English.',
     'Développement de nouvelles fonctionnalités et applications et amélioration des systèmes existants, en collaboration avec des utilisateurs en français et en anglais.'),
    ('Built an ASP.NET Core MVC application that creates, edits and deletes SharePoint intranet sites through the Microsoft Graph API.',
     'Création d’une application ASP.NET Core MVC qui crée, modifie et supprime des sites intranet SharePoint grâce à l’API Microsoft Graph.'),
    ('Wrote and optimized T-SQL stored procedures and queries; documented APIs with Swagger and automated scheduled jobs with Hangfire.',
     'Écriture et optimisation de procédures stockées et de requêtes T-SQL; documentation des API avec Swagger et automatisation des tâches planifiées avec Hangfire.'),
    ('Worked with the organization’s business platforms, including Shopify, ArchivesSpace, ResourceSpace, Gallery Systems and Power BI.',
     'Travail avec les plateformes d’affaires de l’organisation, dont Shopify, ArchivesSpace, ResourceSpace, Gallery Systems et Power BI.'),
    ('Deployed and administered applications on IIS, maintained SSRS reports and managed source control in Azure DevOps (TFS).',
     'Déploiement et administration d’applications sur IIS, maintenance de rapports SSRS et gestion du contrôle de version dans Azure DevOps (TFS).'),
])

landscaper = job('Landscaper', 'Préposé à l’entretien paysager',
                 'Boardwalk, Montréal, QC', 'Boardwalk, Montréal (QC)',
                 'Jul 2021 – Mar 2023', 'juil. 2021 – mars 2023', dur=('1 year 9 months', '1 an 9 mois'),
                 photo='assets/img/jobs/boardwalk.jpg', about=('Residential rental property management company with communities in several Canadian provinces and a major national presence.', 'Entreprise de gestion d’immeubles résidentiels locatifs, présente dans plusieurs provinces canadiennes et bien établie à l’échelle nationale.'), bullets=[
    ('Painted common areas of assigned buildings and maintained lawns and green spaces.',
     'Peinture des aires communes des immeubles assignés et entretien des pelouses et des espaces verts.'),
    ('Supported the maintenance and concierge teams when needed, while completing programming studies.',
     'Soutien aux équipes d’entretien et de conciergerie au besoin, tout en terminant mes études en programmation.'),
], extra_cls='job--minor')

permoda_mgr = job('Applications and Database Manager, ERP', 'Gestionnaire des applications et des bases de données (ERP)',
                  'Permoda Ltda., Bogotá, Colombia', 'Permoda Ltda., Bogotá (Colombie)',
                  'Dec 2017 – Oct 2020', 'déc. 2017 – oct. 2020', dur=('2 years 11 months', '2 ans 11 mois'),
                  photo='assets/img/jobs/permoda.jpg', about=('Colombian company dedicated to the design, manufacturing and distribution of clothing and textile products. Founded in 1983, it operates in the formal, casual and youth fashion segments through its own stores in Colombia’s main cities, with brands such as Armi, Pronto and B.kul, and has expanded to Costa Rica and Ecuador. Its operations ran on the ERP I supported.', 'Entreprise colombienne dédiée à la conception, à la fabrication et à la distribution de vêtements et de produits textiles. Fondée en 1983, elle exerce dans les segments de la mode formelle, décontractée et jeune par l’intermédiaire de ses propres magasins dans les principales villes de Colombie, avec des marques comme Armi, Pronto et B.kul, et s’est étendue au Costa Rica et en Équateur. Ses activités reposaient sur l’ERP que je soutenais.'), bullets=[
    ('Led the technical team responsible for the daily operation and support of the Microsoft Dynamics ERP and other enterprise applications, ensuring service continuity for end users.',
     'Direction de l’équipe technique responsable de l’exploitation quotidienne et du soutien de l’ERP Microsoft Dynamics et d’autres applications d’entreprise, afin d’assurer la continuité du service pour les utilisateurs.'),
    ('Planned and managed the annual ERP improvement budget and software licensing.',
     'Planification et gestion du budget annuel d’amélioration de l’ERP et des licences logicielles.'),
    ('Reviewed and approved new developments, projects and migrations, coordinating requirements and schedules with area managers and third-party providers.',
     'Examen et approbation des nouveaux développements, projets et migrations, avec coordination des exigences et des échéanciers auprès des gestionnaires de secteur et des fournisseurs tiers.'),
    ('Ensured availability, performance and security of the ERP database: optimization, indexing, statistics, locks and backups.',
     'Garantie de la disponibilité, de la performance et de la sécurité de la base de données de l’ERP : optimisation, index, statistiques, verrous et sauvegardes.'),
    ('Led ERP project execution and tracking using Agile methodologies.',
     'Direction de l’exécution et du suivi des projets ERP selon les méthodes agiles.'),
    ('Supported the team debugging Dynamics ERP code (AOT) and wrote SQL queries for incident analysis and resolution.',
     'Soutien de l’équipe dans le débogage du code de Dynamics ERP (AOT) et écriture de requêtes SQL pour l’analyse et la résolution d’incidents.'),
    ('Coordinated virtual training material for application users.',
     'Coordination du matériel de formation virtuelle destiné aux utilisateurs des applications.'),
])

# Permoda roles before 2017 are collapsed in a <details> block.
earlier = f'''<details class="earlier">
      <summary>{el('span', 'Earlier roles at Permoda, 2003 to 2017', 'Postes antérieurs chez Permoda, de 2003 à 2017')}</summary>
      {job('Applications Professional, ERP', 'Spécialiste des applications ERP', 'Permoda Ltda., Bogotá, Colombia', 'Permoda Ltda., Bogotá (Colombie)', 'Aug 2008 – Nov 2017', 'août 2008 – nov. 2017', dur=('9 years 4 months', '9 ans 4 mois'), bullets=[
          ('Implemented and deployed the ERP’s standard modules and local functionalities; enhanced and maintained ERP features and executed new projects.', 'Implantation et déploiement des modules standards de l’ERP et des fonctionnalités locales; amélioration et maintenance des fonctions de l’ERP et exécution de nouveaux projets.'),
          ('Ran tests for approval and release of developments to production.', 'Exécution des tests d’approbation et de mise en production des développements.'),
          ('Led application planning focused on key-user training and developed virtual training materials.', 'Direction de la planification des applications axée sur la formation des utilisateurs clés et conception de matériel de formation virtuelle.'),
          ('Optimized ERP processes and procedures; escalated complex issues to Level III specialists.', 'Optimisation des processus et procédures de l’ERP; escalade des problèmes complexes aux spécialistes de niveau III.')])}
      {job('Production Planning Analyst', 'Analyste de planification de la production', 'Permoda Ltda., Bogotá, Colombia', 'Permoda Ltda., Bogotá (Colombie)', '2006 – 2008', '2006 – 2008', dur=('about 2 years', 'environ 2 ans'), bullets=[
          ('Implemented Material Requirements Planning (MRP) for product production.', 'Mise en œuvre de la planification des besoins en matières (MRP) pour la production.'),
          ('Designed technical sheets and calculated manufacturing routes and bill-of-materials cost for garments.', 'Conception de fiches techniques et calcul des gammes de fabrication et du coût des nomenclatures pour les vêtements.'),
          ('Applied industrial engineering methods to improve the manufacturing process and reduce operating costs; optimized raw-material inventories.', 'Application de méthodes de génie industriel pour améliorer le procédé de fabrication et réduire les coûts d’exploitation; optimisation des stocks de matières premières.')])}
      {job('Production Engineering Analyst', 'Analyste en génie de production', 'Permoda Ltda., Bogotá, Colombia', 'Permoda Ltda., Bogotá (Colombie)', 'Nov 2003 – Dec 2006', 'nov. 2003 – déc. 2006', dur=('3 years 2 months', '3 ans 2 mois'), bullets=[
          ('Designed and improved workload balancing for production plants.', 'Conception et amélioration de l’équilibrage de la charge de travail dans les usines de production.'),
          ('Defined engineering methods and standard times for workstations and garment operations.', 'Définition des méthodes d’ingénierie et des temps standards pour les postes de travail et les opérations de confection.'),
          ('Prepared efficiency reports, controlled unproductive time and identified bottlenecks in production modules.', 'Préparation de rapports d’efficacité, contrôle du temps improductif et repérage des goulots d’étranglement dans les modules de production.')])}
    </details>'''

experience = f'''
<section class="section section--tint" id="experience">
  <div class="wrap">
    {el('h2', 'Experience', 'Expérience')}
    <div class="timeline">
      {cca}
      {landscaper}
      {permoda_mgr}
      {earlier}
    </div>
  </div>
</section>'''


# endregion


# region 8. Projects
def project(idx, title_en, title_fr, short_en, short_fr, long_en, long_fr, tech, img, media, mtype, code='', yt='', alt_en='', alt_fr='', featured=False, poster=''):
    """One project card. The long text, media and links travel in data-* attributes that app.js reads when the dialog opens.

    mtype: 'video' or 'image'.  yt: YouTube id (wins over the local file).  featured: wide card.
    """
    k_long = key(long_en, long_fr)
    k_title = key(title_en, title_fr)
    tech_html = ''.join(f'<li>{t}</li>' for t in tech)
    cta_en, cta_fr = ('Watch the demo', 'Voir la démo') if mtype == 'video' else ('See details', 'Voir les détails')
    cls = 'project project--featured' if featured else 'project'
    data = (f'data-title-key="{k_title}" data-title="{html.escape(title_en, quote=True)}" '
            f'data-desc-key="{k_long}" data-desc="{html.escape(long_en, quote=True)}" '
            f'data-media="{media}" data-type="{mtype}" data-poster="{poster or img}" data-code="{code}" data-youtube="{yt}"')
    return f'''<article class="{cls}">
      <button type="button" class="project__open" {data}>
        <span class="project__img"><img src="{img}" width="650" height="350" loading="lazy" {ia(alt=(alt_en, alt_fr))}>
          <span class="project__play" aria-hidden="true">{icon('play') if mtype == 'video' else icon('external')}</span></span>
        <span class="project__text">
          <span class="project__title" data-i18n="{k_title}">{title_en}</span>
          {el('span', short_en, short_fr, 'project__short')}
          <ul class="project__tech">{tech_html}</ul>
          {el('span', cta_en, cta_fr, 'project__cta')}
        </span>
      </button>
    </article>'''


# Projects: the video of each one is assets/media/project-N.mp4 unless a YouTube id is given.
projects = f'''
<section class="section" id="projects">
  <div class="wrap">
    {el('h2', 'Projects', 'Projets')}
    <div class="projects">
      {project(1, 'Intranet Site - SharePoint', 'Site intranet - SharePoint',
               'Turns PDF documents (procedures, policies, announcements) into SharePoint intranet pages, automatically.',
               'Transforme automatiquement des documents PDF (procédures, politiques, avis) en pages intranet SharePoint.',
               'Application for an intranet hosted on SharePoint. It creates SharePoint Site Pages (.aspx) from PDF documents such as procedures, policies and published information. If the PDF has a table of contents, the application captures it and builds the page content from it, with a link to each page. Every page is an image the process generates from the corresponding page of the PDF. Each department has its own documents, so the PDF can be imported into SharePoint together with its pages. Built with ASP.NET Core MVC and the Microsoft Graph API, which also handles editing and deleting the sites. This is professional work, so the source code is not public; the diagram shows the flow.',
               'Application pour un intranet hébergé sur SharePoint. Elle crée des pages de site SharePoint (.aspx) à partir de documents PDF tels que des procédures, des politiques et de l’information à publier. Si le PDF contient une table des matières, l’application la capture et construit le contenu de la page à partir de celle-ci, avec un lien vers chaque page. Chaque page est une image que le processus génère à partir de la page correspondante du PDF. Chaque service a ses propres documents : le PDF peut donc être importé dans SharePoint avec ses pages. Réalisée avec ASP.NET Core MVC et l’API Microsoft Graph, qui gère aussi la modification et la suppression des sites. Il s’agit d’un travail professionnel : le code source n’est pas public, et le schéma illustre le fonctionnement.',
               ['C#', 'ASP.NET Core MVC', 'Microsoft Graph API', 'SharePoint'], 'assets/img/thumb-5.jpg', 'assets/img/thumb-5.jpg', 'image',
               alt_en='Diagram: a PDF file goes through an ASP.NET Core application and becomes SharePoint intranet pages',
               alt_fr='Schéma : un fichier PDF passe par une application ASP.NET Core et devient des pages intranet SharePoint', featured=True)}
      {project(5, 'Time Control Manufacture (TCM)', 'Time Control Manufacture (TCM)',
               'Real-time production control for manufacturing plants: interfaces with the ERP, captures and processes plant data, and delivers it to BI.',
               'Contrôle de la production en temps réel pour les usines : interface avec l’ERP, saisie et traitement des données d’usine, et livraison à la BI.',
               'Real-time production control system for manufacturing plants. It interfaces with the ERP production module and, through SQL Server, imports production orders, resources and manufacturing routes. Production users and coordinators follow plant execution as it happens, the application captures and processes that data, and it delivers it to the database for transformation and to BI for management reporting. It also manages plant calendars and shift schedules, with roles and permissions for each user.',
               'Système de contrôle de la production en temps réel pour les usines de fabrication. Il s’interface avec le module de production de l’ERP et importe, au moyen de SQL Server, les ordres de production, les ressources et les gammes de fabrication. Les utilisateurs et les coordonnateurs de production suivent l’exécution des usines au fur et à mesure, l’application saisit et traite ces données, puis les livre à la base de données pour la transformation et à la BI pour les rapports de gestion. Elle gère aussi les calendriers et les horaires de quarts des usines, avec des rôles et des permissions pour chaque utilisateur.',
               ['SQL Server', 'Microsoft Dynamics ERP', 'BI reporting'], 'assets/img/thumb-tcm.jpg', 'assets/media/project-5.mp4', 'video',
               alt_en='Time Control Manufacture production control dashboard', alt_fr='Tableau de bord de Time Control Manufacture, contrôle de la production', featured=True)}
      {project(2, 'Favorite Music Albums Manager', 'Gestionnaire d’albums de musique favoris',
               'Search, add and delete favorite albums. REST back-end in Node.js and PostgreSQL, React front-end, Discogs API.',
               'Recherche, ajout et suppression d’albums favoris. Back-end REST en Node.js et PostgreSQL, front-end React, API Discogs.',
               'Web application to manage a list of favorite music albums: search, add and delete. The back-end is a Node.js + Express server exposing REST APIs that manage a PostgreSQL database; the React.js front-end consumes those APIs and the Discogs music API. My role in this team project (two developers) was the back-end.',
               'Application web pour gérer une liste d’albums de musique favoris : recherche, ajout et suppression. Le back-end est un serveur Node.js + Express qui expose des API REST gérant une base de données PostgreSQL; le front-end React.js consomme ces API ainsi que l’API musicale Discogs. Dans ce projet d’équipe (deux développeurs), j’étais responsable du back-end.',
               ['Node.js', 'Express', 'React', 'PostgreSQL'], 'assets/img/thumb-2.jpg', 'assets/media/project-2.mp4', 'video',
               code='https://github.com/jhondeiberd/SoftStructure/tree/jhondeiberd/Final-project', yt='',
               alt_en='Favorite Music Albums Manager', alt_fr='Gestionnaire d’albums de musique favoris')}
      {project(6, 'Phrase Audio', 'Phrase Audio',
               'Web app that turns a bilingual phrase list (PDF) into a custom MP3 for language study, with natural voices and configurable repetitions.',
               'Application web qui transforme une liste de phrases bilingue (PDF) en MP3 personnalisé pour l’étude des langues, avec des voix naturelles et des répétitions configurables.',
               'Web app that reads a bilingual phrase list from a PDF, detects the highlighted phrases and generates a study MP3. You choose how many times each language repeats, the pauses and the voices. A Vercel serverless function turns each phrase into speech with Microsoft neural voices, and the browser assembles and encodes the final MP3. Interface in English and Spanish, with light and dark themes.',
               'Application web qui lit une liste de phrases bilingue dans un PDF, détecte les phrases surlignées et génère un MP3 d’étude. Vous choisissez combien de fois chaque langue se répète, les pauses et les voix. Une fonction serverless Vercel transforme chaque phrase en parole avec les voix neuronales de Microsoft, et le navigateur assemble et encode le MP3 final. Interface en anglais et en espagnol, avec thèmes clair et sombre.',
               ['JavaScript', 'Vercel'], 'assets/img/thumb-pa.jpg', 'assets/media/project-6.mp4', 'video',
               alt_en='Phrase Audio web app', alt_fr='Application web Phrase Audio')}
      {project(3, 'Personal Budget for Android', 'Budget personnel pour Android',
               'Track income, expenses and balance on your phone. Add, edit and delete transactions. Multilingual.',
               'Suivi des revenus, des dépenses et du solde sur le téléphone. Ajout, modification et suppression de transactions. Multilingue.',
               'Android application written in Kotlin to manage income, expenses and personal balance. It supports adding, editing and deleting transactions and is multilingual.',
               'Application Android écrite en Kotlin pour gérer les revenus, les dépenses et le solde personnel. Elle permet d’ajouter, de modifier et de supprimer des transactions et elle est multilingue.',
               ['Kotlin', 'Android'], 'assets/img/thumb-1.jpg', 'assets/media/project-1.mp4', 'video',
               code='https://github.com/jhondeiberd/Android/tree/jhondeiberd/FinalProject', yt='',
               alt_en='Personal Budget Android app', alt_fr='Application Android de budget personnel')}
    </div>
  </div>
</dialog_placeholder>
</section>'''.replace('</dialog_placeholder>\n', '')


# endregion


# region 9. Education
def edu(logo, title_en, title_fr, org_en, org_fr, when_en, when_fr, links='', icon_name=None, href=''):
    """One education item. logo: file in assets/img (or None to use an icon); href makes the logo a link."""
    if logo:
        tile = f'<a class="edu__logo" href="{href}" target="_blank" rel="noopener"><img src="assets/img/{logo}" width="100" height="100" loading="lazy" alt=""></a>' if href else f'<span class="edu__logo"><img src="assets/img/{logo}" width="100" height="100" loading="lazy" alt=""></span>'
    elif href:
        tile = f'<a class="edu__logo edu__logo--icon" href="{href}" target="_blank" rel="noopener" aria-hidden="true" tabindex="-1">{icon(icon_name)}</a>'
    else:
        tile = f'<span class="edu__logo edu__logo--icon">{icon(icon_name)}</span>'
    return f'''<li class="edu__item">{tile}<div>
        {el('p', title_en, title_fr, 'edu__title')}
        {el('p', org_en, org_fr, 'edu__org')}
        <div class="edu__meta">{el('p', when_en, when_fr, 'edu__when')}{links}</div></div></li>'''


def pdf_link(pdf):
    """'Certificate (PDF)' link shown on the same row as the course date."""
    return f'<a class="edu__link" href="{pdf}" target="_blank" rel="noopener">{el("span", "Certificate (PDF)", "Certificat (PDF)")}</a>'


def verify_links(cred, pdf):
    """Link to an online credential check plus the PDF (kept for future use; currently no course uses it)."""
    return (f'<a class="edu__link" href="{cred}" target="_blank" rel="noopener">{el("span", "Verify credential", "Vérifier l’attestation")}</a>'
            f'<a class="edu__link" href="{pdf}" target="_blank" rel="noopener">{el("span", "Certificate (PDF)", "Certificat (PDF)")}</a>')


# Education: studies on the left, courses and certificates on the right.
education = f'''
<section class="section section--tint" id="education">
  <div class="wrap">
    {el('h2', 'Education and training', 'Formation')}
    <div class="edu">
      <div>
        {el('h3', 'Studies', 'Études', 'edu__head')}
        <ul class="edu__list">
          {edu('universel.png', 'Programming and Web Technologies', 'Programmation et technologies Web', 'Attestation of College Studies, Collège Universel, Montréal', 'Attestation d’études collégiales, Collège Universel, Montréal', 'Feb 2021 – Jan 2023', 'févr. 2021 – janv. 2023', href='https://collegeuniversel.ca/en/page-daccueil-en/')}
          {edu('distrital.png', 'Production Engineering, bachelor’s degree', 'Génie de production, baccalauréat', 'Universidad Distrital Francisco José de Caldas, Bogotá', 'Universidad Distrital Francisco José de Caldas, Bogotá', '2008 – 2013', '2008 – 2013', href='https://www.udistrital.edu.co/inicio')}
          {edu('smart.png', 'English language studies, level B2', 'Études d’anglais, niveau B2', 'Academia Smart Colombia (online)', 'Academia Smart Colombia (en ligne)', 'Jul 2026 – present', 'juil. 2026 – présent', href='https://smart.edu.co/')}
          {edu('yves.png', 'Francisation, level 8', 'Francisation, niveau 8', 'Centre Yves-Thériault, Montréal', 'Centre Yves-Thériault, Montréal', 'Jan 2023 – Jul 2025', 'janv. 2023 – juil. 2025', href='https://centre-yves-theriault.cssdm.gouv.qc.ca/')}
          {edu('csai.jpg', 'Francisation, level 3', 'Francisation, niveau 3', 'Centre Social d’aide aux Immigrants (CSAI), Montréal', 'Centre Social d’aide aux Immigrants (CSAI), Montréal', 'Started Oct 2022', 'Débuté en oct. 2022', href='https://centrecsai.org/')}
          {edu('cidca.jpg', 'Industrial Technology, vocational diploma', 'Technologie industrielle, diplôme d’études professionnelles', 'Fundación Cidca, Bogotá', 'Fundación Cidca, Bogotá', '2002 – 2005', '2002 – 2005', href='https://www.linkedin.com/in/fundacion-cidca-34b52a25/')}
        </ul>
      </div>
      <div>
        {el('h3', 'Courses and certificates', 'Cours et certificats', 'edu__head')}
        <ul class="edu__list">
          {edu('lourtec.jpg', 'Developing C# and ASP.NET Core MVC web applications', 'Développement d’applications Web C# et ASP.NET Core MVC', 'Lourtec certificate of excellence, 120 hours (Microsoft MCSA preparation program, online)', 'Certificat d’excellence Lourtec, 120 heures (programme de préparation Microsoft MCSA, en ligne)', 'Sep 2019', 'sept. 2019', links=pdf_link('assets/docs/lourtec-web-applications-certificate.pdf'), href='https://www.lourtec.com/cursos/microsoft/desarrollo-de-software')}
          {edu('lourtec.jpg', 'SQL 2016 Database Development', 'Développement de bases de données SQL 2016', 'Lourtec certificate of excellence, 120 hours (Microsoft MCSA preparation program, online)', 'Certificat d’excellence Lourtec, 120 heures (programme de préparation Microsoft MCSA, en ligne)', 'Jun 2020', 'juin 2020', links=pdf_link('assets/docs/lourtec-sql2016-certificate.pdf'), href='https://lourtec.com/cursos/microsoft/base-de-datos/20762-desarrollando-bases-de-datos-sql')}
          {edu('lourtec.jpg', 'Analyzing and Visualizing Data with Microsoft Power BI', 'Analyse et visualisation de données avec Microsoft Power BI', 'Microsoft MCSA preparation course, Lourtec (online)', 'Cours de préparation Microsoft MCSA, Lourtec (en ligne)', '2020', '2020', href='https://www.lourtec.com/')}
          {edu('slim.jpg', 'Object-Oriented Programming paradigm', 'Paradigme de la programmation orientée objet', 'Fundación Carlos Slim (online), certificate of completion', 'Fundación Carlos Slim (en ligne), certificat de réussite', 'Mar 2021 – May 2021', 'mars 2021 – mai 2021', links=pdf_link('assets/docs/oop-certificate.pdf'), href='https://capacitateparaelempleo.org/pages.php?r=.tema&amp;tagID=15840')}
          {edu('slim.jpg', 'Database Administrator (DBA)', 'Administrateur de bases de données (DBA)', 'Fundación Carlos Slim (online), certificate of completion', 'Fundación Carlos Slim (en ligne), certificat de réussite', 'Dec 2017 – Feb 2018', 'déc. 2017 – févr. 2018', links=pdf_link('assets/docs/dba-certificate.pdf'), href='https://capacitateparaelempleo.org/pages.php?r=.tema&amp;tagID=4066')}
        </ul>
      </div>
    </div>
  </div>
</section>'''

# endregion


# region 10. Contact and footer
contact = f'''
<section class="section" id="contact">
  <div class="wrap contact">
    <div class="contact__info">
      {el('h2', 'Let’s talk', 'Parlons-en')}
      {el('p', 'I’m looking for a software developer or application support role. Send me a message or write to me directly.',
          'Je cherche un poste de développeur logiciel ou de soutien aux applications. Écrivez-moi un message ou contactez-moi directement.', 'contact__lead')}
      <ul class="contact__list">
        <li>{icon('mail')}<a href="mailto:jhondeiberd@gmail.com">jhondeiberd@gmail.com</a></li>
        <li>{icon('phone')}<a href="tel:+15143461672">+1 514 346 1672</a></li>
        <li>{icon('pin')}{el('span', 'Alberta, Canada', 'Alberta, Canada')}</li>
        <li>{icon('linkedin')}<a href="https://www.linkedin.com/in/jhondeiberd/" target="_blank" rel="noopener">LinkedIn</a></li>
        <li>{icon('github')}<a href="https://github.com/jhondeiberd" target="_blank" rel="noopener">GitHub</a></li>
      </ul>
    </div>
    <form class="form" id="contactForm" novalidate>
      <div class="field">
        {el('label', 'Full name', 'Nom complet', '', 'for="name"')}
        <input id="name" name="name" type="text" autocomplete="name" required minlength="2" maxlength="120">
        {el('p', 'Enter your name.', 'Entrez votre nom.', 'field__error')}
      </div>
      <div class="field">
        {el('label', 'Email address', 'Adresse courriel', '', 'for="email"')}
        <input id="email" name="email" type="email" autocomplete="email" required maxlength="200">
        {el('p', 'Enter a valid email address.', 'Entrez une adresse courriel valide.', 'field__error')}
      </div>
      <div class="field">
        {el('label', 'Phone (optional)', 'Téléphone (facultatif)', '', 'for="phone"')}
        <input id="phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" maxlength="40" placeholder="+1 514 346 1672">
      </div>
      <div class="field">
        {el('label', 'Message', 'Message', '', 'for="message"')}
        <textarea id="message" name="message" rows="6" required minlength="10" maxlength="4000"></textarea>
        {el('p', 'Write at least 10 characters.', 'Écrivez au moins 10 caractères.', 'field__error')}
      </div>
      <div class="hp" aria-hidden="true"><label for="website">Leave this field empty</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
      <div class="form__status" id="formStatus" role="status" aria-live="polite"></div>
      <button class="btn btn--primary" id="submitButton" type="submit">{el('span', 'Send message', 'Envoyer le message')}</button>
    </form>
  </div>
</section>'''

# Footer: version label (update it on every release), visit counter, back-to-top link, project dialog.
footer = f'''
<footer class="site-footer">
  <div class="wrap site-footer__bar">
    <p>&copy; <span id="year">2026</span> Jhon Deiber Diaz Parra</p>
    <p class="version">{el('span', 'Portfolio version 1.2.1, October 2026', 'Portfolio version 1.2.1, octobre 2026')}</p>
    <p class="visits" id="visitCounter" hidden>{icon('eye')}<span id="visitCount">0</span> <span id="visitLabel">visits</span></p>
    <a class="totop" href="#top">{el('span', 'Back to top', 'Haut de la page')}</a>
  </div>
</footer>

<dialog class="modal" id="projectDialog" aria-labelledby="projectTitle">
  <div class="modal__box">
    <div class="modal__head">
      <h3 id="projectTitle"></h3>
      <button type="button" class="iconbtn" id="projectClose" aria-label="Close">{icon('x')}</button>
    </div>
    <div class="modal__media" id="projectMedia"></div>
    <p class="modal__desc" id="projectDesc"></p>
    <div class="modal__links" id="projectLinks"></div>
  </div>
</dialog>'''

# endregion


# region 11. Page assembly
page = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-i18n="{title_key}">{REG[title_key][0]}</title>
<meta name="description" {head_meta_desc}>
<meta name="author" content="Jhon Deiber Diaz Parra">
<meta name="color-scheme" content="light dark">
<meta property="og:type" content="website">
<meta property="og:title" content="Jhon Diaz | Software developer">
<meta property="og:description" content="C# / ASP.NET Core, REST APIs, SQL Server, Microsoft Graph. Alberta, Canada.">
<meta property="og:image" content="assets/img/og.jpg">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Person","name":"Jhon Deiber Diaz Parra","jobTitle":"Software Developer","email":"mailto:jhondeiberd@gmail.com","address":{{"@type":"PostalAddress","addressRegion":"AB","addressCountry":"CA"}},"knowsLanguage":["en","fr","es"],"sameAs":["https://www.linkedin.com/in/jhondeiberd/","https://github.com/jhondeiberd"]}}</script>
<link rel="icon" href="assets/favicon.ico">
<link rel="preload" href="assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/instrument.woff2" as="font" type="font/woff2" crossorigin>
<script>
(function () {{
  var d = document.documentElement;
  try {{
    var t = localStorage.getItem('theme');
    if (t !== 'dark' && t !== 'light') t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    d.setAttribute('data-theme', t);
    var q = new URLSearchParams(location.search).get('lang');
    var nl = (navigator.language || 'en').slice(0, 2);
    var l = q || localStorage.getItem('lang') || (nl === 'fr' || nl === 'es' ? nl : 'en');
    d.setAttribute('lang', l === 'fr' || l === 'es' ? l : 'en');
  }} catch (e) {{}}
}})();
</script>
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#about" {ia(**{'data-x': ('Skip to content', 'Aller au contenu')})}>Skip to content</a>
<!-- #region SVG icon sprite -->
{SPRITE}
<!-- #endregion -->
<!-- #region Header -->
{header}
<!-- #endregion -->
<main>
<!-- #region Hero -->
{hero}
<!-- #endregion -->
<!-- #region About -->
{about}
<!-- #endregion -->
<!-- #region Skills -->
{skills}
<!-- #endregion -->
<!-- #region Experience -->
{experience}
<!-- #endregion -->
<!-- #region Projects -->
{projects}
<!-- #endregion -->
<!-- #region Education -->
{education}
<!-- #endregion -->
<!-- #region Contact -->
{contact}
<!-- #endregion -->
</main>
<!-- #region Footer and project dialog -->
{footer}
<!-- #endregion -->
<script src="js/i18n-fr.js"></script>
<script src="js/i18n-es.js"></script>
<script src="js/i18n-ui.js"></script>
<script src="js/app.js"></script>
</body>
</html>
'''
# the skip link text must itself be translatable
page = page.replace('<a class="skip" href="#about" data-x="Skip to content" data-i18n-attr="data-x:' + [k for k, v in REG.items() if v[0] == 'Skip to content'][0] + '">Skip to content</a>',
                    '<a class="skip" href="#about" data-i18n="' + [k for k, v in REG.items() if v[0] == 'Skip to content'][0] + '">Skip to content</a>')

# endregion


# region 12. Output and validation
open(OUT + 'index.html', 'w', encoding='utf-8').write(page)

try:
    from es_dict import ES  # Spanish dictionary, see tools/es_dict.py
except Exception:
    ES = {}
uniq = []
for en, fr in list(REG.values()) + list(JS.values()):
    if en not in uniq:
        uniq.append(en)
if os.environ.get('DUMP'):
    for n, u in enumerate(uniq):
        print(n, '|', u)
    sys.exit(0)
missing = [u for u in uniq if u not in ES]
if missing:
    print('MISSING ES:', len(missing)); [print('  -', m[:80]) for m in missing[:10]]
    sys.exit(1)

def block(name, d, comment):
    lines = ['  %s: %s,' % (json.dumps(k), json.dumps(v, ensure_ascii=False)) for k, v in d.items()]
    return '// %s\n// Generated by tools/build.py. Do not edit by hand.\nwindow.%s = {\n%s\n};\n' % (comment, name, '\n'.join(lines))

fr_d = {k: fr for k, (en, fr) in REG.items()}
es_d = {k: ES[en] for k, (en, fr) in REG.items()}
ui_d = {}
for k, (en, fr) in JS.items():
    ui_d[k] = [en, fr, ES[en]]
open(OUT + 'js/i18n-fr.js', 'w', encoding='utf-8').write(block('I18N_FR', fr_d, 'French translations. Keys match the data-i18n attributes in index.html (the English text lives in the HTML).'))
open(OUT + 'js/i18n-es.js', 'w', encoding='utf-8').write(block('I18N_ES', es_d, 'Spanish translations. Keys match the data-i18n attributes in index.html.'))
ui_lines = ['  %s: %s,' % (json.dumps(k), json.dumps(v, ensure_ascii=False)) for k, v in ui_d.items()]
open(OUT + 'js/i18n-ui.js', 'w', encoding='utf-8').write('// Strings used by app.js: [English, French, Spanish].\n// Generated by tools/build.py. Do not edit by hand.\nwindow.I18N_JS = {\n' + '\n'.join(ui_lines) + '\n};\n')
print('keys:', len(REG), 'html bytes:', len(page))

# Format the generated files with Prettier (installed by `npm install`). Skipped when it is not available.
# On Windows npm installs a prettier.cmd launcher; the extension-less file is a shell script that cannot be run directly.
prettier = os.path.join(ROOT, 'node_modules', '.bin', 'prettier.cmd' if os.name == 'nt' else 'prettier')
if os.environ.get('SKIP_FORMAT'):
    print('SKIP_FORMAT set: generated files left unformatted.')
elif os.path.exists(prettier):
    try:
        subprocess.run([prettier, '--log-level', 'warn', '--write', 'index.html', 'js/i18n-fr.js', 'js/i18n-es.js', 'js/i18n-ui.js'], cwd=ROOT, check=False)
    except OSError as err:  # formatting is optional: never fail the build because of it
        print('Prettier could not run (' + str(err) + '); generated files left unformatted.')
else:
    print('Prettier not found: run `npm install` once to format the generated files.')

# endregion
