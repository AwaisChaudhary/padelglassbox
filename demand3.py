# ---------------- DEMAND RUN 6 (26 Nov 2026): groups + knockout generator, DUPR rating guide + match checker, padel vs squash ----------------
# Executed from demand2.py (shares page(), quick(), href(), e(), AD, _bq2).

# ---------- 1. GROUPS THEN KNOCKOUT GENERATOR ----------
gs = f'''<header class="hero"><div class="wrap"><h1>Padel group stage generator: groups, then a knockout.</h1>
<p class="lead">The format most club tournaments use. Type your pairs, pick the group size, and get balanced groups with every match listed. Type the games won, and the tables sort themselves. When the groups are done, send the qualifiers to our knockout bracket in one tap. Free, no app, saved on this device.</p>
{quick("Split the pairs into groups of 3 or 4, play a round robin in each group (3 matches in a group of 3, 6 in a group of 4), rank by matches won, then game difference, then games won, and send the top 1 or 2 of each group into a knockout. 12 pairs in 3 groups of 4 = 18 group matches, then 6 qualifiers. 16 pairs in 4 groups of 4 = 24 group matches, then a quarter-final knockout with the top 2.", "2026-11-26")}</div></header>
<section style="padding-top:10px"><div class="wrap gen" id="gs">
<div class="gen-main">
<div class="card" id="gs-setup">
<h2 style="font-size:1.6rem">Set up your groups</h2>
<div class="q"><h3><label for="gs-names">Pairs, one team per line (4 to 32). Put the strongest first: they are spread across the groups.</label></h3><textarea class="search" id="gs-names" rows="8" placeholder="Sam &amp; Priya&#10;Omar &amp; Lucia&#10;Ben &amp; Aisha&#10;..."></textarea><p class="muted" id="gs-count" style="margin:-6px 0 0"></p></div>
{_bq2("gs", "size", "Group size", [("3", "Groups of 3"), ("4", "Groups of 4"), ("5", "Groups of 5")], "4")}
{_bq2("gs", "q", "Who goes through from each group?", [("1", "Winner only"), ("2", "Top 2")], "2")}
{_bq2("gs", "fmt", "Group match format", [("20", "Race to 4 games (about 20 min)"), ("30", "One set (about 30-40 min)"), ("15", "Timed 15 min")], "30")}
<div class="gen-nums"><div class="q"><h3><label for="gs-courts">Courts</label></h3><input class="search" id="gs-courts" type="number" min="1" max="16" value="2" inputmode="numeric"></div>
<div class="q"><h3><label for="gs-draw">Groups</label></h3><select class="search" id="gs-draw"><option value="seed">Seeded (spread the top pairs)</option><option value="rand">Random</option></select></div></div>
<p class="msg" id="gs-err" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:4px"><button class="btn lime" type="button" id="gs-start">Make the groups</button><button class="btn ghost" type="button" id="gs-demo">Fill 12 sample pairs</button></div>
</div>
<div id="gs-live" hidden>
<div class="card gen-bar"><div><span class="pill b" id="gs-sum"></span></div><div class="btns" style="margin:0"><button class="btn ghost sm" type="button" id="gs-copy">Copy groups</button><button class="btn ghost sm" type="button" id="gs-new">New event</button></div></div>
<p class="muted" style="margin:0 0 10px">Type the games each pair won (for example 6 and 3). Leave both empty if the match is not played yet. Tables update as you type.</p>
<div id="gs-groups"></div>
</div>
</div>
<aside class="gen-side"><div class="lb" id="gs-board"><h2>Your event</h2><p>Make the groups to see the number of matches, how long the group stage takes, and who qualifies.</p></div></aside>
</div></section>
{AD.format("gs-mid")}
<section><div class="wrap"><div class="sh"><h2>How many matches in a padel group stage?</h2><p class="muted">In a round robin group every pair plays every other pair once: a group of n pairs has n x (n - 1) / 2 matches.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Pairs</th><th scope="col">Groups</th><th scope="col">Group matches</th><th scope="col">Top 2 go through</th><th scope="col">Knockout matches</th><th scope="col">Total</th></tr></thead><tbody>
<tr><td>8</td><td>2 of 4</td><td>12</td><td>4 (semi-finals)</td><td>3</td><td>15</td></tr>
<tr><td>9</td><td>3 of 3</td><td>9</td><td>6</td><td>5</td><td>14</td></tr>
<tr><td>12</td><td>3 of 4</td><td>18</td><td>6</td><td>5</td><td>23</td></tr>
<tr><td>12</td><td>4 of 3</td><td>12</td><td>8 (quarter-finals)</td><td>7</td><td>19</td></tr>
<tr><td>16</td><td>4 of 4</td><td>24</td><td>8 (quarter-finals)</td><td>7</td><td>31</td></tr>
<tr><td>20</td><td>5 of 4</td><td>30</td><td>10</td><td>9</td><td>39</td></tr>
<tr><td>24</td><td>6 of 4</td><td>36</td><td>12</td><td>11</td><td>47</td></tr>
<tr><td>32</td><td>8 of 4</td><td>48</td><td>16</td><td>15</td><td>63</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Knockout matches are always the number of qualifiers minus one (no 3rd-place match). With 6 or 10 qualifiers the top seeds get a bye in round 1: see the <a href="{href("padel-tournament-bracket.html")}">knockout bracket generator</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How are padel group tables ranked?</h2></div><div class="grid">
<div class="card"><span class="pill b">1st</span><h3 style="margin-top:10px">Matches won</h3><p>Each win counts once. This tool does not give points for a loss, so a pair that wins more matches is always higher.</p></div>
<div class="card"><span class="pill b">2nd</span><h3 style="margin-top:10px">Game difference</h3><p>Games won minus games lost across all group matches. It rewards clear wins and close losses.</p></div>
<div class="card"><span class="pill b">3rd</span><h3 style="margin-top:10px">Games won, then head to head</h3><p>If still level, more games won goes higher. Many organisers then use the result between the two tied pairs. If three pairs are tied, agree a rule before the event starts and tell the players.</p></div>
</div>
<p class="muted" style="margin-top:12px">These are common club rules, not an official FIP rule: every tournament sets its own tie-breaks in its rules. Check yours before you start, and write them on the WhatsApp group.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Groups of 3 or groups of 4?</h2></div><div class="grid">
<div class="card"><h3>Groups of 3</h3><p>Each pair plays 2 group matches. Quick, and good when court time is short. One bad match can knock a pair out, and the same pair sits out every third match.</p></div>
<div class="card"><h3>Groups of 4</h3><p>Each pair plays 3 matches and two matches can be played at the same time, which suits 2 courts per group. The most common choice for club events.</p></div>
<div class="card"><h3>Groups of 5</h3><p>Each pair plays 4 matches: great value for a full day, but 10 matches per group. Use short formats like a race to 4 games.</p></div>
</div>
<p class="muted" style="margin-top:12px">Want no one knocked out at all? Use the <a href="{href("round-robin.html")}">round robin generator</a> for one big league or the <a href="{href("americano.html")}">Americano and Mexicano generator</a> for a social night where partners change. Keep score on court with the <a href="{href("score.html")}">score keeper</a>.</p></div></section>'''
gs_faq = [
    ("How do you run a padel tournament with groups and a knockout?", "Split the pairs into groups of 3 or 4, spread the strongest pairs across the groups, play every match in each group, then send the top 1 or 2 of each group into a knockout bracket."),
    ("How many matches are in a padel group of 4?", "6 matches. Each pair plays the other 3 pairs once. A group of 3 has 3 matches and a group of 5 has 10."),
    ("How are ties broken in a padel group?", "Most clubs use matches won, then game difference, then games won, then the result between the tied pairs. There is no single official rule, so set yours before the event."),
    ("How long does a padel group stage take?", "Count the group matches and divide by your courts. 12 pairs in 3 groups of 4 is 18 matches: on 3 courts that is 6 rounds of about 35 to 45 minutes with one-set matches."),
    ("How many pairs should go through from each group?", "Take enough to fill a knockout of 4, 8 or 16 if you can. With 4 groups, the top 2 make a quarter-final. With 3 groups, the top 2 make 6 qualifiers and the 2 best group winners get a bye."),
]
page("padel-group-stage-generator.html", "Padel Group Stage Generator: Groups + Knockout (Free) | Padel Glass Box",
     "Free padel group stage generator: balanced groups of 3, 4 or 5, every match listed, live tables with game difference, then a knockout for the top pairs.",
     gs, gs_faq, "Group stage generator")

# ---------- 2. DUPR RATING: HOW TO GET ONE + MATCH CHECKER ----------
dp_steps = [
    ("acc", "Make a free account on the DUPR website or app."),
    ("claim", "Check if any of your past matches are already on DUPR and claim them."),
    ("event", "Play one match that is submitted to DUPR: a club league, a ladder or a tournament that uses DUPR."),
    ("self", "Or log a rec game in the app yourself (it counts less than a club or tournament result)."),
    ("ten", "Get to about 10 to 15 recorded matches before you trust the number."),
    ("rel", "Watch your reliability score: play regularly so it stays high."),
]
dp_chk = checklist("dupr", [t for k, t in dp_steps])
dp_in = lambda i, lab, val: f'<div class="q"><h3><label for="dp-{i}">{lab}</label></h3><input class="search" id="dp-{i}" type="number" min="2" max="8" step="0.001" value="{val}" inputmode="decimal" style="margin:0"></div>'
dp = f'''<header class="hero"><div class="wrap"><h1>How to get a DUPR rating (pickleball), and what moves it.</h1>
<p class="lead">DUPR is the rating most pickleball clubs, leagues and tournaments use. Here is how to get rated for free, how the number moves, and a match checker that shows which team DUPR expects to win before you play.</p>
{quick("Make a free DUPR account, then play one match that is submitted to DUPR (a league, ladder or tournament) or log a game yourself in the app: one result is enough to get a rating. Ratings run from 2.000 to 8.000. A DUPR coach can also give you a starting rating without matches. The number moves on how many points you win compared with what was expected, not just on wins.", "2026-11-26")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="dp">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">DUPR match checker</h2><p class="muted" style="margin-top:0">Type each player's DUPR rating. In doubles, DUPR uses the average of the two partners.</p>
{_bq2("dp", "mode", "Match", [("d", "Doubles"), ("s", "Singles")], "d")}
<div class="gen-nums">{dp_in("a1", "You", "3.500")}<div id="dp-a2w">{dp_in("a2", "Your partner", "3.700")}</div></div>
<div class="gen-nums">{dp_in("b1", "Opponent 1", "4.000")}<div id="dp-b2w">{dp_in("b2", "Opponent 2", "3.900")}</div></div>
</div>
<aside class="result" id="dp-out" aria-live="polite"><h2 id="dp-h"></h2><p id="dp-p"></p><p id="dp-t" class="wr-src"></p></aside>
</div>
<p class="muted wrap" style="margin-top:12px">This checker only compares team averages. It is not DUPR's own formula, which is not public in full and also uses how many matches each player has, how recent they are and the type of match.</p></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do I get a DUPR rating? Step by step</h2><p class="muted">Tick the steps as you go. Saved on this device.</p></div>
<div class="card">{dp_chk}</div></div></section>
{AD.format("dp-mid")}
<section><div class="wrap"><div class="sh"><h2>What is a DUPR rating?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Question</th><th scope="col">Answer</th></tr></thead><tbody>
<tr><td>What does DUPR stand for?</td><td>Dynamic Universal Pickleball Rating</td></tr>
<tr><td>Scale</td><td>2.000 to 8.000, shown with 3 decimals (for example 3.616)</td></tr>
<tr><td>Before your first match</td><td>NR (not rated)</td></tr>
<tr><td>How many ratings?</td><td>Separate ratings for singles and doubles, plus an age-group rating for older players</td></tr>
<tr><td>Doubles team rating</td><td>The average of the two partners' ratings</td></tr>
<tr><td>Reliability score</td><td>1 to 100%: higher means the rating is built on more and newer results</td></tr>
<tr><td>Cost</td><td>Rating is free. DUPR+ is an optional paid plan (listed at $19.99 a year when we checked) with extra stats</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Source: DUPR's own pages ("How it works", "How to get a pickleball rating", "How your DUPR rating is calculated", DUPR+ page), checked 26 Nov 2026, plus the Pickleheads guide to DUPR. DUPR can change its rules and prices: check the app for the latest.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How is a DUPR rating calculated?</h2></div><div class="grid">
<div class="card"><h3>Points against expectation</h3><p>Before each match DUPR works out an expected score from everyone's rating. If your team wins more points than expected, your rating goes up, even in a loss. A 3.5 who loses 9-11 to a 4.0 can go up.</p></div>
<div class="card"><h3>A win can drop you</h3><p>If you were expected to win 11-3 but only won 11-8, your rating can go down. Beating much weaker players narrowly does not help.</p></div>
<div class="card"><h3>Match type and recency</h3><p>Club and tournament results count more than a self-posted rec game. Recent matches count more than old ones, and early results move a new rating faster.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do I raise my DUPR rating?</h2></div><div class="grid">
<div class="card"><h3>Win points, not just matches</h3><p>Fight for every point in a match you will lose: a close score against stronger players is what lifts the number.</p></div>
<div class="card"><h3>Play logged matches often</h3><p>Leagues, ladders and tournaments count most. More matches make your rating more stable and keep your reliability score high.</p></div>
<div class="card"><h3>Get better, then play up</h3><p>Lessons do not raise the number on their own, and nor does a new paddle. Better skills, then matches against higher-rated players, do. Our <a href="{href("pickleball-rules.html")}">pickleball rules</a> and <a href="{href("pickleball-score.html")}">score keeper</a> help with the basics.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is there a DUPR for padel?</h2></div>
<div class="card"><p>DUPR is for pickleball. Padel has no single universal rating: booking apps and clubs use their own levels, and pros are ranked by FIP points. To find your padel level, try our <a href="{href("level-calculator.html")}">padel level calculator</a>, see how <a href="{href("padel-rankings.html")}">padel world rankings</a> work, or compare the sports in <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a>.</p></div></div></section>'''
dp_faq = [
    ("How do I get a DUPR rating?", "Make a free DUPR account, then play one match that is submitted to DUPR, such as a league, ladder or tournament, or log a game in the app. One submitted result gives you a rating. A DUPR coach can also assess you and give a starting rating without matches."),
    ("Is DUPR free?", "Yes. Getting and keeping a DUPR rating is free. DUPR+ is an optional paid plan with extra stats and features, listed at $19.99 a year when we checked in November 2026."),
    ("What is a good DUPR rating?", "DUPR runs from 2.000 to 8.000. Professionals are at the top of the scale. Most recreational players sit in the 3s and 4s, so a rating in the 4s is strong club level."),
    ("How many matches do you need for a DUPR rating?", "One submitted match gives you a rating, but DUPR suggests 10 to 15 recorded matches before you fully trust it."),
    ("Why did my DUPR go down after a win?", "DUPR compares the score with what was expected. If you beat lower-rated players by less than expected, your rating can drop even though you won."),
]
page("dupr-rating.html", "How to Get a DUPR Rating: Free Steps + Match Checker | Padel Glass Box",
     "How to get a DUPR rating for pickleball: a free account and one submitted match or a coach rating. The 2.000-8.000 scale, how it moves and a match checker.",
     dp, dp_faq, "DUPR rating")

# ---------- 3. PADEL VS SQUASH ----------
sv_rows = [
    ("Court", "20 x 10 m, open-topped glass and mesh box", "9.75 x 6.4 m closed room (singles)"),
    ("Net", "Yes: 88 cm in the middle, 92 cm at the posts", "No net: you hit the front wall, above the tin (0.48 m high)"),
    ("Walls", "Ball must bounce on your side first, then may hit your walls", "Ball may hit side and back walls, but must reach the front wall before it touches the floor"),
    ("Players", "Almost always doubles", "Mostly singles (doubles is played on a wider court)"),
    ("Racket", "Solid holed racket, no strings", "Light strung racket, up to 68.6 cm long"),
    ("Ball", "Pressurised ball close to a tennis ball", "Small rubber ball that must be warmed up; dot colours show the speed"),
    ("Serve", "Underarm, ball bounced and hit at or below waist, 2 tries", "Overarm or underarm from a service box, one try, onto the front wall between the service line and the out line"),
    ("Scoring", "Tennis scoring (15, 30, 40), sets to 6", "Every rally scores, games to 11 (win by 2), usually best of 5"),
]
sv_tbl = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in sv_rows)
sv_habits = [("back", "I hit hard into the back wall"), ("wrist", "I flick with my wrist"), ("all", "I cover the whole court alone"), ("volley", "I volley everything before the wall"), ("drop", "I love drop shots and boasts"), ("serve", "I serve overarm")]
sv = f'''<header class="hero"><div class="wrap"><h1>Padel vs squash: the differences, and how to switch.</h1>
<p class="lead">Both use walls, so squash players pick up padel fast. But the walls work the other way round, the net changes everything, and padel is played in pairs. Here is the side-by-side, plus a fixer for the squash habits that cost padel points.</p>
{quick("Padel is doubles over a net on a 20 x 10 m glass court, and the ball must bounce on your side before it hits your walls. Squash is mostly singles in a closed 9.75 x 6.4 m room with no net: you hit the ball onto the front wall above the 48 cm tin, and side and back walls can be used first. Padel uses tennis scoring; squash scores every rally, games to 11.", "2026-11-26")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="sh"><h2>Padel and squash compared</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">What</th><th scope="col">Padel</th><th scope="col">Squash</th></tr></thead><tbody>{sv_tbl}</tbody></table></div>
<p class="muted" style="margin-top:12px">Sources: padel from the FIP rules (our <a href="{href("rules.html")}">padel rules</a> and <a href="{href("court-dimensions.html")}">court dimensions</a>); squash from the World Squash Federation (WSF) rules and court specification (our <a href="{href("squash-court-dimensions.html")}">squash court dimensions</a>).</p></div></section>
<section style="padding-top:0"><div class="wrap quiz" id="sv">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Squash player? Fix the habit that costs you padel points</h2><p class="muted" style="margin-top:0">Pick the one that sounds most like you.</p>
{_bq2("sv", "h", "Your squash habit", sv_habits, "back")}</div>
<aside class="result" id="sv-out" aria-live="polite"><h2 id="sv-h"></h2><p id="sv-p"></p><p id="sv-next" class="wr-src"></p></aside>
</div></section>
{AD.format("sv-mid")}
<section><div class="wrap"><div class="sh"><h2>Is padel easier than squash?</h2></div><div class="grid">
<div class="card"><h3>Easier to start</h3><p>Padel's underarm serve, bigger court and slower ball mean rallies start in the first hour. Squash takes longer before you can keep the ball going.</p></div>
<div class="card"><h3>Squash is more intense</h3><p>Squash rallies rarely stop and you cover every ball yourself. Padel has short rallies and rest between points. See the <a href="{href("padel-calories.html")}">padel calories calculator</a>.</p></div>
<div class="card"><h3>Both are hard to master</h3><p>Padel's skill is in the walls, the lob and teamwork with your partner. Squash's skill is in length, width and moving your opponent. Your squash reading of the ball off the glass is a big head start.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Can squash players play padel?</h2></div><div class="grid">
<div class="card"><h3>What carries over</h3><p>Reading a ball off the wall, quick feet, soft hands for drops and a compact swing. Most squash players rally well in their first game.</p></div>
<div class="card"><h3>What to change</h3><p>Let the ball come off your back glass, don't hit it into it. Lock your wrist. Share the court with a partner and move as a pair (<a href="{href("positioning.html")}">where to stand</a>).</p></div>
<div class="card"><h3>First steps</h3><p>Learn the <a href="{href("wall-rules.html")}">wall rules</a>, the <a href="{href("serve-rules.html")}">serve rules</a> and the <a href="{href("padel-grip.html")}">grip</a>, then follow the <a href="{href("padel-beginner-plan.html")}">30-day beginner plan</a>.</p></div>
</div>
<p class="muted" style="margin-top:12px">More comparisons: <a href="{href("padel-vs-racquetball.html")}">padel vs racquetball vs platform tennis</a>, <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a>, <a href="{href("court-sizes-compared.html")}">all court sizes to scale</a>.</p></div></section>'''
sv_faq = [
    ("What is the difference between padel and squash?", "Padel is doubles over a net on a 20 x 10 m glass court and the ball must bounce before it hits your walls. Squash is mostly singles in a closed 9.75 x 6.4 m room with no net, and you hit the ball onto the front wall."),
    ("Is padel easier than squash?", "Most beginners find padel easier to start, thanks to the underarm serve, slower ball and doubles court. Squash is more tiring and takes longer to rally well."),
    ("Is padel good for squash players?", "Yes. Squash players read the ball off the walls well and have quick hands. They mainly need to let the ball come off the back glass, lock the wrist and learn to play as a pair."),
    ("Do you hit the walls in padel like in squash?", "No. In squash you can hit the ball into any wall on its way to the front wall. In padel your shot must land on the other side of the net before it touches their walls. You may play it off your own glass so it rebounds over the net, but you never use the walls to reach a front wall."),
    ("How is squash scored compared with padel?", "Squash scores a point on every rally and games go to 11, win by 2. Padel uses tennis scoring: 15, 30, 40, game, with sets to 6 games."),
]
page("padel-vs-squash.html", "Padel vs Squash: Differences + Squash-to-Padel Fixer | Padel Glass Box",
     "Padel vs squash side by side: court, walls, racket, ball, serve and scoring from the official rules, which is easier, and how squash players switch.",
     sv, sv_faq, "Padel vs squash")

DEMAND_PAGES += ["padel-group-stage-generator.html", "dupr-rating.html", "padel-vs-squash.html"]
exec((ROOT / "demand4.py").read_text())
