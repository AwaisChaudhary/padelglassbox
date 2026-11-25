# ---------------- IMPROVE YOUR PADEL: problem fixer + which side quiz (Awais 26 Nov 2026 TOP PRIORITY I1, I4) ----------------
# Executed from build.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, json).
# Demand: 'padel common mistakes', 'how to get better at padel', 'padel tips', 'padel left or right side' (many dedicated guides:
# The Padel School, Padel Browser 14 Sep 2026, Red Bull, allforpadel, padelproshop, Tienda Padel Point). Coaching advice is general, in our own words.

FIX = [
    {"id": "glass", "b": "My ball keeps hitting the back glass or going out",
     "q": "Why does my padel ball keep hitting the back glass?",
     "cause": ["A long tennis-style swing that sends the ball flat and fast.", "Trying to win the point from the back of the court.", "Hitting the ball late, so the racket face opens and the ball flies up."],
     "fix": ["Take the racket back only to shoulder height and finish short, in front of you.", "Aim about 1 m over the net at medium pace. From the back, your job is to keep the ball in play, not to win.", "Meet the ball in front of your body with a firm wrist and a slightly open face (a gentle slice)."],
     "drill": ["Cross-court control rally", "Rally cross-court with a partner at medium pace. Count balls in a row that bounce before the service line on the other side and do not hit the back glass on the full.", "3 sets of 20 in a row"],
     "links": [("drills.html", "Drills planner"), ("shots.html", "Shot library"), ("wall-rules.html", "Wall rules")]},
    {"id": "wall", "b": "I panic when the ball comes off the back glass",
     "q": "How do I play the ball off the back glass in padel?",
     "cause": ["Standing too close to the glass, so there is no room when the ball bounces out.", "Turning late and facing the glass instead of the side wall.", "Hitting the ball while it is still rising off the glass."],
     "fix": ["Wait about 1 m in front of the back glass, not against it.", "Turn your shoulders to the side wall as soon as you see the ball will reach the glass.", "Let the ball come off the glass and drop to about waist height, then hit it forward and up over the net."],
     "drill": ["Throw, catch, hit", "A partner throws the ball so it bounces and hits the back glass. First catch it as it comes off (10 times), then hit it instead.", "10 catches, then 3 sets of 10 hits"],
     "links": [("wall-rules.html", "Wall and fence rules"), ("positioning.html", "Where to stand"), ("drills.html", "Drills planner")]},
    {"id": "net", "b": "I lose points at the net",
     "q": "Why do I lose points at the net in padel?",
     "cause": ["Standing too close to the net, so any lob goes over you.", "The racket hangs low between shots, so you are late on fast balls.", "Trying to hit every volley hard."],
     "fix": ["Volley from about 2 to 2.5 m off the net. Step closer only to finish an easy ball.", "Keep the racket up in front of your chest between every shot.", "Use most volleys to place the ball deep or at the feet. Save power for high, easy balls."],
     "drill": ["Target volleys", "A partner at the back feeds balls to you at the net. Volley each one deep, to a towel or cone placed 1 m off the back glass.", "3 sets of 15, then 15 on the backhand"],
     "links": [("positioning.html", "Where to stand"), ("shots.html", "Volley in the shot library"), ("drills.html", "Drills planner")]},
    {"id": "lob", "b": "Lobs keep going over my head",
     "q": "How do I deal with lobs in padel?",
     "cause": ["Standing too close to the net.", "Running backwards while facing the net instead of turning sideways.", "Waiting too long to decide what to do."],
     "fix": ["Start a step further back at the net (about 2 to 2.5 m away).", "Turn sideways at once and move back with side steps or a cross-over step.", "Decide early: bandeja if you can reach it, or let it go and play it off the back glass. Both of you go back together."],
     "drill": ["Lob and turn", "A partner feeds lobs over you from the back. Turn sideways, move back and catch the ball above your hitting shoulder. Then play a bandeja instead of catching.", "10 catches, then 3 sets of 10 bandejas"],
     "links": [("bandeja-vs-vibora.html", "Bandeja vs víbora vs smash"), ("positioning.html", "Where to stand"), ("wall-rules.html", "Playing off the glass")]},
    {"id": "band", "b": "My bandeja goes long or into the net",
     "q": "Why does my bandeja go long?",
     "cause": ["Hitting it like a smash, with too much power.", "Letting the ball drop behind your head.", "Swinging straight down instead of across and through the ball."],
     "fix": ["Think control, not winner: the bandeja keeps you at the net.", "Hit the ball in front of your head, with your body sideways and the non-hitting arm pointing at the ball.", "Swing across the ball with a slice and aim to land it near the service line and deep corner, so it does not bounce high off the back glass."],
     "drill": ["Bandeja to the corner", "A partner feeds medium lobs. Play bandejas to the opponent's back corner. Count only balls that land past the service line and do not come back high off the glass.", "3 sets of 10"],
     "links": [("bandeja-vs-vibora.html", "Bandeja vs víbora vs smash"), ("shots.html", "Shot library"), ("drills.html", "Drills planner")]},
    {"id": "smash", "b": "I smash everything and still lose the point",
     "q": "Why do my padel smashes come back?",
     "cause": ["Smashing balls that are too far back or too low.", "Hitting into the back glass so the ball bounces back to the opponent.", "Running back to the net late after the smash."],
     "fix": ["Only smash high balls near the net that you can hit in front of you. Play a bandeja or víbora on the rest.", "Aim flat smashes at the side or the feet, not straight into the back glass.", "After every overhead, move straight back to your net position."],
     "drill": ["Smash or bandeja call", "A partner feeds lobs of different depths. Call 'smash' or 'bandeja' before the ball drops, then play it.", "20 balls, aim for 16 right calls"],
     "links": [("bandeja-vs-vibora.html", "Bandeja vs víbora vs smash"), ("out-of-court-play.html", "Out-of-court play")]},
    {"id": "ret", "b": "I miss serve returns",
     "q": "How do I return the serve better in padel?",
     "cause": ["Standing too close to the glass or too far forward.", "A big swing on a ball that is already coming fast.", "Trying to hit a winner off the return."],
     "fix": ["Wait about 1 m in front of the back glass on your half, ready to move either way.", "Use a short swing, like a block, and keep the ball low.", "Aim cross-court and low to the server's feet, or lob if the server is already at the net."],
     "drill": ["Return to a target", "A partner serves. Return each serve cross-court so it lands before the service line, low over the net.", "3 sets of 10 on each side"],
     "links": [("serve-rules.html", "Serve rules"), ("positioning.html", "Where to stand to receive"), ("drills.html", "Drills planner")]},
    {"id": "serve", "b": "My serve is easy to attack",
     "q": "How can I make my padel serve better?",
     "cause": ["Serving high and soft into the middle of the box.", "Rushing the serve.", "Staying at the back after serving."],
     "fix": ["Serve low over the net and aim near the side glass or at the receiver's backhand.", "Take a breath, bounce the ball, and use a smooth, short swing below the waist.", "Move to the net straight after the serve, together with your partner."],
     "drill": ["Serve targets", "Put two towels in the service box: one near the side glass, one near the centre line. Serve 10 at each.", "20 serves, count hits"],
     "links": [("serve-rules.html", "Serve rules and checker"), ("positioning.html", "Where to stand after the serve")]},
    {"id": "partner", "b": "My partner and I both go for the ball (or both leave it)",
     "q": "Who takes the middle ball in padel?",
     "cause": ["No plan for balls down the middle.", "Not calling the ball.", "Moving at different times, so a gap opens between you."],
     "fix": ["Agree a middle rule before you play. A common one: the player with the forehand in the middle takes it (the left-side player in a pair of right-handers).", "Call 'mine' or 'yours' early and loud on every shared ball.", "Move up and back together, about 3 m apart, as if joined by a rope."],
     "drill": ["Middle ball calls", "A coach or third player feeds balls down the middle. The player who takes it must call before hitting. A ball with no call counts as a miss.", "3 sets of 10"],
     "links": [("which-side-padel.html", "Which side should I play?"), ("positioning.html", "Where to stand")]},
    {"id": "late", "b": "I'm always late to the ball",
     "q": "Why am I always late to the ball in padel?",
     "cause": ["Flat feet when the opponent hits.", "Preparing the racket only after the ball bounces.", "Standing in the wrong place, so every ball is a long run."],
     "fix": ["Do a small hop (a split step) just as the opponent hits, then move.", "Turn and take the racket back as soon as you know which side the ball is going.", "Use the positions in our positioning guide so you start in the middle of your zone."],
     "drill": ["Split step and shadow", "Without a ball: a partner points left or right just after you land a split step. Move two steps, shadow a shot, come back.", "4 rounds of 30 seconds"],
     "links": [("positioning.html", "Where to stand"), ("warm-up.html", "Warm-up timer"), ("padel-calories.html", "Fitness and calories")]},
    {"id": "tired", "b": "I get tired or slow late in matches",
     "q": "How do I keep my energy in a padel match?",
     "cause": ["Long points from always playing from the back.", "Not warming up, so you start stiff and then fade.", "Not drinking enough water between games."],
     "fix": ["Win the net more often: it shortens points.", "Do a 10-minute warm-up before you play.", "Drink at each change of ends and bring enough water for the session."],
     "drill": ["Ten-ball sprints", "Partner feeds 10 balls in a row to different corners at a fast pace. Rest 45 seconds.", "4 rounds"],
     "links": [("warm-up.html", "Warm-up timer"), ("padel-calories.html", "Calories calculator"), ("drills.html", "Drills planner")]},
    {"id": "elbow", "b": "My elbow, wrist or shoulder hurts",
     "q": "Why does my elbow hurt after padel?",
     "cause": ["Gripping the racket very tightly all the time.", "A racket that is too heavy, head-heavy or very hard for you.", "Playing a lot more than usual without rest or a warm-up."],
     "fix": ["See a doctor or physio if pain lasts more than a few days, is sharp, or comes back. Do not play through it.", "Hold the racket loosely between shots and squeeze only at contact.", "Check your racket: a lighter, low-balance racket with a soft core is usually easier on the arm."],
     "drill": ["Loose grip rally", "Only once you are pain free: rally at slow pace and say 'soft' between every shot to remind yourself to relax the grip.", "5 minutes at the start of each session"],
     "links": [("padel-injuries.html", "Padel injuries and prevention"), ("racket-balance.html", "Racket weight and balance"), ("padel-grip.html", "How to hold the racket")]},
]
FIX_BY = {x["id"]: x for x in FIX}

def _fix_card(x):
    lk = " · ".join(f'<a href="{href(f)}">{e(t)}</a>' for f, t in x["links"])
    return (f'<details class="card fx-d" id="fx-{x["id"]}"><summary><h3 style="display:inline">{e(x["q"])}</h3></summary>'
            f'<p><strong>Likely causes:</strong></p><ul>' + "".join(f"<li>{e(c)}</li>" for c in x["cause"]) + '</ul>'
            f'<p><strong>Three fixes:</strong></p><ol>' + "".join(f"<li>{e(c)}</li>" for c in x["fix"]) + '</ol>'
            f'<p><strong>Drill: {e(x["drill"][0])}.</strong> {e(x["drill"][1])} <em>Reps: {e(x["drill"][2])}.</em></p><p class="muted">Read next: {lk}</p></details>')

fx_btns = "".join(f'<button type="button" class="opt" data-v="{x["id"]}" aria-pressed="{"true" if i == 0 else "false"}">{e(x["b"])}</button>' for i, x in enumerate(FIX))
fx_js = {x["id"]: {"q": x["q"], "cause": x["cause"], "fix": x["fix"], "drill": x["drill"], "links": [[f[:-5], t] for f, t in x["links"]]} for x in FIX}
fx = f'''<header class="hero"><div class="wrap"><h1>Fix my padel: why do I keep doing that?</h1>
<p class="lead">Pick the problem that costs you the most points. Get the likely cause in plain words, three fixes, and one drill with reps to practise this week.</p>
{quick("Most padel problems for new and improving players come from four habits: swinging like in tennis, standing in the wrong place (too close to the net or the back glass), trying to win the point from the back, and not talking to your partner. Shorten your swing, volley about 2 to 2.5 m from the net, wait about 1 m off the back glass, and call every middle ball.")}
<p class="muted" style="margin-top:8px;font-size:.9rem">Last updated 26 Nov 2026. General coaching advice in our own words, not a lesson. For pain, see a doctor or physio.</p></div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="fx">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Padel problem fixer</h2>
<p class="muted" style="margin-top:0">What goes wrong most often? Tap one.</p>
<div class="opts fx-opts" id="fx-pick" role="group" aria-label="Pick your padel problem">{fx_btns}</div>
<p class="muted" style="margin:14px 0 0;font-size:.92rem">Tip: add the fix to your practice list, work on one thing per session, and come back when it is fixed. Your list is saved on this device only.</p>
</div>
<aside class="result" id="fx-out" aria-live="polite"><h2 id="fx-h">Your fix</h2><p id="fx-c"></p><ol id="fx-f" style="padding-left:20px;color:#d6e0fb;display:grid;gap:6px"></ol><p id="fx-d"></p><p id="fx-l" class="wr-src"></p>
<div class="btns" style="margin:10px 0 0"><button class="btn lime sm" type="button" id="fx-add">Add to my practice list</button></div></aside>
</div></section>
<section style="padding-top:0"><div class="wrap" style="max-width:860px"><div class="card"><h2 style="font-size:1.3rem;margin-top:0">My practice list</h2><ul class="check" id="fx-list"></ul><p class="muted" id="fx-empty">Nothing yet. Pick a problem above and tap "Add to my practice list".</p>
<div class="btns" style="margin:12px 0 0"><button class="btn sm" type="button" id="fx-copy">Copy list</button><button class="btn ghost sm" type="button" id="fx-clear">Clear list</button></div></div></div></section>
<script>window.FIX={json.dumps(fx_js)};</script>
{AD.format("fix-mid")}
<section><div class="wrap"><div class="sh"><h2>What are the most common padel mistakes?</h2><p class="muted">The mistakes coaches see most in new and improving players, and the quick fix for each.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Mistake</th><th scope="col">Quick fix</th><th scope="col">Learn more</th></tr></thead><tbody>
<tr><td>Long, tennis-style swing</td><td>Racket back to shoulder height, short finish in front</td><td><a href="{href("shots.html")}">Shots</a></td></tr>
<tr><td>Hitting too hard from the back</td><td>Medium pace, aim at feet, gaps and corners</td><td><a href="{href("drills.html")}">Drills</a></td></tr>
<tr><td>Not using the back glass</td><td>Let it bounce off the glass, then hit it as it drops</td><td><a href="{href("wall-rules.html")}">Wall rules</a></td></tr>
<tr><td>Standing too close to the net</td><td>About 2 to 2.5 m away when volleying</td><td><a href="{href("positioning.html")}">Positioning</a></td></tr>
<tr><td>Standing against the back glass</td><td>About 1 m in front of it when defending</td><td><a href="{href("positioning.html")}">Positioning</a></td></tr>
<tr><td>Never lobbing</td><td>Lob when both opponents are at the net and you are under pressure</td><td><a href="{href("shots.html")}">Lob</a></td></tr>
<tr><td>Smashing every high ball</td><td>Bandeja or víbora unless the ball is high and near the net</td><td><a href="{href("bandeja-vs-vibora.html")}">Overheads</a></td></tr>
<tr><td>Wrong grip</td><td>Continental grip for almost every shot</td><td><a href="{href("padel-grip.html")}">Grip</a></td></tr>
<tr><td>Not talking to your partner</td><td>Call "mine" or "yours"; agree who takes the middle</td><td><a href="{href("which-side-padel.html")}">Sides</a></td></tr>
<tr><td>Moving apart from your partner</td><td>Move up and back together, about 3 m apart</td><td><a href="{href("positioning.html")}">Positioning</a></td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap" style="max-width:860px"><div class="sh"><h2>All problems and fixes</h2><p class="muted">The same advice as the fixer, open any one.</p></div>
<div style="display:grid;gap:12px">{"".join(_fix_card(x) for x in FIX)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do I get better at padel faster?</h2></div><div class="grid">
<div class="card"><h3>Work on one thing at a time</h3><p>Pick your biggest leak above, practise its drill for a week or two, then test it in a match. Changing five things at once rarely sticks.</p></div>
<div class="card"><h3>Know your level</h3><p>The <a href="{href("level-calculator.html")}">level calculator</a> shows what players at your level usually work on next.</p></div>
<div class="card"><h3>Get eyes on your game</h3><p>A coach spots causes you cannot feel. See what <a href="{href("padel-lessons.html")}">padel lessons</a> cost and how to pick a coach.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Build a practice session</h3><p>Put two or three drills together in the <a href="{href("drills.html")}">padel drills planner</a>.</p></div>
<div class="card"><h3>Pick your side</h3><p>Left or right? Take the 1-minute <a href="{href("which-side-padel.html")}">which side quiz</a> with your partner.</p></div>
<div class="card"><h3>Check your racket</h3><p>Too heavy or too hard can cause errors and sore arms. Try the <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Practice gear</h3><p>Fresh balls bounce truer for drills, and a new overgrip helps you hold the racket loosely.</p><ul class="aff-links"><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round (control) rackets</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 26 Nov 2026: The Padel School "10 common beginner mistakes in padel" (too close to the net, playing like tennis, ignoring the walls, poor positioning, no communication, not lobbing, overhitting, late preparation, losing patience) and Padel Browser "Common padel mistakes beginners make" (9 Jun 2026: long swing, too close to the back glass, hitting instead of placing, no lob, not moving as a pair, wrong grip, not using the walls, rushing the serve). Distances match our <a href="{href("positioning.html")}">positioning guide</a>. Fixes, drills and reps are general coaching advice in our own words; they are not from the sources and are not a substitute for a coach. Pain advice: see a doctor or physio.</p></div></section>'''
fx_faq = [
    ("What is the most common mistake in padel?", "Playing like tennis: a long, hard, flat swing from the back of the court. In padel the walls give the opponents a second chance, so control and placement win more points than power."),
    ("Why does my padel ball keep going out or hitting the back glass?", "Usually a long swing, too much pace, or a late contact that opens the racket face. Shorten the swing, aim about 1 m over the net at medium pace, and meet the ball in front of you."),
    ("How far from the net should I stand in padel?", "About 2 to 2.5 m when volleying. Closer and lobs go over you; further back and the ball drops at your feet."),
    ("How do I stop lobs going over my head in padel?", "Stand about 2 to 2.5 m from the net, turn sideways as soon as you see the lob, and decide early between a bandeja and letting it come off the back glass. Move back together with your partner."),
    ("Who takes the ball down the middle in padel?", "Agree it before you play. A common rule is that the player with the forehand in the middle takes it, which is the left-side player when both partners are right-handed. Always call 'mine' or 'yours'."),
    ("How do I get better at padel quickly?", "Work on one problem at a time with a simple drill, play regular matches at your level, and take a lesson now and then so a coach can spot the cause of your errors."),
    ("Why does my elbow hurt after playing padel?", "Common reasons are gripping too tightly, a racket that is too heavy, head-heavy or hard, and a sudden increase in how much you play. See a doctor or physio if it lasts, and do not play through pain."),
]
page("fix-my-padel.html", "Fix My Padel: Common Padel Mistakes and How to Fix Them (Free Problem Fixer) | Padel Glass Box",
     "Why do I keep hitting the glass, losing at the net or missing lobs? Pick your padel problem and get the cause, three fixes and a drill with reps. Common padel mistakes, fixed.",
     fx, fx_faq, "Fix my padel")

# ---------------- WHICH SIDE: left or right (I4) ----------------
SDQ = [
    ("hand", "Which hand do you play with?", [("r", "Right"), ("l", "Left")], "r"),
    ("ph", "And your partner?", [("r", "Right"), ("l", "Left"), ("x", "No fixed partner")], "r"),
    ("lvl", "How long have you played?", [("new", "Under 6 months"), ("mid", "6 months to 2 years"), ("adv", "Over 2 years")], "mid"),
    ("over", "Who has the more reliable overhead (bandeja and smash)?", [("me", "Me"), ("eq", "About the same"), ("p", "My partner")], "eq"),
    ("move", "Who moves faster sideways and backwards?", [("me", "Me"), ("eq", "About the same"), ("p", "My partner")], "eq"),
    ("calm", "Who makes fewer errors in long rallies?", [("me", "Me"), ("eq", "About the same"), ("p", "My partner")], "eq"),
    ("fh", "Your best groundstroke", [("fh", "Forehand"), ("eq", "Both about the same"), ("bh", "Backhand")], "eq"),
    ("style", "Do you prefer to build points or finish them?", [("b", "Build: patient, keep it in"), ("eq", "Both"), ("f", "Finish: go for the winner")], "eq"),
]
def sdq(name, title, opts, on):
    b = "".join(f'<button type="button" class="opt" data-v="{val}" aria-pressed="{"true" if val == on else "false"}">{e(lab)}</button>' for val, lab in opts)
    return f'<div class="q"><h3>{e(title)}</h3><div class="opts" data-sd="{name}" role="group" aria-label="{e(title)}">{b}</div></div>'
sd = f'''<header class="hero"><div class="wrap"><h1>Which side should I play in padel: left or right?</h1>
<p class="lead">Answer 8 quick questions about you and your partner. Get a side, the reasons, what your job is on that side, and a drill to practise it.</p>
{quick("In a pair of right-handers, the left side (revés) usually suits the player with the stronger overhead and faster movement, because middle balls and lobs down the middle are their forehand. The right side (drive) suits the more patient, consistent player who builds the point. A left-hander with a right-handed partner usually plays the right side, so both forehands cover the middle. New players should try both sides first.")}
<p class="muted" style="margin-top:8px;font-size:.9rem">Last updated 26 Nov 2026.</p></div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="sd">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Left or right side quiz</h2>
<p class="muted" style="margin-top:0">Best done with your partner. Be honest about who is better at what.</p>
{"".join(sdq(*x) for x in SDQ)}
<p class="muted" style="margin:0;font-size:.92rem">The quiz weighs the factors that padel coaches name most often (sources below); the scoring is our own. Answers saved on this device only.</p>
</div>
<aside class="result" id="sd-out" aria-live="polite"><h2 id="sd-h">Your side</h2><p id="sd-conf"></p><ul id="sd-why" style="padding-left:20px;color:#d6e0fb;display:grid;gap:6px"></ul><p id="sd-job"></p><p id="sd-drill"></p><p id="sd-next" class="wr-src"></p></aside>
</div></section>
{AD.format("side-mid")}
<section><div class="wrap"><div class="sh"><h2>What does each side do in padel?</h2><p class="muted">Seen from your own back glass, looking at the net. Roles are for a pair of right-handers.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Right side (drive)</th><th scope="col">Left side (revés)</th></tr></thead><tbody>
<tr><td>Main job</td><td>Build the point: keep the ball low, deep and in play</td><td>Finish the point: take chances on high and middle balls</td></tr>
<tr><td>Middle balls</td><td>Usually on your backhand, so you often leave them</td><td>Usually on your forehand, so you often take them</td></tr>
<tr><td>Lobs down the middle</td><td>Partner usually takes them</td><td>Usually yours: bandeja, víbora or smash</td></tr>
<tr><td>Key shots</td><td>Cross-court rally, low return, backhand volley down the line</td><td>Bandeja, víbora, smash, forehand volley in the middle</td></tr>
<tr><td>Suits</td><td>Patient, consistent players; often a good start for beginners</td><td>Players with a reliable overhead who move well</td></tr>
<tr><td>Serve and return</td><td>Receives the first point of each game (the deuce side)</td><td>Receives the 15-0, 30-15 and advantage points</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Both sides attack and defend in modern padel. These are tendencies, not fixed rules. Where to stand in each situation: <a href="{href("positioning.html")}">positioning guide</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which side should a left-handed padel player play?</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">Pair</th><th scope="col">Usual set-up</th><th scope="col">Why</th></tr></thead><tbody>
<tr><td>Right-hander + right-hander</td><td>Either way: decide by overhead, movement and consistency</td><td>The left player has the forehand in the middle</td></tr>
<tr><td>Left-hander + right-hander</td><td>Left-hander on the right, right-hander on the left</td><td>Both forehands cover the middle, and both overheads face the middle lobs</td></tr>
<tr><td>Left-hander + left-hander</td><td>Either way: the right-side player now has the forehand in the middle</td><td>Everything is mirrored, so the "finisher" usually plays the right</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Should beginners pick a side?</h2></div><div class="grid">
<div class="card"><h3>Play both at first</h3><p>In your first months, swap sides often. You learn both roles, and you find out which one feels natural. Moving well with your partner matters more than the side.</p></div>
<div class="card"><h3>Then settle in</h3><p>Once you play regularly with the same partner, pick sides with the quiz above and stick with them for a few weeks so you both learn the patterns.</p></div>
<div class="card"><h3>Still a tie?</h3><p>Play one set each way and count your unforced errors with the <a href="{href("score.html")}">score keeper</a> open. Keep the set-up with fewer errors.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Fix the weak shot</h3><p>Left side? Your overhead must be reliable. Learn it in <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora vs smash</a>.</p></div>
<div class="card"><h3>Fix a problem</h3><p>Losing at the net or confused in the middle? Try the <a href="{href("fix-my-padel.html")}">padel problem fixer</a>.</p></div>
<div class="card"><h3>Practise as a pair</h3><p>Build a session for two in the <a href="{href("drills.html")}">drills planner</a>.</p></div>
</div></div></section>
<section><div class="wrap"><p class="muted" style="font-size:.9rem">Sources, checked 26 Nov 2026: The Padel School "How to choose your side in padel" (right side usually more consistent and sets up the point; left side usually more aggressive and athletic and covers lobs into the middle; left-handers almost always play the right; don't choose a side too early as a beginner) and Padel Browser "Left side vs right side in padel" (14 Sep 2026: right side builds the point and takes most first balls; left side finishes, owns the middle forehand and middle lobs, needs a reliable bandeja, usually the more mobile player; lefty on the right with a righty on the left puts both forehands in the middle; two lefties mirror the roles; play both sides early, play a set each way if still unsure). Padel Browser also notes a 2024 study of Premier Padel lobs found no link between side and how often a player is lobbed. Serve-order row from FIP rules (first point of each game served to the right). Quiz scoring and drills are our own general advice.</p></div></section>'''
sd_faq = [
    ("Which side is better in padel, left or right?", "Neither is better. The right side (drive) builds the point with consistent, low balls. The left side (revés) usually finishes the point with overheads and takes the middle forehand. Pick the side that fits your strengths and your partner's."),
    ("Which side should a left-handed padel player play?", "With a right-handed partner, a left-hander usually plays the right side, so both forehands and overheads cover the middle. Two left-handers mirror the usual roles."),
    ("Who plays on the left in padel?", "In a pair of right-handers, usually the player with the more reliable overhead who moves faster, because lobs and balls down the middle come to their forehand."),
    ("Is the right side easier in padel?", "Many beginners find the right side a good start because the job is to keep the ball in play rather than finish points. Both sides need volleys, lobs and play off the glass."),
    ("Who takes the middle ball in padel?", "Usually the player whose forehand is in the middle: the left-side player in a pair of right-handers. Agree it before you play and call every middle ball."),
    ("Should beginners play both sides in padel?", "Yes. Swap sides often in your first months, then settle on one side once you play regularly with the same partner."),
    ("What is the drive and revés side in padel?", "Drive is the right side and revés is the left side, seen from your own back glass. The names come from Spanish for forehand (drive) and backhand (revés)."),
]
page("which-side-padel.html", "Which Side Should I Play in Padel? Left or Right Side Quiz | Padel Glass Box",
     "Left (revés) or right (drive) side in padel? Take the free 8-question quiz with your partner: get your side, why, what your job is and a drill. Left-handers, middle balls and beginners explained.",
     sd, sd_faq, "Which side to play")

IMPROVE_PAGES = ["fix-my-padel.html", "which-side-padel.html"]
