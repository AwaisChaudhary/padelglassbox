# ---------------- DEMAND RUN 19 (28 Nov 2026): padel forehand guide + fault fixer, padel racket shapes + shape picker, lob defence merge ----------------
# Executed from demand15.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards).

# ---------- 1. PADEL FOREHAND ----------
pf = f'''<header class="hero"><div class="wrap"><h1>How to hit a padel forehand (and fix the one you have)</h1>
<p class="lead">The padel forehand is shorter and calmer than a tennis forehand. Learn the four steps, when to hit off the bounce or wait for the glass, and use the fault fixer to find out why your forehand goes into the net, flies long or comes late.</p>
{quick("To hit a padel forehand, take the racket back early with a short backswing, turn sideways so your weight can move from the back foot to the front foot, and meet the ball out in front of your body at about hip height. Push through the back of the ball with the face pointing at your target, and keep the finish short. If the ball bounces before the service line, play it off the bounce; if it bounces after the line, let it come off the back glass.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Forehand fault fixer</h2><p class="muted" style="margin-top:0">Pick what goes wrong and where you are when it happens.</p>
{_bq2("pf", "prob", "What goes wrong most?", [("net", "Into the net"), ("long", "Too long or into the glass"), ("late", "I am late or rushed"), ("ctrl", "No control, sprays wide"), ("weak", "No depth, sits up"), ("arm", "Sore arm or wrist")], "net")}
{_bq2("pf", "where", "Where are you when it happens?", [("bounce", "Off the bounce, back of court"), ("glass", "After the back glass"), ("mid", "Low ball, middle of court")], "bounce")}
{_bq2("pf", "bg", "Your background", [("new", "New to racket sports"), ("ten", "I played tennis"), ("pad", "Played padel a while")], "new")}
</div>
<aside class="result" id="pf-out" aria-live="polite"><span class="pill b">Your fix</span><h2 id="pf-h" style="margin-top:10px">Into the net</h2>
<p id="pf-p"></p><h3 style="margin-top:14px;font-size:1rem">Try this, in order</h3><ol id="pf-fix" class="tp-hab"></ol><dl class="spec" id="pf-spec"></dl><p id="pf-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="pf-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">The fixes follow LTA Padel and coaching advice listed at the bottom of the page. The matching of problems to fixes is our own.</p></div></section>
{AD.format("pf-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you hit a forehand in padel, step by step?</h2></div><div class="grid">{_cards([
    ("Prepare early, swing short", "Take the racket back as soon as you see the ball coming to your forehand. Padel needs little power, so a short backswing is enough, and it gives you more time to read the ball."),
    ("Turn sideways", "Turn your shoulders and stand side-on, so your weight can move from the back foot to the front foot. An open stance turns the shot into an arm-only hit."),
    ("Contact in front, at hip height", "Let the ball come to the side of your body and meet it out in front, at about hip height. Move your feet so you are not too close to the ball or reaching for it."),
    ("Push through, finish short", "Push through the back of the ball on a flat, front-to-back path, with the face pointing at your target. No big tennis follow-through over the shoulder."),
], pill="Step")}</div>
<p style="margin-top:12px">Grip: a continental grip works for every padel shot; some coaches let improving players turn the hand one bevel towards the forehand for drives from the back only. See <a href="{href("padel-grip.html")}">how to hold a padel racket</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Off the bounce or off the glass?</h2><p class="muted">The service line is your decision line.</p></div>
<div class="tbl"><table><thead><tr><th>The ball bounces</th><th>Play it</th><th>Why</th></tr></thead><tbody>
<tr><td>Before the service line</td><td>Straight off the bounce</td><td>It will not reach the back glass with enough pace to play after it</td></tr>
<tr><td>After the service line</td><td>Let it hit the back glass, then play it</td><td>The glass slows it down and gives you more time and a better contact point</td></tr>
<tr><td>Slow ball, any depth</td><td>Usually off the bounce</td><td>You have time to set up</td></tr>
<tr><td>Fast ball, deep</td><td>Off the glass</td><td>Let the wall take the pace</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Drill, "yellow card, red card" (LTA Padel): play normal points. If a ball bounces past the service line and you hit it before the glass, that is a yellow card. A second one in the same rally is a red card and you lose the point. More on the glass: <a href="{href("padel-back-glass.html")}">playing off the back glass</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel forehand vs tennis forehand</h2></div>
<div class="tbl"><table><thead><tr><th></th><th>Tennis forehand</th><th>Padel forehand</th></tr></thead><tbody>
<tr><td>Backswing</td><td>Big loop</td><td>Short, racket back early</td></tr>
<tr><td>Contact height</td><td>Often around the waist to chest, with topspin</td><td>About hip height, flatter or with a little slice</td></tr>
<tr><td>Finish</td><td>Over the shoulder</td><td>Short, towards the target</td></tr>
<tr><td>Main aim</td><td>Pace and depth to win the point</td><td>Control and placement: keep it low and away from the net pair</td></tr>
<tr><td>Wrist</td><td>Often brushes up for topspin</td><td>Firmer and quieter</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Coming from tennis? The <a href="{href("padel-racket-for-tennis-players.html")}">racket picker for tennis players</a> lists the habits that cost the most padel points.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What are the most common padel forehand mistakes?</h2></div><div class="grid">{_cards([
    ("Hitting too hard", "The forehand feels like your strongest shot, so you swing harder. Most forehand errors are pace errors: aim for control and vary the pace."),
    ("Too much slice", "Chopping down on the ball makes it float or die in the net. Push through the ball so slices stay low off the glass."),
    ("Late preparation", "If the racket goes back only when the ball arrives, you rush the finish. Get it back as soon as you know it is a forehand."),
    ("Standing still", "Not turning and not moving the feet leaves you too close or too far. Take small steps until the ball is at the side of your body."),
], pill="Mistake")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What about the backhand?</h2></div>
<p>The padel backhand works on the same ideas: racket back early, short backswing, turn sideways, contact in front, push through towards the target. Most players hit it one-handed with the continental grip, which also makes it easier to play off the glass and at the net. If a ball is high on your backhand side, it is often a chance to play a <a href="{href("bandeja-vs-vibora.html")}">bandeja</a> or a <a href="{href("padel-volley.html")}">volley</a> instead.</p>
<p style="margin-top:12px">Next steps: <a href="{href("padel-lob.html")}">the lob</a>, <a href="{href("padel-chiquita.html")}">the chiquita</a>, <a href="{href("padel-return-of-serve.html")}">return of serve</a>, <a href="{href("padel-solo-practice.html")}">solo practice</a> and the full <a href="{href("fix-my-padel.html")}">problem fixer</a>.</p>
<p style="margin-top:12px">Full guide with a one- vs two-handed table and a fault fixer: <a href="{href("padel-backhand.html")}">how to hit a padel backhand</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: LTA Padel "How to play padel forehands and backhands" (early preparation, short backswing, push-through motion, contact in front of the body, face to target, service line as the decision line, "yellow card, red card" drill); The Padel School "The Padel Forehand" (take the racket back early, sideways feet with weight back to front, horizontal swing, hip-height contact, open-stance error) and "The Padel Forehand Biggest Mistakes" (too much slice, distance from the ball, not turning, hitting too hard). Grip advice from our <a href="{href("padel-grip.html")}">grip guide</a>. Written in our own words.</p></div></section>'''
pf_faq = [
    ("How do you hit a forehand in padel?", "Take the racket back early with a short backswing, turn sideways, meet the ball in front of you at about hip height and push through it towards your target with a short finish."),
    ("What grip do you use for a padel forehand?", "The continental grip works for every padel shot. Some coaches let improving players turn the hand slightly towards an eastern forehand grip for drives from the back, but never at the net."),
    ("Why does my padel forehand go into the net?", "Usually you chop down with too much slice, let the ball drop too low, or stand too close. Push through the back of the ball and meet it in front at about hip height."),
    ("Should I hit the forehand before or after the glass?", "If the ball bounces before the service line, play it off the bounce. If it bounces after the service line, let it hit the back glass first."),
    ("Is a padel forehand like a tennis forehand?", "No. It uses a shorter backswing, a flatter path, a short finish and much less pace. Placement and keeping the ball low matter more than power."),
    ("How hard should I hit a padel forehand?", "Less hard than you think. Most forehand errors come from overhitting. Control the pace and aim low, cross-court or at the feet of the net player."),
]
page("padel-forehand.html", "Padel Forehand: How to Hit It + Free Forehand Fault Fixer",
     "How to hit a padel forehand in 4 steps, when to play it off the bounce or the glass, padel vs tennis forehand, common mistakes and a free fault fixer.",
     pf, pf_faq, "Padel forehand")

# ---------- 2. PADEL RACKET SHAPES ----------
_RS_PATH = {
    "round": '<ellipse cx="60" cy="74" rx="47" ry="57"/>',
    "teardrop": '<path d="M60 16C104 16 110 62 101 92C93 118 77 132 60 134C43 132 27 118 19 92C10 62 16 16 60 16Z"/>',
    "diamond": '<path d="M60 16C88 16 104 30 107 52L96 104C88 124 73 133 60 134C47 133 32 124 24 104L13 52C16 30 32 16 60 16Z"/>',
}
_RS_SS = {"round": (60, 78, 26, 30), "teardrop": (60, 66, 22, 24), "diamond": (60, 50, 16, 17)}
def _rs_svg(k, name):
    cx, cy, rx, ry = _RS_SS[k]
    holes = "".join(f'<circle cx="{x}" cy="{y}" r="2.2"/>' for x in range(36, 90, 12) for y in range(36, 116, 12) if (x - 60) ** 2 / 40 ** 2 + (y - 75) ** 2 / 50 ** 2 < 1)
    return f'''<svg viewBox="0 0 120 196" width="120" height="196" role="img" aria-label="{name} padel racket with its sweet spot marked" style="display:block;margin:0 auto 8px">
<g fill="#16306e" stroke="#9fb7ff" stroke-width="3">{_RS_PATH[k]}</g>
<rect x="53" y="132" width="14" height="56" rx="5" fill="#0b1530" stroke="#9fb7ff" stroke-width="2"/>
<g fill="#0b1530">{holes}</g>
<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="rgba(232,248,74,.35)" stroke="#e8f84a" stroke-width="2" stroke-dasharray="4 3"/>
</svg>'''
rs_shapes = "".join(f'<div class="card" style="text-align:center">{_rs_svg(k, n)}<h3>{n}</h3><p>{t}</p></div>' for k, n, t in (
    ("round", "Round", "Big sweet spot in the middle, low balance. The most control and the most forgiving."),
    ("teardrop", "Teardrop", "Medium sweet spot a little higher, medium balance. A mix of control and power."),
    ("diamond", "Diamond", "Small sweet spot near the top, high balance. The most power, the least forgiving."),
))
rs = f'''<header class="hero"><div class="wrap"><h1>Padel racket shapes: round, teardrop or diamond?</h1>
<p class="lead">The shape of a padel racket decides where the sweet spot sits and where the weight is, and that changes control, power and how kind it is to your arm. See the three shapes to scale, compare them side by side, and answer five questions to find the shape that suits you.</p>
{quick("Round padel rackets have a large sweet spot in the middle and a low balance, so they give the most control and suit beginners and defensive players. Diamond rackets have a small sweet spot near the top and a high balance, so they give the most power and suit experienced attacking players. Teardrop rackets sit in between and suit most improving and all-round players. If your elbow or shoulder gets sore, stay with round or a low-balance teardrop.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="grid">{rs_shapes}</div>
<p class="muted" style="margin-top:10px">Our own drawings. The yellow dashed area shows roughly where the sweet spot is on each shape.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="quiz">
<div class="card">
<h2 style="font-size:1.3rem;margin-bottom:4px">Which racket shape suits me?</h2><p class="muted" style="margin-top:0">Five quick questions.</p>
{_bq2("rsh", "lvl", "How long have you played padel?", [("0", "Under 6 months"), ("1", "6 months to 2 years"), ("2", "Over 2 years, or I compete")], "0")}
{_bq2("rsh", "sty", "How do you like to win points?", [("0", "Steady: few errors, long rallies"), ("1", "A bit of both"), ("2", "Attack: smashes and winners")], "1")}
{_bq2("rsh", "fq", "How often do you play?", [("0", "Once a week or less"), ("1", "2 to 3 times a week"), ("2", "4 times or more")], "0")}
{_bq2("rsh", "side", "Which side do you play? (right-hander)", [("0", "Right (drive) side"), ("1", "Not sure or both"), ("2", "Left (revés) side")], "1")}
{_bq2("rsh", "arm", "Any elbow, wrist or shoulder pain?", [("0", "No"), ("1", "Sometimes"), ("2", "Yes, often")], "0")}
</div>
<aside class="result" id="rsh-out" aria-live="polite"><span class="pill b">Your shape</span><h2 id="rsh-h" style="margin-top:10px">Round</h2>
<div class="cp-scale" aria-hidden="true"><i id="rsh-dot"></i></div><div class="cp-lab"><span>Round</span><span>Teardrop</span><span>Diamond</span></div>
<p id="rsh-p"></p><dl class="spec" id="rsh-spec"></dl><p id="rsh-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="rsh-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">Level and style count most. Arm pain caps the result at a low-balance teardrop. The scoring is our own; the balance and weight ranges come from the sources below.</p></div></section>
{AD.format("rsh-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Round vs teardrop vs diamond at a glance</h2></div>
<div class="tbl"><table><thead><tr><th></th><th>Round</th><th>Teardrop</th><th>Diamond</th></tr></thead><tbody>
<tr><td>Sweet spot</td><td>Large, in the centre</td><td>Medium, a little above centre</td><td>Small, near the top</td></tr>
<tr><td>Balance</td><td>Low (head-light), about 250 to 260 mm</td><td>Medium, about 265 to 270 mm</td><td>High (head-heavy), about 270 to 280 mm or more</td></tr>
<tr><td>Control</td><td>Most</td><td>Good</td><td>Least</td></tr>
<tr><td>Power</td><td>Least</td><td>Medium to high</td><td>Most</td></tr>
<tr><td>Forgiveness on mis-hits</td><td>High</td><td>Medium</td><td>Low</td></tr>
<tr><td>Easy on the arm</td><td>Yes</td><td>Mostly, if the balance is not high</td><td>Least: more strain for untrained arms</td></tr>
<tr><td>Usually suits</td><td>Beginners, defensive and steady players</td><td>Improving and all-round players</td><td>Experienced attackers, often on the left side</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Balance is measured from the bottom of the handle. Ranges are from the Tennis Warehouse racket guide; brands measure slightly differently, so treat them as a guide. Check any racket's numbers with the <a href="{href("racket-balance.html")}">balance decoder</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Does shape matter more than weight?</h2></div>
<p>Shape, balance and weight work together. Most rackets weigh about 350 to 380 g; HEAD says beginners and intermediates usually prefer about 340 to 360 g and tournament players about 360 to 375 g. A light diamond can feel easier than a heavy round racket, and a teardrop with a low balance plays closer to a round one. Pick the shape for your game, then the weight for your body: the <a href="{href("padel-racket-weight.html")}">racket weight calculator</a> gives a number in grams.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When should you change racket shape?</h2></div><div class="grid">{_cards([
    ("Round to teardrop", "When you hit cleanly in the middle of the face most of the time, play a few times a week and want more depth on overheads."),
    ("Teardrop to diamond", "When you finish most points at the net with smashes and bandejas, hit the sweet spot reliably and have no arm pain."),
    ("Back to round", "If your elbow or shoulder starts to hurt, or you miss more than you win with a head-heavy racket, go back to a lower balance."),
    ("Try before you buy", "Many clubs rent or demo rackets. Play a full session with a new shape before you spend; the first few games always feel strange."),
], pill="Change")}</div>
<p style="margin-top:12px">Not sure about your level? Try the <a href="{href("level-calculator.html")}">level calculator</a>. Two rackets in mind? <a href="{href("compare-padel-rackets.html")}">Compare them side by side</a>. Want the full spec? Use the <a href="{href("racket-finder.html")}">racket finder</a> or the <a href="{href("control-vs-power-padel-racket.html")}">control vs power test</a>.</p></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop padel rackets by shape</h3><p>Filter by shape first, then check the weight and balance in the product details.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond rackets</a></li><li><a href="{go("padel-black-friday-rackets")}" {AFF_ATTR}>Black Friday racket deals</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: Playtomic "Different padel racket shapes" (8 Apr 2025, edited 8 May 2025: sweet spot position and who each shape suits); HEAD "How to choose a padel racquet" (shape and sweet spot, low/medium/high balance by shape, 340 to 360 g and 360 to 375 g weight bands); Tennis Warehouse "How to choose a padel racket" (balance ranges in mm by shape, forgiveness, arm strain with head-heavy and diamond rackets, adult weights 350 to 380 g); Wilson "How to choose a padel racquet" (updated 12 Sep 2026: round control, teardrop balance of both, diamond power with higher balance). All four agree on the round-control, diamond-power pattern. Written in our own words; we name no models.</p></div></section>'''
rs_faq = [
    ("Which padel racket shape is best for beginners?", "Round. It has the biggest sweet spot in the middle of the face and a low balance, so mis-hits still go over and it is easy on the arm."),
    ("What is the difference between round, teardrop and diamond padel rackets?", "Round gives the most control with a big central sweet spot. Diamond gives the most power with a small sweet spot near the top. Teardrop is in between."),
    ("Is a teardrop padel racket good for intermediate players?", "Yes, it is the usual next step for improving and all-round players who want a little more power without losing much control."),
    ("Is a diamond padel racket bad for tennis elbow?", "It carries more risk. Diamond rackets are usually head-heavy, and racket guides warn that a high balance can strain the elbow in untrained arms. Stay round or low-balance teardrop if you have pain, and see a doctor or physio if it lasts."),
    ("What balance does a round padel racket have?", "Usually low, about 250 to 260 mm from the bottom of the handle. Teardrops are about 265 to 270 mm and diamonds about 270 to 280 mm or more."),
    ("Do professionals use diamond rackets?", "Many attacking pros do, but plenty use teardrop or even round rackets. Shape is a personal choice, not a sign of level."),
]
page("padel-racket-shapes.html", "Padel Racket Shapes: Round vs Teardrop vs Diamond + Picker",
     "Padel racket shapes compared: round vs teardrop vs diamond sweet spot, balance in mm, control, power and arm comfort, drawn to scale, with a free shape picker.",
     rs, rs_faq, "Racket shapes")

DEMAND_PAGES += ["padel-forehand.html", "padel-racket-shapes.html"]
exec((ROOT / "demand17.py").read_text())
