# ---------------- DEMAND RUN 7 (26 Nov 2026): padel booking apps + game invite maker, history of padel timeline ----------------
# Executed from demand3.py (shares page(), quick(), href(), e(), AD, _bq2).

# ---------- 1. PADEL BOOKING APPS + FIND PLAYERS + INVITE MAKER ----------
bk_apps = [
    ("Playtomic", "Book courts, join or post open matches, 0 to 7 level that moves after each match, split the payment.", "Many countries: Spain, the UK, Europe, the Middle East and fast-growing in the US.", "Players"),
    ("PlayByPoint", "Club software: court booking, memberships, clinics and leagues. Often shown under the club's own app name.", "US: one of the two most used systems at US padel clubs.", "Clubs"),
    ("CourtReserve", "Club software for bookings, memberships, leagues and events. Mostly tennis and pickleball clubs that added padel.", "US.", "Clubs"),
    ("OpenCourt", "Court bookings, open games, coaches, leagues and memberships, often branded as the club's own app.", "US.", "Clubs"),
    ("MATCHi", "Search venues, book courts, coaching and club activities, for several racket sports.", "Europe, including some UK venues.", "Players"),
    ("ClubSpark (LTA)", "Booking pages for LTA registered clubs and venues: courts, coaching and competitions.", "UK.", "Clubs"),
]
bk_tbl = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>" for a, b, c, d in bk_apps)
bk_tips = [
    ("Start at your club", "Ask the front desk about beginner socials, mix-ins and the club WhatsApp group. Staff know who is looking for a game."),
    ("Play social formats", "Americano and Mexicano nights change partners every round, so you meet 7 or more players in one evening."),
    ("Join group coaching", "Players in the same group are at a similar level, and the coach can put you together."),
    ("Use open matches", "Where your club uses an app with open matches, join games at your level. Check the level before you book."),
    ("Be honest about your level", "Saying you are better than you are gets you fewer invites. Use our level calculator first."),
    ("Build your own group", "A chat of 6 to 8 people is enough for one game a week; 10 to 15 for flexible games. People drop out, so add more than four."),
    ("Same time, same place", "Play the same slot each week. The same faces see you and invites follow."),
    ("Leagues and ladders", "A league gives a season of fixed matches. A ladder suits players without a fixed partner."),
]
bk_tip_html = "".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in bk_tips)
bk = f'''<header class="hero"><div class="wrap"><h1>Padel booking apps, and how to find people to play with.</h1>
<p class="lead">Most padel courts are booked through an app, and the right one depends on your club and your country. Here is what each main app does, a quick app chooser, and a free invite maker that writes your game message for WhatsApp and splits the court price.</p>
{quick("Playtomic is the most widely used padel app for players: you can book courts, join open matches with players at your level and split the payment. In the US many clubs use PlayByPoint, CourtReserve or OpenCourt, often under the club's own app name. In the UK, many LTA registered venues take bookings through ClubSpark, and some use MATCHi or Playtomic. The simple rule: use the app your club uses, which is listed on its website.", "2026-11-26")}</div></header>
<section style="padding-top:10px"><div class="wrap quiz" id="bk">
<div class="card"><h2 style="font-size:1.3rem;margin-bottom:4px">Which padel app should I use?</h2><p class="muted" style="margin-top:0">Two quick questions.</p>
{_bq2("bk", "where", "Where do you play?", [("uk", "UK"), ("eu", "Spain or rest of Europe"), ("us", "US"), ("me", "Middle East"), ("x", "Somewhere else")], "uk")}
{_bq2("bk", "need", "What do you need most?", [("book", "Book a court for my group"), ("find", "Find players at my level"), ("learn", "Lessons, leagues or tournaments")], "book")}</div>
<aside class="result" id="bk-out" aria-live="polite"><h2 id="bk-h"></h2><p id="bk-p"></p><p id="bk-next" class="wr-src"></p></aside>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Padel booking apps compared</h2><p class="muted">What each one is for. "Clubs" means it is mainly software a club buys, so you only use it if your club does.</p></div>
<div class="card" style="padding:8px 24px;overflow-x:auto"><table class="mt mt-plain"><thead><tr><th scope="col">App</th><th scope="col">What it does</th><th scope="col">Where you see it</th><th scope="col">Made for</th></tr></thead><tbody>{bk_tbl}</tbody></table></div>
<p class="muted" style="margin-top:12px">We are not paid by any of these apps. Club and country counts change every month and the published figures disagree, so we don't quote them. Ask your club which system it uses.</p></div></section>
{AD.format("bk-mid")}
<section><div class="wrap gen" id="pinv">
<div class="gen-main"><div class="card">
<h2 style="font-size:1.6rem">Padel game invite maker</h2>
<p class="muted" style="margin-top:0">Fill in the game. You get a clear message to paste in WhatsApp or your club group, with the price per player worked out.</p>
<div class="gen-nums"><div class="q"><h3><label for="pi-day">Day and date</label></h3><input class="search" id="pi-day" type="text" placeholder="Sat 5 Dec" maxlength="40"></div>
<div class="q"><h3><label for="pi-time">Time</label></h3><input class="search" id="pi-time" type="time" value="19:00"></div></div>
<div class="gen-nums"><div class="q"><h3><label for="pi-club">Club or venue</label></h3><input class="search" id="pi-club" type="text" placeholder="Riverside Padel, court 2" maxlength="60"></div>
<div class="q"><h3><label for="pi-len">Court time</label></h3><select class="search" id="pi-len"><option value="60">60 min</option><option value="90" selected>90 min</option><option value="120">120 min</option></select></div></div>
<div class="gen-nums"><div class="q"><h3><label for="pi-price">Court price (total)</label></h3><input class="search" id="pi-price" type="number" min="0" step="0.5" value="40" inputmode="decimal"></div>
<div class="q"><h3><label for="pi-cur">Currency</label></h3><select class="search" id="pi-cur"><option value="£">£</option><option value="€">€</option><option value="$">$</option><option value="AED ">AED</option><option value="QAR ">QAR</option><option value="SAR ">SAR</option></select></div></div>
{_bq2("pi", "lvl", "Level", [("Beginner (1-2)", "Beginner"), ("Improver (2-3)", "Improver"), ("Intermediate (3-4)", "Intermediate"), ("Advanced (4+)", "Advanced"), ("Any level", "Any")], "Improver (2-3)")}
{_bq2("pi", "need", "Players still needed", [("1", "1"), ("2", "2"), ("3", "3")], "1")}
{_bq2("pi", "type", "Type of game", [("Friendly, rotate partners", "Friendly"), ("Competitive, fixed pairs", "Competitive")], "Friendly, rotate partners")}
<label style="display:flex;gap:10px;align-items:center;margin-top:6px;font-weight:600;cursor:pointer"><input type="checkbox" id="pi-balls" checked style="width:22px;height:22px;accent-color:var(--turf)"> I'm bringing new balls</label>
</div></div>
<aside class="gen-side"><div class="lb"><h2>Your message</h2><pre id="pi-msg" style="white-space:pre-wrap;font-family:inherit;color:#fff;margin:0 0 14px;line-height:1.5"></pre><p id="pi-each" style="margin:0 0 12px"></p><div class="btns" style="margin:0"><button class="btn lime sm" type="button" id="pi-copy">Copy message</button><a class="btn sm" id="pi-wa" href="#" target="_blank" rel="noopener">Open in WhatsApp</a></div></div></aside>
</div></section>
<section><div class="wrap"><div class="sh"><h2>How do I find people to play padel with?</h2><p class="muted">The ways that work best, from LTA Padel advice and club organisers.</p></div>
<div class="grid">{bk_tip_html}</div>
<p class="muted" style="margin-top:12px">Before you join a game, check your level with the <a href="{href("level-calculator.html")}">level calculator</a> and read the <a href="{href("padel-etiquette.html")}">padel etiquette</a> basics: arrive on time, pay your share quickly and call your own lines fairly. Running a club night? Use the <a href="{href("americano.html")}">Americano and Mexicano generator</a>.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do open matches work, and how do you find a regular padel partner?</h2></div>
<p>An open match is a game posted in a booking app with one or more free places. In Playtomic you go to <strong>Find a match</strong>, pick padel, your area and a time, then join a match or open your own. You choose if it is competitive or casual (you cannot change it later) and whether it is open to all. You pay your share online when you join. You do not need a partner: the app suggests matches near your level, and if you are outside the level range you can ask for a place and the other players decide.</p>
<div class="tbl" style="margin-top:12px"><table><thead><tr><th>Goal</th><th>What works</th></tr></thead><tbody>
<tr><td>One game this week</td><td>Join an open match in your club's app, or a beginner social or Americano night</td></tr>
<tr><td>A weekly game</td><td>A group chat of 6 to 8 players and a fixed weekly slot; send the invite with date, time, club, level and price each</td></tr>
<tr><td>Several games a week</td><td>A bigger group of 10 to 20 players, plus club leagues or ladders</td></tr>
<tr><td>A fixed partner</td><td>Group coaching for 4 to 5 weeks, then ask a player at your level; or join a competition alone and let the organiser pair you</td></tr>
</tbody></table></div>
<p style="margin-top:12px">Be honest about your level, arrive about 10 minutes early and send the next invite after the game: reliable players get asked back. In the US, Padel Browser found that 55 of 66 clubs with tracked schedules run open play, socials or round robins, usually split by level. Once you have a group, run a season with the <a href="{href("padel-league.html")}">padel league generator</a> or make fair pairs with the <a href="{href("padel-team-generator.html")}">team generator</a>.</p>
<p class="muted" style="margin-top:12px;font-size:.9rem">Sources, checked 28 Nov 2026: Playtomic Player Help "How to sign up for an Open Match"; Padel Browser "How to find a padel partner" (12 Aug 2026); Padel Speed "How to find people to play padel with" (1 May 2026); LTA Padel "How to play padel more often" (join a competition alone and organisers try to pair you).</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do I book a padel court for the first time?</h2></div><div class="grid">
<div class="card"><span class="pill b">1</span><h3 style="margin-top:10px">Find the venue's app</h3><p>Open the club's website and use the "book" link: it takes you to the app or booking page it uses. Make a free account.</p></div>
<div class="card"><span class="pill b">2</span><h3 style="margin-top:10px">Pick a slot and length</h3><p>Courts are booked by time, often 60 or 90 minutes, for 4 players. Evenings and weekends fill first, so book a few days ahead. See typical prices in <a href="{href("padel-cost.html")}">how much padel costs</a>.</p></div>
<div class="card"><span class="pill b">3</span><h3 style="margin-top:10px">Pay and share</h3><p>Pay the whole court or split it in the app if it allows. Then send the invite above to your group. Check the cancel rules: many clubs charge if you cancel late.</p></div>
</div>
<p class="muted" style="margin-top:12px">First time on court? Read the <a href="{href("beginners.html")}">beginner checklist</a> and bring the right <a href="{href("padel-equipment.html")}">kit</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 26 Nov 2026: LTA Padel "How to play padel more often: clubs, coaching and competitions" (clubs, group coaching, competitions, social groups); Padel Browser "Padel booking platforms in the US" (26 Sep 2026: Playtomic and PlayByPoint are the most used at US clubs, then CourtReserve; open matches and 0-7 level on Playtomic) and "How to find a padel partner" (12 Aug 2026); Padelspeed "Padel apps reviewed and listed" (22 Mar 2026: Playtomic, PlayByPoint, OpenCourt, MATCHi features) and "How to find people to play padel with" (1 May 2026: group sizes for regular games); Bounce "Padel booking software" (28 Jul 2026: Playtomic, PlayByPoint, CourtReserve, OpenCourt); LTA ClubSpark venue booking pages. Advice in our own words.</p></div></section>'''
bk_faq = [
    ("What is the best app to book padel courts?", "Use the app your club uses. Playtomic is the most widely used padel app for players and also finds open matches. In the US many clubs use PlayByPoint, CourtReserve or OpenCourt, and in the UK many LTA venues use ClubSpark."),
    ("How do I find people to play padel with?", "Ask your club about socials and its WhatsApp group, play Americano nights, join group coaching, use open matches in your club's app, and build a group chat of 6 to 8 players for a weekly game."),
    ("How do open matches work in padel?", "In an app like Playtomic, a player posts a game with free places. You pick padel, your area and a time, join a match near your level and pay your share online. You do not need your own partner."),
    ("How do I find a regular padel partner?", "Play open matches, socials and group coaching at your level, then invite the players you click with to a fixed weekly slot. A group chat of 6 to 8 players keeps one weekly game going."),
    ("How many people do you need for padel?", "Four for a normal doubles game. Book the court for 4 players and split the price four ways."),
    ("How do you split the cost of a padel court?", "Divide the court price by 4. A £40 court is £10 each. Some apps split the payment for you when you book."),
    ("Can I play padel on my own?", "Yes. Join an open match in your club's app, a beginner social or an Americano night: you are paired with other players."),
    ("Do I need an app to play padel?", "Not always. Some clubs take bookings by phone or on their website, but most use an app or online booking page. Check the club's website for its booking link."),
]
page("padel-booking-apps.html", "Padel Booking Apps Compared + How to Find Players",
     "Which padel booking app to use: Playtomic, PlayByPoint, CourtReserve, MATCHi, ClubSpark and more, how to find players, and a free WhatsApp invite maker.",
     bk, bk_faq, "Padel booking apps")

# ---------- 2. HISTORY OF PADEL: INTERACTIVE TIMELINE ----------
ht_ev = [
    ("start", "1969", "Enrique Corcuera builds the first padel court at his home in Acapulco, Mexico: a 20 x 10 m space with walls and a net. His wife Viviana writes the first rules.", "LTA, FIP"),
    ("start", "Early 1970s", "Prince Alfonso de Hohenlohe takes the game to Spain and builds the first courts at the Marbella Club on the Costa del Sol (LTA gives 1974).", "LTA, FIP"),
    ("start", "1970s", "Argentine Julio Menditeguy plays it in Marbella and takes it home to Argentina, where it spreads fast (LTA gives 1975).", "LTA, FIP"),
    ("fed", "1988", "The Argentine padel association is founded: the first national association. The first international match, Spain v Argentina, is played in Mar del Plata.", "FIP"),
    ("fed", "1989", "The first glass court that can be taken apart and moved is introduced in Argentina, the start of today's glass box.", "FIP"),
    ("fed", "1991", "The International Padel Federation (FIP) is founded in Madrid on 12 July by the associations of Argentina, Spain and Uruguay.", "LTA, FIP"),
    ("fed", "1992", "The first World Padel Championships are held in Madrid and Seville. They become a regular event every two years.", "LTA, FIP"),
    ("uk", "1992", "British players form the British Paddle Association so a team can play the 1992 World Championships.", "LTA"),
    ("fed", "1993 to 1997", "The spelling 'padel' becomes the standard name. LTA dates it to Spain's sports council in 1993; FIP to a rules agreement between Spain and Argentina in 1997.", "LTA, FIP"),
    ("fed", "2000", "The first World Junior Championship is played in La Plata, Argentina.", "FIP"),
    ("pro", "2005", "The first professional tour, the Padel Pro Tour, begins.", "LTA, FIP"),
    ("pro", "2013", "The World Padel Tour takes over as the main pro tour, until 2023.", "LTA, FIP"),
    ("pro", "2019", "FIP starts its own international circuit, renamed the CUPRA FIP Tour in 2020.", "FIP"),
    ("uk", "2019 to 2020", "The LTA brings padel into its work in 2019 and becomes the national governing body for padel in Great Britain in 2020.", "LTA"),
    ("pro", "2022", "Premier Padel starts. It becomes the official world pro tour, run with FIP.", "FIP"),
    ("pro", "2024", "Premier Padel holds 24 tournaments in 16 countries.", "FIP"),
    ("uk", "End of 2024", "Britain has about 760 courts (51 in 2020) and over 230,000 players (65,000 in 2020).", "LTA"),
    ("pro", "2026", "FIP counts 100 member federations, padel in more than 150 countries and about 35 million amateur players.", "FIP"),
]
ht_list = "".join(f'<li class="card ht-i" data-era="{k}" style="list-style:none;margin:0 0 10px;padding:16px 20px"><span class="pill b">{e(y)}</span> <span class="muted" style="font-size:.85rem">· {e(s)}</span><p style="margin:8px 0 0">{e(t)}</p></li>' for k, y, t, s in ht_ev)
ht = f'''<header class="hero"><div class="wrap"><h1>History of padel: who invented it, and how it grew.</h1>
<p class="lead">Padel began on one home court in Mexico in 1969 and is now played in more than 150 countries. Here is the full story as a timeline you can filter, from Acapulco to Marbella and Argentina, the pro tours and the UK boom.</p>
{quick("Padel was invented in 1969 by Enrique Corcuera in Acapulco, Mexico, who built a court with walls and a net at his home. Prince Alfonso de Hohenlohe took it to Marbella, Spain, in the early 1970s, and it spread to Argentina soon after. The International Padel Federation (FIP) was founded in 1991 and the first World Championships were played in 1992. Premier Padel, today's official pro tour, started in 2022.", "2026-11-26")}</div></header>
<section style="padding-top:10px"><div class="wrap" id="ht">
<div class="sh"><h2>Padel history timeline</h2><p class="muted" id="ht-age"></p></div>
<div class="q" style="margin-bottom:12px">{_bq2("ht", "era", "Show", [("all", "Everything"), ("start", "The beginning"), ("fed", "Federations and rules"), ("pro", "Pro tours"), ("uk", "Padel in Britain")], "all")}</div>
<ol id="ht-list" style="padding:0;margin:0">{ht_list}</ol>
<p class="muted" style="margin-top:12px">Sources: LTA Padel "History of padel" and the International Padel Federation (FIP) "History" page, both checked 26 Nov 2026. Where they give different years we show both. FIP says the first court had 3 m walls; LTA says walls and fencing of up to 4 m.</p>
</div></section>
{AD.format("ht-mid")}
<section><div class="wrap"><div class="sh"><h2>Who invented padel?</h2></div><div class="grid">
<div class="card"><h3>Enrique Corcuera</h3><p>In 1969 he built a court with walls and a net at his home in Acapulco, Mexico. LTA says he called it "Paddle Corcuera".</p></div>
<div class="card"><h3>Viviana Corcuera</h3><p>FIP says his wife wrote the first set of rules. The court size, 20 x 10 m, is still the size used today: see our <a href="{href("court-dimensions.html")}">court dimensions</a>.</p></div>
<div class="card"><h3>Alfonso de Hohenlohe</h3><p>A Spanish prince who discovered the game in Mexico and built the first courts in Spain at the Marbella Club. That is how padel reached Europe.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why is padel so big in Spain and Argentina?</h2></div><div class="grid">
<div class="card"><h3>Argentina first</h3><p>Argentina founded the first national association in 1988 and introduced the movable glass court in 1989. LTA says it has more than 10,000 courts.</p></div>
<div class="card"><h3>Then Spain</h3><p>From the Costa del Sol, padel spread across Spain. LTA says Spain has more than 20,000 courts and about 6 million players.</p></div>
<div class="card"><h3>Now worldwide</h3><p>FIP says Premier Padel held 24 tournaments in 16 countries in 2024. The 2026 tour's last Major is back where padel began: the <a href="{href("premier-padel-mexico-major.html")}">Premier Padel Mexico Major in Acapulco</a>. See the <a href="{href("padel-rankings.html")}">world rankings</a> and our <a href="{href("padel-vs-tennis-vs-pickleball.html")}">padel vs tennis vs pickleball</a> guide.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>Why is it called padel?</h2></div>
<div class="card"><p style="margin:0">Early on it was written "paddle", as in "paddle tennis". The Spanish spelling "padel" became the official name in the 1990s, and the world federation uses it. It is not the same game as American paddle tennis or platform tennis: see <a href="{href("padel-vs-racquetball.html")}">padel vs racquetball vs platform tennis</a>. Learn the Spanish words players still use in the <a href="{href("glossary.html")}">padel glossary</a>, and the game itself in the <a href="{href("rules.html")}">padel rules</a>.</p></div></div></section>'''
ht_faq = [
    ("Who invented padel?", "Enrique Corcuera, in Acapulco, Mexico, in 1969. He built a court with walls and a net at his home, and his wife Viviana wrote the first rules."),
    ("When was padel invented?", "In 1969. That makes padel more than 55 years old."),
    ("Where does padel come from?", "Mexico. It was invented in Acapulco, then grew in Spain (from Marbella, in the 1970s) and in Argentina."),
    ("How did padel get to Spain?", "Prince Alfonso de Hohenlohe played it in Mexico and built the first Spanish courts at the Marbella Club in the early 1970s."),
    ("When did padel come to the UK?", "British players formed a padel association in 1992 to play the first World Championships. The LTA became the governing body for padel in Britain in 2020, and the game has grown fast since."),
    ("How many people play padel?", "FIP says about 35 million amateur players in more than 150 countries (2026). LTA says Britain had over 230,000 players at the end of 2024."),
]
page("history-of-padel.html", "History of Padel: Who Invented It + Interactive Timeline | Padel Glass Box",
     "Padel was invented in 1969 by Enrique Corcuera in Acapulco, Mexico. Interactive timeline from Spain and Argentina to pro tours and padel in the UK.",
     ht, ht_faq, "History of padel")

DEMAND_PAGES += ["padel-booking-apps.html", "history-of-padel.html"]
exec((ROOT / "demand5.py").read_text())
