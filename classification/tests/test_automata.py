import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "normalization", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "extraction", "src"))

from automata import PROFILES, TOKENS, accepted_labels, accepts, build_all, build_automaton, classify
from extractor import extract, extract_file
from sorter import PROFILE_ORDER, sort_tokens
from transducers import normalize

EXAMPLES = os.path.join(HERE, "..", "..", "extraction", "examples")

def first_tokens(profile, route_number):
    tokens = []
    for group in PROFILES[profile]["routes"][route_number]:
        tokens.append(group[0])
    return tokens

def has_epsilon(automaton):
    for state in automaton.to_dict():
        for symbol in automaton.to_dict()[state]:
            if str(symbol) == "epsilon":
                return True
    return False

class TestAssignmentExamples(unittest.TestCase):
    def test_machine_learning_example(self):
        tokens = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]
        self.assertEqual(classify(tokens)["ml_engineer"], "ACCEPTED")

    def test_full_stack_example(self):
        tokens = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        self.assertEqual(classify(tokens)["full_stack"], "ACCEPTED")

    def test_full_stack_example_is_not_the_other_profiles(self):
        result = classify(["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"])
        self.assertEqual(result["ml_engineer"], "REJECTED")
        self.assertEqual(result["data_scientist"], "REJECTED")
        self.assertEqual(result["cloud_engineer"], "REJECTED")

class TestAutomatonTypes(unittest.TestCase):
    def setUp(self):
        self.automata = build_all()

    def test_full_stack_is_a_dfa(self):
        self.assertTrue(self.automata["full_stack"].is_deterministic())

    def test_ml_engineer_is_a_dfa(self):
        self.assertTrue(self.automata["ml_engineer"].is_deterministic())

    def test_data_scientist_is_an_nfa(self):
        automaton = self.automata["data_scientist"]
        self.assertFalse(automaton.is_deterministic())
        self.assertFalse(has_epsilon(automaton))

    def test_cloud_engineer_is_an_epsilon_nfa(self):
        self.assertTrue(has_epsilon(self.automata["cloud_engineer"]))

    def test_number_of_states(self):
        self.assertEqual(len(self.automata["full_stack"].states), 6)
        self.assertEqual(len(self.automata["ml_engineer"].states), 6)
        self.assertEqual(len(self.automata["data_scientist"].states), 9)
        self.assertEqual(len(self.automata["cloud_engineer"].states), 13)

    def test_one_start_state(self):
        for profile in self.automata:
            self.assertEqual(len(self.automata[profile].start_states), 1)

    def test_declared_type_matches_the_automaton(self):
        for profile in PROFILES:
            kind = PROFILES[profile]["type"]
            automaton = self.automata[profile]
            if kind == "DFA":
                self.assertTrue(automaton.is_deterministic())
            else:
                self.assertFalse(automaton.is_deterministic())

class TestDefinitions(unittest.TestCase):
    def test_group_tokens_belong_to_the_alphabet(self):
        for profile in PROFILES:
            for route in PROFILES[profile]["routes"]:
                for group in route:
                    for token in group:
                        self.assertIn(token, TOKENS)

    def test_alphabet_has_no_repeated_token(self):
        self.assertEqual(len(TOKENS), len(set(TOKENS)))
        self.assertEqual(len(TOKENS), 40)

    def test_groups_follow_the_sorting_order(self):
        for profile in PROFILES:
            order = PROFILE_ORDER[profile]
            for route in PROFILES[profile]["routes"]:
                last = -1
                for group in route:
                    positions = []
                    for token in group:
                        self.assertIn(token, order)
                        positions.append(order.index(token))
                    self.assertGreater(min(positions), last)
                    last = max(positions)

    def test_every_profile_has_a_sorting_order(self):
        for profile in PROFILES:
            self.assertIn(profile, PROFILE_ORDER)

class TestEveryProfile(unittest.TestCase):
    def setUp(self):
        self.automata = build_all()

    def test_minimal_sequence_is_accepted(self):
        for profile in PROFILES:
            for number in range(len(PROFILES[profile]["routes"])):
                tokens = sort_tokens(first_tokens(profile, number), profile)
                self.assertTrue(accepts(self.automata[profile], tokens), profile)

    def test_every_token_of_every_group_is_accepted(self):
        for profile in PROFILES:
            for route in PROFILES[profile]["routes"]:
                for position in range(len(route)):
                    for token in route[position]:
                        tokens = []
                        for group in route:
                            tokens.append(group[0])
                        tokens[position] = token
                        tokens = sort_tokens(tokens, profile)
                        self.assertTrue(accepts(self.automata[profile], tokens), profile + " " + token)

    def test_missing_group_is_rejected(self):
        for profile in PROFILES:
            if len(PROFILES[profile]["routes"]) > 1:
                continue
            route = PROFILES[profile]["routes"][0]
            for missing in range(len(route)):
                tokens = []
                for position in range(len(route)):
                    if position != missing:
                        tokens.append(route[position][0])
                tokens = sort_tokens(tokens, profile)
                self.assertFalse(accepts(self.automata[profile], tokens), profile + " " + str(missing))

    def test_empty_sequence_is_rejected(self):
        for profile in PROFILES:
            self.assertFalse(accepts(self.automata[profile], []))

    def test_extra_tokens_do_not_change_the_result(self):
        for profile in PROFILES:
            tokens = sort_tokens(first_tokens(profile, 0) + ["HTML", "LINUX", "MLOPS", "JAVA"], profile)
            self.assertTrue(accepts(self.automata[profile], tokens), profile)

    def test_repeated_use_gives_the_same_result(self):
        for profile in PROFILES:
            first = build_automaton(profile)
            second = build_automaton(profile)
            tokens = sort_tokens(first_tokens(profile, 0), profile)
            self.assertEqual(accepts(first, tokens), accepts(second, tokens))

class TestAgainstSimpleRule(unittest.TestCase):
    def test_random_candidates(self):
        random.seed(7)
        automata = build_all()
        for profile in PROFILES:
            for turn in range(400):
                tokens = []
                for token in TOKENS:
                    if random.random() < 0.35:
                        tokens.append(token)
                expected = False
                for route in PROFILES[profile]["routes"]:
                    complete = True
                    for group in route:
                        found = False
                        for token in group:
                            if token in tokens:
                                found = True
                        if not found:
                            complete = False
                    if complete:
                        expected = True
                ordered = sort_tokens(tokens, profile)
                self.assertEqual(accepts(automata[profile], ordered), expected, profile + " " + str(ordered))

class TestOrder(unittest.TestCase):
    def test_unsorted_input_is_rejected_by_the_automaton(self):
        automaton = build_automaton("full_stack")
        tokens = ["GIT", "POSTGRESQL", "NODE_JS", "REACT", "JAVASCRIPT"]
        self.assertFalse(accepts(automaton, tokens))

    def test_classify_does_not_depend_on_input_order(self):
        tokens = ["GIT", "POSTGRESQL", "NODE_JS", "REACT", "JAVASCRIPT"]
        reverse = list(reversed(tokens))
        self.assertEqual(classify(tokens), classify(reverse))
        self.assertEqual(classify(tokens)["full_stack"], "ACCEPTED")

class TestDataScientist(unittest.TestCase):
    def test_classic_route(self):
        tokens = ["PYTHON", "SQL", "PANDAS", "SCIKIT_LEARN"]
        self.assertEqual(classify(tokens)["data_scientist"], "ACCEPTED")

    def test_deep_learning_route(self):
        tokens = ["R_LANG", "MYSQL", "NUMPY", "NLP"]
        self.assertEqual(classify(tokens)["data_scientist"], "ACCEPTED")

    def test_needs_a_modeling_skill(self):
        tokens = ["PYTHON", "SQL", "PANDAS"]
        self.assertEqual(classify(tokens)["data_scientist"], "REJECTED")

    def test_does_not_need_a_deep_learning_framework(self):
        tokens = ["PYTHON", "SQL", "NUMPY", "MACHINE_LEARNING"]
        result = classify(tokens)
        self.assertEqual(result["data_scientist"], "ACCEPTED")
        self.assertEqual(result["ml_engineer"], "REJECTED")

class TestCloudEngineer(unittest.TestCase):
    def test_each_provider_is_accepted(self):
        for provider in ["AWS", "AZURE", "GCP"]:
            tokens = [provider, "DOCKER", "TERRAFORM"]
            self.assertEqual(classify(tokens)["cloud_engineer"], "ACCEPTED", provider)

    def test_needs_a_provider(self):
        tokens = ["LINUX", "DOCKER", "TERRAFORM", "GIT"]
        self.assertEqual(classify(tokens)["cloud_engineer"], "REJECTED")

    def test_kubernetes_and_ci_cd(self):
        tokens = ["GIT", "CI_CD", "KUBERNETES", "AZURE"]
        self.assertEqual(classify(tokens)["cloud_engineer"], "ACCEPTED")

class TestSeveralProfiles(unittest.TestCase):
    def test_one_candidate_can_fit_two_profiles(self):
        tokens = ["PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT"]
        self.assertEqual(accepted_labels(tokens), ["Machine Learning Engineer", "Data Scientist"])

    def test_no_profile(self):
        self.assertEqual(accepted_labels(["HTML"]), [])

    def test_labels(self):
        self.assertEqual(PROFILES["full_stack"]["label"], "Full Stack Developer")
        self.assertEqual(PROFILES["cloud_engineer"]["label"], "Cloud Engineer")

class TestWithPreviousStages(unittest.TestCase):
    def tokens_of(self, name):
        skills = extract_file(os.path.join(EXAMPLES, name + ".txt"), save=False)["skills"]
        return normalize(skills)["tokens"]

    def test_fullstack_example(self):
        self.assertEqual(classify(self.tokens_of("fullstack_01"))["full_stack"], "ACCEPTED")

    def test_fullstack_example_without_git(self):
        self.assertEqual(classify(self.tokens_of("fullstack_02"))["full_stack"], "REJECTED")

    def test_machine_learning_examples(self):
        for name in ["mlengineer_01", "mlengineer_02"]:
            result = classify(self.tokens_of(name))
            self.assertEqual(result["ml_engineer"], "ACCEPTED", name)
            self.assertEqual(result["full_stack"], "REJECTED", name)

    def test_cloud_skills_from_text(self):
        text = "Skills: Linux, Google Cloud, k8s, Terraform, Git"
        skills = extract(text)["skills"]
        self.assertEqual(classify(normalize(skills)["tokens"])["cloud_engineer"], "ACCEPTED")

if __name__ == "__main__":
    unittest.main()
