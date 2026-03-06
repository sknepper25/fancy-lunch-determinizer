# Fancy Lunch Determinizer

A small utility for a machine shop to decide the lunch plan by day.

## Rules baked in

- **Thursday:** company-provided lunch (restaurant/catering or grill-out)
- **Friday:** everyone goes out together to one restaurant
- **Other days:** no group rule

## Usage

```bash
python3 lunch_utility.py
python3 lunch_utility.py --date 2026-03-12
```

The pick is deterministic for a given date, so if people run it multiple times on
the same day they see the same answer.
