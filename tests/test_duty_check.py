from app.main import duty_check


def test_lines_add_up():
    f = {"lines": [{"duties": [100.0, 25.5]}, {"duties": [10]}], "total_duty": 135.5}
    assert duty_check(f)["ok"] is True


def test_misread_digit_flagged():
    f = {"lines": [{"duties": [1000.0, 25.5]}, {"duties": [10]}], "total_duty": 135.5}
    r = duty_check(f)
    assert r["ok"] is False and r["gap"] == -900.0


def test_missing_values():
    assert duty_check({"lines": [], "total_duty": 0})["ok"] is None
    assert duty_check({"lines": [{"duties": [100.0]}], "total_duty": 0})["reason"] == "Block 37 not read"
