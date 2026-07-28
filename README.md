# ADUCheatSheet.com — Programmatic SEO Site

## Structure
```
/
├── index.html              # Homepage with state/city grid
├── styles.css              # Global styles
├── template-city.html      # City page template
├── cities-data.json        # All city data
├── generate.py             # HTML generator
├── cities/                 # Generated city pages
│   ├── bakersfield-ca.html
│   ├── fresno-ca.html
│   └── ...
└── .gitignore
```

## How to Add a New City

1. Edit `cities-data.json` — add a new entry
2. Run `python3 generate.py`
3. Commit and push

## Deploy

Push to GitHub main branch → auto-deploys via Cloudflare Pages.
