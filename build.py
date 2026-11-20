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
<div><strong style="color:#fff">Tools and guides</strong><ul>{"".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in NAV)}<li><a href="{href("glossary.html")}">Glossary</a></li><li><a href="{href("americano.html")}">Americano generator</a></li><li><a href="{href("court-dimensions.html")}">Court dimensions</a></li><li><a href="{href("level-calculator.html")}">Level calculator</a></li><li><a href="{href("golden-point-star-point.html")}">Golden point vs Star Point</a></li><li><a href="{href("serve-rules.html")}">Serve rules and checker</a></li><li><a href="{href("positioning.html")}">Where to stand</a></li><li><a href="{href("warm-up.html")}">Warm-up timer</a></li><li><a href="{href("padel-balls.html")}">When to change balls</a></li></ul></div>
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
    ("What is padel?", "Padel is a racket sport played mostly in doubles on an enclosed court about a third the size of a tennis court. You use a solid, holed racket and can play the ball off the glass walls."),
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
<div class="card"><h3>Weight</h3><p>Most adult rackets weigh roughly 350 to 385 g. Heavier rackets hit harder but tire your arm sooner; lighter ones are quicker at the net.</p></div>
<div class="card"><h3>Balance</h3><p>Low balance (towards the handle) means control and quick hands. High balance (towards the head) means power but more strain.</p></div>
<div class="card"><h3>Core foam</h3><p>Soft foam gives easy power and comfort at slow speeds. Hard foam gives control when you swing fast.</p></div>
<div class="card"><h3>Face material</h3><p>Fiberglass is softer and forgiving. Carbon is stiffer and more precise, and usually costs more.</p></div>
</div></div></section>'''
finder_faq = [
    ("What padel racket should a beginner buy?", "Most beginners do best with a round racket: low balance, a lighter weight, soft foam and a fiberglass face. It's forgiving and easy to control."),
    ("Round, teardrop or diamond: which is best?", "Round gives the most control, diamond the most power, and teardrop sits in between. Many players start round, move to teardrop, then try diamond."),
    ("How heavy should a padel racket be?", "Most adult rackets weigh around 350 to 385 g. Pick the lighter end if you're new or have sore elbows, and the heavier end if you hit hard."),
    ("Does a racket help with tennis elbow?", "A lighter racket with a soft core and low balance puts less strain on your arm. If pain continues, see a doctor or physio."),
]
page("racket-finder.html", "Padel Racket Finder: Which Racket Suits You? | Padel Glass Box",
     "Answer 3 questions and find the padel racket shape, weight, balance, core and face that suit your level and style. Free and instant.", finder + f'''<section><div class="wrap"><div class="aff-box"><h3>Shop padel gear</h3><p>Browse rackets by shape, plus the shoes, balls and grips you need for your first match.</p><ul class="aff-links"><li><a href="/go/padel-round-rackets" rel="sponsored nofollow noopener" target="_blank">Round rackets</a></li><li><a href="/go/padel-teardrop-rackets" rel="sponsored nofollow noopener" target="_blank">Teardrop rackets</a></li><li><a href="/go/padel-diamond-rackets" rel="sponsored nofollow noopener" target="_blank">Diamond rackets</a></li><li><a href="/go/padel-shoes" rel="sponsored nofollow noopener" target="_blank">Padel shoes</a></li><li><a href="/go/padel-balls" rel="sponsored nofollow noopener" target="_blank">Balls</a></li><li><a href="/go/padel-bags" rel="sponsored nofollow noopener" target="_blank">Bags</a></li><li><a href="/go/padel-overgrips" rel="sponsored nofollow noopener" target="_blank">Overgrips</a></li></ul>{AFF_NOTE}</div></div></section>''', finder_faq, "Racket finder")

# ---------------- SCORE KEEPER ----------------
score = f'''<header class="hero" style="padding-bottom:10px"><div class="wrap"><h1>Padel score keeper.</h1>
<p class="lead">Put your phone by the net and tap the side that wins each point. It handles deuce, golden point, tie-breaks and sets, and remembers the score if you close the page.</p></div></header>
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
<section><div class="wrap"><div class="sh"><h2>How padel scoring works</h2></div><div class="grid">
<div class="card"><h3>Points</h3><p>0, 15, 30, 40, then the game. Exactly like tennis.</p></div>
<div class="card"><h3>Deuce</h3><p>At 40-40 there are three official options: classic advantage, golden point (one deciding point) or the newer Star Point. All three are built in here. Not sure which to pick? See <a href="{href("golden-point-star-point.html")}">golden point vs Star Point</a>.</p></div>
<div class="card"><h3>Sets and tie-breaks</h3><p>A set goes to six games with a two-game lead. At 6-6 a tie-break is played to 7 points, two clear. Most matches are best of three sets.</p></div>
<div class="card"><h3>Golden point side</h3><p>With golden point, the receiving pair chooses which player receives the deciding serve.</p></div>
<div class="card"><h3>Star Point</h3><p>You play advantage twice. If the game comes back to 40-40 a third time, one deciding point wins it. The score keeper counts the deuces for you.</p></div>
</div></div></section>'''
score_faq = [
    ("How do you keep score in padel?", "Like tennis: 0, 15, 30, 40 and game. Sets go to six games with a two-game lead, and a tie-break decides 6-6."),
    ("What is the golden point in padel?", "At 40-40, one deciding point is played. The receiving pair chooses which side receives, and whoever wins that point wins the game."),
    ("What is Star Point in padel?", "Star Point is a deuce format used on the pro tours from 2026. You play advantage twice; if the game reaches 40-40 a third time, one deciding point wins it. This score keeper supports it."),
    ("Does this score keeper save my match?", "Yes. The score is saved on your phone, so you can lock the screen or close the page and carry on."),
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
<p class="lead">Tap any part of the court to see the rule that goes with it, then read the key rules for serving, walls and scoring below.</p></div></header>
<section style="padding-top:10px"><div class="wrap rules-layout">
<div class="court-art" style="max-width:440px;margin-inline:auto;width:100%">{court_svg}</div>
<aside class="card zpanel" id="zpanel" aria-live="polite"></aside>
</div></section>
{AD.format("rules-mid")}
<section><div class="wrap"><div class="sh"><h2>The key rules</h2></div><div class="grid">
<div class="card"><h3>The serve</h3><p>Stand behind the service line with your feet off the lines, bounce the ball, and hit it underhand at or below waist height with one foot on the ground. It must land in the box diagonally opposite. You get two attempts per point.</p></div>
<div class="card"><h3>A serve is a fault if</h3><p>it lands outside the diagonal box, it's hit above the waist, you miss the ball, your foot touches the line, or after bouncing in the box it hits the metal mesh. Not sure? Use our <a href="{href("serve-rules.html")}">serve checker</a>.</p></div>
<div class="card"><h3>Lets</h3><p>If the serve touches the net and still lands in the right box, without touching the metal fence, it is a let and you replay that serve.</p></div>
<div class="card"><h3>Receiving</h3><p>The receiver must let the serve bounce before hitting it. After that, players can volley freely.</p></div>
<div class="card"><h3>Using the walls</h3><p>On your side, the ball can bounce once and then hit the walls; you can still play it. You may also hit the ball into your own walls to get it back over the net.</p></div>
<div class="card"><h3>Lost points</h3><p>You lose the point if the ball bounces twice, if your shot hits the opponents' wall or fence before the ground, or if the ball touches your body.</p></div>
<div class="card"><h3>Scoring</h3><p>15, 30, 40, game, sets to six with a tie-break at 6-6. At deuce, the organiser chooses advantage, golden point or Star Point: <a href="{href("golden-point-star-point.html")}">see how each one works</a>.</p></div>
<div class="card"><h3>Court size</h3><p>The court is 20 m by 10 m, with the service lines 6.95 m from the net. See every measurement, in metres or feet, on our <a href="{href("court-dimensions.html")}">measured court diagram</a>.</p></div>
<div class="card"><h3>Where to stand</h3><p>Rules tell you what is allowed; position wins points. See where all four players stand at the serve, at the net and at the back on our <a href="{href("positioning.html")}">positioning guide</a>.</p></div>
<div class="card"><h3>Social formats</h3><p>At club nights you often play points, not sets: an Americano or Mexicano. Our <a href="{href("americano.html")}">draw maker</a> sets the partners, courts and leaderboard for you.</p></div>
</div></div></section>'''
rules_faq = [
    ("Can you serve overarm in padel?", "No. The padel serve is always underhand: you bounce the ball and hit it at or below waist height."),
    ("Can the ball hit the wall in padel?", "Yes, after it bounces on the ground on your side. If your shot hits the opponents' wall before bouncing on their ground, you lose the point."),
    ("What happens if the ball hits a player?", "The player's team usually loses the point, with only a few exceptions in the official rules."),
    ("How high is a padel net?", "88 cm in the middle and 92 cm at the posts."),
    ("Where must the server stand?", "Behind the service line, which is 6.95 m from the net, between the centre line and the side wall, serving diagonally into the opposite service box."),
    ("What is a let in padel?", "A serve that touches the net and then lands in the correct box without touching the metal fence. The serve is replayed. A let on the second serve replays only the second serve."),
]
page("rules.html", "Padel Rules Explained Simply, With an Interactive Court | Padel Glass Box",
     "Padel rules in plain English: the underhand serve, walls, faults and scoring, plus an interactive court you can tap to learn each part.", rules, rules_faq, "Rules")

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
<p class="lead">What each shot is for, when to play it, and one tip to get it right. Each card shows the ball's path, with the net in the middle and the glass at the ends.</p></div></header>
<section style="padding-top:10px"><div class="wrap">
<div class="filters seg" id="shot-filter" role="group" aria-label="Filter shots by level" style="background:#fff;border:1px solid var(--line)"><button type="button" data-v="all" aria-pressed="true" style="color:var(--ink)">All</button><button type="button" data-v="Beginner" aria-pressed="false" style="color:var(--ink)">Beginner</button><button type="button" data-v="Intermediate" aria-pressed="false" style="color:var(--ink)">Intermediate</button><button type="button" data-v="Advanced" aria-pressed="false" style="color:var(--ink)">Advanced</button></div>
<div class="grid">{shot_cards}</div></div></section>'''
shots_faq = [
    ("What is a bandeja in padel?", "A controlled overhead with slice, played after a lob. Its job is to keep your team at the net, not to win the point outright."),
    ("What's the difference between a bandeja and a víbora?", "Both are overheads, but the víbora adds sidespin and pace to attack, while the bandeja is safer and about placement. Learn the bandeja first."),
    ("What is a chiquita?", "A soft, low ball from the back of the court that drops at the net players' feet, so your team can move forward."),
    ("What is a rulo?", "A topspin smash aimed across the court at the side fence, where the ball bounces unpredictably."),
]
page("shots.html", "Padel Shots Explained: Bandeja, Víbora, Chiquita and More | Padel Glass Box",
     "Every key padel shot explained simply, with animated ball paths: bandeja, víbora, rulo, chiquita, bajada, contrapared, lob, volley and smash.", shots, shots_faq, "Shots")

# ---------------- BEGINNERS ----------------
kit = ["A padel racket (a round one is easiest to start with)", "Padel balls, not tennis balls (they have less pressure)", "Court shoes with good grip for artificial grass", "A wrist strap on your racket, and wear it", "Comfortable sports clothes and water", "A booked court and three other players"]
know = ["Serve underhand, below the waist, diagonally", "Let the ball bounce once, then it can hit your walls", "Never let your shot hit their wall before the ground", "Agree on advantage or golden point before you start", "Stay with your partner: move up and back together", "When in doubt, lob and go to the net"]
def checklist(name, items):
    return f'<div class="prog"><i id="{name}-bar"></i></div><p class="muted" id="{name}-count" style="margin:-8px 0 12px"></p><ul class="check" data-check="{name}">' + "".join(f'<li><label><input type="checkbox"><span>{e(x)}</span></label></li>' for x in items) + "</ul>"
beg = f'''<header class="hero"><div class="wrap"><h1>Your first padel match.</h1>
<p class="lead">Tick these off and you'll walk onto court ready. Your ticks are saved on this device.</p></div></header>
<section style="padding-top:10px"><div class="wrap grid" style="grid-template-columns:repeat(auto-fit,minmax(320px,1fr))">
<div class="card"><h2 style="font-size:1.6rem">What to bring</h2>{checklist("kit", kit)}</div>
<div class="card"><h2 style="font-size:1.6rem">What to know</h2>{checklist("know", know)}</div>
</div></section>
{AD.format("beg-mid")}
<section><div class="wrap"><div class="sh"><h2>Where to play</h2></div><div class="grid">
<div class="card"><h3>Booking apps</h3><p>Many clubs list their courts on booking apps such as Playtomic, where you can also find open matches at your level.</p></div>
<div class="card"><h3>National federations</h3><p>Your country's padel or tennis federation usually lists clubs and beginner sessions. In the UK, that's LTA Padel.</p></div>
<div class="card"><h3>Join a social night</h3><p>Many clubs run Americano evenings where you change partner each round. They are a friendly way to meet players at your level. Running one yourself? Use our <a href="{href("americano.html")}">Americano generator</a>.</p></div>
<div class="card"><h3>Know your level</h3><p>Open matches and clubs often ask for your level. Our <a href="{href("level-calculator.html")}">padel level calculator</a> gives you a quick estimate.</p></div>
<div class="card"><h3>Know where to stand</h3><p>Move up and back with your partner, and stay about 1 metre off the back glass. Our <a href="{href("positioning.html")}">positioning guide</a> shows every situation on a court.</p></div>
<div class="card"><h3>Warm up first</h3><p>Ten minutes of jogging, moving stretches and soft rallies makes the first games easier on your body. Our <a href="{href("warm-up.html")}">warm-up timer</a> talks you through it step by step.</p></div>
<div class="card"><h3>Start with a lesson</h3><p>One group lesson teaches the serve and the walls much faster than working it out alone.</p></div>
</div></div></section>'''
beg_faq = [
    ("What do I need for my first padel game?", "A racket, padel balls, court shoes with grip, comfy sports clothes and water. Many clubs rent rackets if you don't have one yet."),
    ("Can I use tennis balls for padel?", "It's better not to. Padel balls have less pressure inside (about 11 psi against 14 psi for tennis, according to LTA Padel), so they bounce lower and play the way padel should."),
    ("How should I warm up for padel?", "Spend 10 to 15 minutes on an easy jog, moving stretches, a few squats and lunges, then soft rallies, volleys, lobs and serves. Save long, held stretches for after you play."),
    ("Do I need special shoes for padel?", "Shoes with good grip for artificial grass courts help you move safely. Running shoes slip more easily."),
]
page("beginners.html", "Padel for Beginners: First Match Checklist | Padel Glass Box",
     "Everything you need for your first padel match: a kit checklist, the rules to know, and where to find courts and beginner sessions.", beg + f'''<section><div class="wrap"><div class="aff-box"><h3>Shop padel gear</h3><p>Browse rackets by shape, plus the shoes, balls and grips you need for your first match.</p><ul class="aff-links"><li><a href="/go/padel-round-rackets" rel="sponsored nofollow noopener" target="_blank">Round rackets</a></li><li><a href="/go/padel-teardrop-rackets" rel="sponsored nofollow noopener" target="_blank">Teardrop rackets</a></li><li><a href="/go/padel-diamond-rackets" rel="sponsored nofollow noopener" target="_blank">Diamond rackets</a></li><li><a href="/go/padel-shoes" rel="sponsored nofollow noopener" target="_blank">Padel shoes</a></li><li><a href="/go/padel-balls" rel="sponsored nofollow noopener" target="_blank">Balls</a></li><li><a href="/go/padel-bags" rel="sponsored nofollow noopener" target="_blank">Bags</a></li><li><a href="/go/padel-overgrips" rel="sponsored nofollow noopener" target="_blank">Overgrips</a></li></ul>{AFF_NOTE}</div></div></section>''', beg_faq, "Beginners")

# ---------------- GLOSSARY ----------------
gl = "".join(f"<div><b>{e(t)}</b><span>{e(d)}</span></div>" for t, d in D["glossary"])
glos = f'''<header class="hero"><div class="wrap"><h1>Padel words, decoded.</h1>
<p class="lead">Padel borrows lots of Spanish. Search any word you've heard on court.</p></div></header>
<section style="padding-top:10px"><div class="wrap"><label class="sr-only" for="gsearch">Search the glossary</label><input class="search" id="gsearch" type="search" placeholder="Search: bandeja, golden point, malla..."><div class="gl" id="glist">{gl}</div></div></section>'''
page("glossary.html", "Padel Glossary: Every Term Explained | Padel Glass Box",
     "Padel terms explained in plain English: bandeja, víbora, chiquita, bajada, golden point, drive, revés and more. Searchable and free.", glos, None, "Glossary")

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
<p class="lead">Every official measurement on one court you can explore: tap a measurement to light it up and read what it's for. Switch between metres and feet.</p></div></header>
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
<div class="card"><h3>A third of a tennis court</h3><p>At 20 m by 10 m, the court is small enough that you rarely sprint far. That is a big reason padel feels easy to start.</p></div>
<div class="card"><h3>A short back area</h3><p>Only about 3 m sits behind the service line. Balls reach the back glass quickly, so learning to let the ball come off the wall matters early.</p></div>
<div class="card"><h3>A low net</h3><p>The net is lower than in tennis, and dips a little in the middle. Low, flat balls over the centre are the safest way to keep the ball in play.</p></div>
<div class="card"><h3>Where the glass steps down</h3><p>The side glass is tallest near the back walls. Balls that hit the mesh act differently from glass, which you can read about on our <a href="{href("rules.html")}">rules court</a>.</p></div>
</div></div></section>'''
court_faq = [
    ("How big is a padel court?", "A doubles padel court is 20 m long and 10 m wide inside the walls. That is about 65 ft 7 in by 32 ft 10 in."),
    ("How far is the service line from the net?", "6.95 m on each side. That leaves 3.05 m between the service line and the back wall."),
    ("How high is a padel net?", "0.88 m in the middle and 0.92 m at the posts, which is roughly 2 ft 11 in and 3 ft."),
    ("How high are the walls of a padel court?", "The back wall is 4 m in total: 3 m of glass with 1 m of metal mesh on top. The side glass is 3 m high near the back walls, then steps down to 2 m."),
    ("How much ceiling height does indoor padel need?", "The official rules ask for at least 6 m of clear height above the court. Higher is better for lobs."),
    ("How big is a singles padel court?", "Singles courts are 20 m long like doubles, but only 6 m wide."),
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
<div class="card"><h3>Tie-breaks</h3><p>None of this changes the tie-break. At 6-6 you play to 7 points with a two-point lead. Read more on our <a href="{href("rules.html")}">rules page</a>.</p></div>
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
<p class="muted" style="margin-top:14px">A let replays only that serve. A let on the second serve means you take the second serve again, not two new serves. More rules on our <a href="{href("rules.html")}">interactive rules court</a>, and serve tactics on the <a href="{href("positioning.html")}">positioning guide</a>.</p>
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
<p class="lead">Press start and follow the steps. A 10 or 15 minute warm-up that gets your legs, arms and eye ready before the first point. Works on your phone at the court.</p></div></header>
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
<section><div class="wrap"><div class="sh"><h2>How this warm-up works</h2></div><div class="grid">
<div class="card"><h3>1. Get warm</h3><p>A couple of minutes of easy jogging raises your heart rate and sends blood to your muscles. Start slow.</p></div>
<div class="card"><h3>2. Move</h3><p>Moving stretches, like leg swings and lunges with a twist, loosen your hips, back and shoulders. Keep them moving: save long, held stretches for after the match.</p></div>
<div class="card"><h3>3. Activate</h3><p>Squats, lunges and short sprints wake up the legs you use for every split step and change of direction. LTA Padel's warm-up advice is built around exercises like these to help avoid hamstring, calf and thigh strains.</p></div>
<div class="card"><h3>4. Racket</h3><p>Start soft and close to the net, then add volleys, lobs and overheads. Build up the pace: your first smash should not be your hardest.</p></div>
<div class="card"><h3>5. Mind</h3><p>Agree three simple goals with your partner. It takes 30 seconds and helps you start the match switched on.</p></div>
<div class="card"><h3>After you play</h3><p>Walk for a couple of minutes, then gently hold stretches for your calves, thighs, hips, forearms and shoulders, about 20 to 30 seconds each.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Short on court time?</h2></div><div class="grid">
<div class="card"><h3>Do the first half before you go on</h3><p>The jog, moving stretches and squats need no court. Do them by the court while the last game finishes, then use your court time for the racket steps.</p></div>
<div class="card"><h3>Playing early or in the cold?</h3><p>Choose the 15 minute version. Cold muscles need longer, and the balls feel flatter too. Read <a href="{href("padel-balls.html")}">when to change padel balls</a>.</p></div>
<div class="card"><h3>Something hurts?</h3><p>A warm-up is not a fix for an injury. If you feel sharp pain, stop and get advice from a doctor or physiotherapist.</p></div>
</div></div></section>'''
warm_faq = [
    ("How long should a padel warm-up be?", "About 10 to 15 minutes is enough for most players. LTA Padel suggests 10 to 15 minutes, starting with a short jog, then exercises, then a few minutes of rallying."),
    ("Should I stretch before padel?", "Use moving stretches before you play, such as leg swings, arm circles and lunges with a twist. Keep long, held stretches for after the match."),
    ("What should a padel warm-up include?", "A short jog, moving stretches, a few leg exercises such as squats and lunges, short sprints, and then racket work: soft rallies, volleys, lobs, easy overheads and a few serves."),
    ("Can I warm up without a court?", "Yes. The jog, moving stretches, squats, lunges and sprints can all be done next to the court before your booking starts."),
    ("Does the timer work without internet?", "Once the page has loaded, the timer runs in your browser. Keep the screen on, because some phones pause timers when the screen locks."),
]
page("warm-up.html", "Padel Warm-Up Routine With Free Timer (10 or 15 Minutes) | Padel Glass Box",
     "A free padel warm-up timer: follow a 10 or 15 minute routine step by step, from jogging and moving stretches to volleys, lobs and serves. Works on your phone.", warm, warm_faq, "Warm-up timer")

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
page("about.html", f"About {SITE}", f"About {SITE}, a free set of padel tools and guides, and how to contact us.",
     f'<section><div class="wrap" style="max-width:760px"><h1>About {SITE}</h1><p>{SITE} makes free, simple padel tools: a racket finder, a score keeper, an interactive rules court and a shot library.</p><h2>How we check facts</h2><p>Rules follow the International Padel Federation (FIP). Equipment advice is general guidance checked against several trusted guides; we don\'t take payment to recommend gear.</p><h2>Contact</h2><p>Email <strong>[your email address]</strong>.</p></div></section>')
page("privacy.html", f"Privacy Policy | {SITE}", f"{SITE} privacy policy covering cookies, Google AdSense, Google Analytics and affiliate links.",
     f'<section><div class="wrap" style="max-width:760px"><h1>Privacy policy</h1><p>Last updated: {e(UPDATED)}.</p><h2>What we collect</h2><p>Your score, checklist ticks and quiz answers are saved only in your own browser. If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the cheat sheet and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time.</p><h2>Analytics</h2><p>We use Google Analytics to count visits and see which pages are popular. It uses cookies and collects details like pages viewed, approximate location and device type.</p><h2>Advertising</h2><p>This site uses Google AdSense. Google and its partners use cookies to show ads based on your visits to this and other websites. You can turn off personalised ads at <a href="https://adssettings.google.com">Google Ads Settings</a>. Learn more at <a href="https://policies.google.com/technologies/partner-sites">policies.google.com/technologies/partner-sites</a>.</p><h2>Affiliate links</h2><p>Some links may be affiliate links. If you buy through them, we may earn a small fee at no extra cost to you.</p><h2>Contact</h2><p>Email <strong>[your email address]</strong>.</p></div></section>')
page("404.html", f"Page not found | {SITE}", "This page doesn't exist.",
     f'<section><div class="wrap"><h1>That one went out.</h1><p class="lead">This page doesn\'t exist.</p><a class="btn lime" href="{href("index.html")}">Back to the home page</a></div></section>')

page("thanks.html", f"Check your inbox | {SITE}", "Confirm your email to get the free padel rules cheat sheet.", NL_THANKS)
page("welcome.html", f"Your padel cheat sheet | {SITE}", "Download your free padel rules cheat sheet.", NL_WELCOME)

urls = ["index.html", "racket-finder.html", "score.html", "rules.html", "shots.html", "beginners.html", "glossary.html", "americano.html", "court-dimensions.html", "level-calculator.html", "golden-point-star-point.html", "positioning.html", "serve-rules.html", "warm-up.html", "padel-balls.html", "about.html", "privacy.html"]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{canon(u)}</loc><lastmod>{UPDATED}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if u == 'index.html' else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
if not (ROOT / "ads.txt").exists():
    (ROOT / "ads.txt").write_text("google.com, pub-1558743317014653, DIRECT, f08c47fec0942fa0\n")
print("built", len(urls) + 1, "pages", "(preview)" if PREVIEW else "(live)")
write_redirects(ROOT)
