import unittest
from unittest.mock import patch, MagicMock
import src.proposed_method as pm


class TestProposedMethod(unittest.TestCase):
    @patch("src.proposed_method.compare_texts", side_effect=[0.9, 0.8, 0.7, 0.6])
    def test_handle_two_pairs_proposed(self, mock_compare):
        p1 = {"name": "Alice", "email": "alice@example.com"}
        p2 = {"name": "Alicia", "email": "alicia@example.org"}
        result = pm.handle_two_pairs_proposed(p1, p2)

        self.assertEqual(result["name_1"], "Alice")
        self.assertEqual(result["email_1"], "alice@example.com")
        self.assertEqual(result["name_2"], "Alicia")
        self.assertEqual(result["email_2"], "alicia@example.org")
        self.assertEqual(result["c1"], 0.9)
        self.assertEqual(result["c2"], 0.8)
        self.assertEqual(result["c3"], 0.7)
        self.assertEqual(result["c4"], 0.6)
        self.assertEqual(mock_compare.call_count, 4)

    @patch("src.proposed_method.hash_repo_url", return_value="fakehash")
    @patch("src.proposed_method.os.path.exists", return_value=True)
    @patch("src.proposed_method.pd.read_csv")
    def test_apply_proposed_method_cache_hit(self, mock_read_csv, mock_exists, mock_hash):
        mock_read_csv.return_value.to_dict.return_value = [{"name_1": "Alice"}]
        result = pm.apply_proposed_method("repo_url", [{"name_1": "Alice", "email_1": "a", "name_2": "Bob", "email_2": "b"}])
        self.assertEqual(result, [{"name_1": "Alice"}])
        mock_read_csv.assert_called_once()

    @patch("src.proposed_method.hash_repo_url", return_value="fakehash")
    @patch("src.proposed_method.os.path.exists", return_value=False)
    @patch("src.proposed_method.compare_texts", return_value=0.5)
    @patch("src.proposed_method.pd.DataFrame.to_csv")
    def test_apply_proposed_method_cache_miss(self, mock_to_csv, mock_compare, mock_exists, mock_hash):
        pairs = [{"name_1": "Alice", "email_1": "a", "name_2": "Bob", "email_2": "b"}]
        result = pm.apply_proposed_method("repo_url", pairs)
        self.assertIsInstance(result, list)
        self.assertIn("c1", result[0])
        mock_to_csv.assert_called_once()

    @patch("src.proposed_method.hash_repo_url", return_value="fakehash")
    @patch("src.proposed_method.pd.DataFrame.to_csv")
    def test_filter_pairs_proposed(self, mock_to_csv, mock_hash):
        devs_similarity = [
            {"name_1": "Alice", "email_1": "a", "name_2": "Bob", "email_2": "b", "c1": 0.7, "c2": 0.2, "c3": 0.1, "c4": 0.0},
            {"name_1": "Charlie", "email_1": "c", "name_2": "Dave", "email_2": "d", "c1": 0.1, "c2": 0.2, "c3": 0.3, "c4": 0.4},
        ]
        result = pm.filter_pairs_proposed("repo_url", devs_similarity, thresh_hold=0.6)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name_1"], "Alice")
        mock_to_csv.assert_called_once()


if __name__ == "__main__":
    unittest.main()
