import json
import os
import re
import sys

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

EMAIL = r"[\w.+-]+@[\w-]+\.[\w.-]+"

PHONES = [
    r"\+\d{1,3} \d{3} \d{3} \d{4}",
    r"\(\d{3}\) \d{3} \d{4}",
    r"\d{3}[ -]\d{3}[ -]\d{4}",
    r"\d{10}",
]

GITHUB = r"github\.com/[A-Za-z0-9-]+"
LINKEDIN = r"linkedin\.com/in/[A-Za-z0-9_-]+"

YEARS = [
    r"\d+\+? years? of experience",
    r"\d+\+? years? of professional experience",
    r"\d+\+? años? de experiencia",
]

TITLES = [
    "Full Stack Developer", "Frontend Developer", "Backend Developer",
    "Web Developer", "Software Developer", "Software Engineer",
    "Data Scientist", "Data Engineer", "Data Analyst",
    "Machine Learning Engineer", "DevOps Engineer", "AI Engineer",
]
LEVELS = ["Senior", "Junior", "Lead"]

DEGREES = [
    r"Bachelor[A-Za-z. ]*",
    r"Master[A-Za-z. ]*",
    r"B\.Sc\.[A-Za-z. ]*",
    r"M\.Sc\.[A-Za-z. ]*",
    r"Ph\.D\.[A-Za-z. ]*",
]

INSTITUTIONS = [
    r"Universidad [A-Z]\w* de [A-Z]\w*",
    r"Universidad del? [A-Z]\w*",
    r"Universidad [A-Z]\w*",
    r"University of [A-Z]\w*",
    r"[A-Z]\w* University",
]

def find_all(patterns, text, flags=0):
    found = []
    for pattern in patterns:
        for item in re.findall(pattern, text, flags):
            found.append(item.strip())
    return found

def clean(items):
    result = []
    for item in items:
        keep = True
        if item in result:
            keep = False
        for other in items:
            if item != other and item in other:
                keep = False
        if keep:
            result.append(item)
    return result

def extract(text):
    emails = []
    for email in re.findall(EMAIL, text):
        emails.append(email.strip("."))

    phones = find_all(PHONES, text)

    github = []
    for url in find_all([GITHUB], text, re.IGNORECASE):
        github.append(url.split("/")[1])

    linkedin = []
    for url in find_all([LINKEDIN], text, re.IGNORECASE):
        linkedin.append(url.split("/")[2])

    years = []
    for phrase in find_all(YEARS, text, re.IGNORECASE):
        number = phrase.split()[0].replace("+", "")
        years.append(int(number))

    position_patterns = []
    for title in TITLES:
        position_patterns.append(title)
        for level in LEVELS:
            position_patterns.append(level + " " + title)
    positions = find_all(position_patterns, text)

    degrees = find_all(DEGREES, text)
    institutions = find_all(INSTITUTIONS, text)

    return {
        "contact": {
            "emails": clean(emails),
            "phones": clean(phones),
            "github": clean(github),
            "linkedin": clean(linkedin),
        },
        "experience": {
            "years": years,
            "positions": clean(positions),
        },
        "education": {
            "degrees": clean(degrees),
            "institutions": clean(institutions),
        },
    }

def extract_file(path, save=True):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    result = extract(text)
    if save:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        name = os.path.splitext(os.path.basename(path))[0]
        with open(os.path.join(OUTPUT_DIR, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <resume.txt> [...]")
        sys.exit(1)
    for path in sys.argv[1:]:
        print("==", path)
        print(json.dumps(extract_file(path), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
