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
    others = [("court-dimensions.html", "Padel court dimensions"), ("pickleball-court-dimensions.html", "Pickleball court dimensions"), ("badminton-court-dimensions.html", "Badminton court dimensions"), ("tennis-court-dimensions.html", "Tennis court dimensions"), ("pickleball-rules.html", "Pickleball rules"), ("badminton-rules.html", "Badminton rules"), ("table-tennis-rules.html", "Table tennis rules and table size"), ("squash-court-dimensions.html", "Squash court dimensions"), ("padel-vs-tennis-vs-pickleball.html", "Padel vs tennis vs pickleball")]
    return '<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Other racket sports</h2></div><div class="card"><ul>' + "".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in others if f != file) + "</ul></div></div></section>"
CMP = '''<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Court sizes compared</h2></div>''' + dim_table([
    ("Table tennis table", "2.74 × 1.525 m", "9 × 5 ft"), ("Squash", "9.75 × 6.40 m", "32 × 21 ft"), ("Badminton (doubles)", "13.40 × 6.10 m", "44 × 20 ft"), ("Pickleball", "13.41 × 6.10 m", "44 × 20 ft"), ("Padel (doubles)", "20 × 10 m", "65 ft 7 in × 32 ft 10 in"), ("Tennis (doubles)", "23.77 × 10.97 m", "78 × 36 ft")]) + '<p class="muted" style="margin-top:10px">Playing area inside the lines (padel: inside the walls). A badminton court and a pickleball court are almost exactly the same size, which is why many sports halls tape pickleball lines over badminton courts.</p></div></section>'

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

def quiz(qid, Q):
    import json as _j
    return (f'<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Quick quiz: is it legal?</h2></div><div class="card" id="{qid}"></div></div></section>'
      f'<script>(function(){{var Q={_j.dumps(Q)},i=0,s=0,el=document.getElementById("{qid}");'
      'function show(){if(i>=Q.length){el.innerHTML="<h3>You got "+s+" of "+Q.length+"</h3><button class=\\"btn\\" type=\\"button\\">Try again</button>";el.querySelector("button").onclick=function(){i=0;s=0;show()};return}'
      'el.innerHTML="<p><strong>"+(i+1)+". "+Q[i][0]+"</strong></p><div class=\\"opts\\"><button class=\\"opt\\" type=\\"button\\" data-a=\\"1\\">Legal</button> <button class=\\"opt\\" type=\\"button\\" data-a=\\"0\\">Fault</button></div><p class=\\"qa-out\\" aria-live=\\"polite\\"></p>";'
      'el.querySelectorAll(".opt").forEach(function(b){b.onclick=function(){var ok=+b.dataset.a==Q[i][1];if(ok)s++;var o=el.querySelector(".qa-out");o.innerHTML=(ok?"✔ ":"✘ ")+Q[i][2]+" <button class=\\"btn\\" type=\\"button\\">Next</button>";el.querySelectorAll(".opt").forEach(function(x){x.disabled=true});o.querySelector("button").onclick=function(){i++;show()}}})}show()})();</script>')

# ---- Badminton rules ----
br = f"""<header class="hero"><div class="wrap"><h1>Badminton rules, explained simply</h1>
<p class="lead">Scoring, the serve (including the 1.15 m rule), faults and lets, for singles and doubles, with a quick quiz.</p>
{quick("A match is the best of three games. Each game is to 21 points with rally scoring (every rally wins a point); at 20-20 you need a 2-point lead, and at 29-29 the next point wins. Serve diagonally, hitting the shuttle below 1.15 m from the floor, from the right court when your score is even and the left when it's odd.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="grid">
<div class="card"><h3>1. Scoring</h3><p>Rally scoring: whoever wins the rally scores and serves next. Games go to 21, win by 2, capped at 30 (the side reaching 30 at 29-all wins). Best of three games. There's a 60-second break when the leader reaches 11, and up to 2 minutes between games. Players change ends after each game, and in the third game when the leader reaches 11.</p></div>
<div class="card"><h3>2. The serve</h3><p>Serve diagonally into the opposite service court. When the racket hits it, the whole shuttle must be below 1.15 m from the court surface, and the first contact must be on the base (cork). Both feet stay on the floor and inside the service court until the serve is made, without touching the lines.</p></div>
<div class="card"><h3>3. Which side to serve from</h3><p>Serve from the right service court when the server's score is even (0, 2, 4…) and the left when it's odd. In doubles, only the side that wins a rally changes service courts; there is one serve per side, and the receiving pair don't swap places.</p></div>
<div class="card"><h3>4. Faults</h3><p>A rally is lost if the shuttle lands outside the lines, goes through or under the net, hits the ceiling, walls or a person, is hit twice in a row by the same player (or by both partners in a row), or if a player touches the net or reaches over it to hit the shuttle. A shuttle landing on a line is in.</p></div>
<div class="card"><h3>5. Lets</h3><p>A let replays the rally. Examples: the receiver wasn't ready when the serve was hit, the shuttle gets caught on the net after the serve, or there's outside interference such as a shuttle from another court.</p></div>
<div class="card"><h3>6. Singles vs doubles lines</h3><p>Singles serves go long and narrow (to the back line, singles sidelines); doubles serves go short and wide (to the doubles long service line, outer sidelines). See the <a href="{href("badminton-court-dimensions.html")}">badminton court dimensions</a>.</p></div>
</div><p class="muted" style="margin-top:14px">Based on the BWF Laws of Badminton. Club and school games often play shorter formats, such as a single game to 21 or to 15.</p></div></section>
{AD.format("bd-rules")}""" + quiz("bdq", [["You serve with the shuttle hit at 1.10 m from the floor.", 1, "Legal. The whole shuttle must be below 1.15 m."], ["The shuttle lands on the sideline.", 1, "In. The lines are part of the court."], ["Your racket touches the net while you play a net shot.", 0, "Fault. You can't touch the net while the shuttle is in play."], ["At 20-20 you win the next rally.", 0, "Not over yet: at 20-all you need a 2-point lead, so it's 21-20 and play goes on."], ["In doubles, your partner and you hit the shuttle one after the other.", 0, "Fault. Each side gets one hit."], ["The shuttle clips the ceiling and lands in.", 0, "Fault. Touching the ceiling ends the rally."]]) + f"""
{compare_card("badminton-rules.html")}"""
br_faq = [("How many points is a badminton game?", "21, with rally scoring. At 20-20 you need a 2-point lead; at 29-29 the next point wins."),
          ("What is the 1.15 m serve rule in badminton?", "When the server hits the shuttle, the whole shuttle must be below 1.15 m from the court surface."),
          ("How many games in a badminton match?", "Best of three games."),
          ("Can you touch the net in badminton?", "No. Touching the net with your racket, body or clothing while the shuttle is in play is a fault."),
          ("Is the line in or out in badminton?", "In. A shuttle landing on a line counts as in.")]
page("badminton-rules.html", "Badminton Rules Explained Simply: Scoring to 21, Serve Rules (1.15 m), Faults + Quiz | Padel Glass Box",
     "Badminton rules made simple: rally scoring to 21, the 1.15 m serve rule, which side to serve from, faults, lets, and singles vs doubles, with a quick quiz.", br, br_faq, "Badminton rules")

# ---- Table tennis ----
tt_lines = [(0, 0.7625, 2.74, 0.7625)]
tt = f"""<header class="hero"><div class="wrap"><h1>Table tennis rules and table size</h1>
<p class="lead">The official table, net and ball sizes, then the rules of the serve, scoring and doubles, with a quick quiz.</p>
{quick("A table tennis table is 2.74 m long, 1.525 m wide and 76 cm high (9 × 5 ft, 2 ft 6 in high), with a net 15.25 cm (6 in) high. Games go to 11, win by 2, and each player serves two points in turn (one each from 10-10). Toss the ball at least 16 cm straight up from an open palm and hit it so it bounces once on your side, then on your opponent's.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="card court-art">{court_svg(2.74, 1.525, tt_lines, "Table tennis table from above: 2.74 by 1.525 metres with the net across the middle and a centre line for doubles.", net=1.37, colour="#1f5fa8")}
<p style="margin-top:8px;color:#d6e2f2">Drawn to scale. The centre line is only used for doubles serves.</p></div></div></section>
<section><div class="wrap"><div class="sh"><h2>Table, net and ball sizes</h2><p class="muted">From the ITTF Laws of Table Tennis.</p></div>
{dim_table([("Table length", "2.74 m", "9 ft"), ("Table width", "1.525 m", "5 ft"), ("Table height", "76 cm", "2 ft 6 in"), ("Net height", "15.25 cm", "6 in"), ("Net overhang past each side", "15.25 cm", "6 in"), ("White edge lines", "2 cm", "3/4 in"), ("Ball diameter", "40 mm", "1.57 in"), ("Ball weight", "2.7 g", "0.095 oz"), ("Room space recommended for play", "about 6 × 3 m minimum", "about 20 × 10 ft"), ("Competition playing area", "14 × 7 m", "46 × 23 ft")])}
</div></section>
{AD.format("tt-rules")}
<section style="padding-top:0"><div class="wrap"><div class="grid">
<div class="card"><h3>The serve</h3><p>Rest the ball on an open, flat palm behind the end line and above the table. Toss it nearly straight up at least 16 cm and hit it as it falls, so it bounces on your side then your opponent's. The ball must stay visible to the receiver: no hiding it with your body or free arm. If a serve clips the net and lands correctly, it's a let and you serve again.</p></div>
<div class="card"><h3>Scoring</h3><p>Every rally scores a point. A game goes to 11, win by 2. Serve passes every two points, and every point from 10-10. Matches are best of three, five or seven games, and players change ends after each game (and at 5 points in the deciding game).</p></div>
<div class="card"><h3>Losing a point</h3><p>You lose the point if you miss the ball, hit it into the net or off the table, let it bounce twice on your side, volley it before it bounces, move the table, touch the net or put your free hand on the table during a rally. A ball that touches the edge of the table is good; one off the side of the table is not.</p></div>
<div class="card"><h3>Doubles</h3><p>The serve goes from the server's right half to the receiver's right half. Partners must hit in turn. Serve rotates so every player serves to and receives from each opponent.</p></div>
</div></div></section>""" + quiz("ttq", [["Your serve clips the net and lands on your opponent's side.", 1, "Not a fault: it's a let, and you serve again."], ["You toss the ball 8 cm before serving.", 0, "Fault. The toss must be at least 16 cm."], ["The ball hits the top edge of the table.", 1, "Good. An edge ball is in play; a ball off the side face is not."], ["You put your free hand on the table during a rally.", 0, "Fault. Your free hand can't touch the playing surface."], ["At 10-10 you win one point.", 0, "Not yet: you need a 2-point lead."]]) + f"""
{compare_card("table-tennis-rules.html")}"""
tt_faq = [("What size is a table tennis table?", "2.74 m long, 1.525 m wide and 76 cm high (9 × 5 ft, 2 ft 6 in high)."),
          ("How high is a table tennis net?", "15.25 cm (6 in)."),
          ("How many points is a game of table tennis?", "11, win by 2. Serve changes every two points, and every point from 10-10."),
          ("How high do you have to toss the ball to serve?", "At least 16 cm, nearly straight up, from an open palm."),
          ("How much room do I need for a table tennis table?", "About 6 × 3 m for casual play; competition areas are 14 × 7 m.")]
page("table-tennis-rules.html", "Table Tennis Rules + Table Size: Serve, Scoring to 11, Net Height (Quiz) | Padel Glass Box",
     "Table tennis rules made simple: the 16 cm serve toss, scoring to 11, lets, doubles, plus the official table size (2.74 x 1.525 m, 76 cm high) and 15.25 cm net.", tt, tt_faq, "Table tennis rules")

# ---- Squash court ----
sq_lines = [(5.44, 0, 5.44, 6.4), (5.44, 3.2, 9.75, 3.2), (5.44, 1.6, 7.04, 1.6), (7.04, 0, 7.04, 1.6), (5.44, 4.8, 7.04, 4.8), (7.04, 4.8, 7.04, 6.4)]
sq = f"""<header class="hero"><div class="wrap"><h1>Squash court dimensions</h1>
<p class="lead">The floor, the wall lines and the tin of a regulation singles squash court, in metres and feet.</p>
{quick("A singles squash court is 9.75 m long and 6.40 m wide (32 × 21 ft). On the front wall, the out line is 4.57 m high, the service line 1.78 m and the top of the tin 0.48 m. The back wall out line is 2.13 m high. The short line is 5.44 m from the front wall and the service boxes are 1.60 m square.")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="card court-art">{court_svg(9.75, 6.4, sq_lines, "Squash court floor from above: 9.75 by 6.4 metres, with the short line 5.44 metres from the front wall, the half-court line to the back wall and two 1.6 metre service boxes.", colour="#b98a52", lc="#b3121b")}
<p style="margin-top:8px;color:#d6e2f2">Drawn to scale. Front wall on the left. Floor lines are red and 50 mm wide.</p></div></div></section>
<section><div class="wrap"><div class="sh"><h2>All the measurements</h2><p class="muted">World Squash singles court specification.</p></div>
{dim_table([("Floor (inside the walls)", "9.75 × 6.40 m", "32 × 21 ft"), ("Front wall out line (height)", "4.57 m", "15 ft"), ("Back wall out line (height)", "2.13 m", "7 ft"), ("Service line on the front wall", "1.78 m", "5 ft 10 in"), ("Top of the tin", "0.48 m", "19 in"), ("Short line from the front wall", "5.44 m", "17 ft 10 in"), ("Service boxes", "1.60 × 1.60 m", "5 ft 3 in square"), ("Line width", "50 mm", "2 in"), ("Minimum clear height above the floor", "5.64 m", "18 ft 6 in")])}
<p class="muted" style="margin-top:10px">The side wall out lines slope from the front wall line (4.57 m) down to the back wall line (2.13 m). Doubles courts are wider: 9.75 × 7.62 m.</p>
</div></div></section>
{AD.format("sq-court")}
{CMP}{compare_card("squash-court-dimensions.html")}"""
sq_faq = [("What are the dimensions of a squash court?", "9.75 m long and 6.40 m wide (32 × 21 ft) for singles."),
          ("How high is the tin in squash?", "The top of the tin is 0.48 m (19 in) from the floor on a standard court."),
          ("How high is the service line in squash?", "1.78 m (5 ft 10 in) on the front wall."),
          ("How far is the short line from the front wall?", "5.44 m (17 ft 10 in)."),
          ("How big is a squash service box?", "1.60 m square (about 5 ft 3 in), measured to the outside of the lines.")]
page("squash-court-dimensions.html", "Squash Court Dimensions: Floor Size, Wall Lines and Tin Height (m + ft) | Padel Glass Box",
     "Squash court dimensions on a scale diagram: 9.75 x 6.4 m floor, 4.57 m front wall line, 1.78 m service line, 0.48 m tin, short line and service boxes, in metres and feet.", sq, sq_faq, "Squash court dimensions")

COURT_PAGES = ["badminton-rules.html", "table-tennis-rules.html", "squash-court-dimensions.html", "pickleball-court-dimensions.html", "badminton-court-dimensions.html", "tennis-court-dimensions.html", "pickleball-rules.html"]
