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
import sys
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
        description=(
            "Determine the machine shop lunch choice for a given day. "
            "Run with no flags for today's lunch, or use --interactive for"
            " a guided prompt."
        ),
        epilog=(
            "Examples:\n"
            "  python3 lunch_utility.py\n"
            "  python3 lunch_utility.py --date 2026-03-12\n"
            "  python3 lunch_utility.py --interactive"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--date",
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Walk through date selection with prompts.",
    )
    parser.add_argument(
        "--show-rules",
        action="store_true",
        help="Print lunch rules and exit.",
    )
    return parser.parse_args()


def _print_rules() -> None:
    print("Lunch rules:")
    print("- Thursday: company-provided lunch")
    print("- Friday: everyone goes out together")
    print("- Other days: individual choice")


def _parse_date_or_exit(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        print(
            "Could not read that date. Please use YYYY-MM-DD, "
            "for example 2026-03-12.",
            file=sys.stderr,
        )
        raise SystemExit(2)


def _choose_date_interactively() -> dt.date:
    print("\nLet's pick a date for your lunch decision.")
    answer = input("Use today's date? [Y/n]: ").strip().lower()
    if answer in {"", "y", "yes"}:
        return dt.date.today()

    while True:
        entered = input("Enter a date (YYYY-MM-DD): ").strip()
        try:
            return dt.date.fromisoformat(entered)
        except ValueError:
            print("Sorry, that wasn't a valid date. Please try again.")


def _print_decision(decision: LunchDecision) -> None:
    print("\nLunch plan")
    print("-" * 10)
    print(f"Date: {decision.date.isoformat()} ({decision.day_name})")
    print(f"Rule used: {decision.decision_type}")
    print(f"Today's plan: {decision.choice}")


def main() -> None:
    args = parse_args()

    if args.show_rules:
        _print_rules()
        return

    if args.interactive:
        chosen_date = _choose_date_interactively()
    elif args.date:
        chosen_date = _parse_date_or_exit(args.date)
    else:
        chosen_date = dt.date.today()

    decision = decide_lunch(chosen_date)
    _print_decision(decision)


if __name__ == "__main__":
    main()
