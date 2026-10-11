from pyformlang.fst import FST

CATEGORIES = {
    "languages": [
        ["python", "PYTHON"],
        ["python3", "PYTHON"],
        ["java", "JAVA"],
        ["javascript", "JAVASCRIPT"],
        ["js", "JAVASCRIPT"],
        ["typescript", "TYPESCRIPT"],
        ["ts", "TYPESCRIPT"],
        ["sql", "SQL"],
        ["r", "R_LANG"],
    ],
    "frontend": [
        ["html", "HTML"],
        ["html5", "HTML"],
        ["css", "CSS"],
        ["css3", "CSS"],
        ["react", "REACT"],
        ["reactjs", "REACT"],
        ["angular", "ANGULAR"],
        ["angularjs", "ANGULAR"],
        ["vue", "VUE"],
        ["vuejs", "VUE"],
    ],
    "backend": [
        ["node", "NODE_JS"],
        ["nodejs", "NODE_JS"],
        ["express", "EXPRESS"],
        ["expressjs", "EXPRESS"],
        ["spring", "SPRING_BOOT"],
        ["springboot", "SPRING_BOOT"],
        ["django", "DJANGO"],
        ["flask", "FLASK"],
        ["rest", "REST_API"],
        ["restful", "REST_API"],
        ["restapi", "REST_API"],
        ["restapis", "REST_API"],
    ],
    "databases": [
        ["postgres", "POSTGRESQL"],
        ["postgresql", "POSTGRESQL"],
        ["mysql", "MYSQL"],
        ["mongo", "MONGODB"],
        ["mongodb", "MONGODB"],
    ],
    "devops": [
        ["docker", "DOCKER"],
        ["git", "GIT"],
        ["aws", "AWS"],
        ["amazonwebservices", "AWS"],
        ["cicd", "CI_CD"],
    ],
    "data_ml": [
        ["pandas", "PANDAS"],
        ["numpy", "NUMPY"],
        ["scikitlearn", "SCIKIT_LEARN"],
        ["sklearn", "SCIKIT_LEARN"],
        ["tensorflow", "TENSORFLOW"],
        ["tf", "TENSORFLOW"],
        ["pytorch", "PYTORCH"],
        ["torch", "PYTORCH"],
        ["keras", "KERAS"],
        ["machinelearning", "MACHINE_LEARNING"],
        ["ml", "MACHINE_LEARNING"],
        ["deeplearning", "DEEP_LEARNING"],
        ["nlp", "NLP"],
        ["naturallanguageprocessing", "NLP"],
        ["computervision", "COMPUTER_VISION"],
        ["cv", "COMPUTER_VISION"],
        ["mlops", "MLOPS"],
    ],
    "cloud": [
        ["linux", "LINUX"],
        ["azure", "AZURE"],
        ["gcp", "GCP"],
        ["googlecloud", "GCP"],
        ["googlecloudplatform", "GCP"],
        ["kubernetes", "KUBERNETES"],
        ["k8s", "KUBERNETES"],
        ["terraform", "TERRAFORM"],
    ],
}

def simplify(text):
    result = ""
    for char in text.lower():
        if char.isalnum():
            result = result + char
    return result

def build_transducer(pairs):
    fst = FST()
    fst.add_start_state("q0")
    count = 0
    for pair in pairs:
        spelling = pair[0]
        token = pair[1]
        state = "q0"
        output = [token]
        for letter in spelling:
            count = count + 1
            next_state = "q" + str(count)
            fst.add_transition(state, letter, next_state, output)
            output = []
            state = next_state
        fst.add_final_state(state)
    return fst

def build_all():
    transducers = {}
    for category in CATEGORIES:
        transducers[category] = build_transducer(CATEGORIES[category])
    return transducers

def normalize_skill(skill, transducers):
    letters = list(simplify(skill))
    for category in transducers:
        outputs = list(transducers[category].translate(letters))
        if len(outputs) > 0:
            return outputs[0][0]
    return None

def normalize(skills):
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
