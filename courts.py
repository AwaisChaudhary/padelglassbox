# ---------------- OTHER RACKET SPORTS: court dimensions + pickleball (Awais 25 Nov 2026: add categories where data shows demand) ----------------
# Keyword Planner, worldwide, 25 Nov 2026: badminton court dimensions 100k-1M (low comp), tennis court dimensions 10k-100k, pickleball court dimensions 10k-100k (US), pickleball rules 10k-100k (US).
# Executed from build.py (shares page(), quick(), href(), e(), AD).
FT = 0.3048
def _ft(m):
    t = m / FT; f = int(t); i = round((t - f) * 12)
    if i == 12: f, i = f + 1, 0
    return f"{f} ft" + (f" {i} in" if i else "")
def court_svg(L, W, lines, label, unit="m", net=None, zone=None, colour="#2f7d4f", lc="#fff"):
    sx = 820 / L; h = W * sx; pad = 60
    def X(x): return pad + x * sx
    def Y(y): return pad + y * sx
    out = [f'<svg viewBox="0 0 940 {h + 2 * pad:.0f}" role="img" aria-label="{e(label)}" style="max-width:100%;height:auto">',
           f'<rect x="{X(0)}" y="{Y(0)}" width="{L * sx:.1f}" height="{h:.1f}" fill="{colour}"/>']
    if zone:
        for a, b in zone:
            out.append(f'<rect x="{X(a):.1f}" y="{Y(0)}" width="{(b - a) * sx:.1f}" height="{h:.1f}" fill="#d9a441" fill-opacity=".55"/>')
    out.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{L * sx:.1f}" height="{h:.1f}" fill="none" stroke="{lc}" stroke-width="3"/>')
    for x1, y1, x2, y2 in lines:
        out.append(f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" y2="{Y(y2):.1f}" stroke="{lc}" stroke-width="2.5"/>')
    if net is not None:
        out.append(f'<line x1="{X(net):.1f}" y1="{Y(0) - 14:.1f}" x2="{X(net):.1f}" y2="{Y(W) + 14:.1f}" stroke="#111" stroke-width="5" stroke-dasharray="6 3"/><text x="{X(net):.1f}" y="{Y(0) - 22:.1f}" text-anchor="middle" font-size="28" fill="#e4eef6">net</text>')
    u = (lambda v: f"{v:g} {unit}")
    out.append(f'<text x="{X(L / 2):.1f}" y="{Y(W) + 48:.1f}" text-anchor="middle" font-size="30" fill="#e4eef6">{u(L)} long</text>')
    out.append(f'<text x="{X(0) - 22:.1f}" y="{Y(W / 2):.1f}" text-anchor="middle" font-size="30" fill="#e4eef6" transform="rotate(-90 {X(0) - 22:.1f} {Y(W / 2):.1f})">{u(W)} wide</text>')
    out.append("</svg>")
    return "".join(out)
def dim_table(rows):
    return '<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Measurement</th><th scope="col">Metric</th><th scope="col">Imperial</th></tr></thead><tbody>' + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows) + "</tbody></table></div>"
def compare_card(file):
    others = [("court-dimensions.html", "Padel court dimensions"), ("pickleball-court-dimensions.html", "Pickleball court dimensions"), ("badminton-court-dimensions.html", "Badminton court dimensions"), ("tennis-court-dimensions.html", "Tennis court dimensions"), ("pickleball-rules.html", "Pickleball rules"), ("padel-vs-tennis-vs-pickleball.html", "Padel vs tennis vs pickleball")]
    return '<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Other racket sports</h2></div><div class="card"><ul>' + "".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in others if f != file) + "</ul></div></div></section>"
CMP = '''<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Court sizes compared</h2></div>''' + dim_table([
    ("Badminton (doubles)", "13.40 × 6.10 m", "44 × 20 ft"), ("Pickleball", "13.41 × 6.10 m", "44 × 20 ft"), ("Padel (doubles)", "20 × 10 m", "65 ft 7 in × 32 ft 10 in"), ("Tennis (doubles)", "23.77 × 10.97 m", "78 × 36 ft")]) + '<p class="muted" style="margin-top:10px">Playing area inside the lines (padel: inside the walls). A badminton court and a pickleball court are almost exactly the same size, which is why many sports halls tape pickleball lines over badminton courts.</p></div></section>'

# ---- Pickleball court ----
pb_lines = [(15, 0, 15, 20), (29, 0, 29, 20), (0, 10, 15, 10), (29, 10, 44, 10)]
pb = f'''<header class="hero"><div class="wrap"><h1>Pickleball court dimensions</h1>
<p class="lead">Every line on a regulation pickleball court, the kitchen, the net and how much space to leave around it, in feet and metres.</p>
{quick("A pickleball court is 20 ft wide and 44 ft long (6.10 × 13.41 m), the same for singles and doubles. The non-volley zone (the kitchen) runs 7 ft back from the net on each side. The net is 36 in high at the sidelines and 34 in in the middle. Allow a total playing area of at least 30 × 60 ft; 34 × 64 ft is recommended.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="card court-art">{court_svg(44, 20, pb_lines, "Pickleball court from above: 44 by 20 feet, with the 7 foot non-volley zone shaded on both sides of the net and the centre lines dividing the service courts.", unit="ft", net=22, zone=[(15, 29)], colour="#2b6cb0")}
<p style="margin-top:8px;color:#d6e2f2">Shaded: the non-volley zone (kitchen), 7 ft each side of the net. Drawn to scale.</p></div></div></section>
<section><div class="wrap"><div class="sh"><h2>All the measurements</h2><p class="muted">From the USA Pickleball rulebook. Lines are measured to the outside edge.</p></div>
{dim_table([("Court (singles and doubles)", "6.10 × 13.41 m", "20 × 44 ft"), ("Each half", "6.10 × 6.71 m", "20 × 22 ft"), ("Non-volley zone (kitchen) depth", "2.13 m", "7 ft each side"), ("Each service court", "3.05 × 4.57 m", "10 × 15 ft"), ("Net height at the sidelines", "0.914 m", "36 in"), ("Net height in the centre", "0.864 m", "34 in"), ("Net posts", "Outside the sidelines", "22 ft apart"), ("Line width", "5 cm", "2 in"), ("Minimum total playing area", "9.14 × 18.29 m", "30 × 60 ft"), ("Recommended total area", "10.36 × 19.51 m", "34 × 64 ft")])}
</div></section>
{AD.format("pb-court")}
<section style="padding-top:0"><div class="wrap"><div class="grid">
<div class="card"><h3>How many pickleball courts fit on a tennis court?</h3><p>Four, if the surface around the tennis court is used: a tennis court with its run-off is about 60 × 120 ft, which fits four 30 × 60 ft pickleball areas. With only the tennis lines (36 × 78 ft) most clubs paint one or two pickleball courts over it.</p></div>
<div class="card"><h3>Can I mark a pickleball court on a badminton court?</h3><p>Yes. A badminton doubles court is 20 × 44 ft too, so only the kitchen line needs adding: 7 ft from the net, where badminton's short service line sits at about 6 ft 6 in. Pickleball's net is lower, so you need a pickleball net.</p></div>
<div class="card"><h3>Marking out a court at home</h3><p>Measure the 20 × 44 ft rectangle, check it's square by measuring both diagonals (each should be about 48 ft 4 in), then add the kitchen lines 7 ft from the centre on each side and the centre lines from the kitchen to the baselines. Chalk or tape works for temporary courts.</p></div>
</div></div></section>
{CMP}{compare_card("pickleball-court-dimensions.html")}'''
pb_faq = [("What are the dimensions of a pickleball court?", "20 ft wide by 44 ft long (6.10 × 13.41 m), for both singles and doubles."),
          ("How big is the kitchen in pickleball?", "The non-volley zone runs 7 ft from the net on each side, across the full 20 ft width."),
          ("How high is a pickleball net?", "36 in at the sidelines and 34 in in the centre."),
          ("How much space do I need for a pickleball court?", "At least 30 × 60 ft in total; 34 × 64 ft is recommended so players can move around the court."),
          ("Is a pickleball court the same size as a badminton court?", "Almost exactly: a badminton doubles court is 13.40 × 6.10 m, a pickleball court 13.41 × 6.10 m. The kitchen line and net height differ.")]
page("pickleball-court-dimensions.html", "Pickleball Court Dimensions: Size, Kitchen and Net Height (Diagram, ft + m) | Padel Glass Box",
     "Pickleball court dimensions on a scale diagram: 20 x 44 ft court, 7 ft kitchen, 36 in net (34 in centre), service courts and total playing area, in feet and metres.", pb, pb_faq, "Pickleball court dimensions")

# ---- Badminton court ----
bd_lines = [(0, 0.46, 13.4, 0.46), (0, 5.64, 13.4, 5.64), (4.72, 0, 4.72, 6.1), (8.68, 0, 8.68, 6.1), (0.76, 0, 0.76, 6.1), (12.64, 0, 12.64, 6.1), (0, 3.05, 4.72, 3.05), (8.68, 3.05, 13.4, 3.05)]
bd = f'''<header class="hero"><div class="wrap"><h1>Badminton court dimensions</h1>
<p class="lead">The full badminton court with every line explained: singles and doubles, service courts, net height and the space you need above and around the court.</p>
{quick("A badminton court is 13.40 m long and 6.10 m wide for doubles (44 × 20 ft), and 13.40 × 5.18 m for singles (44 × 17 ft). The short service line is 1.98 m from the net, the doubles long service line is 0.76 m inside the back line, and the net is 1.524 m (5 ft) high in the middle and 1.55 m at the posts.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="card court-art">{court_svg(13.4, 6.1, bd_lines, "Badminton court from above: 13.4 by 6.1 metres, with singles sidelines 0.46 metres inside the doubles sidelines, short service lines 1.98 metres from the net and doubles long service lines 0.76 metres inside the back boundary.", net=6.7, colour="#2f7d4f")}
<p style="margin-top:8px;color:#d6e2f2">Drawn to scale. Outer lines: doubles court. Inner long lines: singles sidelines. The lines 0.76 m in from each end are the doubles long service lines.</p></div></div></section>
<section><div class="wrap"><div class="sh"><h2>All the measurements</h2><p class="muted">From the BWF Laws of Badminton. Lines are 40 mm wide and are part of the area they mark.</p></div>
{dim_table([("Doubles court", "13.40 × 6.10 m", "44 × 20 ft"), ("Singles court", "13.40 × 5.18 m", "44 × 17 ft"), ("Side alley (doubles only)", "0.46 m", "1 ft 6 in"), ("Net to short service line", "1.98 m", "6 ft 6 in"), ("Doubles long service line, from the back line", "0.76 m", "2 ft 6 in"), ("Service court depth: singles", "4.72 m", "15 ft 6 in"), ("Service court depth: doubles", "3.96 m", "13 ft"), ("Net height at the centre", "1.524 m", "5 ft"), ("Net height at the posts", "1.55 m", "5 ft 1 in"), ("Net depth (top to bottom)", "0.76 m", "2 ft 6 in"), ("Line width", "40 mm", "1.5 in")])}
</div></section>
{AD.format("bd-court")}
<section style="padding-top:0"><div class="wrap"><div class="grid">
<div class="card"><h3>Singles vs doubles lines</h3><p>Singles uses the inner sidelines and the full length to the back line, for serving and rallies. Doubles uses the outer sidelines, but when serving the shuttle must land short of the doubles long service line, 0.76 m in from the back. After the serve, the whole doubles court is in play.</p></div>
<div class="card"><h3>Space around and above</h3><p>Leave at least 2 m beyond the back lines and about 1.5 m at the sides, and as much ceiling height as you can: international halls use at least 12 m over the court, but 7 to 9 m is common in club and school halls. Low ceilings mostly hurt high serves and clears.</p></div>
<div class="card"><h3>Same size as pickleball</h3><p>A badminton doubles court and a pickleball court are both about 44 × 20 ft, so sports halls often share the floor. The lines and net heights differ: see our <a href="{href("pickleball-court-dimensions.html")}">pickleball court dimensions</a>.</p></div>
</div></div></section>
{CMP}{compare_card("badminton-court-dimensions.html")}'''
bd_faq = [("What are the dimensions of a badminton court?", "13.40 m long and 6.10 m wide for doubles (44 × 20 ft); singles is 13.40 × 5.18 m (44 × 17 ft)."),
          ("How high is a badminton net?", "1.524 m (5 ft) at the centre and 1.55 m (5 ft 1 in) at the posts."),
          ("How far is the short service line from the net?", "1.98 m (6 ft 6 in) on each side."),
          ("What is the doubles long service line?", "A line 0.76 m inside the back boundary. In doubles the serve must land in front of it; after the serve the full length is in play."),
          ("How much ceiling height does badminton need?", "International events use at least 12 m over the court; club halls are often 7 to 9 m. More height is better for high serves and clears.")]
page("badminton-court-dimensions.html", "Badminton Court Dimensions: Singles and Doubles Size, Lines and Net Height (m + ft) | Padel Glass Box",
     "Badminton court dimensions on a scale diagram: 13.4 x 6.1 m doubles, 5.18 m singles, 1.98 m short service line, 0.76 m doubles long service line and 1.524 m net, in metres and feet.", bd, bd_faq, "Badminton court dimensions")

# ---- Tennis court ----
tn_lines = [(0, 1.37, 23.77, 1.37), (0, 9.6, 23.77, 9.6), (5.485, 1.37, 5.485, 9.6), (18.285, 1.37, 18.285, 9.6), (5.485, 5.485, 18.285, 5.485), (0, 5.485, 0.1, 5.485), (23.67, 5.485, 23.77, 5.485)]
tn = f'''<header class="hero"><div class="wrap"><h1>Tennis court dimensions</h1>
<p class="lead">The regulation tennis court for singles and doubles, the service boxes, the net and the run-off space around it, in feet and metres.</p>
{quick("A tennis court is 78 ft long (23.77 m). It is 36 ft wide for doubles (10.97 m) and 27 ft for singles (8.23 m). The service line is 21 ft (6.40 m) from the net. The net is 3 ft (0.914 m) high at the centre and 3 ft 6 in (1.07 m) at the posts. With run-off, a court needs about 120 × 60 ft (36.6 × 18.3 m).")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="card court-art">{court_svg(23.77, 10.97, tn_lines, "Tennis court from above: 23.77 by 10.97 metres for doubles, singles sidelines 1.37 metres inside, service lines 6.40 metres from the net and a centre service line dividing the service boxes.", net=11.885, colour="#3a6ea5")}
<p style="margin-top:8px;color:#d6e2f2">Drawn to scale (metres). Inner long lines: singles sidelines. The doubles alleys are 1.37 m (4 ft 6 in) wide.</p></div></div></section>
<section><div class="wrap"><div class="sh"><h2>All the measurements</h2><p class="muted">From the ITF Rules of Tennis. The run-off figures are the ITF's recommended minimums for club and recreational courts.</p></div>
{dim_table([("Length", "23.77 m", "78 ft"), ("Doubles width", "10.97 m", "36 ft"), ("Singles width", "8.23 m", "27 ft"), ("Doubles alley", "1.37 m", "4 ft 6 in"), ("Net to service line", "6.40 m", "21 ft"), ("Service line to baseline", "5.49 m", "18 ft"), ("Each service box", "6.40 × 4.115 m", "21 × 13 ft 6 in"), ("Net height at the centre", "0.914 m", "3 ft"), ("Net height at the posts", "1.07 m", "3 ft 6 in"), ("Net posts outside the doubles sideline", "0.914 m", "3 ft"), ("Run-off behind each baseline (recommended)", "6.40 m", "21 ft"), ("Run-off at each side (recommended)", "3.66 m", "12 ft"), ("Total area with run-off", "36.57 × 18.29 m", "120 × 60 ft")])}
</div></section>
{AD.format("tn-court")}
<section style="padding-top:0"><div class="wrap"><div class="grid">
<div class="card"><h3>How big is a tennis court in square metres?</h3><p>The doubles court itself is about 261 m² (2,808 sq ft). With the recommended run-off it's about 669 m² (7,200 sq ft), which is the figure to use when planning a court or a hall.</p></div>
<div class="card"><h3>Tennis vs padel</h3><p>A padel court is 20 × 10 m inside glass walls, about three quarters of a tennis doubles court and with no run-off, so up to three padel courts can fit in the space of one tennis court with its surrounds. See the <a href="{href("court-dimensions.html")}">padel court dimensions</a> and what a <a href="{href("padel-court-cost.html")}">padel court costs</a>.</p></div>
<div class="card"><h3>Tennis vs pickleball</h3><p>Four pickleball courts fit on a tennis court with its run-off. See <a href="{href("pickleball-court-dimensions.html")}">pickleball court dimensions</a>.</p></div>
</div></div></section>
{CMP}{compare_card("tennis-court-dimensions.html")}'''
tn_faq = [("What are the dimensions of a tennis court?", "78 ft long (23.77 m); 36 ft wide for doubles (10.97 m) and 27 ft for singles (8.23 m)."),
          ("How high is a tennis net?", "3 ft (0.914 m) at the centre and 3 ft 6 in (1.07 m) at the posts."),
          ("How far is the service line from the net?", "21 ft (6.40 m). The service line is 18 ft (5.49 m) from the baseline."),
          ("How much space do I need for a tennis court?", "About 120 × 60 ft (36.6 × 18.3 m) including the recommended run-off around the lines."),
          ("How wide is the doubles alley?", "4 ft 6 in (1.37 m) on each side.")]
page("tennis-court-dimensions.html", "Tennis Court Dimensions: Size in Feet and Metres, Service Box, Net Height + Run-off | Padel Glass Box",
     "Tennis court dimensions on a scale diagram: 78 x 36 ft doubles, 27 ft singles, 21 ft service line, 3 ft net, and the 120 x 60 ft total area with run-off, in feet and metres.", tn, tn_faq, "Tennis court dimensions")

# ---- Pickleball rules ----
pr = f'''<header class="hero"><div class="wrap"><h1>Pickleball rules, explained simply</h1>
<p class="lead">How to serve, the two-bounce rule, the kitchen and how scoring works, with a quick quiz to check you've got it.</p>
{quick("Serve underhand and diagonally, so the ball clears the kitchen. The receiving side must let the serve bounce, and the serving side must let the return bounce (the two-bounce rule); after that you can volley. Never volley while standing in the 7 ft non-volley zone, the kitchen. Games are usually to 11, win by 2, and in traditional scoring only the serving side scores.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="grid">
<div class="card"><h3>1. The serve</h3><p>Serve underhand, from behind the baseline, diagonally into the opposite service court. The paddle must meet the ball below your waist with an upward arc (the volley serve), or you may drop the ball and hit it after it bounces (the drop serve). The serve must land beyond the kitchen line; a serve on the kitchen line is a fault. You get one serve, no second serve.</p></div>
<div class="card"><h3>2. The two-bounce rule</h3><p>The return of serve must bounce, and then the serving side's next shot must bounce too. After those two bounces, either side can volley (hit the ball in the air) or play it off the bounce.</p></div>
<div class="card"><h3>3. The kitchen</h3><p>The non-volley zone is the 7 ft area on each side of the net. You can't volley while touching it, including the line, and you can't let your momentum carry you into it after a volley. You can step in any time to play a ball that has bounced.</p></div>
<div class="card"><h3>4. Faults</h3><p>A rally ends when the ball lands out, goes into the net, bounces twice, is volleyed from the kitchen, or a player touches the net. Balls landing on any line are in, except a serve on the kitchen line.</p></div>
<div class="card"><h3>5. Scoring (traditional)</h3><p>Only the serving side scores. Games go to 11, win by 2. In doubles both partners serve before the serve passes to the other team, except at the start, when only one player serves; that's why the first score is called "0-0-2". Some leagues and events also use rally scoring, where every rally wins a point.</p></div>
<div class="card"><h3>6. Calling the score</h3><p>In doubles, call three numbers before serving: your score, the opponents' score, then 1 or 2 for which server you are. In singles, call two numbers, and serve from the right when your score is even and the left when it's odd.</p></div>
</div></div></section>
{AD.format("pb-rules")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Quick quiz: is it legal?</h2></div><div class="card" id="pbq"></div></div></section>
<script>(function(){{var Q=[["You volley the ball while one foot is on the kitchen line.",0,"Fault. The line is part of the kitchen."],["You step into the kitchen to hit a ball that has already bounced.",1,"Legal. The kitchen rule only applies to volleys."],["The return of serve comes back and you volley it straight away.",0,"Fault. The serving side must let the return bounce first (two-bounce rule)."],["Your serve lands on the kitchen line.",0,"Fault. A serve must land beyond the kitchen line."],["A rally ball lands on the baseline.",1,"In. Rally balls on any line are good."],["You hit a volley outside the kitchen, then your momentum carries you into it.",0,"Fault, even after the ball is dead."]],i=0,s=0,el=document.getElementById("pbq");
function show(){{if(i>=Q.length){{el.innerHTML="<h3>You got "+s+" of "+Q.length+"</h3><button class=\\"btn\\" type=\\"button\\" id=\\"pbr\\">Try again</button>";document.getElementById("pbr").onclick=function(){{i=0;s=0;show()}};return}}
el.innerHTML="<p><strong>"+(i+1)+". "+Q[i][0]+"</strong></p><div class=\\"opts\\"><button class=\\"opt\\" type=\\"button\\" data-a=\\"1\\">Legal</button> <button class=\\"opt\\" type=\\"button\\" data-a=\\"0\\">Fault</button></div><p id=\\"pba\\" aria-live=\\"polite\\"></p>";
el.querySelectorAll("button").forEach(function(b){{b.onclick=function(){{var ok=+b.dataset.a==Q[i][1];if(ok)s++;document.getElementById("pba").innerHTML=(ok?"✔ ":"✘ ")+Q[i][2]+" <button class=\\"btn\\" type=\\"button\\" id=\\"pbn\\">Next</button>";el.querySelectorAll(".opt").forEach(function(x){{x.disabled=true}});document.getElementById("pbn").onclick=function(){{i++;show()}}}}}})}}show()}})();</script>
<section style="padding-top:0"><div class="wrap"><div class="grid">
<div class="card"><h3>Pickleball vs padel</h3><p>Pickleball has no walls, an underhand serve that must clear the kitchen, and side-out scoring to 11. Padel uses tennis scoring and the glass walls are in play. See <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a>.</p></div>
<div class="card"><h3>The court</h3><p>20 × 44 ft with a 7 ft kitchen each side: see the <a href="{href("pickleball-court-dimensions.html")}">pickleball court dimensions</a>.</p></div>
</div><p class="muted" style="margin-top:14px">Based on the USA Pickleball official rulebook. Rules are updated each year and local leagues may use their own formats, so check with your club for events.</p></div></section>
{compare_card("pickleball-rules.html")}'''
pr_faq = [("What is the two-bounce rule in pickleball?", "The serve must bounce before it's returned, and the return must bounce before the serving side hits it. After that, players can volley."),
          ("What is the kitchen in pickleball?", "The non-volley zone, 7 ft from the net on each side. You can't volley while touching it or carry into it after a volley."),
          ("Can you go in the kitchen in pickleball?", "Yes, any time, as long as you don't volley there. Stepping in to play a ball that has bounced is legal."),
          ("How do you score in pickleball?", "In traditional scoring only the serving side scores. Games go to 11, win by 2. Some events use rally scoring, where every rally scores."),
          ("Why do you say 0-0-2 at the start?", "In doubles only one player on the first serving team serves at the start, so the game begins as if that player were the second server.")]
page("pickleball-rules.html", "Pickleball Rules Explained Simply: Serve, Kitchen, Two-Bounce Rule + Scoring (Quiz) | Padel Glass Box",
     "Pickleball rules made simple: the underhand serve, the two-bounce rule, the kitchen (non-volley zone), faults and how scoring works, with a quick is-it-legal quiz.", pr, pr_faq, "Pickleball rules")

COURT_PAGES = ["pickleball-court-dimensions.html", "badminton-court-dimensions.html", "tennis-court-dimensions.html", "pickleball-rules.html"]
