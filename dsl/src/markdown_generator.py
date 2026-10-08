import sys
from pathlib import Path
 
from validator import validate
 
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

def generate_markdown(model):
    lines = [f"# {model.personal_info.name}", "", "## Candidate Profile", "",
             f"**Classification:** {model.classification.label}", "", "## Contact", "",
             f"- Email: {model.contact.email}", f"- Location: {model.personal_info.location}",
             f"- GitHub: {model.contact.github}"]

    if model.contact.phone:
        lines.append(f"- Phone: {model.contact.phone}")
    lines.append("")

    if model.skills:
        lines.append("## Skills")
        lines.append("")
        for skill in model.skills:
            lines.append(f"- {skill.name}")
        lines.append("")

    if model.qualifications:
        lines.append("## Qualifications")
        lines.append("")
        for q in model.qualifications:
            lines.append(f"- {q.name} ({q.level})")
        lines.append("")

    if model.experiences:
        lines.append("## Experience")
        lines.append("")
        for exp in model.experiences:
            lines.append(f"### {exp.position}")
            lines.append("")
            lines.append(f"**{exp.company}** — {exp.years} year(s)")
            lines.append("")
            lines.append(exp.description)
            lines.append("")

    if model.education:
        lines.append("## Education")
        lines.append("")
        for ed in model.education:
            lines.append(f"**{ed.institution}** — {ed.degree}")
            lines.append("")
            lines.append(ed.description)
            lines.append("")
 
    return "\n".join(lines).rstrip() + "\n"

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/markdown_generator.py <path-to-.resume>")
        sys.exit(1)
 
    resume_path = sys.argv[1]
    ok, result = validate(resume_path)
 
    if not ok:
        print(f"INVALID: {resume_path}")
        print(result)
        sys.exit(1)
 
    markdown = generate_markdown(result)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{Path(resume_path).stem}.md"
    output_path.write_text(markdown, encoding="utf-8")
 
    print(markdown)
    print(f"\nWritten to: {output_path}")

if __name__ == "__main__":
    main()
 