import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
for folder in ["extraction", "normalization", "classification", "dsl"]:
    sys.path.insert(0, os.path.join(ROOT, folder, "src"))

import resume_builder
from automata import PROFILES, classify
from extractor import extract
from markdown_generator import OUTPUT_DIR, generate_markdown
from resume_builder import build_resume
from transducers import normalize
from validator import validate

NOT_SPECIFIED = "Not specified"


def read_header(text):
    rows = text.split("\n")
    name = NOT_SPECIFIED
    location = NOT_SPECIFIED
    if len(rows) > 0 and rows[0].strip() != "":
        name = rows[0].strip()
    if len(rows) > 1 and rows[1].strip() != "":
        location = rows[1].strip()
    return name, location


def run(text, stem):
    name, location = read_header(text)

    extracted = extract(text)

    normalized = normalize(extracted["skills"])
    tokens = normalized["tokens"]

    results = classify(tokens)
    labels = []
    for profile in PROFILES:
        if results[profile] == "ACCEPTED":
            labels.append(PROFILES[profile]["label"])

    content = build_resume(name, location, extracted, tokens, labels)
    os.makedirs(resume_builder.OUTPUT_DIR, exist_ok=True)
    resume_path = os.path.join(resume_builder.OUTPUT_DIR, stem + ".resume")
    with open(resume_path, "w", encoding="utf-8") as f:
        f.write(content)

    valid, model = validate(resume_path)
    markdown_path = None
    if valid:
        os.makedirs(str(OUTPUT_DIR), exist_ok=True)
        markdown_path = os.path.join(str(OUTPUT_DIR), stem + ".md")
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(generate_markdown(model))

    return {
        "extracted": extracted,
        "tokens": tokens,
        "unknown": normalized["unknown"],
        "results": results,
        "labels": labels,
        "resume_path": resume_path,
        "valid": valid,
        "error": None if valid else model,
        "markdown_path": markdown_path,
    }


def show(path, outcome):
    print("=" * 60)
    print(path)
    print("=" * 60)
    print("Stage 1 - Extraction")
    print("  skills: " + ", ".join(outcome["extracted"]["skills"]))
    print("Stage 2 - Normalization")
    print("  tokens: " + ", ".join(outcome["tokens"]))
    if len(outcome["unknown"]) > 0:
        print("  unknown: " + ", ".join(outcome["unknown"]))
    print("Stage 3 - Classification")
    for profile in PROFILES:
        label = PROFILES[profile]["label"]
        print("  " + label + ": " + outcome["results"][profile])
    print("Stage 4 - DSL")
    if outcome["valid"]:
        print("  VALID: " + os.path.relpath(outcome["resume_path"], ROOT))
        print("  Markdown: " + os.path.relpath(outcome["markdown_path"], ROOT))
    else:
        print("  INVALID: " + os.path.relpath(outcome["resume_path"], ROOT))
        print(outcome["error"])
    print("")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline.py <resume.txt> [<resume.txt> ...]")
        sys.exit(1)

    failed = False
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        stem = os.path.splitext(os.path.basename(path))[0]
        outcome = run(text, stem)
        show(path, outcome)
        if not outcome["valid"]:
            failed = True

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
