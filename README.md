# Fancy Lunch Determinizer

A small utility for a machine shop to decide the lunch plan by day.

## Rules baked in

- **Thursday:** company-provided lunch (restaurant/catering or grill-out)
- **Friday:** everyone goes out together to one restaurant
- **Other days:** no group rule

## GitHub Pages (static HTML)

A GitHub Pages-ready version of the app is in `docs/index.html`. You can also open this file directly in a browser without running a server.

1. Push this repo to GitHub.
2. In **Settings → Pages**, choose **Deploy from a branch**.
3. Select your default branch and `/docs` as the folder.
4. Save, then open the published URL GitHub provides.

## Website (recommended)

```bash
python3 lunch_web.py
```

Then open: `http://localhost:8000`

This gives you a simple page where you choose a date and click **Get lunch plan**.

## CLI Usage (optional)

```bash
# Fastest option: use today's date
python3 lunch_utility.py

# Pick a specific date
python3 lunch_utility.py --date 2026-03-12

# Show the rules in plain language
python3 lunch_utility.py --show-rules

# Guided prompts (helpful if you don't want to remember flags)
python3 lunch_utility.py --interactive
```

The pick is deterministic for a given date, so if people run it multiple times on
that same day they see the same answer.
