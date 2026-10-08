import re

EMAIL = r"[\w.+-]+@[\w-]+\.[\w.-]+"
LINK = r"(?:https?://)?(?:www\.)?[\w-]+\.(?:com|org|net|io|co)/\S*"
JOB_TITLE = r"Machine Learning Engineer"

BEFORE = r"(?<![\w.])"
AFTER = r"(?!\w)"

INSENSITIVE = [
    r"python3?",
    r"java",
    r"javascript",
    r"(?<!node )js",
    r"typescript",
    r"sql",
    r"html5?",
    r"css3?",
    r"react(?:\.js|js)?",
    r"angular(?:js)?",
    r"vue(?:\.js|js)?",
    r"node(?:\.js|js| js)?",
    r"express\.js|expressjs",
    r"spring boot|spring",
    r"django",
    r"flask",
    r"restful|rest apis?",
    r"postgres(?:ql)?",
    r"mysql",
    r"mongo(?:db)?",
    r"docker",
    r"git",
    r"aws|amazon web services",
    r"ci ?/ ?cd|cicd",
    r"pandas",
    r"numpy",
    r"scikit[- ]?learn|sklearn",
    r"tensor ?flow",
    r"py ?torch|torch",
    r"keras",
    r"machine learning",
    r"deep learning",
    r"nlp|natural language processing",
    r"computer vision",
    r"mlops",
]

SENSITIVE = [
    r"R(?![&/])",
    r"TS",
    r"TF",
    r"ML",
    r"CV",
    r"Express(?!\.?js)",
    r"REST(?! API)",
]

def clean_text(text):
    for pattern in [EMAIL, LINK, JOB_TITLE]:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)
    return text

def extract_skills(text):
    text = clean_text(text)
    found = []
    seen = []
    for pattern in INSENSITIVE:
        for item in re.findall(BEFORE + "(" + pattern + ")" + AFTER, text, re.IGNORECASE):
            if item.lower() not in seen:
                seen.append(item.lower())
                found.append(item)
    for pattern in SENSITIVE:
        for item in re.findall(BEFORE + "(" + pattern + ")" + AFTER, text):
            if item.lower() not in seen:
                seen.append(item.lower())
                found.append(item)
    return found
