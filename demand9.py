# ---------------- DEMAND RUN 12 (27 Nov 2026): compare two padel rackets, footwork + split-step trainer, partner communication + middle-ball decider ----------------
# Executed from demand8.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards).

# ---------- 1. COMPARE TWO PADEL RACKETS ----------
def _rc_side(s, shape, core, face):
    return f'''<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Racket {s.upper()}</h2>
<div class="q"><h3><label for="rc-{s}-name">Name (optional)</label></h3><input class="search" id="rc-{s}-name" type="text" maxlength="40" placeholder="e.g. the one in my basket"></div>
{_bq2("rc", s + "shape", "Shape", [("round", "Round"), ("tear", "Teardrop"), ("diamond", "Diamond")], shape)}
<div class="gen-nums"><div class="q"><h3><label for="rc-{s}-w">Weight (g)</label></h3><input class="search" id="rc-{s}-w" type="number" min="300" max="400" inputmode="numeric" placeholder="e.g. 360"></div>
<div class="q"><h3><label for="rc-{s}-b">Balance (mm, optional)</label></h3><input class="search" id="rc-{s}-b" type="number" min="230" max="290" inputmode="numeric" placeholder="e.g. 265"></div></div>
{_bq2("rc", s + "core", "Core feel", [("soft", "Soft"), ("med", "Medium"), ("hard", "Hard")], core)}
{_bq2("rc", s + "face", "Face", [("glass", "Fibreglass"), ("mix", "Carbon + glass"), ("carbon", "Carbon")], face)}</div>'''

rc = f'''<header class="hero"><div class="wrap"><h1>Compare two padel rackets side by side.</h1>
<p class="lead">Stuck between two rackets? Copy the shape, weight, balance, core and face from each product page. The comparison says what each difference will feel like on court and which one fits your level, style and arm better.</p>
{quick("When you compare two padel rackets, look at the specs in this order: shape (where the sweet spot sits), balance (head-heavy or head-light), core hardness, face material and, last, weight. A 5 to 10 g gap in weight matters less than a change of shape or balance. Round, head-light, soft rackets suit beginners and sore arms; diamond, head-heavy, hard rackets suit advanced attacking players.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">About you</h2><p class="muted" style="margin-top:0">So the comparison can say which racket fits you, not just which is "better".</p>
{_bq2("rc", "lvl", "Your level", [("beg", "Beginner"), ("int", "Improving / intermediate"), ("adv", "Advanced")], "int")}
{_bq2("rc", "style", "How you like to play", [("ctrl", "Control and consistency"), ("both", "A bit of both"), ("pow", "Power and smashes")], "both")}
{_bq2("rc", "arm", "Your arm", [("ok", "No problems"), ("sore", "Sore elbow or shoulder")], "ok")}</div>
<div class="rc-grid">{_rc_side("a", "round", "soft", "glass")}{_rc_side("b", "diamond", "hard", "carbon")}</div>
<aside class="result" id="rc-out" aria-live="polite" style="position:static;margin-top:18px"><span class="pill" id="rc-pill"></span><h2 id="rc-h" style="margin-top:10px"></h2><p id="rc-p"></p>
<div class="tbl rc-tbl"><table><thead><tr><th>Spec</th><th id="rc-ha">A</th><th id="rc-hb">B</th><th>What the difference means</th></tr></thead><tbody id="rc-rows"></tbody></table></div>
<p id="rc-t" class="wr-src"></p><div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="rc-copy">Copy comparison</button></div></aside>
<p class="muted" style="margin-top:12px">Your choices stay on this device only. The tool works from the specs you enter, not from brand claims, so it is only as good as the numbers on the product page.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which specs matter most when you compare padel rackets?</h2><p class="muted">From biggest to smallest effect on how a racket plays.</p></div>
<div class="grid">{_cards([
    ("Shape", "Decides where the sweet spot sits. Round: low and wide, the most forgiving. Teardrop: a little higher, a mix of control and power. Diamond: high and small, the most power when you hit it right."),
    ("Balance", "How the weight is spread. Above about 265 mm feels head-heavy: more weight behind smashes, slower at the net. Below about 255 mm feels quick and easy. Compare balance numbers from the same brand or shop, because they measure differently."),
    ("Core", "Soft foam holds the ball longer: easy power at slow speeds and kinder on the arm. Hard foam gives the ball back faster, but only if you swing fast. Medium suits most club players."),
    ("Face", "Fibreglass is softer and more forgiving. Carbon is stiffer and more precise, and passes on more vibration. Higher carbon numbers (12K, 18K) are about weave and feel, not automatic quality."),
    ("Weight", "Matters, but least of the five. Rackets from the same model can differ by a few grams, so don't choose on a 5 g gap. A 15 to 20 g gap you will feel."),
    ("Thickness and surface", "Almost all adult rackets are 38 mm thick. A rough or sandy surface adds a little grip for spin. Neither changes much compared with the five above."),
], pill="Spec")}</div>
<p class="muted" style="margin-top:14px">Only comparing weight and balance? The <a href="{href("racket-balance.html")}">weight and balance decoder</a> draws both rackets to scale. Not sure what specs you need at all? Start with the <a href="{href("racket-finder.html")}">racket finder</a>. Carbon numbers explained: <a href="{href("padel-racket-materials.html")}">racket materials</a>.</p></div></section>
{AD.format("rc-mid")}
<section><div class="wrap"><div class="sh"><h2>Common padel racket comparisons</h2></div>
<div class="tbl"><table><thead><tr><th>Choice</th><th>Pick the first if</th><th>Pick the second if</th></tr></thead><tbody>
<tr><td>Round vs diamond</td><td>You are learning, play from the back a lot or want fewer mishits</td><td>You smash well, play the left side and hit the sweet spot most of the time</td></tr>
<tr><td>Round vs teardrop</td><td>Control matters most, or your arm gets sore</td><td>You want a little more power without losing much forgiveness</td></tr>
<tr><td>Teardrop vs diamond</td><td>You want one racket for all shots</td><td>Overheads win you most points</td></tr>
<tr><td>Soft vs hard core</td><td>You swing at medium speed, or have a sore arm</td><td>You swing fast and want a crisp, direct feel</td></tr>
<tr><td>Fibreglass vs carbon</td><td>You want comfort and an easy, lively feel</td><td>You want precision and a stiffer, more solid feel</td></tr>
<tr><td>Light vs heavy (about 345 vs 370 g)</td><td>You want speed at the net and less arm load</td><td>You want stability and weight behind the ball</td></tr>
<tr><td>Old model vs new model</td><td>The specs are the same and the old one is cheaper</td><td>The shape, balance or core actually changed</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Can you try before you buy? Many clubs and shops lend or rent demo rackets. Play at least a few games with each, because the first five minutes with any new racket feel strange. Upgrading from a first racket? See <a href="{href("intermediate-padel-racket.html")}">intermediate rackets</a>. Arm problems? See <a href="{href("padel-elbow.html")}">padel elbow</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="aff-box"><h3>Compare real rackets by shape</h3><p>Shop pages list each racket's weight, balance, core and face. Open two in tabs and copy the specs into the comparison above.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: Padel USA "Stuck between two padel rackets? The five differences that actually change how they play" (26 Oct 2026: compare shape, balance, core, face, then weight; head-heavy above about 265 mm, quick below about 255 mm; compare numbers within one source; don't decide on a 5 g gap); Tienda Padel Point "Compare padel rackets by player type and level" and "Technical factors when choosing a padel racket model"; Playtomic and Tennis Warehouse "How to choose a padel racket" guides (shape, balance, core and face by level). FIP rules for racket size and thickness. Advice is general; no brand claims.</p></div></section>'''
rc_faq = [
    ("How do I compare two padel rackets?", "Compare the specs in order of how much they change the feel: shape first, then balance, core hardness, face material and weight. Use the numbers from the same shop or brand, and try both if you can."),
    ("What matters more in a padel racket: weight or balance?", "Balance usually changes the feel more than a small weight difference. A racket 10 mm more head-heavy feels heavier to swing than one 10 g heavier with the same balance."),
    ("Is a 5 g difference in padel rackets noticeable?", "Hardly. Rackets of the same model can vary by a few grams. Most players start to feel a difference at about 15 to 20 g."),
    ("Is a diamond or round padel racket better?", "Neither is better in general. Round is more forgiving and easier to control; diamond gives more power on smashes if you hit the high sweet spot. Beginners and players with sore arms usually do better with round."),
    ("Is a more expensive padel racket better?", "Not automatically. Price often follows carbon type and the brand's top model. A racket whose shape, balance and core fit your game will feel better than an expensive one that doesn't."),
    ("Can I compare balance numbers from different brands?", "Be careful. Brands and shops measure balance in slightly different ways, so compare numbers from the same source, or measure both rackets yourself the same way."),
]
page("compare-padel-rackets.html", "Compare Padel Rackets Side by Side: Free Tool",
     "Compare two padel rackets: enter shape, weight, balance, core and face and see what each difference feels like and which suits your level, style and arm.",
     rc, rc_faq, "Compare rackets")

# ---------- 2. PADEL FOOTWORK + SPLIT-STEP TRAINER ----------
fw_moves = [
    ("Split step", "A small hop onto both feet, landing just as an opponent hits the ball. You land balanced on the balls of your feet, feet a little wider than your shoulders, ready to push off in any direction."),
    ("Side shuffle", "Short sideways steps without crossing your feet, for balls a step or two away. Your shoulders stay facing the net, so you are ready to volley."),
    ("Crossover step", "For a ball further away, turn your hips and cross one leg over the other to cover ground fast, then go back to small steps before you hit."),
    ("Turn and run back for a lob", "Turn sideways and move back with side or crossover steps, never backwards on your heels. If the lob is good, keep turning and let it come off the back glass."),
    ("Small adjustment steps", "The last two or three steps before a shot are small. They set your distance to the ball so you can hit it in front of your body."),
    ("Recover", "After every shot, move back towards your best position at once: middle of your half, and level with your partner. Hit, then recover, every time."),
]
fw_mistakes = [
    ("No split step", "You are still moving, or flat-footed, when they hit. You start late and arrive late."),
    ("Watching your own shot", "Admiring the ball instead of recovering leaves a gap for the next one."),
    ("Rushing to the net", "Running in behind a weak ball gets you lobbed. Move forward when your shot gives you time."),
    ("Hitting off balance", "Arrive early, set your feet, then hit. A late, stretched shot usually goes up or into the net."),
    ("Recovering too wide", "Drifting to the side wall opens the middle. Recover to the middle of your half, not the edge."),
    ("Crossing feet at the net", "Crossing your legs while volleying makes you slow to change direction. Shuffle instead."),
]
fw = f'''<header class="hero"><div class="wrap"><h1>Padel footwork and the split step, with a reaction trainer.</h1>
<p class="lead">Good padel footwork is mostly small things: a split step as they hit, short steps to the ball and a quick recovery. Learn the six movements, check the common mistakes, then use the trainer: it cues your split step and flashes a direction to move, like a coach with a ball basket.</p>
{quick("The split step is a small hop onto both feet that lands just as your opponent hits the ball, so you are balanced and ready to move any way. After it, use short side shuffles for close balls, a crossover step for wide ones, turn sideways to go back for lobs, take small steps before you hit, and recover to the middle of your half after every shot.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="card" id="fwt">
<h2 style="font-size:1.4rem;margin-bottom:4px">Split-step reaction trainer</h2>
<p class="muted" style="margin-top:0">Stand in your ready position, in a room or on court. On "Split", hop. Then move two or three steps the way the arrow shows, shadow the shot and recover to the start. A beep helps if you can't watch the screen.</p>
{_bq2("fwt", "pace", "Pace", [("slow", "Slow: 5 to 7 s"), ("med", "Medium: 3.5 to 5 s"), ("fast", "Fast: 2.5 to 3.5 s")], "med")}
{_bq2("fwt", "len", "Length", [("60", "1 minute"), ("120", "2 minutes"), ("180", "3 minutes")], "60")}
{_bq2("fwt", "mode", "Directions", [("net", "At the net: left, right, lob"), ("back", "At the back: left, right, short, glass"), ("all", "All of them")], "net")}
{_bq2("fwt", "beep", "Sound", [("on", "Beep on split"), ("off", "Silent")], "on")}
<div class="fw-stage" id="fwt-stage" aria-live="assertive"><div class="fw-cue" id="fwt-cue">Ready</div><div class="fw-dir" id="fwt-dir">Press start</div></div>
<div class="fw-stats"><span class="pill b" id="fwt-time">1:00</span><span class="pill" id="fwt-reps">0 reps</span></div>
<div class="btns" style="margin-top:10px"><button class="btn lime" type="button" id="fwt-go">Start</button><button class="btn ghost" type="button" id="fwt-stop" disabled>Stop</button></div>
<p class="muted" style="margin-top:10px;font-size:.9rem">Clear the space around you first. Stop if anything hurts. Your last session length is saved on this device.</p>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>The six footwork movements in padel</h2></div>
<div class="grid">{_cards(fw_moves, pill="Move")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When do you split step in padel?</h2><p class="muted">Every time an opponent is about to hit, wherever you are.</p></div>
<div class="grid">
<div class="card"><h3>Timing</h3><p>Start the hop as they swing, so you land at the moment their racket hits the ball. Land too early and you are flat-footed again; too late and you are in the air when you need to move.</p></div>
<div class="card"><h3>Size</h3><p>Small. A few centimetres off the ground is enough. At the net it is often just a quick bounce on your toes, because the ball arrives fast.</p></div>
<div class="card"><h3>At the net</h3><p>Racket up in front, split as they hit, then one or two steps to the volley. See <a href="{href("padel-volley.html")}">how to volley</a>.</p></div>
<div class="card"><h3>At the back</h3><p>Split, read whether the ball will hit the back glass, and move early to leave space between you and the wall. See <a href="{href("padel-back-glass.html")}">playing off the back glass</a>.</p></div>
<div class="card"><h3>On the return</h3><p>Split as the server hits, then step in to the ball. See <a href="{href("padel-return-of-serve.html")}">how to return serve</a>.</p></div>
<div class="card"><h3>With your partner</h3><p>Move as a pair: forward together, back together. When one goes to the net, the other follows. See <a href="{href("positioning.html")}">where to stand</a>.</p></div>
</div></div></section>
{AD.format("fw-mid")}
<section><div class="wrap"><div class="sh"><h2>Common padel footwork mistakes</h2></div>
<div class="grid">{_cards(fw_mistakes)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel footwork drills</h2></div>
<div class="tbl"><table><thead><tr><th>Drill</th><th>How</th><th>Time</th></tr></thead><tbody>
<tr><td>Shadow split steps</td><td>Use the trainer above at the net setting, then the back setting. Racket in hand, full shadow swing on each rep.</td><td>3 x 1 min, 1 min rest</td></tr>
<tr><td>Cone shuffle</td><td>Two markers about 3 m apart along the service line. Shuffle between them without crossing your feet, touching each with your racket.</td><td>4 x 30 s</td></tr>
<tr><td>Lob turn-and-chase</td><td>From the net, a partner calls "lob". Turn sideways, move back three steps, shadow a bandeja, then move back in.</td><td>10 reps each side</td></tr>
<tr><td>Feed and recover</td><td>A partner feeds balls left and right. After each shot, recover to the middle of your half before the next feed.</td><td>2 x 20 balls</td></tr>
<tr><td>Split on every shot</td><td>In a normal rally game, your partner says "late" every time you are not landing as the other side hits.</td><td>One game</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Build a full session around these with the <a href="{href("drills.html")}">drills planner</a>, warm up first with the <a href="{href("warm-up.html")}">warm-up timer</a>, and plan the week with the <a href="{href("padel-training-plan.html")}">training plan generator</a>. Footwork also needs grip: worn or wrong soles slide. See <a href="{href("padel-shoes.html")}">padel shoes</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="aff-box"><h3>Shoes for quick feet</h3><p>Padel shoes with a herringbone or mixed sole grip the sandy turf when you split and push off. Running shoes don't.</p><ul class="aff-links"><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls for drills</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: The Padel School "The one padel skill you're ignoring: why footwork matters most" (split step timed to the opponent's contact, recover after every shot, arrive early and set your feet, small steps, don't cross feet, common mistakes), "Padel footwork: the key to agile movement" and "How to move your feet during a padel match"; Tienda Padel Point split-step guides (split step, initial reaction, split-step exercises, padel vs tennis split step, in 4 languages); USA Pickleball "The one footwork step every player needs to know: the split step". The trainer and drill times are our own.</p></div></section>'''
fw_faq = [
    ("What is a split step in padel?", "A small hop onto both feet that lands just as your opponent hits the ball. You land balanced on the balls of your feet, so you can push off quickly in any direction."),
    ("When should you split step in padel?", "Every time an opponent is about to hit: start the hop as they swing and land as the racket meets the ball. At the net it can be just a quick bounce on your toes."),
    ("How do you improve footwork in padel?", "Add a split step before every opponent's shot, use small steps to get to the ball, recover to the middle of your half after every shot, and practise with shadow drills and a feeder a few minutes each session."),
    ("Should you cross your feet in padel?", "Not for short movements: shuffle sideways instead, especially at the net. A crossover step is useful to cover a big distance, such as going back for a lob, before small steps into the shot."),
    ("How do you move back for a lob in padel?", "Turn sideways first, then move back with side or crossover steps. Don't backpedal on your heels. If the lob is too good, keep going and play it off the back glass."),
    ("Is footwork different in padel and tennis?", "Yes. The padel court is smaller and the walls give second chances, so steps are shorter, you split step more often, and you need to leave space for the ball off the glass."),
]
page("padel-footwork.html", "Padel Footwork and Split Step + Reaction Trainer",
     "Padel footwork made simple: the split step, side shuffle, crossover, lob turn and recovery, common mistakes, drills, and a free split-step reaction trainer.",
     fw, fw_faq, "Padel footwork")

# ---------- 3. PARTNER COMMUNICATION + MIDDLE BALL ----------
pc_calls = [
    ("\"Mine\" / \"Yo\"", "I'm taking it. Say it early and loud, before the ball crosses the net, not as you hit it."),
    ("\"Yours\" / \"Tuya\"", "You take it. Just as important as \"mine\": it stops both of you leaving the ball."),
    ("\"Switch\" / \"Cambio\"", "A lob went over one of you and the other is running to get it. Swap sides and keep going."),
    ("\"Glass\" / \"Pared\"", "Let it bounce and come off the wall: you will have more time after the glass."),
    ("\"Out\" / \"Leave it\"", "The ball will hit the back or side glass or fence directly without bouncing. Don't touch it: it's your point."),
    ("\"Up\" / \"Back\"", "Move forward to the net together, or go back together. Pairs that move as one leave fewer gaps."),
    ("\"Middle\"", "Before the point: the next ball goes down the middle. Two players reaching for it often clash or both leave it."),
    ("\"Next one\" / \"Good try\"", "After a mistake, a short positive word. Give information, not emotion."),
]
pc = f'''<header class="hero"><div class="wrap"><h1>Padel partner communication: what to say and who takes the middle ball.</h1>
<p class="lead">Most doubles mix-ups happen down the middle, between the two of you. Use the decider to settle whose ball it is in each situation, learn the eight calls good pairs use, and agree a few rules before the match.</p>
{quick("In padel, call the ball early: \"mine\" or \"yours\" before it crosses the net. If both players are right-handed, the middle usually belongs to the left-side player, because it is their forehand, including lobs down the middle. With a left-hander on the right side, both forehands meet in the middle, so agree one rule before you play, such as the player further forward or the one who called first.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="pcd">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Who takes the middle ball?</h2><p class="muted" style="margin-top:0">Pick your pair and the ball. The answer is a rule of thumb many pairs use; your own agreed rule always comes first.</p>
{_bq2("pcd", "hands", "Your pair", [("rr", "Both right-handed"), ("ll", "Both left-handed"), ("lr", "Lefty on the right side"), ("ll2", "Lefty on the left side")], "rr")}
{_bq2("pcd", "ball", "The ball", [("low", "Low ball / volley down the middle"), ("lob", "Lob over the middle"), ("glass", "Ball off the back glass, middle"), ("serve", "Return down the middle (you are serving)")], "low")}
{_bq2("pcd", "pos", "Where you both are", [("net", "Both at the net"), ("back", "Both at the back"), ("split", "One up, one back")], "net")}</div>
<aside class="result" id="pcd-out" aria-live="polite"><span class="pill" id="pcd-pill"></span><h2 id="pcd-h" style="margin-top:10px"></h2><p id="pcd-p"></p><p id="pcd-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel calls: what to say to your partner</h2><p class="muted">Short words, said early. Many clubs also use the Spanish ones.</p></div>
<div class="grid">{_cards(pc_calls)}</div>
<p class="muted" style="margin-top:14px">Why "out" matters: a ball that hits your back or side glass or fence before it bounces is out, so letting it go wins the point. Check the exact rule in <a href="{href("wall-rules.html")}">wall and fence rules</a>.</p></div></section>
{AD.format("pc-mid")}
<section><div class="wrap"><div class="sh"><h2>What to agree before the match</h2></div>
<div class="grid">
<div class="card"><h3>Who covers the middle</h3><p>Forehand takes it is the usual default. If you are a left and right-hander pair, decide whose it is when both forehands meet: see the decider above.</p></div>
<div class="card"><h3>Who takes overheads</h3><p>Lobs down the middle usually go to the player with the more reliable overhead, often the left-side player. See <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora</a>.</p></div>
<div class="card"><h3>What happens when you are lobbed</h3><p>Agree that when one of you is lobbed, the partner runs and calls "switch" if needed, and you both go back together.</p></div>
<div class="card"><h3>Default plays</h3><p>For example: short ball, attack the middle; under pressure, lob. Simple patterns stop you both guessing.</p></div>
<div class="card"><h3>Serve signals</h3><p>Some pairs use a hand signal behind the back: where the serve goes, and whether the net player will cross. Keep it simple.</p></div>
<div class="card"><h3>Which side each plays</h3><p>Not sure who goes left? Take the <a href="{href("which-side-padel.html")}">left or right side quiz</a> together.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Communication habits of good padel pairs</h2></div>
<div class="tbl"><table><thead><tr><th>Do</th><th>Avoid</th></tr></thead><tbody>
<tr><td>Call early, before the ball crosses the net</td><td>Calling as you hit, or after</td></tr>
<tr><td>Tell your partner where the opponents are ("one up!")</td><td>Silence for whole points</td></tr>
<tr><td>Give information: "high ball next time, let's lob"</td><td>Blame or coaching in the middle of a game</td></tr>
<tr><td>Talk at the change of ends: one thing to keep, one to change</td><td>Long tactical talks between every point</td></tr>
<tr><td>Show with your body and racket that you are going for it</td><td>Half-going for a ball, then pulling out</td></tr>
<tr><td>Short positive words after errors</td><td>Sighs, shrugs and rolled eyes</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Playing with someone new? Agree the middle, the overheads and what to do on a lob in the first minute of the warm-up. More on manners in <a href="{href("padel-etiquette.html")}">padel etiquette</a>, on where to stand in <a href="{href("positioning.html")}">positioning</a>, and on winning patterns in the <a href="{href("padel-tactics.html")}">tactics trainer</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: The Padel School "Padel doubles strategy: how to communicate and win as a team" (call early with mine or yours, call when switching, information not emotion, move forward and back together, agree roles and patterns before the match); HEAD "How to communicate in padel" (verbal and non-verbal signals, agree court coverage by hand preference, reassure your partner); Padel Browser "Left side vs right side in padel" (14 Sep 2026: middle lob is the left player's forehand, left-handers usually play the right so both forehands cover the middle, better overhead goes left); Red Bull "Padel etiquette: unwritten rules"; DUPR "Middle ball: who takes it and when?". The decider rules are general rules of thumb, not official rules.</p></div></section>'''
pc_faq = [
    ("Who takes the middle ball in padel?", "If both players are right-handed, usually the left-side player, because it is their forehand. With a left-hander on the right, both forehands meet in the middle, so agree a rule first, such as the player further forward or the player who called first."),
    ("Who takes the lob down the middle in padel?", "Usually the left-side player for two right-handers, because they can play it on the forehand side with a bandeja or smash. In other pairs, the player with the more reliable overhead."),
    ("What do padel players say to each other?", "Short calls: \"mine\" and \"yours\" to claim a ball, \"switch\" when you swap sides after a lob, \"glass\" to let the ball come off the wall, \"out\" for a ball that will hit the glass or fence without bouncing, and \"up\" or \"back\" to move together."),
    ("When should you call the ball in padel?", "Early, before the ball crosses the net. A late call makes both players hesitate, which is how middle balls get missed or rackets clash."),
    ("What does \"cambio\" mean in padel?", "It is Spanish for \"change\" or \"switch\". You call it when a lob goes over your partner and you run across to take it, so you both swap sides."),
    ("How do you talk to your padel partner after a mistake?", "Keep it short and positive, and give information rather than emotion, such as \"good try, next time lob\". Save bigger talks for the change of ends."),
]
page("padel-communication.html", "Who Takes the Middle Ball in Padel? Partner Calls",
     "Padel partner communication: who takes the middle ball and middle lobs, the 8 calls good pairs use (mine, yours, switch, glass), and a free middle-ball decider.",
     pc, pc_faq, "Partner communication")

DEMAND_PAGES += ["compare-padel-rackets.html", "padel-footwork.html", "padel-communication.html"]

# ---------- 4. PREMIER PADEL MEXICO MAJOR 2026 (Trends 27 Nov: "Mexico Major Premier Padel" rising) ----------
# Sources checked 27 Nov 2026: Red Bull (event page + 2026 calendar + 2026 FAQ: dates 23-29 Nov, QF-final on Red Bull TV, earlier rounds on Premier Padel YouTube, Major = 2,000 pts, Finals Barcelona 10-13 Dec);
# padelspeak (dates, Acapulco, finals Sunday 29 Nov, 2,000 pts, Barcelona Finals next); 2025 champions: FIP (padelfip.com), Outlook India, Red Bull.
mx = f'''<header class="hero"><div class="wrap"><h1>Premier Padel Mexico Major 2026 in Acapulco.</h1>
<p class="lead">Dates, how to watch, what is at stake and who won last year. This is the last Major of the season and the last big chance to qualify for the Barcelona Finals.</p>
{quick("The GNP Mexico Major runs from <strong>Monday 23 to Sunday 29 November 2026</strong> in <strong>Acapulco, Mexico</strong>. The men's and women's finals are on <strong>Sunday 29 November</strong>. Quarter-finals to finals are live on <strong>Red Bull TV</strong>; earlier rounds are on Premier Padel's YouTube channel. Winners get 2,000 ranking points. Last year Coello and Tapia won the men's title, and Bea González and Claudia Fernández the women's.", "2026-11-27")}</div></header>
<section><div class="wrap"><div class="sh"><h2>Mexico Major 2026 at a glance</h2></div>
<div class="tbl"><table><tbody>
<tr><th>Dates</th><td>23 to 29 November 2026</td></tr>
<tr><th>Where</th><td>Acapulco, Guerrero, Mexico</td></tr>
<tr><th>Category</th><td>Major (the top tier of Premier Padel, four a season)</td></tr>
<tr><th>Ranking points for the winners</th><td>2,000</td></tr>
<tr><th>Finals day</th><td>Sunday 29 November 2026</td></tr>
<tr><th>Next on the tour</th><td>Premier Padel Finals, Barcelona, 10 to 13 December 2026</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Acapulco is on Mexico City time (UTC-6), so evening matches there are played overnight in Europe and in the early morning in the UK.</p></div></section>
{AD.format("mx-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How to watch the Mexico Major</h2></div>
<div class="grid">
<div class="card"><h3>Quarter-finals to finals</h3><p>Live on Red Bull TV, which covers every 2026 Premier Padel event from the quarter-finals on, for both the men's and women's draws. The app works on phones and smart TVs.</p></div>
<div class="card"><h3>Earlier rounds</h3><p>The rounds before the quarter-finals are streamed on Premier Padel's own YouTube channel.</p></div>
<div class="card"><h3>Not shown where you are?</h3><p>Red Bull TV's live stream is not available in every country. Where it is blocked, highlights are posted worldwide in English and Spanish after the event.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Who won the Mexico Major last year?</h2></div>
<div class="tbl"><table><thead><tr><th>Draw</th><th>2025 champions</th><th>Beat in the final</th></tr></thead><tbody>
<tr><td>Men</td><td>Arturo Coello and Agustín Tapia</td><td>Federico Chingotto and Ale Galán</td></tr>
<tr><td>Women</td><td>Bea González and Claudia Fernández</td><td>Gemma Triay and Delfina Brea</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">It was González and Fernández's first Major as a pair. Coello and Tapia's win in Acapulco sealed their place as the year-end world No. 1 pair.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why this week matters</h2></div>
<p>Only the top eight men's and top eight women's pairs of the season play the <strong>Premier Padel Finals in Barcelona (10 to 13 December)</strong>. As the last Major, Acapulco carries the most points of the closing weeks, so it can decide who makes it. See how the points work in <a href="{href("padel-rankings.html")}">padel rankings explained</a>, and how matches are scored, including the golden point, in <a href="{href("golden-point-star-point.html")}">golden point and star point</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: Red Bull (GNP Mexico Major event page, 2026 Premier Padel calendar and 2026 FAQ), padelspeak (Mexico Major 2026 guide), FIP and Outlook India (2025 finals). We will add the 2026 results after the finals.</p></div></section>'''
mx_faq = [
    ("When is the Mexico Major 2026?", "From 23 to 29 November 2026 in Acapulco. The men's and women's finals are on Sunday 29 November."),
    ("Where can I watch the Premier Padel Mexico Major?", "Quarter-finals, semi-finals and finals are live on Red Bull TV. Earlier rounds are on Premier Padel's YouTube channel. Red Bull TV's live stream is not available in every country."),
    ("Who won the Mexico Major 2025?", "Arturo Coello and Agustín Tapia won the men's title against Chingotto and Galán. Bea González and Claudia Fernández won the women's title against Gemma Triay and Delfina Brea."),
    ("How many points is a Premier Padel Major worth?", "2,000 ranking points for the winning pair, the most of any regular tour event."),
    ("What comes after the Mexico Major?", "The Premier Padel Finals in Barcelona, 10 to 13 December 2026, for the top eight pairs of the season."),
]
page("premier-padel-mexico-major.html", "Premier Padel Mexico Major 2026: Dates, How to Watch",
     "Premier Padel Mexico Major 2026 in Acapulco, 23-29 November: finals on Sunday 29 Nov, how to watch on Red Bull TV and YouTube, 2,000 points and last year's winners.",
     mx, mx_faq, "Mexico Major 2026")

DEMAND_PAGES += ["premier-padel-mexico-major.html"]
exec((ROOT / "demand10.py").read_text())
