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
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
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
{AD.format(file)}
</main>
<footer><div class="wrap"><div class="fgrid">
<div><a class="brand" href="{href("index.html")}" style="color:#fff">{LOGO}Padel <b style="color:#e8f84a">Glass Box</b></a><p style="margin-top:12px">Free padel tools and plain-English guides: find your racket, keep score, learn the rules and the shots.</p></div>
<div><strong style="color:#fff">Tools and guides</strong><ul>{"".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in NAV)}<li><a href="{href("glossary.html")}">Glossary</a></li></ul></div>
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
     "Answer 3 questions and find the padel racket shape, weight, balance, core and face that suit your level and style. Free and instant.", finder, finder_faq, "Racket finder")

# ---------------- SCORE KEEPER ----------------
score = f'''<header class="hero" style="padding-bottom:10px"><div class="wrap"><h1>Padel score keeper.</h1>
<p class="lead">Put your phone by the net and tap the side that wins each point. It handles deuce, golden point, tie-breaks and sets, and remembers the score if you close the page.</p></div></header>
<section style="padding-top:10px"><div class="wrap"><div class="score" id="score">
<div class="score-top"><div class="seg" id="mode" role="group" aria-label="Deuce format"><button type="button" data-v="adv" aria-pressed="true">Advantage</button><button type="button" data-v="golden" aria-pressed="false">Golden point</button></div>
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
<div class="card"><h3>Deuce</h3><p>At 40-40 there are three official options: classic advantage, golden point (one deciding point) or the newer Star Point. Agree on one before you start.</p></div>
<div class="card"><h3>Sets and tie-breaks</h3><p>A set goes to six games with a two-game lead. At 6-6 a tie-break is played to 7 points, two clear. Most matches are best of three sets.</p></div>
<div class="card"><h3>Golden point side</h3><p>With golden point, the receiving pair chooses which player receives the deciding serve.</p></div>
</div></div></section>'''
score_faq = [
    ("How do you keep score in padel?", "Like tennis: 0, 15, 30, 40 and game. Sets go to six games with a two-game lead, and a tie-break decides 6-6."),
    ("What is the golden point in padel?", "At 40-40, one deciding point is played. The receiving pair chooses which side receives, and whoever wins that point wins the game."),
    ("What is Star Point in padel?", "Star Point is a deuce format added in the 2026 international rules. Play goes through advantage points before a final deciding point. Tournaments say in advance which format they use."),
    ("Does this score keeper save my match?", "Yes. The score is saved on your phone, so you can lock the screen or close the page and carry on."),
]
page("score.html", "Padel Score Keeper: Free Scoreboard for Your Phone | Padel Glass Box",
     "Free padel score keeper for your phone. Tap to score, with advantage or golden point, tie-breaks, sets, undo and server tracking. No app needed.", score, score_faq, "Score keeper")

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
<div class="card"><h3>The serve</h3><p>Stand behind the service line, bounce the ball, and hit it underhand at or below waist height. It must land in the box diagonally opposite. You get two attempts per point.</p></div>
<div class="card"><h3>A serve is a fault if</h3><p>it lands outside the diagonal box, it's hit above the waist, you miss the ball, or after bouncing in the box it hits the metal mesh.</p></div>
<div class="card"><h3>Receiving</h3><p>The receiver must let the serve bounce before hitting it. After that, players can volley freely.</p></div>
<div class="card"><h3>Using the walls</h3><p>On your side, the ball can bounce once and then hit the walls; you can still play it. You may also hit the ball into your own walls to get it back over the net.</p></div>
<div class="card"><h3>Lost points</h3><p>You lose the point if the ball bounces twice, if your shot hits the opponents' wall or fence before the ground, or if the ball touches your body.</p></div>
<div class="card"><h3>Scoring</h3><p>15, 30, 40, game, sets to six with a tie-break at 6-6. At deuce, the organiser chooses advantage, golden point or Star Point.</p></div>
</div></div></section>'''
rules_faq = [
    ("Can you serve overarm in padel?", "No. The padel serve is always underhand: you bounce the ball and hit it at or below waist height."),
    ("Can the ball hit the wall in padel?", "Yes, after it bounces on the ground on your side. If your shot hits the opponents' wall before bouncing on their ground, you lose the point."),
    ("What happens if the ball hits a player?", "The player's team usually loses the point, with only a few exceptions in the official rules."),
    ("How high is a padel net?", "88 cm in the middle and 92 cm at the posts."),
    ("Where must the server stand?", "Behind the service line, which is 6.95 m from the net, serving diagonally into the opposite service box."),
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
kit = ["A padel racket (a round one is easiest to start with)", "Padel balls, not tennis balls (they're slightly softer)", "Court shoes with good grip for artificial grass", "A wrist strap on your racket, and wear it", "Comfortable sports clothes and water", "A booked court and three other players"]
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
<div class="card"><h3>Start with a lesson</h3><p>One group lesson teaches the serve and the walls much faster than working it out alone.</p></div>
</div></div></section>'''
beg_faq = [
    ("What do I need for my first padel game?", "A racket, padel balls, court shoes with grip, comfy sports clothes and water. Many clubs rent rackets if you don't have one yet."),
    ("Can I use tennis balls for padel?", "It's better not to. Padel balls are made for the sport and are slightly softer, so the game plays the way it should."),
    ("Do I need special shoes for padel?", "Shoes with good grip for artificial grass courts help you move safely. Running shoes slip more easily."),
]
page("beginners.html", "Padel for Beginners: First Match Checklist | Padel Glass Box",
     "Everything you need for your first padel match: a kit checklist, the rules to know, and where to find courts and beginner sessions.", beg, beg_faq, "Beginners")

# ---------------- GLOSSARY ----------------
gl = "".join(f"<div><b>{e(t)}</b><span>{e(d)}</span></div>" for t, d in D["glossary"])
glos = f'''<header class="hero"><div class="wrap"><h1>Padel words, decoded.</h1>
<p class="lead">Padel borrows lots of Spanish. Search any word you've heard on court.</p></div></header>
<section style="padding-top:10px"><div class="wrap"><label class="sr-only" for="gsearch">Search the glossary</label><input class="search" id="gsearch" type="search" placeholder="Search: bandeja, golden point, malla..."><div class="gl" id="glist">{gl}</div></div></section>'''
page("glossary.html", "Padel Glossary: Every Term Explained | Padel Glass Box",
     "Padel terms explained in plain English: bandeja, víbora, chiquita, bajada, golden point, drive, revés and more. Searchable and free.", glos, None, "Glossary")

# ---------------- ABOUT / PRIVACY / 404 ----------------
page("about.html", f"About {SITE}", f"About {SITE}, a free set of padel tools and guides, and how to contact us.",
     f'<section><div class="wrap" style="max-width:760px"><h1>About {SITE}</h1><p>{SITE} makes free, simple padel tools: a racket finder, a score keeper, an interactive rules court and a shot library.</p><h2>How we check facts</h2><p>Rules follow the International Padel Federation (FIP). Equipment advice is general guidance checked against several trusted guides; we don\'t take payment to recommend gear.</p><h2>Contact</h2><p>Email <strong>[your email address]</strong>.</p></div></section>')
page("privacy.html", f"Privacy Policy | {SITE}", f"{SITE} privacy policy covering cookies, Google AdSense, Google Analytics and affiliate links.",
     f'<section><div class="wrap" style="max-width:760px"><h1>Privacy policy</h1><p>Last updated: {e(UPDATED)}.</p><h2>What we collect</h2><p>No sign-ups. Your score, checklist ticks and quiz answers are saved only in your own browser.</p><h2>Analytics</h2><p>We use Google Analytics to count visits and see which pages are popular. It uses cookies and collects details like pages viewed, approximate location and device type.</p><h2>Advertising</h2><p>This site uses Google AdSense. Google and its partners use cookies to show ads based on your visits to this and other websites. You can turn off personalised ads at <a href="https://adssettings.google.com">Google Ads Settings</a>. Learn more at <a href="https://policies.google.com/technologies/partner-sites">policies.google.com/technologies/partner-sites</a>.</p><h2>Affiliate links</h2><p>Some links may be affiliate links. If you buy through them, we may earn a small fee at no extra cost to you.</p><h2>Contact</h2><p>Email <strong>[your email address]</strong>.</p></div></section>')
page("404.html", f"Page not found | {SITE}", "This page doesn't exist.",
     f'<section><div class="wrap"><h1>That one went out.</h1><p class="lead">This page doesn\'t exist.</p><a class="btn lime" href="{href("index.html")}">Back to the home page</a></div></section>')

urls = ["index.html", "racket-finder.html", "score.html", "rules.html", "shots.html", "beginners.html", "glossary.html", "about.html", "privacy.html"]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{canon(u)}</loc><lastmod>{UPDATED}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if u == 'index.html' else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
if not (ROOT / "ads.txt").exists():
    (ROOT / "ads.txt").write_text("google.com, pub-1558743317014653, DIRECT, f08c47fec0942fa0\n")
print("built", len(urls) + 1, "pages", "(preview)" if PREVIEW else "(live)")
