import numpy as np
from unittest.mock import patch
import src.compare_str_vector as csv


def test_cosine_similarity_identical():
    v = np.array([1, 2, 3])
    assert np.isclose(csv.cosine_similarity(v, v), 1.0)

def test_cosine_similarity_orthogonal():
    v1 = np.array([1, 0])
    v2 = np.array([0, 1])
    assert np.isclose(csv.cosine_similarity(v1, v2), 0.0)

def test_cosine_similarity_opposite():
    v1 = np.array([1, 0])
    v2 = np.array([-1, 0])
    assert np.isclose(csv.cosine_similarity(v1, v2), -1.0)

@patch("src.compare_str_vector.model.encode", return_value=np.array([0.1, 0.2, 0.3]))
def test_get_embedding(mock_encode):
    result = csv.get_embedding("hello")
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, np.array([0.1, 0.2, 0.3]))
    mock_encode.assert_called_once_with("hello")

@patch("src.compare_str_vector.get_embedding", side_effect=[np.array([1, 0]), np.array([0, 1])])
def test_compare_texts(mock_get_embedding):
    sim = csv.compare_texts("text1", "text2")
    assert np.isclose(sim, 0.0)
    assert mock_get_embedding.call_count == 2
