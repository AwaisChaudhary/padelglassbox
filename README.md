# Padel Glass Box

Free padel tools and plain-English guides: racket finder, score keeper, tappable rules court, shot library, beginner checklists and glossary. Live at https://padelglassbox.com

- `assets/data.json`: court zones, shots, glossary
- `assets/app.js`: all interactive tools, including the live 3D court on the home page
- `assets/style.css`: the "glass box" design system
- `build.py`: builds every page, sitemap.xml and robots.txt. `python3 build.py` = live build (clean URLs). `python3 build.py --preview` = local file:// preview. Never hand-edit .html.

Hosted on Cloudflare Pages: every push to `main` deploys automatically.
