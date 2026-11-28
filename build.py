#!/usr/bin/env python3
"""Builds the padel site. `python3 build.py` = live (clean URLs). `python3 build.py --preview` = local files."""
import json, html, pathlib, sys, hashlib
import pathlib as _pl, sys as _sy
_sy.path.insert(0, str(_pl.Path(__file__).resolve().parent / "tools"))
from og import og_image

ROOT = pathlib.Path(__file__).resolve().parent
DOMAIN = "https://padelglassbox.com"
SITE = "Padel Glass Box"
ADSENSE_CLIENT = "ca-pub-1558743317014653"
GA_ID = "G-J1RHDGXZP0"
PREVIEW = "--preview" in sys.argv
D = json.loads((ROOT / "assets" / "data.json").read_text())
UPDATED = D["updated"]
e = html.escape


def v(n): return hashlib.md5((ROOT / "assets" / n).read_bytes()).hexdigest()[:8]
def href(p): return p if PREVIEW else ("/" if p == "index.html" else "/" + p[:-5])
def canon(p): return DOMAIN + ("/" if p == "index.html" else "/" + p[:-5])
def asset(n): return ("" if PREVIEW else "/") + "assets/" + n + "?v=" + v(n)


NAV = [("racket-finder.html", "Racket finder"), ("score.html", "Score keeper"), ("rules.html", "Rules"), ("shots.html", "Shots"), ("beginners.html", "Beginners")]
LOGO = '<svg viewBox="0 0 40 40" aria-hidden="true"><ellipse cx="17" cy="15" rx="12" ry="13" fill="#1747c9"/><g fill="#f4f6f1"><circle cx="13" cy="11" r="1.6"/><circle cx="19" cy="11" r="1.6"/><circle cx="13" cy="17" r="1.6"/><circle cx="19" cy="17" r="1.6"/><circle cx="16" cy="14" r="1.6"/></g><rect x="14" y="26" width="6" height="12" rx="3" fill="#1747c9"/><circle cx="31" cy="29" r="6" fill="#d4f53c" stroke="#0b1530" stroke-width="1.5"/></svg>'
AD = '<div class="ad-slot" data-ad="{}"><!-- AdSense ad unit goes here --></div>'


def faq_html(faqs):
    if not faqs: return ""
    return '<section class="faq"><div class="wrap"><h2>Questions players ask</h2>' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs) + "</div></section>"


# ---- Email signup (Kit form 10215431). Sign-ups go to Kit; Kit redirects to /thanks, then /welcome after confirming. ----
NL_SKIP = ("thanks.html", "welcome.html", "404.html", "privacy.html")
NOINDEX = ("thanks.html", "welcome.html", "404.html")
def signup(file):
    if file in NL_SKIP:
        return ""
    return """<section class="nl" id="newsletter"><div class="wrap"><div class="nl-card">
<div><h2>Free padel rules cheat sheet</h2><p>All the rules on one printable page, including golden point and the new Star Point. Plus a short email when we add new tools and guides.</p></div>
<form class="nl-form" action="https://app.kit.com/forms/10215431/subscriptions" method="post">
<label class="nl-sr" for="nl-email">Email address</label>
<input id="nl-email" type="email" name="email_address" required placeholder="Your email address" autocomplete="email">
<button type="submit">Send my cheat sheet</button>
</form>
<p class="nl-fine">Free. No spam, unsubscribe in one click. See our <a href="/privacy.html">privacy policy</a>.</p>
</div></div></section>"""
NL_THANKS = """<section><div class="wrap nl-done"><h1>Check your inbox</h1>
<p>We've just emailed you a confirmation link. Tap the button in that email and your padel rules cheat sheet opens straight away.</p>
<p>Can't see it after a minute? Look in your spam or promotions folder.</p>
<div class="nl-links"><a href="/score">Score keeper</a><a href="/americano">Americano draw maker</a><a href="/racket-finder">Racket finder</a></div></div></section>"""
NL_WELCOME = """<section><div class="wrap nl-done"><h1>You're in!</h1>
<p>Thanks for confirming. Here's your padel rules cheat sheet:</p>
<a class="nl-btn" href="/assets/free/padel-rules-cheat-sheet.pdf" download>Download the PDF</a>
<p>We'll email you when there's something worth knowing, never more than once a week.</p>
<div class="nl-links"><a href="/score">Score keeper</a><a href="/americano">Americano draw maker</a><a href="/racket-finder">Racket finder</a></div></div></section>"""


AFF = {
    "padel-round-rackets": "https://padelmarket.com/en/collections/rackets-round-shape",
    "padel-teardrop-rackets": "https://padelmarket.com/en/collections/rackets-teardrop-shape",
    "padel-diamond-rackets": "https://padelmarket.com/en/collections/rackets-diamond-shape",
    "padel-rackets": "https://padelmarket.com/en/collections/rackets",
    "padel-shoes": "https://padelmarket.com/en/collections/shoes",
    "padel-balls": "https://padelmarket.com/en/collections/padel-balls",
    "padel-bags": "https://padelmarket.com/en/collections/padel-bags-1",
    "padel-overgrips": "https://padelmarket.com/en/collections/accessories-overgrips",
    "padel-black-friday": "https://padelmarket.com/en/collections/black-friday",
    "padel-black-friday-rackets": "https://padelmarket.com/en/collections/black-friday-rackets",
}
# ---- Affiliate links. Pages link to /go/<slug>; _redirects sends it to the store.
# Until a programme approves us these are plain store URLs; when approved, replace the URL with the tracked link and rebuild.
AFF_ATTR = 'rel="sponsored nofollow noopener" target="_blank"'
AFF_TOP = '<div class="aff-disclosure" role="note"><div class="wrap"><strong>Affiliate disclosure:</strong> some links on this page are affiliate links. If you buy through them we may earn a small commission, at no extra cost to you. It never changes what we recommend. <a href="/about#affiliate">How we choose products</a>.</div></div>'
AFF_NOTE = '<p class="aff-note">We may earn a commission if you buy through these links, at no extra cost to you.</p>'
def go(slug): return "/go/" + slug
# Quick answer box (standing AI-answers rule in README)
def quick(txt, upd=None):
    return f'<div class="qa"><b>Quick answer</b><p>{txt}</p><span>Last updated {e(upd or UPDATED)}</span></div>'

def write_redirects(root):
    lines = "".join(f"/go/{k} {v} 302\n" for k, v in AFF.items())
    (root / "_redirects").write_text(lines)


def page(file, title, desc, body, faqs=None, crumb=None):
    if len(title) > 60 and title.endswith(" | " + SITE): title = title[:-len(" | " + SITE)]  # Google shows the site name anyway; keep titles <=60
    _og = og_image(file, title, DOMAIN)
    url = canon(file)
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": url, "dateModified": UPDATED,
           "isPartOf": {"@type": "WebSite", "name": SITE, "url": DOMAIN + "/"}}]
    if crumb:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]})
    if faqs:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");</script>' if GA_ID else "")
    crumbs_html = (f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol><li><a href="{href("index.html")}">Home</a></li><li aria-current="page">{e(crumb)}</li></ol></div></nav>' if crumb else "")
    nav = "".join(f'<li><a href="{href(f)}"{" aria-current=\"page\"" if f == file else ""}>{n}</a></li>' for f, n in NAV)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
{ga}
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="msvalidate.01" content="215145BE38DEE30C2985F40FB4D4041F">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{"noindex, follow" if file in NOINDEX else "index, follow, max-image-preview:large"}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SITE}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{_og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{_og}"><meta name="theme-color" content="#0e2468">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231747c9'/%3E%3Ccircle cx='16' cy='16' r='8' fill='%23d4f53c'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800&family=Onest:wght@400;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'"><noscript><link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800&family=Onest:wght@400;600;700&display=swap" rel="stylesheet"></noscript>
<link rel="stylesheet" href="{asset("style.css")}">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="head"><div class="wrap">
<a class="brand" href="{href("index.html")}">{LOGO}Padel <b>Glass Box</b></a>
<button class="burger" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<ul class="nav" id="nav">{nav}</ul>
</div></header>
<main>
{crumbs_html}{AFF_TOP if '/go/' in body else ''}{body}
{faq_html(faqs)}
{signup(file)}
{AD.format(file)}
</main>
<footer><div class="wrap"><div class="fgrid">
<div><a class="brand" href="{href("index.html")}" style="color:#fff">{LOGO}Padel <b style="color:#e8f84a">Glass Box</b></a><p style="margin-top:12px">Free padel tools and plain-English guides: find your racket, keep score, learn the rules and the shots.</p></div>
<div><strong style="color:#fff">Tools and guides</strong><ul>{"".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in NAV)}<li><a href="{href("glossary.html")}">Glossary</a></li><li><a href="{href("americano.html")}">Americano generator</a></li><li><a href="{href("court-dimensions.html")}">Court dimensions</a></li><li><a href="{href("pickleball-court-dimensions.html")}">Pickleball court dimensions</a></li><li><a href="{href("pickleball-rules.html")}">Pickleball rules</a></li><li><a href="{href("pickleball-score.html")}">Pickleball score keeper</a></li><li><a href="{href("court-sizes-compared.html")}">Court sizes compared</a></li><li><a href="{href("badminton-court-dimensions.html")}">Badminton court dimensions</a></li><li><a href="{href("tennis-court-dimensions.html")}">Tennis court dimensions</a></li><li><a href="{href("padel-court-cost.html")}">Padel court cost</a></li><li><a href="{href("level-calculator.html")}">Level calculator</a></li><li><a href="{href("golden-point-star-point.html")}">Golden point vs Star Point</a></li><li><a href="{href("serve-rules.html")}">Serve rules and checker</a></li><li><a href="{href("positioning.html")}">Where to stand</a></li><li><a href="{href("warm-up.html")}">Warm-up timer</a></li><li><a href="{href("padel-balls.html")}">When to change balls</a></li><li><a href="{href("wall-rules.html")}">Wall and fence rules</a></li><li><a href="{href("padel-vs-tennis-vs-pickleball.html")}">Padel vs tennis vs pickleball</a></li><li><a href="{href("racket-balance.html")}">Racket weight and balance</a></li><li><a href="{href("round-robin.html")}">Round robin generator</a></li><li><a href="{href("padel-shoes.html")}">Padel shoes guide</a></li><li><a href="{href("padel-calories.html")}">Padel calories calculator</a></li><li><a href="{href("ladder.html")}">Padel ladder tracker</a></li><li><a href="{href("net-rules.html")}">Net rules checker</a></li><li><a href="{href("racket-care.html")}">Racket care and health check</a></li><li><a href="{href("drills.html")}">Padel drills planner</a></li><li><a href="{href("king-of-the-court.html")}">King of the Court generator</a></li><li><a href="{href("tie-break.html")}">Tie-break rules and tracker</a></li><li><a href="{href("out-of-court-play.html")}">Out-of-court play rules</a></li><li><a href="{href("padel-injuries.html")}">Padel injuries and prevention</a></li><li><a href="{href("padel-grip.html")}">How to hold a padel racket</a></li><li><a href="{href("bandeja-vs-vibora.html")}">Bandeja vs víbora vs smash</a></li><li><a href="{href("padel-rankings.html")}">Padel world rankings</a></li><li><a href="{href("fix-my-padel.html")}">Fix my padel: problem fixer</a></li><li><a href="{href("which-side-padel.html")}">Left or right side quiz</a></li><li><a href="{href("padel-match-tracker.html")}">Padel match tracker</a></li><li><a href="{href("padel-training-plan.html")}">Training plan generator</a></li><li><a href="{href("padel-etiquette.html")}">Padel etiquette</a></li><li><a href="{href("how-to-serve-padel.html")}">How to serve + serve tracker</a></li><li><a href="{href("padel-tactics.html")}">Padel tactics trainer</a></li><li><a href="{href("padel-improvement-guide.html")}">How to get better at padel</a></li><li><a href="{href("padel-beginner-plan.html")}">30-day beginner plan</a></li><li><a href="{href("padel-tournament-bracket.html")}">Tournament bracket generator</a></li><li><a href="{href("padel-vs-racquetball.html")}">Padel vs racquetball vs platform tennis</a></li><li><a href="{href("padel-group-stage-generator.html")}">Group stage generator</a></li><li><a href="{href("padel-vs-squash.html")}">Padel vs squash</a></li><li><a href="{href("padel-booking-apps.html")}">Padel booking apps</a></li><li><a href="{href("history-of-padel.html")}">History of padel</a></li><li><a href="{href("dupr-rating.html")}">How to get a DUPR rating</a></li><li><a href="{href("padel-lob.html")}">How to hit a lob</a></li><li><a href="{href("padel-overgrip.html")}">When to change an overgrip</a></li><li><a href="{href("padel-volley.html")}">How to volley</a></li><li><a href="{href("padel-return-of-serve.html")}">How to return serve</a></li><li><a href="{href("padel-back-glass.html")}">Playing off the back glass</a></li><li><a href="{href("padel-smash.html")}">How to smash (x3, x4)</a></li><li><a href="{href("padel-chiquita.html")}">The chiquita</a></li><li><a href="{href("padel-weather.html")}">Padel in rain, cold and wind</a></li><li><a href="{href("padel-elbow.html")}">Padel elbow + arm-load check</a></li><li><a href="{href("compare-padel-rackets.html")}">Compare two rackets</a></li><li><a href="{href("padel-footwork.html")}">Footwork + split-step trainer</a></li><li><a href="{href("padel-communication.html")}">Partner calls + middle ball</a></li><li><a href="{href("padel-rules-quiz.html")}">Padel rules quiz</a></li><li><a href="{href("junior-padel.html")}">Junior padel guide</a></li><li><a href="{href("padel-cool-down.html")}">Cool-down stretch timer</a></li><li><a href="{href("padel-racket-weight.html")}">Racket weight calculator</a></li><li><a href="{href("padel-court-surfaces.html")}">Court surfaces + checker</a></li><li><a href="{href("padel-solo-practice.html")}">Solo practice + timer</a></li><li><a href="{href("padel-workout.html")}">Padel workout builder</a></li><li><a href="{href("padel-bags.html")}">Padel bag picker</a></li><li><a href="{href("control-vs-power-padel-racket.html")}">Control vs power racket test</a></li><li><a href="{href("padel-racket-for-women.html")}">Padel racket for women</a></li><li><a href="{href("padel-racket-for-tennis-players.html")}">Padel racket for tennis players</a></li><li><a href="{href("padel-racket-for-spin.html")}">Padel racket for spin</a></li><li><a href="{href("padel-forehand.html")}">How to hit a forehand</a></li><li><a href="{href("padel-racket-shapes.html")}">Racket shapes compared</a></li></ul></div>
<div><strong style="color:#fff">Buying</strong><ul><li><a href="{href("best-padel-racket-for-beginners.html")}">Best racket for beginners</a></li><li><a href="{href("cheap-padel-rackets.html")}">Cheap padel rackets</a></li><li><a href="{href("intermediate-padel-racket.html")}">Intermediate rackets</a></li><li><a href="{href("padel-black-friday.html")}">Padel Black Friday 2026</a></li><li><a href="{href("padel-gifts.html")}">Padel gift ideas</a></li><li><a href="{href("padel-equipment.html")}">Padel equipment and what to wear</a></li><li><a href="{href("padel-racket-for-kids.html")}">Padel rackets for kids</a></li><li><a href="{href("padel-racket-materials.html")}">Racket materials explained</a></li><li><a href="{href("padel-lessons.html")}">Padel lessons: cost and first lesson</a></li><li><a href="{href("padel-cost.html")}">How much padel costs</a></li><li><a href="{href("racket-finder.html")}">Racket finder</a></li></ul></div>
<div><strong style="color:#fff">Site</strong><ul><li><a href="{href("about.html")}">About and contact</a></li><li><a href="{href("privacy.html")}">Privacy policy</a></li></ul></div>
</div>
<p class="legal">{SITE} is an independent guide and isn't linked to any padel federation, club or brand. Rules follow the International Padel Federation (FIP); local competitions can use their own formats. Last checked {e(UPDATED)}.</p>
</div></footer>
<script>window.PP={json.dumps({"zones": D["zones"]})};</script>
<script src="{asset("app.js")}"></script>
</body>
</html>
'''
    (ROOT / file).write_text(doc, encoding="utf-8")


ICO = {
    "racket": '<svg viewBox="0 0 32 32"><ellipse cx="14" cy="12" rx="9" ry="10" fill="#1747c9"/><rect x="11.5" y="21" width="5" height="9" rx="2.5" fill="#1747c9"/><circle cx="25" cy="24" r="4.5" fill="#d4f53c" stroke="#0b1530"/></svg>',
    "score": '<svg viewBox="0 0 32 32"><rect x="3" y="6" width="26" height="20" rx="5" fill="#0b1530"/><text x="16" y="21" text-anchor="middle" font-size="11" font-weight="800" fill="#d4f53c" font-family="sans-serif">15-40</text></svg>',
    "court": '<svg viewBox="0 0 32 32"><rect x="5" y="3" width="22" height="26" rx="3" fill="#1747c9"/><path d="M5 16h22M16 7v18M5 7h22M5 25h22" stroke="#fff" stroke-width="1.4"/></svg>',
    "shot": '<svg viewBox="0 0 32 32"><path d="M4 26 Q16 0 28 22" fill="none" stroke="#1747c9" stroke-width="2.5" stroke-dasharray="3 3"/><circle cx="28" cy="22" r="4" fill="#d4f53c" stroke="#0b1530"/></svg>',
    "check": '<svg viewBox="0 0 32 32"><rect x="4" y="4" width="24" height="24" rx="7" fill="#d4f53c"/><path d="M10 16l4 4 8-9" fill="none" stroke="#0b1530" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}

COURT_HERO = '''<svg viewBox="0 0 520 300" role="img" aria-label="Drawing of a padel court with a ball flying over the net">
<rect x="10" y="10" width="500" height="280" rx="10" fill="#1d55e6"/><rect x="10" y="10" width="500" height="280" rx="10" fill="none" stroke="#fff" stroke-width="3"/>
<path d="M260 10v280" stroke="#e8edf8" stroke-width="6"/><path d="M84 10v280M436 10v280M84 150h352" stroke="#fff" stroke-width="3"/>
<rect x="10" y="10" width="500" height="280" rx="10" fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="14"/>
<circle class="ball" cx="100" cy="210" r="12" fill="#d4f53c" stroke="#0b1530" stroke-width="2"/>
</svg>'''

# ---------------- HOME ----------------
RK = '<svg viewBox="0 0 120 200" aria-hidden="true"><ellipse cx="60" cy="62" rx="50" ry="56" fill="#e8f84a"/><g fill="#0e2468">' + "".join(f'<circle cx="{60+x}" cy="{62+y}" r="2.6"/>' for y in range(-36, 37, 12) for x in range(-36, 37, 12) if (x*x)/(34*34)+(y*y)/(38*38) <= 1) + '</g><rect x="52" y="116" width="16" height="70" rx="7" fill="#e8f84a"/></svg>'
RK2 = RK.replace('#e8f84a', '#ffffff').replace('rx="50" ry="56"', 'rx="46" ry="58"')
MINI_COURT = '<svg viewBox="0 0 300 140" aria-hidden="true"><rect x="6" y="6" width="288" height="128" rx="10" fill="#1e46c8"/><path d="M150 6v128" stroke="#e4eef6" stroke-width="5"/><path d="M48 6v128M252 6v128M48 70h204" stroke="#fff" stroke-width="2"/><rect x="6" y="6" width="288" height="128" rx="10" fill="none" stroke="#9cc4ea" stroke-width="7" opacity=".7"/><rect x="49" y="71" width="100" height="62" fill="rgba(255,255,255,0.25)" stroke="#e8f84a" stroke-width="3"/></svg>'
MINI_SHOT = '<svg viewBox="0 0 300 110" aria-hidden="true"><rect width="300" height="110" rx="12" fill="#0e2468"/><path d="M150 62v48" stroke="#e4eef6" stroke-width="5"/><path d="M0 100h300" stroke="#fff" stroke-width="2" opacity=".6"/><rect x="290" y="20" width="10" height="90" fill="#9cc4ea" opacity=".6"/><path d="M30 26 C110 26 200 70 270 96 L290 60 C230 30 140 40 40 74" fill="none" stroke="#e8f84a" stroke-width="2.5" stroke-dasharray="5 6"/><circle r="6" fill="#e8f84a"><animateMotion dur="3.2s" repeatCount="indefinite" path="M30 26 C110 26 200 70 270 96 L290 60 C230 30 140 40 40 74"/></circle></svg>'
R_SERVE = '<svg viewBox="0 0 260 120" aria-hidden="true"><rect x="0" y="0" width="260" height="120" rx="12" fill="#132e80"/><path d="M130 10v100" stroke="#e4eef6" stroke-width="4"/><path d="M40 10v100M220 10v100M40 60h180" stroke="#fff" stroke-width="1.5" opacity=".7"/><rect x="40" y="60" width="90" height="50" fill="none"/><rect x="130" y="10" width="90" height="50" fill="#e8f84a" opacity=".22"/><path d="M28 92 Q110 20 180 36" fill="none" stroke="#e8f84a" stroke-width="2.5" stroke-dasharray="5 5"/><circle cx="28" cy="92" r="6" fill="#e8f84a"/></svg>'
R_WALL = '<svg viewBox="0 0 260 120" aria-hidden="true"><rect width="260" height="120" rx="12" fill="#132e80"/><path d="M0 104h260" stroke="#fff" stroke-width="2" opacity=".7"/><rect x="236" y="14" width="14" height="90" rx="3" fill="#9cc4ea" opacity=".55"/><path d="M20 30 Q120 20 190 104 L236 60 Q170 30 110 50" fill="none" stroke="#e8f84a" stroke-width="2.5" stroke-dasharray="5 5"/><circle cx="190" cy="104" r="4" fill="none" stroke="#fff"/><circle cx="110" cy="50" r="6" fill="#e8f84a"/></svg>'
R_SCORE = '<svg viewBox="0 0 260 120" aria-hidden="true"><rect width="260" height="120" rx="12" fill="#132e80"/>' + "".join(f'<rect x="{16+i*60}" y="30" width="48" height="60" rx="8" fill="{"#e8f84a" if i == 3 else "#1e46c8"}"/><text x="{40+i*60}" y="70" text-anchor="middle" font-family="Unbounded, sans-serif" font-weight="700" font-size="18" fill="{"#0e2468" if i == 3 else "#fff"}">{v}</text>' for i, v in enumerate(["15", "30", "40", "G"])) + '</svg>'
home = f'''<div class="arena"><div class="wrap arena-grid">
<div class="arena-copy"><h1>Learn padel, pick a racket, keep score.</h1>
<p class="lead">Free tools and plain-English guides for new and improving padel players. No sign-up, and it all works on your phone at the court.</p>
<div class="btns"><a class="btn lime" href="{href("racket-finder.html")}">Find my racket</a><a class="btn ghost" href="{href("score.html")}">Open the score keeper</a></div></div>
<div class="stage"><canvas id="court3d" role="img" aria-label="Animated padel court seen from behind the back glass. A rally plays, with the ball bouncing off the glass walls."></canvas>
<div class="hud" aria-hidden="true"><div><b id="hud-shots">0</b><span>Shots this rally</span></div><div><b id="hud-glass">0</b><span>Off the glass</span></div></div>
<p class="stage-hint" id="stage-hint">Tap the court to serve a new rally</p></div>
</div></div>
<section><div class="wrap"><div class="sh"><h2>Tools for every part of your game</h2><p class="muted">Free, quick, and saved on your phone.</p></div>
<div class="bento">
<a class="tile t-finder" href="{href("racket-finder.html")}"><h3>Find the racket that fits your game</h3><p>Three questions about your level, style and arm. You get the shape, weight, balance and materials that suit you, and why.</p><div class="art">{RK}{RK2.replace('#ffffff', 'rgba(255,255,255,0.18)')}</div></a>
<a class="tile t-score" href="{href("score.html")}"><h3>Score keeper</h3><p>Tap the team that wins each point. Golden point, tie-breaks and undo included.</p><div class="art"><div class="mini-board"><span>Team A</span><i>4 games</i><b>40</b><span>Team B</span><i>4 games</i><b>AD</b></div></div></a>
<a class="tile t-rules" href="{href("rules.html")}"><h3>Rules on a court you can tap</h3><p>Touch the net, the glass or the service box to read the rule that goes with it.</p><div class="art">{MINI_COURT}</div></a>
<a class="tile t-shots" href="{href("shots.html")}"><h3>Shot library</h3><p>Bandeja, víbora, chiquita and more, each with its ball path drawn out.</p><div class="art">{MINI_SHOT}</div></a>
<a class="tile t-begin" href="{href("beginners.html")}"><h3>First match checklist</h3><p>What to bring, what to know, and where to find a court near you.</p><div class="art"><ul class="mini-check"><li class="on">Padel racket</li><li class="on">Court shoes</li><li>Padel balls</li></ul></div></a>
<a class="tile t-gloss" href="{href("glossary.html")}"><h3>Padel glossary</h3><p>Padel borrows a lot of Spanish. Look up any word you heard on court.</p><div class="art words"><span>bandeja</span><span>víbora</span><span>chiquita</span><span>bajada</span><span>golden point</span><span>malla</span></div></a>
</div></div></section>
{AD.format("home-mid")}
<section class="band"><div class="wrap"><div class="sh"><h2>Padel in three rules</h2><a class="btn ghost sm" href="{href("rules.html")}">All the rules</a></div>
<div class="rule3">
<div>{R_SERVE}<h3>Serve underhand, diagonally</h3><p>Bounce the ball behind the service line, hit it at or below waist height, and land it in the box across from you. You get two tries.</p></div>
<div>{R_WALL}<h3>Ground first, then the glass</h3><p>On your side the ball may bounce once and then hit the walls, and it's still in play. If it hits a wall before the ground on your side, the other team wins the point.</p></div>
<div>{R_SCORE}<h3>Scored like tennis</h3><p>15, 30, 40, game, with sets to six. At 40-40 many clubs play a golden point, where one deciding point wins the game.</p></div>
</div></div></section>'''
home_faq = [
    ("What is padel?", "Padel is a racket sport played mostly in doubles on an enclosed 20 x 10 m court, smaller than a tennis court. You use a solid, holed racket and can play the ball off the glass walls."),
    ("How big is a padel court?", "A padel court is 20 m long and 10 m wide. The net is 88 cm high in the middle and 92 cm at the posts."),
    ("Is padel easy for beginners?", "Yes. The underhand serve, small court and walls make long rallies possible from the first game, which is why it's one of the fastest-growing sports."),
    ("Is padel scored like tennis?", "Yes: 15, 30, 40 and game, with sets to six. Many matches use a golden point at 40-40, and the 2026 rules also allow a format called Star Point."),
]
page("index.html", "Padel Tennis Rules, Racket Finder and Free Score Keeper | Padel Glass Box",
     "Free padel tools: find the right racket in a minute, keep score on court with your phone, and learn padel rules and shots in plain English.", home, home_faq)

# ---------------- RACKET FINDER ----------------
def q(name, title, opts):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if i == 0 else "false"}">{lab}</button>' for i, (val, lab) in enumerate(opts))
    return f'<div class="q"><h3>{title}</h3><div class="opts" data-q="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'

finder = f'''<header class="hero"><div class="wrap"><h1>Find your padel racket.</h1>
<p class="lead">Three questions. You'll get the racket shape, balance, weight, core and face material that suit your game, and why.</p>
{quick("Most beginners do best with a round padel racket: low balance (under about 260 mm), a weight of about 345 to 360 g, a soft foam core and a fibreglass face. Improving players often move to a teardrop shape, and experienced attacking players to a diamond. If your elbow or shoulder gets sore, stay light, low-balance and soft.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="quiz">
<div class="card">
{q("level", "1. How long have you played?", [("new", "Under 6 months"), ("improving", "6 months to 2 years"), ("advanced", "2 years or more")])}
{q("style", "2. How do you like to play?", [("control", "Steady and in control"), ("allround", "A bit of everything"), ("attack", "Attack and smash")])}
{q("arm", "3. Do you get sore elbows or shoulders?", [("no", "No"), ("yes", "Sometimes")])}
<p class="muted" style="margin:0;font-size:.92rem">Your answer updates instantly. Try different options to compare.</p>
</div>
<aside class="result" id="result" aria-live="polite"></aside>
</div></section>
{AD.format("finder-mid")}
<section><div class="wrap"><div class="sh"><h2>What are the 3 padel racket shapes?</h2></div><div class="grid">
<div class="card"><span class="pill b">Most control</span><h3 style="margin-top:10px">Round</h3><p>The sweet spot is large and right in the middle, and the weight sits towards the handle. Forgiving, easy to handle, and the usual first racket. Plenty of top players use them too.</p></div>
<div class="card"><span class="pill i">All-round</span><h3 style="margin-top:10px">Teardrop</h3><p>A mix of round and diamond, with medium balance. More punch than a round racket while still being fairly easy to control.</p></div>
<div class="card"><span class="pill a">Most power</span><h3 style="margin-top:10px">Diamond</h3><p>Weight sits towards the head and the sweet spot is smaller and higher up. Big smashes, but less forgiving, so it suits experienced attackers.</p></div>
</div></div></section>
<section><div class="wrap"><div class="sh"><h2>What do padel racket specs mean?</h2></div><div class="grid">
<div class="card"><h3>Weight</h3><p>Most adult rackets weigh roughly 345 to 385 g. Heavier rackets hit harder but tire your arm sooner; lighter ones are quicker at the net. New players usually do best under about 360 g.</p></div>
<div class="card"><h3>Balance</h3><p>Measured in mm from the bottom of the handle. Low balance (under about 260 mm) means control and quick hands. High balance (over about 270 mm) means power but more strain. <a href="{href("racket-balance.html")}">Decode and compare two rackets</a>.</p></div>
<div class="card"><h3>Core foam</h3><p>Soft foam gives easy power and comfort at slow speeds. Hard foam gives control when you swing fast.</p></div>
<div class="card"><h3>Face material</h3><p>Fiberglass is softer and forgiving. Carbon is stiffer and more precise, and usually costs more. <a href="{href("padel-racket-materials.html")}">Decode any racket label</a>.</p></div>
</div></div></section>
<section style="padding-top:0" id="grip"><div class="wrap"><div class="sh"><h2>How do you choose a grip and overgrip?</h2><p class="muted">The cheapest upgrade you can make to any racket. How to hold it: <a href="{href("padel-grip.html")}">padel grip guide</a>. Looking after the rest of it: <a href="{href("racket-care.html")}">racket care</a>.</p></div><div class="grid">
<div class="card"><h3>Grip vs overgrip</h3><p>The base grip is the thick, cushioned layer that comes on the handle. An overgrip is a thin, light tape you wrap over it. It protects the base grip, which is harder to replace, and soaks up sweat.</p></div>
<div class="card"><h3>When to change it</h3><p>Change it when it looks dirty or worn, or when it feels slippery, wet or less sticky. Social players often get a few sessions from one. Players who sweat a lot, or play in heat, change it far more often.</p></div>
<div class="card"><h3>How to put one on</h3><p>Take off the old overgrip. Start at the bottom of the handle, by the butt cap, and wrap up towards the head, keeping each turn parallel and slightly overlapping. Cut the end straight and fix it with the finishing tape.</p></div>
<div class="card"><h3>Handle feels too thin?</h3><p>Padel handles often feel small in bigger hands. Overlap the overgrip more as you wrap, or add a second overgrip, to make the handle thicker. Overlap less for a thinner feel. Use the finger test in the <a href="{href("padel-grip.html")}">grip guide</a> to check.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which racket by level?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Level</th><th scope="col">Shape</th><th scope="col">Balance</th><th scope="col">Feel</th></tr></thead><tbody>
<tr><td>Under 6 months</td><td>Round</td><td>Low (head-light)</td><td>Soft core, fibreglass face</td></tr>
<tr><td>6 months to 2 years</td><td>Round or teardrop</td><td>Low to medium</td><td>Soft to medium</td></tr>
<tr><td>2 years or more, attacking</td><td>Teardrop or diamond</td><td>Medium to high</td><td>Harder core, carbon face</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">A guide, not a rule: try a friend's racket or a demo racket at your club before you buy. Moving on from your first racket? Use the <a href="{href("intermediate-padel-racket.html")}">intermediate upgrade check</a>. Buying for a child? See the <a href="{href("padel-racket-for-kids.html")}">junior racket size finder</a>. Not sure of your level? Use the <a href="{href("level-calculator.html")}">level calculator</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Compare two rackets</h3><p>Type in the weight and balance from the label and see what they mean in the <a href="{href("racket-balance.html")}">balance decoder</a>.</p></div>
<div class="card"><h3>Hold it right</h3><p>One grip does almost everything. Learn it with the <a href="{href("padel-grip.html")}">padel grip guide</a> and grip check.</p></div>
<div class="card"><h3>Make it last</h3><p>Keep it out of the hot car and check it for cracks with the <a href="{href("racket-care.html")}">racket health check</a>.</p></div>
</div></div></section>'''
finder_faq = [
    ("How do I hold a padel racket?", "Use the continental grip: stand the racket on its edge and shake hands with the handle, so the V between your thumb and first finger sits on the top edge. It works for almost every shot."),
    ("What padel racket should a beginner buy?", "Most beginners do best with a round racket: low balance, a lighter weight, soft foam and a fiberglass face. It's forgiving and easy to control."),
    ("Round, teardrop or diamond: which is best?", "Round gives the most control, diamond the most power, and teardrop sits in between. Many players start round, move to teardrop, then try diamond."),
    ("How heavy should a padel racket be?", "Most adult rackets weigh around 345 to 385 g. Pick the lighter end if you're new or have sore elbows, and the heavier end if you hit hard."),
    ("What does the balance number on a padel racket mean?", "It is the distance in millimetres from the bottom of the handle to the point where the racket balances. Under about 260 mm is head-light and easy to control; over about 270 mm is head-heavy and more powerful."),
    ("How often should I change my padel overgrip?", "When it starts to feel slippery or less sticky, or looks dirty and worn. For social players that is often every few sessions; players who sweat a lot change it much more often."),
    ("How do I make my padel racket handle thicker?", "Overlap the overgrip more as you wrap it, or put a second overgrip on top of the first."),
    ("Does a racket help with tennis elbow?", "A lighter racket with a soft core and low balance puts less strain on your arm. If pain continues, see a doctor or physio."),
]
page("racket-finder.html", "Padel Racket Finder: Which Racket Suits You? | Padel Glass Box",
     "Answer 3 questions and find the padel racket shape, weight, balance, core and face that suit your level and style. Free and instant.", finder + f'''<section><div class="wrap"><div class="aff-box"><h3>Shop padel gear</h3><p>Browse rackets by shape, plus the shoes, balls and grips you need for your first match.</p><ul class="aff-links"><li><a href="/go/padel-round-rackets" rel="sponsored nofollow noopener" target="_blank">Round rackets</a></li><li><a href="/go/padel-teardrop-rackets" rel="sponsored nofollow noopener" target="_blank">Teardrop rackets</a></li><li><a href="/go/padel-diamond-rackets" rel="sponsored nofollow noopener" target="_blank">Diamond rackets</a></li><li><a href="/go/padel-shoes" rel="sponsored nofollow noopener" target="_blank">Padel shoes</a></li><li><a href="/go/padel-balls" rel="sponsored nofollow noopener" target="_blank">Balls</a></li><li><a href="/go/padel-bags" rel="sponsored nofollow noopener" target="_blank">Bags</a></li><li><a href="/go/padel-overgrips" rel="sponsored nofollow noopener" target="_blank">Overgrips</a></li></ul>{AFF_NOTE}</div></div></section>''', finder_faq, "Racket finder")

# ---------------- SCORE KEEPER ----------------
score = f'''<header class="hero" style="padding-bottom:10px"><div class="wrap"><h1>Padel score keeper.</h1>
<p class="lead">Put your phone by the net and tap the side that wins each point. It handles deuce, golden point, tie-breaks and sets, and remembers the score if you close the page.</p>
{quick("Padel is scored like tennis: points go 0, 15, 30, 40, game. A set is first to 6 games with a 2-game lead, and at 6-6 a tie-break to 7 points (2 clear) decides it. Matches are usually best of three sets. At 40-40 you play advantage, golden point or Star Point, whichever the organiser picks.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="score" id="score">
<div class="score-top"><div class="seg" id="mode" role="group" aria-label="Deuce format"><button type="button" data-v="adv" aria-pressed="true">Advantage</button><button type="button" data-v="golden" aria-pressed="false">Golden point</button><button type="button" data-v="star" aria-pressed="false">Star Point</button></div>
<div class="btns" style="margin:0"><button class="btn sm" type="button" id="rename">Names</button><button class="btn sm" type="button" id="swap-srv">Switch server</button></div></div>
<form id="names" hidden style="display:grid;gap:8px;grid-template-columns:1fr 1fr auto;margin-bottom:12px"><label class="sr-only" for="n0">Team A name</label><input id="n0" class="search" style="margin:0" maxlength="20"><label class="sr-only" for="n1">Team B name</label><input id="n1" class="search" style="margin:0" maxlength="20"><button class="btn lime sm" type="submit">Save</button></form>
<div class="teams">
<button class="team" type="button" data-i="0"><span class="tn"><span class="srv" title="Serving"></span><span class="tname">Team A</span></span><span class="pts">0</span><span class="gs">Games 0</span><span class="tap">Tap when this team wins the point</span></button>
<button class="team b" type="button" data-i="1"><span class="tn"><span class="srv" title="Serving"></span><span class="tname">Team B</span></span><span class="pts">0</span><span class="gs">Games 0</span><span class="tap">Tap when this team wins the point</span></button>
</div>
<div class="msg" id="msg" aria-live="polite"></div><div class="sets" id="sets"></div>
<div class="btns"><button class="btn sm" type="button" id="undo">Undo last point</button><button class="btn sm" type="button" id="reset">New match</button></div>
</div></div></section>
{AD.format("score-mid")}
<section><div class="wrap"><div class="sh"><h2>How does padel scoring work?</h2></div><div class="grid">
<div class="card"><h3>Points</h3><p>0, 15, 30, 40, then the game. Exactly like tennis.</p></div>
<div class="card"><h3>Deuce</h3><p>At 40-40 there are three official options: classic advantage, golden point (one deciding point) or the newer Star Point. All three are built in here. Not sure which to pick? See <a href="{href("golden-point-star-point.html")}">golden point vs Star Point</a>.</p></div>
<div class="card"><h3>Sets and tie-breaks</h3><p>A set goes to six games with a two-game lead. At 6-6 a tie-break is played to 7 points, two clear. Most matches are best of three sets. Who serves when: <a href="{href("tie-break.html")}">tie-break rules and tracker</a>.</p></div>
<div class="card"><h3>Golden point side</h3><p>With golden point, the receiving pair chooses which player receives the deciding serve.</p></div>
<div class="card"><h3>Star Point</h3><p>You play advantage twice. If the game comes back to 40-40 a third time, one deciding point wins it. The score keeper counts the deuces for you.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel scoring at a glance</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Part</th><th scope="col">How it is scored</th></tr></thead><tbody>
<tr><td>Points in a game</td><td>0 (called love), 15, 30, 40, game</td></tr>
<tr><td>40-40</td><td>Deuce: advantage, golden point or Star Point</td></tr>
<tr><td>A set</td><td>First to 6 games, 2 games clear (6-4, 7-5)</td></tr>
<tr><td>At 6-6</td><td>Tie-break: first to 7 points, 2 clear (7-6 in the set)</td></tr>
<tr><td>A match</td><td>Usually best of 3 sets</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Social nights often use other formats, scored by points or by rounds instead of sets.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Not playing a normal match?</h2></div><div class="grid">
<div class="card"><h3>Americano or Mexicano</h3><p>Each match is a set number of points, such as 24, and you keep every point you win. Use the <a href="{href("americano.html")}">Americano draw maker</a>.</p></div>
<div class="card"><h3>King of the Court</h3><p>Short timed rounds where winners move up a court and losers move down. Run it with the <a href="{href("king-of-the-court.html")}">King of the Court generator</a>.</p></div>
<div class="card"><h3>League with fixed pairs</h3><p>Every pair plays every other pair and the table does the maths: <a href="{href("round-robin.html")}">round robin generator</a>. Want a winner fast? Make a <a href="{href("padel-tournament-bracket.html")}">knockout bracket</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Pick a deuce rule</h3><p>See all three side by side in <a href="{href("golden-point-star-point.html")}">golden point vs Star Point vs advantage</a>.</p></div>
<div class="card"><h3>Settle a call</h3><p>Was that ball in? Check the <a href="{href("wall-rules.html")}">wall rules</a>, <a href="{href("net-rules.html")}">net rules</a> or <a href="{href("serve-rules.html")}">serve rules</a>.</p></div>
<div class="card"><h3>Warm up first</h3><p>Start the match ready with the 10-minute <a href="{href("warm-up.html")}">warm-up timer</a>.</p></div>
<div class="card"><h3>Count your errors</h3><p>Log how each point ends and find your weakest shot with the <a href="{href("padel-match-tracker.html")}">padel match tracker</a>.</p></div>
</div></div></section>'''
score_faq = [
    ("How do you keep score in padel?", "Like tennis: 0, 15, 30, 40 and game. Sets go to six games with a two-game lead, and a tie-break decides 6-6."),
    ("What is the golden point in padel?", "At 40-40, one deciding point is played. The receiving pair chooses which side receives, and whoever wins that point wins the game."),
    ("What is Star Point in padel?", "Star Point is a deuce format used on the pro tours from 2026. You play advantage twice; if the game reaches 40-40 a third time, one deciding point wins it. This score keeper supports it."),
    ("Does this score keeper save my match?", "Yes. The score is saved on your phone, so you can lock the screen or close the page and carry on."),
    ("What happens at 6-6 in padel?", "A tie-break is played. The first team to 7 points with a 2-point lead wins the tie-break, and the set ends 7-6."),
    ("How many sets are in a padel match?", "Most padel matches are best of three sets. Social games and leagues sometimes play one set or a timed match instead."),
    ("Why is zero called love in padel?", "Padel took its scoring from tennis, where zero is called love. So 15-0 is said as fifteen-love."),
]
page("score.html", "Padel Score Keeper: Free Scoreboard for Your Phone | Padel Glass Box",
     "Free padel score keeper for your phone. Tap to score with advantage, golden point or Star Point, plus tie-breaks, sets, undo and server tracking. No app needed.", score, score_faq, "Score keeper")

# ---------------- RULES ----------------
court_svg = '''<svg viewBox="0 0 360 640" role="group" aria-label="Top-down padel court. Select a part to read the rule.">
<g class="zone" data-id="court" tabindex="0" role="button" aria-label="Playing area"><rect class="hit" x="30" y="30" width="300" height="580" fill="#1d55e6"/></g>
<g class="zone" data-id="box" tabindex="0" role="button" aria-label="Service box"><rect class="hit" x="30" y="118" width="150" height="202" fill="rgba(255,255,255,0.06)"/><rect class="hit" x="180" y="320" width="150" height="202" fill="rgba(255,255,255,0.06)"/></g>
<g class="zone" data-id="back" tabindex="0" role="button" aria-label="Back wall"><rect class="hit" x="18" y="14" width="324" height="16" rx="4" fill="#8fd3ff"/><rect class="hit" x="18" y="610" width="324" height="16" rx="4" fill="#8fd3ff"/></g>
<g class="zone" data-id="side" tabindex="0" role="button" aria-label="Side walls"><rect class="hit" x="14" y="30" width="16" height="580" fill="#8fd3ff"/><rect class="hit" x="330" y="30" width="16" height="580" fill="#8fd3ff"/><path d="M14 90v460M346 90v460" stroke="#5b6475" stroke-width="16" stroke-dasharray="3 3" opacity=".7"/></g>
<g class="zone" data-id="service" tabindex="0" role="button" aria-label="Service line"><rect class="hit" x="30" y="110" width="300" height="16" fill="transparent"/><rect class="hit" x="30" y="514" width="300" height="16" fill="transparent"/><path d="M30 118h300M30 522h300" stroke="#fff" stroke-width="3" pointer-events="none"/></g>
<g class="zone" data-id="centre" tabindex="0" role="button" aria-label="Centre line"><rect class="hit" x="172" y="118" width="16" height="404" fill="transparent"/><path d="M180 118v404" stroke="#fff" stroke-width="3" pointer-events="none"/></g>
<g class="zone" data-id="net" tabindex="0" role="button" aria-label="The net"><rect class="hit" x="20" y="310" width="320" height="20" rx="4" fill="#f4f6f1"/><path d="M20 320h320" stroke="#0b1530" stroke-width="2" pointer-events="none"/></g>
<text x="180" y="72" text-anchor="middle" fill="#fff" font-family="sans-serif" font-weight="800" font-size="14" pointer-events="none">10 m wide</text>
<text x="180" y="590" text-anchor="middle" fill="#fff" font-family="sans-serif" font-weight="800" font-size="14" pointer-events="none">20 m long</text>
</svg>'''
rules = f'''<header class="hero"><div class="wrap"><h1>Padel rules, tap by tap.</h1>
<p class="lead">Tap any part of the court to see the rule that goes with it, then read the key rules for serving, walls and scoring below.</p>
{quick("Padel is played in pairs on a 20 x 10 m court with glass walls. Serve underhand, after one bounce, at or below waist height, diagonally into the box across the net (two tries). The ball must bounce on the ground before it touches a wall on the other side; after that bounce it may hit the glass and stay in play. Scoring is like tennis: 15, 30, 40, game, sets to six, tie-break at 6-6.")}</div></header>
<section style="padding-top:10px"><div class="wrap rules-layout">
<div class="court-art" style="max-width:440px;margin-inline:auto;width:100%">{court_svg}</div>
<aside class="card zpanel" id="zpanel" aria-live="polite"></aside>
</div></section>
{AD.format("rules-mid")}
<section><div class="wrap"><div class="sh"><h2>What are the basic rules of padel?</h2></div><div class="grid">
<div class="card"><h3>The serve</h3><p>Stand behind the service line with your feet off the lines, bounce the ball, and hit it underhand at or below waist height with one foot on the ground. It must land in the box diagonally opposite. You get two attempts per point.</p></div>
<div class="card"><h3>A serve is a fault if</h3><p>it lands outside the diagonal box, it's hit above the waist, you miss the ball, your foot touches the line, or after bouncing in the box it hits the metal mesh. Not sure? Use our <a href="{href("serve-rules.html")}">serve checker</a>, or test yourself with the <a href="{href("padel-rules-quiz.html")}">padel rules quiz</a>.</p></div>
<div class="card"><h3>Lets</h3><p>If the serve touches the net and still lands in the right box, without touching the metal fence, it is a let and you replay that serve.</p></div>
<div class="card"><h3>Receiving</h3><p>The receiver must let the serve bounce before hitting it. After that, players can volley freely.</p></div>
<div class="card"><h3>Using the walls</h3><p>On your side, the ball can bounce once and then hit the glass or fence; you can still play it. You may also hit the ball into your own glass to get it back over the net, but not into your own metal fence. Not sure about a call? Try the <a href="{href("wall-rules.html")}">wall and fence checker</a>.</p></div>
<div class="card"><h3>Lost points</h3><p>You lose the point if the ball bounces twice on your side, if your shot hits the opponents' wall or fence before their ground, if it hits your own fence, if the ball touches you or your partner, or if you touch the net or posts during the rally. All the net calls: <a href="{href("net-rules.html")}">net rules checker</a>.</p></div>
<div class="card"><h3>Scoring</h3><p>15, 30, 40, game, sets to six with a tie-break at 6-6 (first to 7, 2 clear): see <a href="{href("tie-break.html")}">who serves in a tie-break</a>. At deuce, the organiser chooses advantage, golden point or Star Point: <a href="{href("golden-point-star-point.html")}">see how each one works</a>.</p></div>
<div class="card"><h3>Court size</h3><p>The court is 20 m by 10 m, with the service lines 6.95 m from the net. See every measurement, in metres or feet, on our <a href="{href("court-dimensions.html")}">measured court diagram</a>.</p></div>
<div class="card"><h3>Where to stand</h3><p>Rules tell you what is allowed; position wins points. See where all four players stand at the serve, at the net and at the back on our <a href="{href("positioning.html")}">positioning guide</a>.</p></div>
<div class="card"><h3>Social formats</h3><p>At club nights you often play points, not sets: an Americano or Mexicano. Our <a href="{href("americano.html")}">draw maker</a> sets the partners, courts and leaderboard for you.</p></div>
<div class="card"><h3>Changing ends</h3><p>Change ends after games 1, 3, 5 and every odd game of a set. In a tie-break, change after every 6 points.</p></div>
</div></div></section>
<section style="padding-top:0" id="time-rules"><div class="wrap"><div class="sh"><h2>How long do you have between points in padel? The time rules</h2></div>
<p>Padel is meant to be continuous. Under the FIP rules you get <strong>20 seconds between points</strong>, <strong>90 seconds when you change ends</strong> and <strong>2 minutes between sets</strong>. Use the rest timer below at a tournament, or to keep a friendly match moving.</p>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>Moment</th><th>Time allowed (FIP)</th></tr></thead><tbody>
<tr><td>Between points</td><td>Up to 20 seconds, from the end of the point to the next serve</td></tr>
<tr><td>Change of ends (after games 1, 3, 5...)</td><td>Up to 90 seconds; no rest after game 1 of a set</td></tr>
<tr><td>Change of ends in a tie-break (every 6 points)</td><td>Quick change, no real rest</td></tr>
<tr><td>Between sets</td><td>Up to 120 seconds</td></tr>
<tr><td>Warm-up with opponents</td><td>Normally 3 minutes in FIP events (older rules said 5); then "one minute to start"</td></tr>
<tr><td>Medical time-out</td><td>3 minutes of treatment for an injury; cramp is only treated at changes of ends or set breaks</td></tr>
<tr><td>Late for the match</td><td>Not on court 10 minutes after the start time: you can lose by walkover</td></tr>
</tbody></table></div>
<div class="card" id="rt" style="margin-top:14px"><h3>Rest timer</h3><p class="muted" style="margin:4px 0 10px">Tap the break you are taking. It beeps at 5 seconds left and at zero.</p>
<div class="opts" role="group" aria-label="Break length"><button type="button" class="opt" data-v="20" aria-pressed="false">Point 20 s</button><button type="button" class="opt" data-v="90" aria-pressed="false">Ends 90 s</button><button type="button" class="opt" data-v="120" aria-pressed="false">Set 2 min</button><button type="button" class="opt" data-v="180" aria-pressed="false">Medical 3 min</button></div>
<p style="font-family:Unbounded,sans-serif;font-size:2.6rem;font-weight:800;margin:12px 0 4px" id="rt-clock" aria-live="polite">0:20</p><p class="muted" id="rt-msg" style="margin:0">Pick a break to start.</p>
<div class="btns" style="margin-top:10px"><button class="btn ghost sm" type="button" id="rt-stop">Stop</button></div></div>
<p class="muted" style="margin-top:12px;font-size:.9rem">Sources, checked 28 Nov 2026: FIP "Duties and procedures for officials" (rev. 23 Jan 2026: 20 s, 90 s, 120 s, 3-minute courtesy rally, medical rules) and the FIP / IPF Padel Game Regulations as published by the LTA (20 s, 90 s, 120 s, 3-minute treatment, 10-minute walkover). Repeated delays bring a warning and then penalties from the umpire. Club and social matches often relax these times; agree before you start.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which rule are you checking?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Question</th><th scope="col">Short answer</th><th scope="col">Check it</th></tr></thead><tbody>
<tr><td>Was my serve legal?</td><td>Underhand, at or below the waist, after one bounce, into the diagonal box</td><td><a href="{href("serve-rules.html")}">Serve checker</a></td></tr>
<tr><td>Was that ball in after the wall?</td><td>In if it bounced on the ground first; you can use your own glass but not your own fence</td><td><a href="{href("wall-rules.html")}">Wall checker</a></td></tr>
<tr><td>Can I touch the net?</td><td>No, not you, your clothes or your racket, while the ball is in play</td><td><a href="{href("net-rules.html")}">Net checker</a></td></tr>
<tr><td>What happens at 40-40?</td><td>Advantage, golden point or Star Point, as agreed</td><td><a href="{href("golden-point-star-point.html")}">Deuce formats</a></td></tr>
<tr><td>Who serves in a tie-break?</td><td>One point, then two each; change ends every 6 points</td><td><a href="{href("tie-break.html")}">Tie-break tracker</a></td></tr>
<tr><td>Can I run out of the court to play the ball?</td><td>Only on courts built for it, and before the ball bounces twice</td><td><a href="{href("out-of-court-play.html")}">Out-of-court checker</a></td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Keep score</h3><p>Put a phone by the net with the free <a href="{href("score.html")}">score keeper</a>.</p></div>
<div class="card"><h3>New to padel?</h3><p>What to bring and what to know: the <a href="{href("beginners.html")}">first match checklist</a>.</p></div>
<div class="card"><h3>Learn the words</h3><p>Bandeja, cristal, malla and more in the <a href="{href("glossary.html")}">padel glossary</a>.</p></div>
<div class="card"><h3>Where the rules came from</h3><p>The 20 x 10 m court dates back to the first court in 1969: see the <a href="{href("history-of-padel.html")}">history of padel</a>.</p></div>
</div></div></section>'''
rules_faq = [
    ("Can you serve overarm in padel?", "No. The padel serve is always underhand: you bounce the ball and hit it at or below waist height."),
    ("Can the ball hit the wall in padel?", "Yes, after it bounces on the ground on your side. If your shot hits the opponents' wall before bouncing on their ground, you lose the point."),
    ("What happens if the ball hits a player?", "The player's team usually loses the point, with only a few exceptions in the official rules."),
    ("How high is a padel net?", "88 cm in the middle and 92 cm at the posts."),
    ("Where must the server stand?", "Behind the service line, which is 6.95 m from the net, between the centre line and the side wall, serving diagonally into the opposite service box."),
    ("What is a let in padel?", "A serve that touches the net and then lands in the correct box without touching the metal fence. The serve is replayed. A let on the second serve replays only the second serve."),
    ("Can you play the ball off your own fence in padel?", "No. You may hit the ball into your own glass to send it back over the net, but if your shot hits the metal fence on your side you lose the point."),
    ("What happens at 6-6 in padel?", "A tie-break: first to 7 points with a 2-point lead. One player serves the first point, then each player serves two points in turn, and you change ends every 6 points. The set ends 7-6."),
    ("When do you change ends in padel?", "After the 1st, 3rd and every odd game of a set, and after every 6 points in a tie-break."),
    ("Is a net cord in play during a padel rally?", "Yes. In a rally a ball that touches the net and lands on the other side is in play. Only on the serve does a net touch mean a let."),
    ("How long do you have between points in padel?", "Up to 20 seconds under FIP rules, 90 seconds when you change ends and 2 minutes between sets. There is no rest at the change after the first game of a set."),
    ("How long is a medical time-out in padel?", "3 minutes of treatment for an injury. Cramp cannot get a medical time-out; it can only be treated at changes of ends or between sets."),
    ("How long is the warm-up before a padel match?", "In FIP events the warm-up with your opponents is normally 3 minutes. At clubs, agree it before you start; 5 minutes is common."),
]
page("rules.html", "Padel Rules (Padel Tennis) Explained: Scoring, Serve, Walls",
     "Padel rules in plain English: the underhand serve, walls, net, faults, scoring, tie-breaks and changing ends, plus an interactive court to tap and learn.", rules, rules_faq, "Rules")

# ---------------- SHOTS ----------------
PATHS = {
    "flat": "M20 70 C80 60 140 58 210 64", "high": "M20 90 C70 -10 160 -10 220 80", "wall-back": "M215 90 L232 72 C180 20 120 30 30 70",
    "slice": "M30 20 C90 30 150 60 215 88", "dip": "M20 80 C80 40 130 50 210 92", "spin": "M30 18 C100 30 160 70 215 70",
    "kick": "M30 20 C100 40 170 90 200 60 L225 40", "wall-attack": "M215 90 L232 60 C190 25 120 40 30 30", "down": "M30 15 C100 40 160 80 210 96", "drop": "M20 70 C70 40 100 50 120 95",
}
LV = {"Beginner": "b", "Intermediate": "i", "Advanced": "a"}
shot_cards = ""
for s in D["shots"]:
    pth = PATHS[s["path"]]
    shot_cards += f'''<article class="card shot" data-level="{s["level"]}"><svg viewBox="0 0 240 110" aria-hidden="true"><rect width="240" height="110" fill="#1d55e6"/><path d="M120 60v50" stroke="#f4f6f1" stroke-width="5"/><path d="M0 100h240" stroke="#fff" stroke-width="2"/><rect x="232" y="20" width="8" height="90" fill="#8fd3ff"/><rect x="0" y="20" width="8" height="90" fill="#8fd3ff"/><path class="path" d="{pth}"/><circle class="sball" r="6"><animateMotion dur="2.4s" repeatCount="indefinite" path="{pth}"/></circle></svg>
<span class="pill {LV[s["level"]]}" style="margin-top:12px">{s["level"]} · {s["where"]}</span><h3>{e(s["name"])}</h3><p>{e(s["text"])}</p><div class="tip"><strong>Tip:</strong> {e(s["tip"])}</div></article>'''
shots = f'''<header class="hero"><div class="wrap"><h1>Every padel shot, explained.</h1>
<p class="lead">What each shot is for, when to play it, and one tip to get it right. Each card shows the ball's path, with the net in the middle and the glass at the ends.</p>
{quick("There are 10 key padel shots. Learn them in this order: volley and lob first, then the bandeja, chiquita, contrapared and drop shot, and finally the víbora, bajada, rulo and smash. Most points are won with safe volleys, lobs and bandejas, not big smashes.")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<div class="filters seg" id="shot-filter" role="group" aria-label="Filter shots by level" style="background:#fff;border:1px solid var(--line)"><button type="button" data-v="all" aria-pressed="true" style="color:var(--ink)">All</button><button type="button" data-v="Beginner" aria-pressed="false" style="color:var(--ink)">Beginner</button><button type="button" data-v="Intermediate" aria-pressed="false" style="color:var(--ink)">Intermediate</button><button type="button" data-v="Advanced" aria-pressed="false" style="color:var(--ink)">Advanced</button></div>
<div class="grid">{shot_cards}</div></div></section>
{AD.format("shots-mid")}
<section><div class="wrap"><div class="sh"><h2>Which padel shots should I learn first?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Stage</th><th scope="col">Shots</th><th scope="col">Why</th></tr></thead><tbody>
<tr><td>1. First weeks</td><td><a href="{href("padel-volley.html")}">Volley</a>, <a href="{href("padel-lob.html")}">lob (globo)</a>, <a href="{href("padel-return-of-serve.html")}">return of serve</a></td><td>The lob gets you to the net; the volley keeps you there.</td></tr>
<tr><td>2. Playing regular matches</td><td>Bandeja, <a href="{href("padel-chiquita.html")}">chiquita</a>, contrapared, drop shot</td><td>Safe ways to keep the net and to escape when you are pushed back.</td></tr>
<tr><td>3. Strong club level</td><td>Víbora, <a href="{href("padel-back-glass.html")}">bajada</a>, rulo, <a href="{href("padel-smash.html")}">smash (x3, x4)</a></td><td>Attacking shots. Play them when the ball is right, not every time.</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What makes padel shots different from tennis?</h2></div><div class="grid">
<div class="card"><h3>Shorter swings</h3><p>The court is small and the ball comes back off the glass, so compact swings and control beat raw power.</p></div>
<div class="card"><h3>Let it come off the glass</h3><p>Many balls are easier after the back glass. Wait for the rebound instead of rushing: <a href="{href("padel-back-glass.html")}">how to play off the back glass</a>. The <a href="{href("wall-rules.html")}">wall rules checker</a> shows what is in and out.</p></div>
<div class="card"><h3>Overheads that keep the net</h3><p>The bandeja and víbora are not smashes. Their job is to keep your team at the net, so placement matters more than pace. Not sure which one to play? Try the <a href="{href("bandeja-vs-vibora.html")}">overhead chooser</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Shot keeps going wrong?</h3><p>Pick the problem in the <a href="{href("fix-my-padel.html")}">padel problem fixer</a> and get three fixes and a drill.</p></div>
<div class="card"><h3>Stand in the right place</h3><p>Good shots start with good positions. See the <a href="{href("positioning.html")}">positioning guide</a>.</p></div>
<div class="card"><h3>Learn the words</h3><p>Bandeja, víbora, chiquita and more, with pronunciation, in the <a href="{href("glossary.html")}">padel glossary</a>.</p></div>
<div class="card"><h3>Match your racket</h3><p>Control or power? The <a href="{href("racket-finder.html")}">racket finder</a> picks a shape for your game.</p></div>
<div class="card"><h3>Practise the shots</h3><p>Turn these shots into a timed practice plan for one, two or four players with the <a href="{href("drills.html")}">padel drills planner</a>.</p></div>
</div></div></section>'''
shots_faq = [
    ("What is a bandeja in padel?", "A controlled overhead with slice, played after a lob. Its job is to keep your team at the net, not to win the point outright."),
    ("What's the difference between a bandeja and a víbora?", "Both are overheads, but the víbora adds sidespin and pace to attack, while the bandeja is safer and about placement. Learn the bandeja first."),
    ("What is a chiquita?", "A soft, low ball from the back of the court that drops at the net players' feet, so your team can move forward."),
    ("What is a rulo?", "A topspin smash aimed across the court at the side fence, where the ball bounces unpredictably."),
    ("Which padel shot should a beginner learn first?", "The volley and the lob. The lob moves the other team back so you can take the net, and the volley is how you win points once you are there."),
    ("What is a contrapared in padel?", "A shot where you hit the ball into your own back or side glass so it travels over the net. It is an escape shot when the ball has got past you."),
    ("Is the smash or the bandeja better in padel?", "Most of the time the bandeja. A smash that is not a clear winner often comes back off the glass, while a bandeja keeps your team at the net."),
]
page("shots.html", "Padel Shots Explained: Bandeja, Víbora, Chiquita and More | Padel Glass Box",
     "Every key padel shot explained simply with animated ball paths: volley, lob, bandeja, chiquita, contrapared, víbora, rulo, bajada and smash.", shots, shots_faq, "Shots")

# ---------------- BEGINNERS ----------------
kit = ["A padel racket (a round one is easiest to start with)", "Padel balls, not tennis balls (they have less pressure)", "Court shoes with good grip for artificial grass", "A wrist strap on your racket, and wear it", "Comfortable sports clothes and water", "A booked court and three other players"]
know = ["Serve underhand, below the waist, diagonally", "Let the ball bounce once, then it can hit your walls", "Never let your shot hit their wall before the ground", "Agree on advantage or golden point before you start", "Stay with your partner: move up and back together", "When in doubt, lob and go to the net"]
def checklist(name, items):
    return f'<div class="prog"><i id="{name}-bar"></i></div><p class="muted" id="{name}-count" style="margin:-8px 0 12px"></p><ul class="check" data-check="{name}">' + "".join(f'<li><label><input type="checkbox"><span>{e(x)}</span></label></li>' for x in items) + "</ul>"
beg = f'''<header class="hero"><div class="wrap"><h1>Your first padel match.</h1>
<p class="lead">Tick these off and you'll walk onto court ready. Your ticks are saved on this device.</p>
{quick("For your first padel match you need a padel racket (clubs often rent them), padel balls, court shoes with grip, sports clothes and water, plus a booked court and three other players. Know four rules: serve underhand and diagonally, let the ball bounce once on your side, never hit their wall before their ground, and agree the 40-40 rule before you start.")}</div></header>
<section style="padding-top:10px"><div class="wrap grid" style="grid-template-columns:repeat(auto-fit,minmax(320px,1fr))">
<div class="card"><h2 style="font-size:1.6rem">What do you need for your first padel match?</h2>{checklist("kit", kit)}</div>
<div class="card"><h2 style="font-size:1.6rem">What rules do beginners need to know?</h2>{checklist("know", know)}</div>
</div></section>
{AD.format("beg-mid")}
<section><div class="wrap"><div class="sh"><h2>Where can beginners play padel, and what helps?</h2></div><div class="grid">
<div class="card"><h3>Booking apps</h3><p>Many clubs list their courts on booking apps such as Playtomic, where you can also find open matches at your level. Compare them in <a href="{href("padel-booking-apps.html")}">padel booking apps</a>.</p></div>
<div class="card"><h3>National federations</h3><p>Your country's padel or tennis federation usually lists clubs and beginner sessions. In the UK, that's LTA Padel.</p></div>
<div class="card"><h3>Join a social night</h3><p>Many clubs run Americano evenings where you change partner each round. They are a friendly way to meet players at your level. Running one yourself? Use our <a href="{href("americano.html")}">Americano generator</a>.</p></div>
<div class="card"><h3>Practise between matches</h3><p>A short practice once a week speeds things up. The <a href="{href("drills.html")}">drills planner</a> builds a 20 to 60 minute session with a timer.</p></div>
<div class="card"><h3>Know your level</h3><p>Open matches and clubs often ask for your level. Our <a href="{href("level-calculator.html")}">padel level calculator</a> gives you a quick estimate.</p></div>
<div class="card"><h3>Know where to stand</h3><p>Move up and back with your partner, and stay about 1 metre off the back glass. Our <a href="{href("positioning.html")}">positioning guide</a> shows every situation on a court.</p></div>
<div class="card"><h3>Warm up first</h3><p>Ten minutes of jogging, moving stretches and soft rallies makes the first games easier on your body. Our <a href="{href("warm-up.html")}">warm-up timer</a> talks you through it step by step.</p></div>
<div class="card"><h3>Coming from tennis or pickleball?</h3><p>Your hands will help, but the walls, the underhand serve and the scoring work a little differently. See <a href="{href("padel-vs-racquetball.html")}">padel vs racquetball and platform tennis</a> or <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a> for the key changes.</p></div>
<div class="card"><h3>Pick the right shoes</h3><p>Grip matters more than looks. A herringbone sole suits most sandy courts, and running shoes slip. Our <a href="{href("padel-shoes.html")}">padel shoe finder</a> tells you which sole to look for.</p></div>
<div class="card"><h3>Is it a good workout?</h3><p>An hour of padel burns roughly 400 to 600 kcal for an average adult. Work out your own number with the <a href="{href("padel-calories.html")}">padel calories calculator</a>.</p></div>
<div class="card"><h3>Start with a lesson</h3><p>One group lesson teaches the serve and the walls much faster than working it out alone.</p></div>
<div class="card"><h3>Follow a 30-day plan</h3><p>One short task a day for your first month, with court sessions and rest days: the <a href="{href("padel-beginner-plan.html")}">30-day padel beginner plan</a>.</p></div>
<div class="card"><h3>What will it cost?</h3><p>Court hire is usually split four ways. Work out your cost per game and per month with the <a href="{href("padel-cost.html")}">padel cost calculator</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What mistakes do new padel players make?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Mistake</th><th scope="col">Try this instead</th><th scope="col">Read more</th></tr></thead><tbody>
<tr><td>Hitting the ball before it reaches the back glass</td><td>Let it bounce and come off the glass, then play it</td><td><a href="{href("wall-rules.html")}">Wall rules</a></td></tr>
<tr><td>Serving overhead like in tennis</td><td>Bounce the ball and hit it at or below waist height</td><td><a href="{href("serve-rules.html")}">Serve checker</a></td></tr>
<tr><td>Hitting every ball hard</td><td>Keep the ball in play; a lob often wins more points than a smash</td><td><a href="{href("shots.html")}">Shot library</a></td></tr>
<tr><td>Standing far apart from your partner</td><td>Move up and back together, like a pair joined by a rope</td><td><a href="{href("positioning.html")}">Where to stand</a></td></tr>
<tr><td>Both going for the ball in the middle</td><td>Agree who takes it and call "mine" early</td><td><a href="{href("glossary.html")}">Court calls</a></td></tr>
<tr><td>Running out of the court for a ball</td><td>Only where the court and club allow it</td><td><a href="{href("out-of-court-play.html")}">Out-of-court play</a></td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Keep improving</h3><p>What to learn next at your level: <a href="{href("padel-improvement-guide.html")}">how to get better at padel</a>.</p></div>
<div class="card"><h3>Avoid beginner mistakes</h3><p>See the ten most common padel mistakes and their fixes in the <a href="{href("fix-my-padel.html")}">problem fixer</a>.</p></div>
<div class="card"><h3>Keep score</h3><p>Not sure how scoring works? Use the free <a href="{href("score.html")}">score keeper</a> on your phone.</p></div>
<div class="card"><h3>Find your racket</h3><p>Three questions and you'll know the shape and weight to look for: <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
<div class="card"><h3>Learn the rules</h3><p>Tap any part of the <a href="{href("rules.html")}">interactive rules court</a>.</p></div>
<div class="card"><h3>Pack your bag</h3><p>Get a packing list and what to wear for your game: <a href="{href("padel-equipment.html")}">padel equipment checklist</a>.</p></div>
<div class="card"><h3>Know the etiquette</h3><p>No smashing in the warm-up, and call your own double bounces: <a href="{href("padel-etiquette.html")}">padel etiquette and quiz</a>.</p></div>
<div class="card"><h3>Book a first lesson</h3><p>See typical prices and what a first lesson covers: <a href="{href("padel-lessons.html")}">padel lessons guide and cost checker</a>.</p></div>
</div></div></section>'''
beg_faq = [
    ("What do I need for my first padel game?", "A racket, padel balls, court shoes with grip, comfy sports clothes and water. Many clubs rent rackets if you don't have one yet."),
    ("Can I use tennis balls for padel?", "It's better not to. Padel balls have less pressure inside (about 11 psi against 14 psi for tennis, according to LTA Padel), so they bounce lower and play the way padel should."),
    ("How should I warm up for padel?", "Spend 10 to 15 minutes on an easy jog, moving stretches, a few squats and lunges, then soft rallies, volleys, lobs and serves. Save long, held stretches for after you play."),
    ("Do I need special shoes for padel?", "Tennis shoes are fine to start. Padel shoes with a herringbone sole grip sandy artificial grass best; running shoes slip and give little side support."),    ("Do I need to own a racket to start padel?", "No. Many clubs rent rackets, so you can try a few before you buy. When you do buy, a round shape with a medium weight is the easiest to start with."),
    ("What are the most important padel rules for beginners?", "Serve underhand and diagonally, let the ball bounce once on your side before it hits your walls, make sure your shot lands on their ground before their walls, and don't touch the net."),
    ("Can you leave the court to play the ball in padel?", "Only on courts built for out-of-court play and when the club allows it. Otherwise, a ball that bounces on your side and leaves the court is a point for the other team."),
]
page("beginners.html", "Padel for Beginners: First Match Checklist | Padel Glass Box",
     "Padel for beginners: what to bring to your first match, the four rules to know, common mistakes and where to play. Tick-off checklists saved on your phone.", beg + f'''<section><div class="wrap"><div class="aff-box"><h3>Shop padel gear</h3><p>Browse rackets by shape, plus the shoes, balls and grips you need for your first match.</p><ul class="aff-links"><li><a href="/go/padel-round-rackets" rel="sponsored nofollow noopener" target="_blank">Round rackets</a></li><li><a href="/go/padel-teardrop-rackets" rel="sponsored nofollow noopener" target="_blank">Teardrop rackets</a></li><li><a href="/go/padel-diamond-rackets" rel="sponsored nofollow noopener" target="_blank">Diamond rackets</a></li><li><a href="/go/padel-shoes" rel="sponsored nofollow noopener" target="_blank">Padel shoes</a></li><li><a href="/go/padel-balls" rel="sponsored nofollow noopener" target="_blank">Balls</a></li><li><a href="/go/padel-bags" rel="sponsored nofollow noopener" target="_blank">Bags</a></li><li><a href="/go/padel-overgrips" rel="sponsored nofollow noopener" target="_blank">Overgrips</a></li></ul>{AFF_NOTE}</div></div></section>''', beg_faq, "Beginners")

# ---------------- GLOSSARY ----------------
GL_LINK = {"Bandeja": "shots.html", "Víbora": "shots.html", "Chiquita": "shots.html", "Bajada": "shots.html", "Golden point": "golden-point-star-point.html", "Star Point": "golden-point-star-point.html",
           "Saque": "serve-rules.html", "Let": "serve-rules.html", "Salida de pista": "out-of-court-play.html", "Contrapared": "wall-rules.html", "Malla": "wall-rules.html", "Americano": "americano.html",
           "Mexicano": "americano.html", "Round robin": "round-robin.html", "Overgrip": "racket-finder.html", "Herringbone sole": "padel-shoes.html", "Drive": "positioning.html", "Revés": "positioning.html"}
GL_CATS = ["Shots", "Court", "Scoring", "Players", "Formats", "Gear"]
def _gl(r):
    t, d, say, lit, cat = r
    extra = (f'<i class="gl-say">Say it: {e(say)}</i>' if say else "") + (f'<i class="gl-lit">Means: “{e(lit)}”</i>' if lit else "")
    more = f' <a href="{href(GL_LINK[t])}">More</a>' if t in GL_LINK else ""
    return f'<div data-cat="{cat}"><b>{e(t)}</b><span class="pill">{cat}</span>{extra}<span>{e(d)}{more}</span></div>'
gl = "".join(_gl(r) for r in D["glossary"])
gl_spanish = sum(1 for r in D["glossary"] if r[2])
glos = f'''<header class="hero"><div class="wrap"><h1>Padel words, decoded.</h1>
<p class="lead">Padel borrows lots of Spanish. Search any word you've heard on court, see how to say it, and what it means in English.</p>
{quick(f"The padel words you'll hear most are bandeja (a controlled overhead, said ban-DEH-ha), víbora (a spin smash, VEE-bo-ra), chiquita (a soft low ball, chee-KEE-ta), globo (a lob), pared (wall) and malla (the metal fence, MAH-ya). This glossary has {len(D['glossary'])} terms, {gl_spanish} of them Spanish with a simple way to say each one.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><label class="sr-only" for="gsearch">Search the glossary</label><input class="search" id="gsearch" type="search" placeholder="Search: bandeja, golden point, malla...">
<div class="seg gl-seg" id="gcat" role="group" aria-label="Filter by type"><button type="button" data-v="" aria-pressed="true">All</button>{"".join(f'<button type="button" data-v="{c}" aria-pressed="false">{c}</button>' for c in GL_CATS)}</div>
<p class="muted" id="gcount" aria-live="polite"></p><div class="gl" id="glist">{gl}</div>
<p class="muted" style="margin-top:16px">How to read the sounds: the part in capitals is stressed. In Spanish a "v" sounds close to a soft "b", "j" and "g" before e or i sound like the "h" in "hat", and "ll" sounds like the "y" in "yes" in most of Spain. Accents vary between countries, so you will hear small differences on court.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which Spanish padel words should beginners learn first?</h2></div><div class="grid">
<div class="card"><h3>Calls on court</h3><p><b>Mía</b> (MEE-a, "mine") and <b>tuya</b> (TOO-ya, "yours") tell your partner who takes the ball. <b>Fuera</b> (FWEH-ra) means out. Short, clear calls stop both of you going for the same ball.</p></div>
<div class="card"><h3>The shots you'll hear</h3><p>Bandeja, víbora, globo, chiquita and bajada. See each one move in the <a href="{href("shots.html")}">shot library</a>.</p></div>
<div class="card"><h3>The court</h3><p>Pared and cristal for the glass, malla for the fence, and red (RED) for the net. The <a href="{href("wall-rules.html")}">wall rules checker</a> shows which ones you can use.</p></div>
</div></div></section>
<section style="padding-top:0" id="pronounce"><div class="wrap"><div class="sh"><h2>How do you pronounce padel?</h2></div>
<p>In English most people say <b>PAD-uhl</b>, the same as "paddle". Merriam-Webster lists two ways: PAD-uhl and puh-DEL, and Dictionary.com gives PAD-uhl for American English. In Spanish, where the game grew up, it is <b>pádel</b>, said <b>PAH-del</b>, with a short "a" as in "father" and the stress on the first part. Both are fine on court.</p>
<div class="card" id="pron" style="margin-top:14px"><h3>Hear it</h3><div class="btns" style="margin-top:8px"><button class="btn sm lime" type="button" data-say="paddle" data-lang="en-GB">English: PAD-uhl</button><button class="btn sm ghost" type="button" data-say="pádel" data-lang="es-ES">Spanish: PAH-del</button></div><p class="muted" id="pron-note" style="margin-top:8px;font-size:.9rem">Uses your device's own voice, so it can sound slightly different on each phone.</p></div>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>Word</th><th>Say it</th><th>Note</th></tr></thead><tbody>
<tr><td>Padel (English)</td><td>PAD-uhl</td><td>Sounds like "paddle". Most common in the UK and US.</td></tr>
<tr><td>Padel (also heard)</td><td>puh-DEL</td><td>Stress on the end. Listed by Merriam-Webster.</td></tr>
<tr><td>Pádel (Spanish)</td><td>PAH-del</td><td>Stress on the first part, written with an accent.</td></tr>
<tr><td>Paddle tennis</td><td>PAD-uhl TEN-is</td><td>A different US sport. Padel is not spelled "paddle".</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px;font-size:.9rem">Why the spelling: Merriam-Webster and Wiktionary say the English word "padel" was borrowed from Spanish pádel, which itself came from the English "paddle" (as in paddle tennis). Checked 27 Nov 2026: Merriam-Webster "padel", Dictionary.com "padel", Wiktionary "padel". More on where the game began: <a href="{href("history-of-padel.html")}">history of padel</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Learn the rules</h3><p>Tap any part of the <a href="{href("rules.html")}">interactive rules court</a>.</p></div>
<div class="card"><h3>Find your side</h3><p>Drive or revés? Take the <a href="{href("which-side-padel.html")}">left or right side quiz</a> and read <a href="{href("positioning.html")}">where to stand</a>.</p></div>
<div class="card"><h3>New to padel?</h3><p>Start with the <a href="{href("beginners.html")}">first match checklist</a>.</p></div>
<div class="card"><h3>Why the Spanish words?</h3><p>Padel was born in Mexico and grew up in Spain and Argentina. See the <a href="{href("history-of-padel.html")}">history of padel timeline</a>.</p></div>
</div></div></section>'''
glos_faq = [
    ("How do you pronounce padel?", "In English most people say PAD-uhl, like paddle; puh-DEL is also heard. In Spanish it is pádel, said PAH-del, with the stress on the first part."),
    ("Why is it spelled padel and not paddle?", "The English word was borrowed from Spanish pádel, which came from the English paddle (as in paddle tennis). Padel and paddle tennis are now different sports."),
    ("How do you pronounce bandeja in padel?", "Say ban-DEH-ha. The Spanish j sounds like the h in hat. Bandeja means tray, because you hold the racket face up like a waiter's tray."),
    ("How do you pronounce víbora?", "Say VEE-bo-ra, with the stress on the first part. In Spanish the v sounds close to a soft b, so you will also hear BEE-bo-ra."),
    ("What does mía and tuya mean in padel?", "Mía means mine and tuya means yours. Partners shout them to say who will take a ball down the middle."),
    ("What is the difference between a bandeja and a víbora?", "Both are overheads played from near the net. A bandeja is flatter and controlled to keep your place at the net; a víbora has more sidespin and speed and is more attacking."),
    ("What does malla mean in padel?", "Malla is the metal mesh fence around the sides of the court. Balls that hit it bounce unpredictably, and you can't play off your own fence."),
    ("What are drive and revés in padel?", "Drive is the player on the right side of the court and revés is the player on the left. In Spanish the words also mean forehand and backhand."),
]
page("glossary.html", "Padel Glossary: Terms, Spanish Pronunciation and Meanings | Padel Glass Box",
     "Padel terms in plain English, how to pronounce padel and the Spanish words: bandeja, víbora, chiquita, bajada, malla, golden point and more. Searchable.", glos, glos_faq, "Glossary")

# ---------------- AMERICANO / MEXICANO GENERATOR ----------------
def pts_opts():
    return "".join(f'<button class="opt" type="button" data-v="{p}" aria-pressed="{"true" if p == 24 else "false"}">{p} points</button>' for p in (16, 21, 24, 32))
amer = f'''<header class="hero"><div class="wrap"><h1>Americano and Mexicano draw maker.</h1>
<p class="lead">Type in your players, pick a format and get every round with partners and courts. Enter the points after each match and the leaderboard updates live. Free, no sign-up, saved on this device.</p>
{quick("An Americano is a social padel format for 4 or more players: you change partner every round, each match is a fixed number of points (often 16, 21, 24 or 32) and you keep every point you win. The highest total wins. A Mexicano works the same way, but only round 1 is random: each later round is drawn from the leaderboard, usually 1st and 4th against 2nd and 3rd on court 1, so similar players meet. Seven rounds of 24 points fit about a two-hour booking.")}</div></header>
<section style="padding-top:10px"><div class="wrap gen">
<div class="gen-main">
<div class="card" id="mx-setup">
<h2 style="font-size:1.6rem">Set up your session</h2>
<div class="q"><h3>Format</h3><div class="opts" data-mx="fmt" role="group" aria-label="Format"><button class="opt" type="button" data-v="americano" aria-pressed="true">Americano</button><button class="opt" type="button" data-v="mexicano" aria-pressed="false">Mexicano</button></div><p class="muted" id="mx-fmt-note" style="margin:10px 0 0"></p></div>
<div class="q"><h3>Points per match</h3><div class="opts" data-mx="pts" role="group" aria-label="Points per match">{pts_opts()}</div></div>
<div class="q"><h3><label for="mx-names">Players, one name per line (4 to 24)</label></h3><textarea class="search" id="mx-names" rows="8" placeholder="Sam&#10;Priya&#10;Omar&#10;Lucia&#10;..."></textarea><p class="muted" id="mx-count" style="margin:-6px 0 0"></p></div>
<div class="gen-nums"><div class="q"><h3><label for="mx-courts">Courts</label></h3><input class="search" id="mx-courts" type="number" min="1" max="6" value="1" inputmode="numeric"></div>
<div class="q" id="mx-rounds-q"><h3><label for="mx-rounds">Rounds</label></h3><input class="search" id="mx-rounds" type="number" min="1" max="30" value="7" inputmode="numeric"></div></div>
<p class="msg" id="mx-err" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:4px"><button class="btn lime" type="button" id="mx-start">Make the draw</button><button class="btn ghost" type="button" id="mx-demo">Fill 8 sample names</button></div>
</div>
<div id="mx-live" hidden>
<div class="card gen-bar"><div><span class="pill b" id="mx-sum"></span></div><div class="btns" style="margin:0"><button class="btn ghost sm" type="button" id="mx-copy">Copy results</button><button class="btn ghost sm" type="button" id="mx-new">New session</button></div></div>
<div id="mx-rounds-list"></div>
<div class="btns"><button class="btn" type="button" id="mx-next">Add next round</button></div>
</div>
</div>
<aside class="gen-side"><div class="lb" id="mx-board"><h2>Leaderboard</h2><p>Make the draw and enter scores to see who leads.</p></div></aside>
</div></section>
{AD.format("americano-mid")}
<section><div class="wrap"><div class="sh"><h2>How do Americano and Mexicano work?</h2></div><div class="grid">
<div class="card"><h3>Americano</h3><p>You change partner every round. The aim is that you play with, and against, as many different people as possible. Nobody is knocked out.</p></div>
<div class="card"><h3>Mexicano</h3><p>Round one is random. After that, each round is made from the leaderboard, so players with similar scores meet. A common way, used here, is 1st and 4th against 2nd and 3rd on the top court, then the next four, and so on.</p></div>
<div class="card"><h3>Points, not games</h3><p>Each match is a fixed number of points, such as 24. Every point counts, even if your team loses: lose 10-14 and you still add 10 to your total. The player with the most points at the end wins.</p></div>
<div class="card"><h3>Serving</h3><p>A simple rule many clubs use: each player serves a block of points (often four in a row for 16, 24 or 32 points), then the serve passes to the other team. Agree the rule before you start.</p></div>
<div class="card"><h3>Odd numbers of players</h3><p>It works best with 4, 8, 12 or 16 players. With other numbers, some players sit out each round. This tool spreads the rests as evenly as it can, and the leaderboard shows points per match so it stays fair.</p></div>
<div class="card"><h3>Want more competition?</h3><p>Try <a href="{href("king-of-the-court.html")}">King of the Court</a>: winners move up a court, losers move down, and everyone fights for court 1.</p></div>
<div class="card"><h3>Playing in fixed pairs?</h3><p>If teams want to keep the same partner all night, use the <a href="{href("round-robin.html")}">round robin generator</a>: every pair plays every other pair, with a standings table.</p></div>
<div class="card"><h3>How long it takes</h3><p>A 24-point match often takes around 10 to 15 minutes, and 32 points a bit longer. Seven rounds of 24 points fits a typical two-hour court booking with time for changes.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How does Mexicano pick the next round?</h2><p class="muted">An example with 8 players on 2 courts after round 1.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Leaderboard place</th><th scope="col">Round 2 court</th><th scope="col">Team</th></tr></thead><tbody>
<tr><td>1st and 4th</td><td>Court 1</td><td>Team A</td></tr>
<tr><td>2nd and 3rd</td><td>Court 1</td><td>Team B</td></tr>
<tr><td>5th and 8th</td><td>Court 2</td><td>Team A</td></tr>
<tr><td>6th and 7th</td><td>Court 2</td><td>Team B</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Pairing the top player with the 4th keeps each match close. Some clubs use other pairings (such as 1st and 3rd against 2nd and 4th); agree the rule before you start. The tool above uses 1st and 4th against 2nd and 3rd.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which social format should you pick?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Format</th><th scope="col">Partners</th><th scope="col">Best for</th></tr></thead><tbody>
<tr><td>Americano</td><td>Change every round, planned</td><td>Mixing a group that doesn't know each other</td></tr>
<tr><td>Mexicano</td><td>Change every round, by score</td><td>Mixed levels: close games as the night goes on</td></tr>
<tr><td><a href="{href("king-of-the-court.html")}">King of the Court</a></td><td>Change every round</td><td>Competitive nights on 2 or more courts</td></tr>
<tr><td><a href="{href("round-robin.html")}">Round robin</a></td><td>Fixed pairs</td><td>Teams that want to play together all night</td></tr><tr><td><a href="{href("padel-tournament-bracket.html")}">Knockout bracket</a></td><td>Fixed pairs</td><td>A quick winner with lots of pairs</td></tr>
<tr><td><a href="{href("ladder.html")}">Ladder</a></td><td>Fixed pairs or players</td><td>A league that runs for weeks</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Players of mixed level?</h3><p>Ask everyone to try the <a href="{href("level-calculator.html")}">level calculator</a>, then play Mexicano so levels sort themselves out.</p></div>
<div class="card"><h3>Warm up first</h3><p>Start the night with the <a href="{href("warm-up.html")}">10-minute warm-up timer</a> on court.</p></div>
<div class="card"><h3>Bring the right kit</h3><p>Fresh balls for every court make a big difference: see the <a href="{href("padel-equipment.html")}">equipment checklist</a> and <a href="{href("padel-balls.html")}">when balls are dead</a>.</p></div>
</div></div></section>'''
amer_faq = [
    ("What is an Americano in padel?", "A social format where you change partner every round and play a set number of points per match. Each player keeps the points they win, and the highest total at the end wins."),
    ("What is the difference between Americano and Mexicano?", "In Americano the partners are planned in advance so everyone mixes. In Mexicano each new round is built from the current scores, so players of a similar level end up playing together."),
    ("How many players do you need for an Americano?", "At least four. Multiples of four (8, 12, 16) fill every court in every round. Other numbers work too, with a few players resting each round."),
    ("How many points per match in an Americano?", "Clubs often use 16, 21, 24 or 32. Fewer points means quicker matches and more rounds in the same court time."),
    ("Do you need an app to run an Americano?", "No. This page makes the draw, keeps the scores and shows the leaderboard in your browser. It saves on your device, so you can close it and come back."),
    ("How are teams picked in Mexicano padel?", "Round one is random. After each round the players are ranked by total points, and the top four play on court 1 with 1st and 4th against 2nd and 3rd. The next four play on court 2 the same way, and so on."),
    ("Who wins a padel Americano?", "The player with the most points in total after the last round. If players have played a different number of matches because of rests, compare points per match."),
    ("How long does a padel Americano take?", "It depends on the points per match and the number of rounds. Seven rounds of 24 points usually fits a two-hour court booking, with short breaks to change partners."),
]
page("americano.html", "Padel Americano and Mexicano Generator: Draw + Leaderboard",
     "Free padel Americano and Mexicano generator for 4 to 24 players: every round with partners and courts, points entry, a live leaderboard and format tips.", amer, amer_faq, "Americano generator")

# ---------------- COURT DIMENSIONS ----------------
def dt(m, x, y, extra=""):
    return f'<text class="dt" data-m="{m}" x="{x}" y="{y}" text-anchor="middle"{extra}>{m} m</text>'
def arrow(x1, y1, x2, y2):
    return f'<path class="da" d="M{x1} {y1}L{x2} {y2}" marker-start="url(#ah)" marker-end="url(#ah)"/>'
TOP = f'''<svg viewBox="0 0 1000 600" role="img" aria-label="Padel court seen from above with its measurements: 20 metres long, 10 metres wide, service lines 6.95 metres from the net.">
<defs><marker id="ah" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L9 5L0 9z" fill="#e8f84a"/></marker></defs>
<rect x="100" y="110" width="800" height="400" fill="#1e46c8"/>
<g stroke="#fff" stroke-width="3" fill="none"><rect x="100" y="110" width="800" height="400"/><path d="M222 110v400M778 110v400M214 310h572"/></g>
<g stroke="#9cc4ea" stroke-width="10"><path d="M100 105v410M900 105v410M100 105h160M740 105h160M100 515h160M740 515h160"/></g>
<g stroke="#7a8ba8" stroke-width="6" stroke-dasharray="4 5"><path d="M260 105h480M260 515h480"/></g>
<path d="M500 100v420" stroke="#e4eef6" stroke-width="7"/>
<g class="dim" data-k="len">{arrow(104, 560, 896, 560)}{dt(20, 500, 590)}</g>
<g class="dim" data-k="wid">{arrow(55, 114, 55, 506)}{dt(10, 40, 310, ' transform="rotate(-90 40 310)"')}</g>
<g class="dim" data-k="svc">{arrow(504, 70, 774, 70)}{dt(6.95, 639, 55)}</g>
<g class="dim" data-k="back">{arrow(782, 70, 896, 70)}{dt(3.05, 839, 55)}</g>
<g class="dim" data-k="box">{arrow(360, 116, 360, 304)}{dt(5, 400, 215)}</g>
<g class="dim" data-k="glassl">{arrow(104, 30, 256, 30)}{dt(4, 180, 22)}</g>
<g class="dim" data-k="ext">{arrow(222, 330, 214, 330)}<text class="dt" data-m="0.2" x="232" y="360">0.2 m</text></g>
<text x="500" y="135" text-anchor="middle" class="lab">net</text>
<text x="161" y="300" text-anchor="middle" class="lab">back area</text><text x="361" y="420" text-anchor="middle" class="lab">service box</text>
</svg>'''
SIDE = f'''<svg viewBox="0 0 1000 300" role="img" aria-label="Side view of the padel court walls: 3 metre glass at the back, stepping down to 2 metres, with metal mesh in the middle. The back wall is 4 metres high in total.">
<path d="M60 250h880" stroke="#fff" stroke-width="2" opacity=".7"/>
<g fill="#9cc4ea" fill-opacity=".45" stroke="#9cc4ea" stroke-width="2"><path d="M100 250V130H180V170H260V250Z"/><path d="M900 250V130H820V170H740V250Z"/></g>
<g fill="url(#mesh)" stroke="#7a8ba8" stroke-width="2"><path d="M180 130H820V170H740V250H260V170H180Z"/></g>
<defs><pattern id="mesh" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M0 0L10 10M10 0L0 10" stroke="#7a8ba8" stroke-width="1" opacity=".7"/></pattern></defs>
<g stroke-width="8"><path d="M100 250V130M900 250V130" stroke="#9cc4ea"/><path d="M100 130V90M900 130V90" stroke="#7a8ba8" stroke-dasharray="4 4"/></g>
<path d="M500 250V213" stroke="#e4eef6" stroke-width="6"/>
<g class="dim" data-k="glass3">{arrow(140, 246, 140, 134)}{dt(3, 140, 120)}</g>
<g class="dim" data-k="step2">{arrow(220, 246, 220, 174)}{dt(2, 220, 160)}</g>
<g class="dim" data-k="back4">{arrow(60, 246, 60, 94)}{dt(4, 60, 80)}</g>
<g class="dim" data-k="steplen">{arrow(104, 272, 176, 272)}{arrow(184, 272, 256, 272)}<text class="dt" x="270" y="280"><tspan data-m="2">2 m</tspan> + <tspan data-m="2">2 m</tspan></text></g>
<text x="500" y="200" text-anchor="middle" class="lab">net</text><text x="500" y="150" text-anchor="middle" class="lab">metal mesh</text><text x="140" y="200" text-anchor="middle" class="lab">glass</text>
</svg>'''
NETSVG = f'''<svg viewBox="0 0 1000 230" role="img" aria-label="The net seen from the side of the court: 10 metres long, 88 centimetres high in the middle and 92 centimetres at the posts.">
<path d="M60 200h880" stroke="#fff" stroke-width="2" opacity=".7"/>
<path d="M100 62Q500 74 900 62V200H100Z" fill="url(#net)" stroke="#e4eef6" stroke-width="2"/>
<defs><pattern id="net" width="14" height="14" patternUnits="userSpaceOnUse"><path d="M0 0H14M0 0V14" stroke="#e4eef6" stroke-width="1" opacity=".55"/></pattern></defs>
<path d="M100 62Q500 74 900 62" stroke="#fff" stroke-width="7" fill="none"/>
<path d="M96 200V40M904 200V40" stroke="#e4eef6" stroke-width="8"/>
<g class="dim" data-k="neth">{arrow(500, 196, 500, 72)}<text class="dt" data-m="0.88" x="560" y="140" text-anchor="middle">0.88 m</text>{arrow(140, 196, 140, 66)}<text class="dt" data-m="0.92" x="200" y="140" text-anchor="middle">0.92 m</text></g>
<g class="dim" data-k="netl">{arrow(104, 22, 896, 22)}{dt(10, 500, 14)}</g>
</svg>'''
DIMS = [("len", "Length"), ("wid", "Width"), ("svc", "Net to service line"), ("back", "Service line to back wall"), ("box", "Service box width"), ("ext", "Centre line extension"),
        ("glassl", "Side glass length"), ("glass3", "Glass height"), ("step2", "Side step height"), ("back4", "Back wall total"), ("neth", "Net height"), ("netl", "Net length")]
dbtn = "".join(f'<button class="opt" type="button" data-k="{k}" aria-pressed="false">{n}</button>' for k, n in DIMS)
court = f'''<header class="hero"><div class="wrap"><h1>Padel court dimensions, measured.</h1>
<p class="lead">Every official measurement on one court you can explore: tap a measurement to light it up and read what it's for. Switch between metres and feet.</p>
{quick("A doubles padel court is 20 m long and 10 m wide (about 65 ft 7 in by 32 ft 10 in). The service line is 6.95 m from the net, the net is 0.88 m high in the middle and 0.92 m at the posts, and the back wall is 4 m high: 3 m of glass plus 1 m of mesh. Indoor courts need at least 6 m of clear height.")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<div class="dim-bar"><div class="seg" id="unit" role="group" aria-label="Units"><button type="button" data-v="m" aria-pressed="true">Metres</button><button type="button" data-v="ft" aria-pressed="false">Feet</button></div></div>
<div class="dims-layout">
<div class="court-art dims" id="dims"><h2 class="sr-only">Court from above</h2>{TOP}<h3 class="dims-h">The walls from the side</h3>{SIDE}<h3 class="dims-h">The net from the side (height not to scale)</h3>{NETSVG}</div>
<aside class="card zpanel"><h2 style="font-size:1.4rem">Tap a measurement</h2><div class="opts" id="dim-btns">{dbtn}</div><div id="dim-info" aria-live="polite" style="margin-top:18px"></div></aside>
</div></div></section>
{AD.format("court-mid")}
<section><div class="wrap"><div class="sh"><h2>All the numbers in one place</h2><p class="muted">Inside measurements, from the official FIP rules.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt" id="dim-table"><thead><tr><th scope="col">Part of the court</th><th scope="col">Size</th></tr></thead><tbody>
<tr><td>Playing area (doubles)</td><td><span data-m="20">20 m</span> × <span data-m="10">10 m</span></td></tr>
<tr><td>Each half of the court</td><td><span data-m="10">10 m</span> × <span data-m="10">10 m</span></td></tr>
<tr><td>Net to service line</td><td><span data-m="6.95">6.95 m</span></td></tr>
<tr><td>Service line to back wall</td><td><span data-m="3.05">3.05 m</span></td></tr>
<tr><td>Each service box</td><td><span data-m="6.95">6.95 m</span> deep × <span data-m="5">5 m</span> wide</td></tr>
<tr><td>Centre line past the service line</td><td><span data-m="0.2">0.2 m</span></td></tr>
<tr><td>Width of the lines</td><td><span data-m="0.05">0.05 m</span></td></tr>
<tr><td>Net height in the middle</td><td><span data-m="0.88">0.88 m</span></td></tr>
<tr><td>Net height at the posts</td><td><span data-m="0.92">0.92 m</span></td></tr>
<tr><td>Back wall</td><td><span data-m="3">3 m</span> glass + <span data-m="1">1 m</span> mesh</td></tr>
<tr><td>Side glass near each back wall</td><td><span data-m="3">3 m</span> high for <span data-m="2">2 m</span>, then <span data-m="2">2 m</span> high for <span data-m="2">2 m</span></td></tr>
<tr><td>Free height above the court (minimum)</td><td><span data-m="6">6 m</span></td></tr>
<tr><td>Singles court</td><td><span data-m="20">20 m</span> × <span data-m="6">6 m</span></td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Small building tolerances are allowed. Some courts use a variant with taller side glass, and rules for new venues can ask for more height. If you are building a court, check the current rules with your national federation.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What the measurements mean for your game</h2></div><div class="grid">
<div class="card"><h3>Smaller than a tennis court</h3><p>At 20 m by 10 m, the court is about three quarters the area of a tennis doubles court (23.77 m by 10.97 m), and there is no run-off space behind the walls. You rarely sprint far, which is a big reason padel feels easy to start. See all three sports to scale on our <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a> page, or check how many courts fit in your space with the <a href="{href("court-sizes-compared.html")}">court space planner</a>.</p></div>
<div class="card"><h3>A short back area</h3><p>Only about 3 m sits behind the service line. Balls reach the back glass quickly, so learning to let the ball come off the wall matters early.</p></div>
<div class="card"><h3>A low net</h3><p>The net is lower than in tennis, and dips a little in the middle. Low, flat balls over the centre are the safest way to keep the ball in play.</p></div>
<div class="card"><h3>Where the glass steps down</h3><p>The side glass is tallest near the back walls. Balls that hit the mesh act differently from glass, which you can read about on our <a href="{href("wall-rules.html")}">wall and fence rules</a> page.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>The net</h3><p>Can you touch it or reach over it? Check the <a href="{href("net-rules.html")}">net rules checker</a>.</p></div>
<div class="card"><h3>Where to stand</h3><p>Use the measurements in play with the <a href="{href("positioning.html")}">positioning court</a>.</p></div>
<div class="card"><h3>The serve</h3><p>The service box in action: the <a href="{href("serve-rules.html")}">serve checker</a>.</p></div>
<div class="card"><h3>The floor</h3><p>Grass, sand, colours and indoor vs outdoor: <a href="{href("padel-court-surfaces.html")}">padel court surfaces</a>.</p></div>
</div></div></section>'''
court_faq = [
    ("How big is a padel court?", "A doubles padel court is 20 m long and 10 m wide inside the walls. That is about 65 ft 7 in by 32 ft 10 in."),
    ("How far is the service line from the net?", "6.95 m on each side. That leaves 3.05 m between the service line and the back wall."),
    ("How high is a padel net?", "0.88 m in the middle and 0.92 m at the posts, which is roughly 2 ft 11 in and 3 ft."),
    ("How high are the walls of a padel court?", "The back wall is 4 m in total: 3 m of glass with 1 m of metal mesh on top. The side glass is 3 m high near the back walls, then steps down to 2 m."),
    ("How much ceiling height does indoor padel need?", "The official rules ask for at least 6 m of clear height above the court. Higher is better for lobs."),
    ("How big is a singles padel court?", "Singles courts are 20 m long like doubles, but only 6 m wide."),
    ("Is a padel court smaller than a tennis court?", "Yes. A padel court is 20 x 10 m (200 square metres). A tennis doubles court is 23.77 x 10.97 m (about 261 square metres), so padel is about three quarters of the area, before counting the space tennis needs around the lines."),
]
page("court-dimensions.html", "Padel Court Dimensions and Size: Measured Diagram (m and ft) | Padel Glass Box",
     "Official padel court dimensions on an interactive diagram: 20 x 10 m court, 6.95 m service line, 88 cm net, wall and glass heights. Switch metres and feet.", court, court_faq, "Court dimensions")

# ---------------- LEVEL CALCULATOR ----------------
LVQ = [
    ("rally", "1. How long are your rallies?", [(1, "A few shots, then someone misses"), (2, "5 to 10 shots at a slow pace"), (3, "Long rallies at a medium pace"), (4.5, "Long, fast rallies with few easy mistakes")]),
    ("serve", "2. How are your serve and return?", [(1, "Still learning a legal serve"), (2, "The serve goes in; I return it softly"), (3.5, "I aim my serve and return low or with a lob"), (4.5, "I use spin and pick the target on purpose")]),
    ("glass", "3. What happens when the ball comes off the back glass?", [(1, "I try to hit it before it reaches the glass"), (2.5, "I can return easy balls off the back glass"), (3.5, "I'm happy with back and side glass, including the corner"), (5, "I attack off the glass, even after two walls")]),
    ("net", "4. How do you play at the net?", [(1.5, "I mostly stay at the back"), (2.5, "I can block a volley back"), (3.5, "I volley deep or at an angle on purpose"), (4.5, "I win points at the net and set the pace")]),
    ("over", "5. What do you do with a lob over your head?", [(1.5, "Let it bounce, or miss it"), (2.5, "A basic flat overhead or smash"), (3.5, "A bandeja to keep my place at the net"), (5, "Bandeja, víbora or a smash out of the court, picked for the ball")]),
    ("tact", "6. How do you play with your partner?", [(1, "Still learning where to stand"), (2.5, "We move up and back together most of the time"), (3.5, "We lob to win the net and target the weaker side"), (4.5, "We build points with a plan and read the other pair")]),
    ("comp", "7. What kind of padel do you play?", [("social", "Friendly games only"), ("club", "Club leagues or Americano nights"), ("tour", "Regular tournaments"), ("nat", "Nationally ranked"), ("pro", "Professional tour")]),
]
def lvq(name, title, opts):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="false">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-lv="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
lvl = f'''<header class="hero"><div class="wrap"><h1>What is my padel level?</h1>
<p class="lead">Answer seven quick questions about your game. You get an estimated level from 1 to 7, what it means, and the one thing to work on next. Free and private: your answers stay on this device.</p>
{quick("Padel levels run from 0 or 1 (complete beginner) to 7 (professional). Most club players are between 2 and 4.5: about 1 to 2.5 if you are new, 3 to 3.5 if you can rally and use the back glass, 4 to 4.5 if you play a reliable bandeja and think about tactics, and 5 or more if you play regular tournaments. On Playtomic, your level then moves up or down after each competitive match.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="lvquiz">
<div class="card">
{"".join(lvq(*x) for x in LVQ)}
<div class="btns" style="margin-top:0"><button class="btn ghost sm" type="button" id="lv-reset">Clear my answers</button></div>
</div>
<aside class="result" id="lv-result" aria-live="polite"></aside>
</div></section>
{AD.format("level-mid")}
<section><div class="wrap"><div class="sh"><h2>What do padel levels 1 to 7 mean?</h2><p class="muted">A general guide. Each club or app words it a little differently.</p></div><div class="grid">
<div class="card"><span class="pill b">1 to 2.5</span><h3 style="margin-top:10px">Beginner</h3><p>You are learning the serve, the scoring and how the ball comes off the glass. Rallies are short. Most new players move up quickly here.</p></div>
<div class="card"><span class="pill b">3 to 3.5</span><h3 style="margin-top:10px">Improver</h3><p>You can rally, use the back glass on easy balls and move with your partner. Many tennis and squash players start around here.</p></div>
<div class="card"><span class="pill i">4 to 4.5</span><h3 style="margin-top:10px">Intermediate</h3><p>You control the court, play a bandeja, defend the corners and think about tactics. This is a strong club player.</p></div>
<div class="card"><span class="pill a">5 to 5.5</span><h3 style="margin-top:10px">Advanced</h3><p>You play tournaments, build points on purpose and rarely give away easy errors. Ranked players often sit at 5.5 and up.</p></div>
<div class="card"><span class="pill a">6 to 7</span><h3 style="margin-top:10px">Elite</h3><p>Semi-professional and professional players. Pros are rated by the FIP world ranking instead: see the <a href="{href("padel-rankings.html")}">padel rankings and how pro points work</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why does your padel level matter?</h2></div><div class="grid">
<div class="card"><h3>Better matches</h3><p>Games are most fun when all four players are close in level. Booking apps use levels to suggest open matches for you.</p></div>
<div class="card"><h3>Different scales</h3><p>Not every system is the same. Playtomic uses 0 to 7 and moves your level after each rated match. The LTA in the UK uses 1.0 to 7.0. A 3 in one place may not be a 3 in another.</p></div>
<div class="card"><h3>Your real level comes from results</h3><p>A quiz gives you a starting point. Rated matches, or a coach watching you play, give a truer number over time.</p></div>
<div class="card"><h3>Running a social night?</h3><p>Ask players for a rough level, then use our <a href="{href("americano.html")}">Mexicano generator</a>: it pairs people with similar scores as the night goes on.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How does the Playtomic level work?</h2><p class="muted">From Playtomic's help pages, checked {e(UPDATED)}. Apps change their rules, so check the app if something looks different.</p></div><div class="grid">
<div class="card"><span class="pill b">Start</span><h3 style="margin-top:10px">One questionnaire</h3><p>When you join, a short set of questions about your experience gives your starting level on a 0 to 7 scale. You can only do it once.</p></div>
<div class="card"><span class="pill b">Moves</span><h3 style="margin-top:10px">Results against expectations</h3><p>After a competitive match, the app compares each team's average level with the result. Beat a stronger pair and you go up more; lose to a weaker pair and you go down more. Even a draw can move levels.</p></div>
<div class="card"><span class="pill i">Reliability</span><h3 style="margin-top:10px">Big jumps at first</h3><p>Each level has a reliability figure. When it is low, your level moves a lot after each match. As you play more competitive matches it rises and the changes get smaller. You can't change it yourself.</p></div>
<div class="card"><span class="pill i">Casual</span><h3 style="margin-top:10px">Not every match counts</h3><p>Only competitive matches with an accepted, valid score count. Pick "casual" when you book if you just want a friendly game that won't touch your level.</p></div>
<div class="card"><span class="pill a">Fix it</span><h3 style="margin-top:10px">Levelling session</h3><p>Certified clubs can run a levelling session with a coach, which sets your level and puts its reliability at 50%. Useful if your starting level was far off.</p></div>
<div class="card"><span class="pill a">Fix it</span><h3 style="margin-top:10px">10-Match Challenge</h3><p>If your reliability is 85% or more and you think your level is wrong, you can opt in to 10 competitive matches where changes count 2, 3 or 4 times. You can't stop once you start, and you can repeat it after 3 months.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which skills match which level?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Level</th><th scope="col">You can usually</th><th scope="col">Work on next</th></tr></thead><tbody>
<tr><td>1 to 2.5</td><td>Serve legally, rally slowly, return easy balls</td><td><a href="{href("wall-rules.html")}">The back glass</a> and <a href="{href("rules.html")}">the rules</a></td></tr>
<tr><td>3 to 3.5</td><td>Rally, play easy balls off the glass, move with your partner</td><td><a href="{href("positioning.html")}">Positioning</a> and the bandeja</td></tr>
<tr><td>4 to 4.5</td><td>Bandeja, corners, volleys with direction</td><td><a href="{href("bandeja-vs-vibora.html")}">Picking the right overhead</a></td></tr>
<tr><td>5 to 5.5</td><td>Víbora, attack off the glass, build points on purpose</td><td>Fewer errors under pressure</td></tr>
<tr><td>6 to 7</td><td>Semi-pro and pro play</td><td>You know already</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">A general guide in our own words. Playtomic, the LTA and other systems each describe their levels a little differently.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>What to work on next</h3><p>Three priorities for your level, plus the tools to use: <a href="{href("padel-improvement-guide.html")}">level-by-level improvement guide</a>.</p></div>
<div class="card"><h3>Practise your weak spot</h3><p>Turn your "work on next" into a timed session with the <a href="{href("drills.html")}">drills planner</a>.</p></div>
<div class="card"><h3>Learn the overheads</h3><p>The step from 3.5 to 4.5 is mostly about overheads. Try the <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora chooser</a>.</p></div>
<div class="card"><h3>Match your racket</h3><p>Your level changes which racket suits you. Try the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
</div></div></section>'''
lvl_faq = [
    ("What padel level am I?", "Most people who play for fun sit between 1 and 4 on a 1 to 7 scale. Beginners are 1 to 2.5, improvers 3 to 3.5, strong club players 4 to 4.5, and tournament players 5 and up. Answer the questions on this page for your estimate."),
    ("What is a good padel level?", "There is no bad level. As a rough guide, a 3 can enjoy long rallies, a 4 is a solid club player and a 5 plays regular tournaments."),
    ("How does the Playtomic level work?", "Playtomic uses a 0 to 7 scale. You start with a level from a short questionnaire, then it goes up or down after each competitive match, based on the result and the average level of each team. Beating stronger players moves you up more."),
    ("Why did my Playtomic level change so much?", "When your level's reliability is low, usually because you haven't played many competitive matches, each result moves it a lot. The changes get smaller as reliability rises."),
    ("Do friendly matches change my Playtomic level?", "Not if you choose a casual match. Only competitive matches with an accepted, valid score change your level."),
    ("Can I change my Playtomic level?", "You can't edit reliability yourself. Options are a levelling session at a certified club, which sets your level, or the 10-Match Challenge if your reliability is 85% or higher."),
    ("Is this calculator an official rating?", "No. It's a free estimate to help you pick games and know what to practise. Clubs, apps and federations each run their own rating systems."),
    ("What level is a tennis player starting padel?", "Many good tennis or squash players start around 3 to 3.5, because they already hit the ball well. Learning the glass and the net game usually takes a few months."),
    ("How do I move up a level?", "Fix the weakest part of your game first, as it costs you the most points. For most players that means getting comfortable with the back glass and learning the bandeja."),
]
page("level-calculator.html", "Padel Level Calculator: What Is My Padel Level (1 to 7)? | Padel Glass Box",
     "What is my padel level? Answer 7 quick questions for an estimated level from 1 to 7, what each level means, how Playtomic levels work and what to practise.", lvl, lvl_faq, "Level calculator")

# ---------------- GOLDEN POINT vs STAR POINT ----------------
deuce = f'''<header class="hero"><div class="wrap"><h1>Golden point, Star Point or advantage?</h1>
<p class="lead">Padel has three ways to finish a game at 40-40. Play the same points through all three below and watch how each one decides the game.</p></div></header>
<section style="padding-top:10px"><div class="wrap"><div class="score" id="deuce">
<div class="score-top"><p style="margin:0;font-weight:700">The score is 40-40. Who wins the next point?</p><div class="btns" style="margin:0"><button class="btn sm" type="button" id="dz-rand">Play a random game</button><button class="btn sm" type="button" id="dz-reset">Back to 40-40</button></div></div>
<div class="teams dz-btns"><button class="btn lime" type="button" data-w="0">Team A wins the point</button><button class="btn lime" type="button" data-w="1">Team B wins the point</button></div>
<div class="dz-log" id="dz-log" aria-live="polite"></div>
<div class="dz-cols">
<div class="dz" data-f="adv"><h3>Advantage</h3><b class="dz-s">40-40</b><p class="dz-m">Deuce</p></div>
<div class="dz" data-f="golden"><h3>Golden point</h3><b class="dz-s">40-40</b><p class="dz-m">Next point wins</p></div>
<div class="dz" data-f="star"><h3>Star Point</h3><b class="dz-s">40-40</b><p class="dz-m">First deuce</p></div>
</div></div>
<p class="muted" style="margin-top:14px">Want to use it in a real match? Our <a href="{href("score.html")}">score keeper</a> has all three formats.</p>
</div></section>
{AD.format("deuce-mid")}
<section><div class="wrap"><div class="sh"><h2>How each format works</h2></div><div class="grid">
<div class="card"><span class="pill i">Classic</span><h3 style="margin-top:10px">Advantage</h3><p>At 40-40 (deuce) you need to win two points in a row. Win one and you have the advantage; lose the next and it is deuce again. It can go on for a long time.</p></div>
<div class="card"><span class="pill b">Quickest</span><h3 style="margin-top:10px">Golden point</h3><p>At 40-40 one point decides the game. The receiving pair chooses who receives: the player on the right side or the left. Very common in club games and social padel.</p></div>
<div class="card"><span class="pill a">New in 2026</span><h3 style="margin-top:10px">Star Point</h3><p>At the first deuce you play advantage. If it comes back to 40-40, you play advantage once more. If it comes back to 40-40 a third time, one deciding point, the Star Point, wins the game. The receiving pair chooses the side for that point.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Side by side</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Advantage</th><th scope="col">Golden point</th><th scope="col">Star Point</th></tr></thead><tbody>
<tr><td>Points after 40-40 (most)</td><td>No limit</td><td>1</td><td>5</td></tr>
<tr><td>Longest game from 0-0</td><td>No limit</td><td>7 points</td><td>11 points</td></tr>
<tr><td>Can you win from advantage?</td><td>Yes</td><td>No advantage</td><td>Yes, twice</td></tr>
<tr><td>Deciding point?</td><td>No</td><td>At the first deuce</td><td>At the third deuce</td></tr>
<tr><td>Who picks the receiving side</td><td>Normal order</td><td>Receiving pair</td><td>Receiving pair</td></tr>
<tr><td>Where you see it</td><td>Classic matches and some leagues</td><td>Many clubs and social games</td><td>Pro tours and many sanctioned events since 2026</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Who uses which</h2></div><div class="grid">
<div class="card"><h3>Professional padel</h3><p>The International Padel Federation (FIP) approved Star Point in late 2025. From 2026 it is used on Premier Padel, the FIP Tour, FIP Promises and the FIP Beyond amateur events. You can see it at the <a href="{href("premier-padel-mexico-major.html")}">Mexico Major 2026</a>.</p></div>
<div class="card"><h3>National events</h3><p>Some federations follow the pro tours. In the US, USPA-sanctioned tournaments use Star Point from January 2026. Always check the event's own rules.</p></div>
<div class="card"><h3>Your club game</h3><p>Friendly games can use any of the three. Golden point keeps games short when court time is tight. Agree on one before the first serve, so nobody argues at 40-40.</p></div>
<div class="card"><h3>Tie-breaks</h3><p>None of this changes the tie-break. At 6-6 you play to 7 points with a two-point lead. See who serves each point on our <a href="{href("tie-break.html")}">tie-break page</a>.</p></div>
</div></div></section>'''
deuce_faq = [
    ("What is the Star Point in padel?", "A deuce format used from 2026. You play advantage twice. If the game reaches 40-40 a third time, one deciding point, the Star Point, wins the game."),
    ("What is the golden point in padel?", "At 40-40 one point decides the game. The receiving pair chooses which player receives it, and whoever wins the point wins the game."),
    ("Who chooses the side on the golden point?", "The receiving pair. They pick whether the player on the right or the left receives the serve. The same applies to the Star Point."),
    ("Is golden point still used in padel?", "Yes. Many clubs and social games still use it, as it keeps games short. Professional tours moved to Star Point in 2026."),
    ("How many points can a game last with Star Point?", "At most 5 points after the first 40-40, so 11 points in total from 0-0. With classic advantage there is no limit."),
    ("Which deuce format should we use in a friendly game?", "Any of the three is fine. Golden point is quickest, advantage is the most traditional, and Star Point matches the pro game. Just agree before you start."),
]
page("golden-point-star-point.html", "Golden Point vs Star Point vs Advantage in Padel, Explained | Padel Glass Box",
     "How padel games end at 40-40: classic advantage, golden point and the new 2026 Star Point. Try all three on an interactive deuce simulator.", deuce, deuce_faq, "Golden point vs Star Point")

# ---------------- POSITIONING ----------------
# Court drawn top-down, 30 px per metre, 20 px padding. Your team at the bottom.
def _m(x, y): return 20 + x * 30, 20 + y * 30
POS_SVG = '''<svg viewBox="0 0 340 640" id="pos-court" role="img" aria-label="Top view of a padel court showing where the four players stand">
<defs><marker id="pos-ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#e8f84a"/></marker></defs>
<rect x="20" y="20" width="300" height="600" fill="#1e46c8"/>
<rect x="20" y="20" width="300" height="600" fill="none" stroke="#9cc4ea" stroke-width="8" opacity=".55"/>
<path d="M20 111.5h300M20 528.5h300M170 111.5v417" stroke="#fff" stroke-width="2"/>
<path d="M14 320h312" stroke="#e4eef6" stroke-width="5"/>
<g id="pos-zones"></g><g id="pos-arrows"></g><g id="pos-players"></g>
</svg>'''
pos = f'''<header class="hero"><div class="wrap"><h1>Where to stand in padel.</h1>
<p class="lead">Pick a moment in the point and see where all four players should be. Your team is at the bottom: you on the left, your partner on the right.</p>
{quick("At the net, stand about 2 to 2.5 metres from the net. When you defend, stand about 1 metre in front of the back glass. Move up and back with your partner as a pair, about 3 metres apart, and both slide towards the side the ball is on. Avoid one up and one back: it opens a gap down the diagonal.")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<div class="opts" id="pos-pick" role="group" aria-label="Choose a situation" style="margin-bottom:12px">
<button class="opt" type="button" data-s="serve" aria-pressed="true">Your team serves</button>
<button class="opt" type="button" data-s="receive" aria-pressed="false">You receive</button>
<button class="opt" type="button" data-s="net" aria-pressed="false">Both at the net</button>
<button class="opt" type="button" data-s="back" aria-pressed="false">Both at the back</button>
<button class="opt" type="button" data-s="lob" aria-pressed="false">Lobbed at the net</button>
<button class="opt" type="button" data-s="split" aria-pressed="false">One up, one back</button>
</div>
<div class="dim-bar" id="pos-side-bar"><span class="muted" style="font-weight:600">The ball is on</span><div class="seg" id="pos-side" role="group" aria-label="Which side the ball is on"><button type="button" data-v="L" aria-pressed="true">Your side</button><button type="button" data-v="R" aria-pressed="false">Your partner's side</button></div></div>
<div class="rules-layout" style="margin-top:14px">
<div class="court-art" style="max-width:400px;margin-inline:auto;width:100%">{POS_SVG}
<p class="pos-key"><span><i style="background:#e8f84a"></i>You</span><span><i style="background:#fff"></i>Partner</span><span><i style="background:#ff8a5c"></i>Opponents</span><span><i class="ball"></i>Ball</span></p></div>
<aside class="card zpanel" id="pos-panel" aria-live="polite"></aside>
</div></div></section>
{AD.format("pos-mid")}
<section><div class="wrap"><div class="sh"><h2>What are the habits of good padel positioning?</h2></div><div class="grid">
<div class="card"><h3>Move as a pair</h3><p>Imagine a rope of about 3 metres between you and your partner. When one moves up, back or across, the other follows. Gaps open when you move on your own.</p></div>
<div class="card"><h3>Win the net</h3><p>Most points are won at the net. Stand about 2 to 2.5 metres from it, close enough to volley and far enough back to reach a lob.</p></div>
<div class="card"><h3>Give the glass room</h3><p>When you defend, stand about 1 metre in front of the back glass. Too close and the ball comes off the glass into your body. Too far forward and lobs beat you.</p></div>
<div class="card"><h3>Shade with the ball</h3><p>Both players slide towards the side the ball is on. The player nearer the ball covers the line, the other covers the middle.</p></div>
<div class="card"><h3>Agree on the middle</h3><p>Balls down the middle cause the most mix-ups. By default the player with the forehand in the middle takes them. Call "mine" or "yours" early.</p></div>
<div class="card"><h3>Reset after a lob</h3><p>If a lob goes over you, both players go back together, play a safe shot, then look for the next chance to move forward again.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Should I play on the left or the right side in padel?</h2></div><div class="grid">
<div class="card"><span class="pill i">Right side</span><h3 style="margin-top:10px">The drive side</h3><p>For a right-handed player the forehand is on the outside, near the side wall. This player plays more steady, controlled balls and builds the point.</p></div>
<div class="card"><span class="pill a">Left side</span><h3 style="margin-top:10px">The revés side</h3><p>For a right-handed player the forehand is in the middle. This player takes many middle balls and more of the high balls and smashes, so it is often the more attacking role.</p></div>
<div class="card"><span class="pill b">Mixed hands</span><h3 style="margin-top:10px">One right-hander, one left-hander</h3><p>Many pairs put both forehands in the middle: the left-hander on the right side and the right-hander on the left. Try both ways and see what feels natural.</p></div>
</div>
<p class="muted" style="margin-top:14px">New to the shots named here? See the <a href="{href("shots.html")}">shot library</a>. For court measurements, see the <a href="{href("court-dimensions.html")}">court dimensions</a> page.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How far from the net and the glass should you stand?</h2><p class="muted">Rules of thumb that coaches use. Adjust for your height, speed and the opponents' lobs.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Moment</th><th scope="col">Where to stand</th><th scope="col">Why</th></tr></thead><tbody>
<tr><td>Volleying at the net</td><td>About 2 to 2.5 m from the net</td><td>Close enough to volley, far enough back to reach a lob</td></tr>
<tr><td>Defending at the back</td><td>About 1 m in front of the back glass</td><td>Room to let the ball come off the glass</td></tr>
<tr><td>Receiving the serve</td><td>Near the back, about 1 m off the glass, on your half</td><td>Most serves bounce and then reach the glass</td></tr>
<tr><td>Gap to your partner</td><td>About 3 m, moving together</td><td>No hole in the middle or down the diagonal</td></tr>
<tr><td>After a lob goes over you</td><td>Both back together, then forward again</td><td>One up and one back leaves the diagonal open</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Partner calls</h3><p>Who takes the middle ball, and the eight calls good pairs use: <a href="{href("padel-communication.html")}">partner communication</a>.</p></div>
<div class="card"><h3>What shot should I play?</h3><p>Test your decisions in 10 drawn match situations with the <a href="{href("padel-tactics.html")}">padel tactics trainer</a>.</p></div>
<div class="card"><h3>Practise it</h3><p>Build a session with net and glass work in the <a href="{href("drills.html")}">padel drills planner</a>.</p></div>
<div class="card"><h3>Left or right?</h3><p>Not sure which side to play? Take the <a href="{href("which-side-padel.html")}">which side quiz</a>, or fix a habit with the <a href="{href("fix-my-padel.html")}">padel problem fixer</a>.</p></div>
<div class="card"><h3>Win the net back</h3><p>Learn the overheads that keep you forward in <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora vs smash</a>.</p></div>
<div class="card"><h3>Play off the walls</h3><p>Know what is in and out with the <a href="{href("wall-rules.html")}">wall and fence rules</a>.</p></div>
</div></div></section>'''
pos_faq = [
    ("Where should I stand at the net in padel?", "About 2 to 2.5 metres from the net, slightly towards your side of the centre line. The player nearer the ball can be a little closer, with the partner half a step back to cover the middle and the lob."),
    ("How far from the back glass should I stand?", "About 1 metre in front of it when you defend or receive. That gives the ball room to come off the glass so you can play it comfortably."),
    ("Why is one up and one back bad in padel?", "It leaves a big diagonal gap between the two players, and opponents can hit through it or at the feet of the net player. Move up and back together instead."),
    ("Who takes the ball down the middle?", "As a default, the player with the forehand in the middle. For two right-handers that is the player on the left. Whoever calls it first should take it."),
    ("Where does the server's partner stand?", "Usually at the net, about 2 metres from it, on the other half of the court. The rules let the server's partner stand anywhere on their side, but a serve that hits them is a fault."),
    ("Should I play on the left or the right side?", "For right-handers, the left side suits players who like to attack and smash, and the right side suits steady players who like control. Both are important."),
    ("Where should I stand to receive a serve in padel?", "Near the back of your half, about 1 metre in front of the back glass and a little towards the side wall. Most serves bounce and reach the glass, so give the ball room."),
    ("Should both padel players be at the net?", "Yes, when you can. Most points are won at the net, so move forward together after a good lob or a deep ball, and go back together when you are lobbed."),
]
page("positioning.html", "Padel Positioning: Where to Stand on Court (Interactive) | Padel Glass Box",
     "Where to stand in padel: about 2 to 2.5 m from the net or 1 m off the back glass, moving as a pair. Tap the court for serve, return, net and lob positions.", pos, pos_faq, "Positioning")

# ---------------- SERVE RULES + CHECKER ----------------
def _q(qid, label, opts):
    return f'<div class="q sv-q" data-q="{qid}"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
YN = [("y", "Yes"), ("n", "No")]
serve = f'''<header class="hero"><div class="wrap"><h1>Was that serve legal?</h1>
<p class="lead">Answer a few quick questions about the serve and get the call: good serve, fault or let. Then read every padel serve rule in plain English below.</p>
{quick("Stand behind the service line, bounce the ball once on your side, and hit it at or below waist height with at least one foot on the ground. It must land in the service box diagonally opposite (lines are in). You get two serves. A serve that clips the net and lands in the box is a let (replayed). A serve that bounces in and then hits the metal fence is a fault.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="svc">
<div>
{_q("try", "Which serve was it?", [("1", "First serve"), ("2", "Second serve")])}
{_q("bounce", "Did the server bounce the ball behind the service line, on their own side of the centre line, before hitting it?", YN)}
{_q("feet", "Were the server's feet clear of the service line and the centre line?", YN)}
{_q("ground", "Was at least one foot on the ground at the moment of contact?", YN)}
{_q("waist", "Was the ball hit at or below waist height?", YN)}
{_q("own", "Did the ball touch the server, their partner or anything on their side before crossing the net?", [("n", "No"), ("y", "Yes")])}
{_q("land", "What happened next?", [("in", "Landed in the diagonal box (lines count)"), ("netin", "Touched the net, then landed in the box"), ("out", "Landed outside the box"), ("netout", "Touched the net, then landed out"), ("miss", "The server missed the ball"), ("body", "Hit the receiver before bouncing")])}
<div class="q sv-q" data-q="after" id="sv-after"><h3>After bouncing in the box, what did the ball hit first?</h3><div class="opts"><button class="opt" type="button" data-v="none" aria-pressed="false">Nothing, it was returned</button><button class="opt" type="button" data-v="glass" aria-pressed="false">The glass</button><button class="opt" type="button" data-v="fence" aria-pressed="false">The metal fence</button></div></div>
<button class="btn sm" type="button" id="sv-reset">Start again</button>
</div>
<aside class="result" id="sv-out" aria-live="polite"><h2>Make the call</h2><p>Answer the questions and the verdict appears here.</p></aside>
</div></div></section>
{AD.format("serve-mid")}
<section><div class="wrap"><div class="sh"><h2>How do you serve in padel, step by step?</h2></div><div class="grid">
<div class="card"><h3>1. Stand in the right place</h3><p>Stand behind the service line, between the centre line and the side wall. Your feet must not touch the service line or the imaginary line that extends the centre line.</p></div>
<div class="card"><h3>2. Bounce the ball</h3><p>Drop the ball and let it bounce once on your side, behind the service line, before you hit it. You may not hit it straight from your hand.</p></div>
<div class="card"><h3>3. Hit at or below the waist</h3><p>Contact must be at or below waist height, so you serve underarm or side-arm, never overhead. Keep at least one foot on the ground: no jump serves.</p></div>
<div class="card"><h3>4. Land it diagonally</h3><p>The ball must cross the net and bounce in the service box diagonally opposite you. A ball that lands on the line is good.</p></div>
<div class="card"><h3>5. The receiver waits for the bounce</h3><p>The receiver must let the serve bounce before playing it. After the bounce the ball may hit the glass and stay in play.</p></div>
<div class="card"><h3>6. Two tries</h3><p>A fault on the first serve gives you a second serve. Two faults in a row is a double fault, and the receivers win the point.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What is a fault or a let on a padel serve?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">What happened</th><th scope="col">The call</th></tr></thead><tbody>
<tr><td>Ball hit above the waist</td><td>Fault</td></tr>
<tr><td>Ball not bounced first, or bounced in the wrong place</td><td>Fault</td></tr>
<tr><td>Foot on the service line or centre line</td><td>Fault</td></tr>
<tr><td>Both feet off the ground (jump serve)</td><td>Fault</td></tr>
<tr><td>Server swings and misses</td><td>Fault</td></tr>
<tr><td>Lands outside the diagonal box</td><td>Fault</td></tr>
<tr><td>Lands in the box, then hits the metal fence before a second bounce</td><td>Fault</td></tr>
<tr><td>Hits the server's partner before crossing the net</td><td>Fault</td></tr>
<tr><td>Lands in the box, then goes straight out through a door (court without out-of-court play)</td><td>Fault</td></tr>
<tr><td>Lands in the box, then hits the glass</td><td>Good, play on</td></tr>
<tr><td>Touches the net, lands in the box, does not touch the fence</td><td>Let: replay that serve</td></tr>
<tr><td>Touches the net, then lands out</td><td>Fault</td></tr>
<tr><td>Served before the receiver was ready (and they did not try to return it)</td><td>Let: replay that serve</td></tr>
<tr><td>Hits the receiver before it bounces</td><td>Point to the serving pair</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">A let replays only that serve. A let on the second serve means you take the second serve again, not two new serves. Calls in the rally are on the <a href="{href("wall-rules.html")}">wall and fence checker</a>, more rules on our <a href="{href("rules.html")}">interactive rules court</a>, and serve tactics on the <a href="{href("positioning.html")}">positioning guide</a>.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Who serves first in padel, and when do you switch?</h2></div><div class="grid">
<div class="card"><h3>Toss for the first serve</h3><p>Before the match, a coin toss (or spin of a racket) decides. The winners choose to serve, receive or pick an end, or let the other pair choose.</p></div>
<div class="card"><h3>Set the order for each set</h3><p>Before each set, each pair decides which partner serves first, and keeps that order for the set. The receiving pair also decides who receives on which side in the first game of the set, and keeps it.</p></div>
<div class="card"><h3>A whole game each</h3><p>One player serves for the whole game. Then the other pair serves the next game, and so on.</p></div>
<div class="card"><h3>Swap sides every point</h3><p>The server changes side after every point, so each point is served diagonally to the other receiver.</p></div>
<div class="card"><h3>Golden point and Star Point</h3><p>On a deciding point the receiving pair chooses which player receives. See <a href="{href("golden-point-star-point.html")}">how deciding points work</a>.</p></div>
<div class="card"><h3>First point from the right</h3><p>Each game starts with a serve from the right-hand side of the court, then the server switches sides every point.</p></div>
<div class="card"><h3>Time between points</h3><p>FIP rules allow up to 20 seconds between points, 90 seconds when you change ends, and 2 minutes between sets.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Learn the technique</h3><p>Six steps, three targets and a practice tracker: <a href="{href("how-to-serve-padel.html")}">how to serve in padel</a>. On the other side of the net: <a href="{href("padel-return-of-serve.html")}">how to return serve</a>.</p></div>
<div class="card"><h3>Serving in a tie-break</h3><p>The serve order changes in a tie-break. Track it point by point with the <a href="{href("tie-break.html")}">tie-break tracker</a>.</p></div>
<div class="card"><h3>Keep score</h3><p>Use the free <a href="{href("score.html")}">score keeper</a> on your phone at the court.</p></div>
<div class="card"><h3>Learn the serve with a coach</h3><p>Most first lessons cover the serve. See <a href="{href("padel-lessons.html")}">what padel lessons cost and what to expect</a>.</p></div>
</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Source: FIP Rules of Padel (review of application 1 Jan 2026): rules 2 (time), 4 (toss), 6 (serve), 7 (faults), 8 (receiving), 9 (net and let serves). Checked 25 Nov 2026.</p></div></section>'''
serve_faq = [
    ("Can you serve overarm in padel?", "No. You must hit the ball at or below waist height after it bounces, so every padel serve is underhand."),
    ("Is it a let if the serve hits the net in padel?", "Yes, if it then lands in the correct box and does not touch the metal fence before bouncing again. If it touches the net and lands out, it is a fault."),
    ("What if the serve hits the fence in padel?", "If the ball bounces in the box and then hits the metal fence before a second bounce, it is a fault. If it hits the glass instead, the ball is in play."),
    ("Does the serve have to bounce in padel?", "Yes. The server must bounce the ball behind the service line before hitting it, and the receiver must let the serve bounce before returning it."),
    ("Can you stand on the line when serving in padel?", "No. Touching the service line or the imaginary extension of the centre line with your foot when you serve is a fault."),
    ("Can you jump when you serve in padel?", "No. At least one foot must be on the ground when you hit the ball."),
    ("How many serves do you get in padel?", "Two. If the first is a fault, you have a second serve. Two faults is a double fault and loses the point."),
    ("Who serves first in padel?", "A coin toss decides. The winning pair chooses to serve or receive, or picks an end. Before each set, each pair also decides which partner serves first."),
    ("How long do you have between points in padel?", "Under FIP rules, up to 20 seconds between points, 90 seconds when you change ends and 2 minutes between sets."),
    ("Which side do you serve from first in padel?", "From the right-hand side. The server then switches sides after every point for the rest of the game."),
]
page("serve-rules.html", "Padel Serve Rules: Is My Serve Legal? Free Serve Checker | Padel Glass Box",
     "Padel serve rules in plain English (FIP 2026): behind the line, bounce, hit at or below the waist, land it diagonally. Faults, lets and a serve checker.", serve, serve_faq, "Serve rules")

# ---------------- WARM-UP TIMER ----------------
# Each step: (seconds quick, seconds full, phase, name, how). 0 seconds = step left out of that routine.
WU = [
    (120, 150, "Get warm", "Easy jog and side steps", "Jog slowly round the court, then side-step along the net and back. Breathe easily: you should still be able to talk."),
    (30, 45, "Move", "Arm and wrist circles", "Ten big arm circles forwards, ten backwards. Then roll and shake out both wrists."),
    (40, 60, "Move", "Leg swings", "Hold the fence. Swing one leg front to back, then side to side, about ten each way. Change legs."),
    (40, 45, "Move", "Walking lunges with a twist", "Step forward into a lunge and turn your chest over the front knee. About ten steps in total."),
    (30, 45, "Activate", "Squats", "Feet shoulder-width apart, sit back as if onto a chair, stand up tall. About ten, slow and controlled."),
    (30, 45, "Activate", "Side lunges", "Step wide to one side, bend that knee, push back to the middle. Five each side."),
    (0, 30, "Activate", "Wall press-ups", "Hands on the glass at chest height, body straight. Ten slow press-ups to wake up your shoulders."),
    (40, 60, "Activate", "Short sprints", "From the service line, sprint a few metres to the net, then walk back. Three or four sprints, changing the leg you start with."),
    (90, 120, "Racket", "Mini rally in the service boxes", "Both pairs stand near the service line and hit soft balls after the bounce. No volleys yet. Try to keep each rally going for ten shots."),
    (60, 120, "Racket", "Volleys at the net", "One pair at the net, one at the back. Calm volleys to the players at the back. Swap roles halfway."),
    (60, 90, "Racket", "Lobs and easy overheads", "The back pair lobs, the net pair plays half-speed bandejas. Build up the pace slowly. No full smashes yet."),
    (30, 45, "Racket", "Practice serves", "Two or three serves each to each side, plus a few returns."),
    (30, 45, "Mind", "Pick three goals", "Agree with your partner on three simple aims, for example: lob more, stay together, get first serves in."),
]
def wu_steps(k):
    return [{"t": s[k], "ph": s[2], "n": s[3], "d": s[4]} for s in WU if s[k]]
WU_JSON = json.dumps({"q": wu_steps(0), "f": wu_steps(1)}, ensure_ascii=False)
def mmss(s): return f"{s // 60}:{s % 60:02d}"
warm = f'''<header class="hero"><div class="wrap"><h1>Padel warm-up timer.</h1>
<p class="lead">Press start and follow the steps. A 10 or 15 minute warm-up that gets your legs, arms and eye ready before the first point. Works on your phone at the court.</p>
{quick("Warm up for 10 to 15 minutes before padel: 2 minutes of easy jogging and side steps, a few minutes of moving stretches (leg swings, arm circles, lunges with a twist), squats, lunges and short sprints, then soft rallies, volleys, lobs, easy overheads and a few serves. Save long, held stretches for after the match.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="wu" id="wu">
<div class="wu-stage">
<div class="wu-bar"><div class="seg" id="wu-len" role="group" aria-label="Warm-up length"><button type="button" data-v="q" aria-pressed="true">10 minutes</button><button type="button" data-v="f" aria-pressed="false">15 minutes</button></div>
<div class="seg" id="wu-snd" role="group" aria-label="Sound"><button type="button" data-v="on" aria-pressed="true">Beeps on</button><button type="button" data-v="off" aria-pressed="false">Off</button></div></div>
<div class="wu-main">
<svg class="wu-ring" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="10"/><circle id="wu-arc" cx="60" cy="60" r="52" fill="none" stroke="#e8f84a" stroke-width="10" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="0" transform="rotate(-90 60 60)"/></svg>
<div class="wu-time"><b id="wu-clock">2:00</b><span id="wu-of">Step 1 of 12</span></div>
</div>
<div class="wu-now" aria-live="polite"><span class="pill" id="wu-ph">Get warm</span><h2 id="wu-name">Easy jog and side steps</h2><p id="wu-how"></p><p class="wu-next" id="wu-next"></p></div>
<div class="prog"><i id="wu-prog"></i></div>
<div class="wu-ctl"><button class="btn ghost sm" type="button" id="wu-back">Back</button><button class="btn lime" type="button" id="wu-go">Start</button><button class="btn ghost sm" type="button" id="wu-skip">Skip</button></div>
<p class="wu-left" id="wu-left"></p>
</div>
<ol class="wu-list" id="wu-list"></ol>
</div></div></section>
<script>window.WU={WU_JSON};</script>
{AD.format("warm-mid")}
<section><div class="wrap"><div class="sh"><h2>What should a padel warm-up include?</h2></div><div class="grid">
<div class="card"><h3>1. Get warm</h3><p>A couple of minutes of easy jogging raises your heart rate and sends blood to your muscles. Start slow.</p></div>
<div class="card"><h3>2. Move</h3><p>Moving stretches, like leg swings and lunges with a twist, loosen your hips, back and shoulders. Keep them moving: save long, held stretches for after the match.</p></div>
<div class="card"><h3>3. Activate</h3><p>Squats, lunges and short sprints wake up the legs you use for every split step and change of direction. LTA Padel's warm-up advice is built around exercises like these to help avoid hamstring, calf and thigh strains.</p></div>
<div class="card"><h3>4. Racket</h3><p>Start soft and close to the net, then add volleys, lobs and overheads. Build up the pace: your first smash should not be your hardest.</p></div>
<div class="card"><h3>5. Mind</h3><p>Agree three simple goals with your partner. It takes 30 seconds and helps you start the match switched on.</p></div>
<div class="card"><h3>After you play</h3><p>Walk for a couple of minutes, then gently hold stretches for your calves, thighs, hips, forearms and shoulders, about 20 to 30 seconds each.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Short on court time or playing in the cold?</h2></div><div class="grid">
<div class="card"><h3>Do the first half before you go on</h3><p>The jog, moving stretches and squats need no court. Do them by the court while the last game finishes, then use your court time for the racket steps.</p></div>
<div class="card"><h3>Playing early or in the cold?</h3><p>Choose the 15 minute version. Cold muscles need longer, and the balls feel flatter too. Read <a href="{href("padel-balls.html")}">when to change padel balls</a> and the <a href="{href("padel-weather.html")}">padel weather checker</a>.</p></div>
<div class="card"><h3>Warmed up? Now practise</h3><p>Go straight into a planned session with the <a href="{href("drills.html")}">padel drills planner</a> and its timer.</p></div>
<div class="card"><h3>Something hurts?</h3><p>A warm-up is not a fix for an injury. If you feel sharp pain, stop and get advice from a doctor or physiotherapist. See which areas padel players hurt most in the <a href="{href("padel-injuries.html")}">padel injuries guide</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why warm up before padel?</h2></div><div class="grid">
<div class="card"><h3>Padel injuries are mostly muscles and tendons</h3><p>A 2023 review of padel injury studies found that most injuries were to tendons and muscles, with the elbow, knee, shoulder and lower back reported most. Calf strains also appear often.</p></div>
<div class="card"><h3>Not warming up is a known cause</h3><p>NI Direct, the UK government health site for Northern Ireland, lists not warming up properly among the common causes of sports injuries.</p></div>
<div class="card"><h3>Check your other habits</h3><p>Shoes, grip, rest days and technique matter too. Run the two-minute <a href="{href("padel-injuries.html")}#check">injury prevention check</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>After the match</h3><p>Finish with the 5 to 15 minute <a href="{href("padel-cool-down.html")}">padel cool-down and stretch timer</a>.</p></div>
<div class="card"><h3>Practise with a plan</h3><p>Turn your warm-up into a full session with the <a href="{href("drills.html")}">drills planner</a>.</p></div>
<div class="card"><h3>Keep score</h3><p>Ready to play? Open the <a href="{href("score.html")}">score keeper</a> on your phone.</p></div>
<div class="card"><h3>Protect your body</h3><p>Where padel players get hurt and what helps: the <a href="{href("padel-injuries.html")}">padel injuries guide</a>.</p></div>
</div></div></section>'''
warm_faq = [
    ("How long should a padel warm-up be?", "About 10 to 15 minutes is enough for most players. LTA Padel suggests 10 to 15 minutes, starting with a short jog, then exercises, then a few minutes of rallying."),
    ("Should I stretch before padel?", "Use moving stretches before you play, such as leg swings, arm circles and lunges with a twist. Keep long, held stretches for after the match."),
    ("What should a padel warm-up include?", "A short jog, moving stretches, a few leg exercises such as squats and lunges, short sprints, and then racket work: soft rallies, volleys, lobs, easy overheads and a few serves."),
    ("Can I warm up without a court?", "Yes. The jog, moving stretches, squats, lunges and sprints can all be done next to the court before your booking starts."),
    ("Does warming up prevent padel injuries?", "A warm-up lowers the risk but can't remove it. Not warming up properly is a common cause of sports injuries, and most padel injuries are to muscles and tendons, which a warm-up prepares for play."),
    ("Does the timer work without internet?", "Once the page has loaded, the timer runs in your browser. Keep the screen on, because some phones pause timers when the screen locks."),
]
page("warm-up.html", "Padel Warm-Up Routine With Free Timer (10 or 15 Minutes) | Padel Glass Box",
     "Free padel warm-up timer: a 10 or 15 minute routine step by step, from jogging and moving stretches to volleys, lobs and serves, to help prevent injuries.", warm, warm_faq, "Warm-up timer")

# ---------------- PADEL BALLS ----------------
def _bq(qid, label, opts):
    return f'<div class="q bq" data-q="{qid}"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
balls = f'''<header class="hero"><div class="wrap"><h1>Are your padel balls dead?</h1>
<p class="lead">Six quick checks tell you if a ball is still good for a match, fine for practice, or ready for the bin. Then learn how long padel balls last and how to keep them lively.</p>
{quick("For relaxed social games, a can of padel balls (usually 3 balls) stays playable for about 3 to 5 sessions. For a match that matters, open a new can. A ball is dead when it squashes easily, bounces lower than a new ball, sounds dull and dies off the back glass. Padel balls have less pressure than tennis balls (about 11 psi vs 14 psi), so don't swap one for the other.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="bchk">
<div>
{_bq("use", "How many times have you played with this can?", [("0", "Just opened"), ("1", "Once or twice"), ("2", "3 to 5 times"), ("3", "More than 5")])}
{_bq("squeeze", "Squeeze the ball hard with one hand. How does it feel?", [("0", "Firm"), ("1", "A little soft"), ("3", "Squashes easily")])}
{_bq("drop", "Drop it from shoulder height next to a new ball. How does it bounce?", [("0", "About the same"), ("1", "A bit lower"), ("3", "Much lower"), ("x", "No new ball to compare")])}
{_bq("glass", "In play, what happens when it hits the back glass?", [("0", "Comes back well"), ("1", "Comes back a little short"), ("3", "Dies in the corner")])}
{_bq("felt", "How does the felt look?", [("0", "Fluffy and bright"), ("1", "Flat in places"), ("2", "Bald, dirty or wet and heavy")])}
{_bq("sound", "What does it sound like off the racket?", [("0", "A clear pop"), ("1", "Duller than a new ball")])}
<button class="btn sm" type="button" id="b-reset">Start again</button>
</div>
<aside class="result" id="b-out" aria-live="polite"><h2>Check your ball</h2><p>Answer the questions and the verdict appears here.</p></aside>
</div></div></section>
{AD.format("balls-mid")}
<section><div class="wrap"><div class="sh"><h2>How long do padel balls last?</h2></div><div class="grid">
<div class="card"><h3>Social play: a few sessions</h3><p>For relaxed games, a can usually stays playable for about three to five sessions. After that the bounce gets lower and rallies off the glass get harder.</p></div>
<div class="card"><h3>Serious matches: open a new can</h3><p>Balls lose their best bounce quickly when you hit hard. For a match that matters, most players open a fresh can and keep the older balls for practice.</p></div>
<div class="card"><h3>Pressure leaks from day one</h3><p>Padel balls are filled with air under pressure. Once the can is open, the pressure slowly leaks out, even if you don't play.</p></div>
<div class="card"><h3>Courts wear the felt</h3><p>Sand on artificial grass courts rubs the felt and makes it heavy. Wet or dirty balls slow down a lot.</p></div>
<div class="card"><h3>Heat and cold change the feel</h3><p>On a cold day even new balls feel flat. Keep opened cans away from hot cars and cold garages; a cool, dry cupboard is best. Rain, cold, wind or heat today? Try the <a href="{href("padel-weather.html")}">padel weather checker</a>.</p></div>
<div class="card"><h3>Pressurisers help a little</h3><p>A ball saver tube keeps air in for longer, but it can't fix worn felt or bring a dead ball back to life.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What is the difference between a padel ball and a tennis ball?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Padel ball</th><th scope="col">Tennis ball</th></tr></thead><tbody>
<tr><td>Diameter</td><td>6.35 to 6.77 cm</td><td>6.54 to 6.86 cm</td></tr>
<tr><td>Weight</td><td>56.0 to 59.4 g</td><td>56.0 to 59.4 g</td></tr>
<tr><td>Pressure inside (new)</td><td>About 11 psi</td><td>About 14 psi</td></tr>
<tr><td>Rule bounce test</td><td>135 to 145 cm when dropped from 2.54 m</td><td>Bounces higher</td></tr>
<tr><td>How it plays</td><td>Slower, softer, made to come off the glass</td><td>Faster and bouncier</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">The two balls look almost the same, but the lower pressure is what makes padel feel like padel. Tennis balls bounce too high off the floor and walls, so use real padel balls. Sizes and pressure from LTA Padel; bounce test as given in the padel rules.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do I make padel balls last longer?</h2></div><div class="grid">
<div class="card"><h3>Close the can</h3><p>Put the lid back on tightly after every game, or use a ball saver.</p></div>
<div class="card"><h3>Keep them dry</h3><p>Don't play with wet balls if you can avoid it, and let them dry at room temperature, not on a heater.</p></div>
<div class="card"><h3>Mark your cans</h3><p>Write the date or a tally on the lid each time you play. Then you know which can is fresh and which is for drills.</p></div>
<div class="card"><h3>Use old balls well</h3><p>Old balls are fine for <a href="{href("warm-up.html")}">warming up</a>, drills and practice serves. Just not for your next match. Check if a <a href="{href("serve-rules.html")}">serve is legal</a> while you practise.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Check your racket too</h3><p>Dead balls and a dead racket feel alike. Run the <a href="{href("racket-care.html")}">racket health check</a>.</p></div>
<div class="card"><h3>Use old balls for drills</h3><p>Plan a short practice with the <a href="{href("drills.html")}">padel drills planner</a>.</p></div>
<div class="card"><h3>Buying for a padel player?</h3><p>Balls are the safest present. See more <a href="{href("padel-gifts.html")}">padel gift ideas</a> by budget.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Need fresh balls?</h3><p>Browse padel balls, plus overgrips and bags to keep your kit match-ready.</p><ul class="aff-links"><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>Rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
balls_faq = [
    ("How long do padel balls last?", "For social games, a can usually lasts about three to five sessions. Players who hit hard or play important matches often open a new can each match, because the best bounce goes after one or two uses."),
    ("How do I know if a padel ball is dead?", "Squeeze it, drop it next to a new ball and watch it off the back glass. A dead ball feels soft, bounces lower, sounds dull and dies in the corner instead of coming back."),
    ("Can you use tennis balls for padel?", "It's better not to. Tennis balls have more pressure inside, so they bounce higher and faster. Padel balls are made to play off the glass at the right speed."),
    ("What is the pressure of a padel ball?", "LTA Padel gives about 11 psi for a new padel ball, compared with about 14 psi for a new tennis ball."),
    ("Are padel balls smaller than tennis balls?", "Only very slightly. A padel ball is 6.35 to 6.77 cm across and a tennis ball 6.54 to 6.86 cm, and both weigh 56.0 to 59.4 g."),
    ("Do ball pressurisers work?", "They can slow down the loss of pressure, but they can't repair worn felt or make a dead ball lively again."),
    ("How many balls come in a can of padel balls?", "Most cans or tubes hold 3 padel balls. Shops also sell multi-packs of several cans, which work out cheaper if you play every week."),
    ("Can I play padel with old balls?", "Yes, for warm-ups, drills and relaxed practice. For a match, open a fresh can: old balls bounce low and die off the glass, which changes how the game plays."),
]
page("padel-balls.html", "When to Change Padel Balls: Free Dead Ball Checker | Padel Glass Box",
     "How long do padel balls last? About 3 to 5 social sessions per can. Run the free 6-step dead ball checker and compare padel vs tennis balls.", balls, balls_faq, "Padel balls")

# ---------------- ABOUT / PRIVACY / 404 ----------------
# ---------------- WALL AND FENCE RULES ----------------
# Outcome keys: verdict class (good = your shot is good / play on, win = you win the point, lose = you lose the point), heading, why, FIP rule, ball path (side view).
WR = {
    "a_ret": ("good", "Good shot, play on", "Your ball bounced on their side first, so it was a good shot. They returned it before a second bounce, so the rally carries on.", "FIP rule 12.3", [[70,110],[210,30],[300,140],[345,96],[250,60],[120,140]]),
    "a_two": ("win", "You win the point", "Your shot bounced on their side and then bounced again before they hit it. A second bounce ends the rally in your favour.", "FIP rules 12.3 and 13.1", [[70,110],[210,30],[290,140],[325,112],[355,140]]),
    "a_wall": ("good", "Good shot, play on", "After a bounce on their ground the ball may hit their glass or their metal fence. It stays in play, and they can return it off the wall before it bounces again.", "FIP rules 12.3 and 14.1", [[70,110],[220,30],[315,140],[380,100],[320,84],[240,40],[120,140]]),
    "a_out": ("win", "Your shot was good", "The ball bounced on their side first, so it was a good shot. If the club allows out-of-court play, they may run out through the door and return it before it bounces twice. If they can't, or out-of-court play isn't allowed there, you win the point.", "FIP rules 13.1 and 16", [[70,110],[200,40],[300,140],[372,56],[396,30]]),
    "a_stuck": ("win", "You win the point", "If your ball bounces on their side and then gets stuck in the fence, goes out through a hole in it, or stays on the flat top of a wall, you win the point.", "FIP rule 15.1", [[70,110],[230,36],[312,140],[378,78]]),
    "b": ("lose", "You lose the point", "Your shot hit their glass or fence before touching their ground. In padel the ball must bounce on the other side before it touches any wall there.", "FIP rule 13.1", [[70,110],[240,52],[380,98],[330,140]]),
    "c_good": ("good", "Good shot, play on", "You may hit the ball into your own glass so that it bounces back over the net. As long as it then lands on their ground first, it is a good shot.", "FIP rule 14.1", [[70,110],[20,96],[200,26],[300,140],[350,110]]),
    "c_wall": ("lose", "You lose the point", "Playing off your own glass is fine, but the ball must still bounce on their ground before touching their walls. It went straight into their glass or fence.", "FIP rule 13.1", [[70,110],[20,96],[230,36],[380,102]]),
    "c_short": ("lose", "You lose the point", "After hitting your own glass, the ball must still cross the net. It fell back on your side, so the point goes to them.", "FIP rule 13.1", [[70,110],[20,96],[110,90],[160,140]]),
    "d": ("lose", "You lose the point", "You may play off your own glass, but not off your own metal fence. If your shot hits the mesh on your side, you lose the point.", "FIP rule 13.1", [[70,110],[20,78],[95,140]]),
    "e_good": ("good", "Good shot, play on", "During a rally a ball that clips the net and then lands on their side is a good shot. It is only on the serve that a net touch means a let.", "FIP rule 14.1", [[70,118],[200,123],[236,140],[262,124]]),
    "e_short": ("lose", "You lose the point", "The ball hit the net and dropped back on your side, so it never crossed. The point goes to them.", "FIP rule 13.1", [[70,118],[199,124],[186,140]]),
    "e_wall": ("lose", "You lose the point", "The ball touched the net and then flew straight into their glass or fence without bouncing on their ground first.", "FIP rule 13.1", [[70,118],[199,123],[290,70],[380,98]]),
    "f": ("lose", "You lose the point", "On indoor courts, a shot that hits the ceiling, a light or anything above the court before bouncing on their side loses the point.", "FIP rule 13.1", [[70,110],[170,12],[240,70],[290,140]]),
    "h": ("win", "You win the point", "If your shot hits an opponent's body or clothes before it bounces, their team loses the point, even if they were standing outside the court.", "FIP rule 13.1", [[70,110],[180,60],[296,92]]),
    "g": ("lose", "You lose the point", "If the ball you hit touches you or your partner, your team loses the point.", "FIP rule 13.1", [[70,110],[100,70],[118,100]]),
}
def _wq(qid, label, opts, off=False):
    return f'<div class="q sv-q wr-q{" off" if off else ""}" data-q="{qid}"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
WR_SVG = '''<svg viewBox="0 0 400 160" class="wr-court" role="img" aria-label="Side view of a padel court. The ball path for the chosen situation is drawn on it.">
<rect x="0" y="0" width="400" height="160" rx="14" fill="#0e2468"/>
<path d="M14 12h372" stroke="#7a8ba8" stroke-width="2" stroke-dasharray="4 6" opacity=".7"/><text x="24" y="26" font-size="9" fill="#9fb0e0" font-family="Onest, sans-serif">Ceiling or lights (indoor)</text>
<rect x="20" y="140" width="360" height="6" fill="#1e46c8"/>
<rect x="14" y="86" width="6" height="54" fill="#9cc4ea" opacity=".75"/><rect x="380" y="86" width="6" height="54" fill="#9cc4ea" opacity=".75"/>
<path d="M17 68v18M383 68v18" stroke="#7a8ba8" stroke-width="6" stroke-dasharray="2 2"/>
<rect x="198" y="124" width="4" height="16" fill="#e4eef6"/>
<text x="110" y="156" text-anchor="middle" font-size="9" fill="#9fb0e0" font-family="Onest, sans-serif">Your side</text><text x="290" y="156" text-anchor="middle" font-size="9" fill="#9fb0e0" font-family="Onest, sans-serif">Their side</text>
<text x="26" y="82" font-size="8" fill="#9fb0e0" font-family="Onest, sans-serif">fence</text><text x="26" y="100" font-size="8" fill="#9fb0e0" font-family="Onest, sans-serif">glass</text>
<g fill="#e8f84a"><circle cx="70" cy="104" r="5"/><path d="M70 110v22M70 132l-6 8M70 132l6 8" stroke="#e8f84a" stroke-width="3"/></g>
<g fill="#ffffff"><circle cx="300" cy="84" r="5"/><path d="M300 90v22M300 112l-6 28M300 112l6 28" stroke="#fff" stroke-width="3" opacity=".9"/></g>
<polyline id="wr-path" points="" fill="none" stroke="#e8f84a" stroke-width="2.5" stroke-dasharray="5 5"/>
<g id="wr-marks"></g>
<circle id="wr-ball" cx="70" cy="110" r="6" fill="#e8f84a" stroke="#0b1530" stroke-width="1.5"/>
</svg>'''
wall = f'''<header class="hero"><div class="wrap"><h1>Padel wall rules: was that ball in?</h1>
<p class="lead">Glass, fence, net, ceiling: tap what your shot touched and see the call, with the ball path drawn on a side view of the court. Then read the wall and fence rules in plain English.</p>
{quick("Your shot must bounce on the other team's ground first. After that bounce it may hit their glass or metal fence and stay in play. If it hits their glass or fence before bouncing, you lose the point. On your own side you may play the ball into your own glass, but never into your own metal fence.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="wr">
<div>
{_wq("first", "1. After you hit it, what did the ball touch first?", [("a", "Their ground (it bounced on their side)"), ("b", "Their glass or fence"), ("c", "My own glass"), ("d", "My own metal fence"), ("e", "The net"), ("f", "The ceiling or a light"), ("h", "An opponent"), ("g", "Me or my partner")])}
{_wq("a", "2. Then what happened?", [("ret", "They hit it back before a second bounce"), ("wall", "It hit their glass or fence"), ("two", "It bounced a second time"), ("out", "It left the court over a wall or through a door"), ("stuck", "It got stuck in the fence or on top of a wall")], True)}
{_wq("c", "2. Then what happened?", [("good", "It crossed the net and bounced on their side"), ("wall", "It crossed the net and hit their glass or fence first"), ("short", "It didn't make it over the net")], True)}
{_wq("e", "2. Then what happened?", [("good", "It went over and bounced on their side"), ("short", "It dropped back on my side"), ("wall", "It went over and hit their glass or fence first")], True)}
<button class="btn sm" type="button" id="wr-reset">Start again</button>
</div>
<aside class="result" id="wr-out" aria-live="polite"><div class="wr-svg">{WR_SVG}</div><div id="wr-txt"><h2>Make the call</h2><p>Tap what the ball touched and the verdict appears here. These are rally rules; for the serve, use the <a href="{href("serve-rules.html")}" style="color:#e8f84a">serve checker</a>.</p></div></aside>
</div></div></section>
{AD.format("wall-mid")}
<section><div class="wrap"><div class="sh"><h2>What are the wall rules in padel?</h2></div><div class="grid">
<div class="card"><span class="pill b">The golden rule</span><h3 style="margin-top:10px">Ground first, then walls</h3><p>Your shot must cross the net and bounce on their ground before it touches anything else on their side. After that bounce, the glass and the fence are both part of the game.</p></div>
<div class="card"><span class="pill b">Your side</span><h3 style="margin-top:10px">Your glass is a tool</h3><p>You can hit the ball into your own glass to send it back over the net. This is a normal shot in padel, often used when the ball gets past you into the corner.</p></div>
<div class="card"><span class="pill b">Your side</span><h3 style="margin-top:10px">Your fence is not</h3><p>Hitting the ball into the metal mesh on your own side loses the point. Only the glass may be used to play the ball back.</p></div>
<div class="card"><span class="pill b">Their side</span><h3 style="margin-top:10px">One bounce, then anything</h3><p>After one bounce on their side, the ball may hit their glass, their fence or both, as many times as it likes. They must hit it before it touches the ground a second time.</p></div>
<div class="card"><span class="pill b">Net</span><h3 style="margin-top:10px">Net cord is fine in a rally</h3><p>In a rally, a ball that clips the net and lands on their side is good. On the serve it is a let. Touching the net or the posts with your body or racket loses the point. More in the <a href="{href("net-rules.html")}">net rules checker</a>.</p></div>
<div class="card"><span class="pill b">Outside</span><h3 style="margin-top:10px">Out of the court</h3><p>A ball that bounces on their side and then flies out of the court was a good shot. At clubs that allow it, they may run out and play it back. If not, you win the point.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is it in if the ball hits the glass or the fence?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Your shot</th><th scope="col">The call</th></tr></thead><tbody>
<tr><td>Bounces on their side, then hits their glass</td><td>In play</td></tr>
<tr><td>Bounces on their side, then hits their fence</td><td>In play</td></tr>
<tr><td>Hits their glass or fence before bouncing</td><td>You lose the point</td></tr>
<tr><td>Hits your own glass, then bounces on their side</td><td>In play</td></tr>
<tr><td>Hits your own glass, then goes straight into their glass</td><td>You lose the point</td></tr>
<tr><td>Hits your own metal fence</td><td>You lose the point</td></tr>
<tr><td>Clips the net, then bounces on their side (rally)</td><td>In play</td></tr>
<tr><td>Hits the ceiling or a light before bouncing on their side</td><td>You lose the point</td></tr>
<tr><td>Bounces on their side, then sticks in the fence or on top of a wall</td><td>You win the point</td></tr>
<tr><td>Bounces on their side, then leaves the court</td><td>Good shot: they must play it outside (if allowed) or lose the point</td></tr>
<tr><td>Hits an opponent before bouncing</td><td>You win the point</td></tr>
<tr><td>You touch the net or a post during the rally</td><td>You lose the point</td></tr>
<tr><td>You hit the ball before it crosses to your side</td><td>You lose the point</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">These calls follow the International Padel Federation (FIP) rules in force from January 2026. Club and league formats can add local rules, for example about out-of-court play. See the rest of the game on our <a href="{href("rules.html")}">interactive rules court</a>.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Can you play the ball outside the court in padel?</h2></div><div class="grid">
<div class="card"><h3>What it is</h3><p>Sometimes a strong smash bounces on your side and flies out over the wall or through the door. At some courts you are allowed to run out of the court and hit the ball back before it bounces a second time. In Spanish this is called a salida de pista.</p></div>
<div class="card"><h3>When it is allowed</h3><p>Only where the court is built for it: open door gaps and enough clear space outside. If the space isn't there, the club does not allow it, and a ball that bounces and leaves the court simply wins the point for the hitter.</p></div>
<div class="card"><h3>How to play it</h3><p>Run out through the door, let the ball drop, and hit it back over the wall into the opponents' court. Your feet can be outside the court only when out-of-court play is allowed. Agree on the local rule before you start. Every out-of-court call is on our <a href="{href("out-of-court-play.html")}">out-of-court play checker</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Are the wall rules different on the serve?</h2></div><div class="grid">
<div class="card"><h3>Glass after the bounce: fine</h3><p>A serve that bounces in the correct service box and then hits the glass is a good serve, just like in a rally.</p></div>
<div class="card"><h3>Fence after the bounce: fault</h3><p>A serve that bounces in the box and then hits the metal fence before a second bounce is a fault. In a rally the fence would be fine, so this catches many new players out.</p></div>
<div class="card"><h3>Net, then in: let</h3><p>A serve that clips the net and lands in the right box is a let and is played again, unless it then hits the fence. All serve calls are on the <a href="{href("serve-rules.html")}">serve rules checker</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Learn to play off the glass</h3><p>Letting the ball come off the back glass is the big new skill. Practise it with the <a href="{href("drills.html")}">drills planner</a>.</p></div>
<div class="card"><h3>Other calls</h3><p>Net touches and reaching over: the <a href="{href("net-rules.html")}">net rules checker</a>. Who serves and when: the <a href="{href("serve-rules.html")}">serve rules</a>.</p></div>
<div class="card"><h3>Keep the score</h3><p>Settle the call, then track the match with the <a href="{href("score.html")}">score keeper</a>, including golden point.</p></div>
</div></div></section>'''
wall_faq = [
    ("Can you hit the ball off your own wall in padel?", "Yes, off your own glass. You can hit the ball into your glass so it rebounds over the net, as long as it then bounces on the other side before touching their walls. Hitting your own metal fence loses the point."),
    ("Is it in if the ball hits the fence in padel?", "If the ball bounced on the ground first, yes: it stays in play. If it hit the fence before bouncing on the other side, the player who hit it loses the point."),
    ("What happens if the ball goes out of the court in padel?", "If it bounced on the opponents' side first, the shot was good. Where out-of-court play is allowed, the opponents may run out and return it before a second bounce. Otherwise the hitter wins the point."),
    ("Is a net cord a let in padel?", "Only on the serve. During a rally, a ball that touches the net and lands on the other side is in play, and players carry on."),
    ("What if the ball gets stuck in the fence in padel?", "If it bounced on the opponents' side and then gets stuck in the mesh, goes out through a hole, or stays on top of the wall, the player who hit it wins the point."),
    ("Can you touch the net in padel?", "No. Touching the net, the posts or the opponents' court with your body, clothes or racket while the ball is in play loses the point."),
    ("What if the ball hits the ceiling in padel?", "If your shot hits the ceiling or a light before bouncing on the opponents' side, you lose the point."),
    ("Can the serve hit the fence in padel?", "No. If the serve bounces in the service box and then hits the metal fence before bouncing again, it is a fault. Hitting the glass after the bounce is fine."),
    ("Can the ball hit more than one wall in padel?", "Yes. After it bounces once on the opponents' side, it may hit the glass, the fence or both, as many times as it likes. They must play it before it touches the ground a second time."),
]
page("wall-rules.html", "Padel Wall and Fence Rules: Was That Ball In? Free Checker | Padel Glass Box",
     "Padel wall rules: the ball must bounce before hitting the glass or fence; use your own glass but not your own fence. Plus a free tap-through call checker.", wall + f'<script>window.WR={json.dumps(WR)};</script>', wall_faq, "Wall and fence rules")

# ---------------- PADEL VS TENNIS VS PICKLEBALL ----------------
# Courts drawn to scale, 10 px per metre, centred on the net.
def _rc(w, h): return 130 - w * 5, 65 - h * 5
_tx, _ty = _rc(23.77, 10.97); _sy = 65 - 8.23 * 5
_px, _py = _rc(20, 10); _kx, _ky = _rc(13.41, 6.10)
VS_SVG = f'''<svg viewBox="0 0 260 130" class="vs-court" role="img" aria-label="Tennis, padel and pickleball courts drawn to the same scale, one on top of the other, all centred on the net.">
<rect width="260" height="130" rx="8" fill="#0b1c55"/>
<g class="vs-g" data-s="t" fill="none" stroke="#ffffff" stroke-width=".8"><rect x="{_tx:.2f}" y="{_ty:.2f}" width="237.7" height="109.7" fill="#2e8a5a" fill-opacity=".28"/><path d="M{_tx:.2f} {_sy:.2f}h237.7M{_tx:.2f} {130-_sy:.2f}h237.7M66 {_sy:.2f}v82.3M194 {_sy:.2f}v82.3M66 65h128"/></g>
<g class="vs-g" data-s="p" fill="none" stroke="#ffffff" stroke-width=".8"><rect x="{_px}" y="{_py}" width="200" height="100" fill="#1d55e6" fill-opacity=".55"/><path d="M60.5 {_py}v100M199.5 {_py}v100M60.5 65h139"/><rect x="{_px}" y="{_py}" width="200" height="100" stroke="#9cc4ea" stroke-width="2.6" opacity=".8"/></g>
<g class="vs-g" data-s="k" fill="none" stroke="#e8f84a" stroke-width=".9"><rect x="{_kx:.2f}" y="{_ky:.2f}" width="134.1" height="61" fill="#e8f84a" fill-opacity=".14"/><rect x="108.7" y="{_ky:.2f}" width="42.6" height="61" fill="#e8f84a" fill-opacity=".22"/><path d="M{_kx:.2f} 65h45.75M151.3 65h45.75"/></g>
<path d="M130 6v118" stroke="#e4eef6" stroke-width="1.6"/>
</svg>'''
VS = {
    "t": {"name": "Tennis", "m": [23.77, 10.97], "ft": [78, 36], "note": "Doubles court. Singles uses 8.23 m (27 ft) of the width.", "net": "About 0.91 m (3 ft) in the middle, 1.07 m (3.5 ft) at the posts", "walls": "None. The lines decide in or out."},
    "p": {"name": "Padel", "m": [20, 10], "ft": [65.6, 32.8], "note": "The same court for every game, closed in by glass and metal fence.", "net": "88 cm (34.6 in) in the middle, 92 cm (36.2 in) at the posts", "walls": "Glass and fence all round, and you play off them."},
    "k": {"name": "Pickleball", "m": [13.41, 6.10], "ft": [44, 20], "note": "The same court for singles and doubles, with a 2.13 m (7 ft) non-volley zone, the kitchen, each side of the net.", "net": "86 cm (34 in) in the middle, 91 cm (36 in) at the sidelines", "walls": "None. The lines decide in or out."},
}
vs_q = lambda qid, label, opts: f'<div class="q vsq" data-q="{qid}"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
# Points per answer: tennis, padel, pickleball.
VSQ = {
    "who": {"one": [2, 0, 1], "group": [1, 2, 2], "any": [1, 1, 1]},
    "fit": {"easy": [0, 1, 2], "mid": [1, 2, 1], "hard": [2, 1, 0]},
    "past": {"none": [0, 2, 2], "some": [1, 2, 1], "lots": [2, 1, 1]},
    "fun": {"walls": [0, 3, 0], "touch": [0, 1, 3], "power": [3, 1, 0]},
    "time": {"quick": [0, 1, 2], "hour": [1, 2, 1], "long": [2, 1, 0]},
}
VSWHY = {
    "t": "Tennis gives you the most space, the biggest serves and the most running. It is played singles or doubles, and it takes the longest to learn well, so it rewards players who enjoy practising technique.",
    "p": "Padel is almost always played as two against two on a small court with walls. The underhand serve and the glass keep the ball in play, so new players get real rallies early, and it is very social.",
    "k": "Pickleball has the smallest court, a light plastic ball and an underhand serve. Players often say it is the quickest of the three to pick up, and it is easy on the joints. Games are won with soft shots near the net as much as with power.",
}
vs = f'''<header class="hero"><div class="wrap"><h1>Padel vs tennis vs pickleball.</h1>
<p class="lead">Three racket sports, three very different games. See the courts drawn to the same scale, compare the rules side by side, then answer five quick questions to see which one suits you best.</p>
{quick("Padel is played almost always in doubles on a 20 × 10 m court closed in by glass walls you can play off, with a solid racket full of holes and a low-pressure felt ball. Tennis has the biggest court (23.77 × 10.97 m for doubles), no walls and an overhead serve. Pickleball has the smallest court (13.41 × 6.10 m, or 44 × 20 ft), a solid paddle, a plastic ball and a no-volley zone called the kitchen. Padel and pickleball are not the same sport.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="vs-layout" id="vs">
<div class="court-art vs-art"><div class="vs-bar"><div class="seg" id="vs-show" role="group" aria-label="Show court"><button type="button" data-v="all" aria-pressed="true">All three</button><button type="button" data-v="t" aria-pressed="false">Tennis</button><button type="button" data-v="p" aria-pressed="false">Padel</button><button type="button" data-v="k" aria-pressed="false">Pickleball</button></div>
<div class="seg" id="vs-unit" role="group" aria-label="Units"><button type="button" data-v="m" aria-pressed="true">Metres</button><button type="button" data-v="ft" aria-pressed="false">Feet</button></div></div>
{VS_SVG}
<ul class="vs-key"><li><i class="k-t"></i>Tennis</li><li><i class="k-p"></i>Padel</li><li><i class="k-k"></i>Pickleball</li></ul></div>
<aside class="card zpanel" id="vs-info" aria-live="polite"></aside>
</div></div></section>
{AD.format("vs-mid")}
<section><div class="wrap"><div class="sh"><h2>What is the difference between padel, tennis and pickleball?</h2><p class="muted">The main rules of each sport, side by side.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt vs-t"><thead><tr><th scope="col"></th><th scope="col">Padel</th><th scope="col">Tennis</th><th scope="col">Pickleball</th></tr></thead><tbody>
<tr><th scope="row">Court</th><td>20 × 10 m</td><td>23.77 × 10.97 m (doubles)</td><td>13.41 × 6.10 m (44 × 20 ft)</td></tr>
<tr><th scope="row">Walls</th><td>Yes, glass and fence, part of the game</td><td>No</td><td>No</td></tr>
<tr><th scope="row">Net in the middle</th><td>88 cm</td><td>About 91 cm</td><td>86 cm (34 in)</td></tr>
<tr><th scope="row">Players</th><td>Almost always doubles</td><td>Singles or doubles</td><td>Singles or doubles</td></tr>
<tr><th scope="row">Serve</th><td>Underhand, after a bounce, hit at or below the waist, diagonally</td><td>Usually overhead, no bounce needed</td><td>Underhand, below the waist, diagonally</td></tr>
<tr><th scope="row">Special rule</th><td>Ball may hit the walls after one bounce</td><td>None like it</td><td>No volleys in the kitchen; the ball must bounce once on each side first</td></tr>
<tr><th scope="row">Scoring</th><td>15, 30, 40, game; sets to six; golden point or Star Point at 40-40 in many games</td><td>15, 30, 40, game; sets to six</td><td>Games to 11, win by 2; traditionally only the serving side scores</td></tr>
<tr><th scope="row">Racket</th><td>Solid, no strings, with holes</td><td>Strung racket</td><td>Solid paddle, no holes</td></tr>
<tr><th scope="row">Ball</th><td>Felt ball with lower pressure than tennis</td><td>Pressurised felt ball</td><td>Light plastic ball with holes</td></tr>
<tr><th scope="row">Learning curve</th><td>Moderate: rallies come quickly</td><td>Steepest</td><td>Quickest to pick up</td></tr>
<tr><th scope="row">Body</th><td>Quick reactions, short sprints, lots of bending</td><td>Most running and endurance</td><td>Lowest impact, balance and touch</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Padel figures from the FIP rules (see our <a href="{href("court-dimensions.html")}">padel court dimensions</a>). Pickleball court, net, kitchen and scoring from USA Pickleball. Tennis court and net from the ITF rules of tennis. Local leagues can use other formats.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which sport suits you: padel, tennis or pickleball?</h2><p class="muted">Five questions, no right answers.</p></div>
<div class="quiz" id="vsq">
<div>
{vs_q("who", "1. Who will you usually play with?", [("one", "One friend"), ("group", "Three friends or a group"), ("any", "Either")])}
{vs_q("fit", "2. How hard do you want to work?", [("easy", "Gentle on my joints"), ("mid", "A good sweat"), ("hard", "Lots of running")])}
{vs_q("past", "3. Have you played a racket sport before?", [("none", "Never"), ("some", "A little"), ("lots", "Yes, quite a lot")])}
{vs_q("fun", "4. What sounds most fun?", [("walls", "Long rallies off the walls"), ("touch", "Soft, clever shots at the net"), ("power", "Big serves and an open court")])}
{vs_q("time", "5. How long until you want to enjoy real games?", [("quick", "The first session"), ("hour", "A few weeks is fine"), ("long", "Happy to learn for months")])}
<button class="btn sm" type="button" id="vsq-reset">Start again</button>
</div>
<aside class="result" id="vsq-out" aria-live="polite"><h2>Your match</h2><p>Answer the questions and your best fit appears here. You can change any answer.</p></aside>
</div></div></section>
<section><div class="wrap"><div class="sh"><h2>What makes padel different from tennis and pickleball?</h2></div><div class="grid">
<div class="card"><span class="pill b">Padel</span><h3 style="margin-top:10px">The walls change everything</h3><p>In padel the ball can bounce once and then hit the glass, and you can still play it. That gives you a second chance on many shots, so rallies last longer. Read the <a href="{href("wall-rules.html")}">wall and fence rules</a>.</p></div>
<div class="card"><span class="pill i">Tennis</span><h3 style="margin-top:10px">Space and the serve</h3><p>A tennis court is the biggest of the three, and the overhead serve is a weapon. You need more running and more technique before rallies feel easy.</p></div>
<div class="card"><span class="pill a">Pickleball</span><h3 style="margin-top:10px">The kitchen</h3><p>Pickleball has a 7 ft (2.13 m) zone each side of the net where you can't volley. It stops players smashing from the net, so soft drop shots, called dinks, matter a lot.</p></div>
<div class="card"><span class="pill b">Padel</span><h3 style="margin-top:10px">Scoring like tennis</h3><p>Padel uses the tennis count, but at 40-40 many games use a golden point or the newer Star Point. Keep track with our <a href="{href("score.html")}">score keeper</a> and see <a href="{href("golden-point-star-point.html")}">golden point vs Star Point</a>.</p></div>
<div class="card"><span class="pill a">Pickleball</span><h3 style="margin-top:10px">Only servers score</h3><p>In the traditional pickleball format, only the serving side can win points, and a game goes to 11, won by two. Some events now try rally scoring, where every rally counts.</p></div>
<div class="card"><span class="pill i">All three</span><h3 style="margin-top:10px">Different kit</h3><p>A tennis racket has strings. A padel racket is solid foam with holes. A pickleball paddle is solid and flat. Each sport also has its own ball, so you can't swap them.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is padel easy to learn if you play tennis or pickleball?</h2></div><div class="grid">
<div class="card"><h3>From tennis</h3><p>Your volleys and footwork help a lot. The hard part is letting the ball pass you and come off the glass instead of hitting it early. Shorten your swing: big tennis swings send the ball into the back glass. Start with the <a href="{href("shots.html")}">shot library</a>.</p></div>
<div class="card"><h3>From pickleball</h3><p>You already know the underhand serve and how to win at the net. In padel the serve must bounce first, there is no kitchen, and lobs over the net players are a main weapon. Learn <a href="{href("positioning.html")}">where to stand</a> as a pair.</p></div>
<div class="card"><h3>Brand new</h3><p>Padel is a good first racket sport: the court is small and the walls keep the ball in. Read the <a href="{href("beginners.html")}">first match checklist</a> and find a <a href="{href("racket-finder.html")}">racket that suits you</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Ready to try padel?</h3><p>The <a href="{href("beginners.html")}">beginner's guide</a> has the rules for a first game, and the <a href="{href("padel-equipment.html")}">kit planner</a> shows what to bring.</p></div>
<div class="card"><h3>Learn the walls</h3><p>The glass is the biggest change from tennis and pickleball. Try the <a href="{href("wall-rules.html")}">wall and fence rules</a> checker. Played racquetball or platform tennis? See <a href="{href("padel-vs-racquetball.html")}">how padel compares</a>.</p></div>
<div class="card"><h3>Playing with your kids?</h3><p>Padel is easy for families to share. Find the right junior weight in the <a href="{href("padel-racket-for-kids.html")}">padel racket for kids</a> finder.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Trying padel for the first time?</h3><p>Most clubs rent rackets. If you want your own, start with a forgiving round racket and proper court shoes.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li></ul>{AFF_NOTE}</div></div></section>'''
vs_faq = [
    ("What is the difference between padel and pickleball?", "Padel is played on a 20 × 10 m court with glass walls you can use, with a solid holed racket and a felt ball, almost always in doubles. Pickleball is played on a smaller 44 × 20 ft court with no walls, a solid paddle and a plastic ball, and it has a non-volley zone called the kitchen."),
    ("Is padel easier than tennis?", "For most beginners, yes. The court is smaller, the serve is underhand and the walls keep the ball in play, so rallies come much sooner than in tennis."),
    ("Is padel or pickleball easier to learn?", "Both are quick to learn. Pickleball is often called the easiest of the three to pick up, and padel the easiest way into a racket sport with walls. Many people play both."),
    ("Which court is bigger, padel or pickleball?", "Padel. A padel court is 20 × 10 m (200 m²). A pickleball court is 13.41 × 6.10 m (about 82 m²), so it is less than half the size."),
    ("Is a padel court smaller than a tennis court?", "Yes. A padel court is 20 × 10 m. A tennis doubles court is 23.77 × 10.97 m, so padel covers about three quarters of the area, and the walls make it feel even smaller."),
    ("Is padel scored like tennis?", "Yes: 15, 30, 40 and game, with sets to six. Many padel games use a golden point at 40-40, and the pro tours use Star Point from 2026."),
    ("Are padel and pickleball the same thing?", "No. They are different sports. Padel has glass walls, a felt ball and a racket with holes, on a 20 × 10 m court. Pickleball has no walls, a plastic ball with holes and a solid paddle, on a 44 × 20 ft court with a kitchen zone."),
    ("Can you use a tennis racket or pickleball paddle for padel?", "No. Padel rackets are solid with holes and no strings, and the FIP rules set their size. Each sport has its own racket and ball."),
    ("Which is the best workout: padel, tennis or pickleball?", "Tennis usually means the most running. Padel is lots of short, quick movements and bending. Pickleball is the lowest impact of the three. Any of them is good exercise if you play regularly."),
]
page("padel-vs-tennis-vs-pickleball.html", "Padel vs Tennis vs Pickleball: Differences + Courts to Scale",
     "Padel vs tennis vs pickleball: court size, walls, serve, scoring and kit side by side, the three courts drawn to scale, and a quiz to pick your sport.",
     vs + f'<script>window.VS={json.dumps({"c": VS, "q": VSQ, "why": VSWHY})};</script>', vs_faq, "Padel vs tennis vs pickleball")

# ---------------- RACKET WEIGHT AND BALANCE ----------------
def _rbr(k):
    return f'''<div class="rb-r" data-r="{k}"><div class="rb-rh"><h3><i class="rb-dot rb-{k.lower()}"></i>Racket {k}</h3></div>
<label class="rb-l" for="rb-w-{k}">Weight <output id="rb-wo-{k}">360 g</output></label>
<div class="rb-in"><input type="range" id="rb-w-{k}" min="320" max="395" step="1" value="360" data-f="w"><input type="number" min="320" max="395" step="1" value="360" data-f="w" aria-label="Racket {k} weight in grams"><span>g</span></div>
<label class="rb-l" for="rb-b-{k}">Balance point <output id="rb-bo-{k}">265 mm</output></label>
<div class="rb-in"><input type="range" id="rb-b-{k}" min="240" max="295" step="1" value="265" data-f="b"><input type="number" min="240" max="295" step="1" value="265" data-f="b" aria-label="Racket {k} balance in millimetres from the butt"><span>mm</span></div>
<p class="rb-l">Shape</p><div class="opts rb-shape" role="group" aria-label="Racket {k} shape">{"".join(f'<button type="button" class="opt" data-v="{s}" aria-pressed="false">{n}</button>' for s, n in (("round", "Round"), ("teardrop", "Teardrop"), ("diamond", "Diamond")))}</div>
<p class="rb-l">Or fill with a typical racket</p><div class="rb-pre">{"".join(f'<button type="button" class="btn ghost sm" data-p="{s}">{n}</button>' for s, n in (("round", "Typical round"), ("teardrop", "Typical teardrop"), ("diamond", "Typical diamond")))}</div>
</div>'''

rb = f'''<header class="hero"><div class="wrap"><h1>Padel racket weight and balance, decoded.</h1>
<p class="lead">Type in the weight and balance from the spec sheet. See where the weight sits on a racket drawn to scale, what it means for power, speed and your arm, and how two rackets compare.</p>
{quick("Balance is the distance in mm from the bottom of the handle to the point where the racket balances. Under about 260 mm is low (head-light: control, quick hands, easier on the arm), about 260 to 270 mm is medium, and over about 270 mm is high (head-heavy: more power, more load on the elbow). Most adult rackets weigh about 345 to 385 g; most improving players do well at about 355 to 370 g.")}</div></header>
<section style="padding-top:10px"><div class="wrap rb-layout" id="rb">
<div class="card rb-form">{_rbr("A")}{_rbr("B")}
<p class="muted" style="margin:6px 0 0;font-size:.9rem">Balance is measured in millimetres from the bottom of the handle. No figure on the box? <a href="#measure">Find it at home</a> in a minute.</p></div>
<aside class="result rb-out" aria-live="polite">
<svg class="rb-svg" id="rb-svg" viewBox="0 0 600 520" role="img" aria-label="Racket A and racket B drawn to scale with their balance points marked"></svg>
<ul class="rb-key"><li><i class="rb-dot rb-a"></i>Racket A</li><li><i class="rb-dot rb-b"></i>Racket B</li><li><i class="rb-dash"></i>Middle of the racket (227.5 mm)</li></ul>
<div id="rb-txt"></div>
<button class="btn sm lime" type="button" id="rb-copy">Copy comparison</button>
</aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><p class="muted" style="max-width:80ch">The bars are a rough guide worked out from weight and balance only. The core foam, face material, thickness and how stiff the racket is also change how it feels, so try a racket before you buy when you can.</p></div></section>
{AD.format("balance-mid")}
<section><div class="wrap"><div class="sh"><h2>What is a good balance for a padel racket?</h2><p class="muted">Every padel racket has more weight above its middle point.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Balance</th><th scope="col">Rough balance point</th><th scope="col">How it feels</th><th scope="col">Often found on</th></tr></thead><tbody>
<tr><td>Low (head-light)</td><td>Under about 260 mm</td><td>Quick to move, easy to control, gentler on the arm. Less free power.</td><td>Round rackets</td></tr>
<tr><td>Medium (even)</td><td>About 260 to 270 mm</td><td>A mix of control and power.</td><td>Teardrop rackets</td></tr>
<tr><td>High (head-heavy)</td><td>Over about 270 mm</td><td>More weight behind smashes and hard hits. Slower at the net and more load on the elbow and shoulder.</td><td>Diamond rackets</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Shops and brands draw these lines in slightly different places, so treat them as a guide. A racket is 45.5 cm long at most, so its middle is 227.5 mm from the bottom. Most rackets balance well above that, between about 250 and 285 mm.</p>
<div class="grid" style="margin-top:18px">
<div class="card"><h3>Shape is only a clue</h3><p>Round rackets are usually head-light and diamond rackets head-heavy, but not always. Some round rackets are quite head-heavy, and some diamonds are fairly even. The balance figure tells you more than the shape.</p></div>
<div class="card"><h3>Shape moves the sweet spot</h3><p>The sweet spot is the part of the face that gives the cleanest hit. On a round racket it is big and in the middle. On a teardrop it sits a little higher. On a diamond it is smaller and near the top. Compare all three: <a href="{href("padel-racket-shapes.html")}">racket shapes</a>.</p></div>
<div class="card"><h3>Balance changes the swing</h3><p>Two rackets with the same weight can feel very different. The one with the weight further up feels heavier when you swing it, because more of the weight is far from your hand.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How heavy should a padel racket be?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Weight</th><th scope="col">Range</th><th scope="col">Tends to suit</th></tr></thead><tbody>
<tr><td>Light</td><td>Under about 355 g</td><td>New players, juniors, players with sore elbows or shoulders, and anyone who wants fast hands at the net.</td></tr>
<tr><td>Medium</td><td>About 355 to 370 g</td><td>Most improving players. A good mix of feel and power.</td></tr>
<tr><td>Heavy</td><td>Over about 370 g</td><td>Strong, experienced players who hit hard and want more power and stability.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Most adult rackets weigh between about 345 and 385 g. Weights on the box can be a few grams out, and many are given as a range, such as 360 to 375 g.</p></div></section>
<section style="padding-top:0" id="women"><div class="wrap"><div class="sh"><h2>What padel racket weight is best for women?</h2><p class="muted">Pick by strength, arm history and level, not by gender alone. Shop guides give these starting ranges.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Player</th><th scope="col">Starting range</th><th scope="col">Why</th></tr></thead><tbody>
<tr><td>New player, or sore elbow or shoulder</td><td>About 340 to 360 g</td><td>Easier to swing and to stop, so less load on the arm while technique is new.</td></tr>
<tr><td>Most women club players</td><td>About 345 to 360 g</td><td>The range most shop guides give as an average. A good mix of control and enough power.</td></tr>
<tr><td>Strong or experienced, hits hard</td><td>About 360 to 370 g</td><td>More stability on smashes and volleys against hard hitters.</td></tr>
<tr><td>Advanced attacking player</td><td>About 365 to 375 g</td><td>Close to what advanced players of any gender use. Only if your arm copes over a long match.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Balance counts as much as grams: a 355 g head-heavy racket can feel heavier than a 365 g head-light one, so check both in the decoder above. An overgrip adds about 8 g at the handle. Rackets sold as "women's" are usually just lighter or a different colour; the rules are the same for all rackets. The simple test: you should still swing it fast in the last game of a long match. Sources, checked 27 Nov 2026: Justpadel "Which weight padel racket should you choose?" (17 Jun 2026: women average 345-360 g, beginners and injury-prone 345-365 g, advanced 370-380 g), Zona de Padel "How to choose the weight of a padel racket" (3 Aug 2023: ranges by body weight, light under 355 g, overgrip about 8 g), HEAD "How to choose a padel racquet" (beginners and intermediates 340-360 g). Our own words.</p></div></section>
<section id="measure"><div class="wrap"><div class="sh"><h2>How do you measure padel racket balance at home?</h2><p class="muted">You need a table, a pencil and a tape measure.</p></div>
<div class="grid">
<div class="card"><span class="pill b">Step 1</span><h3 style="margin-top:10px">Set it up as you play</h3><p>Leave the overgrip, frame protector and any tape on the racket. They all change the balance a little.</p></div>
<div class="card"><span class="pill b">Step 2</span><h3 style="margin-top:10px">Find the level point</h3><p>Lay a round pencil on a table. Put the racket across it, face flat, and slide it slowly until it rests level without tipping either way.</p></div>
<div class="card"><span class="pill b">Step 3</span><h3 style="margin-top:10px">Measure</h3><p>Mark the spot where the pencil touches. Measure from the very bottom of the handle to that mark in millimetres. That number is the balance point.</p></div>
<div class="card"><span class="pill i">Weight</span><h3 style="margin-top:10px">Weigh it too</h3><p>A kitchen scale works. Weigh the racket as you play with it, then put both numbers into the decoder above.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What changes the balance of a racket?</h2></div><div class="grid">
<div class="card"><h3>Adding an overgrip</h3><p>An overgrip adds a few grams at the handle, so the balance moves a little towards your hand and the racket feels a touch lighter to swing. Two overgrips move it more. See our <a href="{href("racket-finder.html")}#grip">grip and overgrip tips</a>.</p></div>
<div class="card"><h3>Frame protector tape</h3><p>Tape around the top of the frame protects it from scrapes on the floor and walls, but it adds weight at the head. The balance moves up and the racket feels heavier to swing.</p></div>
<div class="card"><h3>Lead or weight tape</h3><p>Some players add thin weight tape to tune a racket. Put it near the top for more power, or near the handle for more control. The rules allow added weights if they are a sensible size and position.</p></div>
</div></div></section>
<section><div class="wrap"><div class="sh"><h2>Is there a weight or size limit for padel rackets?</h2><p class="muted">From the FIP Rules of Padel, in force from 1 January 2026.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Part</th><th scope="col">Limit</th></tr></thead><tbody>
<tr><td>Total length</td><td>45.5 cm at most</td></tr>
<tr><td>Handle</td><td>20 cm long at most, 50 mm wide and 50 mm thick at most</td></tr>
<tr><td>Head</td><td>26 cm wide and 38 mm thick at most (a small 2.5% allowance when measuring thickness)</td></tr>
<tr><td>Holes</td><td>Any number. In the main area each round hole is 9 to 13 mm across</td></tr>
<tr><td>Faces</td><td>Both must be flat. They can be smooth or rough</td></tr>
<tr><td>Wrist cord</td><td>Must be fixed to the handle, not stretchy, 35 cm long at most, and worn on your wrist</td></tr>
<tr><td>Weight and balance</td><td>No limit. You can choose any weight and balance</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">If your cord breaks or you drop the racket during a point, your pair loses that point. More in our <a href="{href("rules.html")}">padel rules guide</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Not sure what weight?</h3><p>Get a gram range for your level, strength and arm with the <a href="{href("padel-racket-weight.html")}">padel racket weight calculator</a>.</p></div>
<div class="card"><h3>Ready to upgrade?</h3><p>Moving on from your first racket? The <a href="{href("intermediate-padel-racket.html")}">intermediate racket upgrade check</a> shows which specs to keep and which to change.</p></div>
<div class="card"><h3>Take the racket finder</h3><p>Three quick questions give you the shape, weight, balance, core and face that suit your level and style. <a href="{href("racket-finder.html")}">Open the racket finder</a>.</p></div>
<div class="card"><h3>Choosing between two?</h3><p>Enter shape, weight, balance, core and face for both and see which fits you: <a href="{href("compare-padel-rackets.html")}">compare two padel rackets</a>.</p></div>
<div class="card"><h3>Know your level first</h3><p>Weight and balance advice depends a lot on how long you have played. <a href="{href("level-calculator.html")}">Check your padel level</a>.</p></div>
<div class="card"><h3>Sore elbow?</h3><p>Head-heavy and heavy rackets load the arm more. Check your racket and habits with the <a href="{href("padel-elbow.html")}">padel elbow arm-load check</a>, and see what helps in <a href="{href("padel-injuries.html")}">padel injuries</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop rackets by shape</h3><p>Use the decoder on any racket you like the look of: most shops list the weight, and many list the balance.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond rackets</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
rb_faq = [
    ("What is a good balance for a padel racket?", "For beginners and players who want control, a low balance of under about 260 mm from the bottom of the handle. For a mix of control and power, about 260 to 270 mm. Hard hitters who want power often choose over about 270 mm."),
    ("How is padel racket balance measured?", "It is the distance in millimetres from the bottom of the handle to the point where the racket balances level. Rest it across a pencil, slide it until it sits level, and measure to that point."),
    ("What does head-heavy mean on a padel racket?", "More of the weight sits towards the top of the head. That adds power to smashes and hard shots, but the racket is slower to move and puts more load on your elbow and shoulder."),
    ("How heavy should my padel racket be?", "Most adult rackets weigh about 345 to 385 g. New players and those with sore arms usually do best under about 360 g; strong, experienced players often choose 365 to 375 g or more."),
    ("Is a lighter padel racket better for tennis elbow?", "A lighter racket with a low balance usually puts less strain on the arm, and a soft core helps too. If the pain continues, see a doctor or physio."),
    ("Does an overgrip change the balance?", "A little. It adds weight at the handle, so the balance point moves towards your hand. Frame protector tape does the opposite and moves it towards the head."),
    ("What weight and balance suit an intermediate padel player?", "Most intermediate players do well at about 360 to 370 g with a medium balance of about 260 to 270 mm, usually on a teardrop racket. Go lighter and lower if your arm gets sore."),
    ("Is a head-heavy padel racket bad for your elbow?", "It puts more load on the elbow and shoulder than a head-light racket of the same weight. If you have elbow pain, choose a low balance and a lighter, softer racket, and see a doctor or physio if it continues."),
    ("What weight padel racket should a woman use?", "Most women club players start at about 345 to 360 g. Go lighter, about 340 to 355 g, if you are new or have a sore arm, and heavier, 360 to 370 g or more, if you are strong and hit hard. Choose by strength and arm health, not by gender alone."),
    ("Are women's padel rackets different?", "Usually only lighter or a different colour. The rules are the same for every racket. A light men's or unisex racket can suit a woman just as well, so compare the weight and balance, not the label."),
    ("Is there a weight limit for padel rackets?", "No. The FIP rules limit the size of the racket, 45.5 cm long, 26 cm wide and 38 mm thick at most, but not its weight or balance."),
]
RB_PRE = {"round": [355, 255, "round"], "teardrop": [362, 265, "teardrop"], "diamond": [368, 275, "diamond"]}
page("racket-balance.html", "Padel Racket Weight and Balance Explained: Free Spec Decoder | Padel Glass Box",
     "What is a good padel racket weight and balance? Balance in mm, weight bands in grams, and a free decoder that shows the balance point on a to-scale racket.",
     rb + f'<script>window.RB={json.dumps(RB_PRE)};</script>', rb_faq, "Racket weight and balance")

# ---------------- ROUND ROBIN (FIXED PAIRS) ----------------
def _rr_row(n):
    rounds = n - 1 if n % 2 == 0 else n
    per = n // 2
    return f"<tr><td>{n} pairs</td><td>{n * (n - 1) // 2}</td><td>{rounds}</td><td>{per}</td><td>{'None' if n % 2 == 0 else 'One pair each round'}</td></tr>"
rr = f'''<header class="hero"><div class="wrap"><h1>Padel round robin generator for fixed pairs.</h1>
<p class="lead">Every pair plays every other pair once. Type in your teams, pick your courts and get the full schedule, with a standings table that updates as you enter the games. Free, no sign-up, saved on this device.</p>
{quick("A round robin with 4 pairs is 6 matches over 3 rounds; 6 pairs is 15 matches over 5 rounds; 8 pairs is 28 matches over 7 rounds. With an even number of pairs you need one less round than pairs. With an odd number, every pair sits out one round.")}</div></header>
<section style="padding-top:10px"><div class="wrap gen">
<div class="gen-main">
<div class="card" id="rr-setup">
<h2 style="font-size:1.6rem">Set up your round robin</h2>
<div class="q"><h3><label for="rr-names">Pairs, one team per line (3 to 16)</label></h3><textarea class="search" id="rr-names" rows="7" placeholder="Sam &amp; Priya&#10;Omar &amp; Lucia&#10;Ben &amp; Aisha&#10;..."></textarea><p class="muted" id="rr-count" style="margin:-6px 0 0"></p></div>
<div class="q"><h3>How do you score each match?</h3><div class="opts" data-rr="fmt" role="group" aria-label="Match format"><button class="opt" type="button" data-v="set" aria-pressed="true">One set (games)</button><button class="opt" type="button" data-v="race" aria-pressed="false">Race to 4 games</button><button class="opt" type="button" data-v="free" aria-pressed="false">Timed or any score</button></div><p class="muted" id="rr-fmt-note" style="margin:10px 0 0"></p></div>
<div class="q"><h3>Points in the table</h3><div class="opts" data-rr="pts" role="group" aria-label="Table points"><button class="opt" type="button" data-v="w" aria-pressed="true">Rank by wins</button><button class="opt" type="button" data-v="3" aria-pressed="false">3 for a win, 1 for a draw</button></div></div>
<div class="gen-nums"><div class="q"><h3><label for="rr-courts">Courts</label></h3><input class="search" id="rr-courts" type="number" min="1" max="8" value="2" inputmode="numeric"></div>
<div class="q"><h3><label for="rr-legs">Play each pair</label></h3><select class="search" id="rr-legs"><option value="1">Once</option><option value="2">Twice</option></select></div></div>
<p class="msg" id="rr-err" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:4px"><button class="btn lime" type="button" id="rr-start">Make the schedule</button><button class="btn ghost" type="button" id="rr-demo">Fill 6 sample pairs</button></div>
</div>
<div id="rr-live" hidden>
<div class="card gen-bar"><div><span class="pill b" id="rr-sum"></span></div><div class="btns" style="margin:0"><button class="btn ghost sm" type="button" id="rr-copy">Copy table</button><button class="btn ghost sm" type="button" id="rr-new">New round robin</button></div></div>
<div id="rr-list"></div>
</div>
</div>
<aside class="gen-side"><div class="lb" id="rr-board"><h2>Standings</h2><p>Make the schedule and enter the games to see the table.</p></div></aside>
</div></section>
{AD.format("rr-mid")}
<section><div class="wrap"><div class="sh"><h2>How many matches is a round robin?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Teams</th><th scope="col">Matches</th><th scope="col">Rounds</th><th scope="col">Matches per round</th><th scope="col">Who sits out</th></tr></thead><tbody>
{"".join(_rr_row(n) for n in (3, 4, 5, 6, 7, 8, 10, 12))}
</tbody></table></div>
<p class="muted" style="margin-top:14px">The maths: with N pairs there are N × (N − 1) ÷ 2 matches. With fewer courts than matches in a round, the tool splits each round into slots (slot 1, slot 2 and so on) that you play one after the other.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How does a padel round robin work?</h2></div><div class="grid">
<div class="card"><h3>Fixed pairs, everyone meets</h3><p>You keep the same partner all event. Each pair plays each other pair once (or twice). There are no knock-outs, so every team gets the same number of matches.</p></div>
<div class="card"><h3>Round robin vs Americano</h3><p>In an <a href="{href("americano.html")}">Americano</a> you change partner every round and score as a single player. A round robin is for teams that want to stay together, like a club league or a box league.</p></div>
<div class="card"><h3>Odd number of pairs</h3><p>With 5, 7 or 9 pairs, one team rests each round. The tool shows who is resting, and every pair rests exactly once in each cycle.</p></div>
<div class="card"><h3>Pick a match length</h3><p>A full set gives a proper match. A race to 4 games (or a timed match) keeps a big group moving on one court booking. Agree on <a href="{href("golden-point-star-point.html")}">golden point or advantage</a> before you start.</p></div>
<div class="card"><h3>How the table is sorted</h3><p>By default: wins (or points), then game difference, then games won, then the result between the tied pairs. Your league can use other rules, so check them first.</p></div>
<div class="card"><h3>Turn it into a final</h3><p>Many groups finish with a final between the top two pairs. Use the <a href="{href("score.html")}">score keeper</a> on a phone at the net for that match.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Mixing partners instead?</h3><p>Use the <a href="{href("americano.html")}">Americano and Mexicano draw maker</a>.</p></div>
<div class="card"><h3>Pairs of similar level</h3><p>Ask everyone to run the <a href="{href("level-calculator.html")}">level calculator</a> so the teams are fair.</p></div>
<div class="card"><h3>Running it all season?</h3><p>Use the <a href="{href("ladder.html")}">padel ladder tracker</a> and let pairs challenge each other.</p></div>
</div></div></section>'''
rr_faq = [
    ("How many matches are in a round robin with 4 teams?", "Six matches over three rounds. Each pair plays three matches, one against each other pair. With two courts, each round fits on court at the same time."),
    ("How many rounds does a round robin need?", "With an even number of pairs, one less than the number of pairs (6 pairs = 5 rounds). With an odd number, the same number as pairs (5 pairs = 5 rounds), because one pair rests each round."),
    ("What is the difference between a round robin and an Americano in padel?", "In a round robin you keep the same partner and play every other pair. In an Americano you change partner every round and collect points as a single player."),
    ("How is a padel round robin table sorted?", "Most leagues rank by matches won or league points first. Common tie-breaks are game difference, games won and then the head-to-head result. This tool uses that order; your league may use its own."),
    ("What if we have an odd number of pairs?", "One pair sits out each round. Every pair rests once, so everyone still plays the same number of matches."),
    ("Can we play everyone twice?", "Yes. Choose 'Twice' and the tool repeats the schedule, so each pair meets every other pair two times, like a home and away league."),
]
page("round-robin.html", "Padel Round Robin Generator for Fixed Pairs: Schedule, Table",
     "Free padel round robin generator for fixed pairs. Enter 3 to 16 teams and your courts to get every round, then enter the games for a live standings table.",
     rr, rr_faq, "Round robin generator")

# ---------------- PADEL SHOES ----------------
SOLE_SVG = {
    "herring": '<svg viewBox="0 0 120 220" class="sole-svg" role="img" aria-label="Herringbone sole: a zig-zag pattern from toe to heel"><defs><clipPath id="sc1"><path d="M60 6C92 6 108 40 108 80C108 120 98 140 96 170C94 200 80 214 60 214C40 214 26 200 24 170C22 140 12 120 12 80C12 40 28 6 60 6Z"/></clipPath></defs><path d="M60 6C92 6 108 40 108 80C108 120 98 140 96 170C94 200 80 214 60 214C40 214 26 200 24 170C22 140 12 120 12 80C12 40 28 6 60 6Z" fill="#0e2468"/><g clip-path="url(#sc1)" stroke="#d4f53c" stroke-width="5" fill="none">' + "".join(f'<path d="M0 {y}L30 {y-12}L60 {y}L90 {y-12}L120 {y}"/>' for y in range(20, 232, 14)) + '</g></svg>',
    "omni": '<svg viewBox="0 0 120 220" class="sole-svg" role="img" aria-label="Omni sole: many small rubber studs"><defs><clipPath id="sc2"><path d="M60 6C92 6 108 40 108 80C108 120 98 140 96 170C94 200 80 214 60 214C40 214 26 200 24 170C22 140 12 120 12 80C12 40 28 6 60 6Z"/></clipPath></defs><path d="M60 6C92 6 108 40 108 80C108 120 98 140 96 170C94 200 80 214 60 214C40 214 26 200 24 170C22 140 12 120 12 80C12 40 28 6 60 6Z" fill="#0e2468"/><g clip-path="url(#sc2)" fill="#d4f53c">' + "".join(f'<circle cx="{x + (7 if (y // 14) % 2 else 0)}" cy="{y}" r="3.6"/>' for y in range(14, 220, 14) for x in range(10, 120, 14)) + '</g></svg>',
    "hybrid": '<svg viewBox="0 0 120 220" class="sole-svg" role="img" aria-label="Hybrid sole: zig-zag on the outer edge, small studs in the middle"><defs><clipPath id="sc3"><path d="M60 6C92 6 108 40 108 80C108 120 98 140 96 170C94 200 80 214 60 214C40 214 26 200 24 170C22 140 12 120 12 80C12 40 28 6 60 6Z"/></clipPath><clipPath id="sc3i"><ellipse cx="60" cy="110" rx="26" ry="88"/></clipPath></defs><path d="M60 6C92 6 108 40 108 80C108 120 98 140 96 170C94 200 80 214 60 214C40 214 26 200 24 170C22 140 12 120 12 80C12 40 28 6 60 6Z" fill="#0e2468"/><g clip-path="url(#sc3)" stroke="#d4f53c" stroke-width="5" fill="none">' + "".join(f'<path d="M0 {y}L30 {y-12}L60 {y}L90 {y-12}L120 {y}"/>' for y in range(20, 232, 14)) + '</g><ellipse cx="60" cy="110" rx="28" ry="90" fill="#0e2468"/><g clip-path="url(#sc3i)" fill="#9cc4ea">' + "".join(f'<circle cx="{x + (6 if (y // 12) % 2 else 0)}" cy="{y}" r="3"/>' for y in range(24, 200, 12) for x in range(34, 90, 12)) + '</g></svg>',
}
def _sq(qid, label, opts):
    return f'<div class="q sh-q" data-q="{qid}"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
shoes = f'''<header class="hero"><div class="wrap"><h1>Padel shoes: which sole do you need?</h1>
<p class="lead">Grip is the first thing to get right. Answer four questions about your courts and your game and see which sole pattern to look for, how much cushioning, and when to replace your shoes.</p>
{quick("For most padel courts (artificial grass with sand), look for a herringbone (zig-zag) sole. On low-sand or carpet-style courts, an omni or hybrid sole grips better. Don't play in running shoes. If you play every week, plan on new shoes about every 4 to 6 months.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="shoe">
<div>
{_sq("court", "What are your usual courts like?", [("sand", "Grass with lots of loose sand"), ("low", "Little or no sand, or carpet-like"), ("mix", "It changes between clubs"), ("dk", "Not sure")])}
{_sq("often", "How often do you play?", [("1", "A few times a month"), ("2", "Once a week"), ("3", "Two or more times a week")])}
{_sq("now", "What do you wear now?", [("run", "Running or gym shoes"), ("ten", "Tennis shoes"), ("pad", "Padel shoes"), ("none", "Nothing yet")])}
{_sq("feel", "Anything you want more of?", [("grip", "More grip, I slip"), ("soft", "More cushioning, my legs ache"), ("stab", "More support, I roll my ankle"), ("ok", "Nothing in particular")])}
<button class="btn sm" type="button" id="shoe-reset">Start again</button>
</div>
<aside class="result" id="shoe-out" aria-live="polite"><h2>Your shoe match</h2><p>Answer the questions and your sole type and tips appear here.</p></aside>
</div></div></section>
{AD.format("shoes-mid")}
<section><div class="wrap"><div class="sh"><h2>What are the types of padel shoe sole?</h2></div><div class="grid sole-grid">
<div class="card">{SOLE_SVG["herring"]}<h3>Herringbone</h3><p>A zig-zag pattern from toe to heel. It is the classic padel sole: the grooves let sand pass through, so you can slide and stop on sandy artificial grass. It has the most grip of the three.</p><span class="pill b">Best for sandy courts</span></div>
<div class="card">{SOLE_SVG["omni"]}<h3>Omni</h3><p>Lots of small rubber studs. It grips well on courts with little sand, but on a very sandy court it can feel like you are on ice skates.</p><span class="pill i">Best for low-sand courts</span></div>
<div class="card">{SOLE_SVG["hybrid"]}<h3>Hybrid</h3><p>Zig-zag on the outside, where you push off when you change direction, and studs or a softer pattern in the middle. A good choice if you play at different clubs.</p><span class="pill">Good on most courts</span></div>
</div>
<p class="muted" style="margin-top:14px">Our own drawings. Real soles vary a lot; brands use their own names and patterns.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel shoes vs tennis shoes vs running shoes</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col"></th><th scope="col">Padel shoes</th><th scope="col">Tennis shoes</th><th scope="col">Running shoes</th></tr></thead><tbody>
<tr><td>Made for</td><td>Quick stops, turns and short sprints on grass with sand</td><td>Long side-to-side slides on hard or clay courts</td><td>Running forward</td></tr>
<tr><td>Sole</td><td>Herringbone, omni or hybrid</td><td>Flatter on hard-court models; herringbone on clay models</td><td>Soft, smooth tread</td></tr>
<tr><td>Grip on padel turf</td><td>Best</td><td>Usually OK, but can be too much or too little</td><td>Poor, you can slip</td></tr>
<tr><td>Support</td><td>Stable through the middle of the foot</td><td>Strong side support, firm heel</td><td>Little side support</td></tr>
<tr><td>Good for padel?</td><td>Yes</td><td>OK to start</td><td>No</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Guides disagree about clay-court tennis shoes: some say their herringbone sole works well for padel, others say they wear out fast on padel turf. They are fine to try padel in; if you play every week, padel shoes are worth it.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is it time for new padel shoes?</h2></div>
<div class="card"><ul class="check" id="shoe-wear">
<li><label><input type="checkbox" data-w="2"><span>The zig-zag or studs are worn smooth under the ball of your foot</span></label></li>
<li><label><input type="checkbox" data-w="2"><span>You slip on turns where you used to stop easily</span></label></li>
<li><label><input type="checkbox" data-w="1"><span>The cushioning feels hard and your knees or feet ache more after games</span></label></li>
<li><label><input type="checkbox" data-w="1"><span>The upper is torn or your foot slides around inside</span></label></li>
<li><label><input type="checkbox" data-w="1"><span>You have played in them weekly for more than about 6 months</span></label></li>
</ul><p class="shoe-wv" id="shoe-wv" aria-live="polite">Tick anything that sounds like your shoes.</p></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How should padel shoes fit?</h2></div><div class="grid">
<div class="card"><h3>Snug, not tight</h3><p>Your heel should not lift and your foot should not slide when you stop. Tight shoes give blisters.</p></div>
<div class="card"><h3>Room for your toes</h3><p>Your foot moves forward when you stop hard. Leave a little space, about a thumb's width, in front of your longest toe.</p></div>
<div class="card"><h3>Check the width too</h3><p>Some models are narrow. If the sides press on your foot, try a wider model, not just a bigger size.</p></div>
<div class="card"><h3>Try them with your padel socks</h3><p>Shop later in the day, when feet are a little bigger, and wear the socks you play in.</p></div>
<div class="card"><h3>Comfortable from day one</h3><p>Padel shoes should feel good the first time. Wear new shoes for a short session before a long match.</p></div>
<div class="card"><h3>Pain that stays</h3><p>Shoes help, but they don't fix injuries. If pain in your feet, knees or ankles doesn't go away, see a doctor or physio.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Rest of your kit</h3><p>Find a racket that suits you with the <a href="{href("racket-finder.html")}">racket finder</a>, and see <a href="{href("padel-equipment.html")}">what else to bring and wear</a>.</p></div>
<div class="card"><h3>Before you play</h3><p>Look after your legs with the <a href="{href("warm-up.html")}">10-minute warm-up timer</a>.</p></div>
<div class="card"><h3>Check your balls</h3><p>Flat balls make you lunge more. Run the <a href="{href("padel-balls.html")}">dead ball checker</a>.</p></div>
<div class="card"><h3>Know your court</h3><p>Lots of sand, little sand or concrete? Check yours with the <a href="{href("padel-court-surfaces.html")}">court surface checker</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop padel shoes</h3><p>Check the sole type in the product details: herringbone for sandy courts, omni or hybrid for low-sand courts.</p><ul class="aff-links"><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>Rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
shoes_faq = [
    ("Do you need special shoes for padel?", "You can try padel in tennis shoes, but padel shoes grip the sandy artificial grass better and support quick stops and turns. Don't play in running shoes: they slip and give little side support."),
    ("What sole is best for padel shoes?", "Herringbone (a zig-zag pattern) for courts with lots of sand. Omni (small studs) or a hybrid sole for courts with little or no sand."),
    ("Can I use tennis shoes for padel?", "Yes, to start. They grip less well on padel turf and are made for different movement, so if you play every week, padel shoes are a good buy."),
    ("Can I play padel in running shoes?", "It's best not to. Running shoes are made for moving forward, so they have a smooth sole and little side support. That makes it easier to slip or roll an ankle on court."),
    ("How long do padel shoes last?", "If you play every week, about 4 to 6 months. If you play now and then, often a year or more. Replace them when the sole is worn smooth or the cushioning feels hard."),
    ("Should padel shoes be tight?", "Snug but not tight. Your heel shouldn't lift and your foot shouldn't slide, but leave a little room in front of your toes because your foot moves forward when you stop."),
    ("What is the difference between omni and herringbone soles?", "Herringbone has zig-zag grooves that let sand pass, so it grips on sandy courts. Omni has many small studs and grips better on courts with little sand."),
]
page("padel-shoes.html", "Padel Shoes Guide: Which Sole Do You Need? Free Shoe Finder | Padel Glass Box",
     "Which padel shoes do you need? Answer four questions to get your sole type (herringbone, omni or hybrid), compare with tennis shoes and check the fit.",
     shoes + '<script>window.SOLES=' + json.dumps({k: v.replace('id="sc', 'id="sm').replace('url(#sc', 'url(#sm') for k, v in SOLE_SVG.items()}) + ';</script>', shoes_faq, "Padel shoes")

# ---------------- PADEL CALORIES CALCULATOR ----------------
# Padel has no entry in the 2024 Adult Compendium of Physical Activities; we use its tennis values as stand-ins (labelled on the page).
CAL_LV = [("easy", "Relaxed social game", 5.0, "Between the Compendium's two tennis doubles values (4.5 and 6.0)"),
          ("club", "Normal club match", 6.8, "Compendium: tennis, general, moderate effort"),
          ("hard", "Hard, competitive match", 8.0, "Compendium: tennis, general, competitive")]
def _kcal(met, kg, mins): return round(met * 3.5 * kg / 200 * mins)
def _cal_row(kg):
    return f"<tr><td>{kg} kg ({round(kg * 2.20462)} lb)</td>" + "".join(f"<td>{_kcal(m, kg, 60)}</td>" for _, _, m, _ in CAL_LV) + f"<td>{_kcal(6.8, kg, 90)}</td></tr>"
cal = f'''<header class="hero"><div class="wrap"><h1>Padel calories calculator.</h1>
<p class="lead">How many calories does your padel game burn? Enter your weight, how long you play and how hard, and get an estimate per session, per hour and per week, plus how much of the weekly activity target it covers.</p>
{quick("An hour of padel burns roughly 390 to 630 kcal for a 75 kg (165 lb) adult: about 390 kcal for a relaxed social game, 535 kcal for a normal club match and 630 kcal for a hard, competitive match. Heavier players burn more, lighter players less. These are estimates, not measurements.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="cal">
<div class="card">
<h2 style="font-size:1.6rem">Your game</h2>
<div class="q"><h3><label for="cal-w">Your body weight</label></h3><div class="gen-nums"><input class="search" id="cal-w" type="number" min="25" max="400" step="1" value="75" inputmode="decimal"><div class="opts" data-cal="unit" role="group" aria-label="Weight unit"><button class="opt" type="button" data-v="kg" aria-pressed="true">kg</button><button class="opt" type="button" data-v="lb" aria-pressed="false">lb</button></div></div></div>
<div class="q"><h3><label for="cal-t">How long you play: <b id="cal-tv">90 min</b></label></h3><input id="cal-t" class="cal-range" type="range" min="15" max="180" step="15" value="90"><p class="muted" style="margin:6px 0 0">Count the time you are actually playing or warming up, not the drive to the club.</p></div>
<div class="q"><h3>How hard do you play?</h3><div class="opts" data-cal="lv" role="group" aria-label="How hard you play">{"".join(f'<button class="opt" type="button" data-v="{k}" aria-pressed="{"true" if k == "club" else "false"}">{t}</button>' for k, t, _, _ in CAL_LV)}</div><p class="muted" id="cal-lv-note" style="margin:10px 0 0"></p></div>
<div class="q"><h3><label for="cal-s">Sessions a week: <b id="cal-sv">2</b></label></h3><input id="cal-s" class="cal-range" type="range" min="1" max="7" step="1" value="2"></div>
</div>
<div class="result" id="cal-out" aria-live="polite"><h2>Your estimate</h2><p>Enter your weight to see your numbers.</p></div>
</div></div></section>
<script>window.CAL={json.dumps({k: [t, m, s] for k, t, m, s in CAL_LV})};</script>
{AD.format("cal-mid")}
<section><div class="wrap"><div class="sh"><h2>How many calories does padel burn per hour?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Body weight</th><th scope="col">Relaxed, 60 min</th><th scope="col">Club match, 60 min</th><th scope="col">Competitive, 60 min</th><th scope="col">Club match, 90 min</th></tr></thead><tbody>
{"".join(_cal_row(kg) for kg in (55, 65, 75, 85, 95, 105))}
</tbody></table></div>
<p class="muted" style="margin-top:14px">All figures in kcal (the "calories" on food labels), rounded. Worked out as METs × 3.5 × body weight in kg ÷ 200 × minutes, the formula given by the Compendium of Physical Activities.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Where do these numbers come from?</h2></div><div class="grid">
<div class="card"><h3>METs, in one line</h3><p>A MET compares an activity with sitting still. 1 MET is about 1 kcal per kg of body weight per hour, so a 6 MET activity burns about six times more than resting.</p></div>
<div class="card"><h3>Padel has no official value yet</h3><p>The 2024 Adult Compendium of Physical Activities, the standard research list of METs, has no padel entry. We use its tennis values as the closest match: doubles for relaxed games, general tennis for club and hard matches.</p></div>
<div class="card"><h3>Why it is only an estimate</h3><p>Fitness, age, sex, level and how long the rallies last all change the real number. Treat the result as a fair guide, accurate to maybe ± 20 to 30%, not a lab test.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What changes how many calories you burn?</h2></div><div class="grid">
<div class="card"><h3>Your body weight</h3><p>Moving a heavier body costs more energy. At the same effort, a 90 kg player burns about 20% more than a 75 kg player.</p></div>
<div class="card"><h3>Rallies and rests</h3><p>Padel is stop-start. A 2025 study of national-level players (Frontiers in Sports and Active Living) measured rallies of about 6.5 seconds on average, with about 17 seconds between them. More waiting means fewer calories.</p></div>
<div class="card"><h3>How hard you move</h3><p>Getting your feet to the ball, moving up and back with your partner and chasing lobs all add up. Standing still and hitting does not.</p></div>
<div class="card"><h3>Your level</h3><p>Long rallies between good players keep everyone moving. In beginner games the ball is out of play more often, so the burn per hour is lower. See your level with the <a href="{href("level-calculator.html")}">level calculator</a>.</p></div>
<div class="card"><h3>Warm-up time</h3><p>A 10-minute warm-up counts too, at a lower rate. The <a href="{href("warm-up.html")}">warm-up timer</a> walks you through one.</p></div>
<div class="card"><h3>Watches and apps</h3><p>A fitness watch uses your heart rate, so its number can be closer for you, or quite different. Wrist sensors can struggle with fast racket movements.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Does padel count as exercise?</h2></div><div class="grid">
<div class="card"><h3>The weekly target</h3><p>The NHS and the World Health Organization advise adults to do at least 150 minutes of moderate activity a week, or 75 minutes of vigorous activity, or a mix of both, plus strength work on 2 days.</p></div>
<div class="card"><h3>Moderate or vigorous?</h3><p>The US CDC counts 3 to 5.9 METs as moderate and 6 METs or more as vigorous. A relaxed padel game sits in the moderate band; a normal or hard match is usually vigorous, so each minute counts double.</p></div>
<div class="card"><h3>Two games a week</h3><p>Two 90-minute club matches a week is 180 minutes of vigorous play. That is more than twice the 75-minute vigorous target on its own.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Warm up first</h3><p>Use the 10 or 15 minute <a href="{href("warm-up.html")}">warm-up timer</a> before every game, and see how to avoid the most common <a href="{href("padel-injuries.html")}">padel injuries</a>.</p></div>
<div class="card"><h3>Play more often</h3><p>Run a social night with the <a href="{href("americano.html")}">Americano generator</a>, or start a <a href="{href("ladder.html")}">padel ladder</a> at your club.</p></div>
<div class="card"><h3>Shoes that grip</h3><p>More running around means more slips in the wrong shoes. Check the <a href="{href("padel-shoes.html")}">padel shoe finder</a>.</p></div>
</div></div></section>'''
cal_faq = [
    ("How many calories does 1 hour of padel burn?", "Roughly 390 to 630 kcal for a 75 kg adult: about 390 for a relaxed game, 535 for a normal club match and 630 for a hard match. Lighter players burn less, heavier players more."),
    ("How many calories does 90 minutes of padel burn?", "A normal 90-minute club match burns about 800 kcal for a 75 kg player, and about 640 kcal for a 60 kg player. A relaxed game burns about a quarter less."),
    ("Does padel burn more calories than tennis?", "There is no official calorie value for padel yet, so nobody can say for sure. Padel is almost always doubles with short rallies, so it is likely close to tennis doubles for relaxed games and close to general tennis for hard matches."),
    ("Is padel good for weight loss?", "Padel can help as part of regular activity, because it burns a fair amount of energy and is fun enough to keep doing. Weight loss also depends on diet and sleep; for personal advice, talk to your doctor."),
    ("Is padel moderate or vigorous exercise?", "A relaxed game is about 5 METs, which is moderate. A normal or hard match is about 7 to 8 METs, which counts as vigorous under the CDC definition (6 METs or more)."),
    ("How accurate is this padel calorie calculator?", "It gives a fair estimate, not a measurement. It uses published METs for tennis because padel has no entry in the Compendium of Physical Activities. Your real number can be 20 to 30% higher or lower."),
]
page("padel-calories.html", "Padel Calories Calculator: How Many Calories Does It Burn?",
     "Free padel calories calculator: enter your weight, time and effort to see how many calories padel burns per session, per hour and per week.",
     cal, cal_faq, "Padel calories calculator")

# ---------------- PADEL COURT COST (senior SEO pass 25 Nov 2026; KP: "padel court cost"/"price" 100-1k medium, "padel court" 10k-100k) ----------------
cc = f"""<section class="hero" style="padding-bottom:20px"><div class="wrap" style="max-width:860px"><h1>How Much Does a Padel Court Cost?</h1>
<p class="lede">A single outdoor padel court usually costs <strong>£45,000 to £80,000 in the UK</strong> and <strong>$25,000 to $65,000 in the US</strong> once it is installed. Ground work, lighting, panoramic glass and an indoor building push it higher. Below are the published ranges, what moves the price, and a free budget planner for one court or a whole club.</p></div></section>
<section style="padding-top:0"><div class="wrap" style="max-width:860px"><div class="sh"><h2>Padel court cost: published ranges</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Where</th><th scope="col">What it covers</th><th scope="col">Typical range</th><th scope="col">Source</th></tr></thead><tbody>
<tr><td>UK</td><td>Single court, installed</td><td>£45,000–£80,000</td><td>MyBuilder price guide; Padel Market UK guide</td></tr>
<tr><td>UK</td><td>Average court built (planning data)</td><td>about £71,000</td><td>Barbour ABI, 2026</td></tr>
<tr><td>UK</td><td>Projects incl. lighting, drainage, foundations, several courts</td><td>£60,000–£270,000</td><td>LTA Padel construction guidance</td></tr>
<tr><td>UK</td><td>Indoor court, before the building itself</td><td>£60,000–£80,000</td><td>Padel Market UK guide</td></tr>
<tr><td>US</td><td>Single outdoor court</td><td>$25,000–$60,000 (typical $35,000–$45,000)</td><td>PadelBrowser 2026 guide</td></tr>
<tr><td>US</td><td>Turnkey outdoor court (structure, glass, turf, lights, basic ground work)</td><td>$24,000–$65,000</td><td>Dojo Business</td></tr>
<tr><td>US</td><td>LED court lighting</td><td>adds $2,800–$10,000</td><td>Dojo Business</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Ranges are what the sources publish, rounded. They are planning numbers, not quotes. Always get at least three quotes from installers who build to the federation's court rules.</p></div></section>
<section style="padding-top:0"><div class="wrap" style="max-width:860px"><div class="sh"><h2>Padel court budget planner</h2></div>
<div class="tool card" id="cc-tool"><p class="muted">Pick a price per court from the table (or your own quote), set the extras, and see the total with a safety margin.</p>
<div class="q"><h3><label for="cc-cur">Currency</label></h3><select id="cc-cur"><option value="£">£ (UK)</option><option value="$">$ (US)</option><option value="€">€</option><option value="AED ">AED</option></select></div>
<div class="q"><h3><label for="cc-n">Number of courts</label></h3><input id="cc-n" type="number" min="1" max="30" value="1"></div>
<div class="q"><h3><label for="cc-p">Price per court, installed</label></h3><input id="cc-p" type="number" min="0" step="1000" value="60000"></div>
<div class="q"><h3><label for="cc-g">Ground work per court (base, drainage)</label></h3><input id="cc-g" type="number" min="0" step="1000" value="0"><p class="muted" style="margin:6px 0 0">0 if you are building on an existing tennis court or tarmac.</p></div>
<div class="q"><h3><label for="cc-l">Lighting per court</label></h3><input id="cc-l" type="number" min="0" step="500" value="0"></div>
<div class="q"><h3><label for="cc-c">Safety margin (contingency)</label></h3><select id="cc-c"><option value="0.1">10%</option><option value="0.15" selected>15%</option><option value="0.2">20%</option></select></div>
<div class="result" id="cc-out" aria-live="polite"></div></div>
<script>(function(){{var $=function(i){{return document.getElementById(i)}};function f(c,v){{return c+Math.round(v).toLocaleString()}}function r(){{var c=$('cc-cur').value,n=Math.max(1,+$('cc-n').value||1),per=(+$('cc-p').value||0)+(+$('cc-g').value||0)+(+$('cc-l').value||0),sub=per*n,m=+$('cc-c').value;$('cc-out').innerHTML='<h2>Your budget</h2><p><strong>'+f(c,sub*(1+m))+'</strong> in total for '+n+' court'+(n>1?'s':'')+' (including a '+Math.round(m*100)+'% margin).</p><p class="muted">'+f(c,per)+' per court before the margin, '+f(c,sub)+' for all courts. Add planning fees, a building if you play indoors, and turf replacement every 5 to 10 years.</p>'}}['cc-cur','cc-n','cc-p','cc-g','cc-l','cc-c'].forEach(function(i){{$(i).addEventListener('input',r)}});r()}})();</script>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What changes the price of a padel court?</h2></div><div class="grid">
<div class="card"><h3>Standard or panoramic</h3><p>A standard court has glass at the back and mesh on the sides. A panoramic court uses full glass sides with no side posts, which needs more tempered glass and heavier engineering, so it costs more.</p></div>
<div class="card"><h3>The ground under it</h3><p>The court kit costs about the same anywhere. Grading, drainage and a new concrete or asphalt base can change the total by tens of thousands, so a flat existing base (like an old tennis court) saves the most.</p></div>
<div class="card"><h3>Indoor or outdoor</h3><p>Outdoor courts are cheapest. Indoors you also pay for a building or canopy with enough clear height above the court, plus heating, ventilation and planning permission.</p></div>
<div class="card"><h3>Lighting</h3><p>LED floodlights let you sell evening slots, which is when most clubs are busiest. Budget them per court. Want to see what players pay per hour? See <a href="{href("padel-cost.html")}">how much padel costs to play</a>.</p></div>
<div class="card"><h3>Turf and upkeep</h3><p>Sand-filled artificial turf is the standard surface. Plan to brush and top up sand regularly; LTA Padel guidance says to budget for new turf about every 5 years on a busy court. More on turf types: <a href="{href("padel-court-surfaces.html")}">padel court surfaces</a>.</p></div>
<div class="card"><h3>Shipping and install crew</h3><p>Many court systems are made in Europe. Outside Europe, freight, import duty and a specialist install crew add to the bill.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Before you build</h2></div><div class="grid">
<div class="card"><h3>Check the footprint</h3><p>A doubles court is 20 m × 10 m inside the walls. See every measurement on the <a href="{href("court-dimensions.html")}">padel court dimensions diagram</a>.</p></div>
<div class="card"><h3>Fill it from day one</h3><p>Run launch nights with the <a href="{href("americano.html")}">Americano generator</a> and keep members coming back with a <a href="{href("ladder.html")}">padel ladder</a>.</p></div>
<div class="card"><h3>Teach new players</h3><p>Most new members have never played. Share <a href="{href("rules.html")}">padel rules explained simply</a> and the <a href="{href("beginners.html")}">beginner checklist</a>.</p></div>
</div></div></section>"""
cc_faq = [
    ("How much does a padel court cost in the UK?", "Usually £45,000 to £80,000 for a single installed court, with Barbour ABI planning data putting the 2026 average at about £71,000. Projects with lighting, drainage, foundations or several courts can reach £270,000 (LTA)."),
    ("How much does a padel court cost in the US?", "Most 2026 estimates for a single outdoor court fall between about $25,000 and $65,000, with a typical mid-range build around $35,000 to $45,000. Site work and lighting can add a lot."),
    ("Is a panoramic padel court more expensive?", "Yes. Full glass side walls need more tempered glass and stronger engineering than a standard court with mesh sides, so panoramic courts sit at the top of the price range."),
    ("Can you build a padel court on a tennis court?", "Often, yes, if the old base is flat, sound and drains well. Reusing it can save most of the ground work cost; ask an installer to check it first."),
    ("How long does padel court turf last?", "Plan to replace sand-filled artificial turf every 5 to 10 years, depending on how much the court is used and how well it is brushed and topped up."),
]
page("padel-court-cost.html", "How Much Does a Padel Court Cost? UK and US Prices",
     "A padel court costs about £45,000–£80,000 in the UK and $25,000–$65,000 in the US. See published price ranges, what changes the cost, and a free budget planner.",
     cc, cc_faq, "Padel court cost")

# ---------------- PADEL LADDER TRACKER ----------------
lad = f'''<header class="hero"><div class="wrap"><h1>Padel ladder tracker.</h1>
<p class="lead">Run a challenge ladder for your club or group. Add your pairs or players, record each challenge and the ladder reorders itself, with win and loss records, movement arrows and a full match history. Free, no sign-up, saved on this device.</p>
{quick("In a padel ladder, everyone is ranked in a list. You challenge someone a few places above you (often up to 2 or 3). If you win, you take their place; if you lose, nothing changes. Agree the challenge range, the match format and how long people have to accept a challenge before you start.")}</div></header>
<section style="padding-top:10px"><div class="wrap gen">
<div class="gen-main">
<div class="card" id="ld-setup">
<h2 style="font-size:1.6rem">Set up your ladder</h2>
<div class="q"><h3>Who is on the ladder?</h3><div class="opts" data-ld="who" role="group" aria-label="Ladder type"><button class="opt" type="button" data-v="pairs" aria-pressed="true">Fixed pairs</button><button class="opt" type="button" data-v="players" aria-pressed="false">Single players</button></div></div>
<div class="q"><h3><label for="ld-names">Names in starting order, top first (4 to 40)</label></h3><textarea class="search" id="ld-names" rows="7" placeholder="Sam &amp; Priya&#10;Omar &amp; Lucia&#10;Ben &amp; Aisha&#10;..."></textarea><p class="muted" id="ld-count" style="margin:-6px 0 0"></p></div>
<div class="q"><h3>How far up can you challenge?</h3><div class="opts" data-ld="range" role="group" aria-label="Challenge range"><button class="opt" type="button" data-v="2" aria-pressed="false">Up to 2 places</button><button class="opt" type="button" data-v="3" aria-pressed="true">Up to 3 places</button><button class="opt" type="button" data-v="5" aria-pressed="false">Up to 5 places</button><button class="opt" type="button" data-v="99" aria-pressed="false">Anyone above</button></div></div>
<div class="q"><h3>When the challenger wins</h3><div class="opts" data-ld="move" role="group" aria-label="Movement rule"><button class="opt" type="button" data-v="swap" aria-pressed="true">Swap places</button><button class="opt" type="button" data-v="jump" aria-pressed="false">Take the spot, others move down one</button></div><p class="muted" id="ld-move-note" style="margin:10px 0 0"></p></div>
<p class="msg" id="ld-err" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:4px"><button class="btn lime" type="button" id="ld-start">Start the ladder</button><button class="btn ghost" type="button" id="ld-demo">Fill 8 sample pairs</button></div>
</div>
<div id="ld-live" hidden>
<div class="card gen-bar"><div><span class="pill b" id="ld-sum"></span></div><div class="btns" style="margin:0"><button class="btn ghost sm" type="button" id="ld-copy">Copy ladder</button><button class="btn ghost sm" type="button" id="ld-new">New ladder</button></div></div>
<div class="card" id="ld-rec">
<h2 style="font-size:1.4rem">Record a challenge</h2>
<div class="gen-nums"><div class="q"><h3><label for="ld-ch">Challenger</label></h3><select class="search" id="ld-ch"></select></div>
<div class="q"><h3><label for="ld-df">Challenged</label></h3><select class="search" id="ld-df"></select></div></div>
<div class="q"><h3>Who won?</h3><div class="opts" id="ld-win" role="group" aria-label="Winner"><button class="opt" type="button" data-v="c" aria-pressed="false">Challenger won</button><button class="opt" type="button" data-v="d" aria-pressed="false">Challenged won</button></div></div>
<div class="q"><h3><label for="ld-sc">Score (optional)</label></h3><input class="search" id="ld-sc" type="text" maxlength="40" placeholder="6-4 3-6 7-5"></div>
<p class="msg" id="ld-rerr" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:0"><button class="btn lime" type="button" id="ld-save">Save result</button><button class="btn ghost sm" type="button" id="ld-undo">Undo last result</button></div>
</div>
<div class="card"><h2 style="font-size:1.4rem">Add a late entry</h2><div class="gen-nums"><input class="search" id="ld-add" type="text" maxlength="60" placeholder="New pair or player"><button class="btn ghost" type="button" id="ld-addb">Add to the bottom</button></div></div>
<div class="card"><h2 style="font-size:1.4rem">Match history</h2><ol class="ld-hist" id="ld-hist"></ol></div>
</div>
</div>
<aside class="gen-side"><div class="lb" id="ld-board"><h2>The ladder</h2><p>Start the ladder to see the rankings here.</p></div></aside>
</div></section>
{AD.format("ld-mid")}
<section><div class="wrap"><div class="sh"><h2>How does a padel ladder work?</h2></div><div class="grid">
<div class="card"><h3>A ranked list</h3><p>Every pair (or player) has a place on the ladder. The starting order can be by level, by last season, or simply random. Use the <a href="{href("level-calculator.html")}">level calculator</a> if you want a fair first order.</p></div>
<div class="card"><h3>Challenge upwards</h3><p>You can only challenge someone above you, and usually only a few places above. That keeps matches close and stops the bottom team taking on the top team every week.</p></div>
<div class="card"><h3>Win and climb</h3><p>Beat a higher team and you move up. The two common ways: swap places with them, or take their spot and push everyone in between down one. Lose and the ladder stays the same.</p></div>
<div class="card"><h3>No fixed end</h3><p>A ladder runs all season. Players arrange their own matches when it suits them, which makes it a good fit for busy clubs.</p></div>
<div class="card"><h3>Pairs or singles</h3><p>Padel is a doubles game, so most ladders are for fixed pairs. A single-player ladder works if each match is two ladder players against two others, or if you mix partners.</p></div>
<div class="card"><h3>Keep score properly</h3><p>Agree <a href="{href("golden-point-star-point.html")}">golden point or advantage</a> first, and keep score on a phone with the <a href="{href("score.html")}">score keeper</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Ladder rules to agree before you start</h2></div><div class="grid">
<div class="card"><h3>Challenge range</h3><p>How many places up can you challenge? 2 or 3 is common. A bigger range lets new strong pairs climb faster.</p></div>
<div class="card"><h3>Time to accept</h3><p>Set a limit, for example 7 to 14 days to play a challenge. If the challenged pair won't play in time, the challenger can be given the match.</p></div>
<div class="card"><h3>Match format</h3><p>Best of three sets, one long set, or a timed match on one court booking. Keep it the same for everyone.</p></div>
<div class="card"><h3>Rematches</h3><p>Many ladders say you can't challenge the same pair again straight away. You must play someone else first.</p></div>
<div class="card"><h3>Staying active</h3><p>Some ladders move a pair down if they don't play for a few weeks, so the ladder stays live.</p></div>
<div class="card"><h3>Who books and pays</h3><p>Usually the challenger books the court and the cost is shared. Write it down so there are no arguments.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Ladder, box league, round robin or Americano?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Format</th><th scope="col">Partners</th><th scope="col">How long</th><th scope="col">Best for</th></tr></thead><tbody>
<tr><td>Ladder</td><td>Fixed pairs or players</td><td>All season, open-ended</td><td>Clubs where people book their own matches</td></tr>
<tr><td>Box league</td><td>Fixed pairs</td><td>Rounds of a few weeks, then promotion and relegation</td><td>Larger clubs with many levels</td></tr>
<tr><td><a href="{href("round-robin.html")}">Round robin</a></td><td>Fixed pairs</td><td>One event or a short league</td><td>Everyone plays everyone once</td></tr><tr><td><a href="{href("padel-tournament-bracket.html")}">Knockout</a></td><td>Fixed pairs</td><td>One-day cup</td><td>Lose once and you are out</td></tr>
<tr><td><a href="{href("americano.html")}">Americano</a></td><td>Change every round</td><td>One evening</td><td>Social nights and meeting new players</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>One-night event?</h3><p>Use the <a href="{href("round-robin.html")}">round robin generator</a> for fixed pairs, or the <a href="{href("americano.html")}">Americano draw maker</a> to mix partners.</p></div>
<div class="card"><h3>Score the match</h3><p>Keep score at the net with the free <a href="{href("score.html")}">score keeper</a>.</p></div>
<div class="card"><h3>Know the rules</h3><p>Settle arguments fast with the <a href="{href("wall-rules.html")}">wall rules checker</a> and the <a href="{href("serve-rules.html")}">serve checker</a>.</p></div>
</div></div></section>'''
lad_faq = [
    ("What is a padel ladder?", "A ranked list of pairs or players. You challenge someone above you, and if you win you move up. It runs all season and players arrange their own matches."),
    ("How many places can you challenge in a ladder?", "Each ladder sets its own rule. Up to 2 or 3 places above you is common. This tracker lets you pick 2, 3, 5 or anyone above."),
    ("What happens when a challenger wins?", "Either the two swap places, or the winner takes the higher spot and everyone in between moves down one place. Agree which rule you use before you start."),
    ("What happens if the challenger loses?", "In most ladders nothing changes: the challenged pair keeps its place. Some ladders stop the loser challenging the same pair again straight away."),
    ("What is the difference between a ladder and a box league?", "In a ladder you challenge people above you whenever you like. In a box league you play everyone in a small group over a few weeks, then the top moves up a box and the bottom moves down."),
    ("Where is the ladder saved?", "On this device, in your browser. Use 'Copy ladder' to share the rankings in a group chat, and keep updating it on the same phone or computer."),
]
page("ladder.html", "Padel Ladder Tracker: Free Challenge Ladder for Pairs",
     "Free padel ladder tracker: add pairs or players, record challenges and the ladder updates itself, with records, movement, history and ladder rules.",
     lad, lad_faq, "Padel ladder tracker")

# ---------------- NET RULES CHECKER ----------------
# Calls follow the FIP Rules of Padel PDF (in force 01.01.2026). Ball positions are x,y on the 400x160 side view.
NET = {
    "rk": ("lose", "You lose the point", "If your racket touches the net, a net post or the net cable while the ball is in play, your team loses the point. It doesn't matter if your shot was a winner.", "FIP rule 13.1(a)", [186, 100]),
    "bd": ("lose", "You lose the point", "Your body, clothes and anything you carry count too. A shirt, a cap or a hand on the net while the ball is in play loses the point.", "FIP rule 13.1(a)", [190, 118]),
    "cr": ("lose", "You lose the point", "Touching the opponents' court while the ball is in play also loses the point, for example a foot that slides under the net onto their side.", "FIP rule 13.1(a)", [214, 138]),
    "af": ("on", "No net fault", "The net rule applies while the ball is in play. Once the point has ended (for example the ball bounced twice), touching the net does not change the result. Make sure the point really is over first, and treat the net with care.", "FIP rule 13.1(a), which covers touches \"while the ball is in play\"", [190, 112]),
    "ov": ("lose", "You lose the point", "You must wait until the ball has crossed the net to your side. Hitting it while it is still over their court loses the point.", "FIP rule 13.1(f)", [222, 86]),
    "ft": ("on", "Play on", "If you hit the ball on your side, your swing may carry on over the net. What matters is where you hit the ball and that you don't touch the net or their court.", "FIP rules 13.1(a) and 13.1(f)", [194, 84]),
    "sb": ("on", "Play on: they may reach over", "If your shot bounces on their side and then spins or blows back over the net, they may hit it, even by reaching over the net. They lose the point if they touch the net, the posts or your court, or if it bounces a second time first.", "FIP rule 14.1(g)", [180, 120]),
    "nc": ("on", "Play on", "In a rally, a ball that clips the net or a post and then lands on their side is a good shot. Keep playing.", "FIP rule 14.1(e)", [200, 96]),
    "np": ("on", "Play on", "The net posts count like the net. If your shot hits a post and then lands in their court, the rally goes on.", "FIP rule 14.1(e)", [204, 92]),
    "ns": ("let", "Let: serve again", "On the serve it is different. A serve that touches the net or a post and then lands in the correct service box is a let, so you serve that serve again. If it touches the net and lands anywhere else, it is a fault.", "FIP rules 9.1 and 9.2", [200, 96]),
    "hb": ("lose", "You lose the point", "If the other team's shot hits you or your clothes before it bounces, your team loses the point. This is true even if the ball looked like it was going out.", "FIP rule 13.1", [176, 100]),
}
def _nq(label, opts):
    return f'<div class="q nt-q"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
NT_SVG = '''<svg viewBox="0 0 400 160" class="wr-court" role="img" aria-label="Side view of the net. The ball shows where the situation happens.">
<rect x="0" y="0" width="400" height="160" rx="14" fill="#0e2468"/>
<rect x="20" y="140" width="360" height="6" fill="#1e46c8"/>
<defs><pattern id="ntm" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 0H6M0 0V6" stroke="#e4eef6" stroke-width=".8" opacity=".55"/></pattern></defs>
<rect x="197" y="102" width="6" height="38" fill="url(#ntm)"/><path d="M196 100h8" stroke="#fff" stroke-width="4"/>
<rect x="198" y="96" width="4" height="44" fill="#e4eef6" opacity=".35"/>
<text x="110" y="156" text-anchor="middle" font-size="9" fill="#9fb0e0" font-family="Onest, sans-serif">Your side</text><text x="290" y="156" text-anchor="middle" font-size="9" fill="#9fb0e0" font-family="Onest, sans-serif">Their side</text>
<text x="210" y="98" font-size="8" fill="#9fb0e0" font-family="Onest, sans-serif">net 0.88 m</text>
<g fill="#e8f84a"><circle cx="150" cy="84" r="5"/><path d="M150 90v22M150 112l-6 28M150 112l6 28" stroke="#e8f84a" stroke-width="3"/><path d="M150 96l20 -6" stroke="#e8f84a" stroke-width="3"/></g>
<g fill="#ffffff"><circle cx="270" cy="84" r="5"/><path d="M270 90v22M270 112l-6 28M270 112l6 28" stroke="#fff" stroke-width="3" opacity=".9"/></g>
<circle id="nt-ring" cx="200" cy="100" r="13" fill="none" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 3" opacity="0"/>
<circle id="nt-ball" cx="110" cy="132" r="6" fill="#e8f84a" stroke="#0b1530" stroke-width="1.5"/>
</svg>'''
net = f'''<header class="hero"><div class="wrap"><h1>Padel net rules: can you touch the net?</h1>
<p class="lead">Racket on the net, a ball that spins back, a swing over the top, a net cord on the serve: tap what happened and get the call with the FIP rule number.</p>
{quick("No. If you, your clothes or your racket touch the net, the net posts or the other team's court while the ball is in play, you lose the point. You also lose it if you hit the ball before it has crossed to your side. Your swing may go over the net after you hit the ball on your side, and a rally ball that clips the net and lands over is good. On the serve, a net cord that lands in the box is a let.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="nt">
<div>
{_nq("Touching the net", [("rk", "My racket touched the net"), ("bd", "My body or clothes touched the net or a post"), ("cr", "My foot went under the net onto their side"), ("af", "I touched the net after the point was over")])}
{_nq("Hitting over the net", [("ov", "I hit the ball before it crossed to my side"), ("ft", "I hit it on my side and my swing went over the net"), ("sb", "My shot bounced on their side and spun back over")])}
{_nq("The ball and the net", [("nc", "My rally shot clipped the net and landed over"), ("np", "My shot hit the net post and landed in their court"), ("ns", "My serve clipped the net and landed in the box"), ("hb", "Their shot hit me at the net before it bounced")])}
<button class="btn sm" type="button" id="nt-reset">Start again</button>
</div>
<aside class="result" id="nt-out" aria-live="polite"><div class="wr-svg">{NT_SVG}</div><div id="nt-txt"><h2>Make the call</h2><p>Tap a situation and the verdict appears here.</p></div></aside>
</div></div></section>
{AD.format("net-mid")}
<section><div class="wrap"><div class="sh"><h2>What are the net rules in padel?</h2></div><div class="grid">
<div class="card"><span class="pill a">Lose the point</span><h3 style="margin-top:10px">No touching</h3><p>While the ball is in play, you may not touch the net, the posts, the net cable or the other team's court. This covers your racket, your body, your clothes and anything you carry.</p></div>
<div class="card"><span class="pill a">Lose the point</span><h3 style="margin-top:10px">Wait for the ball</h3><p>You may only hit the ball once it has crossed the net to your side. No volleying it over their court.</p></div>
<div class="card"><span class="pill b">Allowed</span><h3 style="margin-top:10px">Follow-through</h3><p>If you hit the ball on your side, your racket may go over the net as you finish the swing, as long as it touches nothing.</p></div>
<div class="card"><span class="pill b">Allowed</span><h3 style="margin-top:10px">Net cord in a rally</h3><p>A rally shot that touches the net or a post and then lands in their court is good.</p></div>
<div class="card"><span class="pill i">Serve again</span><h3 style="margin-top:10px">Net cord on the serve</h3><p>A serve that touches the net and lands in the right box is a let. Touching the net and landing anywhere else is a fault. More on the <a href="{href("serve-rules.html")}">serve rules page</a>.</p></div>
<div class="card"><span class="pill b">Allowed</span><h3 style="margin-top:10px">Ball coming back</h3><p>A ball that bounces on your side and then spins back over the net can still be hit by you, reaching over, as long as you don't touch the net or their court.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Can you reach over the net in padel?</h2></div><div class="grid">
<div class="card"><h3>Before the ball crosses: no</h3><p>If the ball has not yet come over to your side, reaching over to hit it loses the point.</p></div>
<div class="card"><h3>To finish your swing: yes</h3><p>Hit the ball on your side and let the racket carry on over. Keep your racket and body clear of the net.</p></div>
<div class="card"><h3>When the ball spins back: yes</h3><p>After a drop shot or a smash with backspin, the ball can bounce and come back to the hitter's side. The other team may reach over or run around to play it, without touching the net or the court.</p></div>
</div>
<p class="muted" style="margin-top:14px">Some guides add extra conditions, such as only reaching over after the ball has bounced on your side. The FIP rules don't say this: they only say the ball must have crossed the net and you must not touch the net or the other court. In club play, agree how you will call it before you start.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Other calls that happen near the net</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">What happened</th><th scope="col">The call</th></tr></thead><tbody>
<tr><td>You hit the ball twice in one swing</td><td>You lose the point (13.1)</td></tr>
<tr><td>You and your partner both hit the ball</td><td>You lose the point (13.1)</td></tr>
<tr><td>The ball bounces twice on your side</td><td>You lose the point (13.1)</td></tr>
<tr><td>You throw your racket at the ball</td><td>You lose the point (13.1)</td></tr>
<tr><td>You drop your racket or break the safety cord</td><td>You lose the point (13.1)</td></tr>
<tr><td>Their shot touches your racket and goes over</td><td>Good return: play on (14.1)</td></tr>
<tr><td>Your shot hits an opponent before bouncing</td><td>You win the point (13.1)</td></tr>
<tr><td>Their volley at the net hits you before bouncing</td><td>You lose the point (13.1)</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">These calls follow the International Padel Federation (FIP) rules in force from January 2026. Rule numbers are from the FIP Rules of Padel. Local leagues can add their own rules.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How to stay safe at the net</h2></div><div class="grid">
<div class="card"><h3>Stand a step back</h3><p>About a racket length or two from the net gives you time to react and keeps your racket clear of the net on fast volleys.</p></div>
<div class="card"><h3>Racket up, in front</h3><p>Keep the racket head up and in front of your body. Balls aimed at you are easier to block, and you are less likely to be hit.</p></div>
<div class="card"><h3>Stop before the net</h3><p>On a short ball, slow down early. Most net touches happen when a player runs in and can't stop.</p></div>
</div>
<p class="muted" style="margin-top:14px">See where to stand in every situation on our <a href="{href("positioning.html")}">positioning court</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Walls and fences</h3><p>Was that ball in? Check it with the <a href="{href("wall-rules.html")}">wall and fence checker</a>.</p></div>
<div class="card"><h3>The serve</h3><p>Fault, let or good serve? Use the <a href="{href("serve-rules.html")}">serve checker</a>.</p></div>
<div class="card"><h3>All the rules</h3><p>Tap any part of the <a href="{href("rules.html")}">interactive rules court</a>.</p></div>
</div></div></section>'''
net_faq = [
    ("Can you touch the net in padel?", "No. If you, your clothes or your racket touch the net, the posts or the net cable while the ball is in play, your team loses the point."),
    ("Can your racket go over the net in padel?", "Yes, if you hit the ball on your side and the racket carries over as you finish your swing, and you don't touch the net. Hitting the ball before it crosses to your side loses the point."),
    ("What happens if the ball spins back over the net in padel?", "If it bounces on one side and then comes back over the net, the team on that side may still hit it, even by reaching over the net, as long as they don't touch the net or the other court."),
    ("Is a net cord a let in padel?", "Only on the serve, when the ball touches the net and lands in the correct service box. In a rally, a ball that clips the net and lands in the other court is in play."),
    ("Can you volley the ball before it crosses the net in padel?", "No. You must wait until the ball is on your side of the net. Hitting it over the other court loses the point."),
    ("Is it a fault to touch the net after the point is over?", "The FIP net rule applies while the ball is in play, so a touch after the point has ended does not change the result. Make sure the point is really over first."),
    ("What if the ball hits you at the net before bouncing?", "Your team loses the point, even if you think the ball was going out."),
]
page("net-rules.html", "Padel Net Rules: Can You Touch the Net? Free Call Checker",
     "Padel net rules in plain English: touching the net, reaching over, follow-through and net cords on the serve. Tap what happened and get the FIP call.",
     net + f'<script>window.NT={json.dumps(NET)};</script>', net_faq, "Net rules")

# ---------------- RACKET CARE ----------------
# Advice from Babolat help centre, Zona de Padel, PadelProShop and Padelshop care guides (see CONTENT-LOG). Checker verdicts are our own wording.
RC_ITEMS = [
    ("crack", 3, "I can see a crack in the frame"),
    ("crack", 3, "There is a crack, dent or hole in the hitting face"),
    ("in", 2, "Something rattles inside when I shake it"),
    ("in", 2, "It feels dead or soft in spots, or has less power than before"),
    ("in", 1, "Hits feel buzzy, with odd vibrations"),
    ("heat", 1, "It was left in a hot car or in the sun for hours"),
    ("tape", 0, "The protector tape on the top edge is worn through or peeling"),
    ("grip", 0, "The overgrip is slippery, shiny or torn"),
    ("cord", 0, "The wrist cord is frayed or the stopper is loose"),
]
rcare = f'''<header class="hero"><div class="wrap"><h1>Padel racket care: make your racket last</h1>
<p class="lead">Heat, cold, damp and knocks on the glass are what wear a padel racket out. Run the two-minute health check, then follow the simple care routine below.</p>
{quick("Keep your racket in a cover, in a dry place indoors, away from the sun and out of the car. Wipe off sand and sweat after every game and dry it before you put it away. Put protector tape on the top of the frame, change the overgrip when it gets slippery, and check for cracks every few weeks.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="rc">
<div><div class="q"><h3>Racket health check: tick anything that is true</h3>
<ul class="check" id="rc-list">{"".join(f'<li><label><input type="checkbox" data-c="{c}" data-w="{w}"><span>{t}</span></label></li>' for c, w, t in RC_ITEMS)}</ul></div>
<button class="btn sm" type="button" id="rc-reset">Start again</button></div>
<aside class="result" id="rc-out" aria-live="polite"><h2>Your racket check</h2><p>Tick what you notice and the verdict and fixes appear here.</p></aside>
</div></div></section>
{AD.format("care-mid")}
<section><div class="wrap"><div class="sh"><h2>How do you look after a padel racket?</h2></div><div class="grid">
<div class="card"><span class="pill b">After every game</span><h3 style="margin-top:10px">Wipe and dry</h3><p>Wipe sand and dust off the faces and frame with a dry, soft cloth. If it is damp from sweat or rain, let it dry before it goes into its cover.</p></div>
<div class="card"><span class="pill b">After every game</span><h3 style="margin-top:10px">Cover it</h3><p>Put it straight into its cover or the racket pocket of your bag, away from keys and bottles.</p></div>
<div class="card"><span class="pill i">For stains</span><h3 style="margin-top:10px">A little soap</h3><p>Use a cloth that is only slightly damp, with a drop of mild soap. Dry it straight away. Never soak the racket or use strong cleaning products.</p></div>
<div class="card"><span class="pill i">Every few weeks</span><h3 style="margin-top:10px">Check for damage</h3><p>Look along the frame and both faces for cracks and chips, especially at the top edge, which hits the glass and the floor most.</p></div>
<div class="card"><span class="pill i">When worn</span><h3 style="margin-top:10px">New overgrip</h3><p>Change it when it feels slippery. Players who play a lot and sweat a lot may change it every few matches; others go a month or two.</p></div>
<div class="card"><span class="pill i">When worn</span><h3 style="margin-top:10px">New protector tape</h3><p>Replace the tape when it peels or wears through. Old tape can trap sand and grit under it.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Does heat or cold damage a padel racket?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Condition</th><th scope="col">What it does</th><th scope="col">What to do</th></tr></thead><tbody>
<tr><td>Heat (hot car, sun, near a heater)</td><td>The foam core softens and can lose its shape, so the racket can feel different or lose power for good</td><td>Never leave it in the car or in the sun. Take it inside with you.</td></tr>
<tr><td>Cold (garage, car boot in winter)</td><td>The foam core gets stiffer and harder, and cracks are more likely</td><td>Store it indoors. Let a cold racket warm up to room temperature before you play.</td></tr>
<tr><td>Damp and sweat</td><td>Water can get into small cracks and the core, adding weight and changing the feel</td><td>Dry it after play and before you cover it. Don't store it in a damp place.</td></tr>
<tr><td>Big temperature changes</td><td>Repeated hot and cold stresses the materials</td><td>Keep it somewhere with a steady temperature. A bag with a thermal pocket helps.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Most padel rackets have a core of EVA foam or softer foam inside a carbon or fibreglass shell, which is why temperature matters more than with a tennis racket. Rackets are not all the same: follow your brand's care notes if they say something different.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you put on protector tape?</h2></div><div class="grid">
<div class="card"><h3>1. Clean and dry</h3><p>Remove the old tape, then wipe the top of the frame so it is clean and fully dry.</p></div>
<div class="card"><h3>2. Start in the middle</h3><p>Line the centre of the tape up with the very top of the frame and press it down there first.</p></div>
<div class="card"><h3>3. Work outwards</h3><p>Smooth the tape down one side, then the other, pulling it slightly tight so there are no bubbles or creases.</p></div>
<div class="card"><h3>4. Mind the balance</h3><p>Tape adds a little weight to the head, so the racket feels a bit more head-heavy. See how much it matters with the <a href="{href("racket-balance.html")}">balance decoder</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Does protector tape add weight? Is it worth it?</h2></div>
<div class="tbl"><table><thead><tr><th>Question</th><th>Short answer</th></tr></thead><tbody>
<tr><td>How much weight?</td><td>Usually a few grams up to about 10 g. Decathlon lists its strong frame tape at 10 g; Padel Browser lists one thin protector at 6 g.</td></tr>
<tr><td>Does it change the balance?</td><td>A little. Padel Browser works out that 6 g at the top of a 365 g racket moves the balance about 2 mm towards the head. Balance groups (low, medium, high) are about 1 cm apart, so most players barely feel it.</td></tr>
<tr><td>Which type?</td><td>Thin clear tape keeps the feel closest to new. Thicker "strong" tape and moulded bumpers protect more and weigh more.</td></tr>
<tr><td>How long does it last?</td><td>Padel Browser suggests every 2 to 3 months if you play regularly, or sooner once the frame shows through.</td></tr>
<tr><td>How do I remove it?</td><td>Warm it a little (Decathlon suggests this), then peel slowly from one end.</td></tr>
</tbody></table></div>
<p style="margin-top:12px">Our view: worth it for most players, especially beginners who scrape the floor and glass. If you are fussy about balance, put the tape on the day the racket arrives so you get used to the feel from the start.</p>
<p class="muted" style="margin-top:8px">Sources, checked 28 Nov 2026: Decathlon (Kuikma) "Padel racket frame protector tape strong" product page (10 g, TPU, warm to remove); Padel Browser "Best padel racket protectors 2026" (8 Sep 2026: 6 g example, about 2 mm balance shift, replace every 2 to 3 months).</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Habits that break rackets</h2></div><div class="grid">
<div class="card"><h3>Hitting the floor or walls</h3><p>Banging the racket on the ground or the glass in frustration is the quickest way to crack the frame.</p></div>
<div class="card"><h3>Scooping up balls</h3><p>Picking balls up by scraping the face along the turf wears the face and the edge. Use your hand or foot.</p></div>
<div class="card"><h3>Clashing with your partner</h3><p>Racket clashes in the middle crack frames. Call "mine" or "yours" early (in Spanish: mía and tuya).</p></div>
<div class="card"><h3>Leaving it in the car</h3><p>A car in the sun gets very hot, and in winter very cold. Both are bad for the foam inside.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long does a padel racket last?</h2></div>
<div class="card"><p>There is no fixed number. It depends on how often and how hard you play, and how you store it. Instead of counting months, watch for the signs: a crack that grows, a rattle inside, dead or soft spots, or less power than when it was new. If you see them, ask the shop or the brand to look at it, and check whether it is still under warranty. Good care, protector tape and a cover all help a racket last longer.</p></div>
<p class="muted" style="margin-top:14px">Ready for a new one? Find the right shape and weight with the <a href="{href("racket-finder.html")}">racket finder</a>. Just slipping in your hand? It may only need a fresh overgrip: see <a href="{href("padel-overgrip.html")}">how often to change an overgrip</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Grip and overgrip</h3><p>How to wrap an overgrip and make a thin handle thicker, in the <a href="{href("racket-finder.html")}#grip">racket finder guide</a>.</p></div>
<div class="card"><h3>Your balls</h3><p>Flat balls are hard on your arm too. Run the <a href="{href("padel-balls.html")}">dead ball checker</a>.</p></div>
<div class="card"><h3>Your shoes</h3><p>Worn soles mean slips. Check the <a href="{href("padel-shoes.html")}">padel shoes guide</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Kit to keep your racket in shape</h3><p>A thermal racket bag and fresh overgrips are the cheapest ways to protect your racket. If yours is done, browse rackets by shape.</p><ul class="aff-links"><li><a href="{go("padel-bags")}" {AFF_ATTR}>Padel bags</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
rcare_faq = [
    ("How do you look after a padel racket?", "Wipe off sand and sweat after each game, dry it before you cover it, keep it in a cover in a dry place indoors, keep it out of the sun and the car, use protector tape on the frame and change the overgrip when it is slippery."),
    ("Can I leave my padel racket in the car?", "It's best not to. A car gets very hot in the sun and very cold in winter. Heat softens the foam core and cold makes it stiffer and easier to crack."),
    ("Does cold weather affect a padel racket?", "Yes. The foam core gets harder in the cold, so the racket feels stiffer and cracks are more likely. Let it warm up to room temperature before you play."),
    ("Is protector tape worth it on a padel racket?", "Yes for most players. It protects the top of the frame from knocks on the glass and the floor, which is where cracks often start. It adds a little weight to the head."),
    ("How much weight does protector tape add to a padel racket?", "Usually a few grams up to about 10 g. That moves the balance only a couple of millimetres towards the head, which most players barely feel."),
    ("How often should you replace padel protector tape?", "About every 2 to 3 months if you play regularly, or as soon as it is worn through or peeling."),
    ("How do you clean a padel racket?", "Use a dry, soft cloth after each game. For marks, use a cloth that is only slightly damp with a little mild soap, then dry it straight away. Never soak it or use strong cleaners."),
    ("How often should you change your padel overgrip?", "When it gets slippery, shiny or torn. That can be every few matches if you play a lot and sweat a lot, or every month or two if you play less."),
    ("How do I know if my padel racket is broken?", "Look for cracks in the frame or face, listen for a rattle inside, and notice dead spots, odd vibrations or a loss of power. If you find these, ask the shop or brand to check it."),
]
page("racket-care.html", "Padel Racket Care: Heat, Cold, Protector Tape, Health Check",
     "How to look after a padel racket: a 2-minute racket health check, cleaning, storage, heat and cold, protector tape, overgrips and the habits that crack frames.",
     rcare, rcare_faq, "Racket care")

# ---------------- PADEL DRILLS SESSION PLANNER ----------------
# Drills from LTA Padel "Padel training tips" and "Skills for beginners", and Padel Browser "Best padel drills, solo and partner" (Jun 2026). Own wording.
# who: player counts the drill works for. f: focus tags. g: what to count (empty = nothing to count).
DRILLS = [
    ("glass", "Back-glass rally on your own", [1], ["cons", "wall"], "Stand about two metres from the back glass. Hit the ball softly into the glass, let it come back and bounce once, then hit it again. Mix forehands and backhands.", "Best streak without a miss. Start by aiming for 20, then 50."),
    ("chase", "Corner rebound chase", [1], ["wall", "feet"], "From a back corner, hit the ball at an angle into the glass so it comes back across the court. Move to it, play it, and send it back to the same corner. Work for 90 seconds, then rest for 30.", "Balls played in 90 seconds."),
    ("taps", "Racket tap-ups", [1], ["cons"], "Tap the ball straight up off the racket, keeping it at about head height. To make it harder, turn the racket over and use the other face on every tap. You can do this at home.", "Best streak of taps."),
    ("wallv", "Volleys against a wall", [1], ["net"], "Find a solid wall outside the court. Stand two or three metres away and volley the ball against it without letting it bounce. Keep the racket up in front of you and use short punches, not big swings.", "Best streak of volleys."),
    ("serve", "Serve targets", [1, 2, 4], ["serve"], "Put four targets in the service box, such as cones, bottles or spare balls: two near the centre line and two near the side glass. Serve ten balls at each one, then serve from the other side. With a partner, they return each serve and you swap after 20.", "Serves that hit or land close to the target, out of 40."),
    ("feet", "Footwork and split step", [1, 2, 4], ["feet"], "No ball needed. Do short side steps along the baseline, quick in-and-out steps on a chalk grid or agility ladder, and a small hop (the split step) each time you imagine the opponent hitting. Stay on your toes.", ""),
    ("ladder", "Ladder rallies", [2, 4], ["cons"], "Rally on half the court. First keep the ball going for 2 shots, then 3, then 4, and so on. A miss sends you both back to 2. To make it harder, one player stays at the net and the other plays from the back.", "Highest rung you reach together."),
    ("feeds", "Back-glass feeds", [2, 4], ["wall"], "Stand on the same side of the net. The feeder throws the ball onto the floor just in front of the back glass. The player lets it come off the glass and plays it softly back into the feeder's hands. Swap after ten. Harder: feed into the corner so the ball hits two walls.", "Clean returns out of ten."),
    ("cross", "Cross-court rally", [2, 4], ["cons"], "Both players hit only diagonal, cross-court shots from the back of the court, at a steady pace. Count the rally as a team.", "Best team rally. Aim for 30, then 50."),
    ("volley", "Volley to volley", [2, 4], ["net"], "Both players stand at the net, two or three metres apart, and keep soft volleys going between you. No winners, just control.", "Best team streak of volleys."),
    ("netback", "One up, one back", [2, 4], ["net", "wall"], "One player at the net volleys calmly to a player at the back, who lets some balls come off the back glass before returning them. Swap roles halfway through.", "Longest rally."),
    ("lob", "Lob and overhead rotation", [2, 4], ["over"], "One player lobs from the back. The other moves back and plays a controlled bandeja, then a víbora or smash when the bandeja is reliable. After each overhead, step back in towards the net. Swap roles after 15 lobs.", "Overheads that land in, out of 15."),
    ("cards", "Yellow card, red card", [2, 4], ["cons", "game"], "Play normal games, one against one on half a court or two against two on the full court. Your first mistake in a game is a yellow card. A second mistake in the same game is a red card, and you lose that game.", "Games won."),
]
DR_FOCUS = [("mix", "A bit of everything"), ("cons", "Keeping the ball in play"), ("wall", "Playing off the glass"), ("net", "Volleys at the net"), ("over", "Lobs and overheads"), ("serve", "Serve and return")]
DR_JSON = json.dumps([{"id": a, "n": b, "who": c, "f": d, "d": x, "g": y} for a, b, c, d, x, y in DRILLS], ensure_ascii=False)
_WHO = {1: "On your own", 2: "With a partner", 4: "Four players"}
def _dcard(dr):
    i, n, who, f, d, g = dr
    pills = "".join(f'<span class="pill{" b" if w == 1 else " i"}">{_WHO[w]}</span>' for w in who)
    best = f'<label class="dr-pb">Your best <input type="number" min="0" max="9999" inputmode="numeric" data-pb="{i}" aria-label="Your best for {e(n)}"></label>' if g else ""
    return f'<div class="card dr-card" data-who="{" ".join(map(str, who))}"><h3>{e(n)}</h3><div class="dr-pills">{pills}</div><p>{e(d)}</p>{f"<p class=\"muted\"><b>Count:</b> {e(g)}</p>" if g else ""}{best}</div>'
drills = f'''<header class="hero"><div class="wrap"><h1>Padel drills session planner.</h1>
<p class="lead">Tell us who is practising, for how long and what you want to work on. You get a timed practice session built from simple padel drills, with a timer to run it on court and a place to log your records.</p>
{quick("Good padel drills for beginners are rallies with a target (keep the ball going for 10, then 20 shots), back-glass feeds, soft volleys at the net and serves at targets. Practise one skill at a time, warm up first, and count something in every drill so you can see progress. A 30-minute session can be a 5-minute warm-up, four 5-minute drills and a short game.")}</div></header>
<section style="padding-top:10px"><div class="wrap gen">
<div class="gen-main"><div class="card" id="dr-setup">
<h2 style="font-size:1.6rem">Build your session</h2>
<div class="q"><h3>Who is practising?</h3><div class="opts" data-dr="who" role="group" aria-label="Players"><button class="opt" type="button" data-v="1" aria-pressed="false">Just me</button><button class="opt" type="button" data-v="2" aria-pressed="true">Two players</button><button class="opt" type="button" data-v="4" aria-pressed="false">Four players</button></div></div>
<div class="q"><h3>How long?</h3><div class="opts" data-dr="len" role="group" aria-label="Session length"><button class="opt" type="button" data-v="20" aria-pressed="false">20 minutes</button><button class="opt" type="button" data-v="30" aria-pressed="true">30 minutes</button><button class="opt" type="button" data-v="45" aria-pressed="false">45 minutes</button><button class="opt" type="button" data-v="60" aria-pressed="false">60 minutes</button></div></div>
<div class="q"><h3>Your level</h3><div class="opts" data-dr="lv" role="group" aria-label="Level"><button class="opt" type="button" data-v="b" aria-pressed="true">New to padel</button><button class="opt" type="button" data-v="i" aria-pressed="false">Improving</button><button class="opt" type="button" data-v="a" aria-pressed="false">Experienced</button></div><p class="muted" style="margin:10px 0 0">Not sure? Try the <a href="{href("level-calculator.html")}">level calculator</a>.</p></div>
<div class="q"><h3>What do you want to work on?</h3><div class="opts" data-dr="focus" role="group" aria-label="Focus">{"".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="{"true" if v == "mix" else "false"}">{t}</button>' for v, t in DR_FOCUS)}</div></div>
<p class="muted" id="dr-sum" aria-live="polite"></p>
</div></div>
<aside class="gen-side"><div class="lb" id="dr-plan"><h2>Your session</h2><p>Pick your options to see the plan.</p></div></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Run the session with the timer</h2><p class="muted">Press start. It beeps for the last 3 seconds and when it is time to change drill.</p></div>
<div class="wu" id="dr">
<div class="wu-stage">
<div class="wu-bar"><span class="pill" id="dr-tot"></span><div class="seg" id="dr-snd" role="group" aria-label="Sound"><button type="button" data-v="on" aria-pressed="true">Beeps on</button><button type="button" data-v="off" aria-pressed="false">Off</button></div></div>
<div class="wu-main">
<svg class="wu-ring" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="10"/><circle id="dr-arc" cx="60" cy="60" r="52" fill="none" stroke="#e8f84a" stroke-width="10" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="0" transform="rotate(-90 60 60)"/></svg>
<div class="wu-time"><b id="dr-clock">5:00</b><span id="dr-of">Block 1</span></div>
</div>
<div class="wu-now" aria-live="polite"><span class="pill" id="dr-ph"></span><h2 id="dr-name"></h2><p id="dr-how"></p><p class="wu-next" id="dr-best"></p><p class="wu-next" id="dr-next"></p></div>
<div class="prog"><i id="dr-prog"></i></div>
<div class="wu-ctl"><button class="btn ghost sm" type="button" id="dr-back">Back</button><button class="btn lime" type="button" id="dr-go">Start</button><button class="btn ghost sm" type="button" id="dr-skip">Skip</button></div>
<p class="wu-left" id="dr-left"></p>
</div>
<ol class="wu-list" id="dr-list"></ol>
</div></div></section>
<script>window.DRL={DR_JSON};</script>
{AD.format("drills-mid")}
<section><div class="wrap"><div class="sh"><h2>All the drills</h2><div class="seg dr-filter" id="dr-filter" role="group" aria-label="Show drills for" style="background:#dfe8f7"><button type="button" data-v="all" aria-pressed="true">All</button><button type="button" data-v="1" aria-pressed="false">On your own</button><button type="button" data-v="2" aria-pressed="false">Two</button><button type="button" data-v="4" aria-pressed="false">Four</button></div></div>
<p class="muted">Type your best score into a drill and it is saved on this device, so you can try to beat it next time.</p>
<div class="grid" id="dr-lib">{"".join(_dcard(d) for d in DRILLS)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you plan a padel practice session?</h2></div><div class="grid">
<div class="card"><h3>Warm up first</h3><p>Start with a few minutes of easy movement and soft hitting before any drill. Our <a href="{href("warm-up.html")}">warm-up timer</a> gives you a 10 or 15 minute routine.</p></div>
<div class="card"><h3>One skill at a time</h3><p>LTA Padel advises working on one skill per session instead of everything at once. Pick one focus above and most of the session goes to it.</p></div>
<div class="card"><h3>Control before power</h3><p>Hit at a steady pace and aim for the target. New players can aim for about 20 clean shots in a row before they add movement or speed.</p></div>
<div class="card"><h3>Count something</h3><p>A streak, a score out of 40 or a rung on the ladder. Numbers show you are getting better and make drills more fun. Log them in the drill list.</p></div>
<div class="card"><h3>Finish with a game</h3><p>End with a game that rewards fewer mistakes, like yellow card, red card. It puts the drill work under a bit of match pressure.</p></div>
<div class="card"><h3>Swap roles often</h3><p>In partner drills, change who feeds and who hits every few minutes, so both players practise and nobody gets cold.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How should drills change with your level?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Level</th><th scope="col">What to focus on</th><th scope="col">How to make it harder</th></tr></thead><tbody>
<tr><td>New to padel</td><td>Control and a steady rhythm. Learn to let the ball come off the back glass.</td><td>Raise the target streak</td></tr>
<tr><td>Improving</td><td>Add movement: get back to your spot after every shot. Start overheads.</td><td>Play from one up, one back; feed into the corners</td></tr>
<tr><td>Experienced</td><td>Decisions and accuracy when tired. Bandeja and víbora under pressure.</td><td>Smaller targets; do your hardest drill at the end</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Footwork first</h3><p>Split step and recovery drills with a reaction trainer: <a href="{href("padel-footwork.html")}">padel footwork</a>.</p></div>
<div class="card"><h3>Practise your serve</h3><p>Log 10 serves per target and see your serve percentage with the <a href="{href("how-to-serve-padel.html")}">serve practice tracker</a>.</p></div>
<div class="card"><h3>Fix one problem first</h3><p>Not sure what to drill? The <a href="{href("fix-my-padel.html")}">padel problem fixer</a> gives a drill with reps for your biggest leak.</p></div>
<div class="card"><h3>Learn the shots</h3><p>See how the bandeja, víbora and chiquita are played in the <a href="{href("shots.html")}">shot library</a>.</p></div>
<div class="card"><h3>No partner today?</h3><p>Wall, empty court or home: build a 10 to 30 minute session with the <a href="{href("padel-solo-practice.html")}">solo practice timer</a>.</p></div>
<div class="card"><h3>Know where to stand</h3><p>Drills work better when you recover to the right spot. See the <a href="{href("positioning.html")}">positioning guide</a>.</p></div>
<div class="card"><h3>Plan four weeks</h3><p>Turn these drills into a week-by-week plan with the <a href="{href("padel-training-plan.html")}">padel training plan generator</a>.</p></div>
<div class="card"><h3>Play a fun format</h3><p>Got eight or more players? Try <a href="{href("king-of-the-court.html")}">King of the Court</a> or an <a href="{href("americano.html")}">Americano</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Practice kit</h3><p>Drills use a lot of balls. A bag of spare balls and a fresh overgrip make practice easier. Old balls are fine for drills, just not for matches.</p><ul class="aff-links"><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Padel bags</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>Rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
drills_faq = [
    ("What are good padel drills for beginners?", "Rallies with a target streak, back-glass feeds where a partner throws the ball at the glass for you, soft volleys at the net, serves at targets and racket tap-ups at home. Keep them slow and count your best streak."),
    ("How long should a padel practice session be?", "20 to 60 minutes works. Even 20 minutes a week on top of your matches helps. Spend a few minutes warming up, most of the time on one skill, and finish with a short game."),
    ("Can you practise padel on your own?", "Yes. You can rally against the back glass, chase rebounds from the corners, serve at targets, volley against a wall and tap the ball up on your racket at home."),
    ("What padel drills can two players do?", "Ladder rallies on half court, cross-court rallies, volley to volley at the net, back-glass feeds, one up one back, lobs and overheads, and the yellow card, red card game."),
    ("How do you practise playing off the back glass?", "Have a partner throw the ball onto the floor just in front of the back glass. Let it come off the glass, then play it softly back. When that is easy, feed into the corner so it hits two walls."),
    ("What is the yellow card, red card padel drill?", "A game where your first mistake in a game is a yellow card and your second is a red card, which loses you that game. It rewards keeping the ball in play."),
]
page("drills.html", "Padel Drills Session Planner: Free Practice Plan and Timer | Padel Glass Box",
     "Free padel drills planner: pick players, time, level and focus to get a timed practice session from 13 drills for one, two or four players.",
     drills, drills_faq, "Padel drills")

# ---------------- KING OF THE COURT ----------------
# Format: Padel Browser "Padel tournament formats: Americano and King of the Court" (winners up a court, losers down, partners rotate, most rounds on court 1)
# and Champion of the Court Padel rules (winners move up a court, losers down, top/bottom stay, partners change every round, final-round court 1 winners).
kotc = f'''<header class="hero"><div class="wrap"><h1>King of the Court padel generator.</h1>
<p class="lead">Run a King of the Court night on two or more courts. Enter your players, tap the winners on each court, and the next round is made for you: winners move up, losers move down, and partners change. Live table, round timer, saved on this device.</p>
{quick("In padel King of the Court, courts are ranked from court 1 (the king court) down. After each short round, the winning pair moves up one court and the losing pair moves down one; winners on court 1 stay, and losers on the bottom court stay. In most versions you change partner every round. The king is the player who spent the most rounds on court 1, or who won court 1 in the last round.")}</div></header>
<section style="padding-top:10px"><div class="wrap gen">
<div class="gen-main">
<div class="card" id="kc-setup">
<h2 style="font-size:1.6rem">Set up King of the Court</h2>
<div class="q"><h3>Partners</h3><div class="opts" data-kc="mode" role="group" aria-label="Partners"><button class="opt" type="button" data-v="split" aria-pressed="true">Change partner every round</button><button class="opt" type="button" data-v="fixed" aria-pressed="false">Fixed pairs</button></div><p class="muted" id="kc-mode-note" style="margin:10px 0 0"></p></div>
<div class="q"><h3><label for="kc-names">Players, one name per line (8, 12, 16, 20, 24 or 28)</label></h3><textarea class="search" id="kc-names" rows="8" placeholder="Sam&#10;Priya&#10;Omar&#10;Lucia&#10;..."></textarea><p class="muted" id="kc-count" style="margin:-6px 0 0"></p></div>
<div class="q"><h3>Who is king?</h3><div class="opts" data-kc="champ" role="group" aria-label="How the winner is decided"><button class="opt" type="button" data-v="top" aria-pressed="true">Most rounds on court 1</button><button class="opt" type="button" data-v="last" aria-pressed="false">Wins court 1 in the last round</button><button class="opt" type="button" data-v="wins" aria-pressed="false">Most wins</button></div></div>
<div class="q"><h3>Round length</h3><div class="opts" data-kc="len" role="group" aria-label="Round length"><button class="opt" type="button" data-v="8" aria-pressed="false">8 minutes</button><button class="opt" type="button" data-v="10" aria-pressed="true">10 minutes</button><button class="opt" type="button" data-v="12" aria-pressed="false">12 minutes</button><button class="opt" type="button" data-v="15" aria-pressed="false">15 minutes</button></div></div>
<div class="gen-nums"><div class="q"><h3><label for="kc-rounds">Rounds</label></h3><input class="search" id="kc-rounds" type="number" min="2" max="20" value="8" inputmode="numeric"></div><div class="q"><h3>Courts</h3><p class="muted" id="kc-courts" style="margin:0">Add players to see</p></div></div>
<p class="msg" id="kc-err" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:4px"><button class="btn lime" type="button" id="kc-start">Make round 1</button><button class="btn ghost" type="button" id="kc-demo">Fill 12 sample names</button></div>
</div>
<div id="kc-live" hidden>
<div class="card gen-bar"><div><span class="pill b" id="kc-sum"></span></div><div class="btns" style="margin:0"><button class="btn ghost sm" type="button" id="kc-copy">Copy table</button><button class="btn ghost sm" type="button" id="kc-new">New event</button></div></div>
<div class="card kc-timer"><div><b id="kc-clock">10:00</b><span>Round timer</span></div><div class="btns" style="margin:0"><button class="btn lime sm" type="button" id="kc-tgo">Start timer</button><button class="btn ghost sm" type="button" id="kc-treset">Reset</button></div></div>
<div id="kc-round"></div>
<p class="msg" id="kc-rerr" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns"><button class="btn" type="button" id="kc-next">Make next round</button><button class="btn ghost sm" type="button" id="kc-undo">Remove last round</button></div>
<div class="card"><h2 style="font-size:1.4rem">Earlier rounds</h2><div id="kc-hist"><p class="muted">Finished rounds appear here.</p></div></div>
</div>
</div>
<aside class="gen-side"><div class="lb" id="kc-board"><h2>The table</h2><p>Make round 1 and tap the winners to see who is king.</p></div></aside>
</div></section>
{AD.format("kotc-mid")}
<section><div class="wrap"><div class="sh"><h2>How does King of the Court work in padel?</h2></div><div class="grid">
<div class="card"><h3>Courts are ranked</h3><p>Court 1 is the king court. The other courts go down in order: court 2, court 3 and so on. Everyone wants to get to court 1 and stay there.</p></div>
<div class="card"><h3>Short rounds</h3><p>Each round is short, often a timed round of about 10 to 15 minutes, or a quick game to a set number of points. Everyone starts and stops at the same time.</p></div>
<div class="card"><h3>Winners up, losers down</h3><p>The winning pair on each court moves up one court. The losing pair moves down one. Winners on court 1 stay, and losers on the bottom court stay.</p></div>
<div class="card"><h3>New partners</h3><p>In the usual version, the two pairs that arrive on a court split up, so you play with someone new each round. With fixed pairs, the pair moves together.</p></div>
<div class="card"><h3>Who is king?</h3><p>Groups use different rules: most rounds played on court 1, the winners of court 1 in the final round, or simply most wins. Pick one before you start.</p></div>
<div class="card"><h3>A draw when time runs out?</h3><p>Agree a tie rule first. A simple one is to play one more deciding point, like a <a href="{href("golden-point-star-point.html")}">golden point</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How many players and courts do you need?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Players</th><th scope="col">Courts</th><th scope="col">8 rounds of 10 minutes</th></tr></thead><tbody>
<tr><td>8</td><td>2</td><td>About 1 hour 35 minutes</td></tr>
<tr><td>12</td><td>3</td><td>About 1 hour 35 minutes</td></tr>
<tr><td>16</td><td>4</td><td>About 1 hour 35 minutes</td></tr>
<tr><td>20 or more</td><td>5 or more</td><td>Same time: more courts, not more rounds</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Times assume about 2 minutes to change courts between rounds. You need four players per court, so the number of players must be a multiple of four. With other numbers, use the <a href="{href("americano.html")}">Americano draw maker</a>, which handles rests.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>King of the Court, Americano, Mexicano or round robin?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Format</th><th scope="col">Partners</th><th scope="col">How you win</th><th scope="col">Feels like</th></tr></thead><tbody>
<tr><td>King of the Court</td><td>Usually change every round</td><td>Time on court 1, or court 1 at the end</td><td>Fast and competitive, with movement every round</td></tr>
<tr><td><a href="{href("americano.html")}">Americano</a></td><td>Change every round, planned</td><td>Most points in total</td><td>Social: you play with everyone</td></tr>
<tr><td><a href="{href("americano.html")}">Mexicano</a></td><td>Change every round, by score</td><td>Most points in total</td><td>Social but levels sort themselves out</td></tr>
<tr><td><a href="{href("round-robin.html")}">Round robin</a></td><td>Fixed pairs</td><td>Best record in the table</td><td>A mini league</td></tr><tr><td><a href="{href("padel-tournament-bracket.html")}">Knockout</a></td><td>Fixed pairs</td><td>Last pair unbeaten</td><td>A one-day cup</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Keep score on court</h3><p>Put a phone by the net and use the free <a href="{href("score.html")}">score keeper</a>.</p></div>
<div class="card"><h3>Warm up together</h3><p>Start the night with the 10-minute <a href="{href("warm-up.html")}">warm-up timer</a>.</p></div>
<div class="card"><h3>Running a season?</h3><p>Keep a ranking going between nights with the <a href="{href("ladder.html")}">padel ladder tracker</a>.</p></div>
</div></div></section>'''
kotc_faq = [
    ("What is King of the Court in padel?", "A social format on several courts. Court 1 is the king court. After each short round, the winners move up one court and the losers move down one, so the best players end up fighting for court 1."),
    ("How many players do you need for King of the Court?", "At least eight players on two courts. You need four players per court, so 8, 12, 16 or 20 players fit best."),
    ("Do you change partners in King of the Court?", "In the usual version, yes: the pairs that arrive on each court split up, so you play with someone new each round. Some groups play with fixed pairs instead, and this generator supports both."),
    ("How long is a King of the Court round?", "Rounds are short, often 10 to 15 minutes, or a quick game to a set number of points. Pick one length and start and stop every court at the same time."),
    ("Who wins King of the Court?", "It depends on the rule you agree: the player with the most rounds on court 1, the pair that wins court 1 in the last round, or the most wins overall. The generator tracks all three."),
    ("What happens to the winners on court 1?", "They stay on court 1. Losers on the bottom court also stay where they are. Everyone else moves one court up or down."),
]
page("king-of-the-court.html", "King of the Court Padel Generator: Rounds, Courts, Table",
     "Free King of the Court padel generator for 8 to 28 players: tap the winners for the next round, winners up and losers down, with a timer and live table.",
     kotc, kotc_faq, "King of the Court")

# ---------------- TIE-BREAK ----------------
# Sources: FIP Rules of Padel PDF (in force 01.01.2026): Rule 1 tie-break 1.1-1.5, alternative score methods 1(b) and 1(c),
# 2.4 (20 s between points), 2.5 (90 s change of ends, no rest after game 1 or during a tie-break), 2.6 (120 s end of set),
# 2.10 (20 s change of ends in a tie-break), 5.1 (change ends after odd games), 5.2 (tie-break: change ends every 6 points).
# Cross-check: Bounce "Padel scoring" (Jul 2026), LTA Padel rules page (7 points, 2 clear).
def _tb_row(n):
    srv = 0 if n == 0 else ((n + 1) // 2) % 4
    lab = ["Player 1 (team A)", "Player 2 (team B)", "Player 3 (team A)", "Player 4 (team B)"][srv]
    side = "Right" if n % 2 == 0 else "Left"
    ends = "Change ends after this point" if (n + 1) % 6 == 0 else ""
    return f"<tr><td>{n + 1}</td><td>{lab}</td><td>{side}</td><td>{ends}</td></tr>"
TB_COURT = '''<svg viewBox="0 0 440 240" id="tb-court" role="img" aria-label="Top view of a padel court showing who serves next, from which side, and into which box">
<rect x="10" y="10" width="420" height="220" rx="8" fill="#1d55e6"/>
<rect id="tb-box" x="220" y="20" width="139" height="100" fill="#e8f84a" opacity=".28"/>
<path d="M20 20h400v200H20z" fill="none" stroke="#fff" stroke-width="2.5"/>
<path d="M81 20v200M359 20v200M81 120h278" stroke="#fff" stroke-width="2"/>
<path d="M220 14v212" stroke="#e4eef6" stroke-width="5"/>
<rect x="10" y="10" width="420" height="220" rx="8" fill="none" stroke="#9cc4ea" stroke-width="8" opacity=".6"/>
<text id="tb-lname" x="50" y="126" text-anchor="middle" fill="#fff" font-family="sans-serif" font-weight="800" font-size="13" transform="rotate(-90 50 120)">Team A</text>
<text id="tb-rname" x="390" y="126" text-anchor="middle" fill="#fff" font-family="sans-serif" font-weight="800" font-size="13" transform="rotate(90 390 120)">Team B</text>
<path id="tb-arrow" d="M60 170 L290 70" fill="none" stroke="#e8f84a" stroke-width="2.5" stroke-dasharray="6 6"/>
<circle id="tb-srv" cx="60" cy="170" r="10" fill="#e8f84a" stroke="#0b1530" stroke-width="2"/>
</svg>'''
tb = f'''<header class="hero"><div class="wrap"><h1>Padel tie-break rules, point by point.</h1>
<p class="lead">Not sure who serves next in a tie-break, or when to change ends? Enter the four players, tap who wins each point, and the tracker shows the next server, the side to serve from and when to swap ends.</p>
{quick("At 6-6 padel plays a tie-break: first to 7 points with a 2-point lead wins, and the set ends 7-6. The next server in the set's order serves point 1 from the right. After that each player serves two points in turn (first from the left, then the right), keeping the same order. Change ends after every 6 points. A match tie-break (super tie-break) at one set all is the same, but first to 10.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="score" id="tb">
<div class="score-top"><div class="seg" id="tb-type" role="group" aria-label="Tie-break type"><button type="button" data-v="7" aria-pressed="true">Set tie-break (to 7)</button><button type="button" data-v="10" aria-pressed="false">Match tie-break (to 10)</button></div>
<div class="btns" style="margin:0"><button class="btn sm" type="button" id="tb-undo">Undo</button><button class="btn sm" type="button" id="tb-reset">Start again</button></div></div>
<details class="tb-names"><summary>Player names and serve order</summary>
<p class="muted" style="color:#c9d6fb">Put the players in serving order. Player 1 is the player whose turn it is to serve after 6-6. Players 1 and 3 are team A; players 2 and 4 are team B.</p>
<div class="tb-grid">
<label>Player 1, serves first (team A)<input class="search" id="tb-n0" maxlength="18" placeholder="Player 1"></label>
<label>Player 2, serves next (team B)<input class="search" id="tb-n1" maxlength="18" placeholder="Player 2"></label>
<label>Player 3, partner of player 1<input class="search" id="tb-n2" maxlength="18" placeholder="Player 3"></label>
<label>Player 4, partner of player 2<input class="search" id="tb-n3" maxlength="18" placeholder="Player 4"></label>
</div></details>
<div class="tb-now" aria-live="polite"><div><span>Next serve</span><b id="tb-who">Player 1</b><i id="tb-side">from the right side</i></div><div class="tb-sc"><b id="tb-a">0</b><span>-</span><b id="tb-b">0</b></div></div>
<p class="tb-alert" id="tb-alert" role="status"></p>
<div class="court-art tb-art">{TB_COURT}</div>
<div class="teams tb-btns" style="margin-top:12px"><button class="btn lime" type="button" data-w="0" id="tb-wa">Team A wins the point</button><button class="btn lime" type="button" data-w="1" id="tb-wb">Team B wins the point</button></div>
<div class="tb-log" id="tb-log"></div>
<div class="btns" style="margin-top:10px"><button class="btn sm" type="button" id="tb-copy">Copy result</button><button class="btn sm" type="button" id="tb-rand">Play a random tie-break</button></div>
</div>
<p class="muted" style="margin-top:14px">Saved on this device, so you can close the page between points. Playing a full match? The <a href="{href("score.html")}">score keeper</a> counts points, games, sets and tie-breaks.</p>
</div></section>
{AD.format("tb-mid")}
<section><div class="wrap"><div class="sh"><h2>How does a padel tie-break work?</h2></div><div class="grid">
<div class="card"><h3>When it starts</h3><p>When a set reaches 6-6. The tie-break is the last game of the set, and the pair that wins it wins the set 7-6.</p></div>
<div class="card"><h3>How you count</h3><p>Forget 15, 30, 40. In a tie-break you count 0, 1, 2, 3 and so on. The first pair to 7 points wins, but you must be 2 points ahead, so 7-6 is not enough: play on to 8-6, 9-7 and so on.</p></div>
<div class="card"><h3>The first serve</h3><p>The player whose turn it is to serve in the set serves the first point only, from the right side of the court.</p></div>
<div class="card"><h3>Then two serves each</h3><p>The other pair serves the next two points, then each player serves two points in a row, in the same order as the rest of the set. The first of each two is served from the left, the second from the right.</p></div>
<div class="card"><h3>Change ends every 6 points</h3><p>Swap ends after 6, 12, 18 points and so on. There is no long rest: play is meant to be continuous, and the FIP rules give 20 seconds for the change.</p></div>
<div class="card"><h3>The next set</h3><p>The next set starts with a serve from the pair that did not serve first in the tie-break.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Who serves each point of a padel tie-break?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Point</th><th scope="col">Server</th><th scope="col">Serves from</th><th scope="col">Ends</th></tr></thead><tbody>
{"".join(_tb_row(n) for n in range(12))}
</tbody></table></div>
<p class="muted" style="margin-top:12px">The pattern carries on the same way after point 12. "Right" and "left" are from the server's point of view, looking at the net. Player 1 is whoever is next to serve in the set; players 1 and 3 are partners.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Tie-break or super tie-break: what is the difference?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Set tie-break</th><th scope="col">Match tie-break (super tie-break)</th></tr></thead><tbody>
<tr><td>When</td><td>A set reaches 6-6</td><td>At one set all, instead of a third set</td></tr>
<tr><td>Points to win</td><td>7, with a 2-point lead</td><td>10, with a 2-point lead</td></tr>
<tr><td>Result</td><td>Set won 7-6</td><td>Wins the match</td></tr>
<tr><td>Serve order</td><td>1 point, then 2 each</td><td>1 point, then 2 each</td></tr>
<tr><td>Is it always used?</td><td>Yes, unless the event plays a final set with no tie-break</td><td>Only if the organiser chooses it</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">The FIP lists the 10-point match tie-break, and a 7-point one, as other ways to settle a match at one set all. The rules give "every 6 points" for changing ends in a tie-break; this tracker uses the same for the 10-point version. Check with your organiser.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When do you change ends in padel?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Moment</th><th scope="col">What happens</th><th scope="col">Time allowed (FIP)</th></tr></thead><tbody>
<tr><td>Between points</td><td>No change</td><td>Up to 20 seconds</td></tr>
<tr><td>After games 1, 3, 5 and every odd game</td><td>Change ends</td><td>Up to 90 seconds, but no rest after game 1</td></tr>
<tr><td>In a tie-break, every 6 points</td><td>Change ends</td><td>20 seconds, play is continuous</td></tr>
<tr><td>End of a set</td><td>Rest</td><td>Up to 120 seconds</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Common tie-break mix-ups</h2></div><div class="grid">
<div class="card"><h3>"First to 7 wins"</h3><p>Only with a 2-point lead. At 6-6 in the tie-break, keep going until one pair is 2 points clear.</p></div>
<div class="card"><h3>"Golden point at 6-6 in the tie-break"</h3><p>Golden point and Star Point are for 40-40 in a normal game. A tie-break is counted in single points and needs 2 clear. <a href="{href("golden-point-star-point.html")}">How deuce formats work</a>.</p></div>
<div class="card"><h3>Serving from the wrong side</h3><p>Point 1 is served from the right. After that, each player serves their first point from the left and their second from the right.</p></div>
<div class="card"><h3>Forgetting to swap ends</h3><p>Use the total of both scores: when it reaches 6, 12 or 18, swap. At 4-2, 5-1 or 3-3 it's time to change.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Keep the whole score</h3><p>Points, games, sets and tie-breaks on one phone with the <a href="{href("score.html")}">score keeper</a>.</p></div>
<div class="card"><h3>Serve it right</h3><p>Check feet, height and bounce with the <a href="{href("serve-rules.html")}">serve rules checker</a>.</p></div>
<div class="card"><h3>All the rules</h3><p>Walls, net and scoring on a court you can tap: <a href="{href("rules.html")}">padel rules</a>.</p></div>
</div></div></section>'''
tb_faq = [
    ("How many points is a padel tie-break?", "A set tie-break is first to 7 points with a 2-point lead, so it can go past 7, for example 8-6 or 10-8. A match tie-break (super tie-break) is first to 10, also with a 2-point lead."),
    ("Who serves first in a padel tie-break?", "The player whose turn it is to serve in the set. They serve only the first point, from the right. Then the other pair serves two points, and everyone serves two points in turn."),
    ("When do you change ends in a padel tie-break?", "After every 6 points: when the total score reaches 6, 12, 18 and so on. The change should be quick; the FIP rules allow 20 seconds."),
    ("What is a super tie-break in padel?", "A tie-break to 10 points, 2 clear, played at one set all instead of a full third set. It is an option the organiser can choose, often used in club leagues and some events."),
    ("Who serves first in the set after a tie-break?", "The pair that did not serve first in the tie-break starts the next set."),
    ("Is there a golden point in a padel tie-break?", "No. Golden point and Star Point are ways to settle 40-40 in a normal game. In a tie-break you need to win by 2 points."),
    ("What is the score of a set won on a tie-break?", "7-6. The tie-break counts as the deciding game of the set."),
]
page("tie-break.html", "Padel Tie-Break Rules: Who Serves and When to Change Ends",
     "Padel tie-break rules made simple: first to 7, 2 clear, serve order and changing ends every 6 points. Free tracker for set and match tie-breaks.", tb, tb_faq, "Tie-break rules")

# ---------------- OUT-OF-COURT PLAY ----------------
# Calls follow the FIP Rules of Padel PDF (in force 01.01.2026): rule 16, 12.3, 13.1(b)(d)(e)(g)(p), 14.1(a)(j), 7.1(f), 10.1, 11, plus the Court section
# (safety area 3 m wide (4 m recommended) x 4 m long x 3 m high, 2 accesses per side, 2 cm padding, no light poles in the area). Ball x,y on the 400x260 top view.
OC = {
    "side": {"p": [150, 34], "y": ["good", "Play on: go and get it", "Their shot bounced in your court first, then left over the side wall. On this court you may run out through the door and hit it back before it bounces a second time outside.", "FIP rules 12.3, 13.1(e) and 16"], "n": ["lose", "You lose the point", "Their shot bounced in your court and then left over the side wall. Where out-of-court play is not allowed, that ends the point in their favour. It was a good shot.", "FIP rule 13.1(d)"]},
    "door": {"p": [186, 30], "y": ["good", "Play on: go and get it", "A ball that bounces in your court and then goes out through the door is still in play here. Follow it out and return it before its second bounce.", "FIP rules 13.1(e) and 16"], "n": ["lose", "You lose the point", "Without out-of-court play, a ball that bounces in your court and then goes out through the door wins the point for the team that hit it.", "FIP rule 13.1(d)"]},
    "end": {"p": [24, 130], "y": ["let", "Check your local rule", "The ball bounced in your court, then flew out over your back wall. FIP lists this case, but the 2026 text does not clearly say what happens next. On most courts there is no way to reach it anyway. Agree with your opponents or ask the umpire.", "FIP rule 13.1(e), which is unclear here"], "n": ["lose", "You lose the point", "Without out-of-court play, a ball that bounces in your court and then goes out over the back wall wins the point for the other team.", "FIP rule 13.1(d)"]},
    "two": {"p": [140, 22], "y": ["lose", "You lose the point", "You may play the ball outside, but only before it bounces a second time. Once it bounces outside, the point is over.", "FIP rule 13.1(e)"], "n": ["lose", "You lose the point", "Here the point ended when the ball left the court. A second bounce outside doesn't change anything.", "FIP rule 13.1(d)"]},
    "obj": {"p": [120, 26], "y": ["lose", "You lose the point", "Outside the court, the ball must not touch anything that isn't part of the court: a bench, a light pole, another court's fence or a person. If it does before you hit it, you lose the point.", "FIP rule 13.1(e)"], "n": ["lose", "You lose the point", "The point already ended when the ball left the court, so what it hit outside doesn't matter.", "FIP rule 13.1(d)"]},
    "back": {"p": [300, 120], "y": ["good", "Good shot, play on", "A return hit from outside the court counts if it meets the normal rules: it crosses the net and bounces in their court before touching their walls or fence. It can come back over the wall or in through the door.", "FIP rule 14.1(j)"], "n": ["lose", "Not possible here", "On a court without out-of-court play you can't hit the ball from outside, so this situation can't happen. The point ended when the ball left.", "FIP rules 13.1(d) and 13.1(p)"]},
    "vol": {"p": [228, 110], "y": ["good", "Play on: they may volley it", "There is no special rule for balls coming back from outside. The other team may volley your return before it bounces, the same as any other ball.", "FIP rule 14.1(a)"], "n": ["lose", "Not possible here", "Without out-of-court play, the point ended when the ball left the court.", "FIP rule 13.1(d)"]},
    "glass": {"p": [342, 100], "y": ["lose", "You lose the point", "Your return from outside went straight into their glass or fence without bouncing on their ground first. As with any shot, that loses the point.", "FIP rule 13.1(g)"], "n": ["lose", "You lose the point", "Any shot that hits their walls or fence before bouncing on their ground loses the point.", "FIP rule 13.1(g)"]},
    "feet": {"p": [176, 52], "y": ["good", "Allowed here", "On a court with out-of-court play, your feet may be outside the court when you hit the ball.", "FIP rules 13.1(p) and 16"], "n": ["lose", "You lose the point", "On a court without out-of-court play, you lose the point if a foot or any part of your body is outside the court when you hit the ball.", "FIP rule 13.1(p)"]},
    "post": {"p": [200, 60], "y": ["good", "Allowed", "On courts with out-of-court play, the upright post in the doorway is a neutral zone above 0.92 m. Any of the four players may touch it or hold it to turn.", "FIP rule 13.1(b)"], "n": ["let", "Agree before you play", "FIP only names the door post a neutral zone on courts with out-of-court play. For other courts the rules say nothing about it, so agree with your opponents.", "FIP rule 13.1(b)"]},
    "serve": {"p": [210, 30], "y": ["good", "In play", "Your serve bounced in the box and then went out through the door. On a court with out-of-court play, it stays in play and the receiver may run out to return it.", "FIP rules 7.1(f) and 13.1(e)"], "n": ["lose", "Fault", "On a court without out-of-court play, a serve that bounces in the box and then goes straight out through the door is a fault.", "FIP rule 7.1(f)"]},
    "inv": {"p": [110, 150], "y": ["let", "Let: replay the point", "A ball from another court, or anything else that comes onto your court during the point, is a let. Call it straight away: if you keep playing, you lose the right to a let.", "FIP rule 10.1"], "n": ["let", "Let: replay the point", "A ball from another court, or anything else that comes onto your court during the point, is a let. Call it straight away: if you keep playing, you lose the right to a let.", "FIP rule 10.1"]},
}
def _oq(label, opts):
    return f'<div class="q oc-q"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
OC_SVG = '''<svg viewBox="0 0 400 260" class="wr-court" role="img" aria-label="Top view of a padel court with the door openings and the clear area outside. The ball shows where the situation happens.">
<rect x="0" y="0" width="400" height="260" rx="14" fill="#0e2468"/>
<g class="oc-zone"><rect x="144" y="14" width="112" height="42" rx="4" fill="#e8f84a" opacity=".12" stroke="#e8f84a" stroke-dasharray="4 4" stroke-opacity=".6"/><rect x="144" y="204" width="112" height="42" rx="4" fill="#e8f84a" opacity=".12" stroke="#e8f84a" stroke-dasharray="4 4" stroke-opacity=".6"/>
<text x="200" y="38" text-anchor="middle" font-size="8.5" fill="#e8f84a" font-family="Onest, sans-serif">clear area</text><text x="200" y="228" text-anchor="middle" font-size="8.5" fill="#e8f84a" font-family="Onest, sans-serif">clear area</text></g>
<rect x="60" y="60" width="280" height="140" fill="#1e46c8"/>
<path d="M88 60v140M312 60v140M88 130h224" stroke="#fff" stroke-width="1.5" opacity=".8"/>
<path d="M200 56v148" stroke="#e4eef6" stroke-width="4"/>
<g stroke="#9cc4ea" stroke-width="5" fill="none" stroke-linecap="round"><path d="M60 60v140M340 60v140"/><path d="M60 60h112M228 60h112M60 200h112M228 200h112"/><path d="M190 60h8M202 60h8M190 200h8M202 200h8"/></g>
<text x="130" y="196" text-anchor="middle" font-size="9" fill="#cfe0ff" font-family="Onest, sans-serif">Your side</text><text x="270" y="196" text-anchor="middle" font-size="9" fill="#cfe0ff" font-family="Onest, sans-serif">Their side</text>
<text x="200" y="252" text-anchor="middle" font-size="8" fill="#9fb0e0" font-family="Onest, sans-serif">Gaps in the side walls are the doors</text>
<circle id="oc-ring" cx="130" cy="130" r="13" fill="none" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 3" opacity="0"/>
<circle id="oc-ball" cx="130" cy="130" r="6" fill="#e8f84a" stroke="#0b1530" stroke-width="1.5"/>
</svg>'''
OC_COURT = [
    ("door", "There are two openings (doors) on each side of the court"),
    ("zone", "Outside each door there is a clear area with nothing in it: at least 3 m wide and 4 m long"),
    ("high", "There is at least 3 m of clear height above that area"),
    ("pad", "The door frames and net posts by the openings are padded"),
    ("pole", "No light poles, benches or fences stand inside that area"),
    ("club", "The club or organiser says out-of-court play is allowed"),
]
ocp = f'''<header class="hero"><div class="wrap"><h1>Padel out-of-court play: when can you leave the court?</h1>
<p class="lead">The ball bounced and flew out through the door. Can you chase it? Choose the type of court, tap what happened, and get the call with the FIP rule number.</p>
{quick("Only on courts built for it. If the ball bounces in your court and then goes out over the side wall or through the door, you may run out and hit it back before it bounces a second time, if the court has door openings and a clear area outside (at least 3 m wide and 4 m long). On courts without that space, a ball that bounces and leaves the court wins the point for the team that hit it.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="oc">
<div>
<div class="q"><h3>What kind of court are you on?</h3><div class="seg" id="oc-mode" role="group" aria-label="Is out-of-court play allowed?"><button type="button" data-v="y" aria-pressed="true">Out-of-court play allowed</button><button type="button" data-v="n" aria-pressed="false">Not allowed</button></div>
<p class="muted" style="margin:10px 0 0">Not sure? Use the <a href="#court-check">court check</a> below, or ask the club.</p></div>
{_oq("The ball left the court", [("side", "It bounced on my side, then went over the side wall"), ("door", "It bounced on my side, then went out through the door"), ("end", "It bounced on my side, then went over my back wall"), ("two", "It bounced a second time outside before I hit it"), ("obj", "Outside, it hit a bench, a pole or a person")])}
{_oq("Hitting it back from outside", [("back", "I hit it back and it bounced in their court"), ("vol", "They volleyed my return before it bounced"), ("glass", "My return hit their glass before the ground"), ("feet", "My feet were outside the court when I hit it")])}
{_oq("Other calls by the door", [("post", "I grabbed the door post to turn"), ("serve", "My serve bounced in the box, then went out the door"), ("inv", "A ball from another court came onto ours")])}
<button class="btn sm" type="button" id="oc-reset">Start again</button>
</div>
<aside class="result" id="oc-out" aria-live="polite"><div class="wr-svg">{OC_SVG}</div><div id="oc-txt"><h2>Make the call</h2><p>Pick the court type, then tap a situation. The verdict appears here.</p></div></aside>
</div></div></section>
{AD.format("oc-mid")}
<section><div class="wrap"><div class="sh"><h2>What is out-of-court play in padel?</h2></div><div class="grid">
<div class="card"><h3>The idea</h3><p>Your opponents hit a good shot: it bounces in your court and flies out over the side wall or through the door. On some courts you may follow it out and hit it back from outside. In Spanish this is called salida de pista (sa-LEE-da de PEES-ta, "leaving the court").</p></div>
<div class="card"><h3>Who allows it</h3><p>FIP rule 16 allows it whenever the court meets the safety conditions. In practice the club or organiser tells you if it's on. Many club courts don't have the space, so ask before the match.</p></div>
<div class="card"><h3>The one rule to remember</h3><p>You must hit the ball before it bounces a second time, and before it touches anything outside the court. Your return then follows the normal rules: over the net and onto their ground first.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Out-of-court play at a glance</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">What happened</th><th scope="col">Out-of-court play allowed</th><th scope="col">Not allowed</th></tr></thead><tbody>
<tr><td>Bounced in your court, out over the side wall</td><td>Play on: chase it</td><td>You lose the point</td></tr>
<tr><td>Bounced in your court, out through the door</td><td>Play on: chase it</td><td>You lose the point</td></tr>
<tr><td>Bounced in your court, out over the back wall</td><td>Unclear in FIP text: agree locally</td><td>You lose the point</td></tr>
<tr><td>Bounced twice, or touched something outside</td><td>You lose the point</td><td>You lose the point</td></tr>
<tr><td>Your feet outside when you hit the ball</td><td>Allowed</td><td>You lose the point</td></tr>
<tr><td>Serve bounces in the box, then out the door</td><td>In play</td><td>Fault</td></tr>
<tr><td>Holding the door post above 0.92 m</td><td>Allowed (neutral zone)</td><td>Not covered: agree first</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">"You" is the team that has to return the ball. The rule numbers are in the checker above.</p></div></section>
<section style="padding-top:0" id="court-check"><div class="wrap"><div class="sh"><h2>Is your court built for out-of-court play?</h2></div>
<div class="quiz" id="occ"><div><div class="q"><h3>Tick what is true at your court</h3><ul class="check" id="occ-list">{"".join(f'<li><label><input type="checkbox" data-k="{k}"><span>{t}</span></label></li>' for k, t in OC_COURT)}</ul></div>
<button class="btn sm" type="button" id="occ-reset">Clear</button></div>
<aside class="result" id="occ-out" aria-live="polite"><h2>Court check</h2><p>Tick what you can see at your court and the answer appears here.</p></aside></div>
<p class="muted" style="margin-top:14px">These points come from the court section of the FIP rules: two openings per side, a clear area at least 3 m wide (4 m is recommended), 4 m long and 3 m high outside, padding at least 2 cm thick around the openings, and light poles kept out of that area. Your ticks are saved on this device.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you play a ball outside the court?</h2></div><div class="grid">
<div class="card"><h3>1. Read it early</h3><p>A hard smash or a fast ball off the side glass near the net is the one that goes out. When you see it coming, start moving to the door.</p></div>
<div class="card"><h3>2. Go through the nearest door</h3><p>Use the opening on the side where the ball is going. Call to your partner so they know you are going out.</p></div>
<div class="card"><h3>3. Hit it before the second bounce</h3><p>Let it drop, then hit it before it lands again outside. A high lob back over the wall gives you time to run back in.</p></div>
<div class="card"><h3>4. Partner covers the court</h3><p>While you are out, your partner holds the middle. Get back in as fast as you can: the other team will aim for the empty side.</p></div>
</div>
<p class="muted" style="margin-top:14px">Stay safe: only run out where the area is clear, and watch for people walking by. If the space isn't there, let the ball go.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When is a point replayed in padel?</h2></div><div class="grid">
<div class="card"><span class="pill i">Let</span><h3 style="margin-top:10px">Something comes onto the court</h3><p>A ball from the next court or any other object comes onto your court during the point (FIP 10.1).</p></div>
<div class="card"><span class="pill i">Let</span><h3 style="margin-top:10px">The ball breaks</h3><p>The ball splits during the point, or play is stopped by something unexpected that has nothing to do with the players (FIP 10.1).</p></div>
<div class="card"><span class="pill i">Let</span><h3 style="margin-top:10px">Someone puts you off by accident</h3><p>A player disturbs an opponent's shot without meaning to. Done on purpose, it loses the point (FIP 11).</p></div>
<div class="card"><span class="pill a">Call it fast</span><h3 style="margin-top:10px">Stop play straight away</h3><p>Ask for the let at once. If you keep playing, you lose the right to it (FIP 10.1).</p></div>
</div>
<p class="muted" style="margin-top:14px">Net cords on the serve are covered on the <a href="{href("serve-rules.html")}">serve rules page</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Other ball calls</h3><p>Glass, fence, ceiling and stuck balls: use the <a href="{href("wall-rules.html")}">wall and fence checker</a>.</p></div>
<div class="card"><h3>At the net</h3><p>Touching the net and reaching over: try the <a href="{href("net-rules.html")}">net rules checker</a>.</p></div>
<div class="card"><h3>The court itself</h3><p>Every size and line, in metres and feet, on the <a href="{href("court-dimensions.html")}">court dimensions diagram</a>.</p></div>
</div></div></section>'''
ocp_faq = [
    ("Can you play outside the court in padel?", "Yes, but only on courts built for it, with door openings and a clear area outside, and when the club allows it. If the ball bounces in your court and goes out, you may run out and hit it back before its second bounce."),
    ("What happens if the ball goes out of the court in padel?", "If it bounced in your court first, it was a good shot by the other team. Where out-of-court play is allowed you may chase it. Where it isn't, the other team wins the point."),
    ("How much space do you need for out-of-court play?", "The FIP rules ask for two openings per side and a clear area outside of at least 3 m wide (4 m recommended), 4 m long and 3 m high, with nothing standing in it."),
    ("Does the return have to come back over the wall?", "The FIP rules don't say so. A return from outside counts if it crosses the net and bounces in the other team's court before touching their walls or fence. It can come back over the wall or in through the door."),
    ("Can the other team volley a ball hit from outside the court?", "Yes. There is no special rule for these returns, so the other team may volley it like any other ball."),
    ("What is salida de pista in padel?", "Salida de pista is Spanish for leaving the court. It means running out of the court through the door to play a ball that has bounced and gone out, on courts where this is allowed."),
    ("Is it a let if a ball from another court rolls onto ours?", "Yes. If an object such as another ball comes onto your court during the point, it's a let and you replay the point. Call it straight away, or you lose the right to the let."),
]
page("out-of-court-play.html", "Padel Out-of-Court Play Rules: When Can You Leave the Court?",
     "Padel out-of-court play (salida de pista) explained: when you can run out to play the ball, door and serve calls, lets, plus a free FIP call checker.",
     ocp + f'<script>window.OC={json.dumps(OC)};</script>', ocp_faq, "Out-of-court play")

# ---------------- PADEL INJURIES ----------------
# Sources: Dahmen et al. 2023, "Incidence, prevalence and nature of injuries in padel: a systematic review" (BMJ Open Sport & Exercise Medicine 9:e001607);
# NHS "Tennis elbow"; NI Direct "Sports injuries". General information in our own words, not medical advice. See CONTENT-LOG.
# Each zone: id, label, svg x, svg y, how it shows up in padel studies, padel moves that load it, habits that help, red flags.
INJ = [
    ("elbow", "Elbow (outside)", 156, 108,
     "The most often reported injury area in padel studies. Pain on the outer elbow is often called tennis elbow or padel elbow (lateral epicondylitis).",
     "Lots of gripping and wrist movement on every shot: volleys, bandejas and backhands off the glass.",
     ["Don't squeeze the handle: hold it firmly but relaxed, and change a slippery overgrip.", "Build up your playing hours slowly after a break.", "Get a coach to check your technique, especially volleys and the bandeja.", "Rest when it hurts: playing through it can slow recovery."],
     "Pain on the outside of the elbow that is worse when you grip, lift or turn your wrist. Tenderness, or trouble straightening the arm."),
    ("shoulder", "Shoulder", 132, 64,
     "Reported often in padel studies, after the elbow and the knee.",
     "Overheads: bandejas, víboras and smashes, plus reaching for high balls off the glass.",
     ["Warm up your shoulders with arm circles and easy overheads before any full smash.", "Build up overhead pace slowly in the warm-up.", "Mix bandejas with lobs and volleys in practice, not 50 smashes in a row."],
     "Pain lifting the arm above your head, or a shoulder that feels weak or unstable."),
    ("wrist", "Wrist and hand", 166, 148,
     "Reported less often than the elbow, but common in studies that looked only at the upper body.",
     "Flicked shots like the víbora and chiquita, blocked volleys, and catching the ball late.",
     ["Keep the wrist cord on and the grip dry.", "Hit through the ball with your arm and body, not just a flick of the wrist.", "Ease back in after a break."],
     "Swelling, pain on gripping, or numbness or tingling in the fingers."),
    ("back", "Lower back", 110, 126,
     "One of the four most reported areas in padel studies, with the elbow, knee and shoulder.",
     "Twisting to play balls off the glass, bending low for chiquitas, and reaching back for overheads.",
     ["Use your legs: bend your knees for low balls instead of bending your back.", "Turn your hips and shoulders together on glass shots.", "Include hip and trunk moves in your warm-up."],
     "Back pain with numbness, tingling or weakness in the legs needs a doctor quickly."),
    ("knee", "Knee", 126, 204,
     "The second most reported area in padel studies. Knee sprains show up among the common injuries.",
     "Quick stops, lunges to the side glass and turning on a planted foot.",
     ["Wear padel or court shoes with the right sole: running shoes grip badly and slide.", "Split step and take small steps, so you don't lunge on one leg.", "Squats and lunges in the warm-up."],
     "A pop at the moment of injury, quick swelling, or the knee giving way."),
    ("calf", "Calf", 130, 236,
     "Calf strains appear among the common padel injuries in the studies.",
     "Sudden sprints forward to drop shots and pushing off from the back of the court.",
     ["Warm up properly: a jog, then short sprints.", "Take extra time to warm up when it's cold.", "Stop at the first sharp pain instead of playing on."],
     "Sudden sharp pain in the back of the lower leg, or you can't stand on your toes."),
    ("ankle", "Ankle and foot", 133, 268,
     "Ankle sprains and foot pain are reported in padel studies, but less often than the elbow.",
     "Changes of direction, landing on a ball on the turf, and worn or wrong shoes.",
     ["Shoes with grip for your court surface. Replace worn soles.", "Clear loose balls off your side of the court between points.", "Footwork in your warm-up: side steps and quick feet."],
     "You can't put weight on it, it looks out of shape, or there is a lot of swelling."),
]
INJ_HABITS = [
    ("wu", "I warm up for 10 to 15 minutes before I play", "warm-up.html", "warm-up timer"),
    ("build", "After a break, I build my playing time back up slowly", "", ""),
    ("shoes", "I wear padel or court shoes, not running shoes", "padel-shoes.html", "shoe finder"),
    ("grip", "My overgrip is fresh and I don't squeeze the handle", "racket-care.html", "racket care guide"),
    ("rack", "My racket weight suits me (not too heavy for my arm)", "racket-balance.html", "weight and balance decoder"),
    ("coach", "I've had a lesson or coaching on my technique", "", ""),
    ("rest", "I take rest days between hard sessions", "", ""),
    ("stop", "I stop when I feel pain instead of playing through it", "", ""),
    ("cool", "I cool down and stretch gently after playing", "", ""),
]
def _inj_fig():
    dots = "".join(f'<g class="inj-dot" data-z="{z}"><circle cx="{x}" cy="{y}" r="15" fill="#e8f84a" opacity=".18"/><circle cx="{x}" cy="{y}" r="6" fill="#e8f84a" stroke="#0b1530" stroke-width="1.5"/></g>' for z, _, x, y, *_ in INJ)
    return f'''<svg viewBox="0 0 220 300" class="wr-court inj-fig" role="img" aria-label="Simple drawing of a padel player. The dots show the body areas you can choose.">
<rect width="220" height="300" rx="14" fill="#0e2468"/>
<g fill="#1e46c8" stroke="#9cc4ea" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">
<circle cx="110" cy="30" r="16"/>
<path d="M88 56 Q110 50 132 56 L130 140 Q110 146 90 140 Z"/>
<path d="M132 64 L156 108 L166 148" fill="none" stroke-width="12"/>
<path d="M88 64 L70 108 L64 148" fill="none" stroke-width="12"/>
<path d="M100 140 L96 204 L90 268" fill="none" stroke-width="14" opacity=".85"/>
<path d="M120 140 L126 204 L133 268" fill="none" stroke-width="14"/>
</g>
<g transform="rotate(-25 172 162)" opacity=".9"><rect x="168" y="152" width="8" height="26" rx="4" fill="#e8f84a"/><ellipse cx="172" cy="200" rx="16" ry="22" fill="#e8f84a"/></g>
{dots}
</svg>'''
inj = f'''<header class="hero"><div class="wrap"><h1>Padel injuries: where it hurts and how to prevent it</h1>
<p class="lead">Tap the part of the body that worries you to see how often it shows up in padel, which moves load it and the habits that help. Then run the two-minute prevention check.</p>
{quick("The elbow is the most often reported padel injury, followed by the knee, shoulder and lower back, and most padel injuries are tendon or muscle problems, not broken bones. The habits that help most: a 10 to 15 minute warm-up, building up playing time slowly, court shoes, a relaxed grip, coaching on technique and stopping when something hurts. This page is general information, not medical advice.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="inj">
<div>
<div class="q"><h3>Where does it hurt, or what do you want to protect?</h3><div class="opts" id="inj-zones">{"".join(f'<button class="opt" type="button" data-z="{z}" aria-pressed="false">{t}</button>' for z, t, *_ in INJ)}</div></div>
<p class="muted">You can also tap a dot on the drawing. Your choice is only kept in this browser.</p>
</div>
<aside class="result" id="inj-out" aria-live="polite"><div class="wr-svg">{_inj_fig()}</div><div id="inj-txt"><h2>Pick an area</h2><p>Choose a body area to see what padel studies report and what helps.</p></div></aside>
</div></div></section>
<script>window.INJ={json.dumps({z: {"t": t, "s": s, "m": m, "h": h, "r": r} for z, t, _, _, s, m, h, r in INJ}, ensure_ascii=False)};</script>
{AD.format("inj-mid")}
<section><div class="wrap"><div class="sh"><h2>How common are padel injuries?</h2></div><div class="grid">
<div class="card"><h3>About 3 per 1,000 hours</h3><p>A 2023 review of 8 studies with 2,022 padel players (BMJ Open Sport &amp; Exercise Medicine) found about 3 injuries per 1,000 hours of training and about 8 per 1,000 matches.</p></div>
<div class="card"><h3>Most players get one</h3><p>Between 40% and 95% of the players in those studies said they had been injured at some point. Most of the studies asked players to remember, so treat these as rough numbers.</p></div>
<div class="card"><h3>Tendons and muscles</h3><p>Most reported injuries were to tendons (like tennis elbow) or muscles (like calf strains), not bones. These are often overuse injuries that build up over time.</p></div>
</div>
<div class="card" style="padding:8px 24px;overflow-x:auto;margin-top:18px"><table class="mt mt-plain"><thead><tr><th scope="col">Rank</th><th scope="col">Body area</th><th scope="col">Typical problem</th></tr></thead><tbody>
<tr><td>1</td><td>Elbow</td><td>Tennis elbow (pain on the outer elbow)</td></tr>
<tr><td>2</td><td>Knee</td><td>Sprains and pain from twisting</td></tr>
<tr><td>3</td><td>Shoulder</td><td>Pain from overheads</td></tr>
<tr><td>4</td><td>Lower back</td><td>Back pain from twisting and bending</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Order from the 2023 review. Most players in the studies were adult club players in Spain, and study quality was low to moderate, so the review's authors call the evidence limited.</p></div></section>
<section style="padding-top:0" id="check"><div class="wrap"><div class="sh"><h2>Injury prevention check: how well do you protect yourself?</h2></div>
<div class="quiz" id="injc">
<div><div class="q"><h3>Tick every habit you already have</h3>
<ul class="check" id="injc-list">{"".join(f'<li><label><input type="checkbox" data-h="{k}"><span>{t}</span></label></li>' for k, t, _, _ in INJ_HABITS)}</ul></div>
<button class="btn sm" type="button" id="injc-reset">Start again</button></div>
<aside class="result" id="injc-out" aria-live="polite"><h2>Your habits</h2><p>Tick what you already do. Your score and the habits to add appear here.</p></aside>
</div>
<script>window.INJH={json.dumps({k: [t, href(f) if f else "", n] for k, t, f, n in INJ_HABITS}, ensure_ascii=False)};</script>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What is padel elbow, and what can you do about it?</h2></div><div class="grid">
<div class="card"><h3>What it feels like</h3><p>Pain on the outside of the elbow. It can be mild or constant, and it gets worse when you grip, lift or turn your wrist. The NHS lists tenderness and trouble fully straightening the arm as other signs.</p></div>
<div class="card"><h3>Why it happens</h3><p>The NHS describes tennis elbow as a problem with the tendons of the forearm after lots of gripping and twisting. In padel you grip and use your wrist on almost every shot.</p></div>
<div class="card"><h3>Looking after it at home</h3><p>NHS advice: rest from what makes it worse, use painkillers such as paracetamol or an anti-inflammatory gel, and use a hot or cold pack wrapped in a towel for up to 20 minutes every 2 to 3 hours. A forearm strap or brace from a pharmacy may help.</p></div>
<div class="card"><h3>When to see a GP</h3><p>If the pain has not got better after 2 weeks of rest and self-care. A GP may suggest physiotherapy if home treatment has not helped after about 6 weeks.</p></div>
<div class="card"><h3>How long it lasts</h3><p>It often gets better within a few weeks of rest, but the NHS says it can last more than a year. Coming back too fast is a common reason it returns.</p></div>
<div class="card"><h3>Does the racket matter?</h3><p>Many coaches and shops suggest a lighter, less head-heavy racket and a thicker, fresh grip for sore elbows. This makes sense but has not been proven in studies. Compare specs with the <a href="{href("racket-balance.html")}">weight and balance decoder</a>, or run the <a href="{href("padel-elbow.html")}">padel elbow arm-load check</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you prevent padel injuries?</h2></div><div class="grid">
<div class="card"><h3>1. Warm up every time</h3><p>A short jog, moving stretches, leg exercises and easy rallies. Not warming up properly is one of the common causes of sports injuries listed by NI Direct. Use the <a href="{href("warm-up.html")}">warm-up timer</a>.</p></div>
<div class="card"><h3>2. Build up slowly</h3><p>Don't go from one game a week to five. Pushing your body past your current fitness is another common cause of sports injuries.</p></div>
<div class="card"><h3>3. The right shoes</h3><p>Padel or court shoes with a sole that suits your court. Running shoes are made for straight lines, not side steps. See the <a href="{href("padel-shoes.html")}">padel shoes guide</a>.</p></div>
<div class="card"><h3>4. Learn the technique</h3><p>Coaching on the bandeja, volleys and glass shots takes load off your elbow, shoulder and back. Plan practice with the <a href="{href("drills.html")}">drills planner</a>.</p></div>
<div class="card"><h3>5. Fresh balls and grip</h3><p>Flat balls need more effort to hit and a slippery grip makes you squeeze. Check with the <a href="{href("padel-balls.html")}">dead ball checker</a>.</p></div>
<div class="card"><h3>6. Stop when it hurts</h3><p>Playing on with pain can cause more damage and slow your recovery. Rest, and get advice if it doesn't settle.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When should you get medical help?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">What you notice</th><th scope="col">What to do</th></tr></thead><tbody>
<tr><td>You think a bone is broken, a joint looks out of place, or someone hit their head hard</td><td>Go to an emergency department straight away</td></tr>
<tr><td>Pain that has not improved after 2 weeks of rest and self-care</td><td>See a GP or doctor</td></tr>
<tr><td>Pain that comes back every time you play</td><td>See a GP or physiotherapist before it gets worse</td></tr>
<tr><td>A minor strain or knock</td><td>Stop playing, rest it, and ease back in when it feels normal</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Based on NHS and NI Direct advice for UK readers. Outside the UK, follow your local health service. This page is general information and does not replace advice from a doctor or physiotherapist.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Warm up properly</h3><p>Follow the 10 or 15 minute <a href="{href("warm-up.html")}">warm-up timer</a> before your next game.</p></div>
<div class="card"><h3>Check your racket</h3><p>Too heavy for your arm? Try the <a href="{href("padel-racket-weight.html")}">racket weight calculator</a> or the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
<div class="card"><h3>Cool down after</h3><p>Held stretches for legs, hips, back, shoulder and forearm: the <a href="{href("padel-cool-down.html")}">cool-down stretch timer</a>.</p></div>
<div class="card"><h3>Know your load</h3><p>See how hard your games really are with the <a href="{href("padel-calories.html")}">padel calories calculator</a>.</p></div>
<div class="card"><h3>Build strength</h3><p>Legs, core, shoulder and forearm, at home or in the gym: the <a href="{href("padel-workout.html")}">padel workout builder</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Kit that takes the strain off</h3><p>Shoes with grip for your court and a fresh overgrip are the cheapest ways to look after your body. If your racket feels heavy on your arm, browse round rackets, which often have a lower balance.</p><ul class="aff-links"><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
inj_faq = [
    ("What is the most common injury in padel?", "The elbow. In a 2023 review of padel studies, the elbow was the most often reported injury area, mostly tennis elbow (pain on the outer elbow), followed by the knee, shoulder and lower back."),
    ("What is padel elbow?", "Padel elbow is the name players use for tennis elbow (lateral epicondylitis): pain on the outside of the elbow from the forearm tendons, made worse by gripping and turning the wrist."),
    ("Can I keep playing padel with tennis elbow?", "It is better to rest from what makes it worse. The NHS advises rest, painkillers or gel and a hot or cold pack, and seeing a GP if it hasn't improved after 2 weeks. Playing through pain can slow recovery."),
    ("How long does padel elbow take to heal?", "It often improves within a few weeks of rest, but the NHS says tennis elbow can last more than a year. Build back up slowly when it feels better."),
    ("Is padel bad for your knees?", "Not by itself, but quick stops and turns load the knee, and knee injuries are the second most reported in padel studies. Court shoes, a proper warm-up and good footwork help."),
    ("How can I prevent padel injuries?", "Warm up for 10 to 15 minutes, build up playing time slowly, wear court shoes, keep a fresh grip and relaxed hold, get coaching on technique, take rest days and stop when you feel pain."),
    ("Is padel more dangerous than tennis?", "There is not enough research to say. The 2023 review found about 3 injuries per 1,000 hours of padel training, but its authors say comparisons with other racket sports should be made carefully."),
]
page("padel-injuries.html", "Padel Injuries: Elbow, Knee, Back and How to Prevent Them",
     "The most common padel injuries, from padel elbow to knee, shoulder and back pain: tap a body area to see what helps, then run a free injury prevention check.",
     inj, inj_faq, "Padel injuries")

# ---------------- PADEL GRIP: HOW TO HOLD A PADEL RACKET ----------------
# Sources: The Padel School "Find your padel grip" (continental base grip; change grip only at the back; use the free hand to reset),
# Padel Browser "Padel grip guide" (continental for most shots incl. volley, serve, bandeja, víbora, smash; handshake/hammer; V on top edge;
# eastern variants one bevel round for some back-court shots; too tight = forearm fatigue; tennis forehand grip mistake; wrist strap),
# Padelshop "How to hold a padel racket" (hammer, not too tight), Padel Browser grip size guide (finger-gap test, small handle -> squeeze harder,
# overgrip adds thickness), HEAD "How to place an overgrip" (overlap changes thickness, worn grip -> squeeze harder, replace at least every 2 months),
# TotalPadel "How to overgrip a padel racket" (wrap from butt cap upwards, parallel turns, 2-3 sessions for club players). Own wording.
# shot id, name, grip key, note
GRIP_SHOTS = [
    ("serve", "Serve", "c", "Use the continental grip. It lets you hit the underhand serve with a little slice and control."),
    ("ret", "Return of serve", "c", "Stay in the continental grip. The ball comes quickly and there is no time to change."),
    ("vol", "Volley (forehand or backhand)", "c", "Always continental at the net. The same grip works on both sides, so you never have to change it in a fast exchange."),
    ("band", "Bandeja", "c", "Continental. The racket face stays a little open to put slice on the ball and keep it deep."),
    ("vib", "Víbora", "c", "Continental. The grip lets the wrist and forearm add side spin as you hit across the ball."),
    ("smash", "Smash", "c", "Continental for most smashes. Keep your hand relaxed until just before contact."),
    ("glass", "Ball off the back glass", "c", "Continental. Ball after ball comes off the glass at different heights, and one grip makes every one easier."),
    ("chiq", "Chiquita and lob", "c", "Continental. Both are touch shots that need an open, steady racket face."),
    ("fh", "Forehand drive from the back", "e", "Continental is fine. Some coaches let improving players turn the hand one bevel towards the eastern forehand grip for a stronger drive from the back of the court, but only there, never at the net."),
    ("bh", "High backhand from the back", "eb", "Continental is fine. Some coaches use an eastern backhand grip (one bevel the other way) for attacking high backhands from the back. Learn the continental first."),
]
GRIP_JSON = json.dumps({s: [n, g, t] for s, n, g, t in GRIP_SHOTS}, ensure_ascii=False)
GC_ITEMS = [
    ("tight", "My forearm or hand is tired or sore after playing"),
    ("white", "I squeeze the handle hard all through the rally"),
    ("switch", "I change grip for every forehand and backhand volley"),
    ("tennis", "I hold it like a tennis forehand, with the palm under the handle"),
    ("reset", "My grip has slowly turned by the end of a long rally"),
    ("slip", "The handle feels slippery or wet"),
    ("thin", "My fingers dig into my palm and there is no gap at all"),
    ("thick", "There is a big gap between my fingers and my palm"),
    ("strap", "I don't always wear the wrist strap"),
]
GC_FIX = {
    "tight": "Relax your hold. Keep a loose hand between shots and squeeze a little more only as you hit. A tight grip tires the forearm and is linked to elbow trouble.",
    "white": "Relax your hold. Keep a loose hand between shots and squeeze a little more only as you hit. A tight grip tires the forearm and is linked to elbow trouble.",
    "switch": "Stay in the continental grip at the net. It works for forehand and backhand volleys, so you never need to change.",
    "tennis": "Move to the continental grip: a handshake on the handle with the frame edge pointing up and down. A tennis forehand grip makes volleys and balls off the glass harder.",
    "reset": "Use your free hand on the throat of the racket between shots to set the grip back to continental.",
    "slip": "Fit a new overgrip. A slippery handle makes you squeeze harder without noticing.",
    "thin": "Your handle may be too thin. Add an overgrip, or wrap the one you have with more overlap.",
    "thick": "Your handle may be too thick. Wrap the overgrip with less overlap, or take off an extra layer.",
    "strap": "Always wear the wrist strap. It stops the racket flying if it slips, and dropping it during a point loses the point.",
}
GC_JSON = json.dumps(GC_FIX, ensure_ascii=False)
HANDLE_SVG = '''<svg id="gp-svg" viewBox="0 0 220 220" role="img" aria-label="Handle seen from the bottom, with eight numbered bevels and a marker for where the V of your hand sits">
<polygon points="78,20 142,20 188,66 188,154 142,200 78,200 32,154 32,66" fill="#1e46c8" stroke="#e4eef6" stroke-width="3"/>
<polygon points="92,52 128,52 156,80 156,140 128,168 92,168 64,140 64,80" fill="#132e80" stroke="rgba(255,255,255,.25)" stroke-width="1.5"/>
<rect x="104" y="58" width="12" height="104" rx="4" fill="#9cc4ea" opacity=".55"/>
<g font-family="Onest, sans-serif" font-size="15" font-weight="700" fill="#e4eef6" text-anchor="middle">
<text x="110" y="42" id="gb1">1</text><text x="160" y="58" id="gb2">2</text><text x="176" y="115">3</text><text x="160" y="172">4</text>
<text x="110" y="190">5</text><text x="60" y="172">6</text><text x="44" y="115">7</text><text x="60" y="58" id="gb8">8</text></g>
<g id="gp-mark" transform="translate(110 110) translate(0 -97)"><path d="M0 10 L-11 -10 L11 -10 Z" fill="#e8f84a" stroke="#0b1530" stroke-width="2"/></g>
</svg>'''
grip = f'''<header class="hero"><div class="wrap"><h1>How to hold a padel racket.</h1>
<p class="lead">One grip does almost everything in padel. Find it with the steps below, tap a shot to see which grip it uses, and run the grip check to fix what is making your hand tired or the ball fly.</p>
{quick("Use the continental grip for almost every padel shot. Hold the racket with the frame edge pointing up and down and shake hands with the handle, as if holding a hammer: the V between your thumb and first finger sits on the top edge. Keep your hand relaxed between shots, wear the wrist strap, and use the same grip for forehands, backhands, volleys and overheads.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="gp">
<div class="card">
<div class="q"><h3>Which hand do you play with?</h3><div class="seg" id="gp-hand" role="group" aria-label="Playing hand" style="background:#dfe8f7"><button type="button" data-v="r" aria-pressed="true">Right hand</button><button type="button" data-v="l" aria-pressed="false">Left hand</button></div></div>
<div class="q"><h3>Pick a shot</h3><div class="opts" id="gp-shots" role="group" aria-label="Shot">{"".join(f'<button class="opt" type="button" data-v="{s}" aria-pressed="{"true" if s == "vol" else "false"}">{e(n)}</button>' for s, n, g, t in GRIP_SHOTS)}</div></div>
<p class="muted" style="margin:0;font-size:.92rem">The drawing shows the handle from the bottom, with the racket frame standing straight up. Your choice is saved on this device.</p>
</div>
<aside class="result" id="gp-out" aria-live="polite"><h2 id="gp-h">Continental grip</h2><div class="gp-art">{HANDLE_SVG}</div><p id="gp-p"></p><p class="wr-src" id="gp-src"></p></aside>
</div></div></section>
<script>window.GRIPS={GRIP_JSON};window.GCFIX={GC_JSON};</script>
{AD.format("grip-mid")}
<section><div class="wrap"><div class="sh"><h2>How do you find the continental grip?</h2></div><div class="grid">
<div class="card"><span class="pill b">Step 1</span><h3 style="margin-top:10px">Stand the racket on its edge</h3><p>Hold the racket by the throat with your free hand, so the frame points straight up and down and the faces point left and right.</p></div>
<div class="card"><span class="pill b">Step 2</span><h3 style="margin-top:10px">Shake hands with it</h3><p>Put your playing hand on the handle as if you were shaking someone's hand, or holding a hammer to knock in a nail.</p></div>
<div class="card"><span class="pill b">Step 3</span><h3 style="margin-top:10px">Check the V</h3><p>Look down at your hand. The V shape between your thumb and first finger should sit on the top edge of the handle (bevel 1 in the drawing).</p></div>
<div class="card"><span class="pill b">Step 4</span><h3 style="margin-top:10px">Leave a small gap</h3><p>Wrap your fingers round. Spread them a little and keep a small gap between your palm and the handle. Don't press your palm flat on it.</p></div>
<div class="card"><span class="pill i">Step 5</span><h3 style="margin-top:10px">Strap on first</h3><p>Put the wrist strap on before you take your grip. Every padel racket has one, and many clubs ask you to wear it.</p></div>
<div class="card"><span class="pill i">Step 6</span><h3 style="margin-top:10px">Reset between shots</h3><p>After each shot, let your free hand touch the throat of the racket and turn the grip back to continental if it has moved.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is your grip holding you back? Run the grip check</h2></div>
<div class="quiz" id="gc"><div><div class="q"><h3>Tick anything that is true for you</h3>
<ul class="check" id="gc-list">{"".join(f'<li><label><input type="checkbox" data-g="{c}"><span>{e(t)}</span></label></li>' for c, t in GC_ITEMS)}</ul></div>
<button class="btn sm" type="button" id="gc-reset">Start again</button></div>
<aside class="result" id="gc-out" aria-live="polite"><h2>Your grip check</h2><p>Tick what you notice and your fixes appear here.</p></aside>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which grip for which padel shot?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Shot</th><th scope="col">Grip</th><th scope="col">Why</th></tr></thead><tbody>
<tr><td>Serve and return</td><td>Continental</td><td>Control and a little slice</td></tr>
<tr><td>Volleys, both sides</td><td>Continental</td><td>No time to change grip at the net</td></tr>
<tr><td>Bandeja, víbora, smash</td><td>Continental</td><td>Lets you slice and spin overheads</td></tr>
<tr><td>Balls off the glass, lobs, chiquitas</td><td>Continental</td><td>Steady, open racket face</td></tr>
<tr><td>Forehand drive from the back</td><td>Continental (some coaches: eastern forehand)</td><td>Only at the back, once the basics are solid</td></tr>
<tr><td>Attacking high backhand from the back</td><td>Continental (some coaches: eastern backhand)</td><td>Only at the back, once the basics are solid</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Coaches agree the continental grip is the base. The eastern options are extras for improving players and are never used at the net. If you are in your first months of padel, keep one grip for everything.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How tight should you hold a padel racket?</h2></div><div class="grid">
<div class="card"><h3>Relaxed between shots</h3><p>Hold the racket loosely while you wait and move. A loose hand reacts faster at the net.</p></div>
<div class="card"><h3>A little firmer at contact</h3><p>Squeeze a bit more just as you hit, then relax again straight after. Don't hold at full strength all the time.</p></div>
<div class="card"><h3>Why it matters</h3><p>Gripping hard all the time locks your wrist, tires the forearm and is linked to elbow pain. See <a href="{href("padel-injuries.html")}">padel injuries</a> for more on padel elbow.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is my padel grip too small or too big?</h2></div><div class="grid">
<div class="card"><h3>The finger test</h3><p>Take the continental grip. There should be a small gap between your fingertips and the base of your thumb, about the width of one finger of your other hand. No gap means the handle is thin; a big gap means it is thick.</p></div>
<div class="card"><h3>Too small</h3><p>If the handle is too thin, you tend to squeeze harder as the match goes on. Add an overgrip, or wrap with more overlap.</p></div>
<div class="card"><h3>Too big</h3><p>A handle that is too thick is hard to turn and hold relaxed. Wrap the overgrip with less overlap, or remove an extra layer.</p></div>
<div class="card"><h3>Overgrips change the size</h3><p>Many padel rackets come in one handle size, so players change the feel with overgrips. Each extra layer, or more overlap as you wrap, makes the handle a little thicker.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you put on an overgrip?</h2><p class="muted">How often to change it: use the <a href="{href("padel-overgrip.html")}">overgrip change calculator</a>.</p></div>
<div class="card"><ol class="gp-steps">
<li>Pull off the old overgrip and its finishing tape.</li>
<li>Put the wrist strap on its holder so it doesn't get in the way.</li>
<li>Start at the bottom of the handle, by the butt cap. Peel the backing and stick the thin end there.</li>
<li>Turn the racket slowly and wrap up the handle, keeping each turn parallel and overlapping the last one by the same amount.</li>
<li>Stop at the top of the handle. Cut the end straight across and fix it with the finishing tape.</li>
</ol>
<p class="muted" style="margin:10px 0 0">How often to change it: brand guides range from every two or three sessions for club players to at least every two months. Change it sooner if it looks dirty, changes colour or stops feeling sticky. More on this in <a href="{href("racket-care.html")}">racket care</a>.</p></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What grip mistakes do new players make?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Mistake</th><th scope="col">What happens</th><th scope="col">Fix</th></tr></thead><tbody>
<tr><td>Tennis forehand grip</td><td>Volleys and balls off the glass get awkward</td><td>Continental for everything</td></tr>
<tr><td>Squeezing all the time</td><td>Tired forearm, stiff wrist, sore elbow</td><td>Loose hand, firmer only at contact</td></tr>
<tr><td>Changing grip at the net</td><td>Late on fast volleys</td><td>One grip at the net</td></tr>
<tr><td>Never resetting</td><td>Grip slowly turns during a rally</td><td>Free hand on the throat after each shot</td></tr>
<tr><td>Worn or slippery overgrip</td><td>You squeeze harder without noticing</td><td>New overgrip</td></tr>
<tr><td>No wrist strap</td><td>Racket can fly, and dropping it loses the point</td><td>Strap on before you grip</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Use the grip on court</h3><p>See the bandeja, víbora and chiquita drawn out in the <a href="{href("shots.html")}">shot library</a>, and pick the right overhead with the <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora chooser</a>.</p></div>
<div class="card"><h3>Practise it</h3><p>Tap-ups and wall volleys build a relaxed grip. Plan a session with the <a href="{href("drills.html")}">drills planner</a>.</p></div>
<div class="card"><h3>Check your racket</h3><p>Heavy or head-heavy rackets make you squeeze more. Try the <a href="{href("racket-finder.html")}">racket finder</a> or the <a href="{href("racket-balance.html")}">balance decoder</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Grip kit</h3><p>A fresh overgrip is the cheapest way to make any racket feel better in your hand. Keep a few spare in your bag.</p><ul class="aff-links"><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Padel bags</a></li></ul>{AFF_NOTE}</div></div></section>'''
grip_faq = [
    ("What grip do you use in padel?", "The continental grip. It is the base grip for almost every shot: serve, return, volleys on both sides, bandeja, víbora, smash and balls off the glass."),
    ("How do you find the continental grip in padel?", "Stand the racket on its edge and shake hands with the handle, like holding a hammer. The V between your thumb and first finger sits on the top edge of the handle."),
    ("Do you change grip in padel?", "Mostly no. Beginners should use the continental grip for everything. Some coaches let improving players turn the hand one bevel for some forehands or high backhands from the back of the court, but never at the net."),
    ("How tight should I hold my padel racket?", "Loosely between shots and a little firmer just as you hit. Squeezing hard all the time tires your forearm and is linked to elbow pain."),
    ("How do I know if my padel grip is too small?", "Take the continental grip. If your fingertips dig into your palm with no gap, or you find yourself squeezing harder as you play, the handle is probably too thin. Add an overgrip or overlap it more."),
    ("Is the padel grip the same as in tennis?", "The continental grip is the same one tennis players use to serve and volley. Many tennis players use a different grip for forehands, but in padel the continental is used for nearly everything."),
    ("Is the grip different for left-handed players?", "It is the same continental grip, just mirrored. If a coach tells you to turn one bevel for a forehand, a left-hander turns the other way."),
]
page("padel-grip.html", "How to Hold a Padel Racket: Continental Grip Guide",
     "How to hold a padel racket: find the continental grip in 6 steps, see the grip for every shot, check your grip size and fix common new-player grip mistakes.",
     grip, grip_faq, "Padel grip")

# ---------------- OVERHEADS: BANDEJA vs VIBORA vs SMASH ----------------
OH_SHOTS = {
    "smash": {"h": "Flat smash", "what": "An easy, high ball close to the net is the one time to hit an overhead hard.",
              "how": ["Turn sideways and point your free hand at the ball.", "Hit it in front of you with your arm fully stretched, like a tennis serve.", "Aim down into the space between the two players or at their feet. Placement first, then pace."],
              "aim": "Down into the gap or at their feet", "after": "Stay at the net. If they get it back, it will usually be a weak ball."},
    "vibora": {"h": "Víbora", "what": "The attacking version of the bandeja. You are close enough and balanced enough to hurt them, but the ball is not easy enough to smash.",
               "how": ["Take the ball a little later and lower than a bandeja, as it starts to drop.", "Swing more firmly and add side spin, brushing round the side of the ball.", "Aim at the side glass or the corner, so the ball kicks sideways and stays low."],
               "aim": "Side glass or the corner", "after": "Move back to the net with your partner. A víbora that is too short or too hard out of position gives them the attack."},
    "bandeja": {"h": "Bandeja", "what": "The safe overhead that keeps your team at the net. It is about control and depth, not winning the point.",
                "how": ["Turn sideways with the racket up beside your head, like carrying a tray.", "Meet the ball at about eye height and swing forwards and across your body, not straight down. This puts slice on it.", "Keep the pace low and send it deep, past their service line, so it bounces low off their back glass."],
                "aim": "Deep, past their service line", "after": "Use the swing to walk forward and get level with your partner at the net again."},
    "glass": {"h": "Let it go to the glass", "what": "The ball will go over you, or you can't get behind it. Running backwards for an overhead is how most bad overheads happen.",
              "how": ["Call it early (\"mine\" or \"yours\") and turn to follow the ball to your back glass.", "Let it bounce on the ground, hit the glass and come back to you.", "Lob it back high and deep if they are at the net. If it comes off the glass high and you are a confident player, an attacking shot as it drops (a bajada) is an option."],
              "aim": "High and deep over them, if they are at the net", "after": "If your lob goes deep over them, move up together and take the net back."},
}
OH_JSON = json.dumps(OH_SHOTS, ensure_ascii=False)
def ohq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-oh="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
OHQ = [
    ("pos", "1. Where are you when you hit it?", [("near", "Close to the net"), ("mid", "Around the service line"), ("deep", "Near my back glass")], "mid"),
    ("ball", "2. How is the ball coming?", [("easy", "High and slow, I'm under it"), ("hard", "I'm stretching or moving back"), ("over", "It will go over my head")], "easy"),
    ("opp", "3. Where are your opponents?", [("back", "At the back"), ("net", "At the net or coming in")], "back"),
    ("lvl", "4. How long have you played?", [("new", "Under a year"), ("imp", "A year or more"), ("conf", "I'm confident overhead")], "new"),
]
OH_SVG = '''<svg class="wr-court" id="oh-svg" viewBox="0 0 440 240" role="img" aria-label="Top view of a padel court. Your side is on the left. The dot shows where you are, the yellow area shows where to aim.">
<rect x="20" y="20" width="400" height="200" rx="6" fill="#1e46c8"/>
<rect x="20" y="20" width="400" height="200" rx="6" fill="none" stroke="#9cc4ea" stroke-width="6" opacity=".8"/>
<path d="M81 20v200M359 20v200M81 120h278" stroke="#fff" stroke-width="2" opacity=".85"/>
<path d="M220 14v212" stroke="#e4eef6" stroke-width="5"/>
<rect id="oh-zone" x="370" y="40" width="44" height="160" rx="8" fill="#e8f84a" opacity=".45"/>
<path id="oh-path" d="M90 130 Q250 20 392 120" fill="none" stroke="#e8f84a" stroke-width="2.5" stroke-dasharray="5 5"/>
<circle id="oh-me" cx="90" cy="130" r="9" fill="#e8f84a" stroke="#0b1530" stroke-width="2"/>
<circle id="oh-p" cx="90" cy="70" r="7" fill="#9fd8ff" stroke="#0b1530" stroke-width="1.5"/>
<circle class="oh-op" cx="390" cy="70" r="8" fill="#ff9b78" stroke="#0b1530" stroke-width="1.5"/>
<circle class="oh-op" cx="390" cy="170" r="8" fill="#ff9b78" stroke="#0b1530" stroke-width="1.5"/>
<g font-family="Onest, sans-serif" font-size="12" font-weight="700" fill="#e4eef6"><text x="30" y="236">Your side</text><text x="410" y="236" text-anchor="end">Their side</text></g>
</svg>'''
oh = f'''<header class="hero"><div class="wrap"><h1>Bandeja, víbora or smash: which overhead?</h1>
<p class="lead">A lob is coming. Do you smash it, play a bandeja, try a víbora or let it go to the glass? Answer four quick questions and see the shot, how to hit it and where to aim, drawn on the court.</p>
{quick("Smash only easy, high balls close to the net. Play a bandeja when you are further back or a bit off balance: slow, sliced and deep, so you keep the net. Play a víbora when you are balanced around the service line and want to attack: firmer, with side spin, into the side glass. If the lob will go over you, let it bounce off your back glass and lob back.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="oh">
<div class="card">
{"".join(ohq(*x) for x in OHQ)}
<p class="muted" style="margin:0;font-size:.92rem">General coaching advice, not a rule. Your answers are saved on this device.</p>
</div>
<aside class="result" id="oh-out" aria-live="polite"><div class="wr-svg">{OH_SVG}</div><h2 id="oh-h">Bandeja</h2><p id="oh-p1"></p><ul class="b-why" id="oh-how"></ul><p id="oh-aim"></p><p class="wr-src" id="oh-why"></p></aside>
</div></section>
<script>window.OHS={OH_JSON};</script>
{AD.format("overhead-mid")}
<section><div class="wrap"><div class="sh"><h2>What is the difference between a bandeja and a víbora?</h2></div><div class="grid">
<div class="card"><span class="pill b">Bandeja</span><h3 style="margin-top:10px">Control, to keep the net</h3><p>Bandeja means tray in Spanish. It started as the answer to the lob: a way to stay at the net when a smash is too risky. It is slow, sliced and deep. Coaches call it a defensive shot.</p></div>
<div class="card"><span class="pill a">Víbora</span><h3 style="margin-top:10px">Spin, to attack</h3><p>Víbora means viper. It grew out of the bandeja but is hit harder, with side spin, so the ball skids off the side glass. It can win points, but it is riskier.</p></div>
<div class="card"><span class="pill i">Smash</span><h3 style="margin-top:10px">Power, to finish</h3><p>The smash is close to a tennis serve. It is the shot new players reach for most, but in padel it only pays on easy balls near the net. A hard smash from deep often bounces off the glass into the other pair's hands.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Bandeja vs víbora vs smash at a glance</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Bandeja</th><th scope="col">Víbora</th><th scope="col">Flat smash</th></tr></thead><tbody>
<tr><td>Main job</td><td>Keep the net</td><td>Attack, set up a winner</td><td>Win the point</td></tr>
<tr><td>Where you hit from</td><td>Further back, or off balance</td><td>Around the service line, balanced</td><td>Close to the net</td></tr>
<tr><td>Contact point</td><td>About eye height, beside you</td><td>A little later, as the ball drops</td><td>High and in front, arm stretched</td></tr>
<tr><td>Swing</td><td>Forward and across the body</td><td>Wider and firmer, with wrist</td><td>Up and down, like a serve</td></tr>
<tr><td>Spin</td><td>Slice (backspin)</td><td>Side spin and slice</td><td>Little or none</td></tr>
<tr><td>Pace</td><td>Low</td><td>Medium to high</td><td>High</td></tr>
<tr><td>Aim</td><td>Deep, past their service line</td><td>Side glass or the corner</td><td>Down into the gap or their feet</td></tr>
<tr><td>Risk</td><td>Low</td><td>Medium</td><td>High from deep, low from close</td></tr>
<tr><td>Grip</td><td colspan="3">Continental for all three (see <a href="{href("padel-grip.html")}">how to hold a padel racket</a>)</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Coaching guides describe the spin in slightly different words: some call bandeja spin backspin, others slice or underspin, and some say it can be flat. They all agree it is slower and more controlled than a víbora.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When should you smash in padel?</h2></div><div class="grid">
<div class="card"><h3>Yes: close and easy</h3><p>You are near the net, the ball is high and slow, and you are already under it. Hit down into the space between them.</p></div>
<div class="card"><h3>Careful: from the service line</h3><p>From here a flat smash often bounces off their back glass and comes back as an easy ball. A bandeja or víbora is usually the better pick.</p></div>
<div class="card"><h3>No: deep or moving back</h3><p>If you are near your own back glass, or running backwards, a smash is a guess. Play a bandeja, or let the ball go to the glass.</p></div>
<div class="card"><h3>Smashing out of the court</h3><p>Strong players sometimes smash so the ball bounces out over the side wall (often called por 3) or the back wall. That needs a lot of power and, on courts that allow it, the other pair may run out to play it. Read <a href="{href("out-of-court-play.html")}">out-of-court play rules</a> and <a href="{href("padel-smash.html")}">how to hit an x3 or x4 smash</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What overhead mistakes do new players make?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Mistake</th><th scope="col">What happens</th><th scope="col">Fix</th></tr></thead><tbody>
<tr><td>Smashing every lob</td><td>The ball comes back off the glass and they attack you</td><td>Smash only easy balls near the net</td></tr>
<tr><td>Bandeja hit too hard</td><td>You can't recover to the net in time</td><td>Slow it down, aim deep</td></tr>
<tr><td>Bandeja too short</td><td>It sits up for them to attack</td><td>Land it past their service line</td></tr>
<tr><td>Víbora when off balance</td><td>Errors, or a weak ball they can punish</td><td>Bandeja instead</td></tr>
<tr><td>Running backwards to hit</td><td>Late contact, ball into the net or out</td><td>Turn sideways early, or let it go to the glass</td></tr>
<tr><td>Staying back after the shot</td><td>A gap opens between you and your partner</td><td>Walk forward to the net together</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0" id="how-to-hit-a-bandeja"><div class="wrap"><div class="sh"><h2>How do you hit a bandeja, step by step?</h2><p class="muted">Think of it as half overhead, half forehand volley: controlled, sliced and deep.</p></div>
<div class="grid">
<div class="card"><span class="pill b">Step 1</span><h3 style="margin-top:10px">Turn side-on early</h3><p>The moment you see the lob, turn your body to face the side wall and move back with small side steps. Never run backwards facing the net.</p></div>
<div class="card"><span class="pill b">Step 2</span><h3 style="margin-top:10px">Racket up like a tray</h3><p>Lift the racket above your head with the face open, as if you were carrying a tray or plate. Use the continental grip. Point your free hand at the ball.</p></div>
<div class="card"><span class="pill b">Step 3</span><h3 style="margin-top:10px">Contact at eye height</h3><p>Let the ball drop to about eye height, in front of you and to the side. Higher than that is smash territory; lower and it goes into the net.</p></div>
<div class="card"><span class="pill b">Step 4</span><h3 style="margin-top:10px">Swing high to low, across</h3><p>Brush down and across the back of the ball so it gets slice (backspin). The racket finishes across your body, not straight down by your leg.</p></div>
<div class="card"><span class="pill b">Step 5</span><h3 style="margin-top:10px">Aim deep, not hard</h3><p>Use little power. Land the ball past their service line so it stays low off the back glass. Slow and deep beats fast and short.</p></div>
<div class="card"><span class="pill b">Step 6</span><h3 style="margin-top:10px">Walk back to the net</h3><p>Let the swing carry your weight forward and move back up, level with your partner. Keeping the net is the whole point of the shot.</p></div>
</div>
<div class="quiz" style="margin-top:18px"><div class="card"><h3>Bandeja fault fixer: what goes wrong?</h3><div class="opts" data-bjf="miss" role="group" aria-label="What goes wrong with your bandeja?">
<button type="button" class="opt" data-v="net" aria-pressed="true">Into the net</button><button type="button" class="opt" data-v="long" aria-pressed="false">Too long, too hard</button><button type="button" class="opt" data-v="short" aria-pressed="false">Sits up short</button><button type="button" class="opt" data-v="late" aria-pressed="false">Always late</button><button type="button" class="opt" data-v="stuck" aria-pressed="false">I stay back</button><button type="button" class="opt" data-v="arm" aria-pressed="false">It hurts my arm</button></div>
<p class="muted" style="margin-top:12px">Practise with the "defend the net" game: the pair at the back lobs, the net pair must land every bandeja past the service line. First to 10.</p></div>
<aside class="result" id="bjf" aria-live="polite"><span class="pill b">Fix</span><h2 id="bjf-h" style="margin-top:10px"></h2><p id="bjf-p"></p></aside></div>
<p class="muted" style="margin-top:12px;font-size:.9rem">Technique points in our own words, based on LTA Padel "Overheads: the bandeja and the smash" (checked 27 Nov 2026: side-on turn, racket held like a plate, contact around eye height, high-to-low swing across the body for slice, low power, move back to the net, "defend the net" drill) and common coaching advice. More fixes for every shot: <a href="{href("fix-my-padel.html")}">fix my padel</a>. Sore arm: <a href="{href("padel-elbow.html")}">padel elbow</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you practise overheads?</h2></div><div class="grid">
<div class="card"><h3>Bandeja to a target</h3><p>A partner feeds lobs from the other side. Every bandeja must land past their service line. Count how many in a row you can make.</p></div>
<div class="card"><h3>Bandeja, then back to the net</h3><p>After each bandeja, touch the net area with your racket before the next feed. It builds the habit of moving forward.</p></div>
<div class="card"><h3>One shot per session</h3><p>Spend 10 to 15 minutes on one overhead before mixing them. Filming yourself on a phone shows if you are turning sideways early enough.</p></div>
</div>
<p class="muted" style="margin-top:12px">Plan a full session with a timer in the <a href="{href("drills.html")}">drills planner</a>. Short lob and want to finish it? Full technique, x3 and x4: <a href="{href("padel-smash.html")}">how to smash in padel</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>See the ball paths</h3><p>Bandeja, víbora, bajada and chiquita drawn out in the <a href="{href("shots.html")}">shot library</a>.</p></div>
<div class="card"><h3>Stand in the right place</h3><p>Where you and your partner go when you are lobbed at the net: <a href="{href("positioning.html")}">padel positioning</a>.</p></div>
<div class="card"><h3>Check your level</h3><p>Picking the right overhead is a big step up. See where you are with the <a href="{href("level-calculator.html")}">level calculator</a>.</p></div>
<div class="card"><h3>Watch the best</h3><p>See who plays these shots best right now in the <a href="{href("padel-rankings.html")}">padel world rankings</a>.</p></div>
</div></div></section>'''
oh_faq = [
    ("What is the difference between a bandeja and a víbora?", "A bandeja is a slow, sliced overhead hit deep to keep your place at the net. A víbora is firmer and hit with side spin into the side glass or corner to attack. The bandeja is safer; the víbora can win points but is riskier."),
    ("When should I use a bandeja in padel?", "When you are lobbed at the net and the ball is not easy enough to smash, especially if you are further back or a little off balance. Hit it slow and deep, then move back to the net."),
    ("When should I smash in padel?", "Only on an easy, high ball when you are close to the net. From the service line or deeper, a hard smash usually comes back off the glass and gives the other pair the attack."),
    ("Is the bandeja a defensive shot?", "Yes. Coaches describe it as a defensive overhead. Its job is to keep your team at the net, not to win the point."),
    ("Should beginners learn the bandeja or the víbora first?", "The bandeja. It is easier to learn, safer and used more often. Add the víbora once your bandeja is reliable."),
    ("How do you hit a bandeja in padel?", "Turn side-on early, hold the racket up like a tray, let the ball drop to about eye height in front of you, then swing high to low and across your body to slice it. Use little power, aim past their service line and walk back to the net."),
    ("Why does my bandeja go into the net?", "Usually because you let the ball drop too low or swing straight down like a smash. Hit it around eye height, in front of you, and swing forward and across."),
    ("What grip do you use for a bandeja?", "The continental grip, the same one you use for volleys and serves. The víbora and smash use it too."),
    ("What should I do if the lob goes over my head?", "Turn, follow the ball to your back glass, let it bounce and come off the glass, then lob it back deep. Running backwards to force an overhead is a common mistake."),
]
page("bandeja-vs-vibora.html", "Bandeja vs Víbora vs Smash: Which Padel Overhead to Play?",
     "Bandeja, víbora or smash? Answer 4 questions to pick your overhead, learn how to hit a bandeja step by step, and fix it with the bandeja fault fixer.",
     oh, oh_faq, "Bandeja vs víbora")

# ---------------- INTERMEDIATE RACKET UPGRADE CHECK ----------------
def irq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-ir="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
IRQ_NOW = [
    ("shape", "Shape", [("round", "Round"), ("teardrop", "Teardrop"), ("diamond", "Diamond"), ("x", "Not sure")], "round"),
    ("weight", "Weight", [("light", "Under 355 g"), ("mid", "355 to 370 g"), ("heavy", "Over 370 g"), ("x", "Not sure")], "x"),
    ("face", "Face", [("glass", "Fibreglass"), ("carbon", "Carbon"), ("x", "Not sure")], "glass"),
]
IRQ_GAME = [
    ("often", "How often do you play?", [("1", "Once a week or less"), ("2", "2 or 3 times a week"), ("4", "4 times or more")], "2"),
    ("style", "How do you like to play?", [("control", "Steady, few errors"), ("allround", "A bit of everything"), ("attack", "Attack and finish at the net")], "allround"),
    ("arm", "Do your elbow, wrist or shoulder get sore?", [("no", "No"), ("yes", "Sometimes")], "no"),
    ("feel", "What bothers you about your racket?", [("power", "Not enough power"), ("control", "Balls fly long"), ("heavy", "Arm tired late on"), ("worn", "It feels dead or damaged"), ("fine", "Nothing really")], "power"),
]
IR_GO = {"round": go("padel-round-rackets"), "teardrop": go("padel-teardrop-rackets"), "diamond": go("padel-diamond-rackets")}
ir = f'''<header class="hero"><div class="wrap"><h1>Padel racket for intermediate players: is it time to upgrade?</h1>
<p class="lead">You can rally, you play every week and your first racket is starting to feel basic. Tell us what you play with now and how you play, and see which specs to keep, which to change and why.</p>
{quick("Most intermediate players do well with a teardrop racket: medium balance, about 360 to 370 g, a soft or medium EVA core and a fibreglass or carbon face. Stay round and a little lighter if your arm gets sore or you play a steady game. Diamond rackets suit experienced attackers who play often and have no arm trouble. If your racket is not damaged and you play once a week or less, an upgrade will change less than lessons will.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="ir">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">1. Your racket now</h2>
<p class="muted" style="margin:0 0 6px;font-size:.92rem">Check the frame, the box or the shop page. Not sure? Pick "Not sure".</p>
{"".join(irq(*x) for x in IRQ_NOW)}
<h2 style="font-size:1.3rem;margin:18px 0 4px">2. Your game</h2>
{"".join(irq(*x) for x in IRQ_GAME)}
<p class="muted" style="margin:0;font-size:.92rem">General buying advice from racket guides, not a rule. Your answers are saved on this device.</p>
</div>
<aside class="result" id="ir-out" aria-live="polite"><h2 id="ir-h">Your upgrade check</h2><p id="ir-p"></p><dl class="spec" id="ir-spec"></dl><ul class="b-why" id="ir-why"></ul><p id="ir-shop"></p><p class="wr-src">Try the racket before you buy if you can: many clubs and shops lend demo rackets.</p></aside>
</div></section>
<script>window.IRGO={json.dumps(IR_GO)};</script>
{AD.format("intermediate-mid")}
<section><div class="wrap"><div class="sh"><h2>What changes from a beginner to an intermediate racket?</h2><p class="muted">Ranges are a guide. Racket guides draw the lines in slightly different places.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Beginner</th><th scope="col">Intermediate</th><th scope="col">Advanced</th></tr></thead><tbody>
<tr><td>Shape</td><td>Round</td><td>Teardrop (round for control players)</td><td>Teardrop or diamond</td></tr>
<tr><td>Sweet spot</td><td>Large, in the middle</td><td>Medium, a little higher</td><td>Small and high on a diamond</td></tr>
<tr><td>Balance</td><td>Low (head-light)</td><td>Medium</td><td>Medium to high</td></tr>
<tr><td>Weight</td><td>About 355 to 365 g</td><td>About 360 to 370 g</td><td>About 365 to 375 g or more</td></tr>
<tr><td>Core feel</td><td>Soft</td><td>Soft or medium</td><td>Medium to firm</td></tr>
<tr><td>Face</td><td>Fibreglass</td><td>Fibreglass or carbon</td><td>Usually carbon</td></tr>
<tr><td>Who it suits</td><td>New, learning to rally</td><td>Plays 2 to 3 times a week, wants comfort and more options</td><td>Plays most days, leagues or tournaments</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Sources use different weight bands: some split light and heavy at 365 g, others at 370 g. Shop pages often give a range, such as 360 to 375 g. Check yours with the <a href="{href("racket-balance.html")}">weight and balance decoder</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why is teardrop the usual intermediate shape?</h2></div><div class="grid">
<div class="card"><span class="pill i">Teardrop</span><h3 style="margin-top:10px">A step up, not a jump</h3><p>A teardrop sits between round and diamond. You get more punch on overheads than a round racket gives, while the sweet spot is still big enough to forgive a slightly late hit.</p></div>
<div class="card"><span class="pill b">Round</span><h3 style="margin-top:10px">Still a good choice</h3><p>Moving up a level does not mean you must leave round. If you win points with steady lobs and volleys, or your arm gets sore, a better round racket can be the right upgrade.</p></div>
<div class="card"><span class="pill a">Diamond</span><h3 style="margin-top:10px">Wait for it</h3><p>Most guides keep diamonds for advanced attacking players. The sweet spot is small and high, so mis-hits cost more, and the extra head weight puts more load on the elbow.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Soft or hard: which core and face?</h2></div><div class="grid">
<div class="card"><h3>Soft core</h3><p>Soft EVA or foam cushions the ball. It gives easier power at slow speeds, is kind to joints and is often suggested for intermediate players.</p></div>
<div class="card"><h3>Firm core</h3><p>Firm EVA feels stiff. It rewards fast, clean swings with control and power, but it forgives less when you miss the middle. Usually an advanced choice.</p></div>
<div class="card"><h3>Fibreglass face</h3><p>Softer and more flexible. Comfortable, forgiving and cheaper. Plenty of intermediate players stay with it.</p></div>
<div class="card"><h3>Carbon face</h3><p>Stiffer and more durable, with more precise feel, but more vibration reaches your arm. Rackets with carbon faces usually cost more.</p></div>
</div>
<p class="muted" style="margin-top:14px">You will see numbers like 3K, 12K or 18K on carbon rackets. They describe the carbon weave. Brands use them differently, so compare how a racket feels rather than the number alone. See <a href="{href("padel-racket-materials.html")}">what 3K, 12K and 18K mean</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When is it worth buying a new padel racket?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">If this is you</th><th scope="col">What to do</th></tr></thead><tbody>
<tr><td>Your racket has a crack, a rattle or a dead spot</td><td>Run the <a href="{href("racket-care.html")}">racket health check</a>. If it fails, replace it.</td></tr>
<tr><td>You play 2 or more times a week and want more on your overheads</td><td>A teardrop with medium balance is the usual next step</td></tr>
<tr><td>Your arm hurts after playing</td><td>Stay light, low balance and soft. See <a href="{href("padel-elbow.html")}">padel elbow</a> and <a href="{href("padel-injuries.html")}">padel injuries</a></td></tr>
<tr><td>Balls fly long and you lack control</td><td>Do not go harder or heavier. A round or teardrop with a low to medium balance helps</td></tr>
<tr><td>The handle slips or feels thin</td><td>A new overgrip first. It is the cheapest upgrade: <a href="{href("padel-grip.html")}">grip guide</a></td></tr>
<tr><td>You play once a week or less and nothing is wrong</td><td>Keep it. Lessons and <a href="{href("drills.html")}">drills</a> will change more</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">General buying advice in our own words, not a rule.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How should I test a racket before I buy?</h2></div><div class="grid">
<div class="card"><span class="pill b">Step 1</span><h3 style="margin-top:10px">Borrow or demo</h3><p>Ask friends at your club, or ask the club or shop for a demo racket. Play at least a full match with it.</p></div>
<div class="card"><span class="pill b">Step 2</span><h3 style="margin-top:10px">Test at the net</h3><p>Fast volleys show if it is too heavy or head-heavy. If you are late at the net, go lighter or lower balance.</p></div>
<div class="card"><span class="pill b">Step 3</span><h3 style="margin-top:10px">Test off the glass</h3><p>Defend balls off the back glass and lob. If balls keep flying long, the racket may be too powerful for you right now.</p></div>
<div class="card"><span class="pill b">Step 4</span><h3 style="margin-top:10px">Check your arm next day</h3><p>Any new elbow or wrist ache means the racket is too heavy, too head-heavy or too stiff for you.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Compare two rackets</h3><p>Put the weight and balance of your racket and the new one into the <a href="{href("racket-balance.html")}">balance decoder</a>.</p></div>
<div class="card"><h3>On a budget?</h3><p>See good value picks in <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets</a> and what a <a href="{href("best-padel-racket-for-beginners.html")}">beginner racket</a> needs, and this week's <a href="{href("padel-black-friday.html")}">Black Friday deals</a>.</p></div>
<div class="card"><h3>Check your level</h3><p>Not sure you are intermediate yet? Try the <a href="{href("level-calculator.html")}">level calculator</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop rackets by shape</h3><p>Filter by shape first, then check the weight and balance on the product page against your result above.</p><ul class="aff-links"><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop rackets</a></li><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond rackets</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
ir_faq = [
    ("What padel racket should an intermediate player use?", "Usually a teardrop with medium balance, about 360 to 370 g, a soft or medium core and a fibreglass or carbon face. Steady players and anyone with a sore arm can stay with a round, lighter racket."),
    ("When should I upgrade my padel racket?", "When it is damaged or feels dead, when you play two or more times a week and have outgrown it, or when it causes arm pain. If you play once a week or less and it is fine, keep it."),
    ("Should an intermediate player use a diamond racket?", "Most racket guides keep diamond rackets for advanced attacking players. The small, high sweet spot forgives less, and the head weight loads the elbow. Try a teardrop first."),
    ("How heavy should an intermediate padel racket be?", "About 360 to 370 g suits most intermediate players. Go to the lower end if your arm gets tired or sore."),
    ("Is carbon better than fibreglass for intermediate players?", "Not always. Carbon is stiffer and more durable with a more precise feel, but sends more vibration to the arm. Fibreglass is softer and forgiving, and many intermediate players stay with it."),
    ("Soft or hard core for an intermediate padel racket?", "Soft or medium. A soft core gives easier power and comfort; a firm core suits fast, clean swings and is usually for advanced players."),
    ("Is a more expensive padel racket better?", "Not by itself. Higher prices often mean carbon and firmer cores, which suit advanced players. The right shape, weight and balance for your game matter more than the price."),
]
page("intermediate-padel-racket.html", "Padel Racket for Intermediate Players: Free Upgrade Check",
     "Which padel racket should an intermediate player use? Enter your racket and game to see which specs to keep or change: shape, weight, balance and core.",
     ir, ir_faq, "Intermediate padel racket")

# ---------------- PADEL GIFT FINDER (24 Nov 2026, DEMAND R1 "padel gifts") ----------------
def gfq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-gf="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
GFQ = [
    ("who", "How much do they play?", [("new", "Just started"), ("reg", "About once a week"), ("keen", "2 or more times a week")], "reg"),
    ("budget", "Your budget (about, in £, $ or €)", [("s", "Under 20"), ("m", "20 to 60"), ("l", "60 to 150"), ("xl", "Over 150")], "m"),
    ("racket", "Do they have their own racket?", [("no", "No, they rent or borrow"), ("yes", "Yes")], "yes"),
    ("specs", "Do you know which racket suits them (shape, weight)?", [("no", "No idea"), ("yes", "Yes, I know their racket")], "no"),
    ("shoes", "Do they have padel shoes?", [("no", "No, or not sure"), ("yes", "Yes")], "no"),
    ("bag", "Do they have a padel bag?", [("no", "No, or not sure"), ("yes", "Yes")], "no"),
]
GF_LINKS = {k: go(k) for k in ("padel-balls", "padel-overgrips", "padel-bags", "padel-shoes", "padel-round-rackets", "padel-teardrop-rackets", "padel-rackets")}
GF_V = [("lesson", "A padel lesson"), ("court", "A court booking for four"), ("americano", "An Americano night with friends"), ("racket", "A new racket of your choice"), ("shoes", "New padel shoes, we'll choose together"), ("own", "Write my own")]
gf = f'''<header class="hero"><div class="wrap"><h1>Padel gifts: what to buy a padel player.</h1>
<p class="lead">Answer six quick questions about the person and your budget. You get a short list of padel gifts that suit them, what to check before you buy, and the gifts to avoid. Then print a free gift voucher for a lesson, a court or a night of padel.</p>
{quick("The safest padel gifts are things every player uses up: a pack of padel balls, overgrips and frame protector tape (small budget), a padel bag, a court booking or a lesson (medium budget), and padel shoes in their size (bigger budget). Only buy a racket if you know the shape and weight they like, or if they don't own one yet. Otherwise give a voucher and let them choose.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="gf">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">About the player</h2>
{"".join(gfq(*x) for x in GFQ)}
<p class="muted" style="margin:0;font-size:.92rem">General gift advice in our own words, not a rule. Your answers are saved on this device only.</p>
</div>
<aside class="result" id="gf-out" aria-live="polite"><h2 id="gf-h">Gift ideas</h2><p id="gf-p"></p><ol class="gf-list" id="gf-list"></ol><p id="gf-warn" class="wr-src"></p></aside>
</div></section>
<script>window.GFGO={json.dumps(GF_LINKS)};</script>
{AD.format("gifts-mid")}
<section><div class="wrap"><div class="sh"><h2>What are good padel gifts by budget?</h2><p class="muted">Rough price bands in £, $ or €. Prices change, so check the shop.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Budget</th><th scope="col">Gift ideas</th><th scope="col">Good for</th></tr></thead><tbody>
<tr><td>Under 20</td><td>A can of padel balls (most cans hold 3), a pack of overgrips, frame protector tape, sweatbands, sports socks</td><td>Anyone who plays, even once a month</td></tr>
<tr><td>20 to 60</td><td>A multi-pack of balls, a racket cover, a court booking, a ball saver tube, a small padel backpack</td><td>Weekly players</td></tr>
<tr><td>60 to 150</td><td>A padel bag, padel shoes, a lesson with a coach, a first racket for someone who has none</td><td>New players and regulars</td></tr>
<tr><td>Over 150</td><td>A block of lessons, a racket they have already tried, a padel weekend or camp, a voucher for their racket upgrade</td><td>Keen players who play several times a week</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is a padel racket a good gift?</h2></div><div class="grid">
<div class="card"><span class="pill b">Yes</span><h3 style="margin-top:10px">For someone who has none</h3><p>A new player who rents rackets will use a simple first racket a lot. Pick a round shape, light weight, soft core and low balance. See <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets</a> for what to look for. For a child, use the <a href="{href("padel-racket-for-kids.html")}">junior size finder</a>.</p></div>
<div class="card"><span class="pill i">Maybe</span><h3 style="margin-top:10px">If you know their racket</h3><p>If you know the shape, weight and balance they like, or they have already played with a model, a racket can be a great gift. Keep the receipt.</p></div>
<div class="card"><span class="pill a">Avoid</span><h3 style="margin-top:10px">A surprise upgrade</h3><p>Regular players are picky. A racket that is too heavy, too head-heavy or too stiff can feel wrong and even hurt their arm. Give a voucher and let them choose, or send them to the <a href="{href("intermediate-padel-racket.html")}">upgrade check</a>.</p></div>
</div>
<p class="muted" style="margin-top:12px">To find out what suits them without spoiling the surprise, ask what shape their racket is and how heavy it feels, or try our <a href="{href("racket-finder.html")}">racket finder</a> with what you know.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which small padel gifts do players really use?</h2></div><div class="grid">
<div class="card"><h3>Padel balls</h3><p>Balls lose their bounce after a few sessions, so players always need more. Buy padel balls, not tennis balls: padel balls have less pressure inside. More on <a href="{href("padel-balls.html")}">when balls are dead</a>.</p></div>
<div class="card"><h3>Overgrips</h3><p>A thin wrap that goes over the handle. It gets slippery and worn, and HEAD suggests changing it at least every two months. A pack of 3 is a cheap, useful gift. See <a href="{href("padel-grip.html")}">how to put one on</a>.</p></div>
<div class="card"><h3>Frame protector tape</h3><p>A strip that goes round the top of the frame and stops chips when the racket hits the glass or floor. Single protectors cost about $9 to $12 in the US (Padel Browser, Sep 2026). It adds a few grams at the top, so some players skip it. More in <a href="{href("racket-care.html")}">racket care</a>.</p></div>
<div class="card"><h3>Racket cover or ball saver</h3><p>A cover keeps sand, heat and knocks off the racket. A ball saver tube keeps opened balls lively a little longer.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What should I check before buying padel shoes as a gift?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Check</th><th scope="col">Why</th></tr></thead><tbody>
<tr><td>Their size in that brand</td><td>Sizes differ between brands. Look at a pair they already wear.</td></tr>
<tr><td>The sole</td><td>Most padel courts need a herringbone (zig-zag) sole. Running shoes are not safe on sand courts. See the <a href="{href("padel-shoes.html")}">padel shoes guide</a>.</td></tr>
<tr><td>Returns</td><td>Ask for a gift receipt and check the shop's exchange window over the holidays.</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Make a padel gift voucher</h2><p class="muted">Gift a lesson, a court or a night of padel. Fill it in, then print it or save it as a PDF.</p></div>
<div class="quiz" id="gv">
<div class="card">
<div class="q"><h3>What is the gift?</h3><div class="opts" data-gv="gift" role="group" aria-label="What is the gift?">{"".join(f'<button type="button" class="opt" data-v="{k}" aria-pressed="{"true" if k == "lesson" else "false"}">{e(t)}</button>' for k, t in GF_V)}</div></div>
<label class="gv-f">Your own gift text <input id="gv-own" type="text" maxlength="60" placeholder="For example: two hours of padel and lunch"></label>
<label class="gv-f">To <input id="gv-to" type="text" maxlength="40" placeholder="Their name"></label>
<label class="gv-f">From <input id="gv-from" type="text" maxlength="40" placeholder="Your name"></label>
<label class="gv-f">Message <input id="gv-msg" type="text" maxlength="90" placeholder="Happy Christmas! See you on court."></label>
<label class="gv-f">Use by <input id="gv-date" type="text" maxlength="30" placeholder="For example: 31 March 2027"></label>
<button class="btn lime sm" type="button" id="gv-print">Print or save as PDF</button>
<p class="muted" style="margin:10px 0 0;font-size:.92rem">Nothing is sent anywhere. The voucher is made on your device.</p>
</div>
<div class="gv-card" id="gv-card" aria-live="polite"><svg viewBox="0 0 120 120" aria-hidden="true" class="gv-art"><ellipse cx="50" cy="44" rx="34" ry="38" fill="#1e46c8"/><g fill="#e4eef6">{"".join(f'<circle cx="{50+x}" cy="{44+y}" r="2.4"/>' for y in range(-24, 25, 12) for x in range(-24, 25, 12) if x*x + y*y <= 700)}</g><rect x="44" y="80" width="12" height="34" rx="5" fill="#1e46c8"/><circle cx="95" cy="92" r="13" fill="#e8f84a" stroke="#0b1a46" stroke-width="2"/></svg>
<p class="gv-k">Padel gift voucher</p><h3 id="gv-gift">A padel lesson</h3><p class="gv-to">For <b id="gv-to-o">you</b></p><p id="gv-msg-o" class="gv-msg"></p><p class="gv-from">From <b id="gv-from-o">me</b><span id="gv-date-o"></span></p></div>
</div>
<p class="muted" style="margin-top:12px">Booking a lesson or court? Ask the club whether it sells its own gift vouchers or court credit. Running a padel night? Use our <a href="{href("americano.html")}">Americano draw maker</a> to set the games.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Buying a racket?</h3><p>Start with the <a href="{href("racket-finder.html")}">racket finder</a>, check any racket with the <a href="{href("best-padel-racket-for-beginners.html")}">beginner racket checker</a>, then compare budget picks in <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets</a>.</p></div>
<div class="card"><h3>Shopping this week?</h3><p>Black Friday is 27 November. See what is worth buying in our <a href="{href("padel-black-friday.html")}">padel Black Friday guide</a>.</p></div>
<div class="card"><h3>New to padel yourself?</h3><p>The <a href="{href("beginners.html")}">beginner's guide</a> covers what to bring and the rules you need for a first game together.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop padel gifts</h3><p>The gifts players use most: balls, overgrips, bags and shoes, plus rackets by shape.</p><ul class="aff-links"><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-black-friday")}" {AFF_ATTR}>Black Friday deals</a></li></ul>{AFF_NOTE}</div></div></section>'''
gf_faq = [
    ("What is a good gift for a padel player?", "Things they use up: padel balls, overgrips and frame protector tape for a small budget; a bag, a court booking or a lesson for a medium budget; padel shoes in their size for a bigger budget."),
    ("Should I buy a padel racket as a gift?", "Only if they don't have one yet, or you know the shape, weight and balance they like. Regular players are picky about rackets, so a voucher is often the better gift."),
    ("What is a cheap padel gift?", "A can of padel balls, a pack of overgrips, frame protector tape, sweatbands or padel socks. All cost under about 20 in pounds, dollars or euros."),
    ("What padel gift can I give a beginner?", "A simple first racket (round, light, soft) if they rent one now, a lesson with a coach, padel balls, or padel shoes with a herringbone sole."),
    ("How many balls are in a can of padel balls?", "Most cans or tubes of padel balls hold 3 balls. Shops also sell multi-packs of several cans."),
    ("Can I give padel lessons as a gift?", "Yes. Ask the club or coach whether they sell gift vouchers, or print our free voucher and book the lesson together."),
    ("Are padel shoes a good gift?", "Yes, if you know their size in that brand and choose the right sole, usually herringbone. Keep the gift receipt in case they need another size."),
]
page("padel-gifts.html", "Padel Gifts: Free Gift Finder by Budget + Printable Voucher | Padel Glass Box",
     "What to buy a padel player: answer 6 questions for gift ideas that suit their level and your budget, what to check before buying, and a printable voucher.",
     gf, gf_faq, "Padel gifts")

# ---------------- PADEL EQUIPMENT + WHAT TO WEAR (24 Nov 2026, DEMAND R4 "padel equipment", 4 "padel outfits") ----------------
def kpq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-kp="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
KPQ = [
    ("often", "How often do you play?", [("first", "First game"), ("some", "Now and then"), ("week", "Every week or more")], "first"),
    ("where", "Where is the court?", [("in", "Indoors"), ("out", "Outdoors")], "in"),
    ("wx", "What is the weather like?", [("warm", "Warm or hot"), ("mild", "Mild"), ("cold", "Cold")], "mild"),
    ("racket", "Do you have a padel racket?", [("no", "No"), ("yes", "Yes")], "no"),
    ("shoes", "Which shoes do you have?", [("padel", "Padel shoes"), ("tennis", "Tennis or clay court shoes"), ("run", "Only running shoes or trainers")], "run"),
]
KP_LINKS = {k: go(k) for k in ("padel-balls", "padel-overgrips", "padel-bags", "padel-shoes", "padel-round-rackets")}
eq = f'''<header class="hero"><div class="wrap"><h1>Padel equipment: what you need and what to wear.</h1>
<p class="lead">Tell us how often you play, where, and what you already own. You get a packing list split into must bring, good to have and skip for now, with tips for each item. Tick things off as you pack.</p>
{quick("To play padel you only need three things: a padel racket (many clubs rent them), padel balls (usually sold in cans of 3) and court shoes with grip, ideally padel shoes with a herringbone sole. Wear light sports clothes that wick sweat and let you move, with a pocket for the second ball. Most clubs have no strict dress code, but they expect sportswear and non-marking soles. A bag, overgrips and a protector can wait until you play every week.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="kp">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Your game</h2>
{"".join(kpq(*x) for x in KPQ)}
<p class="muted" style="margin:0;font-size:.92rem">General kit advice in our own words. Your answers and ticks are saved on this device only.</p>
</div>
<aside class="result" id="kp-out" aria-live="polite"><h2 id="kp-h">Your packing list</h2><p id="kp-p"></p><div id="kp-list"></div>
<div class="btns" style="margin:14px 0 0"><button class="btn lime sm" type="button" id="kp-copy">Copy my list</button><button class="btn ghost sm" type="button" id="kp-clear" style="color:#fff;border-color:rgba(255,255,255,.4)">Clear ticks</button></div>
<p id="kp-next" class="wr-src" style="margin-top:12px"></p></aside>
</div></section>
<script>window.KPGO={json.dumps(KP_LINKS)};</script>
{AD.format("equipment-mid")}
<section><div class="wrap"><div class="sh"><h2>What equipment do you need for padel?</h2><p class="muted">Must have first, extras later.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Item</th><th scope="col">Do you need it?</th><th scope="col">Tip for new players</th></tr></thead><tbody>
<tr><td>Padel racket</td><td>Yes (rent one at first)</td><td>Solid face with holes, no strings. Start with a round, light, forgiving racket. See the <a href="{href("racket-finder.html")}">racket finder</a> or <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets</a>.</td></tr>
<tr><td>Padel balls</td><td>Yes</td><td>Padel balls have a little less pressure than tennis balls. Most cans hold 3. Check <a href="{href("padel-balls.html")}">when balls are dead</a>.</td></tr>
<tr><td>Court shoes</td><td>Yes</td><td>Padel shoes with a herringbone (zig-zag) sole suit most sand-filled turf courts. Tennis or clay shoes are fine at first. Avoid running shoes. See the <a href="{href("padel-shoes.html")}">shoe guide</a>.</td></tr>
<tr><td>Sports clothes</td><td>Yes</td><td>Light, stretchy, sweat-wicking. Any tennis or gym kit works.</td></tr>
<tr><td>Water bottle</td><td>Yes</td><td>Bring plenty, especially outdoors in summer.</td></tr>
<tr><td>Overgrip</td><td>Later</td><td>A thin wrap over the handle for grip. Change it when it feels slippery. <a href="{href("padel-grip.html")}">How to fit one</a>.</td></tr>
<tr><td>Frame protector</td><td>Optional</td><td>Tape round the top of the frame that stops chips off the glass. Adds a few grams. More in <a href="{href("racket-care.html")}">racket care</a>.</td></tr>
<tr><td>Padel bag</td><td>Later</td><td>A normal sports bag is fine to start. A padel bag helps once you carry a racket, shoes and balls every week.</td></tr>
<tr><td>Wristband, cap, sunglasses</td><td>Optional</td><td>Wristbands stop sweat running to your hand. Cap and sports sunglasses help on sunny outdoor courts.</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What should you wear to play padel?</h2><p class="muted">There is no special padel uniform. Tennis clothes work almost the same.</p></div><div class="grid">
<div class="card"><h3>Top</h3><p>A light T-shirt, polo or tank in a technical fabric (polyester or similar) that dries fast. Avoid heavy cotton: it gets wet and stays wet.</p></div>
<div class="card"><h3>Bottoms</h3><p>Shorts, a sports skirt with shorts under it, or leggings. They should stretch for lunges and low volleys, and not be too loose or too tight.</p></div>
<div class="card"><h3>A pocket for the ball</h3><p>You hold the second serve ball, so a deep, secure pocket (or ball clip) saves trips to the back of the court.</p></div>
<div class="card"><h3>Socks</h3><p>Sports socks with some padding, not thin casual socks. They help stop blisters when you slide and stop a lot.</p></div>
<div class="card"><h3>Layers</h3><p>A light top for the warm-up and after the game. In winter outdoors: a base layer, full-length leggings or joggers and a windproof jacket you can take off.</p></div>
<div class="card"><h3>Sun and sweat</h3><p>Outdoors in summer, wear a cap or visor and sports sunglasses against glare. Wristbands and a small towel help in any heat.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is there a dress code for padel?</h2></div>
<div class="card"><p style="margin:0">Most padel clubs have no strict dress code. They do expect sports clothes and shoes with <b>non-marking soles</b> that won't damage the turf. Some clubs and tournaments have their own rules, so check the club's website before your first booking.</p></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What should you not wear for padel?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Avoid</th><th scope="col">Why</th><th scope="col">Wear instead</th></tr></thead><tbody>
<tr><td>Running shoes</td><td>Little side support and the wrong grip for sand turf, so ankles roll more easily</td><td>Padel shoes (herringbone or omni sole), or tennis/clay shoes at first</td></tr>
<tr><td>Football boots with studs</td><td>Studs can damage the turf and catch on it</td><td>Court shoes</td></tr>
<tr><td>Jeans or chinos</td><td>No stretch for lunges and low shots</td><td>Shorts, a sports skirt or leggings</td></tr>
<tr><td>Heavy cotton tops and hoodies</td><td>Soak up sweat and get heavy</td><td>A light technical top, with a layer for the warm-up</td></tr>
<tr><td>Thin casual socks</td><td>Blisters from sliding and stopping</td><td>Padded sports socks</td></tr>
<tr><td>Shallow pockets</td><td>The spare ball falls out</td><td>Deep or zipped pockets, or a ball clip</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Can you rent padel equipment?</h2></div><div class="grid">
<div class="card"><h3>Rackets</h3><p>Many clubs rent rackets at reception or include them in beginner sessions. Ask when you book. Renting lets you try a few shapes before you buy.</p></div>
<div class="card"><h3>Balls</h3><p>Ask whether the club sells balls at the desk. Bringing your own fresh can is safer, because old balls bounce low.</p></div>
<div class="card"><h3>Shoes</h3><p>Ask the club whether it lends or rents shoes. For a first game, tennis or clay court shoes, or a borrowed pair of padel shoes, are fine.</p></div>
</div>
<p class="muted" style="margin-top:12px">Rental and prices differ from club to club. Check the club's own website or booking app.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Ready for your first game?</h3><p>The <a href="{href("beginners.html")}">first match checklist</a> covers the four rules you need and how to book a court.</p></div>
<div class="card"><h3>Buying a racket?</h3><p>Answer three questions in the <a href="{href("racket-finder.html")}">racket finder</a>, then compare <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets</a>.</p></div>
<div class="card"><h3>Need shoes?</h3><p>The <a href="{href("padel-shoes.html")}">padel shoe finder</a> tells you which sole suits your court. To carry it all, use the <a href="{href("padel-bags.html")}">padel bag picker</a>.</p></div>
<div class="card"><h3>What will it all cost?</h3><p>Add up court hire, kit, balls and lessons with the <a href="{href("padel-cost.html")}">padel cost calculator</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop padel equipment</h3><p>The basics first: a forgiving racket, balls and shoes. Then overgrips and a bag.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li></ul>{AFF_NOTE}</div></div></section>'''
eq_faq = [
    ("What equipment do you need for padel?", "A padel racket, padel balls and court shoes with grip, plus sports clothes and water. Overgrips, a frame protector and a padel bag are useful later but not needed to start."),
    ("What do you wear to play padel?", "Light sportswear that wicks sweat and stretches: a technical T-shirt or polo, shorts, a sports skirt or leggings, padded sports socks and court shoes. A pocket for the second ball helps."),
    ("Is there a dress code for padel?", "Most clubs have no strict dress code, but they expect sports clothes and non-marking court shoes. Some clubs and tournaments set their own rules, so check before you go."),
    ("Can I play padel in running shoes?", "It is better not to. Running shoes have little side support and the wrong grip for sand-filled turf. Use padel shoes, or tennis or clay court shoes for your first games."),
    ("Can I wear tennis clothes for padel?", "Yes. Tennis clothes and padel clothes are almost the same: light, breathable and easy to move in."),
    ("Do I need to buy a racket to start padel?", "No. Many clubs rent rackets. Rent or borrow for a few games, then buy a round, light, forgiving racket when you know you'll keep playing."),
    ("What should I wear for padel in winter?", "Outdoors in the cold: a base layer, a light top, full-length leggings or joggers and a windproof jacket for the warm-up, with cushioned sports socks. Take layers off as you warm up."),
]
page("padel-equipment.html", "Padel Equipment and What to Wear: Beginner Kit Checklist",
     "What do you need to play padel and what should you wear? A packing list for your game (must bring, nice to have, skip), plus a clothing and dress code guide.",
     eq, eq_faq, "Padel equipment")

page("about.html", f"About {SITE}: Free Padel Tools and Guides", f"About {SITE}, a free set of padel tools and plain-English guides to rackets, rules, scoring and shots, and how to get in touch with us.",
     f'<section><div class="wrap" style="max-width:760px"><h1>About {SITE}</h1><p>{SITE} makes free, simple padel tools: a racket finder, a score keeper, an interactive rules court and a shot library.</p><h2>How we check facts</h2><p>Rules follow the International Padel Federation (FIP). Equipment advice is general guidance checked against several trusted guides; we don\'t take payment to recommend gear.</p><h2 id="affiliate">Affiliate links and how we choose products</h2><p>Some shop links on Padel Glass Box are affiliate links (for example through Awin with Padel Market). If you buy through one, we may earn a small commission at no extra cost to you. Pages with affiliate links say so at the top, and the racket finder says so above its shop button. Commissions never decide what we recommend: the finder picks a racket shape, weight and balance from your answers before any shop is involved, and our guides name the features to look for rather than paid placements.</p><h2>Contact</h2><p>Email <a href="mailto:awaiskaramat@hotmail.com">awaiskaramat@hotmail.com</a>.</p></div></section>', crumb="About")

# ---- Buyer pages (23 Nov 2026, from Google Trends: "cheap padel racket" breakout US, "padel racket black friday" +110% UK) ----
_budget = [
    ("Adidas Match 2026", "Round", "Beginner", "about €60", "zonadepadel (Sep 2026)", "The cheapest sensible first racket: light and easy to move."),
    ("Siux Beat Hybrid 2026", "Hybrid", "Beginner to intermediate", "about €56", "zonadepadel (Sep 2026)", "Best value if you want one racket to grow into."),
    ("Head Bolt 2026", "Round", "Beginner", "about €70", "zonadepadel (Sep 2026)", "Easy handling for players coming from tennis."),
    ("Dunlop Megamax 2026", "Round", "Beginner", "about €70", "zonadepadel (Sep 2026)", "A forgiving frame with good ball output."),
    ("Babolat Air Origin", "Teardrop", "Beginner", "under £90", "Padelspeak (Nov 2026)", "Very forgiving at 345 g, a favourite first racket."),
    ("Wilson Optix V2 Power 2026", "Teardrop", "Beginner who likes to attack", "about £95", "Padelspeak (Nov 2026)", "Carbon-reinforced fibreglass with a rough face for spin."),
    ("Kuikma PR Comfort Soft", "Round", "Beginner", "under £100", "Padelspeed (Apr 2026)", "Soft and comfortable: a low-risk choice while you learn."),
    ("Dreampadel Match Carbon 2.0", "Round", "Beginner to intermediate", "about €100", "zonadepadel (Sep 2026)", "A firmer carbon feel at the top of the budget."),
]
_brows = "".join(f'<tr><th scope="row">{e(n)}</th><td>{s}</td><td>{e(l)}</td><td>{e(p)}</td><td>{e(w)}</td></tr>' for n, s, l, p, src, w in _budget)
cheap = f'''<header class="hero"><div class="wrap"><h1>Cheap padel rackets that are actually good.</h1>
<p class="lead">You don't need a $300 racket to start. Here is what a good budget racket looks like, eight that reviewers rate under $100 / £100 / €100, and what you give up by spending less.</p>
{quick("Yes, a cheap padel racket is fine for beginners. Look for a round shape, 355 to 370 g, a soft EVA core and a low (head-light) balance, which costs about £55 to £115. Good picks under €100 include the Adidas Match 2026, Siux Beat Hybrid 2026, Head Bolt 2026 and Babolat Air Origin.")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<h2>What should a cheap padel racket have?</h2><div class="table-wrap"><table class="facts"><tbody>
<tr><th scope="row">Shape</th><td>Round. The sweet spot sits low and in the middle, so mis-hits still go over.</td></tr>
<tr><th scope="row">Weight</th><td>355 to 370 g. Lighter is kinder to your elbow while your technique is new.</td></tr>
<tr><th scope="row">Core</th><td>Soft EVA or foam. More comfort, and the ball comes off the face easily.</td></tr>
<tr><th scope="row">Balance</th><td>Low (head-light). Quicker at the net and easier to control.</td></tr>
<tr><th scope="row">Face</th><td>Fibreglass, or fibreglass with some carbon. Softer and more forgiving than full carbon.</td></tr>
</tbody></table></div>
<p class="muted">Source: Central Sports UK beginner buying guide (2026). Not sure which shape suits you? Answer three questions in our <a href="{href("racket-finder.html")}">racket finder</a>.</p>
<h2>Which cheap padel rackets are worth buying?</h2>
<div class="table-wrap"><table class="facts"><thead><tr><th>Racket</th><th>Shape</th><th>Level</th><th>Price seen</th><th>Why</th></tr></thead><tbody>{_brows}</tbody></table></div>
<p class="muted">Prices are what each reviewer or shop listed on the date shown, so check the current price before you buy. Picks come from Padelspeak, Padelspeed and zonadepadel budget lists; we haven't tested these rackets ourselves.</p>
<div class="aff-box"><h3>Shop budget rackets</h3><ul class="aff-links"><li><a href="/go/padel-round-rackets" {AFF_ATTR}>Round rackets</a></li><li><a href="/go/padel-rackets" {AFF_ATTR}>All rackets</a></li><li><a href="/go/padel-black-friday-rackets" {AFF_ATTR}>Black Friday rackets</a></li></ul>{AFF_NOTE}</div>
<h2>What do you give up with a cheap racket?</h2><ul>
<li><strong>Less power and spin</strong> on smashes and bandejas than carbon rackets. Beginners rarely notice.</li>
<li><strong>A shorter life.</strong> Soft budget cores lose their pop sooner if you play several times a week.</li>
<li><strong>Fewer weight options.</strong> Most come in one weight.</li></ul>
<p>When you play twice a week and hit the ball cleanly, that is the time to move up. See our <a href="{href("racket-balance.html")}">weight and balance guide</a> first.</p>
<h2>Is now a good time to buy?</h2><p>Black Friday is on <strong>27 November 2026</strong>, and last season's rackets usually get the biggest discounts. See our <a href="{href("padel-black-friday.html")}">padel Black Friday guide</a>.</p>
</div></section>'''
cheap_faq = [
    ("Is a cheap padel racket good enough for a beginner?", "Yes. A round, 355 to 370 g racket with a soft EVA core and a low balance forgives mis-hits and is easy on the arm. Most beginners don't benefit from a full-carbon racket."),
    ("How much should I spend on my first padel racket?", "About £55 to £115 (or $60 to $120) buys a good first racket. Put the rest toward court time and a lesson, which will improve your game faster than a more expensive racket."),
    ("What is the best padel racket under $100?", "Reviewers' budget favourites include the Adidas Match 2026, Siux Beat Hybrid 2026, Head Bolt 2026, Dunlop Megamax 2026 and Babolat Air Origin. Pick a round one if you are new."),
    ("Are cheap padel rackets bad for your elbow?", "Not if you choose a light racket with a soft core. Heavy, stiff, head-heavy rackets are the ones that strain the elbow."),
]
page("cheap-padel-rackets.html", "Cheap Padel Rackets: 8 Good Ones Under $100 / £100",
     "Best cheap padel rackets under $100 / £100: what a good budget racket looks like (round, 355-370 g, soft EVA), 8 picks reviewers rate, and what you give up.",
     cheap, cheap_faq, "Cheap padel rackets")

bf = f'''<header class="hero"><div class="wrap"><h1>Padel Black Friday 2026: what's worth buying.</h1>
<p class="lead">When the sales run, which padel gear is a real bargain, and a quick calculator to see what a discount code actually saves you.</p>
{quick("Black Friday is Friday 27 November 2026 and Cyber Monday is 30 November. Last season's rackets are usually the best value, and balls and bags are often discounted too. Padel Market is offering 15% off a selection of rackets, shoes, bags and accessories with the code BLACK15.")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<h2>When is padel Black Friday 2026?</h2><div class="table-wrap"><table class="facts"><tbody>
<tr><th scope="row">Black Friday</th><td>Friday 27 November 2026</td></tr>
<tr><th scope="row">Cyber Monday</th><td>Monday 30 November 2026</td></tr>
<tr><th scope="row">Early deals</th><td>Many padel shops add offers through November ahead of the day.</td></tr>
</tbody></table></div>
<h2>Which padel deals are live now?</h2>
<p><strong>Padel Market</strong>: 15% off a selection of rackets, shoes, clothing, bags, backpacks, accessories and balls with code <strong>BLACK15</strong>. It only works on products in their Black Friday collection and can't be combined with other codes.</p>
<div class="aff-box"><h3>See the Black Friday padel deals</h3><ul class="aff-links"><li><a href="/go/padel-black-friday" {AFF_ATTR}>All Black Friday padel deals</a></li><li><a href="/go/padel-black-friday-rackets" {AFF_ATTR}>Black Friday rackets</a></li><li><a href="/go/padel-bags" {AFF_ATTR}>Bags</a></li><li><a href="/go/padel-balls" {AFF_ATTR}>Balls</a></li></ul>{AFF_NOTE}</div>
<h2>What is the discount really worth?</h2>
<div class="card" id="bf-calc"><label>Normal price <input id="bf-was" type="number" inputmode="decimal" min="0" step="0.01" value="120"></label>
<label>Sale price <input id="bf-now" type="number" inputmode="decimal" min="0" step="0.01" value="96"></label>
<label><input id="bf-code" type="checkbox"> Also apply a 15% code (like BLACK15)</label>
<p id="bf-out" aria-live="polite" style="font-size:1.1rem;margin:12px 0 0"></p></div>
<script>(function(){{function r(){{var w=+document.getElementById('bf-was').value||0,n=+document.getElementById('bf-now').value||0;if(document.getElementById('bf-code').checked)n=n*0.85;var s=w-n,p=w?100*s/w:0;document.getElementById('bf-out').innerHTML=w&&n?'You pay <strong>'+n.toFixed(2)+'</strong> and save <strong>'+s.toFixed(2)+' ('+p.toFixed(0)+'% off)</strong>.':'Enter both prices.';}}['bf-was','bf-now','bf-code'].forEach(function(i){{document.getElementById(i).addEventListener('input',r);}});r();}})();</script>
<h2>What is worth buying on Black Friday?</h2><ul>
<li><strong>Last season's racket.</strong> When shops clear old models to make room for the new year's stock, that is the deepest racket discount of the year. The 2026 version of a racket usually plays almost exactly like the 2027 one.</li>
<li><strong>Balls by the pack.</strong> You go through them fast, so a multi-pack discount adds up. See <a href="{href("padel-balls.html")}">when to change padel balls</a>.</li>
<li><strong>A bag or backpack</strong> if you carry more than one racket.</li>
<li><strong>Shoes, but buy early.</strong> A discount is no use if your size sells out on day one. Check which <a href="{href("padel-shoes.html")}">sole you need</a> first.</li></ul>
<h2>How do I avoid a fake deal?</h2><ul>
<li>Some shops keep a permanent "sale" price, so a big percentage off is not always a real drop. Compare with the price a couple of weeks earlier.</li>
<li>Pick the racket for your level first, then look for it on sale, not the other way round. Our <a href="{href("racket-finder.html")}">racket finder</a> takes a minute.</li>
<li>Budget? These are the <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets worth buying</a>.</li><li>First racket? Check its specs with the <a href="{href("best-padel-racket-for-beginners.html")}">beginner racket checker</a>.</li><li>Buying for someone else? Try the <a href="{href("padel-gifts.html")}">padel gift finder</a>.</li><li>Upgrading from your first racket? Run the <a href="{href("intermediate-padel-racket.html")}">intermediate upgrade check</a> first.</li></ul>
<p class="muted">Sources: Padel Market Black Friday page (code and conditions, November 2026); Padel Browser "When to buy padel gear 2026"; zonadepadel Black Friday 2026 page. We update this page if offers change.</p>
</div></section>'''
bf_faq = [
    ("When is padel Black Friday 2026?", "Black Friday is Friday 27 November 2026 and Cyber Monday is Monday 30 November 2026. Many padel shops start adding offers earlier in November."),
    ("Is Black Friday a good time to buy a padel racket?", "Yes, especially last season's models, which usually get the biggest discounts. Choose the racket for your level first, then look for it on sale."),
    ("Is there a Padel Market discount code for Black Friday?", "Padel Market is offering 15% off a selection of products with the code BLACK15. It only applies to items in their Black Friday collection and can't be combined with other codes."),
    ("Should I buy padel shoes on Black Friday?", "If you know your size and the sole type you need, yes, but buy early: popular sizes sell out first."),
]
page("padel-black-friday.html", "Padel Black Friday 2026: Padel Deals, Rackets, BLACK15 Code",
     "Padel Black Friday 2026 is 27 November (Cyber Monday 30 Nov). Live padel deals, Padel Market's 15% BLACK15 code, a discount calculator and what's worth buying.",
     bf, bf_faq, "Padel Black Friday")

# ---------------- PADEL RACKET FOR KIDS (24 Nov 2026, DEMAND 4 "padel racket for kids") ----------------
def jrq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-jr="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
JRQ = [
    ("age", "How old is the child?", [("0", "3 to 6"), ("1", "7 to 9"), ("2", "10 to 12"), ("3", "13 to 14"), ("4", "15 or older")], "1"),
    ("h", "How tall are they?", [("0", "Under 120 cm (4 ft)"), ("1", "120 to 140 cm"), ("2", "140 to 155 cm"), ("3", "Over 155 cm (5 ft 1)"), ("x", "Not sure")], "x"),
    ("build", "Compared with friends their age, they are", [("s", "Smaller or not so strong"), ("a", "About average"), ("b", "Bigger or stronger")], "a"),
    ("play", "How much do they play?", [("try", "Just trying it"), ("week", "About once a week"), ("lots", "Lessons or club squad, 2+ times a week")], "try"),
    ("sore", "Does their arm or shoulder hurt after playing?", [("no", "No"), ("yes", "Yes, sometimes")], "no"),
]
JR_GO = {k: go(k) for k in ("padel-round-rackets", "padel-teardrop-rackets", "padel-rackets", "padel-balls", "padel-overgrips")}
JR_SVG = '''<svg viewBox="0 0 320 70" class="jr-scale" role="img" aria-label="Racket weight scale from 200 to 400 grams. The suggested band for this child is highlighted. Most adult rackets are about 355 to 375 grams.">
<rect x="10" y="26" width="300" height="14" rx="7" fill="#1a3a9a"/>
<rect id="jr-adult" x="242.5" y="26" width="30" height="14" fill="#9cc4ea" opacity=".45"/>
<rect id="jr-band" x="10" y="22" width="40" height="22" rx="8" fill="#e8f84a"/>
<g fill="#9fb0e0" font-size="10" font-family="Onest, sans-serif" text-anchor="middle"><text x="10" y="60">200 g</text><text x="85" y="60">250</text><text x="160" y="60">300</text><text x="235" y="60">350</text><text x="310" y="60" text-anchor="end">400 g</text></g>
<text x="257.5" y="16" fill="#9cc4ea" font-size="10" font-family="Onest, sans-serif" text-anchor="middle">Most adults</text>
</svg>'''
jr = f'''<header class="hero"><div class="wrap"><h1>Padel racket for kids: which size and weight?</h1>
<p class="lead">Junior padel rackets differ mainly in weight, not length. Answer five quick questions about the child to see the weight band to look for, the right shape and core, and whether they are ready for an adult racket.</p>
{quick("Choose by weight. As a rough guide: about 210 to 260 g for ages 3 to 6, 260 to 300 g for 7 to 9, 300 to 330 g for 10 to 12, and 330 to 355 g for 13 to 14. Pick a round shape with a soft core and a fibreglass face, use the wrist cord, and move to a light adult racket (about 350 to 360 g) at around 12 to 14, when the child is strong enough.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="jr">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">About the child</h2>
{"".join(jrq(*x) for x in JRQ)}
<p class="muted" style="margin:0;font-size:.92rem">A rough guide in our own words, based on maker and retailer sizing advice. Answers are saved on this device only. Ages, sessions and junior competitions: <a href="{href("junior-padel.html")}">junior padel guide for parents</a>.</p>
</div>
<aside class="result" id="jr-out" aria-live="polite"><h2 id="jr-h">Junior racket</h2><p id="jr-p"></p>{JR_SVG}<dl class="spec" id="jr-spec"></dl><p id="jr-move"></p><p id="jr-warn" class="wr-src"></p><p id="jr-next" class="wr-src"></p></aside>
</div></section>
<script>window.JRGO={json.dumps(JR_GO)};</script>
{AD.format("kids-mid")}
<section><div class="wrap"><div class="sh"><h2>What size padel racket does a child need?</h2><p class="muted">Approximate bands. Makers split their ranges at different ages, so use the child's size and strength as well as their age.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Age</th><th scope="col">Height (about)</th><th scope="col">Racket weight</th><th scope="col">Type and shape</th></tr></thead><tbody>
<tr><td>3 to 6</td><td>Under 120 cm (4 ft)</td><td>210 to 260 g</td><td>Mini or foam racket, round</td></tr>
<tr><td>7 to 9</td><td>120 to 140 cm</td><td>260 to 300 g</td><td>Light junior racket, round, soft core</td></tr>
<tr><td>10 to 12</td><td>140 to 155 cm</td><td>300 to 330 g</td><td>Junior racket, round (teardrop for strong players later)</td></tr>
<tr><td>13 to 14</td><td>Over 155 cm (5 ft 1)</td><td>330 to 355 g</td><td>Older junior or light adult racket</td></tr>
<tr><td>Teen ready to move up</td><td>Adult size</td><td>About 350 to 360 g to start</td><td>Light round adult racket</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">For comparison, most adult rackets weigh about 355 to 375 g. Check the weight printed on the racket or the shop page: some rackets sold as "junior" still weigh 330 to 350 g, which is heavy for a young child.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Are junior padel rackets shorter?</h2></div><div class="grid">
<div class="card"><h3>A little, but weight matters more</h3><p>Unlike tennis, padel rackets don't come in many lengths. Older junior rackets are often only about a finger shorter than an adult racket. The big difference is weight, and a thinner handle for small hands.</p></div>
<div class="card"><h3>The adult limit</h3><p>The rules allow a racket up to 45.5 cm long and 38 mm thick. Junior rackets are smaller or thinner than that. See all the sizes on our <a href="{href("racket-balance.html")}">racket weight and balance</a> page.</p></div>
<div class="card"><h3>Don't cut down an adult racket</h3><p>A shortened adult racket is still heavy and stiff, so it tires a young arm. A racket made for juniors is lighter all over.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do I know if a padel racket is too heavy for my child?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Sign</th><th scope="col">What to do</th></tr></thead><tbody>
<tr><td>Their arm, elbow or shoulder is sore after playing</td><td>The most common sign the racket is too heavy or too stiff. Go lighter and softer, and rest. If pain lasts, see a doctor or physio. More in <a href="{href("padel-injuries.html")}">padel injuries</a>.</td></tr>
<tr><td>The racket head drops after a few shots</td><td>Their arm is tired. A lighter racket lets them keep good form for longer.</td></tr>
<tr><td>They are always late on the ball</td><td>A heavy racket is slow to swing and hard to get ready at the net.</td></tr>
<tr><td>They hold it with two hands for most shots</td><td>Often a sign it is too heavy. Try one band lighter.</td></tr>
<tr><td>It feels too light and they say it "flaps"</td><td>Too light is less of a problem than too heavy. Move up one band when they grow or get stronger.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">General coaching advice in our own words. If in doubt, choose the lighter racket.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which shape, core and face suit a child?</h2></div><div class="grid">
<div class="card"><span class="pill b">Shape</span><h3 style="margin-top:10px">Round</h3><p>A round racket has its sweet spot low and in the middle, so off-centre hits still go over. Teardrop and diamond shapes move the sweet spot higher and are harder to control. Keep those for strong teenagers.</p></div>
<div class="card"><span class="pill b">Core</span><h3 style="margin-top:10px">Soft foam</h3><p>A soft EVA or foam core gives an easy, comfortable feel and helps a light swing send the ball deep. Hard cores are for strong adult players.</p></div>
<div class="card"><span class="pill b">Face</span><h3 style="margin-top:10px">Fibreglass</h3><p>Fibreglass faces are more flexible and cheaper. Stiff carbon faces are for older, stronger players. Learn more in <a href="{href("intermediate-padel-racket.html")}">racket specs explained</a>.</p></div>
<div class="card"><span class="pill i">Grip</span><h3 style="margin-top:10px">Thin handle</h3><p>Junior rackets have thinner handles. An overgrip can make a handle thicker as their hand grows, but nothing makes a thick handle thinner. See <a href="{href("padel-grip.html")}">how to hold a padel racket</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>At what age can kids start playing padel?</h2></div><div class="grid">
<div class="card"><h3>From about 3 years old</h3><p>HEAD says children can start hitting first shots from about age three, once they are strong enough to hold the racket. LTA Padel says padel lets children of all ages and abilities join in.</p></div>
<div class="card"><h3>Use the wrist cord</h3><p>The cord on the handle should go round the wrist every time. It stops the racket flying out of a small hand and hitting someone. The FIP rules say every player must wear it.</p></div>
<div class="card"><h3>Coaching and junior events</h3><p>In Great Britain, LTA Padel runs youth competitions for all ages and levels. They use a simple, fast format, usually last about half a day, and earn LTA ranking points. Ask your club about junior sessions with an accredited coach.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When should a child move to an adult padel racket?</h2></div>
<div class="card"><p>There is no fixed age. HEAD suggests around 12 or 13; Padel Browser says usually 12 to 14. It depends on strength and technique more than birthdays. Signs they are ready:</p>
<ul style="margin:8px 0 12px;padding-left:20px;display:grid;gap:6px"><li>They are close to adult height and can swing a 330 to 355 g racket without tiring.</li><li>They play every week and their arm never hurts afterwards.</li><li>They hit with good form at the end of a session, not only at the start.</li></ul>
<p>Start with a light, round adult racket of about 350 to 360 g. Then use the <a href="{href("racket-finder.html")}">racket finder</a> to choose the next one.</p></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>First game as a family?</h3><p>The <a href="{href("beginners.html")}">beginner's guide</a> covers the basic rules, and the <a href="{href("padel-equipment.html")}">kit planner</a> shows what to bring.</p></div>
<div class="card"><h3>Buying it as a present?</h3><p>See more ideas, plus a printable voucher, in the <a href="{href("padel-gifts.html")}">padel gift finder</a>.</p></div>
<div class="card"><h3>Practice at home or the club</h3><p>Short, fun games work best for kids. Pick a few from the <a href="{href("drills.html")}">padel drills planner</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop light rackets and kit</h3><p>Look for round rackets and check the weight in grams on each one before you buy.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 24 Nov 2026: HEAD "How to choose a padel racquet for kids" (start from about 3; under 10 about 300 g, over 10 about 330 g, junior about a finger shorter; adult racket from about 12 or 13), Decathlon UK "How to choose a padel racket for children" (round control rackets; about 265 g for 5 to 8, 310 g for 8 to 11, 330 g for 12+; EVA foam), Padel Browser "Best junior padel rackets 2026" (10 Jun 2026: age and height bands, round shape, soft core, fibreglass, wrist cord, don't cut down adult rackets, move up at 12 to 14), LTA Padel "Padel for kids" and "Youth padel competitions". Weight bands in our table combine these and are rounded.</p></div></section>'''
jr_faq = [
    ("What size padel racket should a child use?", "Choose by weight more than length: about 210 to 260 g for ages 3 to 6, 260 to 300 g for 7 to 9, 300 to 330 g for 10 to 12 and 330 to 355 g for 13 to 14. Adjust for the child's height and strength."),
    ("How heavy should a junior padel racket be?", "Most junior rackets weigh between about 260 and 330 g. Younger children need the lighter end. Adult rackets usually weigh about 355 to 375 g."),
    ("At what age can a child use an adult padel racket?", "Usually around 12 to 14, when they are strong enough. Start with a light, round adult racket of about 350 to 360 g."),
    ("What shape padel racket is best for kids?", "Round. It has a low, central sweet spot that forgives off-centre hits. Teardrop and diamond rackets are harder to control."),
    ("At what age can kids start padel?", "Children can start hitting first shots from about age three, once they can hold a light racket. Coaching sessions for juniors are common at clubs."),
    ("Can a child use a cut-down adult padel racket?", "It is better not to. A shortened adult racket is still heavy and stiff and tires a young arm. Junior rackets are lighter and softer all over."),
    ("Are junior padel rackets shorter than adult rackets?", "Only a little. Older junior rackets are often about a finger shorter than an adult racket. The main difference is a lighter weight and a thinner handle."),
]
page("padel-racket-for-kids.html", "Padel Racket for Kids: Junior Size and Weight Finder by Age | Padel Glass Box",
     "Which padel racket for a child? Junior racket weight by age and height (3 to 14), shape and core, signs it is too heavy, and a free junior size finder.",
     jr, jr_faq, "Padel racket for kids")

# ---------------- PADEL LESSONS (25 Nov 2026, DEMAND R3 "padel lessons") ----------------
def lsq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-ls="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
LSQ = [
    ("reg", "Where do you play?", [("uk", "UK (£)"), ("us", "US ($)"), ("eu", "Europe (€)"), ("ae", "UAE (AED)")], "uk"),
    ("type", "What kind of lesson?", [("p1", "Private, just me"), ("p2", "Shared private, 2 players"), ("p4", "Small group, 3 or 4"), ("cl", "Group clinic, 5 to 8")], "p1"),
    ("per", "The price you were quoted is", [("all", "For the whole lesson"), ("pp", "Per person")], "all"),
    ("len", "How long is the lesson?", [("30", "30 min"), ("60", "60 min"), ("90", "90 min")], "60"),
    ("blk", "How many lessons will you book?", [("1", "Just one"), ("4", "4"), ("6", "6"), ("10", "10")], "1"),
]
ls_nums = '''<div class="gen-nums">
<div class="q"><h3><label for="ls-price">Price quoted</label></h3><input class="search" id="ls-price" type="number" min="0" step="1" value="60" inputmode="decimal" style="margin:0"></div>
<div class="q"><h3><label for="ls-court">Court hire extra (0 if included)</label></h3><input class="search" id="ls-court" type="number" min="0" step="1" value="0" inputmode="decimal" style="margin:0"></div>
</div>
<div class="gen-nums">
<div class="q"><h3><label for="ls-n">Players sharing the cost</label></h3><input class="search" id="ls-n" type="number" min="1" max="8" step="1" value="1" inputmode="numeric" style="margin:0"></div>
<div class="q"><h3><label for="ls-disc">Block discount</label></h3><select class="search" id="ls-disc" style="margin:0"><option value="0">None</option><option value="10">10%</option><option value="15">15%</option><option value="20">20%</option></select></div>
</div>'''
LS_GO = {k: go(k) for k in ("padel-round-rackets", "padel-shoes", "padel-balls")}
LS_ASK = [
    "Is the coach qualified? (UK: an LTA-accredited padel coach. Elsewhere: ask which padel course they did.)",
    "Is the price for the whole lesson or per person?",
    "Is court hire included, and are there extra fees for floodlights or peak times?",
    "Are rackets and balls provided, or do I bring my own?",
    "How many players will be in the group, and are they my level?",
    "What is the cancellation window, and is there a no-show fee?",
    "Is there a discount if I book a block of lessons?",
    "What should I work on after the lesson, and what is the next step?",
]
ls = f'''<header class="hero"><div class="wrap"><h1>Padel lessons: what they cost and what to expect.</h1>
<p class="lead">Private, shared or group: see typical padel lesson prices in the UK and US, work out what your lesson really costs each, and learn what happens in a first lesson and how to pick a good coach.</p>
{quick("A private padel lesson usually costs about £40 to £80 an hour in the UK and about $50 to $160 an hour in the US. Group sessions and clinics are cheaper: about £10 to £30 or $20 to $60 per person. Many US clubs run 60-minute intro clinics for free to $40. Sharing a private lesson with 1 to 3 friends cuts the cost each a lot.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="ls">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Lesson cost checker</h2>
<p class="muted" style="margin-top:0">Enter the price a club or coach gave you. See what it costs you per lesson, per hour and for a block, and how it compares with typical prices.</p>
{"".join(lsq(*x) for x in LSQ[:3])}
{ls_nums}
{"".join(lsq(*x) for x in LSQ[3:])}
<p class="muted" style="margin:0;font-size:.92rem">Typical ranges come from published 2026 price guides (sources below) and are rounded. Your answers are saved on this device only.</p>
</div>
<aside class="result" id="ls-out" aria-live="polite"><h2 id="ls-h">Your lesson</h2><p id="ls-p"></p><dl class="spec" id="ls-spec"></dl><p id="ls-v"></p><p id="ls-tip"></p><p id="ls-next" class="wr-src"></p></aside>
</div></section>
<script>window.LSGO={json.dumps(LS_GO)};</script>
{AD.format("lessons-mid")}
<section><div class="wrap"><div class="sh"><h2>How much do padel lessons cost?</h2><p class="muted">Typical 2026 prices. London and big US cities are often at the top of the range.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Lesson type</th><th scope="col">UK</th><th scope="col">US</th></tr></thead><tbody>
<tr><td>Private lesson, 1 player</td><td>£40 to £80 an hour</td><td>$50 to $160 an hour</td></tr>
<tr><td>Shared private, 2 players</td><td>About £25 to £50 each</td><td>No reliable published range</td></tr>
<tr><td>Group session or clinic</td><td>About £10 to £30 per person</td><td>About $20 to $60 per person</td></tr>
<tr><td>Intro or taster session</td><td>Often free or low cost at clubs; some charge for a short level check</td><td>Free to $40 for 60 minutes</td></tr>
<tr><td>Beginner course, 4 to 6 weeks</td><td>About £80 to £150</td><td>Starter packs of 4 to 6 lessons about $100 to $200</td></tr>
<tr><td>Block of lessons booked ahead</td><td>Often 10 to 20% off</td><td>Packs common, discount varies</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Always check two things: whether the price is per person or for the whole lesson, and whether court hire is included. In Europe and the UAE prices vary a lot by city and club, and we found no reliable published range, so compare two or three local quotes in the checker above.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Private, shared or group: which padel lesson should you book?</h2></div><div class="grid">
<div class="card"><span class="pill b">Private</span><h3 style="margin-top:10px">Best for fixing one thing fast</h3><p>The coach watches only you. Good for a stubborn problem like your grip, serve or play off the back glass. It is the most expensive option per person.</p></div>
<div class="card"><span class="pill b">Shared private</span><h3 style="margin-top:10px">Best value with a regular partner</h3><p>Two to four friends split one coach. Many clubs charge only a small extra amount per added player, so the cost each drops a lot. You also learn to play as a pair.</p></div>
<div class="card"><span class="pill b">Group clinic</span><h3 style="margin-top:10px">Best for your first steps</h3><p>A cheap way to learn the basics and meet players at your level. You get less personal feedback, and you may be grouped with people at a different level.</p></div>
<div class="card"><span class="pill i">Course</span><h3 style="margin-top:10px">Best for building a habit</h3><p>A weekly block of 4 to 6 sessions with the same coach and group. You repeat skills often enough to keep them.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What happens in a first padel lesson?</h2><p class="muted">Most coaches cover the same basics. The order and timing below are a typical example for a 60-minute session.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">About</th><th scope="col">What you do</th></tr></thead><tbody>
<tr><td>5 to 10 min</td><td>Warm-up and a short chat about your sport background. Some clubs do a quick level check.</td></tr>
<tr><td>10 min</td><td>How to hold the racket (the continental grip) and the ready position. Strap round your wrist.</td></tr>
<tr><td>10 to 15 min</td><td>Forehand and backhand from the back of the court, with control rather than power.</td></tr>
<tr><td>10 min</td><td>Letting the ball come off the back glass and hitting it after it rebounds. This is the new skill for most people.</td></tr>
<tr><td>10 min</td><td>Volleys at the net and where to stand with your partner.</td></tr>
<tr><td>5 min</td><td>The underarm serve: bounce, hit at or below the waist, land it diagonally.</td></tr>
<tr><td>5 to 10 min</td><td>A short game or cooperative rally to put it together. Basic scoring.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Most coaches leave the smash, bandeja and víbora for later lessons. Read ahead with our guides to the <a href="{href("padel-grip.html")}">padel grip</a>, <a href="{href("wall-rules.html")}">playing off the walls</a> and <a href="{href("serve-rules.html")}">the serve</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What should I bring to my first padel lesson?</h2></div><div class="grid">
<div class="card"><h3>Racket and balls</h3><p>Intro sessions and clinics usually provide them. Ask when you book. If you buy later, a round racket is easiest to learn with: see the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
<div class="card"><h3>Shoes</h3><p>Padel or tennis shoes grip best on sandy turf. Trainers are usually fine for a first intro session, but not for regular play. See the <a href="{href("padel-shoes.html")}">padel shoes guide</a>.</p></div>
<div class="card"><h3>Clothes and water</h3><p>Normal gym clothes, layers if you play outdoors in winter, and a full water bottle. Arrive about 10 minutes early. Full list in the <a href="{href("padel-equipment.html")}">kit planner</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do I find a good padel coach?</h2></div><div class="grid">
<div class="card"><h3>In the UK</h3><p>Use the LTA "Find a coach" tool with the padel filter, or ask your club which coach runs beginner sessions. The main LTA qualification is the Level 2 Padel Instructor, a five-day course. Check the coach is insured and has safeguarding and first-aid training, especially for children.</p></div>
<div class="card"><h3>In the US and elsewhere</h3><p>Ask the club's pro shop or front desk, or look in the coaching section of booking apps such as Playtomic. There is no single required padel qualification everywhere, so ask what padel-specific training and experience the coach has. Some tennis pros also coach padel.</p></div>
<div class="card"><h3>Good signs</h3><p>The coach asks about your level and goals first, the lesson has a clear plan, they give you one or two things to work on, and they tell you what to do next. A "lesson" that is only feeding balls with no feedback is poor value.</p></div>
</div>
<p class="muted" style="margin-top:12px">Good-sign list is general advice in our own words.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How many padel lessons does a beginner need?</h2></div>
<div class="card"><p>There is no fixed number. A common path, in our own words:</p>
<ul style="margin:8px 0 12px;padding-left:20px;display:grid;gap:6px"><li>Take one intro session or lesson before your first proper match, so you know the grip, the serve and how the walls work.</li><li>Add two or three more hours of coached play or clinics, then join beginner open play or a social like an <a href="{href("americano.html")}">Americano</a>.</li><li>After that, many players book a 4 to 6 week course or a block of shared lessons, and take a private lesson when one thing keeps going wrong.</li></ul>
<p>Check your progress with the <a href="{href("level-calculator.html")}">padel level calculator</a>, and practise between lessons with the <a href="{href("drills.html")}">drills planner</a>.</p></div></div></section>
<section style="padding-top:0"><div class="wrap" style="max-width:860px"><div class="sh"><h2>What should I ask before booking a padel lesson?</h2><p class="muted">Tick each one off as you ask. Saved on this device.</p></div>
<div class="card">{checklist("lsask", LS_ASK)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Before your first lesson</h3><p>Learn the four basic rules in the <a href="{href("beginners.html")}">beginner's guide</a>, follow the <a href="{href("padel-beginner-plan.html")}">30-day beginner plan</a>, and see your full budget with the <a href="{href("padel-cost.html")}">padel cost calculator</a>.</p></div>
<div class="card"><h3>After a few lessons</h3><p>Find your level with the <a href="{href("level-calculator.html")}">level calculator</a> so you join the right group sessions.</p></div>
<div class="card"><h3>Ready for your own racket?</h3><p>Answer three questions in the <a href="{href("racket-finder.html")}">racket finder</a>, check one you found with the <a href="{href("best-padel-racket-for-beginners.html")}">beginner racket checker</a>, or see <a href="{href("cheap-padel-rackets.html")}">good cheap rackets</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Gear for your lessons</h3><p>Most clubs lend rackets for intro sessions. Once you book regular lessons, your own racket and shoes help you improve faster.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 25 Nov 2026. UK prices: UK Padel Guide "Padel coaching cost UK 2026" (13 Oct 2026), Padeli "Padel coaching in the UK 2026" (updated 22 Nov 2026) and "Padel lessons for beginners UK" (28 Oct 2026), RacketRise "How to find a padel coach in the UK" (updated 6 Nov 2026), Padel Finders "How much does padel cost in the UK" (Feb 2026), Park Sports London (shared lessons up to 3 players, small fee per extra player). US prices: Padel Browser "How much does padel cost in the US" (8 Jun 2026), "First padel lesson: intro clinics in the US" (15 Oct 2026) and "How to choose a padel coach" (18 May 2026), Bounce "Why is padel so expensive" (23 Jul 2026), Miami Living "Best padel clubs in Miami 2026" (20 Sep 2026). First lesson content: LTA Padel "What to expect from your first padel session" (16 Oct 2026) plus the UK and US guides above. Coach qualification: LTA Level 2 Padel Instructor, five-day course (Padeli, RacketRise). Prices are rounded ranges, not quotes, and change often. Left out: UAE and European price ranges (no reliable published data), single-source coach certifications.</p></div></section>'''
ls_faq = [
    ("How much does a padel lesson cost?", "A private padel lesson usually costs about £40 to £80 an hour in the UK and about $50 to $160 an hour in the US. Group sessions and clinics cost about £10 to £30 or $20 to $60 per person."),
    ("How much is a group padel lesson?", "In the UK about £10 to £30 per person per session. In the US clinics usually cost about $20 to $60 per person, and many clubs run 60-minute intro clinics for free to $40."),
    ("Can I share a private padel lesson with friends?", "Usually yes. Many coaches let 2 to 4 players share one private lesson for a small extra fee per player, which makes the cost each much lower. Ask when you book."),
    ("How long is a padel lesson?", "Most private lessons are 60 minutes. Group clinics are usually 60 or 90 minutes, and US intro clinics are usually 60 minutes."),
    ("What do you learn in a first padel lesson?", "The grip and ready position, forehand and backhand, playing the ball after it comes off the back glass, volleys at the net, the underarm serve and a short game with basic scoring."),
    ("Do I need my own racket for a padel lesson?", "Not for a first lesson. Intro sessions and clinics usually lend rackets and balls. Ask the club when you book."),
    ("How many padel lessons do I need as a beginner?", "There is no fixed number. One intro session before your first match, then two or three more hours of coaching or clinics, is a common way to start. After that many players book a 4 to 6 week course."),
]
page("padel-lessons.html", "Padel Lessons: UK and US Cost, First Lesson, Cost Checker",
     "How much do padel lessons cost? Private about £40-£80 or $50-$160 an hour, groups less. What a first lesson covers, finding a coach, and a cost checker.",
     ls, ls_faq, "Padel lessons")

page("privacy.html", f"Privacy Policy | {SITE}", f"{SITE} privacy policy: how we use cookies, Google AdSense, Google Analytics and affiliate links, what data is stored and how to opt out.",
     f'<section><div class="wrap" style="max-width:760px"><h1>Privacy policy</h1><p>Last updated: {e(UPDATED)}.</p><h2>What we collect</h2><p>Your score, checklist ticks and quiz answers are saved only in your own browser. If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the cheat sheet and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time.</p><h2>Analytics</h2><p>We use Google Analytics to count visits and see which pages are popular. It uses cookies and collects details like pages viewed, approximate location and device type.</p><h2>Advertising</h2><p>This site uses Google AdSense. Google and its partners use cookies to show ads based on your visits to this and other websites. You can turn off personalised ads at <a href="https://adssettings.google.com">Google Ads Settings</a>. Learn more at <a href="https://policies.google.com/technologies/partner-sites">policies.google.com/technologies/partner-sites</a>.</p><h2>Affiliate links</h2><p>Some links may be affiliate links. If you buy through them, we may earn a small fee at no extra cost to you.</p><h2>Contact</h2><p>Email <a href="mailto:awaiskaramat@hotmail.com">awaiskaramat@hotmail.com</a>.</p></div></section>', crumb="Privacy policy")
page("404.html", f"Page not found | {SITE}", "This page doesn't exist.",
     f'<section><div class="wrap"><h1>That one went out.</h1><p class="lead">This page doesn\'t exist.</p><a class="btn lime" href="{href("index.html")}">Back to the home page</a></div></section>')

page("thanks.html", f"Check your inbox | {SITE}", "Confirm your email to get the free padel rules cheat sheet.", NL_THANKS)
page("welcome.html", f"Your padel cheat sheet | {SITE}", "Download your free padel rules cheat sheet.", NL_WELCOME)

# ---------------- PADEL RANKINGS (25 Nov 2026, RADAR P1 "best padel player in the world" / "padel rankings") ----------------
RK_DATE = "23 Nov 2026"
RK_MEN = [("1", "Arturo Coello", "Spain", 20211), ("1", "Agustín Tapia", "Argentina", 20211), ("3", "Alejandro Galán", "Spain", 14033), ("3", "Federico Chingotto", "Argentina", 14033),
          ("5", "Juan Lebrón", "Spain", 8560), ("6", "Leandro Augsburger", "Argentina", 8483), ("7", "Franco Stupaczuk", "Argentina", 6180), ("8", "Jon Sanz", "Spain", 5243),
          ("9", "Paquito Navarro", "Spain", 5241), ("10", "Martín Di Nenno", "Argentina", 4813)]
RK_WOMEN = [("1", "Gemma Triay", "Spain", 15831), ("1", "Delfina Brea", "Argentina", 15831), ("3", "Bea González", "Spain", 13926), ("4", "Ariana Sánchez", "Spain", 12333),
            ("5", "Claudia Fernández", "Spain", 12306), ("6", "Andrea Ustero", "Spain", 12096), ("7", "Paula Josemaría", "Spain", 11223), ("8", "Martina Calvo", "Spain", 8636),
            ("9", "Claudia Jensen", "Argentina", 5548), ("10", "Sofía Araújo", "Portugal", 5423)]
# Points per round. 2026: LTA Padel guide (17 Apr 2026) + "old" values on Premier Padel's 2027 table + Wikipedia copy of FIP table. 2027: Premier Padel (10 Jun 2026).
RK_PTS = {
    "2026": {"major": {"w": 2000, "f": 1200, "sf": 720, "qf": 360, "r16": 180, "r32": 90, "r64": 35},
             "p1": {"w": 1000, "f": 600, "sf": 360, "qf": 180, "r16": 90, "r32": 45, "r64": 22},
             "p2": {"w": 600, "f": 360, "sf": 180, "qf": 90, "r16": 45, "r32": 22}},
    "2027": {"major": {"w": 2000, "f": 1200, "sf": 720, "qf": 380, "r16": 200, "r32": 100, "r64": 50},
             "p1": {"w": 1000, "f": 600, "sf": 380, "qf": 200, "r16": 110, "r32": 55, "r64": 35},
             "p2": {"w": 600, "f": 380, "sf": 200, "qf": 110, "r16": 55, "r32": 35}},
}
RK_RN = [("w", "Winner"), ("f", "Runner-up (lost the final)"), ("sf", "Semi-final"), ("qf", "Quarter-final"), ("r16", "Last 16"), ("r32", "Last 32"), ("r64", "Last 64 (first round)")]
def _rk_table(rows):
    return '<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Rank</th><th scope="col">Player</th><th scope="col">Country</th><th scope="col">FIP points</th></tr></thead><tbody>' + "".join(
        f'<tr><td>{"=" + r if [x[0] for x in rows].count(r) > 1 else r}</td><td>{e(n)}</td><td>{e(c)}</td><td>{p:,}</td></tr>' for r, n, c, p in rows) + "</tbody></table></div>"
def _rk_pts(y):
    t = RK_PTS[y]
    return '<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Round reached</th><th scope="col">Major</th><th scope="col">P1</th><th scope="col">P2</th></tr></thead><tbody>' + "".join(
        f'<tr><td>{lab}</td>' + "".join(f'<td>{t[c][k]:,}</td>' if k in t[c] else '<td>No round</td>' for c in ("major", "p1", "p2")) + "</tr>" for k, lab in RK_RN) + "</tbody></table></div>"
def rkq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-rk="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
RK_JS = {"pts": RK_PTS, "men": [[r, n, p] for r, n, c, p in RK_MEN], "women": [[r, n, p] for r, n, c, p in RK_WOMEN], "date": RK_DATE}
rk = f'''<header class="hero"><div class="wrap"><h1>Padel rankings: the world top 10 and how FIP points work.</h1>
<p class="lead">Who is the best padel player in the world right now? See the men's and women's FIP top 10, learn how ranking points are won and lost, and work out what a run of results is worth with our points calculator.</p>
{quick(f"In the FIP ranking of {RK_DATE}, Arturo Coello and Agustín Tapia share men's number 1 with 20,211 points each. Gemma Triay and Delfina Brea share women's number 1 with 15,831 points each. The ranking adds up each player's best 22 results over the last 52 weeks. Winning a Major is worth 2,000 points, a P1 1,000 and a P2 600.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="sh"><h2>Who is number 1 in padel right now?</h2><p class="muted">FIP world ranking of {RK_DATE}. It changes after each tournament week; the Mexico Major (23 to 29 Nov) and the season Finals in December will move it again.</p></div>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr))">
<div><h3 style="margin:0 0 10px">Men's top 10</h3>{_rk_table(RK_MEN)}</div>
<div><h3 style="margin:0 0 10px">Women's top 10</h3>{_rk_table(RK_WOMEN)}</div>
</div>
<p class="muted" style="margin-top:12px">Players marked "=" share a place on the same points. Partners who play the same events together usually end up level, which is why both number 1 spots are shared.</p></div></section>
{AD.format("rankings-mid")}
<section style="padding-top:0"><div class="wrap quiz" id="rk">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Ranking points calculator</h2>
<p class="muted" style="margin-top:0">Add tournament results one by one: the level and the round reached. See the points, the total from your best results, and where that total would sit against today's top 10.</p>
{rkq("yr", "Which points table?", [("2026", "2026 (current)"), ("2027", "2027 (new table)")], "2026")}
{rkq("cat", "Tournament level", [("major", "Major"), ("p1", "P1"), ("p2", "P2")], "p1")}
{rkq("rd", "Round reached", [(k, lab.split(" (")[0]) for k, lab in RK_RN], "qf")}
<div style="display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 14px"><button class="btn sm" type="button" id="rk-add">Add this result</button><button class="btn sm ghost" type="button" id="rk-demo">Try an example season</button><button class="btn sm ghost" type="button" id="rk-clear">Clear all</button></div>
<ol id="rk-list" class="rk-list"></ol>
<p class="muted" style="margin:0;font-size:.92rem">Only Major, P1 and P2 events are in the calculator. Real totals also include season Finals and CUPRA FIP Tour events, and points from a year ago drop off week by week. Your list is saved on this device only.</p>
</div>
<aside class="result" id="rk-out" aria-live="polite"><h2 id="rk-h">0 points</h2><p id="rk-p">Add a result to start.</p><dl class="spec" id="rk-spec"></dl><p id="rk-v"></p><p id="rk-next" class="wr-src"></p></aside>
</div></section>
<script>window.RK={json.dumps(RK_JS, ensure_ascii=False)};</script>
<section><div class="wrap"><div class="sh"><h2>How does the padel world ranking work?</h2></div><div class="grid">
<div class="card"><span class="pill b">Counting</span><h3 style="margin-top:10px">Best 22 results</h3><p>Each player's ranking is the total of their best 22 results in Premier Padel and CUPRA FIP Tour events. Weaker results beyond those 22 do not count.</p></div>
<div class="card"><span class="pill b">Time</span><h3 style="margin-top:10px">A rolling 52 weeks</h3><p>Points stay for one year. When the same week comes round again, last year's points drop off and this year's result replaces them. To keep points, a player must match or beat what they did a year earlier.</p></div>
<div class="card"><span class="pill b">Players</span><h3 style="margin-top:10px">Points belong to each player</h3><p>Padel is played in pairs, but the ranking is for individuals. If a player changes partner, they keep the points they have already won.</p></div>
<div class="card"><span class="pill b">Race</span><h3 style="margin-top:10px">The Race is this year only</h3><p>The FIP Race counts only results from the current calendar year, again the best 22. The top 16 in the Race qualify for the season-ending Premier Padel Finals, held in Barcelona.</p></div>
<div class="card"><span class="pill b">Levels</span><h3 style="margin-top:10px">Bigger events, more points</h3><p>The Premier Padel tour has four levels: Majors, P1, P2 and the Finals. Below it, the CUPRA FIP Tour has Platinum, Gold, Silver and Bronze events, worth far fewer points.</p></div>
<div class="card"><span class="pill b">You</span><h3 style="margin-top:10px">Not the same as your club level</h3><p>The FIP ranking is only for players in pro tour events. Club and app levels, such as Playtomic's, are a separate system. Find yours with the <a href="{href("level-calculator.html")}">padel level calculator</a>.</p></div>
</div>
<p class="muted" style="margin-top:12px">The partner line is general background in our own words; the rest follows the FIP and LTA Padel explanations listed below.</p></div></section>
<section style="padding-top:0"><div class="wrap" style="max-width:860px"><div class="sh"><h2>How many points do you get for winning a padel tournament?</h2><p class="muted">FIP ranking points per player in 2026, by the round you reach.</p></div>
{_rk_pts("2026")}
<p class="muted" style="margin-top:12px">Winning the season-ending Premier Padel Finals is worth 1,500 points. A FIP Platinum title is worth 300 and a FIP Gold title 150. Some first-round and qualifying values differ between the men's and women's draws, so treat the last row as a guide.</p></div></section>
<section style="padding-top:0"><div class="wrap" style="max-width:860px"><div class="sh"><h2>What changes in the padel ranking in 2027?</h2><p class="muted">Agreed by Premier Padel and FIP and announced on 10 June 2026.</p></div>
{_rk_pts("2027")}
<div class="grid" style="margin-top:16px">
<div class="card"><h3>More points for middle rounds</h3><p>Titles and finals keep the same points. Quarter-finals, last 16, last 32 and first rounds are worth more, so steady results count for a bit more.</p></div>
<div class="card"><h3>21 results, not 22</h3><p>From 2027 the ranking counts each player's best 21 results instead of 22.</p></div>
<div class="card"><h3>Top players out of small events</h3><p>Higher-ranked players can no longer enter the main draw of lower CUPRA FIP events (Gold, Silver, Bronze), leaving more room for rising players.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid"><div class="card"><h3>On this week</h3><p>The last Major of 2026 is in Acapulco, 23 to 29 November. Dates, how to watch and last year's winners: <a href="{href("premier-padel-mexico-major.html")}">Premier Padel Mexico Major 2026</a>. Next season: <a href="{href("premier-padel-2027.html")}">Premier Padel 2027 calendar</a>.</p></div>
<div class="card"><h3>Play like the pros</h3><p>Learn the overheads you see on the tour in <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora vs smash</a> and the <a href="{href("shots.html")}">shot library</a>.</p></div>
<div class="card"><h3>Know your own level</h3><p>Answer a few questions in the <a href="{href("level-calculator.html")}">level calculator</a> to see where you sit on the 1 to 7 club scale.</p></div>
<div class="card"><h3>Run your own ranking</h3><p>Keep a club or friends ranking with the <a href="{href("ladder.html")}">padel ladder tracker</a>, or run a social night with the <a href="{href("americano.html")}">Americano generator</a>.</p></div>
</div>
<div class="sh" style="margin-top:28px" id="calendar-2027"><h2>Which pro padel events are confirmed for 2027?</h2></div>
<div class="card"><p>The Premier Padel 2027 calendar has not been published yet (checked 28 Nov 2026); the 2026 calendar was announced in December 2025. The new team event, the <strong>Hexagon World Series</strong> (eight teams, run with FIP), has confirmed its 2027 season:</p>
<div class="tbl"><table><thead><tr><th>Dates</th><th>Event</th><th>Place</th></tr></thead><tbody>
<tr><td>21 to 24 Jan 2027</td><td>Hexagon Cup Madrid (season opener)</td><td>Caja Mágica, Madrid, Spain</td></tr>
<tr><td>March 2027</td><td>Hexagon World Series</td><td>North America, city to be announced</td></tr>
<tr><td>June 2027</td><td>Hexagon World Series</td><td>Scandinavia, city to be announced</td></tr>
<tr><td>21 to 24 Oct 2027</td><td>Hexagon World Series finale</td><td>Abu Dhabi, UAE</td></tr>
</tbody></table></div>
<p class="muted" style="margin:10px 0 0;font-size:.9rem">Sources: FIP news (12 Aug 2026 and 21 Oct 2026 Hexagon World Series releases) and SportCal (Madrid dates). We will add Premier Padel 2027 dates when FIP and Premier Padel publish them.</p></div>
<div class="sh" style="margin-top:28px"><h2>When are the Premier Padel Finals 2026?</h2></div>
<div class="card"><p>The 2026 Premier Padel Finals are on <strong>10 to 13 December 2026</strong> at the <strong>Palau Sant Jordi in Barcelona</strong>. The top 16 men and women in the FIP Race qualify, and the winners get 1,500 ranking points. Published sessions: Thursday 10 December (13:00 and 17:00), Friday 11 December (13:00), Saturday 12 December (11:00) and Sunday 13 December (11:00).</p>
<p>Tickets are sold per session and the price depends on the zone. Children under 6 go free with a child ticket, and children aged 6 to 14 get 50% off (Premier Padel ticket page). We will update the top 10 above after the Finals.</p>
<p class="muted" style="margin:0;font-size:.9rem">Dates and venue: Premier Padel "Tour Finals" page and the Palau Sant Jordi event page, both checked 26 Nov 2026.</p></div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 25 Nov 2026. Top 10 tables: FIP ranking of 23 Nov 2026 as published by Padel Addict ("Ranking FIP y RACE 2026", 23 Nov 2026) and Padel Speak ("FIP Ranking 2026", updated 23 Nov 2026); both list the same names and points. Ranking rules: FIP "Ranking System and Points Breakdown" (best 22 results, 52-week point defence, FIP Race), LTA Padel "Your guide to Premier Padel" (17 Apr 2026: points per round, Finals 1,500, best 22 in a rolling 52 weeks), Padel Addict and Padel Magazine (10 Nov 2026) for the Race and the top 16 going to the Finals in Barcelona. 2026 points table also matches the old values shown on Premier Padel's 2027 table. Platinum and Gold title points: FIP announcement of the 2025 ranking points (17 Jan 2025). 2027 changes: Premier Padel and FIP "2027 changes to support player welfare" (10 Jun 2026). We have no link with FIP or Premier Padel. Player names only; no photos.</p></div></section>'''
rk_faq = [
    ("Who is the best padel player in the world?", f"In the FIP ranking of {RK_DATE}, Arturo Coello and Agustín Tapia share men's number 1 with 20,211 points, and Gemma Triay and Delfina Brea share women's number 1 with 15,831 points."),
    ("How does the padel ranking work?", "The FIP ranking adds up each player's best 22 results in Premier Padel and CUPRA FIP Tour events over a rolling 52 weeks. Points from a year ago drop off and are replaced by the result from the same week this year."),
    ("How many points is a padel Major worth?", "Winning a Major is worth 2,000 FIP points. The runner-up gets 1,200, semi-finalists 720 and quarter-finalists 360 in 2026."),
    ("How many points do you get for winning a P1 or P2?", "A P1 title is worth 1,000 points and a P2 title 600 points. The runners-up get 600 at a P1 and 360 at a P2."),
    ("What is the FIP Race in padel?", "The Race counts only results from the current year, using each player's best 22. The top 16 in the Race qualify for the season-ending Premier Padel Finals."),
    ("Why do padel partners have the same ranking points?", "Points are won by each player, but partners who play the same events together win the same points, so they often end up level and share a ranking place."),
    ("Is the FIP ranking the same as a Playtomic level?", "No. The FIP ranking is for players in professional tour events. Playtomic and club levels are separate rating systems for everyday players."),
    ("When are the Premier Padel Finals 2026?", "The 2026 Premier Padel Finals are on 10 to 13 December 2026 at the Palau Sant Jordi in Barcelona, with the top 16 in the FIP Race playing."),
    ("What changes in the padel ranking in 2027?", "From 2027 the ranking counts the best 21 results instead of 22, and quarter-finals and earlier rounds give more points. Titles and finals keep the same points."),
    ("When is the first pro padel event of 2027?", "The Hexagon Cup Madrid, 21 to 24 January 2027 at the Caja Mágica, opens the 2027 Hexagon World Series. The Premier Padel 2027 calendar had not been published as of 28 November 2026."),
]
page("padel-rankings.html", "Padel Rankings 2026: Best Padel Players in the World",
     f"Padel world rankings ({RK_DATE}): men's and women's FIP top 10 with points, how the ranking works, points per event and a free points calculator.",
     rk, rk_faq, "Padel rankings")

# ---------------- PADEL RACKET MATERIALS + LABEL DECODER (25 Nov 2026, competitor watch item 5) ----------------
def mtq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-mt="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
MTQ_RACKET = [
    ("face", "Face (the skin over the core)", [("glass", "Fibreglass"), ("hybrid", "Fibreglass + carbon"), ("carbon", "Carbon"), ("x", "Not stated")], "glass"),
    ("k", "Carbon number on the label", [("none", "None"), ("3", "3K"), ("12", "12K"), ("18", "18K"), ("24", "24K or more"), ("x", "Not stated")], "none"),
    ("core", "Core", [("foam", "Foam"), ("soft", "Soft EVA"), ("med", "Medium EVA"), ("hard", "Hard EVA"), ("multi", "Two layers / mixed"), ("x", "Not stated")], "soft"),
    ("surf", "Surface", [("smooth", "Smooth"), ("sand", "Sandy / gritty"), ("3d", "3D relief"), ("both", "3D + sand"), ("x", "Not stated")], "smooth"),
]
MTQ_YOU = [
    ("lvl", "Your level", [("new", "New or under 1 year"), ("mid", "Improving, plays weekly"), ("adv", "Advanced, plays a lot")], "new"),
    ("arm", "Do your elbow, wrist or shoulder get sore?", [("no", "No"), ("yes", "Sometimes")], "no"),
]
MT_GO = {"round": go("padel-round-rackets"), "teardrop": go("padel-teardrop-rackets"), "diamond": go("padel-diamond-rackets"), "all": go("padel-rackets")}
MT_SVG = '''<svg viewBox="0 0 360 250" role="img" aria-label="Cut-away drawing of a padel racket head: textured surface, face skin, foam core, second face skin and the hollow frame" style="width:100%;height:auto;display:block">
<rect x="0" y="0" width="360" height="250" rx="18" fill="#0e2468"/>
<g font-family="Onest, sans-serif" font-size="12" fill="#dfe8ff">
<rect x="24" y="34" width="210" height="10" rx="4" fill="#d4f53c"/>
<g fill="#0b1530">''' + "".join(f'<circle cx="{30 + i * 10}" cy="39" r="1.6"/>' for i in range(21)) + '''</g>
<text x="246" y="43">Surface texture</text>
<rect x="24" y="52" width="210" height="18" rx="4" fill="#9cc4ea"/>
<path d="M24 61h210" stroke="#5f8fd0" stroke-dasharray="6 4"/>
<text x="246" y="65">Face skin</text><text x="246" y="80" font-size="10.5" fill="#9fb0e0">fibreglass or carbon</text>
<rect x="24" y="78" width="210" height="74" rx="6" fill="#ffffff" opacity=".9"/>
<g fill="#0e2468" opacity=".25">''' + "".join(f'<circle cx="{40 + (i % 9) * 23}" cy="{92 + (i // 9) * 22}" r="{5 if i % 2 else 3}"/>' for i in range(27)) + '''</g>
<text x="246" y="112">Core</text><text x="246" y="127" font-size="10.5" fill="#9fb0e0">EVA rubber or foam</text>
<rect x="24" y="160" width="210" height="18" rx="4" fill="#9cc4ea"/>
<path d="M24 169h210" stroke="#5f8fd0" stroke-dasharray="6 4"/>
<text x="246" y="173">Face skin</text>
<rect x="24" y="186" width="210" height="10" rx="4" fill="#d4f53c"/>
<rect x="24" y="208" width="210" height="22" rx="11" fill="none" stroke="#e8f84a" stroke-width="3"/>
<rect x="30" y="213" width="198" height="12" rx="6" fill="#ffffff" opacity=".35"/>
<text x="246" y="219">Frame</text><text x="246" y="234" font-size="10.5" fill="#9fb0e0">hollow tube, often carbon</text>
<text x="24" y="22" font-size="11" fill="#9fb0e0">Side view of the racket head, cut open (not to scale)</text>
</g></svg>'''
mt = f'''<header class="hero"><div class="wrap"><h1>Padel racket materials: carbon, fibreglass, EVA and foam explained</h1>
<p class="lead">Racket labels are full of words like 3K carbon, hard EVA and 3D rough face. Put in what the label says and see what it means for comfort, power and spin. Compare two rackets side by side.</p>
{quick("A padel racket has a foam core (EVA rubber or softer foam) inside two face skins (fibreglass, carbon or a mix), with a hollow frame. Fibreglass faces and soft cores feel softer and more forgiving and suit most beginners. Carbon faces and hard EVA cores feel stiffer and give more power on fast swings but forgive less. Numbers like 3K, 12K and 18K only describe the carbon weave, usually of the outer layer, so don't choose by them.")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="mt">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:8px">Racket label decoder</h2>
<div class="dim-bar"><span class="muted" style="font-weight:600">Editing</span><div class="seg" id="mt-which" role="group" aria-label="Which racket you are editing"><button type="button" data-v="a" aria-pressed="true">Racket A</button><button type="button" data-v="b" aria-pressed="false">Racket B</button></div></div>
<p class="muted" style="margin:10px 0 6px;font-size:.92rem">Read the shop page or the frame. If a word is missing, pick "Not stated".</p>
{"".join(mtq(*x) for x in MTQ_RACKET)}
<h2 style="font-size:1.3rem;margin:18px 0 4px">About you</h2>
{"".join(mtq(*x) for x in MTQ_YOU)}
<p class="muted" style="margin:0;font-size:.92rem">Bars are our rough guide from racket guides and shops, not lab tests. Shape, weight and balance change feel too. Your answers are saved on this device.</p>
</div>
<aside class="result" id="mt-out" aria-live="polite"><h2 id="mt-h">What the label means</h2><p id="mt-p"></p><div id="mt-bars"></div><ul class="b-why" id="mt-why"></ul><p id="mt-next"></p><p class="wr-src">Try a demo racket before you buy: feel beats any label.</p></aside>
</div></section>
<script>window.MTGO={json.dumps(MT_GO)};</script>
{AD.format("materials-mid")}
<section><div class="wrap"><div class="sh"><h2>What is a padel racket made of?</h2><p class="muted">Every padel racket is built in layers. There are no strings.</p></div>
<div class="grid" style="align-items:start;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr))">
<div class="card" style="padding:14px">{MT_SVG}</div>
<div class="card"><ul style="margin:0;padding-left:18px;line-height:1.7">
<li><strong>Core:</strong> the thick middle, made of EVA rubber or a softer foam. It decides most of the soft or hard feel.</li>
<li><strong>Face skins:</strong> thin sheets on both sides, made of fibreglass, carbon or both.</li>
<li><strong>Surface:</strong> the top finish. Smooth, gritty (sand) or with raised 3D bumps for spin.</li>
<li><strong>Frame:</strong> a hollow tube around the head and handle, often carbon.</li>
<li><strong>Holes:</strong> they make the racket lighter and easier to swing.</li>
</ul></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Carbon or fibreglass: which padel racket face is better?</h2><p class="muted">Neither is better for everyone. It depends on your level and your arm.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Fibreglass</th><th scope="col">Fibreglass + carbon</th><th scope="col">Carbon</th></tr></thead><tbody>
<tr><td>Feel</td><td>Softer, more flex</td><td>In between</td><td>Stiffer, more direct</td></tr>
<tr><td>Forgives mis-hits</td><td>Most</td><td>Medium</td><td>Least</td></tr>
<tr><td>Power on fast swings</td><td>Less</td><td>Medium</td><td>More</td></tr>
<tr><td>Vibration to the arm</td><td>Less</td><td>Medium</td><td>More</td></tr>
<tr><td>Wear</td><td>Can wear faster with heavy use</td><td>Medium</td><td>Usually lasts longer</td></tr>
<tr><td>Price</td><td>Usually cheaper</td><td>Mid range</td><td>Usually costs more</td></tr>
<tr><td>Often suits</td><td>Beginners, sore arms</td><td>Improving players</td><td>Experienced, hard hitters</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Racket guides agree on the direction. How big the difference feels depends on the whole racket, especially the core.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What do 3K, 12K and 18K mean on a padel racket?</h2></div>
<div class="grid">
<div class="card"><span class="pill b">The number</span><h3 style="margin-top:10px">K means thousands of fibres</h3><p>Carbon is woven from bundles of very thin fibres. 3K means about 3,000 fibres per bundle, 12K about 12,000 and 18K about 18,000.</p></div>
<div class="card"><span class="pill b">The layer</span><h3 style="margin-top:10px">Usually only the top sheet</h3><p>A racket face has several layers. The K number on the label usually names the outer, visible layer, not the whole face.</p></div>
<div class="card"><span class="pill a">The catch</span><h3 style="margin-top:10px">Guides don't agree on feel</h3><p>Some shops say a higher K feels stiffer. Others say 18K feels softer and springier than 3K. A detailed tech guide says K on its own has little direct effect on play.</p></div>
<div class="card"><span class="pill i">What to do</span><h3 style="margin-top:10px">Judge the whole racket</h3><p>Look at the core, shape, weight and balance first. Two 12K rackets can feel very different. A higher number is not a higher level.</p></div>
</div>
<div class="card" style="padding:8px 24px;overflow-x:auto;margin-top:16px"><table class="mt mt-plain"><thead><tr><th scope="col">Label</th><th scope="col">What it tells you</th><th scope="col">What it doesn't tell you</th></tr></thead><tbody>
<tr><td>3K</td><td>Fine carbon weave, common on the outer layer</td><td>That the racket is soft or hard</td></tr>
<tr><td>12K</td><td>A thicker weave, very common on mid and high-end rackets</td><td>How much carbon is inside</td></tr>
<tr><td>18K</td><td>An even thicker weave</td><td>That it is better than 12K</td></tr>
<tr><td>24K and up</td><td>The thickest weaves</td><td>That it is worth the higher price</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>EVA or foam: which core should I pick?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Core</th><th scope="col">How it feels</th><th scope="col">Good for</th><th scope="col">Watch out</th></tr></thead><tbody>
<tr><td>Foam</td><td>Very soft, ball leaves easily</td><td>Beginners, sore arms, slow swings</td><td>Less punch on smashes; less common now</td></tr>
<tr><td>Soft EVA</td><td>Soft and comfortable, absorbs shock</td><td>Most beginners and many improving players</td><td>Less control on very hard hits</td></tr>
<tr><td>Medium EVA</td><td>A mix of comfort and firmness</td><td>Improving all-round players</td><td>Names like "medium" vary by brand</td></tr>
<tr><td>Hard EVA</td><td>Firm, stiff, lively at high speed</td><td>Strong players with fast, clean swings</td><td>Forgives less; harder on the arm</td></tr>
<tr><td>Two layers / mixed</td><td>Brands mix densities to blend comfort and power</td><td>Players who want a bit of both</td><td>Check reviews for the real feel</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">EVA and foam slowly compress with use, which is one reason an old racket can feel "dead". Test yours with the <a href="{href("racket-care.html")}">racket health check</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Does a rough padel racket give more spin?</h2></div><div class="grid">
<div class="card"><span class="pill i">Yes, a little</span><h3 style="margin-top:10px">Grip on the ball</h3><p>A rough face holds the ball a fraction longer, which helps slice on bandejas, víboras and chiquitas. Technique still makes most of the spin.</p></div>
<div class="card"><span class="pill b">Sand</span><h3 style="margin-top:10px">Gritty finish</h3><p>Sand or grit mixed into the top layer. It grips well when new. One racket shop notes the grit can wear smooth over time.</p></div>
<div class="card"><span class="pill b">3D</span><h3 style="margin-top:10px">Raised bumps</h3><p>A pattern moulded into the face. The same shop says it keeps its texture longer than sand. Some rackets use both.</p></div>
<div class="card"><span class="pill a">Smooth</span><h3 style="margin-top:10px">Clean contact</h3><p>Smooth faces favour flat, controlled shots. For a beginner learning to hit cleanly, smooth or a light texture is fine.</p></div>
</div>
<p class="muted" style="margin-top:14px">Learn the spin shots on <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which racket materials suit my level?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">You are</th><th scope="col">Face</th><th scope="col">Core</th><th scope="col">Surface</th></tr></thead><tbody>
<tr><td>New to padel</td><td>Fibreglass</td><td>Soft EVA or foam</td><td>Any; smooth is fine</td></tr>
<tr><td>Improving, playing every week</td><td>Fibreglass or a carbon mix</td><td>Soft or medium EVA</td><td>Light texture helps spin</td></tr>
<tr><td>Advanced, attacking</td><td>Carbon</td><td>Medium or hard EVA</td><td>Rough for spin</td></tr>
<tr><td>Sore elbow, wrist or shoulder</td><td>Fibreglass or soft carbon mix</td><td>Soft EVA or foam</td><td>Any</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">General advice from racket guides, in our own words. Match the shape and weight too with the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Find your racket</h3><p>Answer five questions in the <a href="{href("racket-finder.html")}">racket finder</a> to get the shape, weight and balance for your game.</p></div>
<div class="card"><h3>Read weight and balance</h3><p>Decode the grams and the balance point with the <a href="{href("racket-balance.html")}">weight and balance decoder</a>.</p></div>
<div class="card"><h3>Ready to upgrade?</h3><p>See what changes from a first racket in the <a href="{href("intermediate-padel-racket.html")}">intermediate racket check</a>, or good value picks in <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop rackets by shape</h3><p>Pick a shape first, then check the face, core and surface in the product details against your result above.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 25 Nov 2026: Padel Browser "Padel racket carbon 3K, 12K, 18K explained" (16 Jun 2026: K = thousands of filaments per thread, describes the top sheet only, higher K is not always stiffer, core matters more than weave), Tennis Warehouse University "Carbon layup" (15 Jul 2025: K = filaments per tow, label usually names the visible layer, K has little direct effect on performance; frame is a carbon tube filled with foam), STIGA "How to choose a padel racket" (carbon stiffer and longer lasting, fibreglass softer, cheaper, can wear faster; soft vs hard EVA; EVA can compress; rough faces help spin, smooth for control), Justpadel "Difference between padel racket materials" (carbon stiffer, smaller sweet spot; fibreglass more elastic and forgiving; soft vs hard EVA; foam very soft, less durable, less common), Zona de Padel "Padel rackets with more roughness" (30 Jul 2024: roughness adds spin; multi-density EVA cores), Padel Racket ID "Sand, 3D and hybrid surfaces" (23 Aug 2023: sand texture wears, 3D relief lasts longer; single retailer, so labelled). The sources disagree on whether higher K feels stiffer or softer, so we say so and don't score it. Decoder bars are our own estimate.</p></div></section>'''
mt_faq = [
    ("Is carbon or fibreglass better for a padel racket?", "Neither is better for everyone. Fibreglass is softer, more forgiving and usually cheaper, which suits beginners and sore arms. Carbon is stiffer and gives more power on fast swings, which suits experienced players."),
    ("What does 3K, 12K or 18K mean on a padel racket?", "It is the number of carbon fibres in each woven bundle: about 3,000, 12,000 or 18,000. It usually describes only the outer layer of the face, so it says little about how the whole racket plays."),
    ("Is 18K carbon better than 12K or 3K?", "Not by itself. Racket guides disagree on whether a higher K feels stiffer or softer, and a detailed tech guide says the K number has little direct effect. The core, shape, weight and balance matter more."),
    ("What is EVA in a padel racket?", "EVA is a rubbery foam used for the core of most padel rackets. Soft EVA feels comfortable and forgiving; hard EVA feels firm and gives more power to fast, clean swings."),
    ("Is a soft or hard padel racket better for beginners?", "Soft. A soft EVA or foam core with a fibreglass face is easier on the arm and forgives mis-hits while you learn."),
    ("Do rough padel rackets give more spin?", "A little. A rough or 3D face grips the ball slightly longer, which helps slice. Technique makes most of the spin. Sandy finishes can wear smoother over time."),
    ("Which padel racket material is best for tennis elbow?", "Racket guides usually suggest a soft core (soft EVA or foam), a fibreglass or soft mixed face, a lighter weight and a low balance. See a doctor or physio if pain lasts."),
]
page("padel-racket-materials.html", "Padel Racket Materials: Carbon vs Fibreglass, 3K to 18K",
     "Padel racket materials explained: carbon vs fibreglass faces, what 3K, 12K and 18K mean, soft vs hard EVA vs foam cores, and a free label decoder.",
     mt, mt_faq, "Racket materials")


exec((ROOT / "courts.py").read_text())
exec((ROOT / "improve.py").read_text())
exec((ROOT / "skills.py").read_text())
exec((ROOT / "demand.py").read_text())

urls = ["index.html", "cheap-padel-rackets.html", "padel-black-friday.html", "racket-finder.html", "score.html", "rules.html", "shots.html", "beginners.html", "glossary.html", "americano.html", "court-dimensions.html", "level-calculator.html", "golden-point-star-point.html", "positioning.html", "serve-rules.html", "warm-up.html", "padel-balls.html", "wall-rules.html", "padel-vs-tennis-vs-pickleball.html", "racket-balance.html", "round-robin.html", "padel-shoes.html", "padel-calories.html", "ladder.html", "net-rules.html", "racket-care.html", "drills.html", "king-of-the-court.html", "tie-break.html", "out-of-court-play.html", "padel-injuries.html", "padel-grip.html", "bandeja-vs-vibora.html", "intermediate-padel-racket.html", "padel-gifts.html", "padel-equipment.html", "padel-racket-for-kids.html", "padel-court-cost.html", "padel-lessons.html", "padel-rankings.html", "padel-racket-materials.html"] + COURT_PAGES + IMPROVE_PAGES + SKILL_PAGES + DEMAND_PAGES + ["about.html", "privacy.html"]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{canon(u)}</loc><lastmod>{UPDATED}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if u == 'index.html' else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
if not (ROOT / "ads.txt").exists():
    (ROOT / "ads.txt").write_text("google.com, pub-1558743317014653, DIRECT, f08c47fec0942fa0\n")
print("built", len(urls) + 1, "pages", "(preview)" if PREVIEW else "(live)")
write_redirects(ROOT)

# --- honest sitemap: every indexable page, lastmod only when content changes (seo_post.py, 26 Nov) ---
import subprocess as _sp, sys as _sys, pathlib as _pl
_sp.run([_sys.executable, str(_pl.Path(__file__).resolve().parent / "seo_post.py"), str(_pl.Path(__file__).resolve().parent), DOMAIN])
