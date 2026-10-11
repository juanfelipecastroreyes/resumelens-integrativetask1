import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from extractor import extract, extract_file
from skills import extract_skills

EXAMPLES = os.path.join(HERE, "..", "examples")

def load(name):
    return extract_file(os.path.join(EXAMPLES, name + ".txt"), save=False)

class TestContact(unittest.TestCase):
    def test_email(self):
        result = extract("Write to wednesday.addams@correo.com.")
        self.assertEqual(result["contact"]["emails"], ["wednesday.addams@correo.com"])

    def test_phone_formats(self):
        text = "+57 312 400 5566, (601) 555 0199, 312-400-5566, 3124005566"
        self.assertEqual(len(extract(text)["contact"]["phones"]), 4)

    def test_year_range_is_not_a_phone(self):
        self.assertEqual(extract("Worked 2019 - 2022 in 2020")["contact"]["phones"], [])

    def test_github_and_linkedin(self):
        text = "https://github.com/pugsleyaddams linkedin.com/in/gwen-stacy"
        result = extract(text)["contact"]
        self.assertEqual(result["github"], ["pugsleyaddams"])
        self.assertEqual(result["linkedin"], ["gwen-stacy"])

class TestExperience(unittest.TestCase):
    def test_years_english(self):
        self.assertEqual(extract("3 years of experience")["experience"]["years"], [3])

    def test_years_with_plus(self):
        self.assertEqual(extract("10+ years of experience")["experience"]["years"], [10])

    def test_years_spanish(self):
        self.assertEqual(extract("5 años de experiencia")["experience"]["years"], [5])

    def test_position_with_level(self):
        positions = extract("Senior Backend Developer")["experience"]["positions"]
        self.assertEqual(positions, ["Senior Backend Developer"])

    def test_degree_is_not_a_position(self):
        self.assertEqual(extract("Systems Engineering")["experience"]["positions"], [])

class TestEducation(unittest.TestCase):
    def test_degree_and_institution(self):
        result = extract("B.Sc. in Systems Engineering - Universidad ICESI")["education"]
        self.assertEqual(result["degrees"], ["B.Sc. in Systems Engineering"])
        self.assertEqual(result["institutions"], ["Universidad ICESI"])

    def test_institution_with_de(self):
        result = extract("Universidad Nacional de Colombia")["education"]
        self.assertEqual(result["institutions"], ["Universidad Nacional de Colombia"])

class TestSkills(unittest.TestCase):
    def test_node_variants(self):
        self.assertEqual(extract_skills("Node.js and Vue.js"), ["Vue.js", "Node.js"])

    def test_js_is_not_found_inside_node_js(self):
        self.assertEqual(extract_skills("NodeJS, Node JS"), ["NodeJS", "Node JS"])

    def test_java_is_not_javascript(self):
        self.assertEqual(extract_skills("Java and JavaScript"), ["Java", "JavaScript"])

    def test_sql_is_not_inside_mysql(self):
        self.assertEqual(sorted(extract_skills("MySQL and SQL")), ["MySQL", "SQL"])

    def test_short_names_need_capitals(self):
        self.assertEqual(extract_skills("ts tf cv"), [])
        self.assertEqual(sorted(extract_skills("TS, TF, CV")), ["CV", "TF", "TS"])

    def test_r_inside_r_and_d(self):
        self.assertEqual(extract_skills("R&D team"), [])
        self.assertEqual(extract_skills("I know R, Python"), ["Python", "R"])

    def test_job_title_is_not_a_skill(self):
        self.assertEqual(extract_skills("Machine Learning Engineer"), [])

    def test_links_and_emails_are_ignored(self):
        self.assertEqual(extract_skills("github.com/mygit and me@git.com"), [])

    def test_rest_api_is_one_skill(self):
        self.assertEqual(extract_skills("REST APIs"), ["REST APIs"])

    def test_cloud_skills(self):
        text = "Skills: Linux, Azure, GCP, Google Cloud, k8s, Terraform."
        self.assertEqual(extract_skills(text), ["Linux", "Azure", "GCP", "Google Cloud", "k8s", "Terraform"])

class TestExamples(unittest.TestCase):
    def test_fullstack_01(self):
        result = load("fullstack_01")
        self.assertEqual(result["contact"]["phones"], ["+57 312 400 5566"])
        self.assertEqual(result["experience"]["years"], [3])
        self.assertEqual(result["skills"], ["JS", "React.js", "NodeJS", "Postgres", "Git"])

    def test_fullstack_02(self):
        result = load("fullstack_02")
        self.assertEqual(result["experience"]["positions"], ["Senior Backend Developer"])
        self.assertEqual(result["education"]["institutions"], ["Universidad del Valle"])
        self.assertIn("Spring Boot", result["skills"])
        self.assertNotIn("Git", result["skills"])

    def test_mlengineer_01(self):
        result = load("mlengineer_01")
        self.assertEqual(result["contact"]["github"], ["mjwatson"])
        self.assertEqual(
            result["skills"],
            ["Python", "SQL", "Git", "Pandas", "NumPy", "Scikit-learn", "TensorFlow"],
        )

    def test_mlengineer_02(self):
        result = load("mlengineer_02")
        self.assertEqual(result["contact"]["phones"], ["(601) 555 0199"])
        self.assertEqual(result["education"]["degrees"], ["M.Sc. in Data Science"])
        self.assertIn("Tensor Flow", result["skills"])
        self.assertIn("Py Torch", result["skills"])

if __name__ == "__main__":
    unittest.main()
