import datetime as dt

from lunch_utility import decide_lunch


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
