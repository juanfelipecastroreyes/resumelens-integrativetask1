import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from resume_builder import build_from_text, build_resume, level_for, quote
from validator import validate

EXAMPLES = os.path.join(HERE, "..", "..", "extraction", "examples")


def read_example(name):
    with open(os.path.join(EXAMPLES, name), encoding="utf-8") as f:
        return f.read()


def check_valid(test, content):
    folder = tempfile.mkdtemp()
    path = os.path.join(folder, "built.resume")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    ok, result = validate(path)
    test.assertTrue(ok, content)
    return result


class TestHelpers(unittest.TestCase):

    def test_quote_wraps_text(self):
        self.assertEqual(quote("Python"), '"Python"')

    def test_quote_replaces_inner_quotes(self):
        self.assertEqual(quote('say "hi"'), '"say \'hi\'"')

    def test_level_for_years(self):
        self.assertEqual(level_for(0), "Beginner")
        self.assertEqual(level_for(1), "Beginner")
        self.assertEqual(level_for(2), "Intermediate")
        self.assertEqual(level_for(4), "Intermediate")
        self.assertEqual(level_for(5), "Expert")


class TestBuildFromExamples(unittest.TestCase):

    def test_every_example_builds_a_valid_resume(self):
        names = ["fullstack_01.txt", "fullstack_02.txt", "mlengineer_01.txt", "mlengineer_02.txt"]
        for name in names:
            content = build_from_text(read_example(name), ["Full Stack Developer"])
            check_valid(self, content)

    def test_name_and_location_come_from_first_lines(self):
        model = check_valid(self, build_from_text(read_example("fullstack_01.txt"), ["Full Stack Developer"]))
        self.assertEqual(model.personal_info.name, "Wednesday Addams")
        self.assertEqual(model.personal_info.location, "Bogota, Colombia")

    def test_contact_data_is_copied(self):
        model = check_valid(self, build_from_text(read_example("fullstack_01.txt"), ["Full Stack Developer"]))
        self.assertEqual(model.contact.email, "wednesday.addams@correo.com")
        self.assertEqual(model.contact.github, "wednesdayaddams")
        self.assertEqual(model.contact.phone, "+57 312 400 5566")

    def test_skills_keep_the_original_spelling(self):
        model = check_valid(self, build_from_text(read_example("fullstack_01.txt"), ["Full Stack Developer"]))
        names = []
        for skill in model.skills:
            names.append(skill.name)
        self.assertIn("NodeJS", names)

    def test_qualifications_are_normalized_tokens(self):
        model = check_valid(self, build_from_text(read_example("fullstack_01.txt"), ["Full Stack Developer"]))
        names = []
        for q in model.qualifications:
            names.append(q.name)
        self.assertIn("NODE_JS", names)
        self.assertIn("POSTGRESQL", names)

    def test_level_depends_on_years(self):
        model = check_valid(self, build_from_text(read_example("fullstack_01.txt"), ["Full Stack Developer"]))
        self.assertEqual(model.qualifications[0].level, "Intermediate")

    def test_several_labels(self):
        labels = ["Machine Learning Engineer", "Data Scientist"]
        model = check_valid(self, build_from_text(read_example("mlengineer_01.txt"), labels))
        self.assertEqual(len(model.classifications), 2)


class TestBuildResume(unittest.TestCase):

    def empty_extraction(self):
        return {
            "contact": {"emails": [], "phones": [], "github": [], "linkedin": []},
            "experience": {"years": [], "positions": []},
            "education": {"degrees": [], "institutions": []},
            "skills": [],
        }

    def test_empty_extraction_is_still_valid(self):
        content = build_resume("Ana Perez", "Cali, Colombia", self.empty_extraction(), [], [])
        model = check_valid(self, content)
        self.assertEqual(model.classifications[0].label, "Unclassified")
        self.assertEqual(len(model.experiences), 0)
        self.assertEqual(len(model.education), 0)

    def test_phone_is_optional(self):
        content = build_resume("Ana Perez", "Cali, Colombia", self.empty_extraction(), [], ["Data Analyst"])
        model = check_valid(self, content)
        self.assertFalse(model.contact.phone)

    def test_position_without_years_uses_zero(self):
        data = self.empty_extraction()
        data["experience"]["positions"] = ["Data Analyst"]
        content = build_resume("Ana Perez", "Cali, Colombia", data, [], ["Data Analyst"])
        model = check_valid(self, content)
        self.assertEqual(model.experiences[0].years, 0)


if __name__ == "__main__":
    unittest.main()
