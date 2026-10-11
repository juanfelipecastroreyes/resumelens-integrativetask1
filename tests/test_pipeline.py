import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)

import pipeline
import resume_builder

EXAMPLES = os.path.join(ROOT, "extraction", "examples")

FULL_STACK = "Full Stack Developer"
ML_ENGINEER = "Machine Learning Engineer"
DATA_SCIENTIST = "Data Scientist"
CLOUD = "Cloud Engineer"


def read_example(name):
    with open(os.path.join(EXAMPLES, name), encoding="utf-8") as f:
        return f.read()


class PipelineTest(unittest.TestCase):

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.old_resume_dir = resume_builder.OUTPUT_DIR
        self.old_markdown_dir = pipeline.OUTPUT_DIR
        resume_builder.OUTPUT_DIR = os.path.join(self.folder.name, "generated")
        pipeline.OUTPUT_DIR = os.path.join(self.folder.name, "output")

    def tearDown(self):
        resume_builder.OUTPUT_DIR = self.old_resume_dir
        pipeline.OUTPUT_DIR = self.old_markdown_dir
        self.folder.cleanup()

    def run_text(self, text):
        return pipeline.run(text, "case")

    def test_fullstack_01(self):
        outcome = self.run_text(read_example("fullstack_01.txt"))
        self.assertEqual(outcome["labels"], [FULL_STACK])

    def test_fullstack_02_has_no_git(self):
        outcome = self.run_text(read_example("fullstack_02.txt"))
        self.assertEqual(outcome["labels"], [])

    def test_mlengineer_01(self):
        outcome = self.run_text(read_example("mlengineer_01.txt"))
        self.assertEqual(outcome["labels"], [ML_ENGINEER, DATA_SCIENTIST])

    def test_mlengineer_02(self):
        outcome = self.run_text(read_example("mlengineer_02.txt"))
        self.assertEqual(outcome["labels"], [ML_ENGINEER, DATA_SCIENTIST])

    def test_cloud_engineer(self):
        text = "Ana Perez\nCali\n4 years of experience.\nTechnical Skills:\nAWS, Docker, Terraform, Git\n"
        outcome = self.run_text(text)
        self.assertEqual(outcome["labels"], [CLOUD])

    def test_results_cover_all_profiles(self):
        outcome = self.run_text(read_example("fullstack_01.txt"))
        self.assertEqual(len(outcome["results"]), 4)
        for value in outcome["results"].values():
            self.assertIn(value, ["ACCEPTED", "REJECTED"])

    def test_labels_match_accepted_profiles(self):
        outcome = self.run_text(read_example("mlengineer_01.txt"))
        accepted = 0
        for value in outcome["results"].values():
            if value == "ACCEPTED":
                accepted = accepted + 1
        self.assertEqual(accepted, len(outcome["labels"]))

    def test_files_are_written_and_valid(self):
        outcome = self.run_text(read_example("fullstack_01.txt"))
        self.assertTrue(outcome["valid"])
        self.assertTrue(os.path.exists(outcome["resume_path"]))
        self.assertTrue(os.path.exists(outcome["markdown_path"]))

    def test_resume_contains_every_label(self):
        outcome = self.run_text(read_example("mlengineer_01.txt"))
        with open(outcome["resume_path"], encoding="utf-8") as f:
            content = f.read()
        for label in outcome["labels"]:
            self.assertIn('classification "' + label + '"', content)

    def test_markdown_has_candidate_name(self):
        outcome = self.run_text(read_example("fullstack_01.txt"))
        with open(outcome["markdown_path"], encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Wednesday Addams", content)

    def test_no_accepted_profile_is_unclassified_but_valid(self):
        outcome = self.run_text(read_example("fullstack_02.txt"))
        self.assertTrue(outcome["valid"])
        with open(outcome["resume_path"], encoding="utf-8") as f:
            content = f.read()
        self.assertIn('classification "Unclassified"', content)

    def test_empty_text(self):
        outcome = self.run_text("")
        self.assertEqual(outcome["labels"], [])
        self.assertTrue(outcome["valid"])

    def test_header_only(self):
        outcome = self.run_text("Ana Perez\nCali")
        self.assertEqual(outcome["tokens"], [])
        self.assertTrue(outcome["valid"])

    def test_skills_outside_vocabulary_are_ignored(self):
        text = "Ana Perez\nCali\n3 years of experience.\nTechnical Skills:\nCobol, Fortran\n"
        outcome = self.run_text(text)
        self.assertEqual(outcome["tokens"], [])
        self.assertEqual(outcome["labels"], [])

    def test_extra_skills_do_not_block_a_profile(self):
        text = "Ana Perez\nCali\n3 years of experience.\nTechnical Skills:\nPython, Cobol, SQL, Pandas, TensorFlow, Git\n"
        outcome = self.run_text(text)
        self.assertIn(ML_ENGINEER, outcome["labels"])

    def test_skill_order_does_not_change_result(self):
        first = "Ana Perez\nCali\n3 years of experience.\nTechnical Skills:\nGit, TensorFlow, Pandas, SQL, Python\n"
        second = "Ana Perez\nCali\n3 years of experience.\nTechnical Skills:\nPython, SQL, Pandas, TensorFlow, Git\n"
        self.assertEqual(self.run_text(first)["labels"], self.run_text(second)["labels"])

    def test_quotes_in_name_keep_the_file_valid(self):
        text = 'Ana "Pepa" Perez\nCali\n3 years of experience.\nTechnical Skills:\nPython\n'
        outcome = self.run_text(text)
        self.assertTrue(outcome["valid"])

    def test_read_header(self):
        self.assertEqual(pipeline.read_header("Ana Perez\nCali\nrest"), ("Ana Perez", "Cali"))

    def test_read_header_missing_lines(self):
        name, location = pipeline.read_header("")
        self.assertEqual(name, "Not specified")
        self.assertEqual(location, "Not specified")


class AppTest(unittest.TestCase):

    def setUp(self):
        try:
            from streamlit.testing.v1 import AppTest as StreamlitTest
        except ImportError:
            self.skipTest("streamlit is not installed")
        self.app = StreamlitTest.from_file(os.path.join(ROOT, "app.py"), default_timeout=60)

    def test_app_starts_without_errors(self):
        self.app.run()
        self.assertEqual(len(self.app.exception), 0)

    def test_app_shows_four_profiles(self):
        self.app.run()
        shown = len(self.app.success) + len(self.app.error)
        self.assertGreaterEqual(shown, 4)

    def test_app_accepts_pasted_text(self):
        self.app.run()
        self.app.sidebar.radio[0].set_value("Paste text").run()
        text = "Ana Perez\nCali\n4 years of experience.\nTechnical Skills:\nAWS, Docker, Terraform, Git\n"
        self.app.sidebar.text_area[0].set_value(text).run()
        self.assertEqual(len(self.app.exception), 0)
        messages = []
        for item in self.app.success:
            messages.append(item.value)
        self.assertIn("Cloud Engineer (EPSILON_NFA): ACCEPTED", messages)

    def test_app_asks_for_input_when_empty(self):
        self.app.run()
        self.app.sidebar.radio[0].set_value("Paste text").run()
        self.assertEqual(len(self.app.info), 1)


if __name__ == "__main__":
    unittest.main()