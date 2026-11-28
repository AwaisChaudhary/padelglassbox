# ---------------- DEMAND RUN 22 (28 Nov 2026): padel match length calculator, pickleball serve rules + checker ----------------
# Executed from demand20.py (shares page(), quick(), href(), e(), AD, _bq2, _cards).

# ---------- 1. HOW LONG IS A PADEL MATCH (calculator) ----------
# Evidence: 'how long does a padel match last' answered by zonadepadel, tiendapadel5, esprit-padel-shop (5 locales), bornlivingyoga,
# padel-rules / padelmix mini-sites, abargenteuil.fr (28 Nov 2026 web search); DEMAND X4.
# Sources: Ungureanu, Lupo, Brustio (2022) IJERPH 19:8386 (Italian Serie B, 6 matches: 53.7 min average, 16.8 min effective play = 31.3%,
# rally 6.7 s, rest between rallies 14.8 s); Courel-Ibanez et al. (2017) J Hum Kinet 55:161 (WPT Masters Finals 2013, 1527 rallies,
# rally 9.4 s); Martin-Miguel et al. (2024) Sports 12:218 (WPT 2020, 20 matches, men's points 13.5-14.8 s, women's 14.4-16.2 s;
# cites 90-120 min for pro matches). FIP rules for rest times (20 s / 90 s / 120 s, no rest after game 1 of a set).
ml = f'''<header class="hero"><div class="wrap"><h1>How long is a padel match? Match length calculator</h1>
<p class="lead">Pick the format, the deuce rule and your level. The calculator plays the match 2,000 times with real padel scoring and rest times, and tells you how long it usually takes, and if it fits your court booking.</p>
{quick("A club padel match of best of 3 sets usually takes <strong>about 60 to 90 minutes</strong>. Two sets with a super tie-break instead of a third set takes about <strong>45 to 70 minutes</strong>, and one set about <strong>20 to 35 minutes</strong>. A study of Italian second-division matches measured an average of <strong>54 minutes</strong>, with only about a third of that time spent actually rallying. Pro matches often take 90 minutes or more.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="ml">
<div>
{_bq2("ml", "fmt", "Match format", [("3", "Best of 3 sets"), ("stb", "2 sets + super tie-break"), ("1", "One set")], "3")}
{_bq2("ml", "deuce", "At 40-40", [("gp", "Golden point"), ("star", "Star Point"), ("adv", "Advantage")], "gp")}
{_bq2("ml", "lvl", "Your level", [("new", "Beginners"), ("club", "Club players"), ("adv", "Advanced")], "club")}
{_bq2("ml", "even", "How close are the pairs?", [("even", "Very even"), ("mid", "One pair a bit better"), ("one", "One-sided")], "even")}
{_bq2("ml", "warm", "Warm-up on court", [("0", "None"), ("5", "5 minutes"), ("10", "10 minutes")], "5")}
</div>
<aside class="result" id="ml-out" aria-live="polite"><h2>Working it out</h2><p>Pick your options and the estimate appears here.</p></aside>
</div>
<p class="muted" style="margin-top:12px">How it works: each point has a chance of going to the server that depends on your level and how even the pairs are. Each point takes about 20 to 25 seconds of rally plus rest (about 22 s for club players, from the Italian study: 6.7 s rally + 14.8 s rest). We add 90 seconds at each change of ends (none after the first game of a set) and 2 minutes between sets, as the FIP rules allow. Real matches vary: long rallies, chat and ball-chasing add time. It is an estimate, not a promise.</p>
</div></section>
{AD.format("ml-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long does each padel format take?</h2><p class="muted">Typical club times from the calculator (golden point, even pairs, no warm-up). Middle 80% of matches.</p></div>
<div class="tbl"><table><thead><tr><th>Format</th><th>Typical length</th><th>Games played (average)</th><th>Fits a</th></tr></thead><tbody>
<tr><td>One set (first to 6, tie-break at 6-6)</td><td>20 to 35 min</td><td>About 10</td><td>Short slot or Americano round</td></tr>
<tr><td>2 sets + super tie-break to 10</td><td>45 to 70 min</td><td>About 18</td><td>60 to 90 minute booking</td></tr>
<tr><td>Best of 3 sets, golden point</td><td>45 to 90 min</td><td>About 24</td><td>90 minute booking</td></tr>
<tr><td>Best of 3 sets, advantage</td><td>50 to 100 min</td><td>About 24</td><td>90 to 120 minute booking</td></tr>
<tr><td>Pro match (Premier Padel)</td><td>Often 90 to 120 min</td><td>Often 20 to 30</td><td>TV slot</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What makes a padel match longer or shorter?</h2></div><div class="grid">{_cards([
    ("The deuce rule", "Advantage scoring adds about 10% to a match compared with golden point, because games at 40-40 can go on. Star Point sits in between: two advantages, then one deciding point."),
    ("A super tie-break", "Playing a tie-break to 10 instead of a third set saves 15 to 30 minutes. That is why leagues and club tournaments love it. See <a href='" + href("tie-break.html") + "'>tie-break rules</a>."),
    ("Level", "Better players have longer rallies. Pro points last about 10 to 15 seconds, club rallies nearer 7. Beginners have short rallies but spend time picking up balls."),
    ("How even the pairs are", "Even pairs mean more deuces, more tie-breaks and more third sets. A one-sided match can be over in under 45 minutes."),
    ("Rest and chat", "Under FIP rules you get 20 seconds between points, 90 at changes of ends and 2 minutes between sets. At clubs, slow ball-collecting often adds more."),
    ("Warm-up", "The FIP warm-up is usually 3 to 5 minutes. At clubs, agree it first: a 10-minute warm-up eats a big part of a 60-minute booking."),
])}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What did the studies measure?</h2></div>
<div class="tbl"><table><thead><tr><th>Study</th><th>Level</th><th>Finding</th></tr></thead><tbody>
<tr><td>Ungureanu and others, 2022 (6 matches)</td><td>Italian Serie B, men</td><td>53.7 min average match. Only 16.8 min (31%) was ball in play. Rallies 6.7 s, rest between rallies 14.8 s, about 4.7 shots per rally.</td></tr>
<tr><td>Courel-Ibáñez and others, 2017 (1,527 rallies)</td><td>World Padel Tour Masters Finals, men</td><td>Rallies 9.4 s on average; over half the points were won between the 5th and 11th second.</td></tr>
<tr><td>Martín-Miguel and others, 2024 (20 matches)</td><td>World Padel Tour 2020, men and women</td><td>Men's points 13.5 to 14.8 s, women's 14.4 to 16.2 s (longer). About 160 points per match.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px;font-size:.9rem">Sources, checked 28 Nov 2026: Ungureanu, Lupo and Brustio, "Padel match analysis", International Journal of Environmental Research and Public Health 19 (2022) 8386; Courel-Ibáñez, Sánchez-Alcaraz and Cañas, Journal of Human Kinetics 55 (2017) 161-169; Martín-Miguel and others, Sports 12 (2024) 218; FIP rules of padel for rest times. Blog estimates of "about 90 minutes" give no source, so we show the study figures.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Keep score</h3><p>Use the <a href="{href("score.html")}">padel score keeper</a> or the <a href="{href("padel-match-tracker.html")}">match tracker</a> with golden point, Star Point or advantage.</p></div>
<div class="card"><h3>Short on time?</h3><p>Play an <a href="{href("americano.html")}">Americano</a>: fixed points per round, so every round takes about the same time.</p></div>
<div class="card"><h3>Burn it off</h3><p>See how many calories that match was with the <a href="{href("padel-calories.html")}">padel calories calculator</a>.</p></div>
</div></div></section>'''
ml_faq = [
    ("How long does a padel match last?", "A club match of best of 3 sets usually takes about 60 to 90 minutes. Two sets plus a super tie-break takes about 45 to 70 minutes, and one set about 20 to 35 minutes. A study of Italian second-division matches measured 54 minutes on average."),
    ("How long is a professional padel match?", "Pro matches on the Premier Padel tour often take 90 minutes to 2 hours, because points are longer (about 10 to 15 seconds) and many matches go to three sets."),
    ("How long is one set of padel?", "Usually about 20 to 35 minutes for club players, depending on how close it is and whether you play golden point or advantage."),
    ("Is 90 minutes enough for a padel match?", "Usually yes. A 90-minute booking fits a best-of-3 match with golden point and a short warm-up most of the time. With advantage scoring and two even pairs, a third set can push you past 90 minutes, so play a super tie-break instead."),
    ("How much of a padel match is actual play?", "Only about a third. In the Italian study, 31% of the match was ball in play; the rest was time between points, changes of ends and breaks."),
    ("How long is a padel game?", "One game (to 4 points) usually takes about 2 to 3 minutes for club players, longer at 40-40 with advantage scoring."),
]
page("padel-match-length.html", "How Long Is a Padel Match? Match Length Calculator",
     "How long does a padel match last? Best of 3 sets is usually 60-90 minutes. Free calculator by format, golden point or advantage, level and warm-up, with booking fit.",
     ml, ml_faq, "Padel match length")
DEMAND_PAGES += ["padel-match-length.html"]

# ---------- 2. PICKLEBALL SERVE RULES (2026) + serve checker ----------
# Evidence: DEMAND E-R1, Google autocomplete 'pickleball how to' #2 = 'pickleball how to serve'; many 2026 rule-change explainers
# (justpaddles, thekitchenpickle, playpickleball, pickleball.com, mypickleballconnect 'serve rules 2026' and 'drop serve vs volley serve 2026').
# Sources: USA Pickleball 2026 Rulebook Change Document (17 Dec 2025, rules 7.B.2 spin, 7.C.1-7.C.3 volley serve, 7.E landing, 4.B game-winning
# point, 14.A.2 / 15.C.2 provisional rally scoring); The Kitchen Pickle and PlayPickleball 2026 rule-change articles (effective 1 Jan 2026, borderline = fault).
ps = f'''<header class="hero"><div class="wrap"><h1>Pickleball serve rules (2026): volley serve, drop serve and a legal-serve checker</h1>
<p class="lead">How to serve in pickleball under the 2026 USA Pickleball rules, what changed this year, and a quick checker to settle "was that serve legal?" on court.</p>
{quick("Serve <strong>diagonally</strong>, with both feet behind the baseline. With a <strong>volley serve</strong>, three things must be clearly true when you hit the ball: the paddle is moving in an <strong>upward arc</strong>, the top of the paddle head is <strong>not above your wrist</strong>, and the ball is <strong>no higher than your waist</strong>. Or use a <strong>drop serve</strong>: drop the ball, let it bounce, then hit it. The serve must <strong>clear the kitchen</strong> (a serve on the kitchen line is a fault) and land in the diagonal service court. You get <strong>one serve</strong>; a serve that clips the net and lands in is in play.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="ps">
<div>
{_bq2("ps", "type", "Which serve?", [("v", "Volley serve"), ("d", "Drop serve")], "v")}
{_bq2("ps", "feet", "Where were the server's feet?", [("ok", "Both behind the baseline, inside the lines"), ("line", "A foot on or over the baseline"), ("wide", "Outside the sideline or centreline extension")], "ok")}
<div id="ps-v">
{_bq2("ps", "arc", "At contact, was the paddle moving upward?", [("y", "Yes, clearly"), ("n", "No, or not sure")], "y")}
{_bq2("ps", "wrist", "Was the top of the paddle head above the wrist?", [("n", "No, below the wrist"), ("y", "Yes, or level and unclear")], "n")}
{_bq2("ps", "waist", "Where was the ball when it was hit?", [("low", "Clearly below the waist"), ("high", "At or above the waist, or unclear")], "low")}
</div>
<div id="ps-d" hidden>
{_bq2("ps", "drop", "How was the ball released?", [("drop", "Just dropped from the hand"), ("toss", "Tossed up, thrown down or bounced")], "drop")}
</div>
{_bq2("ps", "spin", "Did the server spin the ball with their hand when releasing it?", [("n", "No"), ("y", "Yes")], "n")}
{_bq2("ps", "land", "Where did the serve land?", [("in", "In the diagonal service court"), ("net", "Clipped the net, then landed in"), ("kline", "On the kitchen line"), ("k", "In the kitchen"), ("line", "On the sideline or baseline"), ("out", "Out, or the wrong court")], "in")}
</div>
<aside class="result" id="ps-out" aria-live="polite"><h2>Make the call</h2><p>Answer the questions and the verdict appears here.</p></aside>
</div></div></section>
{AD.format("ps-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you serve in pickleball, step by step?</h2></div><div class="grid">{_cards([
    ("Call the score", "Before serving, say the score: in doubles three numbers (your score, their score, server 1 or 2), in singles two. The first serve of a doubles game is called 0-0-2."),
    ("Stand in the right place", "Both feet behind the baseline, between the centreline and the sideline (imagine them extended). Serve from the right side when your score is even in singles; in doubles you start on the right and switch with your partner each time you win a point on serve."),
    ("Choose volley or drop", "Volley serve: hit the ball out of the air with an upward swing, below the waist. Drop serve: drop the ball from your hand, let it bounce, then hit it."),
    ("Aim diagonally, deep", "The ball must clear the kitchen (the 7 ft non-volley zone) and land in the service court across from you. Deep serves give the receiver less time."),
    ("Then let it bounce", "After the serve, the return must bounce, and your next shot must bounce too (the two-bounce rule). Only then can anyone volley."),
], pill="Step")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Volley serve vs drop serve</h2></div>
<div class="tbl"><table><thead><tr><th></th><th>Volley serve</th><th>Drop serve</th></tr></thead><tbody>
<tr><td>How you hit it</td><td>Out of the air</td><td>After one bounce</td></tr>
<tr><td>Paddle moving upward</td><td>Must be, clearly</td><td>Not required</td></tr>
<tr><td>Paddle head below the wrist</td><td>Must be, clearly</td><td>Not required</td></tr>
<tr><td>Ball below the waist</td><td>Must be, clearly</td><td>Not required</td></tr>
<tr><td>Releasing the ball</td><td>No spin added with the hand</td><td>Drop it: no tossing, throwing or bouncing it down; no spin added with the hand</td></tr>
<tr><td>Spin off the paddle</td><td>Allowed</td><td>Allowed</td></tr>
<tr><td>Good for</td><td>Players with a steady swing</td><td>Beginners, and anyone whose volley serve is called often</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What changed in the 2026 pickleball serve rules?</h2><p class="muted">The 2026 USA Pickleball rulebook took effect on 1 January 2026 and was renumbered; the serve is now rule 7.</p></div>
<div class="tbl"><table><thead><tr><th>Topic</th><th>2026 rule</th><th>What it means</th></tr></thead><tbody>
<tr><td>Upward motion (7.C.1)</td><td>The <em>paddle</em> must move in a clear upward arc at contact</td><td>Before 2026 the rule talked about the arm. Now it is the paddle that counts.</td></tr>
<tr><td>"Clearly"</td><td>Each volley-serve test must be clearly met</td><td>If the referee can't tell, it is a fault. Borderline serves are no longer given the benefit of the doubt.</td></tr>
<tr><td>Spin (7.B.2)</td><td>No spin added with the hand or body before contact</td><td>No finger-spin release. Spin from the paddle at contact is still fine, on both serves.</td></tr>
<tr><td>Landing (7.E)</td><td>Must clear the non-volley zone, with or without touching the net, and land in the correct court</td><td>Net serves that land in are played. Wrong court is a fault.</td></tr>
<tr><td>Scoring (provisional)</td><td>Rally scoring allowed in some events; the receiving side can win the game on the last rally</td><td>Traditional side-out scoring is still standard at most clubs. Check which one your event uses.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px;font-size:.9rem">Sources, checked 28 Nov 2026: USA Pickleball 2026 Rulebook Change Document (published 17 Dec 2025, rules 7.B.2, 7.C, 7.E, 4.B, 14.A.2, 15.C.2); The Kitchen Pickle and PlayPickleball 2026 rule-change guides. Local leagues can use their own house rules.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Common serve faults</h2></div><div class="grid">{_cards([
    ("Serve on the kitchen line", "The kitchen line is part of the kitchen, so a serve that touches it is a fault. Sidelines, the centreline and the baseline are in."),
    ("Foot on the baseline", "Stepping on or over the baseline before you hit the ball is a foot fault. Stay behind it until contact."),
    ("Paddle above the wrist", "On a volley serve, the top of the paddle head must stay below your wrist at contact. A high, tennis-style swing is a fault. Use a drop serve if you like a freer swing."),
    ("Tossing on a drop serve", "The drop serve is a drop. Throwing the ball up or bouncing it down hard is a fault."),
    ("Serving from the wrong side", "In singles, serve from the right when your score is even and the left when it is odd. In doubles, check who should be serving before every point."),
])}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>More pickleball</h2></div><div class="grid">
<div class="card"><h3>All the rules</h3><p>The kitchen, the two-bounce rule and scoring: <a href="{href("pickleball-rules.html")}">pickleball rules explained</a>.</p></div>
<div class="card"><h3>Keep score</h3><p>The <a href="{href("pickleball-score.html")}">pickleball score keeper</a> calls the three numbers for you.</p></div>
<div class="card"><h3>Coming to padel?</h3><p>The padel serve is underhand too, but it must bounce first and you get two tries. See <a href="{href("serve-rules.html")}">padel serve rules</a> and <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs pickleball</a>.</p></div>
</div></div></section>'''
ps_faq = [
    ("What are the serve rules in pickleball?", "Serve diagonally with both feet behind the baseline. A volley serve must be hit with the paddle moving upward, the paddle head not above the wrist and the ball below the waist. Or drop the ball and hit it after it bounces. The serve must clear the kitchen, including its line, and land in the diagonal court. You get one serve."),
    ("What is the difference between a volley serve and a drop serve?", "A volley serve is hit out of the air and must follow three motion rules (upward paddle, paddle head below wrist, ball below waist). A drop serve is dropped from the hand and hit after it bounces, and those motion rules do not apply."),
    ("Is a serve that hits the net legal in pickleball?", "Yes. There are no service lets. A serve that touches the net and still clears the kitchen and lands in the correct court is in play. If it lands in the kitchen or out, it is a fault."),
    ("Can you put spin on a pickleball serve?", "Yes, from the paddle. Under the current rules you may not spin the ball with your hand or body when you release it, but spin made by the paddle at contact is allowed on both serves."),
    ("Do you get two serves in pickleball?", "No. Each server gets one attempt. In doubles both partners serve before the serve passes to the other side, except at the start of the game, when only one player serves."),
    ("Is a serve on the kitchen line in?", "No. The kitchen line is part of the non-volley zone, so a serve that lands on it is a fault. A serve on the sideline, centreline or baseline is in."),
]
page("pickleball-serve-rules.html", "Pickleball Serve Rules 2026: Volley vs Drop Serve + Checker",
     "Pickleball serve rules for 2026: volley serve (paddle upward, below wrist, below waist), drop serve, spin, kitchen line, net serves, and a free legal-serve checker.",
     ps, ps_faq, "Pickleball serve rules")
DEMAND_PAGES += ["pickleball-serve-rules.html"]
