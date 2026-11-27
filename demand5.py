# ---------------- DEMAND RUN 8 (27 Nov 2026): padel lob guide + lob/answer pickers, overgrip change calculator ----------------
# Executed from demand4.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2).

# ---------- 1. PADEL LOB: HOW TO HIT IT + LOB PICKER + 'FACING A LOB' PICKER ----------
lb_steps = [
    ("1", "Get under the ball", "Prepare like any groundstroke, but bend your knees and get low so you meet the ball below its middle."),
    ("2", "Open the racket face", "Tilt the face up a little more than for a drive. The open face gives height, not a big swing."),
    ("3", "Swing low to high", "Move the racket up through the ball and push up with your legs. Do not jump or lift your whole body."),
    ("4", "Finish high", "End with the racket above your head, pointing where you want the ball to go. A high finish gives a deep lob."),
]
lb_step_html = "".join(f'<div class="card"><span class="pill b">Step {a}</span><h3 style="margin-top:10px">{e(b)}</h3><p>{e(c)}</p></div>' for a, b, c in lb_steps)
lb_err = [
    ("Lobbing off balance", "A lob hit while stretched or running usually lands short. When you are in trouble, a higher, safer lob is better than a fast one."),
    ("Lifting the whole body", "Jumping up for height makes the ball fly long. Bend the knees, stay down and let the legs push up."),
    ("Too short", "A lob that lands before the service line is an easy smash. Aim past the service line."),
    ("Too flat", "A low lob is easy to intercept and bounces hard off the back glass, giving your opponents an easy ball."),
    ("Always down the line", "Cross-court is longer, so you have more room for error. Use down the line as a surprise."),
]
lb_err_html = "".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in lb_err)
lb = f'''<header class="hero"><div class="wrap"><h1>How to hit a lob in padel, and what to do when you face one.</h1>
<p class="lead">The lob is the shot that wins the net back. Here is how to hit it, where to aim, a lob picker that tells you which lob to play in your situation, and a second picker for the shot to hit when the lob comes at you.</p>
{quick("To hit a padel lob, get low, open the racket face and swing from low to high with your legs, finishing with the racket above your head. Aim for the ball to bounce past the service line but before the back glass, and play it cross-court for more margin. A good lob pushes the net pair back and gives your team time to take the net.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="lbp">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Which lob should I play?</h2><p class="muted" style="margin-top:0">Three quick questions about the ball you are hitting.</p>
{_bq2("lbp", "opp", "Where are your opponents?", [("net", "Both at the net"), ("mid", "One at the net, one back"), ("back", "Both at the back")], "net")}
{_bq2("lbp", "bal", "How is your balance?", [("set", "Set, with time"), ("rush", "Rushed or stretched"), ("glass", "Playing it off the back glass")], "set")}
{_bq2("lbp", "opp2", "How tall and fast are they at the net?", [("tall", "Tall or quick smashers"), ("avg", "Average"), ("short", "Shorter or slow to move back")], "avg")}</div>
<aside class="result" id="lbp-out" aria-live="polite"><h2 id="lbp-h"></h2><p id="lbp-p"></p><p id="lbp-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Where should a padel lob land?</h2><p class="muted">The target zone, as LTA Padel coaches it.</p></div>
<div class="grid">
<div class="card"><h3>Past the service line</h3><p>The ball should bounce between the service line and the back glass. That pushes the net pair all the way back and makes a strong smash hard.</p></div>
<div class="card"><h3>Before the back glass</h3><p>If it hits the back glass without bouncing, it is out. Land it short of the glass and let it come off the wall slowly.</p></div>
<div class="card"><h3>High enough</h3><p>A high lob clears the players' reach and loses speed off the glass, so it stays close to the wall and is hard to play.</p></div>
<div class="card"><h3>Cross-court first</h3><p>The diagonal is the longest line on the court, so a cross-court lob has more room to land in. See the court sizes in <a href="{href("court-dimensions.html")}">court dimensions</a>.</p></div>
</div></div></section>
{AD.format("lb-mid")}
<section><div class="wrap"><div class="sh"><h2>How do you hit a lob in padel?</h2><p class="muted">Four steps. Use a continental grip, as in our <a href="{href("padel-grip.html")}">grip guide</a>.</p></div>
<div class="grid">{lb_step_html}</div>
<p class="muted" style="margin-top:12px">Practise it: balance the ball on your racket, drop it and tap it up, then tap it up in rallies with a partner before you try full lobs. Then play "two up, two back": one pair at the net, one at the back, first to 10 points, swap every two points. More ideas in the <a href="{href("drills.html")}">drills planner</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Common lob mistakes</h2></div><div class="grid">{lb_err_html}</div></div></section>
<section><div class="wrap quiz" id="lbd">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Facing a lob: which shot do I play?</h2><p class="muted" style="margin-top:0">Turn sideways as soon as you see your opponent get under the ball, then pick your shot.</p>
{_bq2("lbd", "dep", "How deep is the lob?", [("short", "Short, near the service line"), ("mid", "Middle"), ("deep", "Deep, over my head")], "mid")}
{_bq2("lbd", "side", "Which side is it on? (right-hander)", [("fh", "Forehand side"), ("bh", "Backhand side")], "fh")}</div>
<aside class="result" id="lbd-out" aria-live="polite"><h2 id="lbd-h"></h2><p id="lbd-p"></p><p id="lbd-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>When should you lob in padel?</h2></div><div class="grid">
<div class="card"><h3>When both opponents are at the net</h3><p>The lob is the main way to move them back so your pair can take the net. Learn the rest of the plan in <a href="{href("padel-tactics.html")}">padel tactics</a>.</p></div>
<div class="card"><h3>When you need time</h3><p>A high defensive lob buys time to get back into position after a hard ball. See <a href="{href("positioning.html")}">where to stand</a>.</p></div>
<div class="card"><h3>Against tired or slow players</h3><p>Lobs make the net pair turn and run back again and again. Over a match, that tires them out.</p></div>
<div class="card"><h3>Not when they are both back</h3><p>If both opponents are already at the back, a lob just gives them the net. Play a low ball or a <a href="{href("padel-chiquita.html")}">chiquita</a> at their feet instead. See <a href="{href("shots.html")}">padel shots</a>.</p></div>
</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: LTA Padel "Tips to play and improve padel lobs" (technique, target past the service line and before the back glass, height, cross-court margin, the two up two back drill); The Padel School "The Padel Lob" (low preparation, high finish, errors: off balance and lifting the body) and "How to deal with lobs" (recognise early, turn sideways, shot by depth and side). Advice in our own words.</p></div></section>'''
lb_faq = [
    ("How do you hit a good lob in padel?", "Get low, open the racket face and swing from low to high, pushing up with your legs and finishing with the racket above your head. Aim past the service line and before the back glass."),
    ("Where should a padel lob land?", "Between the service line and the back glass on your opponents' side. Cross-court gives you the most room."),
    ("Is the lob an attacking or defensive shot?", "Both. A high, safe lob defends and buys time. A lower, faster lob over a net player who is too close can win the point or the net."),
    ("Should I lob cross-court or down the line?", "Mostly cross-court, because the diagonal is longer and gives more margin. Down the line works as a surprise."),
    ("What do you do against a lob in padel?", "Turn sideways early and move back. Short lobs can be smashed or hit with a víbora; middle lobs suit a bandeja or víbora; deep lobs are often best let past onto the back glass and played from there."),
    ("Why do my lobs go out?", "Usually you lift your whole body, swing too hard, or hit while off balance. Stay low, use your legs, slow the swing and aim higher rather than longer."),
]
page("padel-lob.html", "How to Hit a Lob in Padel + Lob Picker and Lob Answer Tool | Padel Glass Box",
     "How to hit a padel lob step by step: where it should land, common mistakes, a picker for which lob to play, and how to answer a lob from your opponents.",
     lb, lb_faq, "Padel lob")

# ---------- 2. PADEL OVERGRIP: WHEN TO CHANGE IT (CALCULATOR) ----------
og_signs = [
    ("Slippery when dry", "The surface feels smooth or shiny even with dry hands."),
    ("Hand slides on volleys", "The racket turns or slips in your hand on hard balls."),
    ("Stays damp", "It is still wet between points or the next day."),
    ("Torn or loose", "Gaps, tears, or the top edge coming off the tape."),
    ("Dark, stained or smelly", "Sweat stains and smell come from dirt and bacteria."),
    ("Thinner than before", "It feels flat and hard, with less cushion."),
]
og_sign_html = '<ul class="check og-signs">' + "".join(f'<li><label><input type="checkbox" data-ogs="1"><span><b>{e(a)}.</b> {e(b)}</span></label></li>' for a, b in og_signs) + "</ul>"
og = f'''<header class="hero"><div class="wrap"><h1>How often should you change your padel overgrip?</h1>
<p class="lead">A fresh overgrip stops the racket turning in your hand and costs less than a can of balls. Use the calculator to see how often to change yours, how many you need a year and what it costs, then check the signs that it is worn out.</p>
{quick("Change your padel overgrip about every 8 to 12 hours of play, which is roughly once a week if you play 2 or 3 times a week. Change it sooner if it feels slippery when dry, stays damp or tears. Heavy sweat, heat and humidity can halve its life, and competitive players often fit a new one every 2 or 3 matches or before each match. Even if you play rarely, change it at least every two months.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap gen" id="ogc">
<div class="gen-main"><div class="card">
<h2 style="font-size:1.6rem">Overgrip change calculator</h2>
<p class="muted" style="margin-top:0">An estimate from shop and maker guidance. Your hands decide in the end: use the checklist below too.</p>
<div class="gen-nums"><div class="q"><h3><label for="og-n">Sessions per week</label></h3><input class="search" id="og-n" type="number" min="0.25" max="14" step="0.5" value="2" inputmode="decimal"></div>
<div class="q"><h3><label for="og-len">Session length</label></h3><select class="search" id="og-len"><option value="1">60 min</option><option value="1.5" selected>90 min</option><option value="2">120 min</option></select></div></div>
{_bq2("og", "sweat", "How much do your hands sweat?", [("1.2", "Hardly"), ("1", "Normal"), ("0.6", "A lot")], "1")}
{_bq2("og", "clim", "Where do you play?", [("1", "Indoors or cool"), ("0.8", "Outdoors, warm"), ("0.5", "Hot and humid")], "1")}
{_bq2("og", "lvl", "How do you play?", [("1", "Social"), ("0.6", "Competitive"), ("0.3", "Matches I really care about")], "1")}
<div class="gen-nums"><div class="q"><h3><label for="og-p">Price per overgrip</label></h3><input class="search" id="og-p" type="number" min="0" step="0.1" value="2.5" inputmode="decimal"></div>
<div class="q"><h3><label for="og-cur">Currency</label></h3><select class="search" id="og-cur"><option value="£">£</option><option value="€">€</option><option value="$">$</option><option value="AED ">AED</option></select></div></div>
</div></div>
<aside class="gen-side"><div class="lb" aria-live="polite"><h2>Your result</h2><p id="og-h" style="font-size:1.5rem;font-weight:700;color:var(--ball);margin:0 0 8px"></p><p id="og-p2" style="margin:0 0 10px"></p><p id="og-y" style="margin:0 0 10px"></p><p id="og-tip" class="wr-src" style="margin:0"></p></div></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Is my overgrip worn out?</h2><p class="muted">Tick what you notice. One tick: change it soon. Two or more: change it today.</p></div>
<div class="card" id="ogs">{og_sign_html}<p id="ogs-out" style="margin:14px 0 0;font-weight:700"></p></div></div></section>
{AD.format("og-mid")}
<section><div class="wrap"><div class="sh"><h2>Overgrip vs replacement grip</h2></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col"></th><th scope="col">Overgrip</th><th scope="col">Replacement (base) grip</th></tr></thead><tbody>
<tr><td>What it is</td><td>A thin wrap that goes on top of the grip</td><td>The thicker, cushioned grip under it, fixed to the handle</td></tr>
<tr><td>Job</td><td>Tack, sweat and a little thickness</td><td>Shape, cushion and handle size</td></tr>
<tr><td>Change it</td><td>Every 8 to 12 hours of play, or sooner</td><td>Every 2 to 3 months if you play several times a week; about once a season if you play now and then</td></tr>
<tr><td>Weight added</td><td>About 8 g each</td><td>Already counted in the racket's weight</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Want a thicker handle? One overgrip builds it a little; two make it clearly thicker. Overlapping more as you wrap also adds thickness. An overgrip adds weight at the handle, so the racket feels a little more head-light: see <a href="{href("racket-balance.html")}">racket weight and balance</a>. How to fit one, step by step: <a href="{href("padel-grip.html")}">how to hold a padel racket</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Tacky or dry overgrip?</h2></div><div class="grid">
<div class="card"><h3>Tacky</h3><p>Sticky to the touch. Suits most players and dry or cool conditions, and lasts well when your hands stay dry.</p></div>
<div class="card"><h3>Dry (absorbent)</h3><p>Soaks up sweat. Suits players with very sweaty hands and hot, humid courts, but expect to change it more often.</p></div>
<div class="card"><h3>Thin or thick</h3><p>Thinner keeps more feel of the ball. Thicker adds cushion against vibration and builds up the handle.</p></div>
<div class="card"><h3>Make it last</h3><p>Dry your hands with a towel or wristband between points, air your bag after play and don't leave the racket in a damp place. See <a href="{href("racket-care.html")}">racket care</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Stock up on overgrips</h3><p>If you change one every week, a multi-pack costs less per grip than buying singles. Pick tacky for normal hands, absorbent if you sweat a lot.</p><ul class="aff-links"><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Padel overgrips</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>Rackets</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: Padel USA "How often should you change your padel overgrip?" (26 Oct 2026: every 8 to 12 hours, about weekly at 2-3 sessions a week, heat and humidity can halve its life, signs it is finished, one vs two overgrips); Tienda Padel Point "Change grip and overgrip: optimal frequency" (recreational every 4-6 matches, competitive every 2-3, base grip every 2-3 months or once a season, signs and care); HEAD "How to place an overgrip on a padel racquet" (depends on play, sweat and type; at least every two months; advanced players before every match); Zona de Padel (overgrip about 8 g). The calculator is our own estimate built on these ranges, not a maker's formula.</p></div></section>'''
og_faq = [
    ("How often should I change my padel overgrip?", "About every 8 to 12 hours of play, roughly once a week if you play 2 or 3 times a week. Sooner if it is slippery, damp or torn, and at least every two months even if you hardly play."),
    ("How do I know my overgrip needs changing?", "It feels smooth or slippery when your hands are dry, the racket turns in your hand, it stays damp, it is torn or coming loose, or it is dark and smells."),
    ("How often do pro padel players change their overgrip?", "Many fit a new one before every match, and on hot days some change it during the match."),
    ("Should I put an overgrip on a new padel racket?", "Yes, most players do. The base grip lasts longer under an overgrip, and you can pick the tack and thickness you like."),
    ("Can I put two overgrips on a padel racket?", "Yes. Two make the handle clearly thicker. Each adds about 8 g at the handle."),
    ("How often should I change the base grip?", "About every 2 to 3 months if you play several times a week, or once a season if you play now and then, or when it goes flat or hard."),
]
page("padel-overgrip.html", "How Often to Change a Padel Overgrip: Calculator + Signs",
     "How often to change a padel overgrip (about every 8 to 12 hours of play): a free calculator for your sessions, sweat and climate, plus worn-out signs.",
     og, og_faq, "Padel overgrip")

DEMAND_PAGES += ["padel-lob.html", "padel-overgrip.html"]
exec((ROOT / "demand6.py").read_text())
