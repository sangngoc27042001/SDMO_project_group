import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os

import src.mine_and_dedupe as mad


class TestMineAndDedupe(unittest.TestCase):

    def test_hash_repo_url(self):
        h1 = mad.hash_repo_url("https://github.com/test/repo.git", 100)
        h2 = mad.hash_repo_url("https://github.com/test/repo.git", 200)
        self.assertNotEqual(h1, h2)
        self.assertEqual(len(h1), 12)

    def test_handle_two_pairs(self):
        p1 = {"name": "Alice", "email": "alice@example.com"}
        p2 = {"name": "Alicia", "email": "alice@sample.com"}
        with patch("src.mine_and_dedupe.bird_heuristic", return_value=True):
            result = mad.handle_two_pairs(p1, p2)
            self.assertTrue(result)

    def test_apply_bird_with_mock(self):
        pairs = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Alicia", "email": "alice@sample.com"},
            {"name": "Bob", "email": "bob@example.com"},
        ]
        with patch("src.mine_and_dedupe.handle_two_pairs") as mock_handle:
            mock_handle.side_effect = lambda p1, p2: {"c1": 1.0, "c2": 0.9, "c3.1": 1.0, "c3.2": 1.0,
                                                      "c4": False, "c5": False, "c6": False, "c7": False,
                                                      "name_1": p1["name"], "email_1": p1["email"],
                                                      "name_2": p2["name"], "email_2": p2["email"]}
            with patch("pandas.DataFrame.to_csv") as mock_to_csv:
                results = mad.apply_bird("fake_repo", pairs)
            self.assertIsInstance(results, list)
            self.assertTrue(all("name_1" in r for r in results))

    def test_boolean_bird_heuristic(self):
        two_pairs = {
            "c1": 0.9, "c2": 0.1, "c3.1": 0.1, "c3.2": 0.1,
            "c4": False, "c5": False, "c6": False, "c7": False
        }
        result = mad.bird_heuristic(
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Alicia", "email": "alice@sample.com"}
        )
        self.assertGreaterEqual(result["c1"], 0.0)  # just ensure similarity key exists

    def test_filter_pairs(self):
        repo_url = "fake_repo"
        devs_similarity = [
            {"c1": 0.9, "c2": 0.1, "c3.1": 0.1, "c3.2": 0.1,
             "c4": False, "c5": False, "c6": False, "c7": False,
             "name_1": "Alice", "email_1": "alice@example.com",
             "name_2": "Alicia", "email_2": "alice@sample.com"},
            {"c1": 0.1, "c2": 0.1, "c3.1": 0.1, "c3.2": 0.1,
             "c4": False, "c5": False, "c6": False, "c7": False,
             "name_1": "Bob", "email_1": "bob@example.com",
             "name_2": "Charlie", "email_2": "charlie@example.com"},
        ]
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            results = mad.filter_pairs(repo_url, devs_similarity, thresh_hold=0.8)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name_1"], "Alice")


if __name__ == "__main__":
    unittest.main()
