import datetime as dt
import pytest

from lunch_utility import decide_lunch
from lunch_utility import _parse_date_or_exit


def test_thursday_is_company_lunch():
    result = decide_lunch(dt.date(2026, 3, 12))  # Thursday
    assert result.day_name == "Thursday"
    assert result.decision_type == "Company lunch (delivery/catering or grill-out)"


def test_friday_is_restaurant_outing():
    result = decide_lunch(dt.date(2026, 3, 13))  # Friday
    assert result.day_name == "Friday"
    assert result.decision_type == "Shop crew restaurant outing"


def test_other_day_has_no_special_rule():
    result = decide_lunch(dt.date(2026, 3, 11))  # Wednesday
    assert result.decision_type == "No special group lunch rule"


def test_parse_date_or_exit_parses_valid_date():
    result = _parse_date_or_exit("2026-03-12")
    assert result == dt.date(2026, 3, 12)


def test_parse_date_or_exit_exits_on_bad_input():
    with pytest.raises(SystemExit) as exc_info:
        _parse_date_or_exit("03/12/2026")
    assert exc_info.value.code == 2
