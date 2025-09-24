import unittest
from src.bird_heuristic import normalize_text, levenshtein_similarity, parse_name, parse_email, bird_heuristic


class TestBirdHeuristic(unittest.TestCase):

    def test_normalize_text(self):
        self.assertEqual(normalize_text("  Jöhn  "), "john")
        self.assertEqual(normalize_text("DOE"), "doe")
        self.assertEqual(normalize_text(""), "")

    def test_levenshtein_similarity(self):
        self.assertAlmostEqual(levenshtein_similarity("john", "jon"), 0.86, places=2)
        self.assertEqual(levenshtein_similarity("abc", "abc"), 1.0)
        self.assertEqual(levenshtein_similarity("", ""), 1.0)

    def test_parse_name(self):
        self.assertEqual(parse_name("John Doe"), ("John", "Doe"))
        self.assertEqual(parse_name("John"), ("John", ""))
        self.assertEqual(parse_name(""), ("", ""))

    def test_parse_email(self):
        self.assertEqual(parse_email("jdoe@example.com"), ("jdoe", "example.com"))
        self.assertEqual(parse_email("invalidemail"), ("invalidemail", ""))
        self.assertEqual(parse_email(""), ("", ""))

    def test_bird_heuristic_output_structure(self):
        pair1 = {"name": "John Doe", "email": "jdoe@example.com"}
        pair2 = {"name": "J. Doe", "email": "john.doe@example.com"}
        result = bird_heuristic(pair1, pair2)
        expected_keys = {"name_1", "email_1", "name_2", "email_2",
                         "c1", "c2", "c3.1", "c3.2", "c4", "c5", "c6", "c7"}
        self.assertTrue(expected_keys.issubset(result.keys()))

    def test_bird_heuristic_similarity_values(self):
        pair1 = {"name": "John Doe", "email": "jdoe@example.com"}
        pair2 = {"name": "Jon Doe", "email": "jon.doe@example.com"}
        result = bird_heuristic(pair1, pair2)
        self.assertGreater(result["c1"], 0.7)  # name similarity
        self.assertGreater(result["c2"], 0.5)  # email prefix similarity


if __name__ == "__main__":
    unittest.main()
