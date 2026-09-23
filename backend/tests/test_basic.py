def is_valid_status(status):
    return status in ["available", "maintenance", "unavailable"]


def test_valid_status():
    assert is_valid_status("available") == True
    assert is_valid_status("random") == False

def test_numbers(sample_numbers):
    assert len(sample_numbers) == 5