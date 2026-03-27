import pytest

from src.dac import solve_dac
from src.dp import edit_distance_dp, edit_distance_dp_optimized, reconstruct_operations


# Casos con resultado conocido
KNOWN_CASES = [
    ("", "", 0),
    ("", "abc", 3),
    ("xyz", "", 3),
    ("a", "a", 0),
    ("a", "b", 1),
    ("abc", "abc", 0),
    ("abc", "abd", 1),
    ("abc", "abcd", 1),
    ("abcd", "abc", 1),
    ("kitten", "sitting", 3),
    ("abc", "xyz", 3),
    ("abcde", "vwxyz", 5),
    ("aaaa", "bbbb", 4),
    ("sunday", "saturday", 3),
    ("intention", "execution", 5),
    ("horse", "ros", 3),
]


class TestDaC:
    @pytest.mark.parametrize("x,y,expected", KNOWN_CASES)
    def test_known_cases(self, x, y, expected):
        assert solve_dac(x, y) == expected

    def test_symmetry(self):
        """d(x, y) == d(y, x)"""
        assert solve_dac("kitten", "sitting") == solve_dac("sitting", "kitten")

    def test_identity(self):
        """d(x, x) == 0"""
        assert solve_dac("hello", "hello") == 0

    def test_upper_bound(self):
        """d(x, y) <= max(m, n)"""
        x, y = "abc", "xyz"
        assert solve_dac(x, y) <= max(len(x), len(y))

    def test_lower_bound(self):
        """d(x, y) >= |m - n|"""
        x, y = "ab", "abcde"
        assert solve_dac(x, y) >= abs(len(x) - len(y))


class TestDP:
    @pytest.mark.parametrize("x,y,expected", KNOWN_CASES)
    def test_known_cases(self, x, y, expected):
        assert edit_distance_dp(x, y) == expected

    @pytest.mark.parametrize("x,y,expected", KNOWN_CASES)
    def test_optimized_matches(self, x, y, expected):
        assert edit_distance_dp_optimized(x, y) == expected

    def test_symmetry(self):
        assert edit_distance_dp("kitten", "sitting") == edit_distance_dp("sitting", "kitten")

    def test_identity(self):
        assert edit_distance_dp("hello", "hello") == 0

    def test_upper_bound(self):
        x, y = "abc", "xyz"
        assert edit_distance_dp(x, y) <= max(len(x), len(y))

    def test_lower_bound(self):
        x, y = "ab", "abcde"
        assert edit_distance_dp(x, y) >= abs(len(x) - len(y))

    def test_large_input(self):
        """DP debe manejar entradas grandes sin problema."""
        x = "a" * 500
        y = "b" * 500
        assert edit_distance_dp(x, y) == 500


class TestConsistency:
    @pytest.mark.parametrize("x,y,expected", KNOWN_CASES)
    def test_dac_equals_dp(self, x, y, expected):
        assert solve_dac(x, y) == edit_distance_dp(x, y)

    def test_optimized_equals_full(self):
        x, y = "kitten", "sitting"
        assert edit_distance_dp(x, y) == edit_distance_dp_optimized(x, y)


class TestReconstruction:
    def test_operations_count(self):
        x, y = "kitten", "sitting"
        ops = reconstruct_operations(x, y)
        assert len(ops) == edit_distance_dp(x, y)

    def test_empty_for_identical(self):
        ops = reconstruct_operations("abc", "abc")
        assert len(ops) == 0

    def test_all_inserts(self):
        ops = reconstruct_operations("", "abc")
        assert len(ops) == 3
        assert all("Insert" in op for op in ops)

    def test_all_deletes(self):
        ops = reconstruct_operations("abc", "")
        assert len(ops) == 3
        assert all("Delete" in op for op in ops)
