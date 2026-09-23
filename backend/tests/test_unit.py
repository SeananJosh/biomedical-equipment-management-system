import pytest


def calculate_maintenance_cost(hours, rate):
    if hours < 0:
        raise ValueError("Hours cannot be negative")

    return hours * rate


@pytest.mark.parametrize(
    "hours, rate, expected",
    [
        (5, 100, 500),
        (10, 200, 2000),
        (2, 150, 300),
        (8, 250, 2000),
    ]
)
def test_calculate_maintenance_cost(hours, rate, expected):
    result = calculate_maintenance_cost(hours, rate)

    assert result == expected


def test_negative_hours():
    with pytest.raises(ValueError):
        calculate_maintenance_cost(-5, 100)