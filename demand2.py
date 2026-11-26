# ---------------- DEMAND RUN 5 (26 Nov 2026): knockout bracket generator, beginner racket checker, padel vs racquetball vs platform tennis ----------------
# Executed from demand.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, json).
import math as _math

def _bq2(attr, name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-{attr}="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'

# ---------- 1. KNOCKOUT BRACKET GENERATOR ----------
def _ko_row(n):
    r = _math.ceil(_math.log2(n)); byes = 2 ** r - n
    return f"<tr><td>{n}</td><td>{n - 1}</td><td>{r}</td><td>{byes}</td><td>{2 ** r}</td></tr>"
ko = f'''<header class="hero"><div class="wrap"><h1>Padel tournament bracket generator (knockout).</h1>
<p class="lead">Type in your pairs, pick seeding and courts, and get a single-elimination draw with byes placed for you. Tap the winner of each match to move them on. It works out how long the event will take. Free, no app, saved on this device.</p>
{quick("A knockout with N pairs always has N - 1 matches (plus one if you play a 3rd-place match). 8 pairs = 7 matches over 3 rounds; 12 pairs = 11 matches over 4 rounds with 4 byes; 16 pairs = 15 matches over 4 rounds. Byes go to the top seeds so the draw fills up to the next 4, 8, 16 or 32.", "2026-11-26")}</div></header>
<section style="padding-top:10px"><div class="wrap gen" id="ko">
<div class="gen-main">
<div class="card" id="ko-setup">
<h2 style="font-size:1.6rem">Set up your knockout</h2>
<div class="q"><h3><label for="ko-names">Pairs, one team per line (3 to 32). Put the strongest first if you seed.</label></h3><textarea class="search" id="ko-names" rows="8" placeholder="Sam &amp; Priya&#10;Omar &amp; Lucia&#10;Ben &amp; Aisha&#10;..."></textarea><p class="muted" id="ko-count" style="margin:-6px 0 0"></p></div>
{_bq2("ko", "seed", "Draw", [("seed", "Seeded: 1st line is top seed"), ("rand", "Random draw")], "seed")}
{_bq2("ko", "fmt", "Match format", [("30", "One set (about 30-40 min)"), ("20", "Race to 4 games (about 20 min)"), ("60", "Best of 3 sets (about 60-90 min)"), ("15", "Timed 15 min")], "30")}
<div class="gen-nums"><div class="q"><h3><label for="ko-courts">Courts</label></h3><input class="search" id="ko-courts" type="number" min="1" max="16" value="2" inputmode="numeric"></div>
<div class="q"><h3><label for="ko-third">3rd-place match</label></h3><select class="search" id="ko-third"><option value="0">No</option><option value="1">Yes</option></select></div></div>
<p class="msg" id="ko-err" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:4px"><button class="btn lime" type="button" id="ko-start">Make the draw</button><button class="btn ghost" type="button" id="ko-demo">Fill 12 sample pairs</button></div>
</div>
<div id="ko-live" hidden>
<div class="card gen-bar"><div><span class="pill b" id="ko-sum"></span></div><div class="btns" style="margin:0"><button class="btn ghost sm" type="button" id="ko-copy">Copy draw</button><button class="btn ghost sm" type="button" id="ko-new">New draw</button></div></div>
<p class="muted" style="margin:0 0 10px">Tap a team to make it the winner. Tap again to undo. Scroll sideways to see later rounds.</p>
<div class="ko-wrap"><div class="ko-bk" id="ko-bk"></div></div>
</div>
</div>
<aside class="gen-side"><div class="lb" id="ko-board"><h2>Your event</h2><p>Make the draw to see the number of matches, rounds and how long it will take.</p></div></aside>
</div></section>
{AD.format("ko-mid")}
<section><div class="wrap"><div class="sh"><h2>How many matches and byes in a knockout?</h2><p class="muted">Matches are always one less than the teams, because every match knocks out one team.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Pairs</th><th scope="col">Matches</th><th scope="col">Rounds</th><th scope="col">Byes</th><th scope="col">Draw size</th></tr></thead><tbody>
{"".join(_ko_row(n) for n in (4, 5, 6, 8, 10, 12, 16, 20, 24, 32))}</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long does a padel match last?</h2></div><div class="grid">
<div class="card"><span class="pill b">Club best of 3</span><h3 style="margin-top:10px">About 50 to 90 minutes</h3><p>A study of official Italian sub-elite men's matches measured an average of about 54 minutes per match (Ungureanu and others, 2022), and the same paper puts elite matches at about 50 minutes. A retailer guide from Zona de Padel puts a typical three-set match at about 90 minutes and one set at about 18 minutes. Book 90 minutes of court time for a best-of-3 match.</p></div>
<div class="card"><span class="pill b">Rallies</span><h3 style="margin-top:10px">Under 10 seconds a point</h3><p>In professional World Padel Tour matches the average rally lasted about 9.4 seconds (Courel-Ibáñez and others, 2017). In the Italian sub-elite study it was about 6.7 seconds, with about 15 seconds' rest between rallies. Only about a third of match time is actual play.</p></div>
<div class="card"><span class="pill i">Planning</span><h3 style="margin-top:10px">Short formats for big draws</h3><p>For a one-night knockout, one set or a race to 4 games keeps rounds moving. Add 5 minutes per match for changeovers and warm-up. Want everyone to play all night? Use an <a href="{href("americano.html")}">Americano</a> or a <a href="{href("round-robin.html")}">round robin</a> instead: no one is knocked out.</p></div>
</div>
<p class="muted" style="margin-top:12px">Our time estimate in the tool uses your format's typical length plus 5 minutes per match, round by round across your courts. Real matches vary a lot with level and golden point vs advantage (<a href="{href("golden-point-star-point.html")}">golden point explained</a>).</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which tournament format should I use?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Format</th><th scope="col">Teams</th><th scope="col">Best for</th><th scope="col">Downside</th></tr></thead><tbody>
<tr><td>Knockout (this tool)</td><td>Fixed pairs</td><td>A clear winner fast, many pairs, few courts</td><td>Half the teams play only once</td></tr>
<tr><td><a href="{href("round-robin.html")}">Round robin</a></td><td>Fixed pairs</td><td>Fair results, everyone plays everyone</td><td>Many matches if there are lots of pairs</td></tr>
<tr><td><a href="{href("padel-group-stage-generator.html")}">Groups then knockout</a></td><td>Fixed pairs</td><td>Bigger events: round robin groups of 3 or 4, then top 2 into a knockout</td><td>Needs more court time</td></tr>
<tr><td><a href="{href("americano.html")}">Americano / Mexicano</a></td><td>Partners change</td><td>Social nights, mixed levels</td><td>Individual winner, not a team</td></tr>
<tr><td><a href="{href("king-of-the-court.html")}">King of the Court</a></td><td>Fixed pairs</td><td>Quick games on one court</td><td>Only one court</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Running groups first? Use the <a href="{href("padel-group-stage-generator.html")}">group stage generator</a>: it makes the groups, keeps the tables and sends the qualifiers here in seed order. Keep score on court with the <a href="{href("score.html")}">score keeper</a>.</p></div></section>'''
ko_faq = [
    ("How many matches are in a padel knockout tournament?", "One less than the number of pairs: 8 pairs play 7 matches, 16 pairs play 15. Add one if you play a 3rd-place match."),
    ("How do byes work in a padel bracket?", "If the number of pairs is not 4, 8, 16 or 32, some teams skip round 1. Byes fill the draw up to the next size and go to the top seeds. 12 pairs in a 16 draw means 4 byes."),
    ("How long does a padel match last?", "A best-of-3 club match is usually about 50 to 90 minutes. A study of Italian sub-elite matches measured about 54 minutes on average. One set takes roughly 20 to 40 minutes."),
    ("How long does a padel tournament take?", "Count the rounds, then how many matches each round needs per court. 8 pairs on 2 courts with one-set matches is 4 match slots, or about 2 hours 20 minutes with changeovers. The tool above works it out for you."),
    ("Should I seed a padel tournament?", "Seed if you know the levels, so the two strongest pairs can only meet in the final. Use a random draw for social events or when no one knows the levels."),
]
page("padel-tournament-bracket.html", "Padel Tournament Bracket Generator: Free Knockout Draw | Padel Glass Box",
     "Free padel tournament bracket generator: type your pairs, get a knockout draw with seeds and byes, tap winners to move on, and see how long the event takes. No app.",
     ko, ko_faq, "Tournament bracket generator")

# ---------- 2. BEST PADEL RACKET FOR BEGINNERS: SPEC CHECKER ----------
bc_form = (_bq2("bc", "shape", "Shape", [("round", "Round"), ("tear", "Teardrop"), ("diamond", "Diamond"), ("x", "Not sure")], "round")
    + '<div class="q"><h3><label for="bc-w">Weight in grams (look on the frame or the shop page)</label></h3><input class="search" id="bc-w" type="number" min="250" max="420" value="360" inputmode="numeric" style="margin:0"></div>'
    + _bq2("bc", "bal", "Balance", [("low", "Low / head-light"), ("even", "Even / medium"), ("high", "High / head-heavy"), ("x", "Not sure")], "low")
    + _bq2("bc", "core", "Core feel", [("soft", "Soft (soft EVA / foam)"), ("med", "Medium"), ("hard", "Hard EVA"), ("x", "Not sure")], "soft")
    + _bq2("bc", "face", "Face material", [("glass", "Fibreglass"), ("hyb", "Fibreglass + carbon"), ("carbon", "Carbon (3K, 12K, 18K...)"), ("x", "Not sure")], "glass")
    + _bq2("bc", "arm", "Any elbow, shoulder or wrist pain?", [("n", "No"), ("y", "Yes")], "n")
    + _bq2("bc", "who", "Who is it for?", [("adult", "Adult"), ("light", "Smaller adult or teen"), ("kid", "Child under 12")], "adult"))
bc_rows = [
    ("Shape", "Round", "The sweet spot sits low and in the middle, so off-centre hits still go over. Teardrop is fine once you hit cleanly; diamond is for power players."),
    ("Weight", "About 355 to 370 g (adults); 340 to 360 g for smaller players or a sore arm", "Light enough to swing late without tiring, heavy enough to stay stable on volleys."),
    ("Balance", "Low or even", "A head-light racket is quick at the net and kinder on the elbow."),
    ("Core", "Soft EVA or foam", "Soft cores give easy depth with a slow swing and soak up vibration."),
    ("Face", "Fibreglass or a fibreglass-carbon mix", "Fibreglass is flexible and forgiving. Stiff, high-K carbon faces reward fast swings beginners don't have yet."),
    ("Price", "Beginner rackets start just under £50 in the UK and about $60 to $130 in the US", f'Past that you mostly pay for stiffness and power. See <a href="{href("padel-cost.html")}">what padel costs</a>.'),
]
bc_tbl = "".join(f"<tr><td>{a}</td><td><strong>{b}</strong></td><td>{c}</td></tr>" for a, b, c in bc_rows)
bc = f'''<header class="hero"><div class="wrap"><h1>Best padel racket for beginners: check any racket in 30 seconds.</h1>
<p class="lead">Found a racket in a shop or online? Put in its shape, weight, balance, core and face, and see if it suits a beginner, spec by spec, with the reason. No brands pushed, no sign-up.</p>
{quick("The best padel racket for a beginner is round, about 355 to 370 g, head-light (low balance), with a soft EVA or foam core and a fibreglass or fibreglass-carbon face. That mix gives a big sweet spot, easy depth and less strain on the arm. You don't need to spend much: good beginner rackets start just under £50 or about $60 to $130.", "2026-11-26")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="bc">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Beginner racket checker</h2>
<p class="muted" style="margin-top:0">Pick what the racket's page or frame says. "Not sure" is fine: we tell you what to look for.</p>
{bc_form}
</div>
<aside class="result" id="bc-out" aria-live="polite"><h2 id="bc-h">Checking...</h2><p id="bc-p"></p><ul class="bc-list" id="bc-list"></ul><p id="bc-next" class="wr-src"></p></aside>
</div></section>
<script>window.BCGO={json.dumps({k: go(k) for k in ("padel-round-rackets", "padel-rackets", "padel-overgrips")})};</script>
{AD.format("bc-mid")}
<section><div class="wrap"><div class="sh"><h2>What should a beginner padel racket have?</h2><p class="muted">The same advice comes up in most beginner buying guides from padel shops and coaches. These are general ranges, not rules.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Spec</th><th scope="col">Beginner pick</th><th scope="col">Why</th></tr></thead><tbody>{bc_tbl}</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What are the most common mistakes when buying a first padel racket?</h2></div><div class="grid">
<div class="card"><h3>Buying a pro's racket</h3><p>Diamond, head-heavy, hard carbon rackets are built for players who already hit cleanly and fast. For a beginner they feel dead on mis-hits and can hurt the elbow.</p></div>
<div class="card"><h3>Paying for power you can't use</h3><p>Expensive usually means stiffer. At the start, control and comfort win more points than power. Our <a href="{href("cheap-padel-rackets.html")}">cheap padel rackets guide</a> shows what good budget rackets look like.</p></div>
<div class="card"><h3>Too heavy "for stability"</h3><p>A racket over about 375 g gets slow and tiring by the third set. If your arm aches after playing, go lighter and softer (see <a href="{href("padel-injuries.html")}">padel injuries</a>).</p></div>
<div class="card"><h3>Ignoring the grip</h3><p>A thin handle makes you squeeze too hard. Add an overgrip or two to build it up, and learn the <a href="{href("padel-grip.html")}">continental grip</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When should a beginner upgrade?</h2></div>
<div class="card"><p>Most players keep a beginner racket for their first year or so. Think about a change when you hit the sweet spot most of the time, play the bandeja on purpose and want more power on overheads. Then a teardrop, medium-firm racket is the usual next step: check yours with the <a href="{href("intermediate-padel-racket.html")}">intermediate racket upgrade check</a>. Not sure of your level? Take the <a href="{href("level-calculator.html")}">level calculator</a>. Want a full recommendation from your style? Use the <a href="{href("racket-finder.html")}">racket finder</a>. Buying for a child? See <a href="{href("padel-racket-for-kids.html")}">padel rackets for kids</a>.</p></div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop beginner-friendly rackets</h3><p>Round rackets are the easiest place to start. Check each one's weight, balance and core with the tool above before you buy.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Balls</a></li></ul>{AFF_NOTE}</div></div></section>'''
bc_faq = [
    ("What is the best padel racket for a beginner?", "A round racket of about 355 to 370 g with a low balance, a soft EVA or foam core and a fibreglass face. It forgives off-centre hits and is kind to the arm."),
    ("What weight padel racket should a beginner use?", "Most adult beginners do well with about 355 to 370 g. Smaller players, teens or anyone with elbow pain can go to about 340 to 360 g."),
    ("Is a carbon padel racket good for beginners?", "A carbon-fibreglass mix is fine. Full high-K carbon faces are stiffer and suit fast swings, so most beginners get more from fibreglass."),
    ("How much should a beginner spend on a padel racket?", "Not much. Good beginner rackets start just under £50 in the UK and about $60 to $130 in the US. Many clubs also hire rackets while you decide."),
    ("Round, teardrop or diamond for beginners?", "Round. It has the biggest, lowest sweet spot. Teardrop is the usual second racket; diamond is for advanced, attacking players."),
]
page("best-padel-racket-for-beginners.html", "Best Padel Racket for Beginners: Free Spec Checker (2026) | Padel Glass Box",
     "Best padel racket for beginners: round, 355-370 g, low balance, soft core, fibreglass face. Check any racket's specs in 30 seconds and see if it suits a beginner.",
     bc, bc_faq, "Best beginner padel racket")

# ---------- 3. PADEL VS RACQUETBALL VS PLATFORM TENNIS ----------
vr_rows = [
    ("Court", "20 x 10 m (65.6 x 32.8 ft)", "40 x 20 ft (12.2 x 6.1 m), 20 ft (6.1 m) high", "44 x 20 ft (13.4 x 6.1 m) on a 60 x 30 ft deck"),
    ("Walls", "Glass and mesh walls, ball can be played off them after the bounce", "Four walls and the ceiling: all surfaces in play", "12 ft (3.7 m) wire screens, ball can be played off them after the bounce"),
    ("Net", "Yes: 88 cm in the middle, 92 cm at the posts", "No net: you share the court and hit the front wall", "Yes: 34 in (86 cm) in the middle, 37 in (94 cm) at the posts"),
    ("Racket", "Solid, holed padel racket, no strings", "Strung racquet, up to 22 in long, with a wrist cord", "Solid paddle up to 18 in long and 12 in wide"),
    ("Ball", "Pressurised ball, like a slightly softer tennis ball", "Small hollow rubber ball, about 2.25 in across", "Flocked rubber ball"),
    ("Serve", "Underarm, bounce then hit at or below the waist, diagonal box, 2 tries", "Bounce in the service zone, hit the front wall first, land past the short line, 2 tries", "Overarm allowed, into the diagonal box, only 1 serve in doubles"),
    ("Scoring", "Tennis scoring (15, 30, 40), sets to 6, golden point common", "Games to 15, only the server scores, best of 3 with an 11-point tiebreaker", "Tennis scoring, sets to 6, 7-point tie-break at 6-6"),
    ("Players", "Almost always doubles", "Singles or doubles", "Almost always doubles"),
    ("Where", "Fast growing in Europe, the UK, the Middle East and the US", "Mainly indoor courts in the US and Canada", "Mainly the north-east US, outdoors in winter, often with heaters under the deck"),
]
vr_tbl = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in vr_rows)
vr_form = (_bq2("vr", "a", "What sounds most fun?", [("p", "Long doubles rallies with walls"), ("r", "Fast, sweaty, every surface in play"), ("t", "Outdoor game in the cold months")], "p")
    + _bq2("vr", "b", "Who will you play with?", [("p", "Three friends"), ("r", "One friend or alone"), ("t", "A winter club group")], "p")
    + _bq2("vr", "c", "Your background", [("p", "Tennis or none"), ("r", "Squash"), ("t", "Tennis, and I live in the US north-east")], "p"))
vr = f'''<header class="hero"><div class="wrap"><h1>Padel vs racquetball vs platform tennis: the differences.</h1>
<p class="lead">All three are racket sports where walls or screens matter, so people mix them up. Here is how court, racket, ball, serve and scoring compare, side by side, from each sport's official rules.</p>
{quick("Padel is doubles on a 20 x 10 m glass court with a net and a solid racket; the ball may hit the walls after it bounces. Racquetball has no net: you hit a small rubber ball against the front wall of a closed 40 x 20 x 20 ft room, and every wall and the ceiling are in play. Platform tennis is outdoor doubles on a 44 x 20 ft court inside 12 ft wire screens, with one serve and tennis scoring.", "2026-11-26")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="sh"><h2>Padel, racquetball and platform tennis compared</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">What</th><th scope="col">Padel</th><th scope="col">Racquetball</th><th scope="col">Platform tennis</th></tr></thead><tbody>{vr_tbl}</tbody></table></div>
<p class="muted" style="margin-top:12px">Sources: padel from the FIP rules (see our <a href="{href("rules.html")}">padel rules</a> and <a href="{href("court-dimensions.html")}">court dimensions</a>); racquetball from the USA Racquetball rulebook; platform tennis from the American Platform Tennis Association (APTA) rules. Metric values are our conversions, rounded.</p></div></section>
<section style="padding-top:0"><div class="wrap quiz" id="vr">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Which one should you try?</h2><p class="muted" style="margin-top:0">Three quick taps.</p>{vr_form}</div>
<aside class="result" id="vr-out" aria-live="polite"><h2 id="vr-h"></h2><p id="vr-p"></p><p id="vr-next" class="wr-src"></p></aside>
</div></section>
{AD.format("vr-mid")}
<section><div class="wrap"><div class="sh"><h2>What is the difference between padel and racquetball?</h2></div><div class="grid">
<div class="card"><h3>Net vs front wall</h3><p>In padel two teams face each other across a net. In racquetball both players stand in the same room and take turns hitting the front wall, like squash.</p></div>
<div class="card"><h3>When walls count</h3><p>In padel the ball must bounce on your side before it hits your walls. In racquetball the ball can hit side walls, the back wall and the ceiling on the way, as long as it reaches the front wall.</p></div>
<div class="card"><h3>Scoring</h3><p>Padel uses tennis scoring and anyone can win a point. Racquetball games go to 15 and only the serving side scores.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What is the difference between padel and platform tennis?</h2></div><div class="grid">
<div class="card"><h3>Closest cousins</h3><p>Both are doubles, use solid holed rackets or paddles, tennis scoring and let you play the ball off the walls or screens after the bounce. Players switch between them easily.</p></div>
<div class="card"><h3>Court and walls</h3><p>A padel court is bigger (20 x 10 m) with glass back walls. A platform tennis court is 44 x 20 ft inside tight wire screens on a raised deck.</p></div>
<div class="card"><h3>Serve and season</h3><p>Padel serves are underarm with 2 tries. Platform tennis allows an overarm serve, but only one in doubles. Platform tennis is mostly a winter outdoor game in the north-east US.</p></div>
</div>
<p class="muted" style="margin-top:12px">Comparing with other sports too? See <a href="{href("padel-vs-squash.html")}">padel vs squash</a>, <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a>, <a href="{href("squash-court-dimensions.html")}">squash court dimensions</a> and <a href="{href("court-sizes-compared.html")}">all court sizes to scale</a>.</p></div></section>'''
vr_faq = [
    ("Is padel the same as racquetball?", "No. Padel is played over a net on a glass-walled court, mostly in doubles. Racquetball has no net: players hit the front wall of a closed room and every surface, including the ceiling, is in play."),
    ("Is platform tennis the same as padel?", "No, but they are close. Both are doubles with solid paddles, tennis scoring and walls or screens in play after the bounce. Platform tennis is on a smaller 44 x 20 ft court inside wire screens and has only one serve in doubles."),
    ("Is padel easier than racquetball?", "Most beginners find padel easier to start: the underarm serve, slower ball and doubles court make rallies come quickly. Racquetball is faster and more tiring from the first game."),
    ("How big is a racquetball court?", "40 ft long, 20 ft wide and 20 ft high (about 12.2 x 6.1 x 6.1 m), under the USA Racquetball rules."),
    ("How big is a platform tennis court?", "The playing court is 44 x 20 ft on a 60 x 30 ft deck, surrounded by 12 ft wire screens (APTA rules)."),
]
page("padel-vs-racquetball.html", "Padel vs Racquetball vs Platform Tennis: Differences | Padel Glass Box",
     "Padel vs racquetball vs platform tennis: court size, walls, net, racket, ball, serve and scoring side by side from official rules, plus a quick quiz on which to try.",
     vr, vr_faq, "Padel vs racquetball")

DEMAND_PAGES += ["padel-tournament-bracket.html", "best-padel-racket-for-beginners.html", "padel-vs-racquetball.html"]
exec((ROOT / "demand3.py").read_text())
