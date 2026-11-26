# ---------------- DEMAND RUN 4 (26 Nov 2026): padel cost calculator (DEMAND E4), 30-day beginner plan (competitor watch 26 Nov #3) ----------------
# Executed from build.py after skills.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, json, checklist()).

# ---------- 1. HOW MUCH DOES PADEL COST? CALCULATOR ----------
def cq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-pc="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
def cnum(id_, label, val, step="1"):
    return f'<div class="q"><h3><label for="pc-{id_}">{e(label)}</label></h3><input class="search" id="pc-{id_}" type="number" min="0" step="{step}" value="{val}" inputmode="decimal" style="margin:0"></div>'
PC_DEF = {
    "uk": {"cur": "£", "court": 40, "rent": 0, "racket": 50, "shoes": 60, "can": 6, "mem": 0, "disc": 0, "lesson": 20},
    "us": {"cur": "$", "court": 40, "rent": 0, "racket": 100, "shoes": 100, "can": 9, "mem": 0, "disc": 0, "lesson": 30},
    "qa": {"cur": "QAR ", "court": 200, "rent": 40, "racket": 0, "shoes": 300, "can": 30, "mem": 0, "disc": 0, "lesson": 120},
    "eu": {"cur": "€", "court": 30, "rent": 0, "racket": 60, "shoes": 70, "can": 6, "mem": 0, "disc": 0, "lesson": 20},
}
pc_form = f'''{cq("reg", "Where do you play?", [("uk", "UK (£)"), ("us", "US ($)"), ("qa", "Qatar (QAR)"), ("eu", "Europe / other (€)")], "uk")}
<div class="gen-nums">{cnum("court", "Court price for the whole booking", 40)}{cnum("n", "Players splitting the court", 4)}</div>
{cq("len", "Booking length", [("60", "60 min"), ("90", "90 min")], "60")}
{cq("wk", "How often do you play?", [("2", "Twice a month"), ("4", "Once a week"), ("8", "Twice a week"), ("12", "3 times a week")], "4")}
<div class="gen-nums">{cnum("rent", "Racket hire per session (0 if your own)", 0)}{cnum("can", "Price of a can of 3 balls", 6, "0.5")}</div>
<div class="gen-nums">{cnum("racket", "Your racket (0 if you hire)", 50)}{cnum("shoes", "Your padel shoes (0 if you have some)", 60)}</div>
<div class="gen-nums">{cnum("lesson", "Lessons or clinics per month: total cost", 20)}{cnum("mem", "Club membership per month (0 if none)", 0)}</div>
<div class="gen-nums">{cnum("disc", "Member discount on court hire, %", 0)}<div class="q"><h3>Kit lasts about</h3><select class="search" id="pc-life" style="margin:0"><option value="12">1 year</option><option value="18">18 months</option><option value="24">2 years</option></select></div></div>'''
pc_rows = [
    ("Court hire, whole court, 1 hour", "£20 to £80 in London (Time Out, Mar 2025); many London courts about £60, off-peak from about £26 (City AM)", "$20 to $60 (Padel Browser, Jun 2026); $40 to $140 (Bounce, Jul 2026)", "QAR 150 to 300 in Doha (Qatar Living, Aug 2026)"),
    ("Court hire, each of 4 players, 1 hour", "About £5 to £20; about £15 at a £60 London court", "$5 to $15 (Padel Browser); $10 to $35 (Bounce)", "QAR 40 to 75"),
    ("Entry-level racket", "Just under £50 for basic models; good ones run into the hundreds (City AM)", "$60 to $130 (Padel Browser); $120 to $170 for a useful beginner racket (Bounce)", "Racket hire about QAR 30 to 50 a session"),
    ("Padel shoes", "No reliable published range found", "$80 to $140 (Padel Browser); $60 to $180 (Bounce)", "No reliable published range found"),
    ("Can of 3 balls", "No reliable published range found", "$8 to $12 (Padel Browser); $7 to $10 (Bounce)", "Varies by club (Qatar Living says don't assume a fixed price)"),
    ("Club membership, per month", "Varies by club", "$30 to $350 (Padel Browser, Oct 2026); $60 to $250 standard tiers (Bounce)", "No reliable published range found"),
    ("Lessons", f'Private about £40 to £80 an hour, groups £10 to £30 each (<a href="{href("padel-lessons.html")}">our lessons guide</a>)', "Private about $50 to $160 an hour, clinics $20 to $60 each", "No reliable published range found"),
]
pc_tbl = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in pc_rows)
pc = f'''<header class="hero"><div class="wrap"><h1>How much does padel cost? Work out your real cost.</h1>
<p class="lead">Court hire, rackets, shoes, balls, lessons and memberships: see published prices for the UK, the US and Qatar, then put in your own numbers to get your cost per game, per month and per year.</p>
{quick("Most of the cost of padel is court hire, and four players split it. In the UK a court is about £20 to £80 an hour (about £5 to £20 each), and in the US about $20 to $60 an hour, roughly $5 to $15 each, with busy city clubs higher. A beginner racket costs from just under £50 or about $60 to $130, and many clubs rent rackets. Playing once a week, court fees alone come to roughly £20 to £80 or $20 to $140 a month, plus balls and kit.", "2026-11-26")}
<p class="muted" style="margin-top:8px;font-size:.9rem">The monthly figure in the quick answer is our own sum: four one-hour sessions at the published per-player court prices.</p></div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="pc">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Padel cost calculator</h2>
<p class="muted" style="margin-top:0">Pick where you play to load example prices, then change any number to match your club. Saved on this device only.</p>
{pc_form}
<p class="muted" style="margin:0;font-size:.92rem">Example prices are rounded figures inside the published ranges below, not quotes. Balls: we assume one new can every 4 sessions, shared by the players (see <a href="{href("padel-balls.html")}">when to change padel balls</a>).</p>
</div>
<aside class="result" id="pc-out" aria-live="polite"><h2 id="pc-h">Your padel cost</h2><p id="pc-p"></p><dl class="spec" id="pc-spec"></dl><div id="pc-bars" class="pc-bars"></div><p id="pc-memo"></p><p id="pc-tip"></p><p id="pc-next" class="wr-src"></p></aside>
</div></section>
<script>window.PCDEF={json.dumps(PC_DEF)};window.PCGO={json.dumps({k: go(k) for k in ("padel-round-rackets", "padel-shoes", "padel-balls")})};</script>
{AD.format("cost-mid")}
<section><div class="wrap"><div class="sh"><h2>Padel prices in the UK, US and Qatar</h2><p class="muted">Published 2025 and 2026 figures, rounded. Prices change often and big-city clubs sit at the top of each range.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">What</th><th scope="col">UK</th><th scope="col">US</th><th scope="col">Qatar</th></tr></thead><tbody>{pc_tbl}</tbody></table></div>
<p class="muted" style="margin-top:12px">Qatar figures come from one guide only (Qatar Living, Aug 2026), so treat them as a rough guide. We found no reliable published price ranges for the UAE or mainland Europe, so the calculator's Europe example is a placeholder: put in your club's prices.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How much does it cost to start playing padel?</h2></div><div class="grid">
<div class="card"><span class="pill b">Almost nothing</span><h3 style="margin-top:10px">Try it first</h3><p>Book a court with three friends, hire rackets at the club and wear trainers you already have. You pay your share of the court plus racket hire. Some clubs also lend community rackets and balls.</p></div>
<div class="card"><span class="pill b">Starter kit</span><h3 style="margin-top:10px">Once you play every week</h3><p>A round beginner racket, a pair of padel or clay-court tennis shoes and a can of balls. In the US a full beginner set-up is about $100 to $250 (Padel Browser). Our <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets guide</a> and <a href="{href("padel-shoes.html")}">shoe finder</a> help you buy once.</p></div>
<div class="card"><span class="pill i">Regular player</span><h3 style="margin-top:10px">Two or more games a week</h3><p>Court hire becomes the big cost. Padel Browser puts a regular weekly US player at about $1,500 to $4,000 a year. This is where off-peak slots and memberships start to pay.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why is padel so expensive?</h2></div>
<div class="card"><p>Padel is not expensive per person when four people share the court, but a court booking can look expensive at first. The main reasons:</p>
<ul style="margin:8px 0 12px;padding-left:20px;display:grid;gap:6px">
<li><strong>Courts cost a lot to build.</strong> A single court with glass walls usually costs tens of thousands to build; the LTA's loan scheme uses £75,000 for a floodlit outdoor court and £130,000 for a covered one (via Bounce). See <a href="{href("padel-court-cost.html")}">how much a padel court costs</a>.</li>
<li><strong>Many courts are indoors or in city centres</strong>, where rent, heating and lighting add to the price.</li>
<li><strong>Demand is high and courts are few</strong>, so peak evening and weekend slots cost the most.</li>
<li><strong>Kit is optional at first.</strong> Rackets can be hired, so buying expensive gear early is a choice, not a must.</li>
</ul>
<p>Reasons summarised in our own words from City AM, Bounce (23 Jul 2026) and Padel Browser (8 Jun 2026).</p></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How can I play padel for less?</h2></div><div class="grid">
<div class="card"><h3>Play off-peak</h3><p>Daytime and early-morning slots are usually much cheaper than evenings and weekends. In one US club example, members paid $10 off-peak against $20 peak (Padel Browser, Oct 2026).</p></div>
<div class="card"><h3>Always split four ways</h3><p>Fill the court. A singles booking of two players doubles your share. Run a social night with the <a href="{href("americano.html")}">Americano generator</a> to fill courts with 8 or more players.</p></div>
<div class="card"><h3>Check if a membership pays</h3><p>Put the monthly fee and the member discount into the calculator. It tells you how many games a month you need before the membership is cheaper.</p></div>
<div class="card"><h3>Don't overbuy the racket</h3><p>A beginner improves just as fast with a sensible round racket. Last season's models are often discounted. Use the <a href="{href("racket-finder.html")}">racket finder</a> before you shop.</p></div>
<div class="card"><h3>Make balls last</h3><p>For social games a can lasts a few sessions. Share the cost and change them when the bounce goes: <a href="{href("padel-balls.html")}">ball bounce test</a>.</p></div>
<div class="card"><h3>Group lessons first</h3><p>Clinics cost a fraction of a private lesson per person. Compare quotes in the <a href="{href("padel-lessons.html")}">lesson cost checker</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>New to padel?</h3><p>Follow the <a href="{href("padel-beginner-plan.html")}">30-day beginner plan</a>, then check the <a href="{href("beginners.html")}">first-match checklist</a>.</p></div>
<div class="card"><h3>Ready to buy kit?</h3><p>See the <a href="{href("padel-equipment.html")}">padel equipment planner</a> for everything you need and what you can skip.</p></div>
<div class="card"><h3>Building a court?</h3><p>That's a different budget: see the <a href="{href("padel-court-cost.html")}">padel court cost planner</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Starter kit</h3><p>Only buy when you play every week. A round racket, grippy shoes and fresh balls are all a beginner needs.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 26 Nov 2026. UK: Time Out London "A comprehensive map of London's padel courts with pricing" (19 Mar 2025: £20 to £80 an hour), City AM "Padel firm founder calls for operators to lower court rental costs" (London courts sometimes over £95 an hour, many about £60 for four over 60 minutes, off-peak about £26, entry rackets just under £50, community rackets and balls). US: Padel Browser "How much does padel cost in the US" (8 Jun 2026) and "Padel club membership cost in the US" (11 Oct 2026), Bounce "Why is padel so expensive" (23 Jul 2026, including LTA loan-scheme build figures). Qatar: Qatar Living "Padel in Qatar: where to play, costs and booking" (18 Aug 2026). Lesson ranges from our <a href="{href("padel-lessons.html")}">padel lessons guide</a>. Not read: Tienda Padel Point cost FAQ (page would not load). Example prices in the calculator and the monthly estimate are our own, labelled. We have no link with any club named in these sources.</p></div></section>'''
pc_faq = [
    ("How much does it cost to play padel?", "Mostly your share of the court. A court costs about £20 to £80 an hour in the UK and about $20 to $60 in the US, split four ways, so roughly £5 to £20 or $5 to $15 each. Busy city clubs at peak times cost more."),
    ("How much is a padel court per hour in the UK?", "About £20 to £80 an hour in London, with many courts around £60 for four players (about £15 each) and off-peak slots from about £26. Prices outside London are often lower."),
    ("How much does padel cost in the US?", "Court hire is usually about $20 to $60 an hour, roughly $5 to $15 each, though some city clubs charge more. A beginner set-up of racket, shoes and balls costs about $100 to $250."),
    ("Why is padel so expensive?", "Courts are costly to build and many are indoors or in cities, and demand is higher than the number of courts. Split four ways, though, an hour of padel is often similar to other club sports."),
    ("How much is a padel racket for a beginner?", "Basic rackets start just under £50 in the UK and about $60 to $130 in the US. You don't need one to start: most clubs hire rackets."),
    ("Is a padel club membership worth it?", "Usually only if you play often. Divide the monthly fee by what you save on each court booking: that is how many games a month you need before it pays. The calculator above does this for you."),
    ("Do I need to buy padel balls?", "Someone brings a can of three to each game, and it is usual to share the cost. A can lasts a few social sessions before the bounce goes."),
]
page("padel-cost.html", "How Much Does Padel Cost? Free Padel Cost Calculator | Padel Glass Box",
     "How much does padel cost? Court hire is about £20-£80 or $20-$60 an hour, split 4 ways. See UK, US and Qatar prices and work out your cost per game, month and year.",
     pc, pc_faq, "Padel cost")

# ---------- 2. 30-DAY PADEL BEGINNER PLAN ----------
# (day, kind, title, what, [(file, link text)])
BP = [
    (1, "home", "Learn how padel works", "Read the four rules every beginner needs: underarm serve, one bounce, walls after the bounce, and the score.", [("beginners.html", "Beginner checklist"), ("rules.html", "Rules court")]),
    (2, "home", "Hold the racket right", "Learn the continental grip. Hold it for a few minutes while you watch TV, and do 20 slow shadow swings each side.", [("padel-grip.html", "Grip guide")]),
    (3, "court", "First session", "Book a court or a beginner clinic. Hire a racket. Rally gently from the back and let balls come off the back glass.", [("padel-lessons.html", "Lessons and clinics"), ("warm-up.html", "Warm-up timer")]),
    (4, "rest", "Rest and review", "Rest. Write down the two things that felt hardest in your first session.", []),
    (5, "home", "Learn the walls", "Read which balls you can play off the glass and the fence, and which are out.", [("wall-rules.html", "Wall rules")]),
    (6, "court", "Session 2: back glass", "Spend 15 minutes only on balls off the back glass. Wait, turn sideways, hit softly to the middle.", [("drills.html", "Drills planner")]),
    (7, "home", "Watch padel", "Watch one pro match. Notice how both players move up and back together.", [("padel-rankings.html", "Who's who")]),
    (8, "home", "Serve at home", "Practise the serve motion: bounce, hit below the waist, point at the far box. 20 times.", [("how-to-serve-padel.html", "How to serve")]),
    (9, "court", "Session 3: serve and return", "Serve 30 balls and track how many land in. Then return 20 serves cross-court.", [("how-to-serve-padel.html", "Serve tracker")]),
    (10, "home", "Where to stand", "Learn the two positions: both at the net, or both at the back. Never one up and one back for long.", [("positioning.html", "Positioning guide")]),
    (11, "rest", "Rest", "Rest day. Stretch your shoulders, wrist and calves.", [("padel-injuries.html", "Injury prevention")]),
    (12, "court", "Session 4: first real game", "Play a full set with scoring. Agree on golden point or advantage before you start.", [("score.html", "Score keeper"), ("golden-point-star-point.html", "Golden point")]),
    (13, "home", "Find your level", "Take the level test so you can join open matches and clinics at the right level.", [("level-calculator.html", "Level calculator")]),
    (14, "home", "Week 2 check", "Look back at your two hardest things from day 4. Are they easier? Pick one to work on next.", [("fix-my-padel.html", "Problem fixer")]),
    (15, "court", "Session 5: volleys", "At the net, 2 to 3 metres back. Short punch volleys to the middle, no big swing. 50 balls.", [("shots.html", "Shot library")]),
    (16, "home", "Pick a side", "Left or right? Take the one-minute quiz so you and your partner know who covers what.", [("which-side-padel.html", "Side quiz")]),
    (17, "rest", "Rest", "Rest day.", []),
    (18, "court", "Session 6: the lob", "The lob is the most useful beginner shot. Hit 30 lobs high over the net players.", [("padel-tactics.html", "Tactics trainer")]),
    (19, "home", "Etiquette", "Learn the unwritten rules: calls, balls, warm-up and who brings what.", [("padel-etiquette.html", "Etiquette quiz")]),
    (20, "home", "Shoes and racket", "If you play every week now, think about your own racket and padel shoes. Don't overspend.", [("racket-finder.html", "Racket finder"), ("padel-shoes.html", "Shoe finder")]),
    (21, "court", "Session 7: track a match", "Play a match and log your errors by shot. The shot with the most errors is next week's job.", [("padel-match-tracker.html", "Match tracker")]),
    (22, "rest", "Rest", "Rest day. Check your budget if you are playing more.", [("padel-cost.html", "Cost calculator")]),
    (23, "home", "Fix your biggest leak", "Read the fix for the shot with the most errors from day 21.", [("fix-my-padel.html", "Problem fixer")]),
    (24, "court", "Session 8: fix it", "Spend 20 minutes on that one shot, then play games.", [("drills.html", "Drills planner")]),
    (25, "home", "Tactics basics", "Do the tactics trainer: what shot to play when they are at the net and you are at the back.", [("padel-tactics.html", "Tactics trainer")]),
    (26, "court", "Session 9: social play", "Join an open match, a ladder or an Americano night and play new people at your level.", [("americano.html", "Americano"), ("ladder.html", "Ladder")]),
    (27, "rest", "Rest", "Rest day.", []),
    (28, "home", "Bandeja preview", "Read about the bandeja, the safe overhead. You will learn it in the coming weeks.", [("bandeja-vs-vibora.html", "Bandeja vs víbora")]),
    (29, "court", "Session 10: test match", "Play a full match and track it again. Compare your errors with day 21.", [("padel-match-tracker.html", "Match tracker")]),
    (30, "home", "Plan the next month", "Make a 4-week plan for your level and goal.", [("padel-training-plan.html", "Training plan"), ("padel-improvement-guide.html", "What to learn next")]),
]
BP_KIND = {"court": ("On court", "a"), "home": ("At home, 10-20 min", "b"), "rest": ("Rest", "i")}
def _bpday(d, kind, title, what, links):
    lab, cls = BP_KIND[kind]
    ln = " · ".join(f'<a href="{href(f)}">{e(t)}</a>' for f, t in links)
    return (f'<li class="bp-day" data-day="{d}" data-kind="{kind}"><label class="bp-tick"><input type="checkbox" aria-label="Day {d} done"></label>'
            f'<div><div class="bp-top"><b>Day {d}: {e(title)}</b> <span class="pill {cls}">{lab}</span></div><p>{e(what)}</p>'
            + (f'<p class="bp-links">{ln}</p>' if ln else "") + '</div></li>')
def _bpweek(n, lo, hi, head):
    return f'<h3 class="bp-wk">Week {n}: {e(head)}</h3><ol class="bp-list">' + "".join(_bpday(*x) for x in BP if lo <= x[0] <= hi) + "</ol>"
bp_weeks = (_bpweek(1, 1, 7, "rules, grip and the back glass") + _bpweek(2, 8, 14, "serve, position and a real game")
            + _bpweek(3, 15, 21, "volleys, lobs and your first stats") + _bpweek(4, 22, 30, "fix one thing and play new people"))
n_court = sum(1 for x in BP if x[1] == "court")
bp = f'''<header class="hero"><div class="wrap"><h1>30-day padel beginner plan: a day-by-day checklist.</h1>
<p class="lead">New to padel? Follow one short task a day for 30 days: {n_court} court sessions, short home tasks and rest days. Tick each day off and the plan remembers where you are.</p>
{quick(f"A good first month of padel is about {n_court} court sessions (two or three a week) with short tasks between them. Week 1: rules, the grip and balls off the back glass. Week 2: the serve, where to stand and a first scored game. Week 3: volleys, the lob and tracking your errors. Week 4: fix your biggest weakness and play new people. Rest at least one day between hard sessions.", "2026-11-26")}
<p class="muted" style="margin-top:8px;font-size:.9rem">General coaching advice in our own words. Missed a day? Just carry on from the next one.</p></div></header>
<section style="padding-top:10px"><div class="wrap" id="bp" style="max-width:860px">
<div class="card bp-head"><div><h2 style="font-size:1.3rem;margin:0 0 4px">Your progress</h2><p class="muted" id="bp-count" style="margin:0">0 of 30 days done</p></div>
<div class="prog" style="flex:1 1 200px;margin:0"><i id="bp-bar"></i></div>
<div class="bp-btns"><button type="button" class="btn sm" id="bp-next">Go to my next day</button><button type="button" class="btn ghost sm" id="bp-reset">Start again</button></div>
<p id="bp-today" class="muted" style="margin:0;flex-basis:100%" aria-live="polite"></p></div>
<div class="opts" id="bp-filter" role="group" aria-label="Show days" style="margin:14px 0"><button type="button" class="opt" data-v="all" aria-pressed="true">All days</button><button type="button" class="opt" data-v="court" aria-pressed="false">Court sessions</button><button type="button" class="opt" data-v="home" aria-pressed="false">Home tasks</button><button type="button" class="opt" data-v="todo" aria-pressed="false">Not done yet</button></div>
<div class="card">{bp_weeks}</div>
<p class="muted" style="font-size:.9rem">Your ticks are saved on this device only.</p>
</div></section>
{AD.format("bp-mid")}
<section><div class="wrap"><div class="sh"><h2>What should I learn first in padel?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Week</th><th scope="col">Main skill</th><th scope="col">You know it's working when</th></tr></thead><tbody>
<tr><td>1</td><td>Grip and the back glass</td><td>You can let a ball come off the back glass and return it softly most of the time</td></tr>
<tr><td>2</td><td>Serve and position</td><td>Most of your serves land in, and you move up and back with your partner</td></tr>
<tr><td>3</td><td>Volley and lob</td><td>You can keep a short volley rally going and push opponents back with a lob</td></tr>
<tr><td>4</td><td>Fixing one weakness</td><td>Your errors on your worst shot go down from one tracked match to the next</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How often should a beginner play padel?</h2></div><div class="grid">
<div class="card"><h3>Two or three times a week</h3><p>Enough to remember what you learned last time, with time to recover. Once a week still works; the plan just takes longer.</p></div>
<div class="card"><h3>Rest between hard sessions</h3><p>New players often get sore calves, shoulders or elbows. Warm up first and stop if something hurts. See <a href="{href("padel-injuries.html")}">padel injuries and prevention</a>.</p></div>
<div class="card"><h3>Take a lesson early</h3><p>One beginner clinic in week 1 makes the walls and the serve much easier. See <a href="{href("padel-lessons.html")}">what lessons cost</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next after 30 days?</h2></div><div class="grid">
<div class="card"><h3>A plan for month two</h3><p>The <a href="{href("padel-training-plan.html")}">training plan generator</a> builds 4 weeks of sessions for your level and goal.</p></div>
<div class="card"><h3>What to learn next</h3><p>The <a href="{href("padel-improvement-guide.html")}">improvement guide</a> lists three priorities for each level.</p></div>
<div class="card"><h3>What it will cost</h3><p>Playing more? Check your monthly budget with the <a href="{href("padel-cost.html")}">padel cost calculator</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Your first own kit</h3><p>Hire a racket for the first weeks. If you play every week by week 3, a round racket and grippy shoes are worth it.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Checked 26 Nov 2026 against: LTA Padel "How to get started playing padel as a beginner"; The Padel School "Starting padel? Here's what you need" and its Court Ready pathway; Padel Browser "How to get better at padel"; Tienda Padel Point weekly beginner training routine. Rules points follow FIP rules as used on our <a href="{href("rules.html")}">rules page</a>. The day order, tasks and wording are our own general coaching advice.</p></div></section>'''
bp_faq = [
    ("How long does it take to learn padel?", "Most people can rally in their first session. In about a month of playing two or three times a week you can usually serve, play off the back glass and play a full scored game."),
    ("What should I practise first in padel?", "The continental grip, letting the ball come off the back glass before you hit it, and a steady underarm serve. Power comes later."),
    ("How many times a week should a beginner play padel?", "Two or three sessions a week with a rest day between is a good start. Once a week also works, just more slowly."),
    ("Do I need lessons to start padel?", "No, but one beginner clinic early on makes the walls and the serve much easier to learn."),
    ("Can I learn padel in 30 days?", "You can learn the basics and play proper games in 30 days. Getting good takes longer: steady club level usually takes a year or two."),
]
page("padel-beginner-plan.html", "30-Day Padel Beginner Plan: Day-by-Day Checklist | Padel Glass Box",
     f"A free 30-day padel beginner plan: one short task a day, {n_court} court sessions, home tasks and rest days. Tick off each day, see your progress and know what to do next.",
     bp, bp_faq, "30-day beginner plan")

DEMAND_PAGES = ["padel-cost.html", "padel-beginner-plan.html"]
exec((ROOT / "demand2.py").read_text())
