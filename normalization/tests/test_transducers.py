import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "extraction", "src"))

from transducers import CATEGORIES, build_all, normalize, normalize_skill, simplify
from extractor import extract_file

EXAMPLES = os.path.join(HERE, "..", "..", "extraction", "examples")

class TestSimplify(unittest.TestCase):
    def test_removes_symbols_and_capitals(self):
        self.assertEqual(simplify("Node.js"), "nodejs")
        self.assertEqual(simplify("Scikit-learn"), "scikitlearn")
        self.assertEqual(simplify("Tensor Flow"), "tensorflow")
        self.assertEqual(simplify("CI/CD"), "cicd")

class TestNormalizeSkill(unittest.TestCase):
    def setUp(self):
        self.transducers = build_all()

    def check(self, skill, expected):
        self.assertEqual(normalize_skill(skill, self.transducers), expected)

    def test_javascript(self):
        self.check("JS", "JAVASCRIPT")
        self.check("Javascript", "JAVASCRIPT")

    def test_react(self):
        self.check("React.js", "REACT")
        self.check("ReactJS", "REACT")

    def test_node(self):
        self.check("NodeJS", "NODE_JS")
        self.check("Node.js", "NODE_JS")
        self.check("node", "NODE_JS")

    def test_postgres(self):
        self.check("Postgres", "POSTGRESQL")
        self.check("PostgreSQL", "POSTGRESQL")

    def test_scikit_learn(self):
        self.check("sklearn", "SCIKIT_LEARN")
        self.check("scikit learn", "SCIKIT_LEARN")
        self.check("Scikit-learn", "SCIKIT_LEARN")

    def test_tensorflow_and_pytorch(self):
        self.check("Tensor Flow", "TENSORFLOW")
        self.check("TensorFlow", "TENSORFLOW")
        self.check("Py Torch", "PYTORCH")
        self.check("PyTorch", "PYTORCH")

    def test_rest(self):
        self.check("REST APIs", "REST_API")
        self.check("REST", "REST_API")

    def test_prefix_of_another_spelling(self):
        self.check("java", "JAVA")
        self.check("javascript", "JAVASCRIPT")
        self.check("node", "NODE_JS")
        self.check("nodejs", "NODE_JS")

    def test_unknown_skill(self):
        self.check("Cobol", None)
        self.check("nod", None)
        self.check("", None)

class TestVocabulary(unittest.TestCase):
    def test_every_spelling_gives_its_token(self):
        transducers = build_all()
        for category in CATEGORIES:
            for pair in CATEGORIES[category]:
                self.assertEqual(normalize_skill(pair[0], transducers), pair[1])

    def test_no_spelling_is_used_twice(self):
        seen = []
        for category in CATEGORIES:
            for pair in CATEGORIES[category]:
                self.assertNotIn(pair[0], seen)
                seen.append(pair[0])

class TestNormalize(unittest.TestCase):
    def test_assignment_example(self):
        result = normalize(["JS", "React.js", "NodeJS", "Postgres", "Git"])
        self.assertEqual(result["tokens"], ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"])
        self.assertEqual(result["unknown"], [])

    def test_repeated_spellings_give_one_token(self):
        result = normalize(["sklearn", "scikit learn", "Scikit-learn"])
        self.assertEqual(result["tokens"], ["SCIKIT_LEARN"])

    def test_unknown_skills_are_reported(self):
        result = normalize(["Python", "Cobol"])
        self.assertEqual(result["tokens"], ["PYTHON"])
        self.assertEqual(result["unknown"], ["Cobol"])

class TestWithExtraction(unittest.TestCase):
    def test_all_examples_are_normalized(self):
        for name in ["fullstack_01", "fullstack_02", "mlengineer_01", "mlengineer_02"]:
            skills = extract_file(os.path.join(EXAMPLES, name + ".txt"), save=False)["skills"]
            result = normalize(skills)
            self.assertEqual(result["unknown"], [])
            self.assertGreater(len(result["tokens"]), 0)

if __name__ == "__main__":
    unittest.main()
