# ---------------- SKILLS: how to serve + serve tracker, padel tactics trainer, improvement guide hub (26 Nov 2026, DEMAND P3, I5, I6) ----------------
# Executed from build.py after improve.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, json).
# Sources: LTA Padel "How to serve in padel: expert tips"; Padel Browser "How to serve in padel"; The Padel School "How to win a padel point";
# HEAD "Padel tactics to improve your game"; FIP rules as already used on /serve-rules. Coaching advice is general, in our own words.

# ---------- court drawing (top view, 10 x 20 m, 10 px per m, our side at the bottom) ----------
def court_svg(us=(), them=(), ball=None, arrow=None, label=""):
    P = 8
    X = lambda x: P + x * 10
    Y = lambda y: P + y * 10
    s = [f'<svg class="tc-svg" viewBox="0 0 116 216" role="img" aria-label="{e(label)}">',
         f'<rect x="{X(0)}" y="{Y(0)}" width="100" height="200" rx="2" fill="#1f5fd1" stroke="#cfe0ff" stroke-width="1.6"/>',
         f'<line x1="{X(0)}" y1="{Y(10)}" x2="{X(10)}" y2="{Y(10)}" stroke="#fff" stroke-width="2.4"/>',
         f'<line x1="{X(0)}" y1="{Y(3.05)}" x2="{X(10)}" y2="{Y(3.05)}" stroke="#fff" stroke-width=".9"/>',
         f'<line x1="{X(0)}" y1="{Y(16.95)}" x2="{X(10)}" y2="{Y(16.95)}" stroke="#fff" stroke-width=".9"/>',
         f'<line x1="{X(5)}" y1="{Y(3.05)}" x2="{X(5)}" y2="{Y(16.95)}" stroke="#fff" stroke-width=".9"/>']
    if arrow:
        (x1, y1), (x2, y2) = arrow
        s.append(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" stroke="#e8f84a" stroke-width="1.6" stroke-dasharray="4 3"/>')
    for x, y in them:
        s.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="5.5" fill="#ff9b78" stroke="#0b1530" stroke-width="1.2"/>')
    for i, (x, y) in enumerate(us):
        s.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="5.5" fill="#fff" stroke="#0b1530" stroke-width="1.2"/><text x="{X(x)}" y="{Y(y) + 2.6}" text-anchor="middle" font-size="7" font-weight="700" fill="#0b1530">{"Y" if i == 0 else "P"}</text>')
    if ball:
        s.append(f'<circle cx="{X(ball[0])}" cy="{Y(ball[1])}" r="2.6" fill="#e8f84a" stroke="#0b1530" stroke-width=".8"/>')
    s.append("</svg>")
    return "".join(s)

# ---------- 1. HOW TO SERVE + SERVE PRACTICE TRACKER ----------
SV_TARGETS = [("wide", "Wide (side glass)"), ("body", "At the body"), ("t", "Down the T (centre)")]
SV_RESULTS = [("hit", "Hit the target", "in"), ("in", "In the box, missed target", "in"), ("net", "Fault: into the net", "f"),
              ("long", "Fault: long (past service line)", "f"), ("wide", "Fault: wide or wrong box", "f"), ("mesh", "Fault: hit the fence", "f"), ("foot", "Fault: foot or height", "f")]
SV_TIPS = {
    "net": "Most of your faults go into the net. Let the ball drop to about knee height, keep contact just below the waist, and swing low to high so the ball clears the net by about half a metre.",
    "long": "Most faults are long. Slow down to about two thirds of your full pace and add a little slice. Placement beats power on the padel serve.",
    "wide": "Most faults are wide or in the wrong box. Turn your front shoulder to the target box before you drop the ball, and drop it in the same place each time, just in front of your front foot.",
    "mesh": "Your serves bounce in and then hit the metal fence. That is a fault. Aim a little further from the side, so the ball reaches the glass, not the mesh.",
    "foot": "Foot or height faults. Stand clearly behind the service line, keep at least one foot on the ground, and hit at or below the waist. Check the details on the serve rules page.",
}
sv_tgt = "".join(f'<button type="button" class="opt" data-v="{k}" aria-pressed="{"true" if i == 0 else "false"}">{e(t)}</button>' for i, (k, t) in enumerate(SV_TARGETS))
sv_res = "".join(f'<button type="button" class="btn sm{" lime" if k == "hit" else (" ghost" if c == "f" else "")}" data-r="{k}">{e(t)}</button>' for k, t, c in SV_RESULTS)
sv_js = {"t": dict(SV_TARGETS), "r": {k: [t, c] for k, t, c in SV_RESULTS}, "tip": SV_TIPS}

def box_svg():
    # our service box seen from the server's side (opponents' right-hand box): 5 m wide x 6.95 m deep
    return ('<svg class="sv-box" viewBox="0 0 240 200" role="img" aria-label="Diagram of the three padel serve targets in the service box: wide near the side glass, at the body, and down the T near the centre line">'
            '<rect x="20" y="20" width="200" height="139" fill="#1f5fd1" stroke="#cfe0ff" stroke-width="2"/>'
            '<line x1="220" y1="20" x2="220" y2="159" stroke="#fff" stroke-width="2"/><text x="120" y="14" text-anchor="middle" font-size="11" fill="currentColor">Service line (far end of the box)</text>'
            '<text x="120" y="176" text-anchor="middle" font-size="11" fill="currentColor">Net</text><line x1="10" y1="160" x2="230" y2="160" stroke="currentColor" stroke-width="3"/>'
            '<text x="14" y="95" font-size="10" fill="currentColor" transform="rotate(-90 14 95)" text-anchor="middle">Side glass</text>'
            '<text x="232" y="95" font-size="10" fill="currentColor" transform="rotate(90 232 95)" text-anchor="middle">Centre line</text>'
            '<rect x="24" y="24" width="52" height="46" rx="6" fill="#e8f84a" opacity=".85"/><text x="50" y="51" text-anchor="middle" font-size="11" font-weight="700" fill="#0b1530">Wide</text>'
            '<rect x="94" y="24" width="52" height="46" rx="6" fill="#ff9b78" opacity=".85"/><text x="120" y="51" text-anchor="middle" font-size="11" font-weight="700" fill="#0b1530">Body</text>'
            '<rect x="164" y="24" width="52" height="46" rx="6" fill="#fff" opacity=".9"/><text x="190" y="51" text-anchor="middle" font-size="11" font-weight="700" fill="#0b1530">T</text>'
            '<text x="120" y="110" text-anchor="middle" font-size="10" fill="#cfe0ff">Aim for the back third of the box</text></svg>')

sv = f'''<header class="hero"><div class="wrap"><h1>How to serve in padel: 6 steps and a serve practice tracker.</h1>
<p class="lead">Learn a reliable padel serve step by step, choose where to aim, then log a practice basket to see your serve percentage and what to fix.</p>
{quick("To serve in padel: stand sideways behind the service line with a continental grip, drop the ball just in front of your front foot, let it bounce once, and hit it at or below waist height with a short low-to-high swing. Aim deep into the diagonal service box: wide to the side glass, at the receiver's body, or down the T. Then move up to the net. You get two attempts, and placement matters more than power.", "2026-11-26")}
<p class="muted" style="margin-top:8px;font-size:.9rem">Last updated 26 Nov 2026. Technique is general coaching advice in our own words. Rule details: <a href="{href("serve-rules.html")}">padel serve rules</a>.</p></div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="sv">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Serve practice tracker</h2>
<p class="muted" style="margin-top:0">Pick a target, serve, then tap what happened. Do 10 serves per target.</p>
<div class="q"><h3>Target</h3><div class="opts" id="sv-tgt" role="group" aria-label="Serve target">{sv_tgt}</div></div>
<div class="q"><h3>What happened?</h3><div class="btns sv-res" id="sv-res" style="margin:0">{sv_res}</div></div>
<div class="btns" style="margin:6px 0 0"><button class="btn ghost sm" type="button" id="sv-undo">Undo last</button><button class="btn lime sm" type="button" id="sv-save">Finish and save session</button><button class="btn ghost sm" type="button" id="sv-reset">Clear this session</button></div>
<p class="muted" style="margin:12px 0 0;font-size:.92rem">Saved on this device only. Put a towel or a cone in each target zone if you can.</p>
</div>
<aside class="result" id="sv-out" aria-live="polite"><h2>This session</h2><p id="sv-sum"></p><div id="sv-bars"></div><p id="sv-tip"></p><p class="wr-src">Next: <a href="{href("serve-rules.html")}" style="color:#e8f84a">Serve rules checker</a> · <a href="{href("drills.html")}" style="color:#e8f84a">Drills planner</a> · <a href="{href("padel-tactics.html")}" style="color:#e8f84a">Tactics trainer</a></p>
<div class="btns" style="margin:10px 0 0"><button class="btn sm" type="button" id="sv-copy">Copy summary</button></div></aside>
</div></section>
<section style="padding-top:0"><div class="wrap" style="max-width:860px"><div class="card"><h2 style="font-size:1.3rem;margin-top:0">My serve sessions</h2><div id="sv-hist"></div><p class="muted" id="sv-hempty">No saved sessions yet.</p></div></div></section>
<script>window.SERVE={json.dumps(sv_js, ensure_ascii=False)};</script>
{AD.format("sv-mid")}
<section><div class="wrap"><div class="sh"><h2>How do you serve in padel, step by step?</h2></div><div class="grid">
<div class="card"><h3>1. Stand sideways</h3><p>Stand behind the service line, on the right half for the first point of each game. Turn your front shoulder toward the box you are serving into. Feet about shoulder-width apart, knees soft.</p></div>
<div class="card"><h3>2. Use a continental grip</h3><p>Hold the racket like a hammer, the same grip as for volleys. See <a href="{href("padel-grip.html")}">how to hold a padel racket</a>.</p></div>
<div class="card"><h3>3. Drop, don't toss</h3><p>Drop the ball beside your body, just in front of your front foot. Let it bounce once. Do not throw it up: the ball must bounce before you hit it.</p></div>
<div class="card"><h3>4. Hit at or below the waist</h3><p>Wait for the ball to start falling, around knee to thigh height. Contact must be at or below your waist, with at least one foot on the ground.</p></div>
<div class="card"><h3>5. Short swing, low to high</h3><p>A compact swing that moves from low to high. Power comes from moving your weight from the back foot to the front foot, not from a big arm swing.</p></div>
<div class="card"><h3>6. Move to the net</h3><p>Follow the serve forward to your volley spot, about 2 to 2.5 m from the net. The serve is your way to take the net, where most points are won.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Where should you aim your padel serve?</h2><p class="muted">Aim deep, into the back third of the box. Then pick one of three targets.</p></div>
<div class="grid" style="align-items:center"><div class="card" style="text-align:center">{box_svg()}</div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Target</th><th scope="col">Why</th></tr></thead><tbody>
<tr><td>Wide, into the side glass</td><td>The ball bounces off the side glass and the receiver has to turn. Works at every level.</td></tr>
<tr><td>At the body (hip)</td><td>The receiver has no room to swing and often plays a weak, high return.</td></tr>
<tr><td>Down the T</td><td>Lands near the centre line, often on the receiver's backhand. Narrows their angles.</td></tr>
<tr><td>Mix them</td><td>Change target and speed so the receiver cannot settle.</td></tr>
</tbody></table></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What types of serve are there in padel?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Serve</th><th scope="col">What it does</th><th scope="col">Who should use it</th></tr></thead><tbody>
<tr><td>Flat</td><td>Straight, medium pace, easy to repeat</td><td>Learn this first</td></tr>
<tr><td>Slice (backspin)</td><td>Stays low after the bounce and off the glass</td><td>Improvers and up: the most common club serve</td></tr>
<tr><td>Side-spin</td><td>Curves toward the side glass and spins off it</td><td>Club players who already have a steady slice</td></tr>
<tr><td>Body serve</td><td>Jams the receiver at the hip</td><td>Anyone, as a surprise</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why do I keep missing my padel serve?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Problem</th><th scope="col">Likely cause</th><th scope="col">Fix</th></tr></thead><tbody>
<tr><td>Into the net</td><td>Contact too low or swing too flat</td><td>Let it drop to knee height, swing low to high</td></tr>
<tr><td>Long</td><td>Too much power</td><td>Serve at about two thirds pace, add slice</td></tr>
<tr><td>Wide or wrong box</td><td>Body facing the net, drop in a different place each time</td><td>Shoulder to the target, same drop spot</td></tr>
<tr><td>Bounces in, then hits the fence</td><td>Aiming too close to the side</td><td>Aim a little further in, so it reaches the glass</td></tr>
<tr><td>Foot fault</td><td>Standing on the line or jumping</td><td>Stand clearly behind the line, one foot down</td></tr>
<tr><td>Easy to attack</td><td>High and soft into the middle of the box</td><td>Low over the net, deep, to a target</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel serve drills</h2></div><div class="grid">
<div class="card"><h3>10 per target</h3><p>Serve 10 balls at each of the three targets and log them above. Repeat on the left side. Watch your "hit the target" number grow week by week.</p></div>
<div class="card"><h3>First-serve percentage</h3><p>Serve 20 first serves at match pace. Aim to get at least 8 in 10 in. If you are under that, slow down before you add spin.</p></div>
<div class="card"><h3>Serve and get to the net</h3><p>Put a marker about one racket length from the centre line, level with the second post of the side fence. Serve, then reach the marker before the return. Five in a row wins.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Check a serve</h3><p>Was it in? Answer 3 questions in the <a href="{href("serve-rules.html")}">serve rules checker</a>.</p></div>
<div class="card"><h3>After the serve</h3><p>Learn what to play next in common situations with the <a href="{href("padel-tactics.html")}">padel tactics trainer</a>.</p></div>
<div class="card"><h3>Count your faults in matches</h3><p>Log serve errors with the rest of your game in the <a href="{href("padel-match-tracker.html")}">match tracker</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Serve practice gear</h3><p>A basket of fresh balls makes serve practice quicker, and a control racket helps you place the ball.</p><ul class="aff-links"><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round (control) rackets</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 26 Nov 2026: LTA Padel "How to serve in padel: expert tips" (underarm, diagonal, bounce first; placement over power; serve deep; side glass works at all levels; serve-and-net-marker drill); Padel Browser "How to serve in padel" (continental grip, sideways stance, drop in front of the front foot, weight transfer, flat/slice/side-spin/body serves, T/wide/body targets, about two-thirds pace, 80% first-serve goal). Rule points match our <a href="{href("serve-rules.html")}">serve rules page</a> (FIP rules). The tracker, tips and wording are our own.</p></div></section>'''
sv_faq = [
    ("How do you serve in padel?", "Stand behind the service line, drop the ball and let it bounce once, then hit it at or below waist height into the service box diagonally opposite. Use a short, low-to-high swing and move to the net after the serve."),
    ("Is the padel serve underarm?", "Yes. You must hit the ball at or below waist height, so the serve is underarm or side-arm. Overhead and jump serves are not allowed."),
    ("Where should I aim my padel serve?", "Deep in the box, at one of three targets: wide into the side glass, at the receiver's body, or down the T near the centre line. Mix targets and speed."),
    ("How many serves do you get in padel?", "Two. If the first is a fault, you serve again. Two faults in a row lose the point. A serve that clips the net and lands in the box is a let and is replayed."),
    ("Should I serve hard in padel?", "Usually not. Very few padel serves are unreturnable, so placement and getting to the net matter more than speed. Many players serve at about two thirds pace with slice."),
    ("What is a good first-serve percentage in padel?", "Aim to get at least 8 in 10 first serves in. Missing first serves gives away free pressure on your second serve."),
]
page("how-to-serve-padel.html", "How to Serve in Padel: 6 Steps + Serve Practice Tracker | Padel Glass Box",
     "How to serve in padel: stand sideways, drop and bounce, hit below the waist with a short low-to-high swing, aim deep (wide, body or T) and move to the net. Free serve tracker.",
     sv, sv_faq, "How to serve")

# ---------- 2. PADEL TACTICS TRAINER ----------
# Scenario: (title, situation, us positions, them positions, ball, arrow, options[(text, correct)], why)
TAC = [
    ("Both opponents at the net",
     "You are deep at the back. Both opponents are close to the net and you are under pressure.",
     [(3, 18.8), (7.5, 17.5)], [(3, 7.6), (7, 7.6)], (3.2, 18.2), ((3.2, 18.2), (7, 2)),
     [("Drive it hard straight at them", 0), ("Lob it deep over them", 1), ("Hit a fast ball down the middle", 0)],
     "A deep lob over the net players is the best way out of trouble. It pushes them back, and you and your partner can move up and take the net."),
    ("You have time, they are at the net",
     "Both opponents are at the net, but the ball comes to you slowly at a nice height near your service line.",
     [(3, 16), (7, 17.5)], [(3, 7.8), (7, 7.8)], (3, 15.6), ((3, 15.6), (5, 9)),
     [("A soft, low ball at their feet", 1), ("A hard flat drive into the back glass", 0), ("A short drop shot", 0)],
     "A soft ball that dips at their feet (often called a chiquita) forces them to volley up. Then you and your partner move forward."),
    ("Easy high ball near the net",
     "You and your partner are at the net. The opponents are deep and you get a high, slow ball close to the net.",
     [(3, 12.5), (7, 12.5)], [(3, 18.8), (7, 18.8)], (3, 12), ((3, 12), (1, 1.5)),
     [("Play a safe bandeja to keep the point going", 0), ("Smash it: this is the ball to finish", 1), ("Lob it back", 0)],
     "Go for the winner only on an easy ball like this one. A high, slow ball near the net is the time to finish the point.",),
    ("Medium lob over you",
     "You are at the net. A medium lob goes over your head toward the back corner. You can reach it, but you are moving back.",
     [(3, 13.2), (7, 12.5)], [(3, 2), (7, 2.5)], (3.3, 15), ((3.3, 15), (1.5, 2)),
     [("Bandeja to their deep corner", 1), ("Full power smash", 0), ("Let it go and run to the back glass", 0)],
     "A controlled bandeja deep to the corner keeps you at the net. Smashing a ball that is behind you usually gives the opponents an easy ball off the glass."),
    ("Deep lob you can't reach",
     "You are at the net and a high lob lands deep in your back corner. You cannot reach it in the air.",
     [(3, 13), (7, 13)], [(3, 2.5), (7, 2.5)], (2, 18.6), ((3, 13), (2.2, 18.2)),
     [("Jump and try a smash anyway", 0), ("Both of you go back; play it after the back glass", 1), ("Your partner stays at the net", 0)],
     "Turn and go back together. Let the ball come off the back glass, then play a lob or a soft ball and rebuild the point. Moving as a pair stops gaps opening."),
    ("Opponents close together",
     "You are at the net. Both opponents are at the net too, standing close to each other.",
     [(3, 12.3), (7, 12.3)], [(4, 7.8), (6, 7.8)], (7, 12), ((7, 12), (5, 6.5)),
     [("Hit it down the middle", 1), ("Aim at the side glass", 0), ("Lob over both of them", 0)],
     "Down the middle creates doubt about who takes it, and both players may go for it or both leave it. The net is lower in the middle too."),
    ("One opponent is weaker",
     "After a few games you notice one opponent misses more, especially on the backhand.",
     [(3, 13), (7, 13)], [(3, 3), (7, 3)], (3, 12.5), ((3, 12.5), (6.5, 4)),
     [("Share the balls equally", 0), ("Play most balls to the weaker player's backhand", 1), ("Only lob", 0)],
     "Focus your play on the weaker opponent and their weaker side. It adds pressure and leaves the stronger player out of rhythm."),
    ("Your serve",
     "You have just served deep into the side glass.",
     [(3.5, 17.2), (7, 11.8)], [(2.5, 3.5), (6, 8)], (2, 6), ((3.5, 17.2), (3, 12.5)),
     [("Stay at the back and wait", 0), ("Follow the serve to the net", 1), ("Run to the middle of the court", 0)],
     "Use the serve to take the net. Move forward to your volley spot, about 2 to 2.5 m from the net, as the ball crosses."),
    ("Hard ball into your back glass",
     "You are at the back. An opponent hits a fast ball that will bounce and hit your back glass.",
     [(3, 17), (7, 17)], [(3, 8), (7, 8)], (3.2, 19.4), ((3, 8), (3.2, 19.4)),
     [("Hit it before it reaches the glass", 0), ("Let it come off the glass and play it as it drops", 1), ("Volley it", 0)],
     "A fast ball loses speed off the glass. Wait about 1 m from the glass, let it come out, and play it as it drops to waist height."),
    ("Your partner is pulled wide",
     "Your partner is pulled out wide to the side glass to play a ball.",
     [(5.5, 13), (9.2, 15)], [(3, 3), (7, 3)], (9.4, 15.4), ((9.4, 15.4), (2, 3)),
     [("Stay on your own half", 0), ("Shift toward the middle to cover the gap", 1), ("Run to the back", 0)],
     "Move with your partner. When they go wide, you slide toward the middle so there is no gap down the centre. Think of a rope joining you, about 3 m apart."),
]
tac_js = [{"t": t, "s": s, "svg": court_svg(u, th, b, a, t + ": you are Y, your partner P, opponents in orange"), "o": [[x, c] for x, c in o], "w": w} for t, s, u, th, b, a, o, w in TAC]
tc = f'''<header class="hero"><div class="wrap"><h1>Padel tactics: what shot should I play?</h1>
<p class="lead">Ten real match situations, each drawn on a court. Pick your shot and see why it works. Then learn the simple rules club players use to win more points.</p>
{quick("The core padel tactics: take the net together, because most points are won there; when both opponents are at the net, lob deep or play a soft ball at their feet; only go for a winner on an easy, high ball; play down the middle when they stand close; pick on the weaker player's backhand; and move as a pair, about 3 m apart. At club level most points end with an error, so keep the ball in play.", "2026-11-26")}
<p class="muted" style="margin-top:8px;font-size:.9rem">Last updated 26 Nov 2026. General coaching advice in our own words. You are Y, your partner P, opponents in orange, the yellow line is the ball.</p></div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="tc">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Padel tactics trainer</h2><p class="muted" style="margin-top:0">Read the situation, look at the court, pick a shot.</p><div id="tc-q"></div></div>
<aside class="result" id="tc-out" aria-live="polite"><h2>Your tactics score</h2><p id="tc-s"></p><p id="tc-m"></p><p class="wr-src">Next: <a href="{href("positioning.html")}" style="color:#e8f84a">Where to stand</a> · <a href="{href("bandeja-vs-vibora.html")}" style="color:#e8f84a">Bandeja vs víbora</a> · <a href="{href("fix-my-padel.html")}" style="color:#e8f84a">Fix my padel</a></p>
<div class="btns" style="margin:10px 0 0"><button class="btn ghost sm" type="button" id="tc-reset">Start again</button></div></aside>
</div></section>
<script>window.TACQ={json.dumps(tac_js, ensure_ascii=False)};</script>
{AD.format("tc-mid")}
<section><div class="wrap"><div class="sh"><h2>How do you win a point in padel?</h2><p class="muted">There are only three ways.</p></div><div class="grid">
<div class="card"><h3>1. The opponents make an unforced error</h3><p>The most common way at club level. Keep one more ball in play than them. Count yours with the <a href="{href("padel-match-tracker.html")}">match tracker</a>.</p></div>
<div class="card"><h3>2. You force an error</h3><p>Play at their feet, into the corners, and change speed and direction so they play under pressure.</p></div>
<div class="card"><h3>3. You hit a winner</h3><p>Only on easy balls: high, slow and near the net. On hard balls, be patient and reset.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What shot should I play? The quick tactics table</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">You are</th><th scope="col">Opponents are</th><th scope="col">Usually play</th></tr></thead><tbody>
<tr><td>At the back</td><td>At the net</td><td>Deep lob, or a soft low ball at their feet, then move up</td></tr>
<tr><td>At the back</td><td>At the back</td><td>Steady cross-court rally; move up on the first short ball</td></tr>
<tr><td>At the net</td><td>At the back</td><td>Deep volleys to the corners or at the feet; finish only high balls</td></tr>
<tr><td>At the net</td><td>At the net</td><td>Low, fast down the middle or at the body; lob if you have time</td></tr>
<tr><td>At the net, lobbed</td><td>Moving up</td><td>Bandeja or víbora deep; if you can't reach, go back together</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel tactics for doubles: 8 simple rules</h2></div><div class="grid">
<div class="card"><h3>Take the net</h3><p>The pair at the net wins most points. Serve and move up, and lob to win the net back.</p></div>
<div class="card"><h3>Consistency before power</h3><p>Fewer errors usually beats more winners. Medium pace, good placement.</p></div>
<div class="card"><h3>Don't rush forward</h3><p>Go to the net on a good lob or a short ball, not every time. Rushing tires you and leads to rushed shots.</p></div>
<div class="card"><h3>Find the weak spot</h3><p>Most players have a weaker backhand. Find who is weaker early and play to them.</p></div>
<div class="card"><h3>Use the middle</h3><p>When opponents stand close or both at the net, the middle causes confusion.</p></div>
<div class="card"><h3>Move them around</h3><p>Change direction and depth so they run and play off balance.</p></div>
<div class="card"><h3>Move as a pair</h3><p>Up and back together, about 3 m apart. Call "mine" or "yours". See <a href="{href("which-side-padel.html")}">which side to play</a>.</p></div>
<div class="card"><h3>Keep it simple</h3><p>Agree one or two plans before the match, such as "lob the left player" or "serve to the body".</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Where to stand</h3><p>Distances from the net and the glass in every situation: <a href="{href("positioning.html")}">padel positioning</a>.</p></div>
<div class="card"><h3>Practise the shots</h3><p>Lobs, chiquitas and bandejas in the <a href="{href("drills.html")}">drills planner</a> and <a href="{href("shots.html")}">shot library</a>.</p></div>
<div class="card"><h3>Start with the serve</h3><p>Take the net from the first ball: <a href="{href("how-to-serve-padel.html")}">how to serve in padel</a>.</p></div>
</div></div></section>
<section><div class="wrap"><p class="muted" style="font-size:.9rem">Sources, checked 26 Nov 2026: The Padel School "How to win a padel point" (three ways to win a point; most recreational points end with unforced errors; feet, corners, change of pace; winners only on easy balls); HEAD "Padel tactics to improve your game" (consistency over power, controlled volleys, don't rush the net, find weaknesses and the weaker backhand, focus on one opponent, the middle, lob to take the net, communication); LTA Padel serve guide (serve to get to the net). Scenarios, court drawings and wording are our own. Distances match our <a href="{href("positioning.html")}">positioning guide</a>.</p></div></section>'''
tc_faq = [
    ("What is the best tactic in padel?", "Take the net with your partner and keep the ball in play. Most points at club level end with an error, and the pair at the net wins most points. Lob deep to win the net back when the opponents have it."),
    ("What should I do when both opponents are at the net?", "Lob deep over them, or play a soft, low ball at their feet so they have to volley up. Then move forward with your partner."),
    ("When should I go for a winner in padel?", "Only on an easy ball: high, slow and near the net. On difficult balls, be patient and play a safe shot that resets the point."),
    ("Why hit down the middle in padel?", "A ball down the middle can make both opponents go for it or both leave it, and the net is lowest in the middle."),
    ("Should both padel players be at the net?", "Ideally yes, together. Move up and back as a pair about 3 m apart, so no gap opens down the middle."),
    ("How do you beat better padel players?", "Cut your errors, lob a lot to keep them off the net, play to the weaker player's backhand, and keep the ball low and in the middle. Make them hit one more ball."),
]
page("padel-tactics.html", "Padel Tactics: What Shot Should I Play? (10-Scenario Trainer) | Padel Glass Box",
     "Padel tactics trainer: 10 match situations drawn on a court. When both opponents are at the net, lob or hit at their feet; finish only easy balls; use the middle; move as a pair.",
     tc, tc_faq, "Padel tactics")

# ---------- 3. HOW TO GET BETTER AT PADEL: level-by-level guide (hub) ----------
LV = [
    ("new", "Just started (under 6 months)", "Level about 1 to 2.5",
     ["Learn the continental grip and a short, compact swing.", "Let the ball come off the back glass instead of hitting it early.", "Get a reliable underarm serve in, every time."],
     [("padel-grip.html", "Grip guide"), ("beginners.html", "Beginner's guide"), ("how-to-serve-padel.html", "How to serve"), ("rules.html", "Rules")],
     "Play 1 to 2 times a week. One short lesson or a beginners' session every few weeks helps a lot."),
    ("imp", "Improver (6 months to 2 years)", "Level about 2.5 to 3.5",
     ["Play steady cross-court rallies at medium pace.", "Volley from about 2 to 2.5 m off the net with the racket up.", "Start using the lob, and learn the bandeja."],
     [("fix-my-padel.html", "Fix my padel"), ("positioning.html", "Where to stand"), ("bandeja-vs-vibora.html", "Bandeja guide"), ("padel-training-plan.html", "4-week plan")],
     "Two sessions a week: one practice (drills) and one match. Track one match a month."),
    ("club", "Club player", "Level about 3.5 to 4.5",
     ["Win the net with lobs and soft balls at the feet.", "Make your bandeja deep and steady; add the víbora.", "Play patterns with your partner: who takes the middle, who covers the lob."],
     [("padel-tactics.html", "Tactics trainer"), ("padel-match-tracker.html", "Match tracker"), ("which-side-padel.html", "Which side?"), ("drills.html", "Drills planner")],
     "Two to three sessions a week. Track matches to find your biggest leak and drill it."),
    ("adv", "Strong player (4.5 and up)", "Level about 4.5 and up",
     ["Out-of-court play and smashes por 3 or por 4 when they are on.", "Vary serve spin and target on purpose.", "Plan tactics by opponent: who to target and how."],
     [("out-of-court-play.html", "Out-of-court play"), ("how-to-serve-padel.html", "Serve tracker"), ("padel-tactics.html", "Tactics"), ("padel-injuries.html", "Injury prevention")],
     "Three or more sessions a week, with fitness and recovery. Work with a coach on details."),
]
lv_btns = "".join(f'<button type="button" class="opt" data-v="{k}" aria-pressed="{"true" if i == 1 else "false"}">{e(n)}</button>' for i, (k, n, *_ ) in enumerate(LV))
def _lv(k, n, lvl, todo, tools, wk, i):
    tl = "".join(f'<li><a href="{href(f)}">{e(t)}</a></li>' for f, t in tools)
    return (f'<div class="card ig-p" data-lv="{k}"{"" if i == 1 else " hidden"}><h3>{e(n)} <span class="muted" style="font-weight:500;font-size:.9rem">({e(lvl)})</span></h3>'
            f'<p><strong>Work on these three things next:</strong></p><ol>' + "".join(f"<li>{e(t)}</li>" for t in todo) + '</ol>'
            f'<p><strong>Use these:</strong></p><ul class="ig-tools">{tl}</ul><p><strong>How often:</strong> {e(wk)}</p></div>')
ig_panels = "".join(_lv(*x, i) for i, x in enumerate(LV))
ig_rows = "".join(f'<tr><td>{e(n)}</td><td>{e(lvl)}</td><td>{e(todo[0])}</td></tr>' for k, n, lvl, todo, *_ in LV)
ig = f'''<header class="hero"><div class="wrap"><h1>How to get better at padel: a level-by-level guide.</h1>
<p class="lead">Pick your level and see the three things to work on next, which free tools to use, and how often to play.</p>
{quick("To get better at padel: work on one thing at a time, play at least twice a week (one practice session with drills and one match), and track your errors to see what to fix. New players should learn the grip, a short swing and playing off the back glass. Improvers should volley 2 to 2.5 m from the net and learn the lob and bandeja. Club players should win the net with lobs and play patterns with their partner.", "2026-11-26")}
<p class="muted" style="margin-top:8px;font-size:.9rem">Last updated 26 Nov 2026. General coaching advice in our own words.</p></div></header>
<section style="padding-top:10px"><div class="wrap" id="ig" style="max-width:860px">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">What level are you?</h2><p class="muted" style="margin-top:0">Not sure? Take the 2-minute <a href="{href("level-calculator.html")}">level calculator</a>.</p>
<div class="opts" id="ig-pick" role="group" aria-label="Your padel level">{lv_btns}</div></div>
<div style="margin-top:14px" aria-live="polite">{ig_panels}</div>
</div></section>
{AD.format("ig-mid")}
<section><div class="wrap"><div class="sh"><h2>What should I work on at each padel level?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Stage</th><th scope="col">Level</th><th scope="col">First priority</th></tr></thead><tbody>{ig_rows}</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How can I improve at padel fast?</h2></div><div class="grid">
<div class="card"><h3>Repeat, repeat</h3><p>Short drills with many balls build habits faster than matches alone. Build a session in the <a href="{href("drills.html")}">drills planner</a>.</p></div>
<div class="card"><h3>Measure, don't guess</h3><p>Log one match in the <a href="{href("padel-match-tracker.html")}">match tracker</a>. The shot with the most errors is your next job.</p></div>
<div class="card"><h3>Fix one thing</h3><p>The <a href="{href("fix-my-padel.html")}">problem fixer</a> gives the cause, three fixes and a drill for 12 common problems.</p></div>
<div class="card"><h3>Follow a plan</h3><p>Turn it into four weeks with the <a href="{href("padel-training-plan.html")}">training plan generator</a>.</p></div>
<div class="card"><h3>Think tactics</h3><p>Better choices win points without better shots. Try the <a href="{href("padel-tactics.html")}">tactics trainer</a>.</p></div>
<div class="card"><h3>Play better players</h3><p>Join a <a href="{href("ladder.html")}">ladder</a> or an <a href="{href("americano.html")}">Americano</a>, take the odd <a href="{href("padel-lessons.html")}">lesson</a>, and warm up properly with the <a href="{href("warm-up.html")}">warm-up timer</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long does it take to get good at padel?</h2></div>
<div class="card"><p>Padel is quick to start: most new players can rally in their first session, because the racket is short and the serve is underarm. Going from beginner to steady club level usually takes a year or two of playing twice a week. These are rough guides, not promises: lessons, fitness and playing other racket sports speed it up.</p></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Know your level</h3><p>Get a number from 1 to 7 with the <a href="{href("level-calculator.html")}">level calculator</a>.</p></div>
<div class="card"><h3>Right racket for your level</h3><p>Answer 6 questions in the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
<div class="card"><h3>Pick your side</h3><p>Left or right? The <a href="{href("which-side-padel.html")}">side quiz</a> takes one minute.</p></div>
</div></div></section>
<section><div class="wrap"><p class="muted" style="font-size:.9rem">Checked 26 Nov 2026 against: The Padel School "The power of repetition: how to improve padel fast"; LTA "Training tips to improve your padel skills"; Padel Browser "How to get better at padel". Level bands follow our <a href="{href("level-calculator.html")}">level calculator</a>. Priorities, timings and wording are general coaching advice in our own words.</p></div></section>'''
ig_faq = [
    ("How do I get better at padel?", "Work on one thing at a time, play at least twice a week (one practice and one match), track your errors to find what to fix, and take a lesson now and then."),
    ("How long does it take to get good at padel?", "Most people rally in their first session. Reaching steady club level usually takes a year or two of playing about twice a week, faster with lessons or a tennis or squash background."),
    ("What should a beginner padel player practise first?", "The continental grip, a short swing, a reliable underarm serve, and letting the ball come off the back glass before hitting it."),
    ("How often should I play padel to improve?", "Two sessions a week is a good start: one practice with drills and one match. Strong players add a third session plus fitness work."),
    ("Is it better to take padel lessons or just play?", "Both. Matches teach decisions; lessons and drills fix technique faster than matches alone. A lesson every few weeks plus regular games works well for most players."),
]
page("padel-improvement-guide.html", "How to Get Better at Padel: Level-by-Level Guide | Padel Glass Box",
     "How to get better at padel: pick your level and see the 3 things to work on next, which free tools to use and how often to play. Beginner, improver, club and strong players.",
     ig, ig_faq, "Improvement guide")

SKILL_PAGES = ["how-to-serve-padel.html", "padel-tactics.html", "padel-improvement-guide.html"]
