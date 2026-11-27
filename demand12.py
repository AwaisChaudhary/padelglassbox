# ---------------- DEMAND RUN 15 (28 Nov 2026): padel court surfaces + surface checker ----------------
# Executed from demand11.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards, json).

cs = f'''<header class="hero"><div class="wrap"><h1>Padel court surfaces: what you are playing on, and how it plays.</h1>
<p class="lead">Most padel courts are artificial grass with sand, but not all grass is the same. Answer four quick questions about the court you play on and the checker tells you what surface it probably is, how the ball will bounce, which shoe sole grips best and one tactic that works on it.</p>
{quick("The official rules allow three kinds of padel court floor: artificial grass, other synthetic surfaces, and porous concrete or cement. Almost every club court today is artificial grass (10 to 15 mm pile) dressed with fine, rounded silica sand. More sand and shorter, straight monofilament fibres make a slower court with a lower bounce; less sand and taller, split fibrillated fibres play faster and livelier. The floor must be one colour: green, blue or terracotta (black is allowed indoors only).", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz" id="cs">
<div class="card">
{_bq2("cs", "where", "Where is the court?", [("in", "Indoors"), ("out", "Outdoors")], "out")}
{_bq2("cs", "sand", "Scuff the floor with your shoe. How much loose sand moves?", [("lots", "Lots, it sprays"), ("some", "A little"), ("none", "Almost none")], "some")}
{_bq2("cs", "fib", "Look closely at the grass fibres", [("mono", "Separate straight strands"), ("fibr", "Flat, split or curly ribbons"), ("flat", "No grass, hard floor"), ("dk", "Not sure")], "dk")}
{_bq2("cs", "cond", "How is it today?", [("dry", "Dry"), ("damp", "Damp or just dried"), ("worn", "Worn: flat fibres, bald patches")], "dry")}
</div>
<aside class="result" id="cs-out" aria-live="polite"><span class="pill b" id="cs-pill">Your court</span><h2 id="cs-h" style="margin-top:10px">Sand-filled artificial grass</h2><p id="cs-p"></p><dl class="spec" id="cs-spec"></dl><p id="cs-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="cs-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">A rule of thumb from what you can see and feel, not a lab test. Club staff can tell you the exact surface and when it was last resurfaced.</p></div></section>
{AD.format("cs-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What surface is a padel court made of?</h2></div>
<p>The FIP rules say the floor can be porous concrete or cement, a synthetic material, or artificial grass, as long as the ball bounces evenly and water does not collect on it. Artificial and synthetic grass should meet the Spanish UNE standard for padel surfaces. In practice nearly every new club court is sand-dressed artificial grass laid on a porous base. In the UK, LTA Padel's guidance asks for a single-colour, sand-dressed synthetic turf with monofilament as the preferred fibre.</p>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>Surface</th><th>What it looks like</th><th>How it plays</th><th>Where you find it</th></tr></thead><tbody>
<tr><td>Monofilament grass + sand</td><td>Separate, straight fibres standing up through the sand</td><td>Slower, lower and more even bounce; good grip</td><td>Most new club and competition courts</td></tr>
<tr><td>Fibrillated grass + sand</td><td>Flat ribbons that split into a net; can curl when old</td><td>Faster and a little livelier; wears faster</td><td>Older or lower-cost courts</td></tr>
<tr><td>Texturised (curly) grass, low sand</td><td>Short, crimped fibres, little loose sand</td><td>Quick, skidding ball; less sand to slip on</td><td>Some newer courts</td></tr>
<tr><td>Porous concrete or cement</td><td>Hard, rough, no fibres</td><td>Fast, high, true bounce; hard on the joints</td><td>Older outdoor courts</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Speed and bounce differences come from maker and installer guides (TigerTurf, Mondo) and the Padel Browser surfaces guide, which agree on the pattern. Exact feel depends on the product and how much sand is on it.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why does the sand matter?</h2></div><div class="grid">{_cards([
    ("It holds the fibres up", "Fine, rounded silica sand fills the grass so the fibres stand up and the ball bounces the same everywhere. Sharp sand cuts the fibres, so courts use rounded grains."),
    ("More sand = slower", "A freshly topped-up court with lots of sand plays slow and low, and the ball can skid. Feet slide more until the sand settles."),
    ("Less sand = faster", "When sand is thin, or pushed into the corners by wind and play, the ball comes through quicker and higher, and bare patches feel slippery."),
], pill="Sand")}</div>
<p class="muted" style="margin-top:12px">Clubs brush the court to spread the sand evenly (LTA Padel guidance says weekly) and top it up when it gets thin. If one side of the court plays differently from the other, uneven sand is the usual reason.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What colour is a padel court?</h2></div>
<p>The FIP rules allow <strong>green, blue or terracotta</strong>, in one even colour that stands out clearly from the walls. A black floor is allowed only indoors. The lines are 5 cm wide and are usually white. Outdoor courts fade in strong sun, which is normal and does not change the rules. All the court measurements are on the <a href="{href("court-dimensions.html")}">padel court dimensions</a> page.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Indoor vs outdoor padel courts: what is different?</h2></div>
<div class="tbl"><table><thead><tr><th>Thing</th><th>Indoor</th><th>Outdoor</th></tr></thead><tbody>
<tr><td>Floor colour</td><td>Green, blue, terracotta or black</td><td>Green, blue or terracotta</td></tr>
<tr><td>Glass (LTA 2025 guidance)</td><td>10 mm toughened glass</td><td>12 mm toughened glass (12 mm is the UK minimum for any court)</td></tr>
<tr><td>Ceiling or obstacles (FIP)</td><td>At least 6 m clear height over the whole court; 8 m suggested for new halls</td><td>Open sky, but lights and trees must not overhang the court</td></tr>
<tr><td>Lighting for club play</td><td>300 lux or more (FIP, local play)</td><td>200 to 300 lux or more (FIP and LTA, recreational)</td></tr>
<tr><td>Base</td><td>Usually a level slab</td><td>Free-draining stone and porous asphalt so rain drains through</td></tr>
<tr><td>How it plays</td><td>The same every day; balls stay lively; dust can make sand pack hard</td><td>Changes with rain, cold, wind and sun: see the <a href="{href("padel-weather.html")}">weather checker</a></td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which shoes for which padel surface?</h2></div>
<div class="tbl"><table><thead><tr><th>Surface</th><th>Sole to look for</th><th>Why</th></tr></thead><tbody>
<tr><td>Grass with lots of sand</td><td>Herringbone (zig-zag)</td><td>The grooves let sand pass through, so the sole bites</td></tr>
<tr><td>Grass with little sand, texturised grass</td><td>Omni (small studs) or hybrid</td><td>More rubber touches the fibres; less skidding on thin sand</td></tr>
<tr><td>Concrete or cement</td><td>Hard-court or hybrid, well cushioned</td><td>Grip on a hard floor and protection for knees and ankles</td></tr>
<tr><td>Any court</td><td>Not running shoes</td><td>Running soles are made for forward motion and slip when you move sideways</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Not sure? Answer four questions in the <a href="{href("padel-shoes.html")}">padel shoe finder</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How long does a padel court surface last?</h2></div>
<p>LTA Padel tells UK venues to plan to replace the surface about every <strong>5 years</strong>, depending on how busy the court is, and to brush it every week. Installer and industry guides give a similar 4 to 6 years, with a deep clean once or twice a year. Signs a court needs work:</p>
<div class="grid" style="margin-top:14px">{_cards([
    ("Flat, shiny fibres", "The grass lies down in the busy areas (behind the service lines and at the net) and the ball skids or dies."),
    ("Bald or lifting patches", "You can see the backing, or seams lift. These spots are slippery and can catch a foot."),
    ("Odd bounces", "The ball bounces differently in different areas, often because the sand is uneven or packed hard."),
], pill="Sign")}</div>
<p class="muted" style="margin-top:12px">Tell the club if you see a lifting seam or a puddle that does not drain: they are safety issues, not just playing issues. Building or pricing a court? See the <a href="{href("padel-court-cost.html")}">padel court cost calculator</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Get the right grip</h3><p>Herringbone, omni or hybrid in four questions: the <a href="{href("padel-shoes.html")}">padel shoe finder</a>.</p></div>
<div class="card"><h3>Slow court tactics</h3><p>On a slow, sandy court the lob and the patient game win: <a href="{href("padel-lob.html")}">how to hit a lob</a> and the <a href="{href("padel-tactics.html")}">tactics trainer</a>.</p></div>
<div class="card"><h3>Fresh balls help</h3><p>Flat balls die on slow courts first. Check yours: <a href="{href("padel-balls.html")}">when to change padel balls</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Gear for your surface</h3><p>Check the sole pattern in the product details before you buy.</p><ul class="aff-links"><li><a href="{go("padel-shoes")}" {AFF_ATTR}>Padel shoes (herringbone, omni, hybrid)</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Padel balls</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: FIP / IPF Padel Game Regulations (ground surfaces: porous concrete or cement, synthetic or artificial grass; green, blue or terracotta, black indoors only; lines 5 cm; 6 m minimum clear height; lighting levels), LTA "Padel court guidance" datasheet and LTA "Padel court construction guidance note 2025" (sand-dressed synthetic turf, monofilament preferred, 10 mm indoor / 12 mm outdoor glass, free-draining base, weekly brushing, resurface about every 5 years), Padel Browser "Padel court surfaces explained" (21 Sep 2026), TigerTurf UK and Mondo surface guides (pile 10 to 15 mm, monofilament vs fibrillated, sand and speed). The checker's rules are our own simple rules of thumb.</p></div></section>'''
cs_faq = [
    ("What surface is a padel court?", "Usually artificial grass dressed with fine silica sand. The official rules also allow other synthetic surfaces and porous concrete or cement."),
    ("Why is there sand on a padel court?", "The sand holds the grass fibres up, gives an even bounce and lets rain drain. More sand makes the court slower and the bounce lower."),
    ("What is the difference between monofilament and fibrillated padel grass?", "Monofilament has separate straight fibres and plays slower with a more even bounce; it lasts longer. Fibrillated has flat, split ribbons, plays a bit faster and wears out sooner."),
    ("What colour should a padel court be?", "Green, blue or terracotta, in one even colour that contrasts with the walls. Black is allowed only on indoor courts."),
    ("Are indoor padel courts faster than outdoor courts?", "Often a little, because they stay dry and the balls stay lively, but the surface and the amount of sand matter more than the roof."),
    ("How often should a padel court be resurfaced?", "About every 5 years on a busy court, according to LTA Padel guidance, with weekly brushing and sand top-ups in between."),
    ("What shoes are best for a sandy padel court?", "Padel shoes with a herringbone (zig-zag) sole. On courts with little sand, an omni or hybrid sole grips better."),
]
page("padel-court-surfaces.html", "Padel Court Surfaces: Grass, Sand, Colours + Checker",
     "Padel court surfaces explained: artificial grass, sand, monofilament vs fibrillated, colours, indoor vs outdoor, shoes per surface and a free court checker.",
     cs, cs_faq, "Court surfaces")

DEMAND_PAGES += ["padel-court-surfaces.html"]
