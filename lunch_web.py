#!/usr/bin/env python3
"""Simple web interface for the lunch determinizer."""

from __future__ import annotations

import datetime as dt
from html import escape
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from lunch_utility import LunchDecision, decide_lunch


def _try_parse_date(value: str) -> tuple[dt.date | None, str | None]:
    if not value:
        return dt.date.today(), None

    try:
        return dt.date.fromisoformat(value), None
    except ValueError:
        return None, "Please enter a valid date in YYYY-MM-DD format."


def _render_decision(decision: LunchDecision) -> str:
    return (
        "<section class='card' aria-live='polite'>"
        "<h2>Lunch Plan</h2>"
        f"<p><strong>Date:</strong> {decision.date.isoformat()} ({escape(decision.day_name)})</p>"
        f"<p><strong>Rule:</strong> {escape(decision.decision_type)}</p>"
        f"<p><strong>Choice:</strong> {escape(decision.choice)}</p>"
        "</section>"
    )


def _render_page(date_text: str, decision: LunchDecision | None, error: str | None) -> bytes:
    error_html = f"<p class='error' role='alert'>{escape(error)}</p>" if error else ""
    decision_html = _render_decision(decision) if decision else ""

    html = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Fancy Lunch Determinizer</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem auto; max-width: 760px; line-height: 1.5; padding: 0 1rem; }}
    h1 {{ margin-bottom: .25rem; }}
    .hint {{ color: #444; margin-top: 0; }}
    form {{ display: flex; flex-wrap: wrap; gap: .75rem; align-items: end; margin: 1rem 0 1.5rem; }}
    label {{ font-weight: 600; }}
    input[type=date] {{ padding: .45rem; font-size: 1rem; }}
    button {{ padding: .5rem .85rem; font-size: 1rem; cursor: pointer; }}
    .card {{ border: 1px solid #d1d5db; border-radius: 8px; padding: 1rem; background: #fafafa; }}
    .error {{ color: #b00020; font-weight: 700; }}
  </style>
</head>
<body>
  <main>
    <h1>Fancy Lunch Determinizer</h1>
    <p class="hint">Pick a date to get a deterministic lunch plan.</p>

    <form method="get" action="/">
      <div>
        <label for="date">Date</label><br />
        <input id="date" name="date" type="date" value="{escape(date_text)}" />
      </div>
      <button type="submit">Get lunch plan</button>
    </form>

    {error_html}
    {decision_html}

    <section>
      <h2>Rules</h2>
      <ul>
        <li><strong>Thursday:</strong> company-provided lunch.</li>
        <li><strong>Friday:</strong> everyone goes out together.</li>
        <li><strong>Other days:</strong> individual choice.</li>
      </ul>
    </section>
  </main>
</body>
</html>
"""
    return html.encode("utf-8")


def app(environ: dict, start_response) -> list[bytes]:
    params = parse_qs(environ.get("QUERY_STRING", ""))
    date_text = params.get("date", [""])[0]
    selected_date, error = _try_parse_date(date_text)

    decision = decide_lunch(selected_date) if selected_date else None
    date_field_value = selected_date.isoformat() if selected_date else date_text

    page = _render_page(date_field_value, decision, error)
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(page))),
        ],
    )
    return [page]


def main() -> None:
    host = "0.0.0.0"
    port = 8000
    print(f"Serving Fancy Lunch Determinizer at http://{host}:{port}")
    with make_server(host, port, app) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
