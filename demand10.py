# ---------------- DEMAND RUN 13 (27 Nov 2026): padel rules quiz, junior padel parents' guide + planner ----------------
# Executed from demand9.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards).

# ---------- 1. PADEL RULES QUIZ ----------
# Each question: (question, [options], index of correct option, explanation, page slug for more)
RQ = [
    ("How must you hit the serve in padel?", ["Overhead, like tennis", "After one bounce, at or below waist height", "Straight from your hand, at any height"], 1,
     "The ball must bounce once on your side, behind the service line, and you hit it at or below your waist with at least one foot on the ground.", "serve-rules"),
    ("Where must the serve land?", ["Anywhere on the other side", "In the service box straight ahead", "In the service box diagonally opposite"], 2,
     "Like tennis, the serve goes diagonally into the box across the net. A ball on the line is good.", "serve-rules"),
    ("Your serve bounces in the right box, then hits the metal fence. What is it?", ["A good serve", "A fault", "A let, serve again"], 1,
     "After bouncing in the box, the serve may hit the glass, but not the metal mesh. Bounce then fence is a fault.", "serve-rules"),
    ("Your serve clips the net and lands in the right box. What happens?", ["You lose the point", "It is a let: serve again", "It is good, play on"], 1,
     "A net cord serve that lands in the right box (and doesn't then hit the fence) is a let. You replay that serve.", "net-rules"),
    ("Can the receiver volley the serve before it bounces?", ["Yes, if they are at the net", "No, the serve must bounce first", "Only on a second serve"], 1,
     "The receiver must let the serve bounce. After the return, both teams may volley freely.", "rules"),
    ("Your shot crosses the net and hits their back glass before it bounces. Who wins the point?", ["You do", "They do", "Play a let"], 1,
     "Your shot must bounce on their ground first. Hitting their glass or fence before the bounce loses you the point.", "wall-rules"),
    ("The ball bounces on your side, hits your back glass and comes out. Can you still play it?", ["Yes, before it bounces again", "No, the point is over", "Only if it reaches the net"], 0,
     "After one bounce on your side the ball may hit your glass as often as it likes. You must hit it before the second bounce.", "wall-rules"),
    ("Can you hit the ball into your own back glass to get it over the net?", ["Yes, that is a normal shot", "No, it loses the point", "Only on the serve"], 0,
     "Playing the ball into your own glass and back over the net is allowed and is a common way out of the corner.", "wall-rules"),
    ("Can you hit the ball into your own metal fence to get it over?", ["Yes, the same as the glass", "No, you lose the point", "Yes, but only once per rally"], 1,
     "Only your glass may be used to send the ball back. Hitting your own metal mesh loses the point.", "wall-rules"),
    ("Your racket touches the net during the rally. What happens?", ["Nothing, if the ball was already over", "You lose the point", "Replay the point"], 1,
     "Touching the net, the posts or the other side's court with your body, clothes or racket while the ball is in play loses the point.", "net-rules"),
    ("The ball hits your partner before it bounces. Whose point is it?", ["Yours, it was an accident", "The other team's", "Replay it"], 1,
     "If the ball touches you or your partner (except your racket) while it is in play, you lose the point.", "rules"),
    ("How many serve attempts do you get per point?", ["One", "Two", "Three"], 1,
     "You get two tries. Miss both and you lose the point (a double fault).", "serve-rules"),
    ("What is the golden point?", ["A point worth double", "At 40-40, one deciding point wins the game", "The first point of a tie-break"], 1,
     "With the golden point there is no advantage: at deuce the next point wins the game. The receiving pair chooses which side receives.", "golden-point-star-point"),
    ("When is a tie-break played in a set?", ["At 5-5", "At 6-6", "At 7-7"], 1,
     "At 6 games all you play a tie-break: first to 7 points, 2 points clear.", "tie-break"),
    ("Your opponents' shot bounces and flies out over the wall. Can you run out and play it back?", ["Never, the point is over", "Yes, where the club and event allow out-of-court play", "Only on the serve"], 1,
     "Out-of-court play is allowed by the rules when the court has open exits and the event allows it. Many clubs and courts do not, so agree before you play.", "out-of-court-play"),
]

def _rq_html():
    out = []
    for i, (q, opts, c, why, slug) in enumerate(RQ):
        b = "".join(f'<button type="button" class="opt" data-v="{j}">{e(o)}</button>' for j, o in enumerate(opts))
        out.append(f'<div class="rq-q" data-rq="{i}" data-c="{c}" data-l="{slug}"{"" if i == 0 else " hidden"}><p class="muted" style="margin:0 0 6px">Question {i + 1} of {len(RQ)}</p><h3>{e(q)}</h3>'
                   f'<div class="opts" role="group" aria-label="{e(q)}">{b}</div><p class="rq-why" hidden>{e(why)}</p></div>')
    return "".join(out)

rqz = f'''<header class="hero"><div class="wrap"><h1>Padel rules quiz: how well do you know the rules?</h1>
<p class="lead">Fifteen quick questions on the serve, the walls, the net and the scoring. Each answer comes with a short explanation and a link to the full rule, so you learn as you go. Good for beginners, club players and anyone who argues about calls.</p>
{quick("The rules most players get wrong: the serve must bounce and be hit at or below the waist; a serve that bounces in the box and then hits the metal fence is a fault; your shot must bounce on their ground before it touches their glass; and you may play the ball into your own glass, but not your own fence. Test yourself with the 15-question quiz below.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card" id="rq"><div class="prog" aria-hidden="true"><i id="rq-bar" style="width:0%"></i></div>{_rq_html()}
<div class="btns" style="margin-top:14px"><button class="btn lime sm" type="button" id="rq-next" hidden>Next question</button></div></div>
<aside class="result" id="rq-out" aria-live="polite"><span class="pill b" id="rq-pill">Score</span><h2 id="rq-h" style="margin-top:10px">0 / 0</h2><p id="rq-p">Pick an answer to start. You see the right answer and why straight away.</p><p id="rq-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="rq-copy" hidden>Copy my score</button><button class="btn sm ghost" type="button" id="rq-again" hidden>Try again</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">Questions follow the FIP rules of padel as explained on our rules pages. Local clubs and leagues can add their own rules (for example on out-of-court play or the deciding point), so check before a match.</p></div></section>
{AD.format("rq-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which padel rules do players get wrong most?</h2></div>
<div class="tbl"><table><thead><tr><th>Myth</th><th>The actual rule</th><th>Full rule</th></tr></thead><tbody>
<tr><td>"You can serve overhead."</td><td>No. Bounce it, then hit at or below the waist.</td><td><a href="{href("serve-rules.html")}">Serve checker</a></td></tr>
<tr><td>"Serve into the fence after the bounce is fine."</td><td>No. Glass is fine, the metal fence is a fault.</td><td><a href="{href("serve-rules.html")}">Serve checker</a></td></tr>
<tr><td>"Any wall is fine once it's over the net."</td><td>No. It must bounce on their ground before it touches their glass or fence.</td><td><a href="{href("wall-rules.html")}">Wall checker</a></td></tr>
<tr><td>"You can use your own fence like the glass."</td><td>No. Only your own glass can be used to send the ball back.</td><td><a href="{href("wall-rules.html")}">Wall checker</a></td></tr>
<tr><td>"Brushing the net doesn't count if you didn't mean it."</td><td>It counts. Any touch while the ball is in play loses the point.</td><td><a href="{href("net-rules.html")}">Net checker</a></td></tr>
<tr><td>"Deuce is always advantage."</td><td>The organiser decides: advantage, golden point or Star Point.</td><td><a href="{href("golden-point-star-point.html")}">Deciding points</a></td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Using the quiz with a group or club</h2></div><div class="grid">
<div class="card"><h3>Beginner sessions</h3><p>Run it on a phone at the start of a first lesson. The explanations cover what new players need before their first match.</p></div>
<div class="card"><h3>Club social</h3><p>Pairs answer together and compare scores. Use "Copy my score" to post results in your club chat.</p></div>
<div class="card"><h3>Settle an argument</h3><p>For a real call in a real match, the step-by-step checkers are faster: <a href="{href("serve-rules.html")}">serve</a>, <a href="{href("wall-rules.html")}">walls</a>, <a href="{href("net-rules.html")}">net</a> and <a href="{href("out-of-court-play.html")}">out of court</a>.</p></div>
</div>
<p class="muted" style="margin-top:14px">All the rules on one page: <a href="{href("rules.html")}">padel rules explained</a>. Keep score while you play with the <a href="{href("score.html")}">padel score keeper</a>.</p></div></section>'''
rqz_faq = [
    ("What are the main rules of padel?", "Serve underhand after one bounce, at or below the waist, diagonally into the box. The receiver lets it bounce. In the rally your shot must bounce on the other side before touching their walls. You may use your own glass but not your own fence. Scoring is like tennis."),
    ("Is a serve that hits the fence a fault in padel?", "Yes, if it bounces in the service box and then hits the metal fence. If it bounces in the box and hits the glass, the serve is good."),
    ("Can you hit the ball off your own wall in padel?", "Yes, off your own glass. You may hit the ball into your own glass so it goes back over the net. You may not hit it into your own metal fence."),
    ("Can you volley the serve in padel?", "No. The receiver must let the serve bounce first. After the return, players can volley."),
    ("What happens if you touch the net in padel?", "You lose the point, if the ball is still in play. That includes your racket, body and clothes."),
    ("Is there a padel rules test?", "Yes, this free 15-question quiz checks the serve, wall, net and scoring rules, with an explanation for each answer."),
]
page("padel-rules-quiz.html", "Padel Rules Quiz: 15 Questions to Test Yourself",
     "Free padel rules quiz: 15 questions on the serve, walls, fence, net and scoring, with an explanation and the full rule for every answer. Copy your score.",
     rqz, rqz_faq, "Rules quiz")

# ---------- 2. JUNIOR PADEL: PARENTS' GUIDE + STARTER PLANNER ----------
jp = f'''<header class="hero"><div class="wrap"><h1>Junior padel: a guide for parents, plus a starter planner.</h1>
<p class="lead">Thinking of getting your child into padel? Tell the planner their age, experience and goal. It suggests the racket weight, ball, session length, scoring and the next step into junior competitions in the UK, the US or abroad.</p>
{quick("Children can start padel young: the US federation's junior guide suggests groups from age 5 to 8, 7 to 12 and 12 to 18. For young beginners use a light junior racket, foam or low-compression balls, sessions of 30 to 60 minutes in groups of 4 to 8, and simple rally scoring before full padel scoring. In the UK, the next step is LTA Team Challenge and then the LTA Youth Tour, where juniors earn LTA ranking points.", "2026-11-27")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card">
{_bq2("jp", "age", "How old is your child?", [("u8", "5 to 7"), ("u12", "8 to 11"), ("u14", "12 to 13"), ("u18", "14 to 17")], "u12")}
{_bq2("jp", "exp", "Have they played padel or tennis?", [("new", "Never"), ("some", "A few times"), ("reg", "Every week")], "new")}
{_bq2("jp", "goal", "What do they want from it?", [("fun", "Fun with friends"), ("better", "Get better"), ("comp", "Play tournaments")], "fun")}
{_bq2("jp", "where", "Where do you live?", [("uk", "UK"), ("us", "US"), ("other", "Elsewhere")], "uk")}
</div>
<aside class="result" id="jp-out" aria-live="polite"><span class="pill b" id="jp-pill">Starter plan</span><h2 id="jp-h" style="margin-top:10px">Junior plan</h2><p id="jp-p"></p><dl class="spec" id="jp-spec"></dl><p id="jp-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="jp-copy">Copy plan</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">A starting point, not coaching advice. A qualified coach at your club can judge what your child is ready for.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What age can a child start padel?</h2></div>
<p>There is no official minimum age. The smaller court, the walls that keep the ball in play and the underarm serve make padel easier to start than tennis. The US Padel Association's guide for clubs starting a junior programme suggests two groups to begin with, <strong>under 12 (ages 7 to 12)</strong> and <strong>under 18 (ages 12 to 18)</strong>, then splitting into <strong>under 8 (ages 5 to 8)</strong> and <strong>under 14 (ages 9 to 14)</strong> as numbers grow. UK junior national events use 12U, 14U, 16U and 18U age groups.</p>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>Age</th><th>Racket weight to look for</th><th>Ball</th><th>Session</th></tr></thead><tbody>
<tr><td>5 to 7</td><td>Lightest junior racket (well under 300 g)</td><td>Foam or low-compression</td><td>30 to 45 minutes, lots of games</td></tr>
<tr><td>8 to 11</td><td>About 260 to 330 g, round shape</td><td>Low-compression to start</td><td>About 60 minutes</td></tr>
<tr><td>12 to 13</td><td>About 300 to 355 g</td><td>Normal ball once rallies last</td><td>60 minutes</td></tr>
<tr><td>14 to 17</td><td>Light adult racket (about 340 to 360 g)</td><td>Normal ball</td><td>60 to 90 minutes for keen players</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Weights are general guidance; height and strength matter more than age. Find the exact band with the <a href="{href("padel-racket-for-kids.html")}">padel racket for kids finder</a>.</p></div></section>
{AD.format("jp-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How should a junior padel session work?</h2></div><div class="grid">{_cards([
    ("Safe, fun, learn", "The US federation's guide puts it in that order: be safe, have fun, learn. A child who enjoys the first sessions comes back."),
    ("Small groups", "Four to eight children per coach is the size the guide calls ideal for under-12s, so everyone gets plenty of hits."),
    ("Short sessions", "Sixty minutes is standard. Ninety minutes suits older, keen players, but is usually too long for beginners or under-12s. First taster sessions can be 30 to 45 minutes."),
    ("Rallies, not queues", "Avoid long lines of children waiting for one feed. Short mini-rallies of 3 to 5 shots keep everyone moving."),
    ("Easy rules first", "Let beginners play the ball after two bounces and use simple rally scoring. Full padel scoring and the walls can come later."),
    ("Softer balls", "Foam or low-compression balls bounce slower and lower, so small children can reach them and rallies last longer."),
], pill="Tip")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Junior padel competitions: where to start</h2></div><div class="grid">
<div class="card"><span class="pill i">UK</span><h3 style="margin-top:10px">LTA Team Challenge</h3><p>Fun team matches with friends at your local venue. The LTA describes it as a way to introduce children to padel competition.</p></div>
<div class="card"><span class="pill i">UK</span><h3 style="margin-top:10px">LTA Youth Tour</h3><p>The first step where juniors earn LTA ranking points. Matches use a simple, fast format, so a tournament usually lasts about half a day. Find events on the LTA competitions search.</p></div>
<div class="card"><span class="pill i">UK</span><h3 style="margin-top:10px">Junior National Championships</h3><p>The first LTA Junior Padel National Championships were held in Derby in autumn 2026, with 128 players across eight events: boys and girls 12U, 14U, 16U and 18U.</p></div>
<div class="card"><span class="pill b">US</span><h3 style="margin-top:10px">USPA junior events</h3><p>In the US Padel Association's junior pathway, children who reach the "match play ready" stage can enter USPA junior tournaments.</p></div>
<div class="card"><span class="pill a">World</span><h3 style="margin-top:10px">FIP junior events</h3><p>International junior tournaments are run by the International Padel Federation (FIP), and entries go through the FIP website.</p></div>
</div>
<p class="muted" style="margin-top:14px">Run a junior event yourself with the <a href="{href("padel-group-stage-generator.html")}">group stage generator</a> or the <a href="{href("americano.html")}">Americano generator</a>. Teach the basics with the <a href="{href("padel-rules-quiz.html")}">padel rules quiz</a> and <a href="{href("beginners.html")}">beginner's guide</a>.</p></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Junior kit</h3><p>Check the weight on the product page against the planner above before you buy.</p><ul class="aff-links"><li><a href="{go("padel-rackets")}" {AFF_ATTR}>Rackets (check the weight)</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 27 Nov 2026: US Padel Association "How to start a junior padel program" (2026, edition 1.0: age groups, class size 4 to 8, 60-minute sessions, 90 too long for under-12s, double bounce and rally scoring for beginners, foam or low-compression balls, junior tournaments), LTA Padel "Youth padel competitions" and LTA support centre "What is the LTA Padel Youth Tour" (Team Challenge, Youth Tour ranking points, half-day format, FIP entries for international events), LTA Padel news 4 Nov 2026 (first Junior Padel National Championships, Derby, 128 players, eight events), David Lloyd Clubs "How to get kids into padel" (lighter rackets, softer balls, scoring can wait). Racket weights from our junior racket finder.</p></div></section>'''
jp_faq = [
    ("What age can kids start playing padel?", "There is no official minimum age. The US Padel Association's junior guide includes a group for ages 5 to 8, and UK junior events start at 12U. Young children do best with a light racket, soft balls and short sessions."),
    ("Is padel good for kids?", "Yes. The small court, walls that keep the ball in play and underarm serve mean children get long rallies sooner than in many racket sports, and it is played in pairs, so it is social."),
    ("What size padel racket does a child need?", "Junior rackets differ mostly in weight. As a rough guide: about 260 to 300 g for ages 7 to 9, 300 to 330 g for 10 to 12 and 330 to 355 g for 13 to 14. Use our junior racket finder for your child's height."),
    ("How long should a kids' padel session be?", "About 60 minutes. The US federation's guide says 90 minutes is usually too long for beginners and under-12s; first taster sessions can be 30 to 45 minutes."),
    ("Are there junior padel tournaments in the UK?", "Yes. LTA Team Challenge introduces team matches, the LTA Youth Tour gives juniors their first LTA ranking points in half-day events, and there are LTA Junior Padel National Championships in 12U to 18U age groups."),
    ("What balls should kids use for padel?", "Foam or low-compression balls for young beginners, because they bounce slower and lower. Move to normal padel balls once rallies last."),
]
page("junior-padel.html", "Junior Padel: Parents' Guide, Ages, Kit and Competitions",
     "Junior padel for parents: what age kids can start, racket weight by age, softer balls, session length, junior competitions and a free starter planner.",
     jp, jp_faq, "Junior padel")

DEMAND_PAGES += ["padel-rules-quiz.html", "junior-padel.html"]
exec((ROOT / "demand11.py").read_text())
