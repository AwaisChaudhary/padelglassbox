#!/usr/bin/env python3
"""Builds the padel site. `python3 build.py` = live (clean URLs). `python3 build.py --preview` = local files."""
import json, html, pathlib, sys, hashlib

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
}
# ---- Affiliate links. Pages link to /go/<slug>; _redirects sends it to the store.
# Until a programme approves us these are plain store URLs; when approved, replace the URL with the tracked link and rebuild.
AFF_ATTR = 'rel="sponsored nofollow noopener" target="_blank"'
AFF_NOTE = '<p class="aff-note">We may earn a commission if you buy through these links, at no extra cost to you.</p>'
def go(slug): return "/go/" + slug
# Quick answer box (standing AI-answers rule in README)
def quick(txt):
    return f'<div class="qa"><b>Quick answer</b><p>{txt}</p><span>Last updated {e(UPDATED)}</span></div>'

def write_redirects(root):
    lines = "".join(f"/go/{k} {v} 302\n" for k, v in AFF.items())
    (root / "_redirects").write_text(lines)


def page(file, title, desc, body, faqs=None, crumb=None):
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
<meta name="twitter:card" content="summary"><meta name="theme-color" content="#0e2468">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231747c9'/%3E%3Ccircle cx='16' cy='16' r='8' fill='%23d4f53c'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800&family=Onest:wght@400;600;700&display=swap" rel="stylesheet">
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
{body}
{faq_html(faqs)}
{signup(file)}
{AD.format(file)}
</main>
<footer><div class="wrap"><div class="fgrid">
<div><a class="brand" href="{href("index.html")}" style="color:#fff">{LOGO}Padel <b style="color:#e8f84a">Glass Box</b></a><p style="margin-top:12px">Free padel tools and plain-English guides: find your racket, keep score, learn the rules and the shots.</p></div>
<div><strong style="color:#fff">Tools and guides</strong><ul>{"".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in NAV)}<li><a href="{href("glossary.html")}">Glossary</a></li><li><a href="{href("americano.html")}">Americano generator</a></li><li><a href="{href("court-dimensions.html")}">Court dimensions</a></li><li><a href="{href("level-calculator.html")}">Level calculator</a></li><li><a href="{href("golden-point-star-point.html")}">Golden point vs Star Point</a></li><li><a href="{href("serve-rules.html")}">Serve rules and checker</a></li><li><a href="{href("positioning.html")}">Where to stand</a></li><li><a href="{href("warm-up.html")}">Warm-up timer</a></li><li><a href="{href("padel-balls.html")}">When to change balls</a></li><li><a href="{href("wall-rules.html")}">Wall and fence rules</a></li><li><a href="{href("padel-vs-tennis-vs-pickleball.html")}">Padel vs tennis vs pickleball</a></li><li><a href="{href("racket-balance.html")}">Racket weight and balance</a></li><li><a href="{href("round-robin.html")}">Round robin generator</a></li><li><a href="{href("padel-shoes.html")}">Padel shoes guide</a></li><li><a href="{href("padel-calories.html")}">Padel calories calculator</a></li><li><a href="{href("ladder.html")}">Padel ladder tracker</a></li><li><a href="{href("net-rules.html")}">Net rules checker</a></li><li><a href="{href("racket-care.html")}">Racket care and health check</a></li><li><a href="{href("drills.html")}">Padel drills planner</a></li><li><a href="{href("king-of-the-court.html")}">King of the Court generator</a></li><li><a href="{href("tie-break.html")}">Tie-break rules and tracker</a></li><li><a href="{href("out-of-court-play.html")}">Out-of-court play rules</a></li><li><a href="{href("padel-injuries.html")}">Padel injuries and prevention</a></li></ul></div>
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
page("index.html", "Padel Racket Finder, Score Keeper and Rules | Padel Glass Box",
     "Free padel tools: find the right racket in a minute, keep score on court with your phone, and learn padel rules and shots in plain English.", home, home_faq)

# ---------------- RACKET FINDER ----------------
def q(name, title, opts):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if i == 0 else "false"}">{lab}</button>' for i, (val, lab) in enumerate(opts))
    return f'<div class="q"><h3>{title}</h3><div class="opts" data-q="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'

finder = f'''<header class="hero"><div class="wrap"><h1>Find your padel racket.</h1>
<p class="lead">Three questions. You'll get the racket shape, balance, weight, core and face material that suit your game, and why.</p></div></header>
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
<section><div class="wrap"><div class="sh"><h2>The 3 racket shapes</h2></div><div class="grid">
<div class="card"><span class="pill b">Most control</span><h3 style="margin-top:10px">Round</h3><p>The sweet spot is large and right in the middle, and the weight sits towards the handle. Forgiving, easy to handle, and the usual first racket. Plenty of top players use them too.</p></div>
<div class="card"><span class="pill i">All-round</span><h3 style="margin-top:10px">Teardrop</h3><p>A mix of round and diamond, with medium balance. More punch than a round racket while still being fairly easy to control.</p></div>
<div class="card"><span class="pill a">Most power</span><h3 style="margin-top:10px">Diamond</h3><p>Weight sits towards the head and the sweet spot is smaller and higher up. Big smashes, but less forgiving, so it suits experienced attackers.</p></div>
</div></div></section>
<section><div class="wrap"><div class="sh"><h2>What the specs mean</h2></div><div class="grid">
<div class="card"><h3>Weight</h3><p>Most adult rackets weigh roughly 345 to 385 g. Heavier rackets hit harder but tire your arm sooner; lighter ones are quicker at the net. New players usually do best under about 360 g.</p></div>
<div class="card"><h3>Balance</h3><p>Measured in mm from the bottom of the handle. Low balance (under about 260 mm) means control and quick hands. High balance (over about 270 mm) means power but more strain. <a href="{href("racket-balance.html")}">Decode and compare two rackets</a>.</p></div>
<div class="card"><h3>Core foam</h3><p>Soft foam gives easy power and comfort at slow speeds. Hard foam gives control when you swing fast.</p></div>
<div class="card"><h3>Face material</h3><p>Fiberglass is softer and forgiving. Carbon is stiffer and more precise, and usually costs more.</p></div>
</div></div></section>
<section style="padding-top:0" id="grip"><div class="wrap"><div class="sh"><h2>Grip and overgrip</h2><p class="muted">The cheapest upgrade you can make to any racket. Looking after the rest of it? See <a href="{href("racket-care.html")}">racket care</a>.</p></div><div class="grid">
<div class="card"><h3>Grip vs overgrip</h3><p>The base grip is the thick, cushioned layer that comes on the handle. An overgrip is a thin, light tape you wrap over it. It protects the base grip, which is harder to replace, and soaks up sweat.</p></div>
<div class="card"><h3>When to change it</h3><p>Change it when it looks dirty or worn, or when it feels slippery, wet or less sticky. Social players often get a few sessions from one. Players who sweat a lot, or play in heat, change it far more often.</p></div>
<div class="card"><h3>How to put one on</h3><p>Take off the old overgrip. Start at the bottom of the handle, by the butt cap, and wrap up towards the head, keeping each turn parallel and slightly overlapping. Cut the end straight and fix it with the finishing tape.</p></div>
<div class="card"><h3>Handle feels too thin?</h3><p>Padel handles often feel small in bigger hands. Overlap the overgrip more as you wrap, or add a second overgrip, to make the handle thicker. Overlap less for a thinner feel.</p></div>
</div></div></section>'''
finder_faq = [
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
<div class="card"><h3>League with fixed pairs</h3><p>Every pair plays every other pair and the table does the maths: <a href="{href("round-robin.html")}">round robin generator</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Pick a deuce rule</h3><p>See all three side by side in <a href="{href("golden-point-star-point.html")}">golden point vs Star Point vs advantage</a>.</p></div>
<div class="card"><h3>Settle a call</h3><p>Was that ball in? Check the <a href="{href("wall-rules.html")}">wall rules</a>, <a href="{href("net-rules.html")}">net rules</a> or <a href="{href("serve-rules.html")}">serve rules</a>.</p></div>
<div class="card"><h3>Warm up first</h3><p>Start the match ready with the 10-minute <a href="{href("warm-up.html")}">warm-up timer</a>.</p></div>
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
<div class="card"><h3>A serve is a fault if</h3><p>it lands outside the diagonal box, it's hit above the waist, you miss the ball, your foot touches the line, or after bouncing in the box it hits the metal mesh. Not sure? Use our <a href="{href("serve-rules.html")}">serve checker</a>.</p></div>
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
]
page("rules.html", "Padel Rules Explained Simply, With an Interactive Court | Padel Glass Box",
     "Padel rules in plain English: the underhand serve, walls, net, faults, scoring, tie-breaks and changing ends, plus an interactive court you can tap to learn each part.", rules, rules_faq, "Rules")

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
<tr><td>1. First weeks</td><td>Volley, lob (globo)</td><td>The lob gets you to the net; the volley keeps you there.</td></tr>
<tr><td>2. Playing regular matches</td><td>Bandeja, chiquita, contrapared, drop shot</td><td>Safe ways to keep the net and to escape when you are pushed back.</td></tr>
<tr><td>3. Strong club level</td><td>Víbora, bajada, rulo, smash</td><td>Attacking shots. Play them when the ball is right, not every time.</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What makes padel shots different from tennis?</h2></div><div class="grid">
<div class="card"><h3>Shorter swings</h3><p>The court is small and the ball comes back off the glass, so compact swings and control beat raw power.</p></div>
<div class="card"><h3>Let it come off the glass</h3><p>Many balls are easier after the back glass. Wait for the rebound instead of rushing. The <a href="{href("wall-rules.html")}">wall rules checker</a> shows what is in and out.</p></div>
<div class="card"><h3>Overheads that keep the net</h3><p>The bandeja and víbora are not smashes. Their job is to keep your team at the net, so placement matters more than pace.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
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
     "Every key padel shot explained simply, with animated ball paths and the order to learn them: volley, lob, bandeja, chiquita, contrapared, víbora, rulo, bajada and smash.", shots, shots_faq, "Shots")

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
<div class="card"><h3>Booking apps</h3><p>Many clubs list their courts on booking apps such as Playtomic, where you can also find open matches at your level.</p></div>
<div class="card"><h3>National federations</h3><p>Your country's padel or tennis federation usually lists clubs and beginner sessions. In the UK, that's LTA Padel.</p></div>
<div class="card"><h3>Join a social night</h3><p>Many clubs run Americano evenings where you change partner each round. They are a friendly way to meet players at your level. Running one yourself? Use our <a href="{href("americano.html")}">Americano generator</a>.</p></div>
<div class="card"><h3>Practise between matches</h3><p>A short practice once a week speeds things up. The <a href="{href("drills.html")}">drills planner</a> builds a 20 to 60 minute session with a timer.</p></div>
<div class="card"><h3>Know your level</h3><p>Open matches and clubs often ask for your level. Our <a href="{href("level-calculator.html")}">padel level calculator</a> gives you a quick estimate.</p></div>
<div class="card"><h3>Know where to stand</h3><p>Move up and back with your partner, and stay about 1 metre off the back glass. Our <a href="{href("positioning.html")}">positioning guide</a> shows every situation on a court.</p></div>
<div class="card"><h3>Warm up first</h3><p>Ten minutes of jogging, moving stretches and soft rallies makes the first games easier on your body. Our <a href="{href("warm-up.html")}">warm-up timer</a> talks you through it step by step.</p></div>
<div class="card"><h3>Coming from tennis or pickleball?</h3><p>Your hands will help, but the walls, the underhand serve and the scoring work a little differently. See <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a> for the key changes.</p></div>
<div class="card"><h3>Pick the right shoes</h3><p>Grip matters more than looks. A herringbone sole suits most sandy courts, and running shoes slip. Our <a href="{href("padel-shoes.html")}">padel shoe finder</a> tells you which sole to look for.</p></div>
<div class="card"><h3>Is it a good workout?</h3><p>An hour of padel burns roughly 400 to 600 kcal for an average adult. Work out your own number with the <a href="{href("padel-calories.html")}">padel calories calculator</a>.</p></div>
<div class="card"><h3>Start with a lesson</h3><p>One group lesson teaches the serve and the walls much faster than working it out alone.</p></div>
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
<div class="card"><h3>Keep score</h3><p>Not sure how scoring works? Use the free <a href="{href("score.html")}">score keeper</a> on your phone.</p></div>
<div class="card"><h3>Find your racket</h3><p>Three questions and you'll know the shape and weight to look for: <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
<div class="card"><h3>Learn the rules</h3><p>Tap any part of the <a href="{href("rules.html")}">interactive rules court</a>.</p></div>
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
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Learn the rules</h3><p>Tap any part of the <a href="{href("rules.html")}">interactive rules court</a>.</p></div>
<div class="card"><h3>Find your side</h3><p>Drive or revés? Read <a href="{href("positioning.html")}">where to stand</a>.</p></div>
<div class="card"><h3>New to padel?</h3><p>Start with the <a href="{href("beginners.html")}">first match checklist</a>.</p></div>
</div></div></section>'''
glos_faq = [
    ("How do you pronounce bandeja in padel?", "Say ban-DEH-ha. The Spanish j sounds like the h in hat. Bandeja means tray, because you hold the racket face up like a waiter's tray."),
    ("How do you pronounce víbora?", "Say VEE-bo-ra, with the stress on the first part. In Spanish the v sounds close to a soft b, so you will also hear BEE-bo-ra."),
    ("What does mía and tuya mean in padel?", "Mía means mine and tuya means yours. Partners shout them to say who will take a ball down the middle."),
    ("What is the difference between a bandeja and a víbora?", "Both are overheads played from near the net. A bandeja is flatter and controlled to keep your place at the net; a víbora has more sidespin and speed and is more attacking."),
    ("What does malla mean in padel?", "Malla is the metal mesh fence around the sides of the court. Balls that hit it bounce unpredictably, and you can't play off your own fence."),
    ("What are drive and revés in padel?", "Drive is the player on the right side of the court and revés is the player on the left. In Spanish the words also mean forehand and backhand."),
]
page("glossary.html", "Padel Glossary: Terms, Spanish Pronunciation and Meanings | Padel Glass Box",
     "Padel terms explained in plain English, with how to say the Spanish words: bandeja, víbora, chiquita, bajada, malla, golden point, drive, revés and more. Searchable and free.", glos, glos_faq, "Glossary")

# ---------------- AMERICANO / MEXICANO GENERATOR ----------------
def pts_opts():
    return "".join(f'<button class="opt" type="button" data-v="{p}" aria-pressed="{"true" if p == 24 else "false"}">{p} points</button>' for p in (16, 21, 24, 32))
amer = f'''<header class="hero"><div class="wrap"><h1>Americano and Mexicano draw maker.</h1>
<p class="lead">Type in your players, pick a format and get every round with partners and courts. Enter the points after each match and the leaderboard updates live. Free, no sign-up, saved on this device.</p></div></header>
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
<section><div class="wrap"><div class="sh"><h2>How the two formats work</h2></div><div class="grid">
<div class="card"><h3>Americano</h3><p>You change partner every round. The aim is that you play with, and against, as many different people as possible. Nobody is knocked out.</p></div>
<div class="card"><h3>Mexicano</h3><p>Round one is random. After that, each round is made from the leaderboard, so players with similar scores meet. A common way, used here, is 1st and 4th against 2nd and 3rd on the top court, then the next four, and so on.</p></div>
<div class="card"><h3>Points, not games</h3><p>Each match is a fixed number of points, such as 24. Every point counts, even if your team loses: lose 10-14 and you still add 10 to your total. The player with the most points at the end wins.</p></div>
<div class="card"><h3>Serving</h3><p>A simple rule many clubs use: each player serves a block of points (often four in a row for 16, 24 or 32 points), then the serve passes to the other team. Agree the rule before you start.</p></div>
<div class="card"><h3>Odd numbers of players</h3><p>It works best with 4, 8, 12 or 16 players. With other numbers, some players sit out each round. This tool spreads the rests as evenly as it can, and the leaderboard shows points per match so it stays fair.</p></div>
<div class="card"><h3>Want more competition?</h3><p>Try <a href="{href("king-of-the-court.html")}">King of the Court</a>: winners move up a court, losers move down, and everyone fights for court 1.</p></div>
<div class="card"><h3>Playing in fixed pairs?</h3><p>If teams want to keep the same partner all night, use the <a href="{href("round-robin.html")}">round robin generator</a>: every pair plays every other pair, with a standings table.</p></div>
<div class="card"><h3>How long it takes</h3><p>A 24-point match often takes around 10 to 15 minutes, and 32 points a bit longer. Seven rounds of 24 points fits a typical two-hour court booking with time for changes.</p></div>
</div></div></section>'''
amer_faq = [
    ("What is an Americano in padel?", "A social format where you change partner every round and play a set number of points per match. Each player keeps the points they win, and the highest total at the end wins."),
    ("What is the difference between Americano and Mexicano?", "In Americano the partners are planned in advance so everyone mixes. In Mexicano each new round is built from the current scores, so players of a similar level end up playing together."),
    ("How many players do you need for an Americano?", "At least four. Multiples of four (8, 12, 16) fill every court in every round. Other numbers work too, with a few players resting each round."),
    ("How many points per match in an Americano?", "Clubs often use 16, 21, 24 or 32. Fewer points means quicker matches and more rounds in the same court time."),
    ("Do you need an app to run an Americano?", "No. This page makes the draw, keeps the scores and shows the leaderboard in your browser. It saves on your device, so you can close it and come back."),
]
page("americano.html", "Padel Americano and Mexicano Generator: Free Draw and Leaderboard | Padel Glass Box",
     "Free padel Americano and Mexicano generator. Enter player names, get every round with partners and courts, type in the points and see a live leaderboard.", amer, amer_faq, "Americano generator")

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
<div class="card"><h3>Smaller than a tennis court</h3><p>At 20 m by 10 m, the court is about three quarters the area of a tennis doubles court (23.77 m by 10.97 m), and there is no run-off space behind the walls. You rarely sprint far, which is a big reason padel feels easy to start. See all three sports to scale on our <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a> page.</p></div>
<div class="card"><h3>A short back area</h3><p>Only about 3 m sits behind the service line. Balls reach the back glass quickly, so learning to let the ball come off the wall matters early.</p></div>
<div class="card"><h3>A low net</h3><p>The net is lower than in tennis, and dips a little in the middle. Low, flat balls over the centre are the safest way to keep the ball in play.</p></div>
<div class="card"><h3>Where the glass steps down</h3><p>The side glass is tallest near the back walls. Balls that hit the mesh act differently from glass, which you can read about on our <a href="{href("wall-rules.html")}">wall and fence rules</a> page.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>The net</h3><p>Can you touch it or reach over it? Check the <a href="{href("net-rules.html")}">net rules checker</a>.</p></div>
<div class="card"><h3>Where to stand</h3><p>Use the measurements in play with the <a href="{href("positioning.html")}">positioning court</a>.</p></div>
<div class="card"><h3>The serve</h3><p>The service box in action: the <a href="{href("serve-rules.html")}">serve checker</a>.</p></div>
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
page("court-dimensions.html", "Padel Court Dimensions: Interactive Measured Diagram (m and ft) | Padel Glass Box",
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
<p class="lead">Answer seven quick questions about your game. You get an estimated level from 1 to 7, what it means, and the one thing to work on next. Free and private: your answers stay on this device.</p></div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="lvquiz">
<div class="card">
{"".join(lvq(*x) for x in LVQ)}
<div class="btns" style="margin-top:0"><button class="btn ghost sm" type="button" id="lv-reset">Clear my answers</button></div>
</div>
<aside class="result" id="lv-result" aria-live="polite"></aside>
</div></section>
{AD.format("level-mid")}
<section><div class="wrap"><div class="sh"><h2>The levels in plain English</h2><p class="muted">A general guide. Each club or app words it a little differently.</p></div><div class="grid">
<div class="card"><span class="pill b">1 to 2.5</span><h3 style="margin-top:10px">Beginner</h3><p>You are learning the serve, the scoring and how the ball comes off the glass. Rallies are short. Most new players move up quickly here.</p></div>
<div class="card"><span class="pill b">3 to 3.5</span><h3 style="margin-top:10px">Improver</h3><p>You can rally, use the back glass on easy balls and move with your partner. Many tennis and squash players start around here.</p></div>
<div class="card"><span class="pill i">4 to 4.5</span><h3 style="margin-top:10px">Intermediate</h3><p>You control the court, play a bandeja, defend the corners and think about tactics. This is a strong club player.</p></div>
<div class="card"><span class="pill a">5 to 5.5</span><h3 style="margin-top:10px">Advanced</h3><p>You play tournaments, build points on purpose and rarely give away easy errors. Ranked players often sit at 5.5 and up.</p></div>
<div class="card"><span class="pill a">6 to 7</span><h3 style="margin-top:10px">Elite</h3><p>Semi-professional and professional players. If this is you, you already know your ranking.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why your level matters</h2></div><div class="grid">
<div class="card"><h3>Better matches</h3><p>Games are most fun when all four players are close in level. Booking apps use levels to suggest open matches for you.</p></div>
<div class="card"><h3>Different scales</h3><p>Not every system is the same. Playtomic uses 0 to 7 and moves your level after each rated match. The LTA in the UK uses 1.0 to 7.0. A 3 in one place may not be a 3 in another.</p></div>
<div class="card"><h3>Your real level comes from results</h3><p>A quiz gives you a starting point. Rated matches, or a coach watching you play, give a truer number over time.</p></div>
<div class="card"><h3>Running a social night?</h3><p>Ask players for a rough level, then use our <a href="{href("americano.html")}">Mexicano generator</a>: it pairs people with similar scores as the night goes on.</p></div>
</div></div></section>'''
lvl_faq = [
    ("What padel level am I?", "Most people who play for fun sit between 1 and 4 on a 1 to 7 scale. Beginners are 1 to 2.5, improvers 3 to 3.5, strong club players 4 to 4.5, and tournament players 5 and up. Answer the questions on this page for your estimate."),
    ("What is a good padel level?", "There is no bad level. As a rough guide, a 3 can enjoy long rallies, a 4 is a solid club player and a 5 plays regular tournaments."),
    ("How does the Playtomic level work?", "Playtomic uses a 0 to 7 scale. You start with a level from a short questionnaire, then it goes up or down based on your rated match results and the level of the players you face."),
    ("Is this calculator an official rating?", "No. It's a free estimate to help you pick games and know what to practise. Clubs, apps and federations each run their own rating systems."),
    ("What level is a tennis player starting padel?", "Many good tennis or squash players start around 3 to 3.5, because they already hit the ball well. Learning the glass and the net game usually takes a few months."),
    ("How do I move up a level?", "Fix the weakest part of your game first, as it costs you the most points. For most players that means getting comfortable with the back glass and learning the bandeja."),
]
page("level-calculator.html", "Padel Level Calculator: What Is My Padel Level (1 to 7)? | Padel Glass Box",
     "Free padel level calculator. Answer 7 quick questions and get your estimated padel level from 1 to 7, what it means, and what to practise next.", lvl, lvl_faq, "Level calculator")

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
<div class="card"><h3>Professional padel</h3><p>The International Padel Federation (FIP) approved Star Point in late 2025. From 2026 it is used on Premier Padel, the FIP Tour, FIP Promises and the FIP Beyond amateur events.</p></div>
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
<p class="lead">Pick a moment in the point and see where all four players should be. Your team is at the bottom: you on the left, your partner on the right.</p></div></header>
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
<section><div class="wrap"><div class="sh"><h2>Five habits of good positioning</h2></div><div class="grid">
<div class="card"><h3>Move as a pair</h3><p>Imagine a rope of about 3 metres between you and your partner. When one moves up, back or across, the other follows. Gaps open when you move on your own.</p></div>
<div class="card"><h3>Win the net</h3><p>Most points are won at the net. Stand about 2 to 2.5 metres from it, close enough to volley and far enough back to reach a lob.</p></div>
<div class="card"><h3>Give the glass room</h3><p>When you defend, stand about 1 metre in front of the back glass. Too close and the ball comes off the glass into your body. Too far forward and lobs beat you.</p></div>
<div class="card"><h3>Shade with the ball</h3><p>Both players slide towards the side the ball is on. The player nearer the ball covers the line, the other covers the middle.</p></div>
<div class="card"><h3>Agree on the middle</h3><p>Balls down the middle cause the most mix-ups. By default the player with the forehand in the middle takes them. Call "mine" or "yours" early.</p></div>
<div class="card"><h3>Reset after a lob</h3><p>If a lob goes over you, both players go back together, play a safe shot, then look for the next chance to move forward again.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Left side or right side?</h2></div><div class="grid">
<div class="card"><span class="pill i">Right side</span><h3 style="margin-top:10px">The drive side</h3><p>For a right-handed player the forehand is on the outside, near the side wall. This player plays more steady, controlled balls and builds the point.</p></div>
<div class="card"><span class="pill a">Left side</span><h3 style="margin-top:10px">The revés side</h3><p>For a right-handed player the forehand is in the middle. This player takes many middle balls and more of the high balls and smashes, so it is often the more attacking role.</p></div>
<div class="card"><span class="pill b">Mixed hands</span><h3 style="margin-top:10px">One right-hander, one left-hander</h3><p>Many pairs put both forehands in the middle: the left-hander on the right side and the right-hander on the left. Try both ways and see what feels natural.</p></div>
</div>
<p class="muted" style="margin-top:14px">New to the shots named here? See the <a href="{href("shots.html")}">shot library</a>. For court measurements, see the <a href="{href("court-dimensions.html")}">court dimensions</a> page.</p>
</div></section>'''
pos_faq = [
    ("Where should I stand at the net in padel?", "About 2 to 2.5 metres from the net, slightly towards your side of the centre line. The player nearer the ball can be a little closer, with the partner half a step back to cover the middle and the lob."),
    ("How far from the back glass should I stand?", "About 1 metre in front of it when you defend or receive. That gives the ball room to come off the glass so you can play it comfortably."),
    ("Why is one up and one back bad in padel?", "It leaves a big diagonal gap between the two players, and opponents can hit through it or at the feet of the net player. Move up and back together instead."),
    ("Who takes the ball down the middle?", "As a default, the player with the forehand in the middle. For two right-handers that is the player on the left. Whoever calls it first should take it."),
    ("Where does the server's partner stand?", "Usually at the net, about 2 metres from it, on the other half of the court. The rules let the server's partner stand anywhere on their side, but a serve that hits them is a fault."),
    ("Should I play on the left or the right side?", "For right-handers, the left side suits players who like to attack and smash, and the right side suits steady players who like control. Both are important."),
]
page("positioning.html", "Padel Positioning: Where to Stand on Court (Interactive) | Padel Glass Box",
     "Where to stand in padel for every moment of the point: serving, receiving, at the net, at the back and after a lob. Tap an interactive court to see all four players.", pos, pos_faq, "Positioning")

# ---------------- SERVE RULES + CHECKER ----------------
def _q(qid, label, opts):
    return f'<div class="q sv-q" data-q="{qid}"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
YN = [("y", "Yes"), ("n", "No")]
serve = f'''<header class="hero"><div class="wrap"><h1>Was that serve legal?</h1>
<p class="lead">Answer a few quick questions about the serve and get the call: good serve, fault or let. Then read every padel serve rule in plain English below.</p></div></header>
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
<section><div class="wrap"><div class="sh"><h2>The padel serve, step by step</h2></div><div class="grid">
<div class="card"><h3>1. Stand in the right place</h3><p>Stand behind the service line, between the centre line and the side wall. Your feet must not touch the service line or the imaginary line that extends the centre line.</p></div>
<div class="card"><h3>2. Bounce the ball</h3><p>Drop the ball and let it bounce once on your side, behind the service line, before you hit it. You may not hit it straight from your hand.</p></div>
<div class="card"><h3>3. Hit at or below the waist</h3><p>Contact must be at or below waist height, so the padel serve is always an underhand serve. Keep at least one foot on the ground: no jump serves.</p></div>
<div class="card"><h3>4. Land it diagonally</h3><p>The ball must cross the net and bounce in the service box diagonally opposite you. A ball that lands on the line is good.</p></div>
<div class="card"><h3>5. The receiver waits for the bounce</h3><p>The receiver must let the serve bounce before playing it. After the bounce the ball may hit the glass and stay in play.</p></div>
<div class="card"><h3>6. Two tries</h3><p>A fault on the first serve gives you a second serve. Two faults in a row is a double fault, and the receivers win the point.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Faults and lets at a glance</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">What happened</th><th scope="col">The call</th></tr></thead><tbody>
<tr><td>Ball hit above the waist</td><td>Fault</td></tr>
<tr><td>Ball not bounced first, or bounced in the wrong place</td><td>Fault</td></tr>
<tr><td>Foot on the service line or centre line</td><td>Fault</td></tr>
<tr><td>Both feet off the ground (jump serve)</td><td>Fault</td></tr>
<tr><td>Server swings and misses</td><td>Fault</td></tr>
<tr><td>Lands outside the diagonal box</td><td>Fault</td></tr>
<tr><td>Lands in the box, then hits the metal fence before a second bounce</td><td>Fault</td></tr>
<tr><td>Hits the server's partner before crossing the net</td><td>Fault</td></tr>
<tr><td>Lands in the box, then hits the glass</td><td>Good, play on</td></tr>
<tr><td>Touches the net, lands in the box, does not touch the fence</td><td>Let: replay that serve</td></tr>
<tr><td>Touches the net, then lands out</td><td>Fault</td></tr>
<tr><td>Served before the receiver was ready (and they did not try to return it)</td><td>Let: replay that serve</td></tr>
<tr><td>Hits the receiver before it bounces</td><td>Point to the serving pair</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">A let replays only that serve. A let on the second serve means you take the second serve again, not two new serves. Calls in the rally are on the <a href="{href("wall-rules.html")}">wall and fence checker</a>, more rules on our <a href="{href("rules.html")}">interactive rules court</a>, and serve tactics on the <a href="{href("positioning.html")}">positioning guide</a>.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Who serves and when</h2></div><div class="grid">
<div class="card"><h3>A whole game each</h3><p>One player serves for the whole game. Then the other pair serves the next game, and so on.</p></div>
<div class="card"><h3>Swap sides every point</h3><p>The server changes side after every point, so each point is served diagonally to the other receiver.</p></div>
<div class="card"><h3>Golden point and Star Point</h3><p>On a deciding point the receiving pair chooses which player receives. See <a href="{href("golden-point-star-point.html")}">how deciding points work</a>.</p></div>
</div></div></section>'''
serve_faq = [
    ("Can you serve overarm in padel?", "No. You must hit the ball at or below waist height after it bounces, so every padel serve is underhand."),
    ("Is it a let if the serve hits the net in padel?", "Yes, if it then lands in the correct box and does not touch the metal fence before bouncing again. If it touches the net and lands out, it is a fault."),
    ("What if the serve hits the fence in padel?", "If the ball bounces in the box and then hits the metal fence before a second bounce, it is a fault. If it hits the glass instead, the ball is in play."),
    ("Does the serve have to bounce in padel?", "Yes. The server must bounce the ball behind the service line before hitting it, and the receiver must let the serve bounce before returning it."),
    ("Can you stand on the line when serving in padel?", "No. Touching the service line or the imaginary extension of the centre line with your foot when you serve is a fault."),
    ("Can you jump when you serve in padel?", "No. At least one foot must be on the ground when you hit the ball."),
    ("How many serves do you get in padel?", "Two. If the first is a fault, you have a second serve. Two faults is a double fault and loses the point."),
]
page("serve-rules.html", "Padel Serve Rules: Is My Serve Legal? Free Serve Checker | Padel Glass Box",
     "Padel serve rules in plain English: where to stand, the bounce, waist height, faults and lets. Use the free serve checker to make the call on any serve.", serve, serve_faq, "Serve rules")

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
<div class="card"><h3>Playing early or in the cold?</h3><p>Choose the 15 minute version. Cold muscles need longer, and the balls feel flatter too. Read <a href="{href("padel-balls.html")}">when to change padel balls</a>.</p></div>
<div class="card"><h3>Warmed up? Now practise</h3><p>Go straight into a planned session with the <a href="{href("drills.html")}">padel drills planner</a> and its timer.</p></div>
<div class="card"><h3>Something hurts?</h3><p>A warm-up is not a fix for an injury. If you feel sharp pain, stop and get advice from a doctor or physiotherapist. See which areas padel players hurt most in the <a href="{href("padel-injuries.html")}">padel injuries guide</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why warm up before padel?</h2></div><div class="grid">
<div class="card"><h3>Padel injuries are mostly muscles and tendons</h3><p>A 2023 review of padel injury studies found that most injuries were to tendons and muscles, with the elbow, knee, shoulder and lower back reported most. Calf strains also appear often.</p></div>
<div class="card"><h3>Not warming up is a known cause</h3><p>NI Direct, the UK government health site for Northern Ireland, lists not warming up properly among the common causes of sports injuries.</p></div>
<div class="card"><h3>Check your other habits</h3><p>Shoes, grip, rest days and technique matter too. Run the two-minute <a href="{href("padel-injuries.html")}#check">injury prevention check</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
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
     "Free padel warm-up timer: a 10 or 15 minute routine step by step, from jogging and moving stretches to volleys, lobs and serves, plus why warming up helps prevent padel injuries.", warm, warm_faq, "Warm-up timer")

# ---------------- PADEL BALLS ----------------
def _bq(qid, label, opts):
    return f'<div class="q bq" data-q="{qid}"><h3>{label}</h3><div class="opts">' + "".join(f'<button class="opt" type="button" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts) + '</div></div>'
balls = f'''<header class="hero"><div class="wrap"><h1>Are your padel balls dead?</h1>
<p class="lead">Six quick checks tell you if a ball is still good for a match, fine for practice, or ready for the bin. Then learn how long padel balls last and how to keep them lively.</p></div></header>
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
<div class="card"><h3>Heat and cold change the feel</h3><p>On a cold day even new balls feel flat. Keep opened cans away from hot cars and cold garages; a cool, dry cupboard is best.</p></div>
<div class="card"><h3>Pressurisers help a little</h3><p>A ball saver tube keeps air in for longer, but it can't fix worn felt or bring a dead ball back to life.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel ball vs tennis ball</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Padel ball</th><th scope="col">Tennis ball</th></tr></thead><tbody>
<tr><td>Diameter</td><td>6.35 to 6.77 cm</td><td>6.54 to 6.86 cm</td></tr>
<tr><td>Weight</td><td>56.0 to 59.4 g</td><td>56.0 to 59.4 g</td></tr>
<tr><td>Pressure inside (new)</td><td>About 11 psi</td><td>About 14 psi</td></tr>
<tr><td>Rule bounce test</td><td>135 to 145 cm when dropped from 2.54 m</td><td>Bounces higher</td></tr>
<tr><td>How it plays</td><td>Slower, softer, made to come off the glass</td><td>Faster and bouncier</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">The two balls look almost the same, but the lower pressure is what makes padel feel like padel. Tennis balls bounce too high off the floor and walls, so use real padel balls. Sizes and pressure from LTA Padel; bounce test as given in the padel rules.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Make your balls last longer</h2></div><div class="grid">
<div class="card"><h3>Close the can</h3><p>Put the lid back on tightly after every game, or use a ball saver.</p></div>
<div class="card"><h3>Keep them dry</h3><p>Don't play with wet balls if you can avoid it, and let them dry at room temperature, not on a heater.</p></div>
<div class="card"><h3>Mark your cans</h3><p>Write the date or a tally on the lid each time you play. Then you know which can is fresh and which is for drills.</p></div>
<div class="card"><h3>Use old balls well</h3><p>Old balls are fine for <a href="{href("warm-up.html")}">warming up</a>, drills and practice serves. Just not for your next match. Check if a <a href="{href("serve-rules.html")}">serve is legal</a> while you practise.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Need fresh balls?</h3><p>Browse padel balls, plus overgrips and bags to keep your kit match-ready.</p><ul class="aff-links"><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>Rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
balls_faq = [
    ("How long do padel balls last?", "For social games, a can usually lasts about three to five sessions. Players who hit hard or play important matches often open a new can each match, because the best bounce goes after one or two uses."),
    ("How do I know if a padel ball is dead?", "Squeeze it, drop it next to a new ball and watch it off the back glass. A dead ball feels soft, bounces lower, sounds dull and dies in the corner instead of coming back."),
    ("Can you use tennis balls for padel?", "It's better not to. Tennis balls have more pressure inside, so they bounce higher and faster. Padel balls are made to play off the glass at the right speed."),
    ("What is the pressure of a padel ball?", "LTA Padel gives about 11 psi for a new padel ball, compared with about 14 psi for a new tennis ball."),
    ("Are padel balls smaller than tennis balls?", "Only very slightly. A padel ball is 6.35 to 6.77 cm across and a tennis ball 6.54 to 6.86 cm, and both weigh 56.0 to 59.4 g."),
    ("Do ball pressurisers work?", "They can slow down the loss of pressure, but they can't repair worn felt or make a dead ball lively again."),
]
page("padel-balls.html", "When to Change Padel Balls: Free Dead Ball Checker | Padel Glass Box",
     "Are your padel balls dead? Use the free 6-step checker, learn how long padel balls last, padel vs tennis ball pressure and size, and how to store them.", balls, balls_faq, "Padel balls")

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
<p class="lead">Glass, fence, net, ceiling: tap what your shot touched and see the call, with the ball path drawn on a side view of the court. Then read the wall and fence rules in plain English.</p></div></header>
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
<section><div class="wrap"><div class="sh"><h2>The wall rules in one minute</h2></div><div class="grid">
<div class="card"><span class="pill b">The golden rule</span><h3 style="margin-top:10px">Ground first, then walls</h3><p>Your shot must cross the net and bounce on their ground before it touches anything else on their side. After that bounce, the glass and the fence are both part of the game.</p></div>
<div class="card"><span class="pill b">Your side</span><h3 style="margin-top:10px">Your glass is a tool</h3><p>You can hit the ball into your own glass to send it back over the net. This is a normal shot in padel, often used when the ball gets past you into the corner.</p></div>
<div class="card"><span class="pill b">Your side</span><h3 style="margin-top:10px">Your fence is not</h3><p>Hitting the ball into the metal mesh on your own side loses the point. Only the glass may be used to play the ball back.</p></div>
<div class="card"><span class="pill b">Their side</span><h3 style="margin-top:10px">One bounce, then anything</h3><p>After one bounce on their side, the ball may hit their glass, their fence or both, as many times as it likes. They must hit it before it touches the ground a second time.</p></div>
<div class="card"><span class="pill b">Net</span><h3 style="margin-top:10px">Net cord is fine in a rally</h3><p>In a rally, a ball that clips the net and lands on their side is good. On the serve it is a let. Touching the net or the posts with your body or racket loses the point. More in the <a href="{href("net-rules.html")}">net rules checker</a>.</p></div>
<div class="card"><span class="pill b">Outside</span><h3 style="margin-top:10px">Out of the court</h3><p>A ball that bounces on their side and then flies out of the court was a good shot. At clubs that allow it, they may run out and play it back. If not, you win the point.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Every wall and fence call</h2></div>
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
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Out-of-court play, explained</h2></div><div class="grid">
<div class="card"><h3>What it is</h3><p>Sometimes a strong smash bounces on your side and flies out over the wall or through the door. At some courts you are allowed to run out of the court and hit the ball back before it bounces a second time. In Spanish this is called a salida de pista.</p></div>
<div class="card"><h3>When it is allowed</h3><p>Only where the court is built for it: open door gaps and enough clear space outside. If the space isn't there, the club does not allow it, and a ball that bounces and leaves the court simply wins the point for the hitter.</p></div>
<div class="card"><h3>How to play it</h3><p>Run out through the door, let the ball drop, and hit it back over the wall into the opponents' court. Your feet can be outside the court only when out-of-court play is allowed. Agree on the local rule before you start. Every out-of-court call is on our <a href="{href("out-of-court-play.html")}">out-of-court play checker</a>.</p></div>
</div></div></section>'''
wall_faq = [
    ("Can you hit the ball off your own wall in padel?", "Yes, off your own glass. You can hit the ball into your glass so it rebounds over the net, as long as it then bounces on the other side before touching their walls. Hitting your own metal fence loses the point."),
    ("Is it in if the ball hits the fence in padel?", "If the ball bounced on the ground first, yes: it stays in play. If it hit the fence before bouncing on the other side, the player who hit it loses the point."),
    ("What happens if the ball goes out of the court in padel?", "If it bounced on the opponents' side first, the shot was good. Where out-of-court play is allowed, the opponents may run out and return it before a second bounce. Otherwise the hitter wins the point."),
    ("Is a net cord a let in padel?", "Only on the serve. During a rally, a ball that touches the net and lands on the other side is in play, and players carry on."),
    ("What if the ball gets stuck in the fence in padel?", "If it bounced on the opponents' side and then gets stuck in the mesh, goes out through a hole, or stays on top of the wall, the player who hit it wins the point."),
    ("Can you touch the net in padel?", "No. Touching the net, the posts or the opponents' court with your body, clothes or racket while the ball is in play loses the point."),
    ("What if the ball hits the ceiling in padel?", "If your shot hits the ceiling or a light before bouncing on the opponents' side, you lose the point."),
]
page("wall-rules.html", "Padel Wall and Fence Rules: Was That Ball In? Free Checker | Padel Glass Box",
     "Padel wall rules in plain English: glass, metal fence, net cord, ceiling and out-of-court play. Tap what the ball touched and get the call on a side-view court.", wall + f'<script>window.WR={json.dumps(WR)};</script>', wall_faq, "Wall and fence rules")

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
<p class="lead">Three racket sports, three very different games. See the courts drawn to the same scale, compare the rules side by side, then answer five quick questions to see which one suits you best.</p></div></header>
<section style="padding-top:10px"><div class="wrap"><div class="vs-layout" id="vs">
<div class="court-art vs-art"><div class="vs-bar"><div class="seg" id="vs-show" role="group" aria-label="Show court"><button type="button" data-v="all" aria-pressed="true">All three</button><button type="button" data-v="t" aria-pressed="false">Tennis</button><button type="button" data-v="p" aria-pressed="false">Padel</button><button type="button" data-v="k" aria-pressed="false">Pickleball</button></div>
<div class="seg" id="vs-unit" role="group" aria-label="Units"><button type="button" data-v="m" aria-pressed="true">Metres</button><button type="button" data-v="ft" aria-pressed="false">Feet</button></div></div>
{VS_SVG}
<ul class="vs-key"><li><i class="k-t"></i>Tennis</li><li><i class="k-p"></i>Padel</li><li><i class="k-k"></i>Pickleball</li></ul></div>
<aside class="card zpanel" id="vs-info" aria-live="polite"></aside>
</div></div></section>
{AD.format("vs-mid")}
<section><div class="wrap"><div class="sh"><h2>Side by side</h2><p class="muted">The main rules of each sport, in short.</p></div>
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
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which sport suits you?</h2><p class="muted">Five questions, no right answers.</p></div>
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
<section><div class="wrap"><div class="sh"><h2>The biggest differences</h2></div><div class="grid">
<div class="card"><span class="pill b">Padel</span><h3 style="margin-top:10px">The walls change everything</h3><p>In padel the ball can bounce once and then hit the glass, and you can still play it. That gives you a second chance on many shots, so rallies last longer. Read the <a href="{href("wall-rules.html")}">wall and fence rules</a>.</p></div>
<div class="card"><span class="pill i">Tennis</span><h3 style="margin-top:10px">Space and the serve</h3><p>A tennis court is the biggest of the three, and the overhead serve is a weapon. You need more running and more technique before rallies feel easy.</p></div>
<div class="card"><span class="pill a">Pickleball</span><h3 style="margin-top:10px">The kitchen</h3><p>Pickleball has a 7 ft (2.13 m) zone each side of the net where you can't volley. It stops players smashing from the net, so soft drop shots, called dinks, matter a lot.</p></div>
<div class="card"><span class="pill b">Padel</span><h3 style="margin-top:10px">Scoring like tennis</h3><p>Padel uses the tennis count, but at 40-40 many games use a golden point or the newer Star Point. Keep track with our <a href="{href("score.html")}">score keeper</a> and see <a href="{href("golden-point-star-point.html")}">golden point vs Star Point</a>.</p></div>
<div class="card"><span class="pill a">Pickleball</span><h3 style="margin-top:10px">Only servers score</h3><p>In the traditional pickleball format, only the serving side can win points, and a game goes to 11, won by two. Some events now try rally scoring, where every rally counts.</p></div>
<div class="card"><span class="pill i">All three</span><h3 style="margin-top:10px">Different kit</h3><p>A tennis racket has strings. A padel racket is solid foam with holes. A pickleball paddle is solid and flat. Each sport also has its own ball, so you can't swap them.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Coming to padel from another sport</h2></div><div class="grid">
<div class="card"><h3>From tennis</h3><p>Your volleys and footwork help a lot. The hard part is letting the ball pass you and come off the glass instead of hitting it early. Shorten your swing: big tennis swings send the ball into the back glass. Start with the <a href="{href("shots.html")}">shot library</a>.</p></div>
<div class="card"><h3>From pickleball</h3><p>You already know the underhand serve and how to win at the net. In padel the serve must bounce first, there is no kitchen, and lobs over the net players are a main weapon. Learn <a href="{href("positioning.html")}">where to stand</a> as a pair.</p></div>
<div class="card"><h3>Brand new</h3><p>Padel is a good first racket sport: the court is small and the walls keep the ball in. Read the <a href="{href("beginners.html")}">first match checklist</a> and find a <a href="{href("racket-finder.html")}">racket that suits you</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Trying padel for the first time?</h3><p>Most clubs rent rackets. If you want your own, start with a forgiving round racket and proper court shoes.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li></ul>{AFF_NOTE}</div></div></section>'''
vs_faq = [
    ("What is the difference between padel and pickleball?", "Padel is played on a 20 × 10 m court with glass walls you can use, with a solid holed racket and a felt ball, almost always in doubles. Pickleball is played on a smaller 44 × 20 ft court with no walls, a solid paddle and a plastic ball, and it has a non-volley zone called the kitchen."),
    ("Is padel easier than tennis?", "For most beginners, yes. The court is smaller, the serve is underhand and the walls keep the ball in play, so rallies come much sooner than in tennis."),
    ("Is padel or pickleball easier to learn?", "Both are quick to learn. Pickleball is often called the easiest of the three to pick up, and padel the easiest way into a racket sport with walls. Many people play both."),
    ("Which court is bigger, padel or pickleball?", "Padel. A padel court is 20 × 10 m (200 m²). A pickleball court is 13.41 × 6.10 m (about 82 m²), so it is less than half the size."),
    ("Is a padel court smaller than a tennis court?", "Yes. A padel court is 20 × 10 m. A tennis doubles court is 23.77 × 10.97 m, so padel covers about three quarters of the area, and the walls make it feel even smaller."),
    ("Is padel scored like tennis?", "Yes: 15, 30, 40 and game, with sets to six. Many padel games use a golden point at 40-40, and the pro tours use Star Point from 2026."),
    ("Which is the best workout: padel, tennis or pickleball?", "Tennis usually means the most running. Padel is lots of short, quick movements and bending. Pickleball is the lowest impact of the three. Any of them is good exercise if you play regularly."),
]
page("padel-vs-tennis-vs-pickleball.html", "Padel vs Tennis vs Pickleball: Differences, Courts to Scale and Quiz | Padel Glass Box",
     "Padel vs tennis vs pickleball: compare court size, walls, serve, scoring and kit side by side, see the three courts drawn to scale, and take a quick quiz to pick your sport.",
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
<p class="lead">Type in the weight and balance from the spec sheet. See where the weight sits on a racket drawn to scale, what it means for power, speed and your arm, and how two rackets compare.</p></div></header>
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
<section><div class="wrap"><div class="sh"><h2>Balance: low, medium or high</h2><p class="muted">Every padel racket has more weight above its middle point.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Balance</th><th scope="col">Rough balance point</th><th scope="col">How it feels</th><th scope="col">Often found on</th></tr></thead><tbody>
<tr><td>Low (head-light)</td><td>Under about 260 mm</td><td>Quick to move, easy to control, gentler on the arm. Less free power.</td><td>Round rackets</td></tr>
<tr><td>Medium (even)</td><td>About 260 to 270 mm</td><td>A mix of control and power.</td><td>Teardrop rackets</td></tr>
<tr><td>High (head-heavy)</td><td>Over about 270 mm</td><td>More weight behind smashes and hard hits. Slower at the net and more load on the elbow and shoulder.</td><td>Diamond rackets</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Shops and brands draw these lines in slightly different places, so treat them as a guide. A racket is 45.5 cm long at most, so its middle is 227.5 mm from the bottom. Most rackets balance well above that, between about 250 and 285 mm.</p>
<div class="grid" style="margin-top:18px">
<div class="card"><h3>Shape is only a clue</h3><p>Round rackets are usually head-light and diamond rackets head-heavy, but not always. Some round rackets are quite head-heavy, and some diamonds are fairly even. The balance figure tells you more than the shape.</p></div>
<div class="card"><h3>Shape moves the sweet spot</h3><p>The sweet spot is the part of the face that gives the cleanest hit. On a round racket it is big and in the middle. On a teardrop it sits a little higher. On a diamond it is smaller and near the top.</p></div>
<div class="card"><h3>Balance changes the swing</h3><p>Two rackets with the same weight can feel very different. The one with the weight further up feels heavier when you swing it, because more of the weight is far from your hand.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Weight: what the grams mean</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Weight</th><th scope="col">Range</th><th scope="col">Tends to suit</th></tr></thead><tbody>
<tr><td>Light</td><td>Under about 355 g</td><td>New players, juniors, players with sore elbows or shoulders, and anyone who wants fast hands at the net.</td></tr>
<tr><td>Medium</td><td>About 355 to 370 g</td><td>Most improving players. A good mix of feel and power.</td></tr>
<tr><td>Heavy</td><td>Over about 370 g</td><td>Strong, experienced players who hit hard and want more power and stability.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Most adult rackets weigh between about 345 and 385 g. Weights on the box can be a few grams out, and many are given as a range, such as 360 to 375 g.</p></div></section>
<section id="measure"><div class="wrap"><div class="sh"><h2>Find your racket's balance at home</h2><p class="muted">You need a table, a pencil and a tape measure.</p></div>
<div class="grid">
<div class="card"><span class="pill b">Step 1</span><h3 style="margin-top:10px">Set it up as you play</h3><p>Leave the overgrip, frame protector and any tape on the racket. They all change the balance a little.</p></div>
<div class="card"><span class="pill b">Step 2</span><h3 style="margin-top:10px">Find the level point</h3><p>Lay a round pencil on a table. Put the racket across it, face flat, and slide it slowly until it rests level without tipping either way.</p></div>
<div class="card"><span class="pill b">Step 3</span><h3 style="margin-top:10px">Measure</h3><p>Mark the spot where the pencil touches. Measure from the very bottom of the handle to that mark in millimetres. That number is the balance point.</p></div>
<div class="card"><span class="pill i">Weight</span><h3 style="margin-top:10px">Weigh it too</h3><p>A kitchen scale works. Weigh the racket as you play with it, then put both numbers into the decoder above.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Small changes that move the balance</h2></div><div class="grid">
<div class="card"><h3>Adding an overgrip</h3><p>An overgrip adds a few grams at the handle, so the balance moves a little towards your hand and the racket feels a touch lighter to swing. Two overgrips move it more. See our <a href="{href("racket-finder.html")}#grip">grip and overgrip tips</a>.</p></div>
<div class="card"><h3>Frame protector tape</h3><p>Tape around the top of the frame protects it from scrapes on the floor and walls, but it adds weight at the head. The balance moves up and the racket feels heavier to swing.</p></div>
<div class="card"><h3>Lead or weight tape</h3><p>Some players add thin weight tape to tune a racket. Put it near the top for more power, or near the handle for more control. The rules allow added weights if they are a sensible size and position.</p></div>
</div></div></section>
<section><div class="wrap"><div class="sh"><h2>What the rules say about the racket</h2><p class="muted">From the FIP Rules of Padel, in force from 1 January 2026.</p></div>
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
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Not sure what you need?</h2></div><div class="grid">
<div class="card"><h3>Take the racket finder</h3><p>Three quick questions give you the shape, weight, balance, core and face that suit your level and style. <a href="{href("racket-finder.html")}">Open the racket finder</a>.</p></div>
<div class="card"><h3>Know your level first</h3><p>Weight and balance advice depends a lot on how long you have played. <a href="{href("level-calculator.html")}">Check your padel level</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop rackets by shape</h3><p>Use the decoder on any racket you like the look of: most shops list the weight, and many list the balance.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond rackets</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li></ul>{AFF_NOTE}</div></div></section>'''
rb_faq = [
    ("What is a good balance for a padel racket?", "For beginners and players who want control, a low balance of under about 260 mm from the bottom of the handle. For a mix of control and power, about 260 to 270 mm. Hard hitters who want power often choose over about 270 mm."),
    ("How is padel racket balance measured?", "It is the distance in millimetres from the bottom of the handle to the point where the racket balances level. Rest it across a pencil, slide it until it sits level, and measure to that point."),
    ("What does head-heavy mean on a padel racket?", "More of the weight sits towards the top of the head. That adds power to smashes and hard shots, but the racket is slower to move and puts more load on your elbow and shoulder."),
    ("How heavy should my padel racket be?", "Most adult rackets weigh about 345 to 385 g. New players and those with sore arms usually do best under about 360 g; strong, experienced players often choose 365 to 375 g or more."),
    ("Is a lighter padel racket better for tennis elbow?", "A lighter racket with a low balance usually puts less strain on the arm, and a soft core helps too. If the pain continues, see a doctor or physio."),
    ("Does an overgrip change the balance?", "A little. It adds weight at the handle, so the balance point moves towards your hand. Frame protector tape does the opposite and moves it towards the head."),
    ("Is there a weight limit for padel rackets?", "No. The FIP rules limit the size of the racket, 45.5 cm long, 26 cm wide and 38 mm thick at most, but not its weight or balance."),
]
RB_PRE = {"round": [355, 255, "round"], "teardrop": [362, 265, "teardrop"], "diamond": [368, 275, "diamond"]}
page("racket-balance.html", "Padel Racket Weight and Balance Explained: Free Spec Decoder | Padel Glass Box",
     "What padel racket weight and balance really mean. Enter grams and balance in mm to see the balance point on a to-scale racket, compare two rackets, and learn to measure balance at home.",
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
page("round-robin.html", "Padel Round Robin Generator for Fixed Pairs: Free Schedule and Table | Padel Glass Box",
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
<div class="card"><h3>Rest of your kit</h3><p>Find a racket that suits you with the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
<div class="card"><h3>Before you play</h3><p>Look after your legs with the <a href="{href("warm-up.html")}">10-minute warm-up timer</a>.</p></div>
<div class="card"><h3>Check your balls</h3><p>Flat balls make you lunge more. Run the <a href="{href("padel-balls.html")}">dead ball checker</a>.</p></div>
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
     "Which padel shoes do you need? Answer four questions to get your sole type (herringbone, omni or hybrid), then compare padel vs tennis vs running shoes, check fit and see when to replace them.",
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
page("padel-calories.html", "Padel Calories Calculator: How Many Calories Does Padel Burn? | Padel Glass Box",
     "Free padel calories calculator. Enter your weight, time and effort to see how many calories padel burns per session, per hour and per week, and how it counts toward the weekly activity target.",
     cal, cal_faq, "Padel calories calculator")

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
<tr><td><a href="{href("round-robin.html")}">Round robin</a></td><td>Fixed pairs</td><td>One event or a short league</td><td>Everyone plays everyone once</td></tr>
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
page("ladder.html", "Padel Ladder Tracker: Free Challenge Ladder for Pairs or Players | Padel Glass Box",
     "Free padel ladder tracker. Add your pairs or players, record challenges and the ladder updates itself, with records, movement and history. Plus ladder rules to agree.",
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
page("net-rules.html", "Padel Net Rules: Can You Touch the Net? Free Net Call Checker | Padel Glass Box",
     "Padel net rules in plain English: touching the net, reaching over, follow-through, balls that spin back, net cords in a rally and on the serve. Tap what happened and get the FIP call.",
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
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Habits that break rackets</h2></div><div class="grid">
<div class="card"><h3>Hitting the floor or walls</h3><p>Banging the racket on the ground or the glass in frustration is the quickest way to crack the frame.</p></div>
<div class="card"><h3>Scooping up balls</h3><p>Picking balls up by scraping the face along the turf wears the face and the edge. Use your hand or foot.</p></div>
<div class="card"><h3>Clashing with your partner</h3><p>Racket clashes in the middle crack frames. Call "mine" or "yours" early (in Spanish: mía and tuya).</p></div>
<div class="card"><h3>Leaving it in the car</h3><p>A car in the sun gets very hot, and in winter very cold. Both are bad for the foam inside.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long does a padel racket last?</h2></div>
<div class="card"><p>There is no fixed number. It depends on how often and how hard you play, and how you store it. Instead of counting months, watch for the signs: a crack that grows, a rattle inside, dead or soft spots, or less power than when it was new. If you see them, ask the shop or the brand to look at it, and check whether it is still under warranty. Good care, protector tape and a cover all help a racket last longer.</p></div>
<p class="muted" style="margin-top:14px">Ready for a new one? Find the right shape and weight with the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div></section>
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
    ("How do you clean a padel racket?", "Use a dry, soft cloth after each game. For marks, use a cloth that is only slightly damp with a little mild soap, then dry it straight away. Never soak it or use strong cleaners."),
    ("How often should you change your padel overgrip?", "When it gets slippery, shiny or torn. That can be every few matches if you play a lot and sweat a lot, or every month or two if you play less."),
    ("How do I know if my padel racket is broken?", "Look for cracks in the frame or face, listen for a rattle inside, and notice dead spots, odd vibrations or a loss of power. If you find these, ask the shop or brand to check it."),
]
page("racket-care.html", "Padel Racket Care: Heat, Cold, Protector Tape and a Free Health Check | Padel Glass Box",
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
<div class="card"><h3>Learn the shots</h3><p>See how the bandeja, víbora and chiquita are played in the <a href="{href("shots.html")}">shot library</a>.</p></div>
<div class="card"><h3>Know where to stand</h3><p>Drills work better when you recover to the right spot. See the <a href="{href("positioning.html")}">positioning guide</a>.</p></div>
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
     "Free padel drills planner. Pick players, time, level and focus to get a timed practice session, with 13 drills for one, two or four players and a place to log your records.",
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
<tr><td><a href="{href("round-robin.html")}">Round robin</a></td><td>Fixed pairs</td><td>Best record in the table</td><td>A mini league</td></tr>
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
page("king-of-the-court.html", "King of the Court Padel Generator: Free Rounds, Courts and Table | Padel Glass Box",
     "Free King of the Court padel generator. Enter 8 to 28 players, tap the winners and get the next round: winners up, losers down, new partners. Round timer and live table.",
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
page("tie-break.html", "Padel Tie-Break Rules: Who Serves and When to Change Ends (Free Tracker) | Padel Glass Box",
     "Padel tie-break rules made simple: first to 7, 2 clear, serve order 1 then 2 each, change ends every 6 points. Free tracker for set and 10-point match tie-breaks.", tb, tb_faq, "Tie-break rules")

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
page("out-of-court-play.html", "Padel Out-of-Court Play Rules: When Can You Leave the Court? (Free Checker) | Padel Glass Box",
     "Padel out-of-court play (salida de pista) explained: when you can run out to play the ball, what space a court needs, door and serve calls, and lets. Free FIP call checker.",
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
<div class="card"><h3>Does the racket matter?</h3><p>Many coaches and shops suggest a lighter, less head-heavy racket and a thicker, fresh grip for sore elbows. This makes sense but has not been proven in studies. Compare specs with the <a href="{href("racket-balance.html")}">weight and balance decoder</a>.</p></div>
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
<div class="card"><h3>Check your racket</h3><p>Too heavy for your arm? Try the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
<div class="card"><h3>Know your load</h3><p>See how hard your games really are with the <a href="{href("padel-calories.html")}">padel calories calculator</a>.</p></div>
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
page("padel-injuries.html", "Padel Injuries: Elbow, Knee, Back and How to Prevent Them (Free Check) | Padel Glass Box",
     "The most common padel injuries, from padel elbow to knee, shoulder and back pain: tap a body area to see what studies report and what helps, and run a free injury prevention check.",
     inj, inj_faq, "Padel injuries")

page("about.html", f"About {SITE}", f"About {SITE}, a free set of padel tools and guides, and how to contact us.",
     f'<section><div class="wrap" style="max-width:760px"><h1>About {SITE}</h1><p>{SITE} makes free, simple padel tools: a racket finder, a score keeper, an interactive rules court and a shot library.</p><h2>How we check facts</h2><p>Rules follow the International Padel Federation (FIP). Equipment advice is general guidance checked against several trusted guides; we don\'t take payment to recommend gear.</p><h2>Contact</h2><p>Email <strong>[your email address]</strong>.</p></div></section>')
page("privacy.html", f"Privacy Policy | {SITE}", f"{SITE} privacy policy covering cookies, Google AdSense, Google Analytics and affiliate links.",
     f'<section><div class="wrap" style="max-width:760px"><h1>Privacy policy</h1><p>Last updated: {e(UPDATED)}.</p><h2>What we collect</h2><p>Your score, checklist ticks and quiz answers are saved only in your own browser. If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the cheat sheet and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time.</p><h2>Analytics</h2><p>We use Google Analytics to count visits and see which pages are popular. It uses cookies and collects details like pages viewed, approximate location and device type.</p><h2>Advertising</h2><p>This site uses Google AdSense. Google and its partners use cookies to show ads based on your visits to this and other websites. You can turn off personalised ads at <a href="https://adssettings.google.com">Google Ads Settings</a>. Learn more at <a href="https://policies.google.com/technologies/partner-sites">policies.google.com/technologies/partner-sites</a>.</p><h2>Affiliate links</h2><p>Some links may be affiliate links. If you buy through them, we may earn a small fee at no extra cost to you.</p><h2>Contact</h2><p>Email <strong>[your email address]</strong>.</p></div></section>')
page("404.html", f"Page not found | {SITE}", "This page doesn't exist.",
     f'<section><div class="wrap"><h1>That one went out.</h1><p class="lead">This page doesn\'t exist.</p><a class="btn lime" href="{href("index.html")}">Back to the home page</a></div></section>')

page("thanks.html", f"Check your inbox | {SITE}", "Confirm your email to get the free padel rules cheat sheet.", NL_THANKS)
page("welcome.html", f"Your padel cheat sheet | {SITE}", "Download your free padel rules cheat sheet.", NL_WELCOME)

urls = ["index.html", "racket-finder.html", "score.html", "rules.html", "shots.html", "beginners.html", "glossary.html", "americano.html", "court-dimensions.html", "level-calculator.html", "golden-point-star-point.html", "positioning.html", "serve-rules.html", "warm-up.html", "padel-balls.html", "wall-rules.html", "padel-vs-tennis-vs-pickleball.html", "racket-balance.html", "round-robin.html", "padel-shoes.html", "padel-calories.html", "ladder.html", "net-rules.html", "racket-care.html", "drills.html", "king-of-the-court.html", "tie-break.html", "out-of-court-play.html", "padel-injuries.html", "about.html", "privacy.html"]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{canon(u)}</loc><lastmod>{UPDATED}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if u == 'index.html' else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
if not (ROOT / "ads.txt").exists():
    (ROOT / "ads.txt").write_text("google.com, pub-1558743317014653, DIRECT, f08c47fec0942fa0\n")
print("built", len(urls) + 1, "pages", "(preview)" if PREVIEW else "(live)")
write_redirects(ROOT)
