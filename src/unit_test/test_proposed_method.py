from unittest.mock import patch, MagicMock
import src.proposed_method as pm


@patch("src.proposed_method.compare_texts", side_effect=[0.9, 0.8, 0.7, 0.6])
def test_handle_two_pairs_proposed(mock_compare):
    p1 = {"name": "Alice", "email": "alice@example.com"}
    p2 = {"name": "Alicia", "email": "alicia@example.org"}
    result = pm.handle_two_pairs_proposed(p1, p2)

    assert result["name_1"] == "Alice"
    assert result["email_1"] == "alice@example.com"
    assert result["name_2"] == "Alicia"
    assert result["email_2"] == "alicia@example.org"
    assert result["c1"] == 0.9
    assert result["c2"] == 0.8
    assert result["c3"] == 0.7
    assert result["c4"] == 0.6
    assert mock_compare.call_count == 4


@patch("src.proposed_method.hash_repo_url", return_value="fakehash")
@patch("src.proposed_method.os.path.exists", return_value=True)
@patch("src.proposed_method.pd.read_csv")
def test_apply_proposed_method_cache_hit(mock_read_csv, mock_exists, mock_hash):
    mock_read_csv.return_value.to_dict.return_value = [{"name_1": "Alice"}]
    result = pm.apply_proposed_method("repo_url", [{"name_1": "Alice", "email_1": "a", "name_2": "Bob", "email_2": "b"}])
    assert result == [{"name_1": "Alice"}]
    mock_read_csv.assert_called_once()


@patch("src.proposed_method.hash_repo_url", return_value="fakehash")
@patch("src.proposed_method.os.path.exists", return_value=False)
@patch("src.proposed_method.compare_texts", return_value=0.5)
@patch("src.proposed_method.pd.DataFrame.to_csv")
def test_apply_proposed_method_cache_miss(mock_to_csv, mock_compare, mock_exists, mock_hash):
    pairs = [{"name_1": "Alice", "email_1": "a", "name_2": "Bob", "email_2": "b"}]
    result = pm.apply_proposed_method("repo_url", pairs)
    assert isinstance(result, list)
    assert "c1" in result[0]
    mock_to_csv.assert_called_once()


@patch("src.proposed_method.hash_repo_url", return_value="fakehash")
@patch("src.proposed_method.pd.DataFrame.to_csv")
def test_filter_pairs_proposed(mock_to_csv, mock_hash):
    devs_similarity = [
        {"name_1": "Alice", "email_1": "a", "name_2": "Bob", "email_2": "b", "c1": 0.7, "c2": 0.2, "c3": 0.1, "c4": 0.0},
        {"name_1": "Charlie", "email_1": "c", "name_2": "Dave", "email_2": "d", "c1": 0.1, "c2": 0.2, "c3": 0.3, "c4": 0.4},
    ]
    result = pm.filter_pairs_proposed("repo_url", devs_similarity, thresh_hold=0.6)
    assert len(result) == 1
    assert result[0]["name_1"] == "Alice"
    mock_to_csv.assert_called_once()
