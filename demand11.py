# ---------------- DEMAND RUN 14 (27/28 Nov 2026): padel cool-down + stretch timer, padel racket weight calculator ----------------
# Executed from demand10.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards, json).

# ---------- 1. PADEL COOL-DOWN AND STRETCHES (timer) ----------
# step: n = name, ph = phase, t = seconds, d = how
_CD_WALK = {"n": "Easy walk and slow breathing", "ph": "Slow down", "t": 120, "d": "Walk round the court or the car park. Breathe in through your nose, out slowly. Let your heart rate come down before you stretch."}
_CD_STEPS = [
    {"n": "Calf stretch (each leg)", "ph": "Legs", "t": 60, "d": "Hands on the glass, one foot back, heel down, back knee straight. Lean in until you feel the calf. 30 seconds a side, no bouncing."},
    {"n": "Front of thigh (each leg)", "ph": "Legs", "t": 60, "d": "Stand tall, hold the glass, pull one heel towards your bottom. Knees together, hips forward. 30 seconds a side."},
    {"n": "Back of thigh (each leg)", "ph": "Legs", "t": 60, "d": "Heel on the bench or the ground in front, leg straight, toes up. Hinge forward from the hips with a flat back. 30 seconds a side."},
    {"n": "Hip flexor lunge (each side)", "ph": "Hips", "t": 60, "d": "Half-kneel on a towel. Tuck your bottom under and move your hips forward gently until the front of the back hip stretches. 30 seconds a side."},
    {"n": "Inner thigh side lunge", "ph": "Hips", "t": 40, "d": "Wide stance, shift your weight to one bent knee, other leg straight. 20 seconds each way. All those side steps live here."},
    {"n": "Glute stretch (each side)", "ph": "Hips", "t": 60, "d": "Sit on the bench, ankle over the other knee, sit tall and lean forward a little. 30 seconds a side."},
    {"n": "Lower back: knees to chest", "ph": "Back", "t": 40, "d": "Lie on your back (or sit and hug one knee). Pull your knees in gently and breathe out slowly."},
    {"n": "Side reach (each side)", "ph": "Back", "t": 40, "d": "Stand tall, reach one arm up and over to the opposite side. Feel the side of your trunk that turns for every overhead."},
    {"n": "Shoulder across the chest (each arm)", "ph": "Arm", "t": 60, "d": "Bring your hitting arm across your chest and hold it with the other hand above the elbow. 30 seconds a side."},
    {"n": "Forearm: wrist extensors (each arm)", "ph": "Arm", "t": 60, "d": "Arm straight in front, palm down. Gently bend the wrist down with the other hand. This is the muscle behind padel elbow. 30 seconds a side."},
    {"n": "Forearm: wrist flexors (each arm)", "ph": "Arm", "t": 60, "d": "Arm straight, palm up. Gently pull the fingers back towards you. 30 seconds a side."},
    {"n": "Chest opener on the glass", "ph": "Arm", "t": 40, "d": "Forearm flat on the glass at shoulder height, turn your body slowly away until the front of the shoulder stretches."},
]
def _cd_pick(names):
    return [_CD_WALK] + [s for s in _CD_STEPS if s["n"] in names]
CD_JSON = json.dumps({
    "q": [dict(_CD_WALK, t=60)] + [x for x in _CD_STEPS if x["n"] in {"Calf stretch (each leg)", "Front of thigh (each leg)", "Back of thigh (each leg)", "Forearm: wrist extensors (each arm)"}],
    "f": [_CD_WALK] + _CD_STEPS[:4] + _CD_STEPS[5:10],
    "l": [dict(_CD_WALK, t=180)] + _CD_STEPS + [{"n": "Slow breathing to finish", "ph": "Relax", "t": 60, "d": "Sit or lie down, eyes closed if you like. Breathe in for 4, out for 6. Then drink some water."}],
}, ensure_ascii=False)

cd = f'''<header class="hero"><div class="wrap"><h1>Padel cool-down: a stretch timer for after you play.</h1>
<p class="lead">Pick 5, 10 or 15 minutes and press start. The timer walks you through each stretch with a beep at every change, so you can do it on the bench with your phone next to you. Then read why it helps, how long to hold a stretch, and what to do if you are sore the next day.</p>
{quick("A good padel cool-down takes 5 to 15 minutes: 2 minutes of easy walking, then slow, held stretches for the calves, thighs, hips, lower back, shoulder and forearm. Hold each stretch for about 20 to 30 seconds, gently, without bouncing and never into pain. Soreness that peaks a day or two after a hard or first game is normal and usually fades within a few days.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="wu" id="cd">
<div class="wu-stage">
<div class="wu-bar"><div class="seg" id="cd-len" role="group" aria-label="Cool-down length"><button type="button" data-v="q" aria-pressed="true">5 min</button><button type="button" data-v="f" aria-pressed="false">10 min</button><button type="button" data-v="l" aria-pressed="false">15 min</button></div>
<div class="seg" id="cd-snd" role="group" aria-label="Sound"><button type="button" data-v="on" aria-pressed="true">Beeps on</button><button type="button" data-v="off" aria-pressed="false">Off</button></div></div>
<div class="wu-main">
<svg class="wu-ring" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="10"/><circle id="cd-arc" cx="60" cy="60" r="52" fill="none" stroke="#e8f84a" stroke-width="10" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="0" transform="rotate(-90 60 60)"/></svg>
<div class="wu-time"><b id="cd-clock">2:00</b><span id="cd-of">Step 1</span></div>
</div>
<div class="wu-now" aria-live="polite"><span class="pill" id="cd-ph">Slow down</span><h2 id="cd-name">Easy walk and slow breathing</h2><p id="cd-how"></p><p class="wu-next" id="cd-next"></p></div>
<div class="prog"><i id="cd-prog"></i></div>
<div class="wu-ctl"><button class="btn ghost sm" type="button" id="cd-back">Back</button><button class="btn lime" type="button" id="cd-go">Start</button><button class="btn ghost sm" type="button" id="cd-skip">Skip</button></div>
<p class="wu-left" id="cd-left"></p>
</div>
<ol class="wu-list" id="cd-list"></ol>
</div>
<p class="muted" style="margin-top:12px">Tap any step in the list to jump to it. A stretch should feel like a mild pull. Stop if anything hurts, and see a doctor or physio about pain that does not settle.</p></div></section>
<script>window.CD={CD_JSON};</script>
{AD.format("cd-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Should you cool down after padel?</h2></div>
<p>Yes, if you can spare five minutes. Padel is stop-start: sprints, lunges, twists and overheads, often late in the evening. A short walk lets your heart rate and breathing come down slowly, and held stretches after play are the right time to work on the hips, legs and shoulder you used. Padel New Zealand, the national federation, lists a cool-down with stretching as part of its injury-prevention advice, next to a proper warm-up.</p>
<div class="grid" style="margin-top:14px">{_cards([
    ("1. Walk it off", "Two minutes of easy walking. Don't sit down straight after the last point, especially after a long match."),
    ("2. Stretch, slowly", "Held stretches for the muscles padel uses most: calves, front and back of the thigh, hips, lower back, shoulder and forearm."),
    ("3. Drink and refuel", "Drink water, more after a hot or long session, and eat a normal meal with some protein and carbohydrate within a few hours."),
], pill="Step")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which muscles should you stretch after padel?</h2></div>
<div class="tbl"><table><thead><tr><th>Area</th><th>Why it gets tight in padel</th><th>Stretch in the timer</th></tr></thead><tbody>
<tr><td>Calves and Achilles</td><td>Split steps and quick starts on your toes</td><td>Calf stretch on the glass</td></tr>
<tr><td>Front and back of the thigh</td><td>Low volleys, lunges and short sprints</td><td>Thigh stretches</td></tr>
<tr><td>Hips and inner thigh</td><td>Side steps, wide lunges to the corners</td><td>Hip flexor lunge, side lunge, glute stretch</td></tr>
<tr><td>Lower back and sides</td><td>Bending low and twisting for every shot</td><td>Knees to chest, side reach</td></tr>
<tr><td>Shoulder and chest</td><td>Bandejas, smashes and the serve</td><td>Arm across the chest, chest opener</td></tr>
<tr><td>Forearm and wrist</td><td>Gripping the racket for an hour or more</td><td>Wrist extensor and flexor stretches</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long should you hold a stretch?</h2></div>
<p>About <strong>20 to 30 seconds</strong> for each stretch is a good target. The American College of Sports Medicine's guidance for adults is to hold static stretches for 10 to 30 seconds, gently, to the point of mild tightness, not pain. Breathe out as you settle into the stretch, keep still and don't bounce. Once or twice per side is enough after a match.</p>
<div class="grid" style="margin-top:14px">{_cards([
    ("Before play: moving", "Leg swings, lunges with a twist and short sprints. Save long, held stretches for later. Use the warm-up timer."),
    ("After play: held", "Slow, held stretches while your muscles are still warm. This is what the timer on this page does."),
    ("Rest days: either", "A 10-minute stretch on a rest day is fine and can help with stiffness. Keep it gentle."),
], pill="When")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why am I so sore after padel?</h2></div>
<p>New players and anyone back after a break often feel sore one or two days after playing, mostly in the thighs, calves, bottom and shoulder. This is called delayed onset muscle soreness (DOMS). The American College of Sports Medicine describes it as soreness that usually starts 12 to 24 hours after unfamiliar or hard exercise, peaks at about 24 to 72 hours, and fades within about 5 to 7 days. Padel's lunges, low volleys and quick changes of direction are new movements for most people.</p>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>Normal soreness</th><th>See a doctor or physio if</th></tr></thead><tbody>
<tr><td>Dull ache, both sides, in big muscles</td><td>Sharp pain in one spot, or pain that started with a pop or a sudden pull</td></tr>
<tr><td>Worst on day 1 or 2, then better each day</td><td>Pain that gets worse or still hurts after a week</td></tr>
<tr><td>Eases as you walk and warm up</td><td>Swelling, bruising, or you can't put weight on the leg</td></tr>
<tr><td>Elbow or forearm a bit tired</td><td>Outer elbow pain that keeps coming back: read <a href="{href("padel-elbow.html")}">padel elbow</a></td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Gentle movement (a walk, an easy bike ride, the timer above) usually helps soreness more than full rest. Build up slowly: one or two games a week at first. More on common problems: <a href="{href("padel-injuries.html")}">padel injuries and prevention</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Warm up first</h3><p>The other half of the routine: the 10 or 15 minute <a href="{href("warm-up.html")}">padel warm-up timer</a>.</p></div>
<div class="card"><h3>Move better</h3><p>Less lunging, more balance: the <a href="{href("padel-footwork.html")}">footwork and split-step trainer</a>.</p></div>
<div class="card"><h3>Plan your week</h3><p>Fit games, drills and rest days together with the <a href="{href("padel-training-plan.html")}">training plan generator</a>.</p></div>
</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: Padel New Zealand "Injury prevention in padel" (a 10 to 15 minute cool-down after play; static stretching is best after play, when muscles are warm), American College of Sports Medicine guidance on flexibility (hold static stretches 10 to 30 seconds to mild tightness) and its information sheet on delayed onset muscle soreness (starts 12 to 24 h, peaks 24 to 72 h, fades in 5 to 7 days). The stretches are common, simple ones written in our own words; this page is general information, not medical advice.</p></div></section>'''
cd_faq = [
    ("How long should a padel cool-down be?", "About 5 to 15 minutes: 2 minutes of easy walking, then held stretches for the legs, hips, lower back, shoulder and forearm."),
    ("Should you stretch before or after padel?", "Do moving stretches (leg swings, lunges, twists) before you play, and slow, held stretches after you play, when your muscles are warm."),
    ("How long should I hold each stretch?", "About 20 to 30 seconds. Sports-medicine guidance for adults is 10 to 30 seconds, to mild tightness, not pain, without bouncing."),
    ("Is it normal to be sore after playing padel?", "Yes, especially after your first games or a long break. Muscle soreness usually peaks one to two days after playing and fades within a few days. Sharp, one-sided or worsening pain is different: get it checked."),
    ("What muscles does padel work?", "Mostly the calves, thighs, bottom and hips from lunges and side steps, the trunk from twisting, and the shoulder and forearm of your hitting arm."),
    ("What should I do the day after padel if I am sore?", "Keep moving gently: a walk, an easy bike ride or a 10-minute stretch. Drink water, sleep well, and play lighter until it eases."),
]
page("padel-cool-down.html", "Padel Cool-Down and Stretches: Free 5-15 Min Timer",
     "Free padel cool-down timer: 5, 10 or 15 minutes of stretches after you play, what to stretch, how long to hold, and why you're sore after padel.",
     cd, cd_faq, "Padel cool-down")

# ---------- 2. PADEL RACKET WEIGHT CALCULATOR ----------
rw = f'''<header class="hero"><div class="wrap"><h1>Padel racket weight calculator: what weight should you get?</h1>
<p class="lead">Answer six quick questions about your level, strength, arm and style. The calculator gives a weight range in grams to look for on the product page, plus the balance and feel that go with it.</p>
{quick("Most adult padel rackets weigh 345 to 385 g. As a rough guide: beginners and players with sore elbows or shoulders do best around 345 to 360 g, most improving players around 355 to 370 g, and strong advanced players who hit hard around 360 to 375 g or more. Juniors need lighter rackets. Weight on the label can be a few grams out, and an overgrip or protector tape adds a little.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card">
{_bq2("rw", "lvl", "How long have you played padel?", [("new", "New, under 6 months"), ("mid", "6 months to 2 years"), ("adv", "2 years or more, competing")], "new")}
{_bq2("rw", "str", "How strong is your hitting arm?", [("light", "Not very strong"), ("avg", "Average"), ("strong", "Strong, gym or racket-sport arm")], "avg")}
{_bq2("rw", "arm", "Any elbow, wrist or shoulder pain?", [("no", "No"), ("some", "Sometimes"), ("yes", "Yes, now or recently")], "no")}
{_bq2("rw", "sty", "How do you like to play?", [("ctrl", "Control and placement"), ("all", "A bit of both"), ("pow", "Power and smashes")], "all")}
{_bq2("rw", "age", "Age group", [("jr", "Under 14"), ("ad", "14 to 54"), ("55", "55 or over")], "ad")}
{_bq2("rw", "freq", "How often do you play?", [("1", "Once a week or less"), ("2", "2 to 3 times a week"), ("4", "4 or more times a week")], "1")}
</div>
<aside class="result" id="rw-out" aria-live="polite"><span class="pill b" id="rw-pill">Your weight</span><h2 id="rw-h" style="margin-top:10px">345 to 360 g</h2><p id="rw-p"></p><dl class="spec" id="rw-spec"></dl><p id="rw-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="rw-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">General guidance, not a medical or brand recommendation. If you can, hold or borrow a racket in your range before you buy.</p></div></section>
{AD.format("rw-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What weight should a padel racket be?</h2></div>
<div class="tbl"><table><thead><tr><th>Player</th><th>Weight to look for</th><th>Why</th></tr></thead><tbody>
<tr><td>Beginner adult</td><td>About 345 to 360 g</td><td>Easy to swing, quick at the net, kind to the arm while technique is new</td></tr>
<tr><td>Improving club player</td><td>About 355 to 370 g</td><td>More stability and depth on lobs and overheads</td></tr>
<tr><td>Strong advanced player</td><td>About 360 to 375 g+</td><td>More power and less twisting on hard hits, if the arm can handle it</td></tr>
<tr><td>Sore elbow or shoulder</td><td>Light end, about 345 to 360 g</td><td>Less load per swing; pair with a low balance and soft feel</td></tr>
<tr><td>Junior, under 14</td><td>Lighter junior rackets</td><td>Weight by height and age: see the junior racket finder</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">These ranges are what most maker and shop sizing guides suggest. Brands label weight differently: some print one number, others a range such as 360 to 375 g.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is a heavier or lighter padel racket better?</h2></div><div class="grid">{_cards([
    ("Lighter", "Faster to move at the net and in quick exchanges, easier on the arm and easier to learn with. Less power from the racket itself, and it can twist on off-centre hits."),
    ("Heavier", "More power and stability on smashes, deep lobs and hard volleys. Slower to swing and more tiring, so late hits and arm strain are more likely if you are not ready for it."),
    ("Weight vs balance", "A heavy, head-light racket can feel lighter than a lighter head-heavy one. Balance decides how heavy the head feels. Check both numbers."),
], pill="Feel")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you know if your padel racket is too heavy?</h2></div>
<div class="tbl"><table><thead><tr><th>Sign</th><th>What it usually means</th></tr></thead><tbody>
<tr><td>You are often late on fast volleys at the net</td><td>Too heavy, or too head-heavy, for your hand speed</td></tr>
<tr><td>Your arm or shoulder is tired by the second set</td><td>Too heavy for how long and how often you play</td></tr>
<tr><td>Outer elbow pain after playing</td><td>Try lighter and lower balance, and look at grip tension: <a href="{href("padel-elbow.html")}">padel elbow check</a></td></tr>
<tr><td>Smashes and lobs feel weak and the racket twists</td><td>Possibly too light for how hard you hit</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Small changes add up: an overgrip and protector tape each add a few grams, mostly at the handle or the frame. Lead tape on the frame adds weight and moves the balance towards the head, so add it a little at a time.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Check the balance</h3><p>Decode the balance number and measure it at home: <a href="{href("racket-balance.html")}">racket weight and balance explained</a>.</p></div>
<div class="card"><h3>Pick the shape</h3><p>Round, teardrop or diamond in six questions: the <a href="{href("racket-finder.html")}">padel racket finder</a>.</p></div>
<div class="card"><h3>Two rackets in mind?</h3><p>Put them side by side: <a href="{href("compare-padel-rackets.html")}">compare two padel rackets</a>. Buying for a child? Use the <a href="{href("padel-racket-for-kids.html")}">junior racket finder</a>. Buying for a woman player? See <a href="{href("padel-racket-for-women.html")}">padel racket for women</a>. Control or power? Take the <a href="{href("control-vs-power-padel-racket.html")}">7-question test</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop by weight</h3><p>Check the weight and balance on each product page against your range above.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets (often lighter, low balance)</a></li><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond rackets (head-heavy)</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">How we set the ranges, checked 27 Nov 2026: the typical adult range (about 345 to 385 g) and the light-for-beginners, heavier-for-strong-players pattern appear across maker and shop sizing guides, including HEAD "How to choose a padel racquet", Tennis Warehouse "How to choose a padel racket", TennisOnly "Padel racket guide: weight", Zona de Padel "How to choose the weight of a padel racket" and Justpadel "What weight of padel racket should you choose?". The calculator's adjustments are our own simple rules of thumb, not a brand's sizing chart.</p></div></section>'''
rw_faq = [
    ("What weight padel racket should I get?", "Most adults do well between 345 and 375 g. Beginners and players with sore arms should stay around 345 to 360 g; strong, experienced players who hit hard can go to 365 to 375 g or more."),
    ("What is a good padel racket weight for beginners?", "About 345 to 360 g. A lighter racket is easier to swing, quicker at the net and kinder to your elbow while you learn."),
    ("Is 370 g heavy for a padel racket?", "It is at the heavier end of normal. Many advanced players use 365 to 375 g, but for beginners or players with elbow pain it is usually too heavy."),
    ("Are heavier padel rackets more powerful?", "Yes, a heavier racket gives more power and stability if you can swing it at the same speed. If it makes you late or tired, you lose that advantage."),
    ("Does an overgrip change the weight of a padel racket?", "A little. An overgrip and protector tape each add a few grams. Lead tape adds more and also changes the balance."),
    ("What weight padel racket for women?", "Pick by strength and arm history, not gender. Many players start around 345 to 360 g; strong, experienced players can go heavier."),
]
page("padel-racket-weight.html", "Padel Racket Weight Calculator: What Weight Should I Get?",
     "What weight padel racket should you get? Free calculator by level, strength, arm and style, with ranges for beginners, advanced players and sore elbows.",
     rw, rw_faq, "Racket weight")

DEMAND_PAGES += ["padel-cool-down.html", "padel-racket-weight.html"]
exec((ROOT / "demand12.py").read_text())
