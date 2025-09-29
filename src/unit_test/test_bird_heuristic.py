import unittest
from src.bird_heuristic import (
    preprocess_text,
    get_first_last_name,
    get_firt_index_value,
    calculate_similarity,
    process,
    bird_heuristic
)


class TestBirdHeuristic(unittest.TestCase):

    def test_preprocess_text(self):
        self.assertEqual(preprocess_text(" Jöhn, Doe! "), "john doe")
        self.assertEqual(preprocess_text(""), "")
        self.assertEqual(preprocess_text("ÁÉÍÓÚ"), "aeiou")

    def test_get_first_last_name(self):
        self.assertEqual(get_first_last_name("john doe"), ("john", "doe"))
        self.assertEqual(get_first_last_name("john"), ("john", ""))
        self.assertEqual(get_first_last_name("john michael doe"), ("john", "michael doe"))

    def test_get_firt_index_value(self):
        self.assertEqual(get_firt_index_value("john", "doe"), ("j", "d"))
        self.assertEqual(get_firt_index_value("a", "b"), ("", ""))  # too short
        self.assertEqual(get_firt_index_value("", ""), ("", ""))

    def test_calculate_similarity(self):
        self.assertAlmostEqual(calculate_similarity("john", "john"), 1.0, places=2)
        self.assertLess(calculate_similarity("john", "doe"), 0.5)

    def test_process(self):
        name, first, last, i_first, i_last, email, prefix = process(("John Doe", "jdoe@example.com"))
        self.assertEqual(name, "john doe")
        self.assertEqual(first, "john")
        self.assertEqual(last, "doe")
        self.assertEqual(i_first, "j")
        self.assertEqual(i_last, "d")
        self.assertEqual(email, "jdoe@example.com")
        self.assertEqual(prefix, "jdoe")

    def test_bird_heuristic(self):
        pair1 = {"name": "John Doe", "email": "jdoe@example.com"}
        pair2 = {"name": "J. Doe", "email": "john.doe@example.com"}
        result = bird_heuristic(pair1, pair2)
        self.assertIn("c1", result)
        self.assertIn("c2", result)
        self.assertIn("c3.1", result)
        self.assertIn("c3.2", result)
        self.assertIn("c4", result)
        self.assertIn("c5", result)
        self.assertIn("c6", result)
        self.assertIn("c7", result)
        self.assertGreaterEqual(result["c1"], 0.5)  # similarity should be reasonable


if __name__ == "__main__":
    unittest.main()
