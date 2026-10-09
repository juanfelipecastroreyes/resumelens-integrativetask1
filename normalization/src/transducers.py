import os

from pyformlang.fst import FST

END = "#"

CATEGORIES = {
    "languages": {
        "PYTHON": ["python", "python3"],
        "JAVA": ["java"],
        "JAVASCRIPT": ["javascript", "js"],
        "TYPESCRIPT": ["typescript", "ts"],
        "SQL": ["sql"],
        "R_LANG": ["r"],
    },
    "frontend": {
        "HTML": ["html", "html5"],
        "CSS": ["css", "css3"],
        "REACT": ["react", "reactjs"],
        "ANGULAR": ["angular", "angularjs"],
        "VUE": ["vue", "vuejs"],
    },
    "backend": {
        "NODE_JS": ["node", "nodejs"],
        "EXPRESS": ["express", "expressjs"],
        "SPRING_BOOT": ["spring", "springboot"],
        "DJANGO": ["django"],
        "FLASK": ["flask"],
        "REST_API": ["rest", "restful", "restapi", "restapis"],
    },
    "databases": {
        "POSTGRESQL": ["postgres", "postgresql"],
        "MYSQL": ["mysql"],
        "MONGODB": ["mongo", "mongodb"],
    },
    "devops": {
        "DOCKER": ["docker"],
        "GIT": ["git"],
        "AWS": ["aws", "amazonwebservices"],
        "CI_CD": ["cicd"],
    },
    "data_ml": {
        "PANDAS": ["pandas"],
        "NUMPY": ["numpy"],
        "SCIKIT_LEARN": ["scikitlearn", "sklearn"],
        "TENSORFLOW": ["tensorflow", "tf"],
        "PYTORCH": ["pytorch", "torch"],
        "KERAS": ["keras"],
        "MACHINE_LEARNING": ["machinelearning", "ml"],
        "DEEP_LEARNING": ["deeplearning"],
        "NLP": ["nlp", "naturallanguageprocessing"],
        "COMPUTER_VISION": ["computervision", "cv"],
        "MLOPS": ["mlops"],
    },
}

def simplify(text):
    result = ""
    for char in text.lower():
        if char.isalnum():
            result = result + char
    return result

def state_order(state):
    if state == "qf":
        return 1000000
    return int(state[1:])

def build_transducer(spellings_by_token):
    fst = FST()
    fst.add_start_state("q0")
    fst.add_final_state("qf")
    names = {"": "q0"}
    count = 0
    for token in spellings_by_token:
        for spelling in spellings_by_token[token]:
            prefix = ""
            for char in spelling:
                new_prefix = prefix + char
                if new_prefix not in names:
                    count = count + 1
                    names[new_prefix] = "q" + str(count)
                    fst.add_transition(names[prefix], char, names[new_prefix], [])
                prefix = new_prefix
            fst.add_transition(names[prefix], END, "qf", [token])
    return fst

def build_all():
    transducers = {}
    for category in CATEGORIES:
        transducers[category] = build_transducer(CATEGORIES[category])
    return transducers

def normalize_skill(skill, transducers):
    symbols = list(simplify(skill))
    symbols.append(END)
    for category in transducers:
        for output in transducers[category].translate(symbols):
            return output[0]
    return None

def normalize(skills, transducers=None):
    if transducers is None:
        transducers = build_all()
    tokens = []
    unknown = []
    for skill in skills:
        token = normalize_skill(skill, transducers)
        if token is None:
            unknown.append(skill)
        elif token not in tokens:
            tokens.append(token)
    return {"tokens": tokens, "unknown": unknown}

def describe(name, fst):
    states = sorted(fst.states, key=state_order)
    inputs = sorted(fst.input_symbols)
    outputs = sorted(fst.output_symbols)
    lines = ["Transducer: " + name]
    lines.append("Q = {" + ", ".join(states) + "}")
    lines.append("Sigma = {" + ", ".join(inputs) + "}")
    lines.append("Gamma = {" + ", ".join(outputs) + "}")
    lines.append("q0 = " + ", ".join(sorted(fst.start_states)))
    lines.append("F = {" + ", ".join(sorted(fst.final_states)) + "}")
    lines.append("delta and omega (state, input -> next state, output):")
    for key in sorted(fst.transitions, key=lambda k: (state_order(k[0]), k[1])):
        for next_state, output in fst.transitions[key]:
            text = "ε"
            if len(output) > 0:
                text = " ".join(output)
            lines.append("  (" + key[0] + ", " + key[1] + ") -> (" + next_state + ", " + text + ")")
    return "\n".join(lines)

def save_dot_files(folder, transducers=None):
    if transducers is None:
        transducers = build_all()
    os.makedirs(folder, exist_ok=True)
    for category in transducers:
        transducers[category].write_as_dot(os.path.join(folder, category + ".dot"))

if __name__ == "__main__":
    all_transducers = build_all()
    for category in all_transducers:
        print(describe(category, all_transducers[category]))
        print()
