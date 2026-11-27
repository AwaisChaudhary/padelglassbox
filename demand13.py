# ---------------- DEMAND RUN 16 (28 Nov 2026): solo padel practice planner + timer, padel strength workout builder + circuit timer ----------------
# Executed from demand12.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards, json).

def _seg(px, name, label, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{v}" aria-pressed="{"true" if v == on else "false"}">{e(t)}</button>' for v, t in opts)
    return f'<div class="q"><h3>{e(label)}</h3><div class="opts" id="{px}-{name}" role="group" aria-label="{e(label)}">{b}</div></div>'

def _timer_block(px, first_name, first_ph):
    return f'''<div class="wu" id="{px}">
<div class="wu-stage">
<div class="wu-bar"><span class="pill" id="{px}-sum" style="align-self:center">Your session</span>
<div class="seg" id="{px}-snd" role="group" aria-label="Sound"><button type="button" data-v="on" aria-pressed="true">Beeps on</button><button type="button" data-v="off" aria-pressed="false">Off</button></div></div>
<div class="wu-main">
<svg class="wu-ring" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="10"/><circle id="{px}-arc" cx="60" cy="60" r="52" fill="none" stroke="#e8f84a" stroke-width="10" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="0" transform="rotate(-90 60 60)"/></svg>
<div class="wu-time"><b id="{px}-clock">2:00</b><span id="{px}-of">Step 1</span></div>
</div>
<div class="wu-now" aria-live="polite"><span class="pill" id="{px}-ph">{e(first_ph)}</span><h2 id="{px}-name">{e(first_name)}</h2><p id="{px}-how"></p><p class="wu-next" id="{px}-next"></p></div>
<div class="prog"><i id="{px}-prog"></i></div>
<div class="wu-ctl"><button class="btn ghost sm" type="button" id="{px}-back">Back</button><button class="btn lime" type="button" id="{px}-go">Start</button><button class="btn ghost sm" type="button" id="{px}-skip">Skip</button></div>
<p class="wu-left" id="{px}-left"></p>
</div>
<ol class="wu-list" id="{px}-list"></ol>
</div>'''

# ---------- 1. SOLO PADEL PRACTICE ----------
# w = where it works: c = on a padel court alone, w = against a wall, h = at home / small space (no wall hitting)
# f = focus tags: vo volley, gr groundstrokes + glass, se serve, fw footwork, ov overheads, bc ball control
_SP_WARM = {"n": "Easy jog, side steps and arm circles", "ph": "Warm up", "t": 180, "d": "Jog gently, then side steps both ways, then big arm circles and trunk turns. You want to feel warm before you hit a ball.", "w": "cwh", "f": "all"}
_SP_POOL = [
    {"n": "Bounce-ups on the racket", "ph": "Ball control", "t": 120, "d": "Bounce the ball up off the face, about head height, as many times as you can. Then alternate forehand and backhand faces. Count your best run.", "w": "cwh", "f": "bc vo"},
    {"n": "Bounce-downs and walk", "ph": "Ball control", "t": 90, "d": "Bounce the ball down to the floor with the racket while you walk forwards, sideways and backwards. Keep the face flat and the wrist firm.", "w": "cwh", "f": "bc"},
    {"n": "Edge and catch control", "ph": "Ball control", "t": 90, "d": "Bounce the ball up, then catch it softly on the face with no bounce, like a cushion. This trains the soft hands you need for blocks and drop volleys.", "w": "cwh", "f": "bc vo"},
    {"n": "Shadow forehand and backhand with split step", "ph": "Shadow", "t": 120, "d": "No ball. Split step, turn your shoulders, short backswing, swing through and recover to the middle. Forehand, recover, backhand, recover. Slow and clean.", "w": "cwh", "f": "gr fw"},
    {"n": "Shadow volleys at the net", "ph": "Shadow", "t": 90, "d": "Racket up in front of your chest. Split step, small step forward and punch the volley with a short movement, then back to ready. No big swing.", "w": "cwh", "f": "vo fw"},
    {"n": "Shadow bandeja turn", "ph": "Shadow", "t": 90, "d": "Turn sideways, non-hitting arm up to point at the ball, racket back behind your head. Side steps back, then swing forward and slightly down. Keep the turn, finish balanced.", "w": "cwh", "f": "ov"},
    {"n": "Quick feet: split step and shuffle", "ph": "Footwork", "t": 90, "d": "Split step, three fast side shuffles left, split step, three right. Stay low, never cross your feet. 20 seconds on, 10 seconds easy, repeat.", "w": "cwh", "f": "fw"},
    {"n": "Wall volleys: forehand only", "ph": "Wall", "t": 120, "d": "Stand 2 to 3 m from a solid wall. Volley the ball to the wall without letting it bounce, forehand only. Short punch, firm wrist, aim at chest height.", "w": "cw", "f": "vo"},
    {"n": "Wall volleys: backhand, then alternate", "ph": "Wall", "t": 120, "d": "Same distance, now backhand only for a minute, then alternate forehand and backhand. If you miss, restart with a soft feed. Count your best rally.", "w": "cw", "f": "vo"},
    {"n": "Wall groundstrokes", "ph": "Wall", "t": 150, "d": "Stand 5 to 6 m back. Let the ball bounce once and hit it to the wall at waist height with a smooth, controlled swing. Control first, speed later.", "w": "cw", "f": "gr"},
    {"n": "Wall lob control", "ph": "Wall", "t": 90, "d": "Hit the ball high up the wall with an open face and a slow, lifting swing. Let it bounce, then do it again. This builds the feel for a deep lob.", "w": "cw", "f": "gr"},
    {"n": "Serve to a line on the wall", "ph": "Serve", "t": 120, "d": "Mark a line about 90 cm high (net height) with tape or chalk. Bounce, hit below the waist, and land the ball just above the line. 10 serves, rest, 10 more.", "w": "w", "f": "se"},
    {"n": "Serves to targets", "ph": "Serve", "t": 180, "d": "Put a ball can or towel in the corner of the service box (to the side glass) and one in the middle (the T). 10 serves at each target from each side. Bounce, hit below the waist, one foot behind the line.", "w": "c", "f": "se"},
    {"n": "Self-feed off the back glass", "ph": "Glass", "t": 150, "d": "Throw the ball against the back glass after a bounce. Turn sideways, wait for it to come off the glass, step and hit it cross-court. Then the backhand side.", "w": "c", "f": "gr"},
    {"n": "Side glass exits", "ph": "Glass", "t": 120, "d": "Throw the ball so it bounces and hits the side glass, then the back glass. Move your feet early, let it come out and hit it back to the middle of the court.", "w": "c", "f": "gr"},
    {"n": "Self-feed volleys to targets", "ph": "Net", "t": 150, "d": "Stand at the net. Toss the ball up, volley it deep to a target near the back glass, then a short one to the feet area. Change sides every 10.", "w": "c", "f": "vo"},
    {"n": "Self-feed bandejas", "ph": "Overhead", "t": 150, "d": "From near the service line, toss the ball high in front of your hitting shoulder, turn and hit a controlled bandeja deep. Aim for the back glass after the bounce, not the fence.", "w": "c", "f": "ov"},
    {"n": "Net to back recovery runs", "ph": "Footwork", "t": 120, "d": "Start at the net in ready position. Side-step and back-pedal to the service line, split step, then move forward again. 6 runs, walk back between them.", "w": "c", "f": "fw"},
    {"n": "Ball drop forehands to a target", "ph": "Groundstroke", "t": 150, "d": "Drop the ball beside you, let it bounce and hit a forehand cross-court to a target. 10 forehands, then 10 backhands. Same height every time, just over the net.", "w": "c", "f": "gr"},
]
_SP_COOL = {"n": "Cool down: walk and stretch", "ph": "Finish", "t": 120, "d": "Walk slowly, then stretch calves, thighs and forearms. The full routine is on the cool-down timer page.", "w": "cwh", "f": "all"}
SP_JSON = json.dumps({"warm": _SP_WARM, "pool": _SP_POOL, "cool": _SP_COOL}, ensure_ascii=False)

sp = f'''<header class="hero"><div class="wrap"><h1>Solo padel practice: a drill plan and timer for when you have no partner.</h1>
<p class="lead">No partner tonight? Pick where you can practise, what you want to work on and how long you have. You get a step-by-step session with a timer that beeps at every change, so you can just follow it. Works on an empty padel court, against any solid wall, or in a small space at home.</p>
{quick("Yes, you can practise padel alone. The most useful solo drills are wall volleys (stand 2 to 3 m from a wall and volley without a bounce), wall groundstrokes from 5 to 6 m, serves to targets, self-feeds off the back glass on an empty court, ball-control bounce-ups and shadow swings with a split step. Twenty minutes, two or three times a week, is enough to feel the difference.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<div class="card" style="margin-bottom:16px" id="sp-set">
{_seg("sp", "where", "Where can you practise?", [("c", "Empty padel court"), ("w", "A wall"), ("h", "Home, no wall")], "c")}
{_seg("sp", "focus", "What do you want to work on?", [("all", "A bit of everything"), ("vo", "Volleys"), ("gr", "Groundstrokes + glass"), ("se", "Serve"), ("ov", "Overheads"), ("fw", "Footwork")], "all")}
{_seg("sp", "len", "How long do you have?", [("10", "10 min"), ("20", "20 min"), ("30", "30 min")], "20")}
</div>
{_timer_block("sp", "Easy jog, side steps and arm circles", "Warm up")}
<p class="muted" style="margin-top:12px">Tap any drill in the list to jump to it. Your choices are saved on this device. Ask your club before booking a court just for solo practice; many allow it at quiet times.</p></div></section>
<script>window.SP={SP_JSON};</script>
{AD.format("sp-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Can you practise padel on your own?</h2></div>
<p>Yes. You can't play points alone, but most of what makes a padel player better can be trained solo: clean contact, soft hands at the net, a repeatable serve, early footwork and reading the glass. Coaches use the same building blocks in lessons. What you can't train alone is reading opponents and working with a partner, so mix solo sessions with real games and use them to fix one thing at a time.</p>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>Where</th><th>Best solo drills</th><th>What you need</th></tr></thead><tbody>
<tr><td>Empty padel court</td><td>Serves to targets, self-feeds off the back and side glass, self-feed volleys and bandejas, recovery runs</td><td>6 to 12 balls, 2 ball cans or towels as targets</td></tr>
<tr><td>Any solid wall</td><td>Wall volleys, wall groundstrokes, lob control, serve to a tape line at 90 cm</td><td>A flat wall with no windows, 2 or 3 balls, tape or chalk</td></tr>
<tr><td>Home or garden, no wall</td><td>Bounce-ups, bounce-downs, catch control, shadow swings, quick-feet footwork</td><td>A racket, one ball and 2 m of space</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What are the best padel wall drills?</h2></div><div class="grid">{_cards([
    ("Forehand wall volleys", "Stand 2 to 3 m from the wall and keep the ball going without a bounce. Short punch, racket head up. Start with 10 in a row, then 25."),
    ("Backhand and alternate volleys", "The backhand volley is where most club players lose points. Do a full minute backhand only, then alternate sides."),
    ("Wall groundstrokes", "From 5 to 6 m, one bounce, controlled swing to waist height on the wall. A smooth rally of 20 beats ten hard hits."),
    ("Serve to a tape line", "A line at about 90 cm copies the net. Land the ball just above it with a below-the-waist serve, then aim left and right of a mark."),
], pill="Drill")}</div>
<p class="muted" style="margin-top:12px">Use a wall you are allowed to hit, away from windows and cars. Padel balls are slightly less bouncy than tennis balls, so stand a little closer than you would for tennis.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you practise padel serves alone?</h2></div>
<p>Book or use a quiet court, put two targets in each service box (the corner by the side glass and the middle line, the T), and hit 10 serves at each from both sides. Remember the rules: bounce the ball behind the service line, hit it at or below waist height, and keep at least one foot on the ground. Count how many land in the box and how many reach the target, and write it down so you can see progress. More on the technique in <a href="{href("how-to-serve-padel.html")}">how to serve in padel</a>, and check what is legal with the <a href="{href("serve-rules.html")}">serve checker</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long and how often should you practise alone?</h2></div>
<div class="tbl"><table><thead><tr><th>Your time</th><th>A good plan</th></tr></thead><tbody>
<tr><td>10 minutes</td><td>Warm up, 2 or 3 drills on one weakness, done. Great before a match or on a busy day.</td></tr>
<tr><td>20 minutes</td><td>Warm up, 5 or 6 drills with one main focus plus ball control, short cool-down.</td></tr>
<tr><td>30 minutes</td><td>Warm up, 8 to 10 drills, focus first while you are fresh, then mixed drills, cool-down.</td></tr>
</tbody></table></div>
<p style="margin-top:12px">Two or three short solo sessions a week usually help more than one long one, because you repeat the movement more often. Keep the quality high: when your contact gets sloppy, stop the drill and move on. If you want a full week plan with games, lessons and solo time, build one with the <a href="{href("padel-training-plan.html")}">training plan generator</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What mistakes do people make when practising alone?</h2></div><div class="grid">{_cards([
    ("Hitting too hard", "Speed hides bad contact. Hit at 60 to 70% and keep the ball going; power comes later."),
    ("Standing still", "Real padel is moving and recovering. Add a split step before every ball, even in wall drills."),
    ("Only the favourite shot", "Most people drill the forehand they already like. Spend at least half the time on the weaker side."),
    ("No targets", "Without a target you can't tell if you are improving. Use cans, towels or tape and count your hits."),
], pill="Mistake")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Got a partner?</h3><p>Plan a 2 to 4 player session with timers in the <a href="{href("drills.html")}">padel drills planner</a>.</p></div>
<div class="card"><h3>Footwork first</h3><p>Train your reaction with the <a href="{href("padel-footwork.html")}">split-step trainer</a>.</p></div>
<div class="card"><h3>Get stronger off court</h3><p>Ten to thirty minutes, at home or in the gym: the <a href="{href("padel-workout.html")}">padel workout builder</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Kit for solo practice</h3><p>Solo drills go faster with more balls: a pack or a bucket saves chasing every miss.</p><ul class="aff-links"><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls (packs)</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: LTA "Training tips to improve your padel skills" and LTA Padel "Padel training tips" (practise a weakness, short regular sessions, footwork and split step), The Padel School "Practicing on your own" (wall and ball-control work), Padel Browser "Best padel drills solo and with a partner" (wall volleys, serve targets, glass self-feeds). Serve rules: FIP / IPF Padel Game Regulations (bounce behind the line, hit at or below the waist, one foot on the ground). Drill times and the session builder are our own.</p></div></section>'''
sp_faq = [
    ("Can you practise padel alone?", "Yes. Wall volleys, wall groundstrokes, serves to targets, self-feeds off the glass on an empty court, ball-control bounce-ups and shadow swings can all be done alone."),
    ("What is the best padel drill to do alone?", "Wall volleys: stand 2 to 3 m from a solid wall and volley without letting the ball bounce, forehand, then backhand, then alternating. It trains contact, soft hands and quick reactions."),
    ("How do I practise my padel serve alone?", "Put targets in the corner and the middle of each service box and hit 10 legal serves at each target from both sides, counting how many land. At a wall, aim just above a tape line at about 90 cm."),
    ("Can I practise padel against a wall at home?", "Yes, if the wall is solid and safe to hit, away from windows. With no wall you can still do bounce-ups, catch control, shadow swings and footwork in about 2 m of space."),
    ("How long should a solo padel session be?", "Ten to thirty minutes is enough. Two or three short sessions a week usually help more than one long one."),
    ("Can I book a padel court to practise on my own?", "Many clubs allow it, often at quiet times. Ask the club first, as some only allow bookings for two or four players."),
]
page("padel-solo-practice.html", "Solo Padel Practice: Drills Alone + Free Session Timer",
     "How to practise padel alone: wall drills, serve targets, glass self-feeds and home drills, with a free solo session builder and beep timer for 10 to 30 minutes.",
     sp, sp_faq, "Solo practice")

# ---------- 2. PADEL WORKOUT (strength) ----------
# k = kit: h = no kit (home), g = gym; f = focus tags: l legs, c core, s shoulder/arm care
_WO_POOL = [
    {"n": "Squats", "ph": "Legs", "d": "Feet shoulder width, sit back and down until thighs are about level, chest up, then stand. Slow down, quick up.", "k": "hg", "f": "l"},
    {"n": "Goblet squats", "ph": "Legs", "d": "Hold a dumbbell or kettlebell at your chest and squat. Knees follow your toes. Pick a weight you can lift 10 to 12 times with good form.", "k": "g", "f": "l"},
    {"n": "Reverse lunges", "ph": "Legs", "d": "Step back, lower the back knee towards the floor, push back up through the front heel. Alternate legs. This is the low position of a volley.", "k": "hg", "f": "l"},
    {"n": "Side lunges", "ph": "Legs", "d": "Big step to the side, sit into that hip with the other leg straight, push back to the middle. Alternate. Copies reaching wide for a ball.", "k": "hg", "f": "l"},
    {"n": "Calf raises", "ph": "Legs", "d": "Rise onto your toes, pause, lower slowly. Hold a wall for balance or a dumbbell for more load. Calves take a beating in padel.", "k": "hg", "f": "l"},
    {"n": "Glute bridges", "ph": "Hips", "d": "Lie on your back, knees bent, push your hips up until your body is straight from knees to shoulders, squeeze, lower slowly.", "k": "hg", "f": "l c"},
    {"n": "Romanian deadlifts", "ph": "Hips", "d": "Dumbbells in front of your thighs, soft knees, hinge at the hips with a flat back until you feel the back of the thighs, then stand tall.", "k": "g", "f": "l"},
    {"n": "Skater hops", "ph": "Power", "d": "Jump sideways from one foot to the other and land softly on one leg. Small and controlled first. Skip this one if your knees or ankles hurt.", "k": "hg", "f": "l"},
    {"n": "Plank", "ph": "Core", "d": "On forearms and toes, body straight from head to heels. Squeeze your bottom and belly. Drop to the knees if your back sags.", "k": "hg", "f": "c"},
    {"n": "Side plank (switch halfway)", "ph": "Core", "d": "On one forearm and the side of your feet, hips high. Switch sides halfway. Your sides turn your body on every shot.", "k": "hg", "f": "c"},
    {"n": "Dead bug", "ph": "Core", "d": "Lie on your back, arms up, knees over hips. Lower the opposite arm and leg slowly while your lower back stays pressed to the floor. Alternate.", "k": "hg", "f": "c"},
    {"n": "Bird dog", "ph": "Core", "d": "On hands and knees, reach one arm forward and the opposite leg back, hold 2 seconds, return. Alternate. Good for the lower back.", "k": "hg", "f": "c"},
    {"n": "Cable or band woodchop", "ph": "Rotation", "d": "Pull a cable or band diagonally from high to low across your body, turning from the hips, arms long. Half the time each side.", "k": "g", "f": "c s"},
    {"n": "Pallof press", "ph": "Rotation", "d": "Stand side-on to a cable or band, hold it at your chest and press it straight out, resisting the twist. Half the time each side.", "k": "g", "f": "c"},
    {"n": "Push-ups", "ph": "Upper body", "d": "Hands under shoulders, body straight, lower your chest towards the floor and push up. On your knees or hands on a bench is fine.", "k": "hg", "f": "s"},
    {"n": "Dumbbell rows", "ph": "Upper body", "d": "One hand and knee on a bench, pull the dumbbell up to your hip, elbow close, then lower slowly. Half the time each arm.", "k": "g", "f": "s"},
    {"n": "Band external rotation", "ph": "Shoulder care", "d": "Elbow at your side bent 90 degrees, a light band in the hand, turn the forearm out and back slowly. Half the time each arm. Light and controlled.", "k": "g", "f": "s"},
    {"n": "Y-T raises lying face down", "ph": "Shoulder care", "d": "Lie face down, thumbs up, lift your arms into a Y, lower, then into a T, lower. No weight needed. Wakes up the upper back.", "k": "hg", "f": "s"},
    {"n": "Wrist curls with a water bottle", "ph": "Forearm", "d": "Forearm on your thigh, palm down, a full bottle in the hand. Raise the hand slowly and lower over 3 seconds. Half the time each arm. Helps the forearm that hurts in padel elbow.", "k": "h", "f": "s"},
    {"n": "Reverse wrist curls", "ph": "Forearm", "d": "Forearm on a bench, palm down, a light dumbbell. Lift the back of the hand, lower slowly over 3 seconds. Half the time each arm.", "k": "g", "f": "s"},
    {"n": "Farmer's carry", "ph": "Grip", "d": "Hold a heavy dumbbell in each hand and walk tall for the whole time, shoulders down. Grip, core and posture in one.", "k": "g", "f": "s c"},
]
WO_JSON = json.dumps({"pool": _WO_POOL}, ensure_ascii=False)

wo = f'''<header class="hero"><div class="wrap"><h1>Padel workout builder: strength for your legs, core and arm.</h1>
<p class="lead">Choose home or gym, what you want to work on and how long you have. You get a circuit of padel-focused exercises with a work and rest timer that beeps at every change. No account, no app, just press start.</p>
{quick("The best gym exercises for padel train the legs (squats, lunges, side lunges, calf raises), the core and rotation (planks, side planks, woodchops, Pallof press) and the shoulder and forearm (rows, band external rotation, wrist curls). Health guidelines from the WHO and the NHS say adults should do muscle-strengthening work on at least 2 days a week; two 20 to 30 minute sessions on days you don't play is a simple way to do it.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<div class="card" style="margin-bottom:16px" id="wo-set">
{_seg("wo", "kit", "Where are you training?", [("h", "Home, no kit"), ("g", "Gym")], "h")}
{_seg("wo", "focus", "What do you want to work on?", [("all", "Full body for padel"), ("l", "Legs and power"), ("c", "Core and rotation"), ("s", "Shoulder and arm care")], "all")}
{_seg("wo", "len", "How long do you have?", [("15", "15 min"), ("25", "25 min"), ("35", "35 min")], "25")}
{_seg("wo", "lvl", "Your level", [("new", "New to strength work"), ("reg", "I train often")], "new")}
</div>
{_timer_block("wo", "Warm up: march, arm circles, easy squats", "Warm up")}
<p class="muted" style="margin-top:12px">The timer counts work and rest. Stop any exercise that hurts. If you have a health condition, an injury or have not exercised for a long time, check with a doctor or physio first.</p></div></section>
<script>window.WO={WO_JSON};</script>
{AD.format("wo-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which muscles matter most in padel?</h2></div>
<div class="tbl"><table><thead><tr><th>Area</th><th>Why padel needs it</th><th>Good exercises</th></tr></thead><tbody>
<tr><td>Legs and hips</td><td>Low volleys, side steps, lunging for wide balls and pushing off for overheads</td><td>Squats, reverse lunges, side lunges, glute bridges, Romanian deadlifts</td></tr>
<tr><td>Calves and ankles</td><td>Constant short steps and split steps on sand-filled grass</td><td>Calf raises, skater hops (small)</td></tr>
<tr><td>Core and rotation</td><td>Every shot turns the body; a stable trunk protects the lower back</td><td>Plank, side plank, dead bug, bird dog, woodchops, Pallof press</td></tr>
<tr><td>Shoulder and upper back</td><td>Bandejas, víboras and smashes load the shoulder many times a match</td><td>Rows, band external rotation, Y-T raises, push-ups</td></tr>
<tr><td>Forearm and grip</td><td>The forearm works on every contact; it is where padel elbow starts</td><td>Wrist curls, reverse wrist curls (slow lowering), farmer's carry</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How often should padel players do strength training?</h2></div>
<p>The WHO's physical activity guidelines and the NHS both say adults should do muscle-strengthening activities that work all the major muscle groups on <strong>at least 2 days a week</strong>, on top of their aerobic activity (and padel counts as aerobic activity). For most club players, a simple week looks like this:</p>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>Day</th><th>Plan (example)</th></tr></thead><tbody>
<tr><td>Monday</td><td>Strength 25 min (full body)</td></tr>
<tr><td>Tuesday</td><td>Padel match</td></tr>
<tr><td>Wednesday</td><td>Rest or easy walk</td></tr>
<tr><td>Thursday</td><td>Strength 25 min (legs or core focus) or a <a href="{href("padel-solo-practice.html")}">solo practice</a> session</td></tr>
<tr><td>Saturday</td><td>Padel match or lesson</td></tr>
</tbody></table></div>
<p style="margin-top:12px">Our own suggestion: keep hard leg sessions at least a day away from a match, so your legs are fresh on court. Start with body weight, and add load only when 12 clean reps feel easy.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How many sets and reps?</h2></div><div class="grid">{_cards([
    ("New to strength work", "40 seconds work, 20 seconds rest, 2 or 3 rounds. Body weight only. Move slowly and stop 2 or 3 reps before form breaks."),
    ("You train often", "45 seconds work, 15 seconds rest, 3 or 4 rounds, or 3 sets of 8 to 12 reps with a weight that makes the last 2 reps hard (NHS guidance: repeat until it is hard to do one more)."),
    ("Forearm and shoulder care", "Light weights, slow lowering over 3 seconds. These are about tissue health, not lifting heavy. Daily is fine if they feel good."),
], pill="Level")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Can strength training help prevent padel injuries?</h2></div>
<p>Stronger muscles and tendons handle load better, and sports bodies and physios recommend strength work as part of injury prevention, together with a proper warm-up and building up your playing time gradually. It is not a guarantee. For the common padel problems (elbow, calf, knee, lower back and shoulder) and when to see a professional, read <a href="{href("padel-injuries.html")}">padel injuries and prevention</a>. Forearm pain on the outside of the elbow has its own page: <a href="{href("padel-elbow.html")}">padel elbow and the arm-load check</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Before you play</h3><p>Ten minutes, guided, with beeps: the <a href="{href("warm-up.html")}">padel warm-up timer</a>.</p></div>
<div class="card"><h3>After you play</h3><p>Stretch calves, thighs, hips and forearm with the <a href="{href("padel-cool-down.html")}">cool-down timer</a>.</p></div>
<div class="card"><h3>How much you burn</h3><p>Estimate calories for a match with the <a href="{href("padel-calories.html")}">padel calories calculator</a>.</p></div>
</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: WHO "Guidelines on physical activity and sedentary behaviour" (2020: adults, muscle-strengthening activities on 2 or more days a week), NHS "Physical activity guidelines for adults aged 19 to 64" (strengthening activities that work all major muscle groups at least 2 days a week; repeat until it is hard to do another repetition), LTA Padel "Padel warm-up exercises". Exercise choices match the areas named by padel coaches and fitness writers (The Padel School padel fitness, Men's Fitness "8 key exercises for padel"), in our own words. General fitness information, not medical advice.</p></div></section>'''
wo_faq = [
    ("What are the best gym exercises for padel?", "Squats, lunges and side lunges for the legs, calf raises, planks, side planks and woodchops for the core and rotation, and rows, band external rotation and wrist curls for the shoulder and forearm."),
    ("How often should I strength train for padel?", "At least 2 days a week, which is what the WHO and NHS recommend for all adults. Short 20 to 30 minute sessions on days you don't play work well."),
    ("Can I do a padel workout at home with no equipment?", "Yes. Squats, lunges, side lunges, calf raises, glute bridges, planks, side planks, push-ups, Y-T raises and wrist curls with a water bottle need no gym."),
    ("Should I lift weights before or after playing padel?", "Many players keep hard leg sessions on a different day from matches so their legs are fresh. If you must do both on one day, play first and keep the strength work short."),
    ("Which exercises help with padel elbow?", "Slow wrist curls and reverse wrist curls with a light weight, plus grip and shoulder work, are commonly used. See a physio if pain lasts."),
    ("How long should a padel workout be?", "Fifteen to thirty-five minutes is enough for most club players: a short warm-up, a circuit of 6 to 10 exercises for 2 to 4 rounds, then a stretch."),
]
page("padel-workout.html", "Padel Workout: Gym + Home Exercises With Free Timer",
     "Padel workout builder: the best gym and home exercises for padel (legs, core, rotation, shoulder, forearm), how often to train, and a free circuit timer.",
     wo, wo_faq, "Padel workout")

DEMAND_PAGES += ["padel-solo-practice.html", "padel-workout.html"]
