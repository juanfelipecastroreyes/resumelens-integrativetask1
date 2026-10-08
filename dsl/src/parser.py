#%%
import sys
from validator import validate

class Resume:

    def interpret(self, model):
        print(f"Candidate: {model.personal_info.name} ({model.personal_info.location})")

        print(f"Email: {model.contact.email} | GitHub: {model.contact.github}")
        if model.contact.phone:
            print(f"Phone: {model.contact.phone}")

        for e in model.experiences:
            print(f"Experience: {e.position} at {e.company} ({e.years} yr(s)) — {e.description}")

        for ed in model.education:
            print(f"Education: {ed.degree} — {ed.institution}")

        for s in model.skills:
            print(f"Skill: {s.name}")

        for q in model.qualifications:
            print(f"Qualification: {q.name} ({q.level})")

        print(f"Classification: {model.classification.label}")


resume_path = sys.argv[1]
ok, result = validate(resume_path)

if ok:
    resume = Resume()
    resume.interpret(result)
else:
    print(f"INVALID: {resume_path}")
    print(result)
