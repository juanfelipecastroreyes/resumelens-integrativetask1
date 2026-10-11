import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from sorter import PROFILE_ORDER, sort_tokens
from transducers import CATEGORIES, normalize

class TestSortTokens(unittest.TestCase):
    def test_assignment_example(self):
        tokens = ["GIT", "NODE_JS", "JAVASCRIPT", "POSTGRESQL", "REACT"]
        expected = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        self.assertEqual(sort_tokens(tokens, "full_stack"), expected)

    def test_order_does_not_depend_on_input_order(self):
        first = ["REACT", "GIT", "JAVASCRIPT", "NODE_JS", "POSTGRESQL"]
        second = ["POSTGRESQL", "NODE_JS", "REACT", "JAVASCRIPT", "GIT"]
        self.assertEqual(sort_tokens(first, "full_stack"), sort_tokens(second, "full_stack"))

    def test_ml_engineer(self):
        tokens = ["GIT", "TENSORFLOW", "SQL", "PANDAS", "PYTHON", "SCIKIT_LEARN"]
        expected = ["PYTHON", "SQL", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "GIT"]
        self.assertEqual(sort_tokens(tokens, "ml_engineer"), expected)

    def test_tokens_outside_the_profile_go_last(self):
        tokens = ["KERAS", "GIT", "REACT"]
        self.assertEqual(sort_tokens(tokens, "full_stack"), ["REACT", "GIT", "KERAS"])

    def test_empty_list(self):
        self.assertEqual(sort_tokens([], "full_stack"), [])

    def test_unknown_profile(self):
        with self.assertRaises(KeyError):
            sort_tokens(["GIT"], "cook")

    def test_profile_tokens_exist_in_the_vocabulary(self):
        vocabulary = []
        for category in CATEGORIES:
            for pair in CATEGORIES[category]:
                vocabulary.append(pair[1])
        for profile in PROFILE_ORDER:
            for token in PROFILE_ORDER[profile]:
                self.assertIn(token, vocabulary)

    def test_profile_has_no_repeated_token(self):
        for profile in PROFILE_ORDER:
            self.assertEqual(len(PROFILE_ORDER[profile]), len(set(PROFILE_ORDER[profile])))

class TestNormalizeAndSort(unittest.TestCase):
    def test_full_stack_example(self):
        tokens = normalize(["Git", "NodeJS", "JS", "Postgres", "React.js"])["tokens"]
        expected = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        self.assertEqual(sort_tokens(tokens, "full_stack"), expected)

if __name__ == "__main__":
    unittest.main()
