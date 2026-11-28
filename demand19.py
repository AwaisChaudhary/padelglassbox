# ---------------- DEMAND RUN 21 (28 Nov 2026): padel league season generator (divisions, points, promotion/relegation) ----------------
# Executed from demand18.py (shares page(), quick(), href(), e(), AD, _bq2, _cards).

lg = f'''<header class="hero"><div class="wrap"><h1>Padel league generator: divisions, fixtures, table and promotion</h1>
<p class="lead">Run a club or friends' padel league for a whole season. Type in your pairs, strongest first. You get divisions, a week-by-week fixture list, a live league table and, at the end, one tap to move pairs up and down for the next season. Free, no sign-up, saved on this device.</p>
{quick("A simple padel league: put 4 to 6 pairs of similar level in each division, let every pair play every other pair once over a season of about 4 to 6 weeks (one match a week, booked by the pairs), score best of 3 sets with a super tie-break to 10 as the third set, give 4 points for a 2-0 win, 3 for 2-1, 2 for a 1-2 loss and 1 for a 0-2 loss, then move the top 1 or 2 pairs up a division and the bottom 1 or 2 down.", "2026-11-28")}</div></header>
<section style="padding-top:10px"><div class="wrap">
<div class="card" id="lg-setup">
<h2 style="font-size:1.6rem">Set up your league</h2>
<div class="q"><h3><label for="lg-names">Pairs, one per line, strongest first (4 to 36)</label></h3><textarea class="search" id="lg-names" rows="8" placeholder="Sam &amp; Priya&#10;Omar &amp; Lucia&#10;Ben &amp; Aisha&#10;..."></textarea><p class="muted" id="lg-count" style="margin:-6px 0 0"></p></div>
{_bq2("lg", "size", "Pairs per division", [("4", "4"), ("5", "5"), ("6", "6"), ("8", "8")], "5")}
{_bq2("lg", "legs", "Each pair meets", [("1", "Once"), ("2", "Twice")], "1")}
{_bq2("lg", "pts", "Points system", [("4321", "4-3-2-1 by sets"), ("3", "3 for a win")], "4321")}
{_bq2("lg", "move", "Pairs up and down each season", [("1", "1"), ("2", "2")], "1")}
<p class="msg" id="lg-err" role="alert" style="color:#a43c13;min-height:0"></p>
<div class="btns" style="margin-top:4px"><button class="btn lime" type="button" id="lg-start">Make the league</button><button class="btn ghost" type="button" id="lg-demo">Fill 10 sample pairs</button></div>
</div>
<div id="lg-live" hidden style="margin-top:16px">
<div class="card gen-bar"><div><span class="pill b" id="lg-sum"></span></div><div class="btns" style="margin:0"><button class="btn ghost sm" type="button" id="lg-copy">Copy tables</button><button class="btn ghost sm" type="button" id="lg-next">Start next season</button><button class="btn ghost sm" type="button" id="lg-new">New league</button></div></div>
<p class="muted" style="margin:10px 0 0">Type each result as the set scores of the first pair named, for example <strong>6-4 3-6 10-7</strong>. Leave it empty until the match is played. Tables update as you type.</p>
<div id="lg-divs"></div>
</div>
<p class="muted" style="margin-top:12px">Saved on this device only. To share, copy the tables into your league WhatsApp group after each week.</p>
</div></section>
{AD.format("lg-mid")}
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How do you run a padel league, step by step?</h2></div><div class="grid">{_cards([
    ("Gather 8 to 12 players or more", "The Padel School suggests 8 to 12 players (4 to 6 pairs) to start a league, so there are regular doubles matches. Bigger groups get more divisions."),
    ("Group pairs by level", "A league is grouped by level, unlike a mixed social. Put similar pairs together in divisions of 4 to 6. If you are unsure, ask everyone to use the <a href='"+href("level-calculator.html")+"'>level calculator</a>."),
    ("Set a season and a match window", "Pick a season of about 4 to 6 weeks and give each round a week. Pairs book their own court (often 90 minutes) inside that week."),
    ("Agree the format and points", "Best of 3 sets with a super tie-break to 10 instead of a third set fits a 90-minute booking. Write down the points, the tie-break order and what happens if a match is not played."),
    ("Collect results the same day", "The winners send the score to the organiser or the group chat. One person updates the table, so there is one version of the truth."),
    ("Move pairs up and down", "At the end, the top pairs go up a division and the bottom pairs go down. Then the next season starts with fresh, closer divisions."),
], pill="Step")}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What points system should a padel league use?</h2></div>
<div class="tbl"><table><thead><tr><th>Result</th><th>4-3-2-1 by sets</th><th>3 for a win</th></tr></thead><tbody>
<tr><td>Win 2-0</td><td>4</td><td>3</td></tr>
<tr><td>Win 2-1</td><td>3</td><td>3</td></tr>
<tr><td>Lose 1-2</td><td>2</td><td>0</td></tr>
<tr><td>Lose 0-2</td><td>1</td><td>0</td></tr>
<tr><td>1-1 (time ran out)</td><td>2 each</td><td>1 each (draw)</td></tr>
<tr><td>Walkover given or no-show</td><td>Winner 4, no-show 0</td><td>Winner 3, no-show 0</td></tr>
</tbody></table></div>
<p class="muted" style="margin-top:12px">The 4-3-2-1 system rewards every pair that turns up and plays, even when they lose, which keeps lower pairs coming back. Roehampton Club's padel league uses this system. "3 for a win" is simpler and familiar from football. Both work; pick one before the season starts.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How does promotion and relegation work in a padel league?</h2></div>
<p>At the end of each season, the top pairs of each division swap places with the bottom pairs of the division above. With 4 to 6 pairs per division, moving 1 pair is gentle and moving 2 mixes levels faster. Some clubs move the winner up two divisions and the last pair down two. The generator moves the number you choose: tap <strong>Start next season</strong> and it builds the new divisions and an empty fixture list.</p>
<div class="tbl" style="margin-top:12px"><table><thead><tr><th>Table position</th><th>Next season</th></tr></thead><tbody>
<tr><td>1st (and 2nd if moving 2)</td><td>Up one division</td></tr>
<tr><td>Middle places</td><td>Stay</td></tr>
<tr><td>Last (and second last if moving 2)</td><td>Down one division</td></tr>
<tr><td>Top division winner</td><td>Champion, stays at the top</td></tr>
</tbody></table></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>How is a padel league table sorted when pairs are level on points?</h2></div>
<p>This generator sorts by points, then set difference, then game difference, then games won. Many leagues use the head-to-head result first: Roehampton Club, for example, uses head-to-head, then the fewest sets conceded per match, then a coin toss. Use whatever your rules say and settle it before the season.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>League, ladder, round robin or box league: which should you choose?</h2></div>
<div class="tbl"><table><thead><tr><th>Format</th><th>Best for</th><th>Tool</th></tr></thead><tbody>
<tr><td>League with divisions</td><td>A season of fixed pairs at a club, many levels</td><td>This page</td></tr>
<tr><td>Round robin, one evening</td><td>Fixed pairs, everyone meets in one session</td><td><a href="{href("round-robin.html")}">Round robin generator</a></td></tr>
<tr><td>Challenge ladder</td><td>Open-ended, pairs challenge the pair above</td><td><a href="{href("ladder.html")}">Ladder tracker</a></td></tr>
<tr><td>Groups then knockouts</td><td>A one-day tournament</td><td><a href="{href("padel-group-stage-generator.html")}">Group stage generator</a></td></tr>
<tr><td>Changing partners</td><td>Socials and players without a partner</td><td><a href="{href("americano.html")}">Americano</a> or <a href="{href("king-of-the-court.html")}">King of the Court</a></td></tr>
</tbody></table></div>
<p style="margin-top:12px">In the UK, clubs and county teams can also enter the LTA Padel National League, where men's and women's teams play in three divisions for a place in the National Finals. Entry goes through a county or district league administrator.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sh"><h2>What should padel league rules include?</h2></div><div class="grid">{_cards([
    ("Match format", "Sets to 6 with a tie-break at 6-6, and a super tie-break to 10 as the third set. Agree <a href='"+href("golden-point-star-point.html")+"'>golden point or advantage</a>."),
    ("Who books and pays", "Usually the pairs book a court between them inside the match week and split the cost. Say who brings new balls."),
    ("Missed matches", "A deadline (the end of the match week), then a walkover to the pair that was available. Points only when a match is played."),
    ("Rain and injuries", "Allow an unfinished score to stand or be finished later. If a pair withdraws, void their results so the table stays fair."),
    ("Self-umpiring and honesty", "Players call their own lines. Wrong results mean removal from the league. Our <a href='"+href("padel-etiquette.html")+"'>padel etiquette guide</a> covers the calls."),
    ("Substitutes", "Can a pair use a sub of the same level? Most social leagues allow one, if the opponents agree."),
], pill="Rule")}</div>
<p style="margin-top:12px">Need fair pairs first? Use the <a href="{href("padel-team-generator.html")}">padel team generator</a>. Keeping score on court: the <a href="{href("score.html")}">score keeper</a> or <a href="{href("padel-match-tracker.html")}">match tracker</a>. Finding players to fill a division: <a href="{href("padel-booking-apps.html")}">open matches and how to find players</a>.</p>
<p class="muted" style="margin-top:14px;font-size:.9rem">Sources, checked 28 Nov 2026: The Padel School "How to start a local padel meetup or league" (league grouped by level with a schedule and results, round robin usually best, 8 to 12 players, same day, time and venue each week, WhatsApp and a shared sheet); Roehampton Club "Padel league rules" overview (league runs of about six weeks, 4 to 6 pairs per division, best of 3 with a tie-break at 6-6 and a 10-point championship tie-break as the third set, points 4/3/2/1/0, head-to-head then sets conceded then coin toss, promotion and relegation by position, self-umpired); Playtomic Manager "Main concepts about leagues" (teams of two, groups by level, rounds, match weeks, 60/90/120-minute bookings, teams up and down set by the club); LTA Padel "LTA Padel National League" (three divisions, National Finals, entry via county or district administrators). The generator is our own. Written in our own words.</p></div></section>'''
lg_faq = [
    ("How do you organise a padel league?", "Get 8 or more players in fixed pairs, group them by level into divisions of 4 to 6 pairs, set a season of 4 to 6 weeks with one match a week, agree the format and points, collect results every week and move pairs up and down at the end."),
    ("How many pairs should be in a padel league division?", "Four to six pairs works best. Four pairs is 3 matches each; six pairs is 5 matches each, which fits a 5 or 6 week season."),
    ("What is the best scoring format for a padel league match?", "Best of 3 sets with a tie-break at 6-6, and a super tie-break to 10 points instead of a full third set. It fits a 90-minute court booking."),
    ("How many points for a win in a padel league?", "Two common systems: 4 for a 2-0 win, 3 for 2-1, 2 for a 1-2 loss and 1 for a 0-2 loss; or simply 3 for a win, 1 for a draw and 0 for a loss."),
    ("How long should a padel league season be?", "About 4 to 8 weeks. Roehampton Club runs leagues of about six weeks. Shorter seasons mean more promotion and relegation and fresher divisions."),
    ("What is the difference between a padel league and a ladder?", "A league has a fixed fixture list and season, then promotion and relegation. A ladder has no end: pairs challenge the pair above them and swap places if they win."),
]
page("padel-league.html", "Padel League Generator: Divisions, Fixtures, Table, Promotion",
     "Free padel league generator: split pairs into divisions, get week-by-week fixtures, a live league table with 4-3-2-1 or 3-point scoring, and promotion and relegation.",
     lg, lg_faq, "Padel league generator")

DEMAND_PAGES += ["padel-league.html"]
