import os
import sys

from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import Epsilon, State, Symbol

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "normalization", "src"))

from sorter import sort_tokens
from transducers import CATEGORIES

TOKENS = []
for category in CATEGORIES:
    for pair in CATEGORIES[category]:
        if pair[1] not in TOKENS:
            TOKENS.append(pair[1])

LANGUAGE = ["PYTHON", "R_LANG"]
DATABASE = ["SQL", "POSTGRESQL", "MYSQL"]
DATA_LIBRARY = ["PANDAS", "NUMPY"]
CONTAINER = ["DOCKER", "KUBERNETES"]
AUTOMATION = ["TERRAFORM", "CI_CD"]

PROFILES = {
    "full_stack": {
        "label": "Full Stack Developer",
        "type": "DFA",
        "routes": [
            [
                ["JAVASCRIPT", "TYPESCRIPT"],
                ["REACT", "ANGULAR", "VUE"],
                ["NODE_JS", "EXPRESS", "SPRING_BOOT", "DJANGO", "FLASK"],
                ["SQL", "POSTGRESQL", "MYSQL", "MONGODB"],
                ["GIT"],
            ],
        ],
    },
    "ml_engineer": {
        "label": "Machine Learning Engineer",
        "type": "DFA",
        "routes": [
            [
                ["PYTHON"],
                DATABASE,
                DATA_LIBRARY,
                ["TENSORFLOW", "PYTORCH", "KERAS"],
                ["GIT"],
            ],
        ],
    },
    "data_scientist": {
        "label": "Data Scientist",
        "type": "NFA",
        "routes": [
            [
                LANGUAGE,
                DATABASE,
                DATA_LIBRARY,
                ["SCIKIT_LEARN", "MACHINE_LEARNING"],
            ],
            [
                LANGUAGE,
                DATABASE,
                DATA_LIBRARY,
                ["DEEP_LEARNING", "NLP", "COMPUTER_VISION"],
            ],
        ],
    },
    "cloud_engineer": {
        "label": "Cloud Engineer",
        "type": "EPSILON_NFA",
        "routes": [
            [["AWS"], CONTAINER, AUTOMATION],
            [["AZURE"], CONTAINER, AUTOMATION],
            [["GCP"], CONTAINER, AUTOMATION],
        ],
    },
}

PREFIXES = ["q", "p", "r"]

def later_tokens(route, position):
    tokens = []
    for group in route[position:]:
        for token in group:
            tokens.append(token)
    return tokens

def add_route(automaton, route, prefix, start_name):
    count = len(route)
    for position in range(count + 1):
        if position == 0:
            name = start_name
        else:
            name = prefix + str(position)
        if position < count:
            next_name = prefix + str(position + 1)
            for token in route[position]:
                automaton.add_transition(State(name), Symbol(token), State(next_name))
        pending = later_tokens(route, position)
        for token in TOKENS:
            if token not in pending:
                automaton.add_transition(State(name), Symbol(token), State(name))
    automaton.add_final_state(State(prefix + str(count)))

def build_automaton(profile):
    kind = PROFILES[profile]["type"]
    routes = PROFILES[profile]["routes"]
    if kind == "DFA":
        automaton = DeterministicFiniteAutomaton()
    elif kind == "NFA":
        automaton = NondeterministicFiniteAutomaton()
    else:
        automaton = EpsilonNFA()
    if kind == "EPSILON_NFA":
        automaton.add_start_state(State("s"))
    else:
        automaton.add_start_state(State("q0"))
    number = 0
    for route in routes:
        prefix = PREFIXES[number]
        number = number + 1
        if kind == "EPSILON_NFA":
            start_name = prefix + "0"
            automaton.add_transition(State("s"), Epsilon(), State(start_name))
        elif kind == "NFA":
            start_name = "q0"
        else:
            start_name = prefix + "0"
        add_route(automaton, route, prefix, start_name)
    return automaton

def build_all():
    automata = {}
    for profile in PROFILES:
        automata[profile] = build_automaton(profile)
    return automata

def accepts(automaton, tokens):
    symbols = []
    for token in tokens:
        symbols.append(Symbol(token))
    return automaton.accepts(symbols)

def classify(tokens):
    automata = build_all()
    result = {}
    for profile in PROFILES:
        ordered = sort_tokens(tokens, profile)
        if accepts(automata[profile], ordered):
            result[profile] = "ACCEPTED"
        else:
            result[profile] = "REJECTED"
    return result

def accepted_labels(tokens):
    result = classify(tokens)
    labels = []
    for profile in PROFILES:
        if result[profile] == "ACCEPTED":
            labels.append(PROFILES[profile]["label"])
    return labels
