# ---------------- DEMAND RUN 9 (27 Nov 2026): volley guide + volley picker + fault finder, return of serve picker, back glass rebound picker ----------------
# Executed from demand5.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2).

def _cards(rows, pill=None):
    out = []
    for i, (a, b) in enumerate(rows):
        top = f'<span class="pill b">{e(pill)} {i + 1}</span><h3 style="margin-top:10px">' if pill else "<h3>"
        out.append(f'<div class="card">{top}{e(a)}</h3><p>{b}</p></div>')
    return "".join(out)

# ---------- 1. PADEL VOLLEY ----------
vo_steps = [
    ("Racket up and in front", "Wait with the racket head up, in front of your body and above net height. Then you only push it forward, you never have to lift it first."),
    ("Continental grip", "Hold it like a hammer, the same grip for forehand and backhand volleys. A flat, frying-pan grip opens your wrist and the ball flies up."),
    ("Turn the shoulders", "Turn your shoulders towards the side the ball is coming. The turn is your backswing, so the racket hardly goes back."),
    ("Short, firm punch", "A volley is a block or a short push, not a swing. Meet the ball out in front of your body and stop the racket soon after contact."),
    ("Step in", "Step towards the ball with the opposite foot (left foot on a right-hander's forehand, right foot on the backhand). The power comes from the step, not the arm."),
    ("Low ball? Bend the knees", "Get down to the ball with your legs and keep the racket head up. Do not drop the racket head to reach a low ball."),
]
vo_types = [
    ("Block volley", "For fast balls at you. Hold the racket firm and let the ball's own speed send it back. Aim deep and through the middle."),
    ("Push (deep) volley", "For an easier rally ball. Push the ball deep, past the service line, to keep your opponents back."),
    ("Slice (fizz) volley", "For slow balls you can attack. Cut under the ball for backspin so it stays low after the back glass and is hard to play."),
    ("Setup volley", "A softer, sliced volley into the back corner, landing just before the glass. It sets up the next ball rather than trying to win now."),
    ("First volley", "The first ball after you serve and run in. Get the racket up early, play it deep, and only finish if the ball is really easy."),
    ("Low volley", "A ball below the net. Bend your knees, open the face a little and play it slow and deep. You cannot attack from below the net."),
]
vo = f'''<header class="hero"><div class="wrap"><h1>How to volley in padel: technique, the right volley for each ball, and a fault finder.</h1>
<p class="lead">Most points in padel are won at the net, and the volley is how you stay there. Learn the six basics, pick the right volley for the ball coming at you, then use the fault finder to fix the volley that keeps going wrong.</p>
{quick("To volley in padel, keep the racket up and in front of you with a continental grip, turn your shoulders, and play a short, firm punch out in front of your body while stepping in with the opposite foot. Do not swing. Most volleys should go deep, past the service line, to keep your opponents back. Play a block on fast balls, a deep push on easy balls and a sliced volley on slow balls you can attack.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="vop">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Which volley should I play?</h2><p class="muted" style="margin-top:0">Three questions about the ball coming at you.</p>
{_bq2("vop", "spd", "How fast is the ball?", [("fast", "Fast"), ("med", "Medium"), ("slow", "Slow, floating")], "med")}
{_bq2("vop", "ht", "Where do you meet it?", [("low", "Below the net"), ("chest", "Net to chest height"), ("high", "Above the shoulder")], "chest")}
{_bq2("vop", "opp", "Where are your opponents?", [("back", "Both at the back"), ("mid", "One coming in"), ("net", "Both at the net")], "back")}</div>
<aside class="result" id="vop-out" aria-live="polite"><h2 id="vop-h"></h2><p id="vop-p"></p><p id="vop-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you hit a volley in padel?</h2><p class="muted">Six basics. They are the same for forehand and backhand. Grip details in our <a href="{href("padel-grip.html")}">grip guide</a>.</p></div>
<div class="grid">{_cards(vo_steps, "Step")}</div></div></section>
{AD.format("vo-mid")}
<section><div class="wrap"><div class="sh"><h2>Types of padel volley</h2><p class="muted">Pick by the ball, not by what you would like to play.</p></div>
<div class="grid">{_cards(vo_types)}</div></div></section>
<section style="padding-top:0"><div class="wrap gen" id="vof">
<div class="gen-main"><div class="card"><h2 style="font-size:1.4rem">Volley fault finder</h2><p class="muted" style="margin-top:0">What keeps happening to your volleys?</p>
<div class="q"><h3><label for="vof-s">My volley...</label></h3><select class="search" id="vof-s">
<option value="up">flies up and comes back off their back glass</option>
<option value="net">goes into the net</option>
<option value="long">goes out long or over the glass</option>
<option value="late">is late, the ball is past me</option>
<option value="lob">is fine, but I keep getting lobbed</option>
<option value="weak">has no power</option>
<option value="bh">breaks down on the backhand</option>
</select></div></div></div>
<aside class="gen-side"><div class="lb" aria-live="polite"><h2>Likely cause</h2><p id="vof-c" style="font-weight:700;color:var(--ball);margin:0 0 8px"></p><h2 style="margin-top:12px">Fix</h2><p id="vof-f" style="margin:0 0 10px"></p><p id="vof-d" class="wr-src" style="margin:0"></p></div></aside>
</div></section>
<section><div class="wrap"><div class="sh"><h2>Where should you aim your volleys?</h2></div><div class="grid">
<div class="card"><h3>Deep, past the service line</h3><p>A deep volley keeps the other pair back, where they cannot attack you. This is the default for most volleys.</p></div>
<div class="card"><h3>Down the middle</h3><p>The middle makes both opponents think about who takes it, and the net is lowest there. A slower ball down the middle dies near the back glass.</p></div>
<div class="card"><h3>At the feet of a player coming in</h3><p>If one opponent runs to the net, a low volley at their feet forces them to hit up to you.</p></div>
<div class="card"><h3>Into the corner, only to finish</h3><p>A firm volley into the back corner and the side glass (the double glass) can win the point, but only on an easy, high ball.</p></div>
</div>
<p class="muted" style="margin-top:14px">Volley drill, "push them back": one pair at the net, one at the back. The back pair starts each point. The net pair must land their volleys past the service line; after three good volleys, play the point out. Only the net pair can win the point; if the back pair wins it, they swap to the net. More drills in the <a href="{href("drills.html")}">drills planner</a>. Where to stand at the net: <a href="{href("positioning.html")}">positioning</a>. Answering lobs over your head: <a href="{href("padel-lob.html")}">padel lob guide</a> and <a href="{href("bandeja-vs-vibora.html")}">bandeja vs víbora</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: LTA Padel "Volley tips and techniques" (racket at contact height, short push, contact in front, step with the opposite foot, block / push / fizz volleys, slice, aim past the service line, the push-them-back drill); The Padel School "The Padel Volley" (continental grip, shoulder turn, block not swing, step-in foot, bend knees, not too close to the net), "Padel volleys: biggest mistakes" (open face, late preparation, low racket, over-aggression), "How to hit a great first volley" and "How to win at net using the setup volley". Advice in our own words; the pickers are our own summary of these sources.</p></div></section>'''
vo_faq = [
    ("How do you volley in padel?", "Racket up and in front, continental grip, turn your shoulders and play a short, firm punch out in front of your body while stepping in with the opposite foot. Do not swing."),
    ("What grip is best for padel volleys?", "The continental grip, the same one you serve with. It works for forehand and backhand volleys without changing grip at the net."),
    ("Where should I aim my volleys in padel?", "Mostly deep, past the service line, and often down the middle. Aim at the feet of a player who is coming in, and go for the corners only to finish an easy ball."),
    ("Why does my volley go up in padel?", "Usually the racket face is too open or you were late, so you met the ball behind you. Get the racket ready earlier, meet it in front and keep the face a little more closed."),
    ("How far from the net should I stand to volley?", "About two to three metres, not touching distance. Too close and any lob goes over you; a small step back gives you time, and you step forward into each volley."),
    ("Should I swing on a padel volley?", "No. A volley is a block or a short push. The power comes from your step and the ball's speed. A bigger swing only for a slow, high ball you can attack."),
]
page("padel-volley.html", "How to Volley in Padel: Technique, Volley Picker, Fault Finder",
     "How to volley in padel: six basics, the types of volley, where to aim, a picker for the right volley for each ball, and a fault finder for common errors.",
     vo, vo_faq, "Padel volley")

# ---------- 2. RETURN OF SERVE ----------
rt_prob = [
    ("Going for winners", "The return's job is to get the ball back and make the server's team play another shot. Aim deep or at the feet of the server coming in."),
    ("Taking it too early", "Against a good serve, let the ball come off the side glass. That gives you room to swing and better timing."),
    ("Moving towards the glass", "After the bounce, step away from the glass, not into it, so the ball can come to you."),
    ("Racket back too late", "See which side the serve goes, then take the racket back at once, before the bounce. Then only your feet need to adjust."),
    ("Not reading the server", "Most servers repeat their spin and target. After a few points, start a step towards where their serve usually goes."),
]
rt = f'''<header class="hero"><div class="wrap"><h1>How to return serve in padel: where to stand and which return to play.</h1>
<p class="lead">Half your points start with a return. Most club players lose them by trying too much. Use the return picker to choose a safe, smart return for the serve you face, and fix the five most common return problems.</p>
{quick("To return serve in padel, stand about one step behind the service line and close to (not against) the side glass, take the racket back as soon as you see the serve's direction, and let a good serve come off the side glass before you hit. The goal is not a winner: return deep or low at the feet of the server coming to the net, or lob over the net player. You must let the serve bounce once in your box; you may not volley it.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="rtp">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Return picker</h2><p class="muted" style="margin-top:0">Tell it about the serve. It tells you where to stand and what to hit.</p>
{_bq2("rtp", "tgt", "Where does the serve go?", [("glass", "Into the side glass"), ("t", "Down the middle (T)"), ("body", "At my body"), ("easy", "Slow, to the middle of the box")], "glass")}
{_bq2("rtp", "spin", "What does it do after the bounce?", [("flat", "Nothing special"), ("side", "Moves away from the glass (side spin)"), ("slice", "Stays low (slice)"), ("fast", "Comes fast")], "flat")}
{_bq2("rtp", "srv", "What does the server do next?", [("net", "Runs to the net"), ("stay", "Stays back")], "net")}</div>
<aside class="result" id="rtp-out" aria-live="polite"><h2 id="rtp-h"></h2><p id="rtp-p"></p><p id="rtp-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Where should you stand to return serve in padel?</h2></div><div class="grid">
<div class="card"><h3>Just behind the service line</h3><p>Start about one small step behind the service line, facing the server, not turned sideways. Too far back and you rush in late; too close and good serves jam you.</p></div>
<div class="card"><h3>Near the side glass, not on it</h3><p>Stand close enough to the side glass to cover a serve into it, with room to swing. Against a left-hander, or on the backhand side, the ball hugs the wall more: move a little closer.</p></div>
<div class="card"><h3>On your toes</h3><p>Split step as the server hits, read the side, and turn. The racket goes back before the ball bounces.</p></div>
<div class="card"><h3>Your partner</h3><p>Your partner usually stands back too, about level with you, ready to defend. Formation choices: <a href="{href("positioning.html")}">where to stand on court</a>.</p></div>
</div></div></section>
{AD.format("rt-mid")}
<section><div class="wrap"><div class="sh"><h2>Five common return problems and the fix</h2></div><div class="grid">{_cards(rt_prob)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Return of serve rules in padel</h2><p class="muted">The short version. Full detail and a checker: <a href="{href("serve-rules.html")}">serve rules</a>.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><tbody>
<tr><td>Must it bounce?</td><td>Yes. The serve must bounce in your service box before you hit it. Volleying the serve loses the point.</td></tr>
<tr><td>Which player returns?</td><td>The player on the side the serve goes to. The returning pair keeps the same sides for the whole set and can only swap at the start of a new set.</td></tr>
<tr><td>Serve hits the fence</td><td>If the serve touches the wire fence before you hit it, it is a fault. If it hits the glass after bouncing in the box, it is in play.</td></tr>
<tr><td>Net touch</td><td>A serve that clips the net and lands in the box is a let: serve again.</td></tr>
<tr><td>Golden point</td><td>At 40-40 with golden point, the returning pair chooses which side receives. See <a href="{href("golden-point-star-point.html")}">golden point vs star point</a>.</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:14px">Practise both ends: <a href="{href("how-to-serve-padel.html")}">how to serve + serve tracker</a>. Can't decide which side to play? <a href="{href("which-side-padel.html")}">Left or right side quiz</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: The Padel School "How to return serve in padel: fix these common problems first" (stance, racket back before the bounce, let good serves come off the glass, side spin and slice adjustments, reading the server), "The Padel Return", "Where to hit the return" (block a serve into the glass, lob a serve down the T, attack an easy serve), "Essential padel return rules" and "How to dominate an easy serve"; FIP Rules of Padel (bounce before return, fence fault, let, sides kept for the set). Advice in our own words.</p></div></section>'''
rt_faq = [
    ("Where do you stand to return serve in padel?", "About one step behind the service line, facing the server, near but not against the side glass. Adjust a little after a few serves once you see what the server does."),
    ("Can you volley a serve in padel?", "No. The serve must bounce in your service box first. If you volley it, you lose the point."),
    ("What is the best return of serve in padel?", "The safe one. A deep or low return at the feet of the server coming in, or a lob over the net player when the serve is hard. Save winners for slow, easy serves."),
    ("Should I hit the return before or after the glass?", "Against a good serve into the side glass, let it come off the glass first: you get more room and better timing. Take an easy, central serve early and be more aggressive."),
    ("How do I return a serve with side spin?", "Give it more space. A side-spin serve moves away from the glass towards you after the bounce, so stand a little further from the glass and let it come in."),
    ("How do I return a low, sliced serve?", "Stand a little closer to the glass and bend your knees early, because the ball stays low after the glass. Play it slow and deep or lob; do not try to hit it hard."),
]
page("padel-return-of-serve.html", "How to Return Serve in Padel: Where to Stand + Return Picker",
     "How to return serve in padel: where to stand, a free return picker for each type of serve, the five most common return mistakes, and the return rules.",
     rt, rt_faq, "Return of serve")

# ---------- 3. BACK GLASS ----------
bg_steps = [
    ("Turn side-on early", "As soon as the ball passes you, turn sideways to the side wall and take the racket back. Do not face the glass square on."),
    ("Give it room", "Move away from the glass with small, quick steps. Most mistakes come from standing too close to the wall."),
    ("Watch the ball into the glass", "Keep your eyes on the ball as it hits the glass. The first contact tells you where it will come out."),
    ("Let it come back to you", "Wait for the ball to finish its rebound. It is now moving towards the net, so it needs little power from you."),
    ("Low and step in", "Bend your knees, step forward into the shot and swing up through the ball, before it bounces again."),
]
bg_err = [
    ("Crowding the glass", "The ball comes out further than you think. Start further from the wall than feels right."),
    ("Hitting too early", "Taking the ball before it has finished its rebound gives a rushed, weak shot. Wait."),
    ("Too much power", "The ball is already coming towards the net. A smooth swing is enough; hard hits fly out or into the net."),
    ("Back to the court", "Turning your back on the court means you lose track of the other pair. Stay side-on."),
    ("Flat feet", "Backing up flat-footed leaves you stuck. Stay on the balls of your feet and keep moving."),
]
bg = f'''<header class="hero"><div class="wrap"><h1>How to play off the back glass in padel.</h1>
<p class="lead">Letting the ball come off the back glass is the skill tennis players find hardest when they start padel. Learn the five basics, then use the rebound picker: tell it what the ball does off the glass and it tells you where to stand and which shot to play.</p>
{quick("To play off the back glass in padel, turn side-on as the ball passes you, move away from the glass with small steps, watch the ball hit the wall and let it finish its rebound, then bend your knees and step forward into the shot. Fast, flat balls come out fast and far, so give them more room; slow, high balls die near the glass, so move closer. From the back, a high lob or a low ball at the net player's feet is usually best; a high rebound can be attacked with a bajada.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="bgp">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Back glass rebound picker</h2><p class="muted" style="margin-top:0">What is the ball doing?</p>
{_bq2("bgp", "spd", "How does it hit the glass?", [("fast", "Fast and flat"), ("med", "Medium"), ("slow", "Slow, a high lob")], "med")}
{_bq2("bgp", "ht", "How high does it come off?", [("low", "Below the knee"), ("mid", "Waist height"), ("high", "Shoulder height or higher")], "mid")}
{_bq2("bgp", "wall", "Which walls?", [("back", "Back glass only"), ("sb", "Side glass, then back glass"), ("bs", "Back glass, then side glass")], "back")}
{_bq2("bgp", "opp", "Where are your opponents?", [("net", "Both at the net"), ("back", "At the back")], "net")}</div>
<aside class="result" id="bgp-out" aria-live="polite"><h2 id="bgp-h"></h2><p id="bgp-p"></p><p id="bgp-t" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you play the ball off the back glass?</h2><p class="muted">Five basics for forehand and backhand.</p></div>
<div class="grid">{_cards(bg_steps, "Step")}</div></div></section>
{AD.format("bg-mid")}
<section><div class="wrap"><div class="sh"><h2>How to read the rebound</h2></div><div class="grid">
<div class="card"><h3>Fast and flat</h3><p>Comes off the glass fast and low and travels a long way back towards the net. Stand further from the wall.</p></div>
<div class="card"><h3>Slow and high</h3><p>A lob loses speed in the glass and drops close to the wall. Move in closer, or it bounces twice before you get there.</p></div>
<div class="card"><h3>Topspin</h3><p>Kicks up and forward off the glass. Expect it higher and further out.</p></div>
<div class="card"><h3>Slice (backspin)</h3><p>Stays low after the glass. Get down early and lift it.</p></div>
<div class="card"><h3>Side glass, then back glass</h3><p>Usually comes out towards the middle of the court, nearer your partner. Agree who takes these.</p></div>
<div class="card"><h3>Back glass, then side glass</h3><p>Runs further along the side wall and comes out nearer the net, on the same side. Follow it along the wall.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Common back glass mistakes</h2></div><div class="grid">{_cards(bg_err)}</div>
<p class="muted" style="margin-top:14px">Back glass drill: a partner feeds slow, deep balls past the service line. First let each ball bounce twice (court, glass, court) before you hit, then take away the extra bounce. Mix forehand and backhand feeds. Next level: the feeder sends waist-high rebounds and you drive them low, then move to the net. Build a full session in the <a href="{href("drills.html")}">drills planner</a>.</p>
<p class="muted" style="margin-top:14px">When is a ball off the glass in or out? See the <a href="{href("wall-rules.html")}">wall and fence rules checker</a>. Lobbing from the back: <a href="{href("padel-lob.html")}">how to hit a lob</a>. Playing balls that leave the court: <a href="{href("out-of-court-play.html")}">out-of-court play</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: LTA Padel "How to play off the back glass in padel" (side-on, early racket, small steps, get low, slow balls need you closer, the feed drill); Padel Browser "How to play off the back wall in padel" (18 Jun 2026: read speed, height and spin, let the rebound finish, waist-high balls to drive, bajada, mistakes, drills); Tennis Warehouse "Using the walls in padel" (let balls past the service line come off the wall, double-wall paths); Nox "Bajada de pared de revés"; The Padel School "Hit against the back glass" (lob most of the time, or low to the feet). Advice in our own words; the picker is our own summary.</p></div></section>'''
bg_faq = [
    ("How do you play off the back wall in padel?", "Turn side-on, move away from the glass, watch the ball into the wall and let it finish its rebound, then bend your knees and step into the shot. It is already coming towards the net, so use a smooth swing."),
    ("How far from the back glass should I stand?", "Further than you think for fast, flat balls, which come out a long way. Closer for slow, high lobs, which drop near the wall. Reading the speed is the key."),
    ("What shot should I play off the back glass?", "Most of the time a high lob over the net pair, or a low ball at their feet. If the ball comes off high, at waist to shoulder height, you can attack with a bajada."),
    ("What is a bajada in padel?", "An attacking shot played on a ball that comes off the back glass high. You take it on the way down, at about shoulder height, and drive it low and hard, then move to the net."),
    ("Why do I keep missing balls off the back glass?", "Usually you stand too close to the glass, face the wall square on or hit too early. Turn side-on, give the ball more room and wait for it."),
    ("Should I let the ball hit the back glass or take it before?", "Let balls that land past the service line come off the glass. The exception is a soft ball that will die right at the wall: take that one before it reaches the glass."),
]
page("padel-back-glass.html", "How to Play Off the Back Glass in Padel + Rebound Picker",
     "How to play off the back glass in padel: five basics, how to read fast, slow and double-wall rebounds, a free shot picker, common mistakes and a drill.",
     bg, bg_faq, "Back glass")

DEMAND_PAGES += ["padel-volley.html", "padel-return-of-serve.html", "padel-back-glass.html"]
