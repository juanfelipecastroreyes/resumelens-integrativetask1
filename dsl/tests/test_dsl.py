import sys
import unittest
from pathlib import Path

DSL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DSL / "src"))

from validator import validate
from markdown_generator import generate_markdown


class TestValidFiles(unittest.TestCase):

    def test_examples_are_valid(self):
        for path in sorted((DSL / "examples").glob("*.resume")):
            ok, result = validate(str(path))
            self.assertTrue(ok, path.name)

    def test_valid_tests_are_valid(self):
        for path in sorted((DSL / "tests" / "valid").glob("*.resume")):
            ok, result = validate(str(path))
            self.assertTrue(ok, path.name)


class TestInvalidFiles(unittest.TestCase):

    def test_invalid_tests_are_rejected(self):
        for path in sorted((DSL / "tests" / "invalid").glob("*.resume")):
            ok, result = validate(str(path))
            self.assertFalse(ok, path.name)


class TestClassifications(unittest.TestCase):

    def test_single_classification(self):
        ok, model = validate(str(DSL / "examples" / "resume_01.resume"))
        self.assertEqual(len(model.classifications), 1)
        self.assertEqual(model.classifications[0].label, "Backend Developer")

    def test_multiple_classifications(self):
        ok, model = validate(str(DSL / "tests" / "valid" / "valid_03_multiple_classifications.resume"))
        labels = []
        for c in model.classifications:
            labels.append(c.label)
        self.assertEqual(labels, ["Machine Learning Engineer", "Cloud Engineer"])

    def test_markdown_lists_every_classification(self):
        ok, model = validate(str(DSL / "tests" / "valid" / "valid_03_multiple_classifications.resume"))
        markdown = generate_markdown(model)
        self.assertIn("- Machine Learning Engineer", markdown)
        self.assertIn("- Cloud Engineer", markdown)

    def test_no_classification_is_invalid(self):
        ok, result = validate(str(DSL / "tests" / "invalid" / "invalid_01_missing_mandatory.resume"))
        self.assertFalse(ok)

    def test_optional_phone_is_none(self):
        ok, model = validate(str(DSL / "tests" / "valid" / "valid_01_no_optional_phone.resume"))
        self.assertFalse(model.contact.phone)


if __name__ == "__main__":
    unittest.main()
