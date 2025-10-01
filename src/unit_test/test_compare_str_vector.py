import unittest
import numpy as np
from unittest.mock import patch
import src.compare_str_vector as csv


class TestCompareStrVector(unittest.TestCase):
    def test_cosine_similarity_identical(self):
        v = np.array([1, 2, 3])
        self.assertTrue(np.isclose(csv.cosine_similarity(v, v), 1.0))

    def test_cosine_similarity_orthogonal(self):
        v1 = np.array([1, 0])
        v2 = np.array([0, 1])
        self.assertTrue(np.isclose(csv.cosine_similarity(v1, v2), 0.0))

    def test_cosine_similarity_opposite(self):
        v1 = np.array([1, 0])
        v2 = np.array([-1, 0])
        self.assertTrue(np.isclose(csv.cosine_similarity(v1, v2), -1.0))

    @patch("src.compare_str_vector.model.encode", return_value=np.array([0.1, 0.2, 0.3]))
    def test_get_embedding(self, mock_encode):
        result = csv.get_embedding("hello")
        self.assertIsInstance(result, np.ndarray)
        np.testing.assert_array_equal(result, np.array([0.1, 0.2, 0.3]))
        mock_encode.assert_called_once_with("hello")

    @patch("src.compare_str_vector.get_embedding", side_effect=[np.array([1, 0]), np.array([0, 1])])
    def test_compare_texts(self, mock_get_embedding):
        sim = csv.compare_texts("text1", "text2")
        self.assertTrue(np.isclose(sim, 0.0))
        self.assertEqual(mock_get_embedding.call_count, 2)


if __name__ == "__main__":
    unittest.main()
