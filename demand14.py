# ---------------- DEMAND RUN 17 (28 Nov 2026): padel bag picker, control vs power racket test, padel racket for women ----------------
# Executed from demand13.py (shares page(), quick(), href(), e(), AD, go(), AFF_ATTR, AFF_NOTE, _bq2, _cards, json).

# ---------- 1. PADEL BAGS ----------
bg = f'''<header class="hero"><div class="wrap"><h1>Padel bags: which bag do you need? A quick bag picker and buying guide.</h1>
<p class="lead">Racket bag, backpack or just a cover? Answer four questions about how many rackets you carry, how you get to the court and what else you bring. You get the bag type, the size to look for and whether a thermal pocket is worth paying for.</p>
{quick("Most club players need a padel backpack (about 20 to 30 litres, 1 or 2 rackets) or a medium racket bag (2 or 3 rackets, about 35 to 45 litres). Pick a bag with a thermal racket pocket if your bag sits in a car or you play in very hot or cold weather, and a separate shoe pocket to keep court sand off your clothes. Large racket bags (up to about 6 rackets) and wheeled bags are for competition players.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card">
{_bq2("bg", "rk", "How many rackets do you take?", [("1", "1 racket"), ("2", "2 or 3"), ("4", "4 or more")], "1")}
{_bq2("bg", "go", "How do you get to the court?", [("walk", "Walk, bike or train"), ("car", "Car, and the bag stays in it"), ("fly", "Flights and padel trips")], "walk")}
{_bq2("bg", "kit", "What else goes in the bag?", [("min", "Balls, grip, water"), ("shoe", "Plus court shoes"), ("full", "Shoes, change of clothes, towel")], "shoe")}
{_bq2("bg", "lvl", "How often do you play?", [("1", "Once a week or less"), ("2", "2 to 3 times a week"), ("4", "Tournaments or 4+ a week")], "1")}
</div>
<aside class="result" id="bg-out" aria-live="polite"><span class="pill b">Your bag</span><h2 id="bg-h" style="margin-top:10px">Padel backpack</h2><p id="bg-p"></p><dl class="spec" id="bg-spec"></dl><p id="bg-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="bg-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">General buying guidance with no brand claims. Check the product page for racket capacity and litres before you buy.</p></div></section>
{AD.format("bg-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What types of padel bag are there?</h2></div>
<div class="tbl"><table><thead><tr><th>Type</th><th>Rackets</th><th>Typical size</th><th>Best for</th></tr></thead><tbody>
<tr><td>Racket cover</td><td>1</td><td>Racket plus a small pocket</td><td>Protecting one racket inside another bag</td></tr>
<tr><td>Padel backpack</td><td>1, sometimes 2 (tight)</td><td>About 20 to 30 litres</td><td>Most social players, walking, cycling, train</td></tr>
<tr><td>Medium racket bag</td><td>2 to 3</td><td>About 35 to 45 litres</td><td>Regular players with shoes and a change of clothes</td></tr>
<tr><td>Large racket bag</td><td>Up to about 6</td><td>About 45 to 55+ litres</td><td>Competition players, coaches, sharing with a partner</td></tr>
<tr><td>Wheeled bag</td><td>Many</td><td>Large</td><td>Tournaments and travel with heavy kit</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Racket counts follow Padel Market's small, medium and large bag sizes; litre bands follow Decathlon's and Stubble &amp; Co's guides. Brands measure differently, so treat these as rough ranges.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Do you need a thermal compartment in a padel bag?</h2></div>
<p>A thermal pocket is a lined racket compartment that slows down heat and cold getting to the racket. Padel rackets have a foam (EVA) core and resin in the face, and shop guides warn that big temperature changes, such as a hot car boot in summer or a freezing one in winter, are bad for them.</p>
<div class="grid" style="margin-top:14px">{_cards([
    ("Worth it", "Your bag stays in the car between matches, you play outdoors in hot summers or cold winters, or your racket was expensive."),
    ("Nice to have", "You go straight from home to the court and back, and the bag spends most of its time indoors."),
    ("What it is not", "A thermal pocket protects from temperature, not from knocks. A padded racket pocket and a frame protector handle bumps."),
], pill="Thermal")}</div>
<p style="margin-top:12px">Even with a thermal pocket, take the bag inside after you play. More on looking after your racket: <a href="{href("racket-care.html")}">padel racket care</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What should a good padel bag have?</h2></div>
<div class="tbl"><table><thead><tr><th>Feature</th><th>Why it matters</th></tr></thead><tbody>
<tr><td>Padded racket pocket</td><td>Stops the frame and face getting knocked against keys, bottles and the car boot</td></tr>
<tr><td>Separate shoe pocket, ideally vented</td><td>Court shoes carry sand and sweat; a separate pocket keeps clean clothes clean and stops smells</td></tr>
<tr><td>Thermal racket pocket</td><td>Protects the racket from heat and cold (see above)</td></tr>
<tr><td>Small valuables pocket</td><td>Phone, keys and wallet stay in one place on the bench</td></tr>
<tr><td>Bottle holder</td><td>Water within reach at the change of ends</td></tr>
<tr><td>Water-resistant fabric and covered zips</td><td>Outdoor courts and rainy walks to the club</td></tr>
<tr><td>Padded straps</td><td>A full bag with two rackets and shoes gets heavy</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel backpack or racket bag: which is better?</h2></div><div class="grid">{_cards([
    ("Backpack", "Light, hands-free and easy on a bike or the train. Fits one racket well. Two rackets plus shoes is a squeeze."),
    ("Racket bag", "Long holdall with a big racket section, so 2 to 6 rackets fit with shoes and clothes. Bulkier to carry, best if you drive."),
    ("Our view", "Start with a backpack. Move to a medium racket bag once you own two rackets or bring a full change of clothes every time."),
], pill="Option")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>What to pack</h3><p>Build a packing list for your match with the <a href="{href("padel-equipment.html")}">padel equipment checklist</a>.</p></div>
<div class="card"><h3>Shoes for your court</h3><p>Herringbone, omni or clay sole? Check the <a href="{href("padel-shoes.html")}">padel shoes guide</a>.</p></div>
<div class="card"><h3>A gift idea</h3><p>A bag is a safe present. More ideas by budget: <a href="{href("padel-gifts.html")}">padel gift finder</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop padel bags</h3><p>Check racket capacity, litres, a thermal pocket and a shoe pocket on each product page.</p><ul class="aff-links"><li><a href="{go("padel-bags")}" {AFF_ATTR}>Padel bags and backpacks</a></li><li><a href="{go("padel-black-friday")}" {AFF_ATTR}>Black Friday padel deals</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-balls")}" {AFF_ATTR}>Balls</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: Decathlon UK "How to choose your padel bag" (bag types, thermal pocket for regular players, backpacks about 30 L, padel bags 35 to 54 L), Padel Market "Best padel bags and backpacks guide" (5 Jun 2026: small 1 racket, medium 2 to 3, large up to 6; heat and cold in a car affect the resin and EVA core; ventilated shoe compartment), Stubble &amp; Co "How to choose a padel bag" (24 Jul 2026: 30 to 40 L suits most players, separate shoe compartment). Written in our own words; the picker's rules are our own.</p></div></section>'''
bg_faq = [
    ("What size padel bag do I need?", "Most players need a backpack of about 20 to 30 litres for one racket, or a medium racket bag of about 35 to 45 litres for two or three rackets plus shoes and clothes."),
    ("How many rackets fit in a padel bag?", "A backpack fits one racket well and two only tightly. Medium racket bags hold two or three, and large ones up to about six."),
    ("Do I need a thermal padel bag?", "It is worth it if your bag stays in a car or you play in very hot or cold weather, because heat and cold can harm the racket's foam core and resin. If you go straight to the court and back, it is a nice extra."),
    ("Is a padel backpack or racket bag better?", "A backpack is lighter and better for walking, cycling or the train with one racket. A racket bag is better if you carry two or more rackets, a full change of clothes, or you drive."),
    ("Can I use a tennis bag for padel?", "Yes, if the racket pocket fits a padel racket and protects it. Padel rackets are shorter and thicker than tennis rackets, so check the pocket depth."),
    ("Should I leave my padel racket in the car?", "Try not to. Hot and cold car boots are bad for rackets. If you must, use a thermal pocket and take it inside as soon as you can."),
]
page("padel-bags.html", "Padel Bags: Bag Picker + Which Size and Type to Buy",
     "Which padel bag do you need? Free bag picker: backpack vs racket bag, size in litres, how many rackets fit, and when a thermal pocket is worth it.",
     bg, bg_faq, "Padel bags")

# ---------- 2. CONTROL VS POWER RACKET ----------
cp = f'''<header class="hero"><div class="wrap"><h1>Control vs power padel racket: which one suits your game?</h1>
<p class="lead">Take the seven-question test. It places you on a scale from control to power and gives you the shape, balance, weight, core and face to look for. If you're unsure, the advice from every guide we checked is the same: start with control.</p>
{quick("A control racket is usually round, with a low (head-light) balance, a large central sweet spot and a soft core: it is forgiving and easy to place. A power racket is usually diamond-shaped, head-heavy, with a smaller, higher sweet spot and a firmer core: it hits harder overheads but punishes off-centre hits. Teardrop rackets sit in between. Beginners, players with arm pain and right-side (forehand side) players usually suit control; experienced left-side finishers often choose power.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card">
{_bq2("cp", "lvl", "How long have you played?", [("0", "Under 1 year"), ("1", "1 to 3 years"), ("2", "3+ years, competing")], "0")}
{_bq2("cp", "win", "How do you usually win points?", [("0", "Opponents' errors, long rallies"), ("1", "A mix"), ("2", "My smashes and fast volleys")], "1")}
{_bq2("cp", "side", "Which side do you play?", [("0", "Right (forehand side)"), ("1", "Both or not sure"), ("2", "Left (backhand side)")], "1")}
{_bq2("cp", "ovh", "Do your overheads land where you aim?", [("0", "Not often"), ("1", "Sometimes"), ("2", "Most of the time")], "0")}
{_bq2("cp", "miss", "Do you often hit off-centre?", [("0", "Yes, quite often"), ("1", "Sometimes"), ("2", "Rarely")], "1")}
{_bq2("cp", "arm", "Any elbow, wrist or shoulder pain?", [("x", "Yes, now or recently"), ("0", "Sometimes"), ("2", "No")], "2")}
{_bq2("cp", "freq", "How often do you play?", [("0", "Once a week or less"), ("1", "2 times a week"), ("2", "3+ times a week")], "0")}
</div>
<aside class="result" id="cp-out" aria-live="polite"><span class="pill b">Your racket type</span><h2 id="cp-h" style="margin-top:10px">Control</h2>
<div class="cp-scale" aria-hidden="true"><i id="cp-dot"></i></div><div class="cp-lab"><span>Control</span><span>Hybrid</span><span>Power</span></div>
<p id="cp-p"></p><dl class="spec" id="cp-spec"></dl><p id="cp-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="cp-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">General guidance, not a brand recommendation. The test's scoring is our own rule of thumb based on what the guides below agree on.</p></div></section>
{AD.format("cp-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What is the difference between a control and a power padel racket?</h2></div>
<div class="tbl"><table><thead><tr><th>Spec</th><th>Control</th><th>Hybrid (all-round)</th><th>Power</th></tr></thead><tbody>
<tr><td>Shape</td><td>Round</td><td>Teardrop</td><td>Diamond</td></tr>
<tr><td>Balance</td><td>Low, towards the handle</td><td>Medium, even</td><td>High, towards the head</td></tr>
<tr><td>Sweet spot</td><td>Large, in the centre</td><td>Medium</td><td>Smaller, higher up the face</td></tr>
<tr><td>Core</td><td>Soft (soft EVA or foam)</td><td>Medium</td><td>Firmer (high-density EVA)</td></tr>
<tr><td>Typical weight</td><td>About 340 to 360 g</td><td>About 355 to 370 g</td><td>About 360 to 375 g</td></tr>
<tr><td>Feels</td><td>Forgiving, easy to place, kind to the arm</td><td>A bit of each</td><td>Punchy on overheads, less forgiving</td></tr>
<tr><td>Suits</td><td>Beginners, defenders, right-side players, sore arms</td><td>Improving players, both sides</td><td>Experienced attackers, left-side finishers</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">Shape, balance and sweet spot: HEAD, Padel Market and Padel USA agree. Weight bands follow HEAD's guidance (340 to 360 g for beginners and intermediates, 360 to 375 g for advanced players). Every racket mixes features, so read the balance and core on the product page, not just the shape.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Does a power racket make you hit harder?</h2></div>
<p>Only if you hit the sweet spot with good technique. A head-heavy diamond racket adds speed to a well-timed smash, but its sweet spot is smaller and higher, so off-centre hits lose pace and control. For a player whose overheads don't land yet, a control racket often wins more points. Padel USA's advice puts it simply: move to power once your overheads land where you aim them.</p>
<p style="margin-top:10px">Core hardness is not a simple power switch either. A hard core gives more speed to a fast, full swing; with a slower swing, a soft core can send the ball deeper because it gives more bounce back. Learn more about cores and faces: <a href="{href("padel-racket-materials.html")}">racket materials explained</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Carbon or fibreglass: which face is more powerful?</h2></div><div class="grid">{_cards([
    ("Carbon face", "Stiffer and more durable, with a direct, precise feel. It needs a good swing to make it fly."),
    ("Fibreglass face", "Softer and more flexible, so the ball comes off with more help on slow shots and it feels comfortable."),
    ("Rough face", "A gritty, textured face helps add spin to bandejas, víboras and kick smashes. It does not change control or power much on its own."),
], pill="Face")}</div>
<p class="muted" style="margin-top:12px">HEAD and Padel Market both describe carbon as stiffer and fibreglass as softer and more forgiving.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Which racket for the left side and the right side?</h2></div>
<p>The right side (forehand side for a right-hander) mostly builds the point: returns, lobs and patient volleys. A control or all-round racket suits that job. The left side (backhand side) takes more of the overheads in the middle and finishes points, so many left-side players move to all-round or power. Not sure which side you are? Use the <a href="{href("which-side-padel.html")}">which side should I play quiz</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Pick a weight</h3><p>Get a gram range for your level and arm: the <a href="{href("padel-racket-weight.html")}">racket weight calculator</a>.</p></div>
<div class="card"><h3>Full racket match</h3><p>Shape, weight, balance, core and face in one go: the <a href="{href("racket-finder.html")}">padel racket finder</a>.</p></div>
<div class="card"><h3>Two rackets in mind?</h3><p>Put them side by side: <a href="{href("compare-padel-rackets.html")}">compare two padel rackets</a>. Balance numbers explained: <a href="{href("racket-balance.html")}">racket balance</a>. Spin: <a href="{href("padel-racket-for-spin.html")}">does a rough face help?</a></p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop by racket type</h3><p>Round for control, teardrop for all-round, diamond for power. Check balance and core on each product page.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round (control) rackets</a></li><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop (hybrid) rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond (power) rackets</a></li><li><a href="{go("padel-black-friday-rackets")}" {AFF_ATTR}>Black Friday rackets</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: HEAD "How to choose a padel racquet" (shapes, balance, sweet spot, weight bands, carbon vs fibreglass), Padel Market "Padel racket: control vs power" (29 May 2026: comparison of shape, balance, core and sweet spot; side of the court; soft core for arm pain), Padel USA "Control vs power in padel: which racket fits your game the best?" (Nov 2026: start with control, core and swing speed, side of the court). Written in our own words.</p></div></section>'''
cp_faq = [
    ("Should a beginner buy a control or power padel racket?", "Control. A round, head-light racket with a large sweet spot and a soft core is more forgiving while you learn. Move towards power once your overheads land where you aim."),
    ("What makes a padel racket powerful?", "A diamond shape, a high (head-heavy) balance, a bit more weight and a firmer core. Together they add speed to a well-hit smash but shrink the sweet spot."),
    ("Is a teardrop racket control or power?", "Teardrop rackets sit in the middle, with a medium balance, so they are usually sold as all-round or hybrid rackets."),
    ("Which padel racket is best for tennis elbow, control or power?", "Control. Guides recommend a lighter racket with a low balance and a soft core if you have elbow, wrist or shoulder pain. See a doctor or physio if pain lasts."),
    ("Do left-side padel players need a power racket?", "Not always, but many do. The left side finishes more points overhead, so experienced left-side players often choose an all-round or power racket."),
    ("Can a power racket make me a better player?", "Only once your technique is good enough to hit the smaller sweet spot. Before that, a control racket usually wins you more points."),
]
page("control-vs-power-padel-racket.html", "Control vs Power Padel Racket: Free 7-Question Test",
     "Control or power padel racket? Take the free 7-question test and see the shape, balance, weight, core and face that suit your level, side and style.",
     cp, cp_faq, "Control vs power")

# ---------- 3. PADEL RACKET FOR WOMEN ----------
wr = f'''<header class="hero"><div class="wrap"><h1>Best padel racket for women: the specs that matter, and a quick spec picker.</h1>
<p class="lead">Most "women's rackets" are lighter versions of a normal frame. That can be exactly right, or not. Answer five questions and get the weight, balance, shape, core and face to look for, whatever the label says.</p>
{quick("Choose by level, strength and arm, not by the label. Most women do well with a racket of about 340 to 360 g, a low or medium balance and a soft core; beginners suit a round shape, improving players a teardrop, and strong advanced players can go to 360 to 370 g with a higher balance or a diamond. A women's line is usually a lighter version of the same racket, and many women play the regular version.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap"><div class="quiz">
<div class="card">
{_bq2("wr", "lvl", "Your level", [("new", "New, under 1 year"), ("mid", "Improving, 1 to 3 years"), ("adv", "Advanced, competing")], "new")}
{_bq2("wr", "str", "How strong is your hitting arm?", [("light", "Not very strong"), ("avg", "Average"), ("strong", "Strong, gym or racket sports")], "avg")}
{_bq2("wr", "arm", "Any elbow, wrist or shoulder pain?", [("yes", "Yes, now or recently"), ("some", "Sometimes"), ("no", "No")], "no")}
{_bq2("wr", "sty", "How do you like to play?", [("ctrl", "Defend and place the ball"), ("all", "A bit of both"), ("pow", "Attack and smash")], "all")}
{_bq2("wr", "hand", "Hand size", [("s", "Small"), ("m", "Medium"), ("l", "Large")], "m")}
</div>
<aside class="result" id="wr-out" aria-live="polite"><span class="pill b">Your specs</span><h2 id="wr-h" style="margin-top:10px">340 to 355 g, round</h2><p id="wr-p"></p><dl class="spec" id="wr-spec"></dl><p id="wr-t" class="wr-src"></p>
<div class="btns" style="margin-top:10px"><button class="btn lime sm" type="button" id="wr-copy">Copy result</button></div></aside>
</div>
<p class="muted" style="margin-top:12px">General guidance, not a brand or medical recommendation. If you can, try a racket at your club before you buy.</p></div></section>
{AD.format("wr-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What weight padel racket should a woman use?</h2></div>
<div class="tbl"><table><thead><tr><th>Player</th><th>Weight</th><th>Balance</th><th>Shape</th><th>Core</th></tr></thead><tbody>
<tr><td>Beginner</td><td>About 340 to 360 g</td><td>Low</td><td>Round</td><td>Soft EVA or foam</td></tr>
<tr><td>Improving</td><td>About 345 to 365 g</td><td>Low to medium</td><td>Teardrop or hybrid</td><td>Soft to medium</td></tr>
<tr><td>Advanced, attacking</td><td>About 350 to 370 g</td><td>Medium to high</td><td>Teardrop or diamond</td><td>Medium to firm</td></tr>
<tr><td>Elbow, wrist or shoulder pain</td><td>About 340 to 355 g</td><td>Low</td><td>Round</td><td>Soft</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">These bands are where Padel Market, Padel Browser and Padelful's 2026 women's guides overlap: 340 to 360 g is the common advice for beginners and anyone with arm pain, and about 365 g and up only for advanced players with solid technique.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Are women's padel rackets different?</h2></div><div class="grid">{_cards([
    ("Usually lighter", "A women's line is most often a lighter version of an existing frame, sometimes with a lower balance or a softer core. The shape and face are often the same."),
    ("Not a rule", "Anyone can use a women's racket, and many women, including top professionals, play the regular version. The label tells you less than the weight and balance numbers."),
    ("What to check", "Weight in grams, balance (low, medium or high, or in mm), shape, core softness and face material. Colour and the word 'woman' do not change how it plays."),
], pill="Fact")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why balance matters as much as weight</h2></div>
<p>A head-heavy racket feels heavier than its weight suggests. Padel Market gives a good example: a 355 g racket with a high balance can feel heavier in the hand than a 360 g racket with a low balance. If a racket tires your wrist or shoulder by the second set, try a lower balance before you go much lighter. The numbers explained: <a href="{href("racket-balance.html")}">racket weight and balance</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What grip size for smaller hands?</h2></div>
<p>Most padel rackets come with one standard handle, and you change the thickness with overgrips. A grip that is too thick makes you squeeze, which tires the forearm; too thin and you also grip harder to stop it turning. Smaller hands often need just one overgrip, larger hands two. How to fit one: <a href="{href("padel-overgrip.html")}">padel overgrip guide</a> and <a href="{href("padel-grip.html")}">how to hold a padel racket</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What is the best padel racket for women with tennis elbow?</h2></div>
<p>Go lighter (about 340 to 355 g), low balance, round shape, soft core and a fibreglass or soft face, and avoid jumping to a stiff, heavy racket. Pain usually comes from the racket, technique and how much you play together, so get lasting pain checked by a doctor or physio. Check your own arm load with the <a href="{href("padel-elbow.html")}">padel elbow check</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What next?</h2></div><div class="grid">
<div class="card"><h3>Control or power?</h3><p>Seven questions on your game: the <a href="{href("control-vs-power-padel-racket.html")}">control vs power racket test</a>. Want more bite? <a href="{href("padel-racket-for-spin.html")}">Padel racket for spin</a>.</p></div>
<div class="card"><h3>Your exact weight</h3><p>Gram range by level, strength and arm: the <a href="{href("padel-racket-weight.html")}">racket weight calculator</a>.</p></div>
<div class="card"><h3>First racket?</h3><p>Start here: <a href="{href("best-padel-racket-for-beginners.html")}">best padel racket for beginners</a>, or the full <a href="{href("racket-finder.html")}">racket finder</a>.</p></div>
</div></div></section>
<section><div class="wrap"><div class="aff-box"><h3>Shop rackets by type</h3><p>Check weight, balance and core on each product page against your specs above.</p><ul class="aff-links"><li><a href="{go("padel-round-rackets")}" {AFF_ATTR}>Round rackets (light, low balance)</a></li><li><a href="{go("padel-teardrop-rackets")}" {AFF_ATTR}>Teardrop rackets</a></li><li><a href="{go("padel-diamond-rackets")}" {AFF_ATTR}>Diamond rackets</a></li><li><a href="{go("padel-overgrips")}" {AFF_ATTR}>Overgrips</a></li><li><a href="{go("padel-bags")}" {AFF_ATTR}>Bags</a></li></ul>{AFF_NOTE}</div>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: Padel Market "Best padel racket for women 2026" (weight bands, balance vs weight, grip thickness, see a health professional for pain), Padel Browser "Best padel rackets for women 2026" (340 to 375 g range, 340 to 360 g for learners and elbow issues, choose by level and swing, not the label), Padelful "Best padel rackets for women" (women's lines usually lighter versions of regular frames; picks 335 to 370 g). Written in our own words; we list no models because the guides disagree on picks.</p></div></section>'''
wr_faq = [
    ("What weight padel racket is best for women?", "Most women do well with about 340 to 360 g. Beginners and anyone with arm pain should stay at the lighter end; strong advanced players can use 360 to 370 g."),
    ("Are women's padel rackets just lighter?", "Mostly. A women's line is usually a lighter version of an existing frame, sometimes with a lower balance or softer core. Many women play the regular version."),
    ("What padel racket shape is best for women?", "The same as for anyone: round for beginners and control, teardrop for improving all-round players, diamond for strong attacking players."),
    ("Can men use women's padel rackets?", "Yes. If the weight and balance suit you, the label does not matter."),
    ("What padel racket do female pros use?", "Many top women play the same models as the men, or the women's versions of them, which are often a little lighter. Pros also have stronger technique and train every day, so their specs are not a guide for club players."),
    ("What is a good padel racket for a woman with tennis elbow?", "A light (about 340 to 355 g), low-balance, round racket with a soft core and a soft face. Get lasting pain checked by a doctor or physio."),
]
page("padel-racket-for-women.html", "Best Padel Racket for Women: Weight, Balance + Picker",
     "Best padel racket for women: weight in grams by level, balance, shape, core and grip, whether women's rackets differ, and a free spec picker.",
     wr, wr_faq, "Racket for women")

DEMAND_PAGES += ["padel-bags.html", "control-vs-power-padel-racket.html", "padel-racket-for-women.html"]
exec((ROOT / "demand15.py").read_text())
