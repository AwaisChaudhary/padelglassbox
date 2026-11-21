# Padel Glass Box

Free padel tools and plain-English guides: racket finder, score keeper, tappable rules court, shot library, beginner checklists and glossary. Live at https://padelglassbox.com

- `assets/data.json`: court zones, shots, glossary
- `assets/app.js`: all interactive tools, including the live 3D court on the home page
- `assets/style.css`: the "glass box" design system
- `build.py`: builds every page, sitemap.xml and robots.txt. `python3 build.py` = live build (clean URLs). `python3 build.py --preview` = local file:// preview. Never hand-edit .html.

Hosted on Cloudflare Pages: every push to `main` deploys automatically.

## Standing rule: ChatGPT and AI answers (added 21 Nov 2026 at Awais's request)
ChatGPT now sends about 90% of NeonCoast's visitors: it links pages that give a direct, specific, up-to-date answer plus something useful to do next. Every run on this site follows this on each new or refreshed page:
- Open with a 1-2 sentence "Quick answer" that states the specific answer (numbers, sizes, prices, steps), then the detail.
- Use question-style H2s that match how people ask, keep a visible "Last checked/updated" date, and add FAQ JSON-LD for those questions.
- Make facts easy to quote: short lists and tables, one fact per line, units included.
- Keep visitors on the site: end every page and every tool result with 2-3 links to related pages or tools ("what next").
- Keep robots.txt open to all crawlers (Bingbot, OAI-SearchBot, GPTBot included); never add blocks.
