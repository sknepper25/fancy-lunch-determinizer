#!/usr/bin/env python3
"""Machine shop lunch decision utility.

The shop lunch schedule rules are:
- Thursday: company provided lunch (restaurant delivery/catering or grill-out)
- Friday: the crew goes out together to one restaurant

This script picks a deterministic option for a given date so everyone gets
consistent answers for the same day.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
from dataclasses import dataclass


THURSDAY_OPTIONS = [
    "Taco bar catering",
    "BBQ brisket plates",
    "Burgers & dogs grill-out",
    "Build-your-own burrito bowls",
    "Pizza + salad combo",
    "Fried chicken and sides",
    "Pulled pork sandwiches",
    "Sandwich platter and chips",
]

FRIDAY_RESTAURANTS = [
    "Iron Skillet Diner",
    "Mesa Grill",
    "Foundry Smokehouse",
    "Rivertown Mexican Kitchen",
    "Main Street Burgers",
    "The Noodle Joint",
    "Depot Pizza Co.",
    "Sakura Hibachi",
]


@dataclass(frozen=True)
class LunchDecision:
    date: dt.date
    day_name: str
    decision_type: str
    choice: str


def _stable_index(key: str, length: int) -> int:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest, 16) % length


def decide_lunch(day: dt.date) -> LunchDecision:
    weekday = day.weekday()  # Monday=0 ... Sunday=6
    day_name = day.strftime("%A")

    if weekday == 3:  # Thursday
        index = _stable_index(f"THU-{day.isoformat()}", len(THURSDAY_OPTIONS))
        return LunchDecision(
            date=day,
            day_name=day_name,
            decision_type="Company lunch (delivery/catering or grill-out)",
            choice=THURSDAY_OPTIONS[index],
        )

    if weekday == 4:  # Friday
        index = _stable_index(f"FRI-{day.isoformat()}", len(FRIDAY_RESTAURANTS))
        return LunchDecision(
            date=day,
            day_name=day_name,
            decision_type="Shop crew restaurant outing",
            choice=FRIDAY_RESTAURANTS[index],
        )

    return LunchDecision(
        date=day,
        day_name=day_name,
        decision_type="No special group lunch rule",
        choice="Pack your own lunch or choose individually",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Determine the machine shop lunch choice for a given day."
    )
    parser.add_argument(
        "--date",
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.date:
        chosen_date = dt.date.fromisoformat(args.date)
    else:
        chosen_date = dt.date.today()

    decision = decide_lunch(chosen_date)

    print(f"Date: {decision.date.isoformat()} ({decision.day_name})")
    print(f"Type: {decision.decision_type}")
    print(f"Choice: {decision.choice}")


if __name__ == "__main__":
    main()
