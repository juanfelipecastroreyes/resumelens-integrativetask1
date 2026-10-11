import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "extraction", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "normalization", "src"))

from extractor import extract
from transducers import normalize
from validator import validate

OUTPUT_DIR = os.path.join(HERE, "..", "generated")
NOT_SPECIFIED = "Not specified"


def quote(text):
    return '"' + text.replace('"', "'") + '"'


def first(items, default):
    if len(items) > 0:
        return items[0]
    return default


def pick(items, index, default):
    if index < len(items):
        return items[index]
    return default


def level_for(years):
    if years >= 5:
        return "Expert"
    if years >= 2:
        return "Intermediate"
    return "Beginner"


def build_resume(name, location, extracted, tokens, labels):
    contact = extracted["contact"]
    experience = extracted["experience"]
    education = extracted["education"]
    years = experience["years"]
    positions = experience["positions"]
    degrees = education["degrees"]
    institutions = education["institutions"]

    lines = []
    lines.append("personal " + quote(name) + " " + quote(location))
    lines.append("")

    contact_line = "contact " + quote(first(contact["emails"], "")) + " " + quote(first(contact["github"], ""))
    if len(contact["phones"]) > 0:
        contact_line = contact_line + " " + quote(contact["phones"][0])
    lines.append(contact_line)
    lines.append("")

    experience_count = max(len(positions), len(years))
    for i in range(experience_count):
        position = pick(positions, i, NOT_SPECIFIED)
        number = pick(years, i, first(years, 0))
        lines.append("experience " + quote(position) + " " + quote(NOT_SPECIFIED) + " " + str(number) + " " + quote(NOT_SPECIFIED))
    if experience_count > 0:
        lines.append("")

    education_count = max(len(degrees), len(institutions))
    for i in range(education_count):
        institution = pick(institutions, i, NOT_SPECIFIED)
        degree = pick(degrees, i, NOT_SPECIFIED)
        lines.append("education " + quote(institution) + " " + quote(degree) + " " + quote(NOT_SPECIFIED))
    if education_count > 0:
        lines.append("")

    for skill in extracted["skills"]:
        lines.append("skill " + quote(skill))
    if len(extracted["skills"]) > 0:
        lines.append("")

    top_years = 0
    for number in years:
        if number > top_years:
            top_years = number
    level = level_for(top_years)
    for token in tokens:
        lines.append("qualification " + quote(token) + " " + level)
    if len(tokens) > 0:
        lines.append("")

    if len(labels) == 0:
        labels = ["Unclassified"]
    for label in labels:
        lines.append("classification " + quote(label))

    return "\n".join(lines) + "\n"


def build_from_text(text, labels):
    rows = text.split("\n")
    name = rows[0].strip()
    location = rows[1].strip()
    extracted = extract(text)
    tokens = normalize(extracted["skills"])["tokens"]
    return build_resume(name, location, extracted, tokens, labels)


def main():
    if len(sys.argv) < 3:
        print("Usage: python resume_builder.py <resume.txt> <label> [label ...]")
        sys.exit(1)

    path = sys.argv[1]
    labels = sys.argv[2:]
    with open(path, encoding="utf-8") as f:
        text = f.read()

    content = build_from_text(text, labels)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    output_path = os.path.join(OUTPUT_DIR, stem + ".resume")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(content)
    ok, result = validate(output_path)
    if ok:
        print("VALID: " + output_path)
    else:
        print("INVALID: " + output_path)
        print(result)


if __name__ == "__main__":
    main()
