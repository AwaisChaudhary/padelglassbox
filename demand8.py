# ---------------- DEMAND RUN 11 (27 Nov 2026): padel weather checker (rain, cold, wind, heat), padel elbow arm-load check ----------------
# Executed from demand7.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards).

# ---------- 1. PADEL WEATHER: RAIN, COLD, WIND, HEAT ----------
wx_rain = [
    ("Light drizzle", "Often playable on a well-drained outdoor court, if the venue allows it and the turf, glass and your grip still feel safe. Expect a slower, lower game."),
    ("Steady rain", "Water collects on the glass and the turf. The ball skids low off the walls and you lose grip on turns. Most players stop or move indoors."),
    ("Puddles or standing water", "Stop. Standing water is where slips happen, and the bounce becomes random."),
    ("Snow or ice", "Do not play. On snow the ball no longer bounces properly, and ice on turf is dangerous."),
    ("Thunder or lightning", "Stop at once and go inside a building or a closed car. Wait 30 minutes after the last thunder. An open-sided padel roof is not shelter."),
]
wx_cold = [
    ("Balls go dead", "In the cold, padel balls lose bounce and feel slower. Smashes stay in the court and volleys die near the back glass. Keep balls in your bag, not in a cold car, and open a new tube if they feel flat."),
    ("Dress in layers", "It is easier to take a layer off than to add one. Bring a spare dry top in case of a shower."),
    ("Warm up for longer", "Plan about 15 minutes to warm up and 15 to cool down, so a one-hour booking needs about 90 minutes of your time. Cold and wet raise the injury risk."),
    ("Protect your arm", "Dead, damp balls make your arm work harder. Light band work for the wrist, elbow and shoulder before you play helps. See <a href=\"{pe}\">padel elbow</a>."),
]
wx_wind = [
    ("Keep lobs lower", "Above the glass the wind moves the ball much more. A high lob can drift half a court. Play lower, flatter lobs, or keep the ball under the glass height."),
    ("Watch the direction", "Playing into the wind, you can lob harder. With the wind behind you, lobs fly long, so take pace off."),
    ("Let more balls bounce", "Overheads are hard to time in gusts. Letting a ball come off the glass is often safer than a smash."),
    ("Stay patient", "The other pair hate the wind too. Fewer risky shots usually wins windy points."),
]
wx_heat = [
    ("Faster, bouncier game", "Warm air makes balls and glass livelier. The ball comes off the walls faster and lobs travel further."),
    ("Book early or late", "Midday sun on glass courts gets very hot. Early morning or evening slots are cooler."),
    ("Drink and rest", "Bring more water than you think, use the change of ends to drink in the shade, and stop if you feel dizzy or sick. General advice, not medical advice."),
    ("Use the sun", "If the sun is in an opponent's eyes, a lob is a good option. Courts often run end to end, so the sun can move along the court during a session."),
]
pe_link = href("padel-elbow.html")
wx_cold = [(a, b.replace("{pe}", pe_link)) for a, b in wx_cold]
wx = f'''<header class="hero"><div class="wrap"><h1>Can you play padel in the rain? A weather checker for rain, cold, wind and heat.</h1>
<p class="lead">Tell the checker what the court and sky look like. It says play, play with care, wait or stop, and what to bring: the right balls, layers, a towel and shoes. Then read how rain, cold, wind and heat change the game.</p>
{quick("You can play padel in light drizzle on a well-drained outdoor court if the venue allows it and the turf and glass still feel safe, but stop if it rains steadily, if water stands on the court, if anyone slips, or at the first thunder. Wet glass is slippery and the ball skids low off it; soaked balls get heavy and dead. After light rain a modern court is often playable in 15 to 30 minutes: press a towel into the turf, and if it comes up wet, wait. In cold weather balls lose bounce, so warm up for about 15 minutes and dress in layers.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="wxc">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Can we play right now?</h2><p class="muted" style="margin-top:0">Five quick questions about the court and the weather.</p>
{_bq2("wxc", "court", "What kind of court?", [("in", "Indoor"), ("cov", "Covered, open sides"), ("out", "Outdoor")], "out")}
{_bq2("wxc", "rain", "Rain right now", [("dry", "Dry"), ("after", "Stopped in the last hour"), ("drizzle", "Light drizzle"), ("rain", "Steady rain"), ("pool", "Puddles on court"), ("snow", "Snow or ice")], "dry")}
{_bq2("wxc", "temp", "Temperature", [("freeze", "Below 5°C (41°F)"), ("cold", "5 to 12°C"), ("mild", "12 to 25°C"), ("warm", "25 to 32°C"), ("hot", "Above 32°C (90°F)")], "mild")}
{_bq2("wxc", "wind", "Wind", [("calm", "Calm"), ("breeze", "Breezy"), ("strong", "Strong gusts")], "calm")}
{_bq2("wxc", "storm", "Thunder or lightning?", [("no", "No"), ("yes", "Yes, heard or seen")], "no")}</div>
<aside class="result" id="wxc-out" aria-live="polite"><span class="pill" id="wxc-pill"></span><h2 id="wxc-h" style="margin-top:10px"></h2><p id="wxc-p"></p><h3 style="font-size:1rem;margin:14px 0 6px">Bring and do</h3><ul id="wxc-kit"></ul><p id="wxc-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Can you play padel in the rain?</h2><p class="muted">It depends on how much rain, and on the court. Indoor courts are not affected.</p></div>
<div class="grid">{_cards(wx_rain)}</div>
<p class="muted" style="margin-top:14px">Why rain matters: a padel court is artificial grass with sand brushed in, and the sand is what lets you slide and stop. Water makes that grip unpredictable, and wet glass is slippery for both feet and ball. A wet ball can also slip on the racket face. Many clubs close outdoor courts in heavy rain, so check the booking app's cancellation rules: see <a href="{href("padel-booking-apps.html")}">padel booking apps</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long after rain can you play padel?</h2></div><div class="grid">
<div class="card"><h3>Modern court: 15 to 30 minutes</h3><p>A newer court with good drainage is often playable 15 to 30 minutes after light rain stops.</p></div>
<div class="card"><h3>Older court: hours</h3><p>Older turf or poor drainage can hold water for hours. Look for dark, shiny patches near the service lines and in the corners.</p></div>
<div class="card"><h3>The towel test</h3><p>Press a dry towel into the turf near the service line. If it comes up wet, the court is not ready yet.</p></div>
<div class="card"><h3>Dry the glass</h3><p>Wipe the glass at ball height with a towel. Wet glass makes the ball slide down instead of bouncing out.</p></div>
</div></div></section>
{AD.format("wx-mid")}
<section><div class="wrap"><div class="sh"><h2>Playing padel in winter and cold weather</h2></div><div class="grid">{_cards(wx_cold)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you play padel in the wind?</h2></div><div class="grid">{_cards(wx_wind)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Playing padel in hot weather</h2></div><div class="grid">{_cards(wx_heat)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What happens to padel balls in the rain, cold and heat?</h2></div>
<div class="tbl"><table><thead><tr><th>Condition</th><th>What the ball does</th><th>What to do</th></tr></thead><tbody>
<tr><td>Cold (under about 12°C)</td><td>Less bounce, feels slow and dead</td><td>Keep the tube warm in your bag; use a fresh tube</td></tr>
<tr><td>Heat (over about 25°C)</td><td>Bouncier and faster, flies further</td><td>Lower lobs; store balls out of the sun</td></tr>
<tr><td>Wet or soaked</td><td>Heavier, bounces low, may never fully recover</td><td>Use them only for practice once dry, or retire them</td></tr>
<tr><td>Strong wind</td><td>Drifts above the glass</td><td>Keep the ball low; some players prefer a heavier, newer ball</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">When balls are finished in any weather: <a href="{href("padel-balls.html")}">when to change padel balls</a>. Wet shoes: dry them at room temperature, never on a radiator or in a dryer, and check the sole: one that is fine on dry turf can slide on wet turf. See <a href="{href("padel-shoes.html")}">padel shoes</a>. Before a cold session, use the <a href="{href("warm-up.html")}">warm-up timer</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="aff-box"><h3>Kit for cold and wet days</h3><p>A fresh tube of balls, shoes with good tread and a few overgrips (they get slippery when damp) make the biggest difference outdoors in winter.</p><ul class="aff-links"><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: LTA Padel "Top five tips for playing padel in winter" (layers, spare top, check the court has dried, slippery glass, stop if it rains or snows or someone slips, about 15 minutes to warm up and cool down, balls lose bounce in the cold, band work for the arm, floodlights); Padel Browser "Playing padel in the rain" (22 Sep 2026: sand-filled turf and traction, standing water, 15 to 30 minutes after light rain, towel test, glass rebound, soaked balls, drying shoes, the US National Weather Service thunder rule); The Padel School "How weather affects padel" (light rain on artificial grass, wet glass, cold and hot balls, wind above the glass, sun and lobs); Tienda Padel Point wet-balls FAQ (Mar 2026: wet balls heavier, pressure and temperature); Justpadel "Can you play padel in the rain?" (snow, moisture and rackets). Advice in our own words; the checker is our own summary, not venue or safety rules. Always follow your club's decision.</p></div></section>'''
wx_faq = [
    ("Can you play padel in the rain?", "In light drizzle on a well-drained outdoor court, often yes, if the venue allows it and the court still feels safe. Stop in steady rain, if water stands on the court, if anyone slips, or at the first thunder. Indoor courts are not affected."),
    ("Is padel cancelled if it rains?", "It depends on the club. Many close outdoor courts in heavy rain or move you indoors. Check the club's or booking app's weather and cancellation rules before you go."),
    ("How long after rain can you play padel?", "A modern, well-drained court is often playable 15 to 30 minutes after light rain stops; an older court can take hours. Press a towel into the turf: if it comes up wet, wait."),
    ("Can you play padel in winter?", "Yes. Dress in layers, warm up for about 15 minutes, use a fresh tube of balls because cold balls lose bounce, and check the court is dry. Stop if it rains or snows or the surface gets slippery."),
    ("Why do padel balls feel dead in the cold?", "Padel balls are pressurised. In the cold the air inside has less push, so the ball bounces less and feels slower. In heat it is the opposite: they fly faster."),
    ("Can you play padel in the wind?", "Yes, but lobs and overheads get hard above the glass. Keep the ball lower, take pace off lobs with the wind behind you and let more balls come off the glass."),
]
page("padel-weather.html", "Can You Play Padel in the Rain? Weather Checker",
     "Can you play padel in the rain, cold or wind? Free checker says play, wait or stop, plus how long after rain, winter tips, wind tactics and what balls do.",
     wx, wx_faq, "Padel weather")

# ---------- 2. PADEL ELBOW ----------
pe_causes = [
    ("Late contact", "Hitting the ball beside or behind your body, often after it comes off the back glass, makes the forearm do the work instead of your legs and shoulders."),
    ("Wristy backhands", "Short backhands where the wrist flicks over the ball load the tendons on the outside of the elbow. Turn your shoulders and keep the wrist firm."),
    ("Gripping too tight", "Squeezing the handle all the time keeps the forearm muscles tense on every shot. Hold it at about 3 or 4 out of 10 between shots."),
    ("Off-centre hits", "Mishits send more vibration into the wrist and elbow. This is common while technique is new."),
    ("A racket that is heavy for you", "A heavy or head-heavy (high balance) racket is more weight to swing and stop on every shot."),
    ("A very stiff racket", "A hard core and stiff face pass on more shock. Softer foam cores absorb more of it."),
    ("Too much, too soon", "Going from one game a week to four, or long sessions without rest days, gives the tendons no time to adapt."),
]
pe = f'''<header class="hero"><div class="wrap"><h1>Padel elbow: why it happens and the arm-load check.</h1>
<p class="lead">Pain on the outside of the elbow is the most common padel complaint. Answer eight questions about your racket, your shots and how much you play. The check shows which habits load your arm most and what to change first.</p>
{quick("Padel elbow is the padel name for tennis elbow (lateral epicondylitis): pain on the outside of the elbow from overloaded forearm tendons. In padel it is most often linked to late contact and wristy backhands, gripping too tight, mishits, a racket that is heavy, head-heavy or stiff for you, and playing much more than before. For arm-friendly gear, look at about 340 to 360 g, low balance (under about 260 mm) and a soft core. The NHS advises rest from what hurts and seeing a GP if it is no better after 2 weeks.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="pec">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Arm-load check</h2><p class="muted" style="margin-top:0">Pick what fits you best. Not sure? Choose "not sure".</p>
{_bq2("pec", "wt", "Racket weight", [("light", "Under 355 g"), ("mid", "355 to 370 g"), ("heavy", "Over 370 g"), ("x", "Not sure")], "x")}
{_bq2("pec", "bal", "Racket balance", [("low", "Low / head-light"), ("med", "Medium"), ("high", "High / head-heavy (diamond)"), ("x", "Not sure")], "x")}
{_bq2("pec", "core", "How does the racket feel?", [("soft", "Soft"), ("med", "Medium"), ("hard", "Hard / stiff")], "med")}
{_bq2("pec", "grip", "How tight do you hold the handle?", [("relax", "Relaxed between shots"), ("tight", "Tight all the time")], "relax")}
{_bq2("pec", "late", "Do you hit balls beside or behind you, e.g. after the back glass?", [("rare", "Rarely"), ("some", "Sometimes"), ("often", "Often")], "some")}
{_bq2("pec", "bh", "Your backhand", [("turn", "I turn my shoulders"), ("wrist", "Mostly arm and wrist")], "turn")}
{_bq2("pec", "load", "How much do you play?", [("same", "About the same as usual"), ("more", "A lot more than a month ago")], "same")}
{_bq2("pec", "pain", "Elbow pain right now?", [("no", "No"), ("some", "After playing"), ("yes", "During play or daily life")], "no")}</div>
<aside class="result" id="pec-out" aria-live="polite"><span class="pill" id="pec-pill"></span><h2 id="pec-h" style="margin-top:10px"></h2><p id="pec-p"></p><ol id="pec-list"></ol><p id="pec-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What causes padel elbow?</h2><p class="muted">Usually several small things together, not one shot.</p></div>
<div class="grid">{_cards(pe_causes)}</div></div></section>
{AD.format("pe-mid")}
<section><div class="wrap"><div class="sh"><h2>What is the best padel racket for tennis elbow?</h2><p class="muted">No racket cures it. Shop and coach guides broadly agree on these starting points; it makes sense, but studies have not proven it.</p></div>
<div class="tbl"><table><thead><tr><th>Feature</th><th>Easier on the elbow</th><th>Harder on the elbow</th></tr></thead><tbody>
<tr><td>Weight</td><td>About 340 to 360 g, if you can still swing it smoothly</td><td>Over about 370 g</td></tr>
<tr><td>Balance</td><td>Low (head-light), under about 260 mm</td><td>High (head-heavy), over about 270 mm</td></tr>
<tr><td>Shape</td><td>Round: big sweet spot, fewer mishits</td><td>Diamond: small sweet spot, weight in the head</td></tr>
<tr><td>Core</td><td>Soft foam (EVA soft) or soft rubber</td><td>Hard EVA</td></tr>
<tr><td>Face</td><td>Fibreglass, or carbon with a soft core</td><td>Stiff high-K carbon with a hard core</td></tr>
<tr><td>Grip</td><td>A fresh overgrip, so you don't need to squeeze</td><td>A worn, slippery grip</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">One caution: a racket that is far too light can make you swing harder to get pace, so go light but not extreme. Full detail in <a href="{href("racket-balance.html")}">racket weight and balance</a> and <a href="{href("padel-racket-materials.html")}">carbon vs fibreglass</a>, or let the <a href="{href("racket-finder.html")}">racket finder</a> pick a shape for you (choose "sometimes" for sore arms). A worn grip? <a href="{href("padel-overgrip.html")}">When to change your overgrip</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you stop padel elbow coming back?</h2></div><div class="grid">
<div class="card"><h3>Meet the ball in front</h3><p>Move your feet so you hit in front of your body. Off the back glass, step back and let the ball come to you. See <a href="{href("padel-back-glass.html")}">playing off the back glass</a>.</p></div>
<div class="card"><h3>Turn for backhands</h3><p>Use your shoulders and a firm wrist rather than a flick. Check the continental grip in the <a href="{href("padel-grip.html")}">grip guide</a>.</p></div>
<div class="card"><h3>Warm up the forearm</h3><p>Wrist circles, light band work and easy rallies before you hit hard. Use the <a href="{href("warm-up.html")}">warm-up timer</a>; in winter take longer: <a href="{href("padel-weather.html")}">cold-weather padel</a>.</p></div>
<div class="card"><h3>Strengthen slowly</h3><p>Forearm strength work, such as slow wrist-extensor exercises with a light band or weight 2 to 3 times a week, is widely recommended. Ask a physio which exercises suit you.</p></div>
<div class="card"><h3>Build up gradually</h3><p>Add one session a week at a time and keep rest days. A <a href="{href("padel-training-plan.html")}">training plan</a> helps you spread the load.</p></div>
<div class="card"><h3>Use fresh balls</h3><p>Dead, flat or damp balls need more effort to hit. See <a href="{href("padel-balls.html")}">when to change balls</a>.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you treat padel elbow?</h2></div><div class="grid">
<div class="card"><h3>Rest from what hurts</h3><p>The NHS advises resting from the movements that make it worse. Playing through pain can slow recovery.</p></div>
<div class="card"><h3>At home</h3><p>NHS self-care includes painkillers such as paracetamol or an anti-inflammatory gel, and a hot or cold pack wrapped in a towel for up to 20 minutes every 2 to 3 hours. A forearm strap may help.</p></div>
<div class="card"><h3>See a GP or physio</h3><p>If it is no better after 2 weeks of self-care, see a GP. A physiotherapist can give a tailored exercise plan. It often improves within weeks, but it can last much longer.</p></div>
<div class="card"><h3>Coming back</h3><p>Start with short, easy sessions, a lighter or softer racket if yours is heavy, and stop if the pain returns. A brace eases symptoms but does not fix the cause.</p></div>
</div>
<p class="muted" style="margin-top:14px">Knee, back, calf and shoulder too: the full <a href="{href("padel-injuries.html")}">padel injuries guide</a> and its prevention check. This page is general information and does not replace advice from a doctor or physiotherapist. Outside the UK, follow your local health service.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="aff-box"><h3>Arm-friendly gear</h3><p>Round rackets are usually the lightest-feeling and most forgiving. Check each one's weight (about 340 to 360 g), balance (low) and core (soft) on the product page before you buy.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets</a></li><li><a href="{go("padel-rackets")}" {AFF_ATTR}>All rackets</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Fresh balls</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: NHS "Tennis elbow" (what it is, rest, painkillers or gel, hot or cold packs, strap, GP after 2 weeks, how long it lasts; same facts as our injuries guide); The Padel Paper "Prevention, diagnosis and treatment of tennis elbow in padel players" (28 Aug 2023, physiotherapist author: grip size, heavy or head-heavy rackets, backhand wrist position, warm-up, forearm strength); Justpadel "The least chance of a padel arm" (19 Jan 2022: contact beside or behind the body, short wristy backhands, cushioning, round light rackets, rest); Esprit Padel "Epicondylitis in padel" (2 Sep 2026: tight grip, off-centre contact, too light can mean harder swings, low balance, stiffness, eccentric exercises 2-3 times a week, braces). Advice in our own words; the check is our own summary, not a diagnosis.</p></div></section>'''
pe_faq = [
    ("What is padel elbow?", "Padel elbow is the padel name for tennis elbow (lateral epicondylitis): pain on the outside of the elbow caused by overloaded forearm tendons from repeated gripping and wrist movement."),
    ("What is the best padel racket for tennis elbow?", "Look for a racket that is light but not extreme (about 340 to 360 g), low balance (under about 260 mm), a round shape for a bigger sweet spot, and a soft core. No racket cures it, so fix technique and rest too."),
    ("Can I play padel with tennis elbow?", "It is better to rest from what makes it worse. The NHS advises rest, painkillers or gel and hot or cold packs, and seeing a GP if it is no better after 2 weeks. Come back with short, easy sessions."),
    ("Does a heavy padel racket cause tennis elbow?", "A racket that is heavy or head-heavy for you adds load on every swing, so it is a common factor. But a racket that is far too light can make you swing harder. Choose one you can swing smoothly."),
    ("How long does padel elbow last?", "It often gets better within a few weeks of rest, but the NHS says tennis elbow can last much longer, sometimes more than a year. Coming back too fast is a common reason it returns."),
    ("Does an elbow brace help padel elbow?", "A forearm strap or brace may ease the pain while you play, but it does not fix the cause. Combine it with rest, better technique and arm-friendly gear."),
]
page("padel-elbow.html", "Padel Elbow: Causes, Best Racket + Arm-Load Check",
     "Padel elbow (tennis elbow): what causes it, the best racket weight, balance and core for a sore arm, prevention, NHS self-care and a free arm-load check.",
     pe, pe_faq, "Padel elbow")

DEMAND_PAGES += ["padel-weather.html", "padel-elbow.html"]
