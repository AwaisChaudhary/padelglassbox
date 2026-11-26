## SEO PLAYBOOK — standing rules for every run (Awais 26 Nov 01:35: "do SEO like the best SEO guy in the world for all sites")
Tools in this repo: `seo_post.py` (runs at the end of build.py: sitemap = every indexable page; lastmod changes ONLY when visible content changes; image sitemap entries) and `seo_audit.py` (`python3 seo_audit.py . <https://domain>`: titles, descriptions, canonicals, H1, JSON-LD, broken links, orphans, sitemap gaps, thin pages).
1. EVERY NEW PAGE: one main query (Keyword Planner / autocomplete / People Also Ask). Title: the query first, under ~60 characters where possible. Meta description 140-160 chars that contains the answer. One H1. A quick answer to the query in the first 100 words. FAQ from real PAA questions. Link IN from at least 3 relevant existing pages (not just nav) and OUT to 3+ related pages. An original image where it helps (our own diagrams/maps/screens, descriptive alt text). Then run seo_audit.py and fix anything it flags for that page.
2. AFTER DEPLOY: IndexNow ping (key in README/OPERATIONS) + Search Console URL Inspection > Request indexing for the 2-5 most important new URLs (max ~10/day per property; account ocrial@gmail.com = authuser=1).
3. WEEKLY (Monday run): Search Console > Performance > 28 days > Pages + Queries (500 rows). (a) Pages at position 5-15 with 200+ impressions: rework them first: answer the exact top queries word-for-word in the quick answer/H2s, add the missing sub-topics the queries show, refresh facts and "last checked" dates, add FAQ entries for question-type queries, strengthen internal links to the page. (b) Pages with CTR under 1% at position under 10: rewrite title/description to match the dominant query wording and promise the specific answer (numbers, "all N locations", year). (c) Queries with impressions but no matching page: new page or section. Log every change with before/after position in CONTENT-LOG.md, and don't touch a page again for 14 days so the effect can be measured.
4. NEVER: stamp fake lastmod/"updated" dates, change URLs of pages that get traffic (if unavoidable, 301 in _redirects), keyword-stuff, mass-produce thin pages, buy links, swap links, or copy competitors' text/data.
5. Links: only real editorial links via outreach batches Awais approves; build "linkable assets" (original data, free tools, maps) and list pitch targets in DEMAND for approval.
6. Monthly: run seo_audit.py on the whole site and fix broken links, orphans, duplicate titles/descriptions, missing schema.

## COMPETITOR WATCH 26 Nov 2026 (vs racketguide.com (2,500-racket database), Tennis Warehouse University padel, App Store padel apps: Padel Tracker, Learn Padel 21-Day Course, Padel Coach swing analysis)
We have 63 pages incl. 12 tools (level calculator, racket finder, gift finder, score keeper, match tracker, Americano, round robin, ladder, king of the court, FIP points, training plan, fix-my-padel).
1. GAP: racket database + compare (open since 25 Nov): racketguide lists ~2,500 rackets with filters and side-by-side compare; we have a quiz + 3 guide pages. Plan: /padel-rackets table from maker spec pages (start 60 current models), filters (shape, weight, balance, hardness, level) + compare 2-3, 'similar to my racket'. Biggest affiliate value.
2. GAP: Mexicano mode (Playtomic and every tournament app have it; still open from 24 Nov). Plan: Mexicano toggle on /americano (re-pair by standings each round).
3. DONE 26 Nov https://padelglassbox.com/padel-beginner-plan GAP: structured beginner course: the 'Learn Padel - 21 Day Course' app sells a day-by-day plan. We have /padel-training-plan + /drills. Plan BETTER: free '21-day padel starter plan' page that ticks off each day in the browser (progress saved on device), each day linking our drills/shots pages.
4. GAP: Premier Padel 2027 calendar + results hub (open since 24 Nov). Plan: /premier-padel-2027 with official dates only.
5. GAP: video swing analysis apps (Padel Coach). Plan: not worth building now; instead a 'film yourself' checklist on /fix-my-padel (what angle, what to look for per shot).
6. BETTER-THAN-THEM: 'Padel night planner': pick players + courts + time, get Americano/Mexicano rounds, court rotation, cost split per player and a share link for WhatsApp. Apps need everyone to install; ours works in one link.

## RADAR 26 Nov (demand-first build run 4; web search)
C1. DONE 26 Nov https://padelglassbox.com/padel-cost — 'how much does padel cost', 'padel court hire price per hour', 'why is padel so expensive', 'padel membership worth it': Time Out London price map (Mar 2025), City AM court-rental-cost story, Padel Browser US cost (Jun 2026) + US membership cost (Oct 2026), Bounce 'why is padel so expensive' (Jul 2026), Qatar Living costs (Aug 2026), Bannatyne/club padel FAQs, Tienda Padel Point cost FAQ. Built as cost calculator (per game/month/year, membership break-even) = E4.
C2. DONE 26 Nov https://padelglassbox.com/padel-beginner-plan — '30 day padel beginner plan', 'padel for beginners plan': The Padel Passport 30-day beginner plans for 5+ cities, Learn Padel 21-Day Course app (competitor watch 26 Nov #3), Selkirk 30-day pickleball challenge, Tienda weekly beginner routine. Built as day-by-day tickable checklist.
C3. DONE 26 Nov (merged H2 + FAQ on https://padelglassbox.com/padel-rankings) 'Premier Padel Finals 2026 dates': premierpadel.com/tourfinals + Palau Sant Jordi page: 10-13 Dec 2026, Barcelona. Covers part of D4/N4 (event hub still open for results after 13 Dec).
C4. OPEN 'padel membership cost' / 'is padel membership worth it' (Padel Browser Oct 2026 membership guide, Playtomic club membership pages): calculator now on /padel-cost; a dedicated UK membership comparison needs 2 UK sources.
C5. OPEN 'padel in Qatar / Doha' (Qatar Living Aug 2026: courts, costs, booking): Middle East where-to-play page only with 2+ sources (check Qatar federation / Visit Qatar).

## RADAR 26 Nov (demand-first build run 3; web search)
T1. DONE 26 Nov https://padelglassbox.com/how-to-serve-padel — 'how to serve in padel', 'padel serve tips', 'padel serve drills': Red Bull 'padel how to serve beginners guide' (4 editions) + 'padel serve tips', HEAD 'how to serve in padel' (4 locales), LTA Padel serve page, Padel Browser, The Padel School (4+ serve posts), Tienda Padel Point serve-accuracy exercises x2. Built as 6 steps + serve practice tracker.
T2. DONE 26 Nov https://padelglassbox.com/padel-tactics — 'padel tactics', 'how to win more padel points': The Padel School tactics hub + 'how to win a padel point', HEAD 'padel tactics' (4 locales), LTA Padel 'how to win more padel matches' (Mar 2026), bet365 (Apr 2026), Lidl. Built as 10-scenario trainer with own court drawings.
T3. DONE 26 Nov https://padelglassbox.com/padel-improvement-guide — 'how to get better at padel', 'improve padel fast': Padel Browser, Bounce (9 Jun 2026), LTA training tips, The Padel School, Total Padel x2, Everything Padel x2, Red Bull, HEAD (6 locales), padelspeak.
T4. OPEN 'padel elbow' (Decathlon, Tienda Padel Point x2, Justpadel, The Padel Paper, Esprit Padel x3): /padel-injuries already has an outer-elbow zone + 2 FAQs (NHS). Next: add a dedicated 'What is padel elbow?' H2 with racket/grip checklist (needs a 2nd readable source; Tienda + Padel Paper fetch failed this run).
T5. WATCH Mexico Major 2026 results still not indexed (search returns 2025: Coello/Tapia, Bea Gonzalez/Claudia Fernandez); refresh /padel-rankings after Finals.

## DEMAND RADAR 26 Nov 06:45 (Google autocomplete US)
P1. OPEN /padel-vs-racquetball + platform tennis / paddleball comparisons (autocomplete "padel vs racquetball/paddleball/platform tennis/squash"), one comparison page with a table.
P2. OPEN "best padel racket for beginners" guide (we have /cheap-padel-rackets, /intermediate-padel-racket: add a beginner page or section), "best padel player in the world" (rankings, dated).
P3. PARTLY DONE 26 Nov (serve part: https://padelglassbox.com/how-to-serve-padel) "how to serve in padel" step-by-step with a drill (we have /serve-rules = rules only) and "pickleball how to hold paddle".

## RADAR 26 Nov (demand-first build run 2; web search)
E1. DONE 26 Nov https://padelglassbox.com/padel-etiquette — 'padel etiquette' / 'padel unwritten rules': Red Bull article in 5 country editions (gb, us, ca, int, ph), Padel Browser (15 Apr 2026), Dummies cheat sheet, Jean Galea, club FAQ pages. Built as a 10-situation quiz + checklist + rule-vs-custom table.
E2. DONE 26 Nov /padel-training-plan — 'padel training plan', 'weekly padel training routine': 8+ Tienda Padel Point guides, The Padel School pathways, padel-rules beginner 4-week and intermediate 8-week plans.
E3. DONE 26 Nov /padel-match-tracker — 'padel match tracker / stats': 15+ App Store apps (PadelRatio, Pelota, Padel Stats Pro, RecordUp, PadelTick, Racketly) + 'padel match tracker' blog guides.
E4. DONE 26 Nov https://padelglassbox.com/padel-cost 'why is padel so expensive' / 'cost to start padel' — The Padel School post + podcast, Bounce blog (23 Jul 2026), Tienda Padel Point FAQ. Plan: H2 + cost calculator section on /padel-lessons or a /padel-cost page (court hire per person, racket, shoes, balls) with 2 sources per figure.
E5. PARTLY (see T4) 'padel elbow' — The Padel School dedicated post; we have /padel-injuries: add a 'padel elbow' H2 + FAQ there (merge, not new page).
E6. WATCH Premier Padel Mexico Major (Acapulco) 2026 results not yet indexed (search returns 2025 edition); refresh /padel-rankings after the Finals.

## TOP PRIORITY (Awais 26 Nov 01:00): "Don't just add dimensions or rules. Add something people will USE the site for: solve their problems, help them improve their padel game." Build these BEFORE any more reference pages (2-3 per run, tools first):
I1. DONE 26 Nov https://padelglassbox.com/fix-my-padel — ("why do I keep...": interactive problem fixer). Player picks a problem (hitting the glass/out, losing at the net, can't return lobs, weak serve return, bandeja goes long, partner confusion, tired/late to the ball, elbow pain) -> cause in plain words, 3 fixes, one drill with reps, link to the shot/drill page. Coaching advice general and safe; injury items say see a physio.
I2. DONE 26 Nov https://padelglassbox.com/padel-training-plan — /padel-training-plan (generator): level (from /level-calculator), days per week, goal (net game, defence, fitness, matches) -> a 4-week plan with drills from /drills, warm-up, match play, rest; printable + copy.
I3. DONE 26 Nov https://padelglassbox.com/padel-match-tracker — /padel-match-tracker: tap-to-log winners and errors by shot (serve, return, volley, bandeja, vibora, smash, lob, wall) during or after a match; shows where points are lost + the fix page for the worst shot; saves locally.
I4. DONE 26 Nov https://padelglassbox.com/which-side-padel — ("left or right side?" quiz: forehand/backhand strengths, smash, lefty/righty, partner) -> recommended side and why, with what each side does.
I5. DONE 26 Nov https://padelglassbox.com/padel-tactics — /padel-tactics: interactive scenarios ("opponents at the net, you're at the back: what shot?") with answers and diagrams (own SVG), building on /positioning.
I6. DONE 26 Nov https://padelglassbox.com/padel-improvement-guide — /padel-improvement-guide hub: "how to get better at padel" (level by level: what to learn next, which tools to use) linking I1-I5, drills, level calculator.
I7. DONE (already built: Mexicano mode on https://padelglassbox.com/americano) /mexicano (generator) if /americano doesn't already do Mexicano pairing; otherwise add a Mexicano mode to /americano.
Evidence: 'how to get better at padel', 'padel tips', 'padel drills', 'padel left or right side', 'padel tactics', 'how to improve padel' (Google autocomplete, People Also Ask). Re-check autocomplete each run.

## RADAR 26 Nov (build run; web search)
N1. 'padel common mistakes' / 'beginner mistakes padel' — 10+ dedicated guides (The Padel School, Padel Browser 9 Jun 2026, Village Gym, Red Bull, Tienda Padel Point x8, Everything Padel) = strong demand. DONE in /fix-my-padel.
N2. 'padel left or right side' — 15+ guides (The Padel School x5, Padel Browser 14 Sep 2026, Red Bull, allforpadel, padelproshop, Tienda Padel Point). DONE /which-side-padel.
N3. DONE 26 Nov /padel-match-tracker — 'padel stats tracker' — 15+ App Store apps (PadelRatio, Padel Stats Pro, Padel Stats AI, RecordUp, Pelota) = demand for I3 /padel-match-tracker (free, no app). Build next.
N4. OPEN Premier Padel Mexico Major (Acapulco, late Nov) + Finals Barcelona Dec: news trending (padelfip, Padel Addict, Red Bull) — refresh /padel-rankings top 10 after 30 Nov; D4 event hub.

## RADAR 25 Nov ~20:00 PKT (build run; Google autocomplete endpoint blocked from the cloud, used web search)
D1. DONE 25 Nov /court-sizes-compared — 'how many padel courts fit on a tennis court' and 'how many pickleball courts fit on a tennis court' return many dedicated articles (Sportmaster, Selkirk, PB5star, Alibaba, LTA guidance) = clear demand.
D2. DONE 25 Nov /pickleball-score — many App Store score-keeper apps (Pickleball ScoreKeeper, PicklePoints, DinkTally, My PickleBall Scoreboard) + guides on 'how to call the score 0-0-2' (pickleball.com, AARP, Wilson).
D3. OPEN /padel-booking-apps — 'padel booking platforms', 'Playtomic alternatives': Bounce, Padel Browser (US 2026), Cal.com, Capterra lists. Facts only, 2 sources each.
D4. PARTLY DONE 26 Nov (dates on /padel-rankings) Premier Padel Finals 2026 (Barcelona, December) + Mexico Major: event hub with official dates only (padelfip.com, premierpadel.com/tourfinals).
D5. BLOCKED this run: P3 platform tennis / racquetball facts (APTA, USA Racquetball, Wikipedia fetches timed out) — retry next run.

## NEW CATEGORY: OTHER RACKET-SPORT COURTS + RULES (Keyword Planner, worldwide, 25 Nov 2026)
"badminton court dimensions" 100k-1M LOW comp (+900% 3-month), "tennis court dimensions" 10k-100k, "badminton rules" 10k-100k, "table tennis rules" 10k-100k, "squash court dimensions" 1k-10k.
R1. DONE 25 Nov /badminton-court-dimensions, /tennis-court-dimensions (scale SVG, m + ft, compared table).
R2. DONE 25 Nov /badminton-rules (serve height 1.15 m rule, scoring to 21, quiz) — BWF Laws.
R3. DONE 25 Nov (one page: /table-tennis-rules incl. table size) /table-tennis-rules (serve toss 16 cm, scoring to 11, let) + /table-tennis-table-dimensions (2.74 x 1.525 m, net 15.25 cm) — ITTF.
R4. DONE 25 Nov /squash-court-dimensions (9.75 x 6.4 m, tin 0.48 m) — WSF.
R5. DONE 25 Nov https://padelglassbox.com/court-sizes-compared (all six courts to scale + 'how many courts fit in my space' planner; 1 padel / 4 pickleball per tennis plot).

## NEW CATEGORY: PICKLEBALL (Awais 25 Nov: add new topic areas where data shows demand) — Keyword Planner, US, 25 Nov 2026
"pickleball court dimensions" 10k-100k LOW comp, "pickleball rules" 10k-100k, "pickleball paddles" 100k-1M, "padel vs pickleball" autocomplete #1, "platform tennis" 1k-10k rising. Racket-sport players overlap heavily, so build a Pickleball section with the same tool-first approach:
K1. DONE 25 Nov /pickleball-court-dimensions — measured SVG diagram (m and ft), kitchen/non-volley zone, net height, converting a tennis court (USA Pickleball rulebook + 1 more source).
K2. DONE 25 Nov /pickleball-rules — rules explained simply + interactive serve/kitchen quiz.
K3. DONE 25 Nov https://padelglassbox.com/pickleball-score (doubles/singles, traditional/rally, 0-0-2, serve side, undo, saved).
K4. OPEN /pickleball-paddle-finder — weight/shape/core finder (no brand claims), with clearly labelled affiliate links only if a pickleball programme is approved; otherwise no shop links.
K5. OPEN /platform-tennis — what it is, rules, court; and update /padel-vs-tennis-vs-pickleball links to the new pages.
Link the section from the home page and footer; keep top nav at 5.

## COMPETITOR WATCH 25 Nov 2026 (vs racketguide.com, Tennis Warehouse University padel, padelful/padel.fyi)
We have 45 pages incl. tools: level calculator, racket finder, gift finder, score keeper, Americano, round robin, ladder, king of the court, FIP points calculator (/padel-rankings).
1. GAP: racket database. racketguide.com lists 2,503 rackets with search/filters, 'similar rackets', side-by-side compare, favourites and price comparison from 40+ stores; TWU has measured-specs compare + spin prediction. We have a quiz with a short list. Plan: /padel-rackets table (shape, weight, balance, core, hardness, level) from maker spec pages, start with 60 current models, filter + compare 2-3 side by side, affiliate /go/ links. Highest affiliate value on the site.
2. GAP: 'similar racket' finder ("I like X, what else?"). Plan: once the table exists, nearest-spec match (shape+balance+weight+hardness) = cheap feature on top of item 1.
3. GAP: Mexicano generator (still open from 24 Nov item 4); Playtomic-style apps own this. Plan: add Mexicano mode to /americano (re-pair by standings each round).
4. GAP: Premier Padel 2027 calendar/results hub + Hexagon World Series (open from 24 Nov). Plan: /premier-padel-2027 with official dates only.
5. GAP: physics/tech explainers (TWU: power, spin, carbon layups). Plan: /padel-racket-materials (carbon K-count, EVA vs foam, fibreglass) in our own words, 2 sources; links into racket table.
6. BETTER-THAN-THEM: racket finder that uses the player's result from our level calculator + injury flags (tennis elbow -> soft core, low weight) + budget, then shows 3 picks with WHY. racketguide's quiz ignores injuries and level tests. Free, no login.

## RADAR 25 Nov 06:45 PKT (Google autocomplete, US)
P1. OPEN 'best padel player in the world' / 'padel rankings' (best #1, r #5) -> /padel-rankings (men's + women's top 10 from the official tour rankings, update monthly).
P2. OPEN 'padel racket for sale' / 'best padel rackets 2026' -> extend racket finder copy with a 2026 shortlist (no fake reviews).
P3. OPEN 'padel vs racquetball' / 'paddleball' / 'platform tennis' -> H2s on /padel-vs-tennis-vs-pickleball.
P4. OPEN 'padel ratings' (r #6) -> link /level-calculator with 'padel rating' wording.
P5. OPEN 'padel smash game' -> skip (mobile game, off-topic).
Covered: rules, court dimensions, beginners, kids racket, intermediate racket, shoes, court cost (new 25 Nov).

## COMPETITOR WATCH 24 Nov 2026 (vs padelfip/premierpadel, padelful, padel.fyi, padelverdict, visu.network, xporty, sportsvenuecalculator)
We have 40 pages incl. 5 tools (level calc, racket finder, gift finder, americano, round robin/ladder/king of the court).
1. GAP: pro rankings (FIP/Premier Padel men + women) explained; we have none. Plan: /padel-rankings (how points work, current top 10 with date, 2 sources), refresh weekly.
2. GAP: Premier Padel 2027 calendar + results hub (2027 format changes published June 2026; Hexagon World Series 2027). Plan: /premier-padel-2027 calendar (official dates only, "TBC" labelled) + /hexagon-world-series.
3. GAP: racket database/reviews with filters (shape, balance, weight, stiffness): padelful/padel.fyi. Plan: grow racket-finder data into a filterable /padel-rackets table (own specs from maker sites, affiliate links). Biggest affiliate value.
4. GAP: Mexicano generator (we have Americano only). Plan: add Mexicano mode to /americano or new /mexicano (quick).
5. GAP: court build cost calculator (B2B, high CPC): /padel-court-cost calculator (UK/US/EU ranges from 2+ sources).
6. BETTER-THAN-THEM: one free tournament tool (Americano, Mexicano, round robin, knockout) with live scores, shareable leaderboard link, no app/login, and "auto-balance teams" from our level calculator. Competitors split this across paid apps.

# Padel Glass Box demand queue (Google autocomplete, 24 Nov 2026)
## RADAR 24 Nov 06:45 PKT — NEW top OPEN items
R1. DONE 24 Nov (/padel-gifts) Padel gifts ('padel gifts'): Christmas gift guide for padel players by budget (own picks, general advice, affiliate /go/ links where we have them). Timely: build before 1 Dec.
R2. OPEN City guides (top autocomplete: austin, atlanta, boston, chicago, dallas, denver, miami, los angeles, nyc, jersey city, kansas city, las vegas, charlotte, detroit, fort lauderdale, frisco, el paso, indianapolis): hub /where-to-play-padel then cities with 3+ confirmed venues (rule from earlier block).
R3. DONE 25 Nov (/padel-lessons) 'padel lessons' / 'lessons near me' -> how to find lessons + what a first lesson covers + cost ranges (2 sources).
R4. PARTLY DONE 24 Nov (/padel-equipment kit checklist + what to wear; padel ball vs tennis ball done on /padel-balls); 'padel ball vs tennis ball' -> section on /padel-balls; 'padel game rules' -> make /rules title match; 'padel definition / meaning / en ingles' -> 'What is padel?' page.
R5. OPEN 'padel app' -> best apps to book courts (Playtomic etc., facts only).

Biggest padel search cluster = LOCAL: 'padel <city>' (where to play). Build genuinely useful city guides (clubs, number of courts, indoor/outdoor, booking app, price range, beginner lessons) with facts from the clubs' own sites + 1 more source. NOT doorway pages: each must have real club data; skip a city if fewer than 3 confirmed venues.
1. OPEN /where-to-play-padel hub (UK, US, UAE sections) linking city guides.
2. OPEN US cities in order: Miami, Los Angeles (Culver City/Century City), New York (Williamsburg/Brooklyn), Austin, Atlanta, Orlando, Denver, Kansas City, Nashville, Jersey City, Chandler/Phoenix, Katy/Houston, Jacksonville, El Paso.
3. OPEN UK: London (Wandsworth, Wimbledon); Spain/Zaragoza later.
4. PARTLY DONE 24 Nov (/padel-racket-for-kids) 'padel racket for intermediate players' (buying guides with AFF links), 'padel lessons: what to expect / cost', 'padel outfits: what to wear', 'best padel player in the world (FIP ranking)', 'what is padel' (also 'padel en ingles', 'padel y pickleball es lo mismo' -> short ES/EN explainer).
