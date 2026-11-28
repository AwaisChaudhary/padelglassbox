# ---------------- DEMAND RUN 20 (28 Nov 2026): padel backhand + fault fixer, padel team generator, benefits of padel + weekly activity check ----------------
# Executed from demand17.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards).

# ---------- 1. PADEL BACKHAND ----------
pb = f'''<header class="hero"><div class="wrap"><h1>How to hit a padel backhand (one or two hands)</h1>
<p class="lead">The backhand is where most padel players lose points, because opponents aim at it. Learn the four steps, decide between one and two hands, and use the fault fixer to find out why your backhand floats, hits the net or comes late.</p>
{quick("To hit a padel backhand, hold a continental grip, turn your shoulders sideways early with your free hand on the throat of the racket, and step across with your front foot. Keep the backswing short, meet the ball slightly in front of your front foot with a firm wrist and a slightly closed face, and finish towards your target. Most padel players hit one-handed because it reaches further and works better off the glass; two hands give more stability on balls close to the body.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Backhand fault fixer</h2><p class="muted" style="margin-top:0">Pick what goes wrong, where, and how you hit it now.</p>
{_bq2("pbh", "prob", "What goes wrong most?", [("float", "It floats up, easy volley for them"), ("net", "Into the net"), ("late", "I am late or cramped"), ("glass", "I miss it off the back glass"), ("weak", "No depth or pace"), ("arm", "Sore elbow or wrist")], "float")}
{_bq2("pbh", "where", "Where are you when it happens?", [("back", "Back of court, off the bounce"), ("glass", "After the back glass"), ("net", "At the net (volley)")], "back")}
{_bq2("pbh", "hands", "How do you hit it now?", [("one", "One hand"), ("two", "Two hands"), ("mix", "Mix or not sure")], "one")}
{_bq2("pbh", "bg", "Your background", [("new", "New to racket sports"), ("t2", "Tennis, two-handed backhand"), ("t1", "Tennis, one-handed backhand")], "new")}
</div>
<aside class="result" id="pbh-out" aria-live="polite"><span class="pill b">Your fix</span><h2 id="pbh-h" style="margin-top:10px">It floats up</h2>
<p id="pbh-p"></p><h3 style="margin-top:14px;font-size:1rem">Try this, in order</h3><ol id="pbh-fix" class="tp-hab"></ol><dl class="spec" id="pbh-spec"></dl><p id="pbh-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="pbh-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">The fixes follow the coaching sources at the bottom of the page. The matching of problems to fixes is our own.</p></div></section>
{AD.format("pbh-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you hit a backhand in padel, step by step?</h2></div><div class="grid">{_cards([
    ("Continental grip, free hand on the throat", "Use the same continental grip as for your forehand and volleys, so you never change grip in a fast rally. Keep your free hand on the throat of the racket as you turn: it helps you turn the shoulders and keeps the backswing short."),
    ("Turn sideways early", "As soon as you see the ball coming to your backhand, turn your shoulders and step across with your front foot (the right foot for a right-hander). Bend your knees and stay low."),
    ("Short backswing, contact in front", "Take the racket back no higher than your shoulder. Meet the ball a little in front of your front foot, at the side of your body, with a firm wrist."),
    ("Slightly closed face, finish to target", "Keep the face slightly closed so the ball stays low over the net, then finish smoothly towards your target. Do not slow the racket down at contact."),
], pill="Step")}</div>
<p style="margin-top:12px">Grip help: <a href="{href("padel-grip.html")}">how to hold a padel racket</a>. Forehand side: <a href="{href("padel-forehand.html")}">how to hit a padel forehand</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>One-handed or two-handed backhand in padel?</h2><p class="muted">Most padel players hit one-handed. Two hands is allowed and some good players use it.</p></div>
<div class="tbl"><table><thead><tr><th></th><th>One-handed</th><th>Two-handed</th></tr></thead><tbody>
<tr><td>Reach</td><td>More: you can stretch for wide balls</td><td>Less: you need to move closer to the ball</td></tr>
<tr><td>Off the back glass</td><td>Easier, often with slice</td><td>Harder when the ball comes off the glass close to you</td></tr>
<tr><td>At the net</td><td>Natural for volleys and blocks</td><td>Slower for fast volleys</td></tr>
<tr><td>Balls at body height</td><td>Harder to control with pace</td><td>More stable, more power</td></tr>
<tr><td>Contact point</td><td>Further in front</td><td>A little further back, closer to the body</td></tr>
<tr><td>Good for</td><td>Most players, especially from the start</td><td>Tennis players with a two-handed backhand, players who lack wrist strength</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">A common mix: two hands when you have time and the ball is close, one hand when you have to reach or play off the back wall. Volleys and blocks at the net are almost always one-handed.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you play a backhand off the back glass?</h2></div><div class="grid">{_cards([
    ("Read the bounce", "If the ball bounces after the service line, let it hit the back glass. Follow it all the way to the wall."),
    ("Turn early, move away", "Turn sideways as soon as it passes you and take small steps towards the net, so the ball comes back to the side of your body."),
    ("Let it drop to waist height", "Do not hit it on the way up. Wait until it drops to about waist height, then play a short, controlled swing."),
    ("Aim deep and safe", "Play it back deep or cross-court, or lob if they are at the net. The glass ball is about getting back into the point, not winning it."),
], pill="Step")}</div>
<p style="margin-top:12px">Full guide with a decision table: <a href="{href("padel-back-glass.html")}">playing off the back glass</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What are the most common padel backhand mistakes?</h2></div><div class="grid">{_cards([
    ("Late contact", "The racket goes back only when the ball arrives, so you hit it next to or behind your body. Turn as soon as you know it is a backhand."),
    ("Open face, ball floats", "A face tilted up sends the ball high, which gives the net pair an easy volley or smash. Close the face a little."),
    ("Reaching instead of moving", "Stretching with the arm, not the feet, kills control and strains the elbow. Take small steps so the ball is at the side of you."),
    ("Slowing down at contact", "Fear of hitting long makes players stop the racket at contact. Keep a smooth, full but short swing and control the ball with the face."),
], pill="Mistake")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which drills improve a padel backhand?</h2></div><div class="grid">{_cards([
    ("Cross-court backhand rally", "Two players on the backhand diagonal rally cross-court backhands only. Count how many you can keep low and deep in a row."),
    ("Wall forehand-backhand", "Against a wall or the side glass, alternate forehand and backhand. It trains the early turn and the grip you keep for both."),
    ("Glass rebound feeds", "A partner feeds balls into your back glass on the backhand side. Turn, move, let it drop, play it deep. 10 balls, then swap."),
], pill="Drill")}</div>
<p style="margin-top:12px">Plan sessions with the <a href="{href("drills.html")}">drills planner</a>, practise alone with the <a href="{href("padel-solo-practice.html")}">solo practice timer</a>, or see the <a href="{href("padel-volley.html")}">volley</a>, <a href="{href("padel-lob.html")}">lob</a> and <a href="{href("bandeja-vs-vibora.html")}">bandeja</a> guides for the other backhand-side shots.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: Padel Browser "How to hit a backhand in padel" (19 Jun 2026: continental grip, early shoulder turn, free hand on the throat, short backswing, contact slightly in front, firm wrist and slightly closed face, one- vs two-handed reach and stability, glass backhand, common mistakes, drills); LTA Padel "How to play padel forehands and backhands" (early preparation, short backswing, contact in front, face to target); The Padel School "How to hit a good padel backhand?"; Nox "How to do the backhand in padel". Written in our own words.</p></div></section>'''
pb_faq = [
    ("How do you hit a backhand in padel?", "Use a continental grip, turn sideways early with your free hand on the racket throat, step across with the front foot, keep the backswing short and meet the ball slightly in front of you with a firm wrist. Finish towards your target."),
    ("Should I use a one-handed or two-handed backhand in padel?", "Most players use one hand because it reaches further and is easier off the glass and at the net. Two hands give more stability on balls close to the body, so some tennis players keep it for those."),
    ("What grip do you use for a padel backhand?", "The continental grip, the same as for the forehand, volleys and serve. That way you never need to change grip in a fast rally."),
    ("Why does my padel backhand float?", "Usually the racket face is open (tilted up) or you hit late, under the ball. Turn earlier, meet the ball in front and close the face a little."),
    ("How do you hit a backhand off the back glass?", "Let the ball hit the glass, turn sideways early, move with it towards the net and wait until it drops to about waist height. Then play a short, controlled swing deep or cross-court."),
    ("Is a two-handed backhand allowed in padel?", "Yes. The rules do not limit how many hands you use. It is just less common because padel rewards reach and quick volleys."),
]
page("padel-backhand.html", "Padel Backhand: How to Hit It, One vs Two Hands + Fault Fixer",
     "How to hit a padel backhand in 4 steps, one-handed vs two-handed, how to play it off the back glass, common mistakes, drills and a free backhand fault fixer.",
     pb, pb_faq, "Padel backhand")

# ---------- 2. PADEL TEAM GENERATOR ----------
tg = f'''<header class="hero"><div class="wrap"><h1>Padel team generator: fair doubles pairs in one tap</h1>
<p class="lead">Type in your players and, if you like, a level for each. Get balanced pairs, the match on each court and who sits out. Re-draw as often as you want. Free, no sign-up, names saved on this device.</p>
{quick("For fair padel doubles, sort the players by level and pair the strongest with the weakest, the second strongest with the second weakest, and so on. Then put the two pairs with the closest totals on the same court. This generator does that for you, with a small random shuffle so the pairs change each draw. Without levels it makes a fully random draw.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap gen">
<div class="gen-main">
<div class="card" id="tg-setup">
<h2 style="font-size:1.6rem">Your players</h2>
<div class="q"><h3>How to draw</h3><div class="opts" data-tg="mode" role="group" aria-label="How to draw"><button class="opt" type="button" data-v="bal" aria-pressed="true">Balanced by level</button><button class="opt" type="button" data-v="rnd" aria-pressed="false">Fully random</button></div></div>
<div class="q"><h3><label for="tg-names">One player per line. Add a level after a comma if you want (1 to 7, like "Sam, 4")</label></h3><textarea class="search" id="tg-names" rows="9" placeholder="Sam, 4&#10;Priya, 3.5&#10;Omar, 2&#10;Lucia, 5&#10;..."></textarea><p class="muted" id="tg-count" style="margin:-6px 0 0"></p></div>
<div class="q"><h3><label for="tg-courts">Courts available</label></h3><input class="search" id="tg-courts" type="number" min="1" max="12" value="2" inputmode="numeric" style="max-width:120px"></div>
<p class="msg" id="tg-err" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:4px"><button class="btn lime" type="button" id="tg-go">Make the teams</button><button class="btn ghost" type="button" id="tg-demo">Fill 8 sample players</button></div>
</div>
</div>
<aside class="gen-side"><div class="lb" id="tg-out" aria-live="polite"><h2>Teams</h2><p>Add at least 4 players and tap Make the teams.</p></div>
<div class="btns" style="margin-top:10px"><button class="btn ghost sm" type="button" id="tg-again">Draw again</button><button class="btn ghost sm" type="button" id="tg-copy">Copy for WhatsApp</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">Players without a level get the average of the others (or 3 if nobody has one). Levels are only used to balance; they are never shown in the copied text. Not sure of a level? Use the <a href="{href("level-calculator.html")}">padel level calculator</a>.</p></div></section>
{AD.format("tg-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you make fair padel teams?</h2></div><div class="grid">{_cards([
    ("Balance pairs, not players", "In padel the unit is the pair. Two strong players together beat everyone; one strong and one weaker player make a fair team."),
    ("Strongest with weakest", "Sort by level and pair 1st with last, 2nd with second last. Each pair ends up with a similar total. This is what the generator does."),
    ("Similar pairs on one court", "Put the two pairs with the closest totals on the same court, so every match is close. Court 1 gets the strongest two pairs."),
    ("Add a little chance", "Pure balance gives the same pairs every week. A small random shuffle between players of a similar level keeps it fresh but fair."),
], pill="Rule")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which padel format should you use after the draw?</h2></div>
<div class="tbl"><table><thead><tr><th>You want</th><th>Use</th></tr></thead><tbody>
<tr><td>Same pairs all evening, everyone plays everyone</td><td><a href="{href("round-robin.html")}">Round robin generator</a></td></tr>
<tr><td>New partner every round, points add up</td><td><a href="{href("americano.html")}">Americano / Mexicano</a></td></tr>
<tr><td>Winners move up a court, losers move down</td><td><a href="{href("king-of-the-court.html")}">King of the Court</a></td></tr>
<tr><td>Groups first, then knockouts</td><td><a href="{href("padel-group-stage-generator.html")}">Group stage generator</a></td></tr>
<tr><td>A single knockout</td><td><a href="{href("padel-tournament-bracket.html")}">Tournament bracket</a></td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What if the number of players is not a multiple of 4?</h2></div>
<p>Each court needs 4 players. With 5, 6 or 7 players on one court, the extra players sit out and swap in after each set or each 15 minutes. The generator lists who sits out first; press Draw again for the next round so different people rest. With 6 or 7 players an <a href="{href("americano.html")}">Americano</a> spreads the rests automatically. If you have more players than court places, the extra players also sit out.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Method: greedy balancing by level (sort, then pair strongest with weakest), the same idea fair-team guides describe as level-balanced random draws, for example visu.network "How to make fair random teams" (20 Oct 2026), which also advises balancing pairs rather than individuals in padel. The 1 to 7 level scale matches our <a href="{href("level-calculator.html")}">level calculator</a>. The tool is our own code.</p></div></section>'''
tg_faq = [
    ("How do you make balanced teams in padel?", "Sort players by level, then pair the strongest with the weakest, the second strongest with the second weakest, and so on. Put pairs with similar totals on the same court."),
    ("Can I make random padel teams without levels?", "Yes. Choose Fully random, or just leave the levels out, and the generator shuffles everyone into pairs and courts."),
    ("What do I do with 5, 6 or 7 padel players?", "Four play and the others sit out, then swap after each set or a fixed time. The generator lists who rests first; draw again for the next round."),
    ("What level scale should I use?", "Any scale works if you use it for everyone. We use 1 to 7, the same as many club apps and our level calculator. Half levels like 3.5 are fine."),
    ("Does the generator save my players?", "Yes, the list is saved on this device only, so you can reuse it next week. Nothing is sent to us."),
]
page("padel-team-generator.html", "Padel Team Generator: Balanced or Random Doubles Pairs",
     "Free padel team generator: type your players and levels, get fair doubles pairs, the match on each court and who sits out. Random or balanced, copy to WhatsApp.",
     tg, tg_faq, "Team generator")

# ---------- 3. BENEFITS OF PADEL ----------
bn = f'''<header class="hero"><div class="wrap"><h1>Benefits of padel: what it does for your body and mind</h1>
<p class="lead">What the evidence says about padel for fitness, heart, strength, mood and social life, where the research is still thin, and a quick check of how much your weekly padel counts towards the health guideline.</p>
{quick("Padel is a moderate-to-vigorous workout: LTA Padel says most data puts players at about 70 to 85% of their maximum heart rate. Studies link it with better aerobic fitness, sprint speed, grip strength, agility, coordination and mood, and it is easier to start than tennis. Most research is still small and early. Two or three 60 to 90 minute games a week meets the WHO guideline of at least 150 minutes of moderate activity.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Does my padel meet the guideline?</h2><p class="muted" style="margin-top:0">The WHO advises adults to do at least 150 minutes of moderate activity a week (or 75 minutes of vigorous activity), plus muscle-strengthening on 2 days.</p>
{_bq2("bn", "n", "Padel sessions a week", [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4 or more")], "2")}
{_bq2("bn", "len", "Length of a session", [("60", "60 min"), ("90", "90 min"), ("120", "2 hours")], "90")}
{_bq2("bn", "int", "How hard do you play?", [("easy", "Social, lots of standing"), ("mod", "Steady rallies"), ("hard", "Competitive, out of breath")], "mod")}
{_bq2("bn", "str", "Strength training a week", [("0", "None"), ("1", "1 day"), ("2", "2 days or more")], "0")}
</div>
<aside class="result" id="bn-out" aria-live="polite"><span class="pill b">Your week</span><h2 id="bn-h" style="margin-top:10px">Guideline met</h2>
<div class="cp-scale" aria-hidden="true"><i id="bn-dot"></i></div><div class="cp-lab"><span>0</span><span>150 min</span><span>300 min</span></div>
<p id="bn-p"></p><dl class="spec" id="bn-spec"></dl><p id="bn-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="bn-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">Active time is our own estimate: in a social game you rest between points and change ends, so we count 60% of court time for social play, 75% for steady rallies and 85% for competitive play. Competitive play is counted as vigorous (each minute counts double), as the WHO guideline allows. To stay on the safe side we count steady rallies as moderate, although by MET values a normal club match is often vigorous (see the calories page). This is general information, not medical advice.</p></div></section>
{AD.format("bn-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What are the health benefits of padel?</h2></div><div class="grid">{_cards([
    ("Heart and fitness", "Players spend much of a game at about 70 to 85% of their maximum heart rate (LTA Padel). That is aerobic training, done in short bursts with rests, which many people find easier to keep up than running."),
    ("Speed, agility and balance", "Constant short sprints, stops and turns train agility, coordination and balance. Studies reviewed by National Geographic link padel with gains in sprint speed."),
    ("Strength", "Research suggests gains in grip strength and lower-back (lumbar) strength. Padel alone is not full strength training, so add 2 days of exercises: see the <a href='"+href("padel-workout.html")+"'>padel workout builder</a>."),
    ("Mood and stress", "LTA Padel reports reduced stress and better mood from regular play. Early studies also look at brain health markers, but this research is new."),
    ("Thinking and decisions", "Fast rallies make you read the ball, the walls and your partner every second. LTA Padel's coach says there is good evidence across racket sports for decision-making benefits."),
    ("Social and easy to start", "It is always doubles, the court is small and the serve is underarm, so beginners can rally in their first session. That is why people keep coming back."),
], pill="Benefit")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is padel good exercise compared with tennis and the gym?</h2></div>
<div class="tbl"><table><thead><tr><th></th><th>Padel</th><th>Tennis</th><th>Gym session</th></tr></thead><tbody>
<tr><td>How hard</td><td>Moderate to vigorous, in bursts</td><td>Moderate to vigorous, more running for beginners</td><td>Whatever you choose</td></tr>
<tr><td>Easy to start</td><td>Very: rallies in session one</td><td>Harder: serve and long court</td><td>Easy, but less fun for many</td></tr>
<tr><td>Strength</td><td>Grip, legs, core, some lower back</td><td>Similar</td><td>Best for strength</td></tr>
<tr><td>Social</td><td>Always 4 players</td><td>Singles or doubles</td><td>Often alone</td></tr>
<tr><td>Injury watch</td><td>Elbow, calf, ankle, shoulder</td><td>Elbow, shoulder, knee</td><td>Depends on the exercise</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">National Geographic quotes a University of Zaragoza researcher saying padel is less demanding than tennis at beginner and intermediate level and the intensity is easy to control. Calories by weight and time: <a href="{href("padel-calories.html")}">padel calories calculator</a>. Full sport comparison: <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is padel good for older players and people over 50?</h2></div>
<p>Yes, for most people, because you can control the intensity, the court is small and the game is social. LTA Padel notes that about 42% of UK adults over 55 are estimated to be physically inactive, against 29% of all adults, and points to club programmes built for older and returning players. Start with social games, warm up every time and build up slowly. If you have a heart, joint or other health condition, check with your doctor first.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What are the risks, and what does the research not show yet?</h2></div><div class="grid">{_cards([
    ("Injuries happen, but are not common", "A systematic review cited by National Geographic found about 3 injuries per 1,000 hours of padel, with elbow problems more common than in many sports. See <a href='"+href("padel-injuries.html")+"'>padel injuries and prevention</a> and the <a href='"+href("padel-elbow.html")+"'>padel elbow check</a>."),
    ("The research is young", "Most padel studies are small and use similar groups of players. Mental health and hormone findings especially are early, so treat big claims with care."),
    ("It does not replace strength work", "Padel trains fitness and agility well, but the guideline still asks for 2 days of muscle-strengthening a week."),
], pill="Note")}</div>
<p style="margin-top:12px">Getting started: <a href="{href("beginners.html")}">padel for beginners</a>, the <a href="{href("padel-beginner-plan.html")}">30-day beginner plan</a>, a <a href="{href("warm-up.html")}">warm-up timer</a> and the <a href="{href("padel-cool-down.html")}">cool-down stretch timer</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: LTA Padel "Why padel is so good for your health" (2 Apr 2026: 70 to 85% max heart rate from LTA's lead physical preparation coach; aerobic fitness, agility, coordination, balance, mood and stress, decision-making; 42% of UK over-55s vs 29% of adults inactive); National Geographic "Padel exercise health benefits" (3 Feb 2026: sprint speed, grip and lumbar strength, early brain-health research, less demanding than tennis for beginners, about 3 injuries per 1,000 hours from a systematic review, research still preliminary with small samples); World Health Organization physical activity guidelines for adults (150 to 300 minutes moderate or 75 to 150 minutes vigorous a week, muscle-strengthening on 2 or more days). The weekly check is our own estimate. Written in our own words.</p></div></section>'''
bn_faq = [
    ("What are the benefits of playing padel?", "Better aerobic fitness, agility, coordination, balance and grip strength, plus mood and social benefits. It is also easy to start, so people tend to keep playing."),
    ("Is padel a good workout?", "Yes. Players spend much of a game at about 70 to 85% of their maximum heart rate, which is moderate to vigorous exercise, done in short bursts."),
    ("Is padel better exercise than tennis?", "Not better, but easier to start. At beginner and intermediate level it is usually less demanding than tennis, and the intensity is easy to control."),
    ("How often should I play padel to stay fit?", "Two or three 60 to 90 minute games a week usually meets the WHO guideline of 150 minutes of moderate activity. Add 2 days of strength exercises."),
    ("Is padel good for weight loss?", "It burns a fair amount of energy and is easy to do often, which helps. Check your number with our padel calories calculator; diet matters too."),
    ("Is padel safe for older people?", "For most people, yes, because you can control the pace. Warm up, start with social games and check with your doctor if you have a health condition."),
]
page("padel-benefits.html", "Benefits of Padel: Health, Fitness and Mood (What Studies Say)",
     "The benefits of padel for fitness, heart, strength, mood and social life, what the research does not show yet, and a free check of your weekly activity.",
     bn, bn_faq, "Benefits of padel")

DEMAND_PAGES += ["padel-backhand.html", "padel-team-generator.html", "padel-benefits.html"]

exec((ROOT / "demand19.py").read_text())
