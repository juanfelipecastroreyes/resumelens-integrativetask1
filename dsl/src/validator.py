import sys
from pathlib import Path
from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError

GRAMMAR_PATH = Path(__file__).resolve().parent.parent / "grammar" / "resume.tx"


def validate(resume_path):
    mm = metamodel_from_file(str(GRAMMAR_PATH))
    try:
        model = mm.model_from_file(resume_path)
        return True, model
    except TextXSyntaxError as e:
        return False, str(e)


def main():
    resume_path = sys.argv[1]
    ok, result = validate(resume_path)

    if ok:
        print(f"VALID: {resume_path}")
    else:
        print(f"INVALID: {resume_path}")
        print(result)


if __name__ == "__main__":
    main()
