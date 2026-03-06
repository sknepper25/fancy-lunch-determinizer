from wsgiref.util import setup_testing_defaults

from lunch_web import _try_parse_date, app


def _call_app(query_string: str):
    environ = {}
    setup_testing_defaults(environ)
    environ["QUERY_STRING"] = query_string
    status_headers = {}

    def start_response(status, headers):
        status_headers["status"] = status
        status_headers["headers"] = headers

    body = b"".join(app(environ, start_response)).decode("utf-8")
    return status_headers["status"], body


def test_try_parse_date_valid():
    selected, error = _try_parse_date("2026-03-12")
    assert selected is not None
    assert selected.isoformat() == "2026-03-12"
    assert error is None


def test_try_parse_date_invalid():
    selected, error = _try_parse_date("03/12/2026")
    assert selected is None
    assert error == "Please enter a valid date in YYYY-MM-DD format."


def test_app_renders_plan_for_selected_date():
    status, body = _call_app("date=2026-03-13")
    assert status == "200 OK"
    assert "Lunch Plan" in body
    assert "Shop crew restaurant outing" in body


def test_app_shows_error_for_bad_date():
    status, body = _call_app("date=03/13/2026")
    assert status == "200 OK"
    assert "Please enter a valid date in YYYY-MM-DD format." in body
