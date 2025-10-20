from src.bird_heuristic import (
    preprocess_text,
    get_first_last_name,
    get_firt_index_value,
    calculate_similarity,
    process,
    bird_heuristic
)


def test_preprocess_text():
    assert preprocess_text(" Jöhn, Doe! ") == "john doe"
    assert preprocess_text("") == ""
    assert preprocess_text("ÁÉÍÓÚ") == "aeiou"

def test_get_first_last_name():
    assert get_first_last_name("john doe") == ("john", "doe")
    assert get_first_last_name("john") == ("john", "")
    assert get_first_last_name("john michael doe") == ("john", "michael doe")

def test_get_firt_index_value():
    assert get_firt_index_value("john", "doe") == ("j", "d")
    assert get_firt_index_value("a", "b") == ("", "")  # too short
    assert get_firt_index_value("", "") == ("", "")

def test_calculate_similarity():
    assert round(calculate_similarity("john", "john"), 2) == 1.0
    assert calculate_similarity("john", "doe") < 0.5

def test_process():
    name, first, last, i_first, i_last, email, prefix = process(("John Doe", "jdoe@example.com"))
    assert name == "john doe"
    assert first == "john"
    assert last == "doe"
    assert i_first == "j"
    assert i_last == "d"
    assert email == "jdoe@example.com"
    assert prefix == "jdoe"

def test_bird_heuristic():
    pair1 = {"name": "John Doe", "email": "jdoe@example.com"}
    pair2 = {"name": "J. Doe", "email": "john.doe@example.com"}
    result = bird_heuristic(pair1, pair2)
    for key in ["c1", "c2", "c3.1", "c3.2", "c4", "c5", "c6", "c7"]:
        assert key in result
    assert result["c1"] >= 0.5  # similarity should be reasonable
