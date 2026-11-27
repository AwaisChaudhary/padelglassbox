# ---------------- DEMAND RUN 10 (27 Nov 2026): smash guide + smash picker, chiquita guide + chiquita-or-lob picker ----------------
# Executed from demand6.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards).

# ---------- 1. PADEL SMASH ----------
sm_steps = [
    ("Turn side-on at once", "As soon as you see the lob, turn your shoulders so your non-hitting shoulder points at the net. Turning first is what gives you time."),
    ("Move with crossover steps", "Go back with side or crossover steps, not by running backwards. Get behind the ball so you can hit it while moving forward."),
    ("Point at the ball", "Lift your free hand and point at the ball. Hold the racket up behind your head, ready, with a continental grip."),
    ("Hit high and in front", "Meet the ball at the highest point you can, a little in front of your head. A ball that drops low in front of you should be a bandeja, not a smash."),
    ("Snap and finish across", "Let the wrist and forearm turn over at contact for speed and topspin, and finish the racket across your body."),
    ("Get back to the net", "After the smash, move forward again at once. A good pair will often get the ball back off the glass."),
]
sm_types = [
    ("Flat smash", "A hard, flat hit aimed down the middle or at the feet. It does not leave the court, so it comes back off the back glass if the other pair waits for it. Hit it at an angle or at feet, not straight into the glass at speed."),
    ("Kick smash", "Heavy topspin so the ball bounces deep and kicks up high off the back glass. It keeps the other pair back and buys you time, rather than winning the point at once."),
    ("x3 (por tres)", "A topspin smash that bounces in the other court, hits the back glass and flies out over the side wall, which is 3 m high. That is where the name comes from. It needs a lot of power and a short lob."),
    ("x4 (por cuatro)", "A smash that bounces and goes out over the back wall (glass plus mesh, about 4 m in total). It is the hardest version. The names x3 and x4 are informal, and descriptions differ a little between sources."),
]
sm_err = [
    ("Smashing every lob", "Most lobs at club level are too deep to smash. Play a bandeja or a víbora and keep the net instead."),
    ("Hitting too hard", "A very hard flat smash into the back glass comes back fast and gives the other pair an easy ball. Placement beats speed."),
    ("Ball too low", "Waiting until the ball drops to head height, then trying to smash. Hit high, or change to a bandeja."),
    ("Running backwards", "Backpedalling face-on is slow and you lose balance. Turn first, then use side steps."),
    ("Forgetting your partner", "Call the ball ('mine' or 'yours'). On a lob down the middle, the player on the forehand side usually takes it."),
]
sm = f'''<header class="hero"><div class="wrap"><h1>How to smash in padel, and when not to.</h1>
<p class="lead">The smash is the shot everyone wants to hit and the one that loses club players the most points. Use the smash picker to see if this lob is a smash, a bandeja, a víbora or one to let off the glass, then learn the technique and what the x3 and x4 smashes are.</p>
{quick("To smash in padel, turn side-on as soon as you see the lob, move back with side steps, point at the ball with your free hand and hit it high and a little in front of your head with a continental grip, then move forward to the net again. Only smash short lobs you can hit above your head while moving forward; for deeper lobs, play a bandeja or víbora. A flat smash stays in the court and comes back off the glass. An x3 (por tres) bounces and goes out over the 3 m side wall; an x4 goes out over the back wall.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="smp">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Smash or not? The lob picker</h2><p class="muted" style="margin-top:0">Four questions about the lob coming at you.</p>
{_bq2("smp", "dep", "How deep is the lob?", [("short", "Short, near the net"), ("mid", "Around the service line"), ("deep", "Deep, near the back glass")], "mid")}
{_bq2("smp", "ht", "Where can you meet it?", [("high", "Well above my head"), ("head", "Around head height")], "high")}
{_bq2("smp", "bal", "Your balance", [("fwd", "Moving forward or still"), ("back", "Moving backwards")], "fwd")}
{_bq2("smp", "out", "Can players run outside on this court?", [("y", "Yes, there are door openings"), ("n", "No / not sure")], "n")}</div>
<aside class="result" id="smp-out" aria-live="polite"><h2 id="smp-h"></h2><p id="smp-p"></p><p id="smp-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you hit a smash in padel?</h2><p class="muted">Six steps. Same grip as your volley: see the <a href="{href("padel-grip.html")}">grip guide</a>.</p></div>
<div class="grid">{_cards(sm_steps, "Step")}</div></div></section>
{AD.format("sm-mid")}
<section><div class="wrap"><div class="sh"><h2>Types of padel smash: flat, kick, x3 and x4</h2><p class="muted">From the most common to the hardest.</p></div>
<div class="grid">{_cards(sm_types)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What is an x3 smash in padel, and how do you hit one?</h2></div>
<div class="grid">
<div class="card"><h3>Pick the right ball</h3><p>Only a comfortable, short lob that you can hit at full stretch. The closer you are to the net, the easier it is. From further back you need much more topspin.</p></div>
<div class="card"><h3>Aim for the bounce</h3><p>Aim to bounce the ball about a metre before the other pair's service line, so it hits the back glass high and near the corner and flies out over the side wall. Cross-court is easier than down the line.</p></div>
<div class="card"><h3>Jump and brush up</h3><p>Jump, hit as high as you can with the face a little open, and brush up and over the ball for topspin, finishing across your hip.</p></div>
<div class="card"><h3>It is not always a winner</h3><p>On courts with door openings and space outside, the other pair may run out and play the ball back before it bounces again. Rules: <a href="{href("out-of-court-play.html")}">out-of-court play</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Common smash mistakes</h2></div><div class="grid">{_cards(sm_err)}</div>
<p class="muted" style="margin-top:14px">Smash drill, "call it": a partner feeds lobs of different depths. Before contact, call out "smash", "bandeja" or "víbora", then play that shot. After each one, run back to the net and touch it with your racket. Start with 10 short lobs, then mix in deep ones. Build a full session in the <a href="{href("drills.html")}">drills planner</a>. Overhead options compared: <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora vs smash</a>. Facing smashes? See <a href="{href("padel-back-glass.html")}">playing off the back glass</a> and <a href="{href("padel-lob.html")}">how to hit a lob</a> they can't smash.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: Padel Browser "How to hit a smash in padel" (27 May 2026: when to smash vs bandeja or víbora, flat, kick, por tres and por cuatro, sideways turn, crossover step, continental grip, mistakes, decision drill); Nox "How to hit a 3-metre smash in padel" (bounce about 1 m before the service line, rebound near the back corner, short comfortable lob, open face, topspin, opponents may play it outside if the court allows); FIP Rules of Padel (out-of-court play). Advice in our own words; the picker is our own summary.</p></div></section>'''
sm_faq = [
    ("How do you smash in padel?", "Turn side-on early, move back with side steps, point at the ball, hit it high and slightly in front of your head with a continental grip, snap the wrist over and finish across your body. Then move back to the net."),
    ("When should you smash in padel?", "Only on short lobs you can hit well above your head while moving forward or standing still. For deep lobs, or when you are moving backwards, play a bandeja or a víbora."),
    ("What is an x3 in padel?", "An x3 (por tres) is a topspin smash that bounces in the other court, hits the back glass and goes out over the 3 m side wall. It is very hard to return unless the court allows players to run outside."),
    ("What is an x4 in padel?", "An x4 (por cuatro) is a smash that bounces and goes out over the back wall, which is glass plus mesh, about 4 m high. It is the hardest smash to hit."),
    ("Why does my smash come back in padel?", "A flat smash stays inside the court, so the ball hits the back glass and comes back for the other pair. Aim at their feet or at an angle, or use topspin, instead of hitting straight and hard into the glass."),
    ("Bandeja or smash: which is better?", "Neither is better; they do different jobs. The bandeja keeps you at the net safely on a deeper lob. The smash is for short, easy lobs you can finish."),
]
page("padel-smash.html", "How to Smash in Padel: x3, x4 + Smash or Bandeja Picker",
     "How to smash in padel: six steps, flat vs kick vs x3 (por tres) vs x4, when to smash or play a bandeja, a free lob picker, common mistakes and a drill.",
     sm, sm_faq, "Padel smash")

# ---------- 2. CHIQUITA ----------
cq_steps = [
    ("Pick the right ball", "A ball you can reach comfortably, usually one that bounces in the middle of your half. Not one that pins you against the back glass."),
    ("Prepare like a lob", "Get under the ball with small side steps, knees bent, the racket face a little open. The other pair should think a lob is coming."),
    ("Play it soft and slow", "Use a gentle, controlled swing. Placement, not power. A fast chiquita gives them a ball to volley back hard."),
    ("Aim at the feet", "The target is the net player's feet, or the gap between the two of them, so the ball dips below the net on their side."),
    ("Move in at once", "Follow the ball forward straight away with your partner. Do not stop to watch: the chiquita's whole point is to win back the net."),
]
cq_err = [
    ("Too fast", "A hard ball at net players is a gift. Slow it down so it drops at their feet."),
    ("Too high", "If it floats above the net they can attack it. Keep it low; aim to clear the net by a little."),
    ("From too deep", "Played with your back at the glass, you cannot get forward in time. Lob from there instead."),
    ("Standing to watch", "If you wait, a good volley leaves you stuck in the middle. Go forward as you hit."),
    ("Only chiquitas", "Use it with the lob. Once they step in to cover the chiquita, the lob goes over them."),
]
cq = f'''<header class="hero"><div class="wrap"><h1>The chiquita in padel: what it is, how to hit it, and when to play it.</h1>
<p class="lead">The chiquita is a soft, low ball from the back that drops at the net players' feet, so your pair can take the net. Use the picker to see if this ball is a chiquita or a lob, learn the five steps, and see what to do when someone plays one at you.</p>
{quick("A chiquita (say chee-KEE-ta, Spanish for 'small one') is a slow, low shot played from the middle or back of the court so it lands at the feet of the opponents at the net. It makes them volley up, so you and your partner can move forward and attack the next ball. Play it soft, from a ball you can reach comfortably, when the other pair expects a lob; never from right against the back glass.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="cqp">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Chiquita or lob?</h2><p class="muted" style="margin-top:0">Three questions. You are at the back, they are at the net.</p>
{_bq2("cqp", "pos", "Where are you hitting from?", [("mid", "Middle of my half"), ("back", "Near the back glass"), ("glass", "Off a high rebound")], "mid")}
{_bq2("cqp", "opp", "Where are the net players?", [("close", "Very close to the net"), ("normal", "About 2 to 3 m from it"), ("back", "Stepping back for lobs")], "normal")}
{_bq2("cqp", "ball", "What is the ball like?", [("easy", "Easy, I have time"), ("hard", "Fast or awkward")], "easy")}</div>
<aside class="result" id="cqp-out" aria-live="polite"><h2 id="cqp-h"></h2><p id="cqp-p"></p><p id="cqp-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you hit a chiquita?</h2><p class="muted">Five steps. Forehand or backhand; many players find the backhand easier to slice.</p></div>
<div class="grid">{_cards(cq_steps, "Step")}</div></div></section>
{AD.format("cq-mid")}
<section><div class="wrap"><div class="sh"><h2>When should you play a chiquita?</h2></div><div class="grid">
<div class="card"><h3>When they expect a lob</h3><p>If the net pair starts to step back for your lobs, a chiquita at their feet catches them out.</p></div>
<div class="card"><h3>When they volley well from mid-court</h3><p>A pair that is comfortable volleying high balls has to bend and lift a low ball. That slows them down.</p></div>
<div class="card"><h3>When you want the net</h3><p>The chiquita is not a winner. It is a way to swap places: they hit up, you come forward.</p></div>
<div class="card"><h3>Down the middle or cross-court</h3><p>Through the middle is the safest. Cross-court at a player's body works too, but only from a good position, or a fast reply at your body can win them the point.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Common chiquita mistakes</h2></div><div class="grid">{_cards(cq_err)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you deal with a chiquita?</h2><p class="muted">When you are at the net and a low ball comes at your feet.</p></div><div class="grid">
<div class="card"><h3>Bend, don't attack</h3><p>You are below the net, so you cannot hit down. Bend your knees, keep the racket head up and play a soft, low volley back.</p></div>
<div class="card"><h3>Play it deep or soft</h3><p>Either a slow, deep volley down the middle to keep them back, or a soft drop at the feet of the player coming in. More in the <a href="{href("padel-volley.html")}">volley guide</a> (try the low volley in the picker).</p></div>
<div class="card"><h3>Don't stand too close</h3><p>About two to three metres from the net gives you time to bend for the chiquita and still turn for a lob.</p></div>
</div>
<p class="muted" style="margin-top:14px">Chiquita drill: one pair at the net, one at the back. The back pair must play a chiquita on any ball that bounces in the middle of the court, then move in. Score a point each time the net pair has to volley up. Then switch roles. More drills in the <a href="{href("drills.html")}">drills planner</a>. The chiquita's partner shot: <a href="{href("padel-lob.html")}">how to hit a lob</a>. Every shot: <a href="{href("shots.html")}">shot library</a>. Words like chiquita and globo: <a href="{href("glossary.html")}">glossary</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: The Padel School "Use the chiquita" and "Learn the chiquita" (slow ball at the feet, reachable ball, not against the back glass, soft so you can close in, cross-court only from a good position); Nox "La chiquita en pádel" (29 Jun 2021: counterattack from mid or back court, prepare like a lob, gentle and flat, move in at once); Padel USA "Learn about the chiquita" (12 May 2025: forehand or backhand, timing when they expect a lob, feet or the gap, use with the lob). Advice in our own words; the picker is our own summary.</p></div></section>'''
cq_faq = [
    ("What is a chiquita in padel?", "A slow, low ball played from the back half of the court that drops at the feet of the players at the net. It makes them hit up, so your pair can move forward."),
    ("How do you pronounce chiquita?", "Chee-KEE-ta. It is Spanish and means 'small one'."),
    ("When should you play a chiquita in padel?", "From a ball you can reach comfortably in the middle of your half, when the net pair expects a lob or is standing back a little. Not when you are pinned against the back glass."),
    ("Where should a chiquita land?", "At the net player's feet or in the gap between the two net players, low over the net so they have to volley up."),
    ("Chiquita or lob: which is better?", "Use both. The lob sends them back; the chiquita brings them in or makes them bend. Mixing them is what makes each one work."),
    ("How do you return a chiquita?", "Bend your knees, keep the racket head up and play a soft, low volley, deep down the middle or at the feet of the player coming in. Do not try to hit down on a ball below the net."),
]
page("padel-chiquita.html", "Chiquita in Padel: How and When to Play It + Picker",
     "The chiquita in padel: what it is, five steps to hit it, when to play it, mistakes, how to deal with one, and a free chiquita-or-lob picker for each ball.",
     cq, cq_faq, "Chiquita")

DEMAND_PAGES += ["padel-smash.html", "padel-chiquita.html"]
exec((ROOT / "demand8.py").read_text())
