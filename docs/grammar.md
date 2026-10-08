# Grammar Specification — ResumeLens DSL

## 1. Design overview

The DSL represents a candidate résumé profile as produced by ResumeLens. The
language groups candidate information into seven categories, chosen to cover
the minimum structure required by the assignment: personal information,
contact information, professional experience, education, skills, normalized
qualifications, and the classification result.

Per-category fields and multiplicity are documented in
`docs/metamodel.md`, which lists the classes textX generates from this
grammar. The design decisions below explain *why* the grammar is shaped
this way.

### 1.1 Design decisions

- **Skill vs. Qualification.** These two categories look similar but serve
  different purposes. `Skill` is a raw, informal tag extracted directly from
  the résumé text (just a `name`, e.g. `"Python"`). `Qualification` is the
  *normalized* version explicitly requested by the assignment (Section 3:
  "normalized qualifications") — a skill that ResumeLens has processed into a
  structured form with a proficiency `level` (e.g. Beginner, Intermediate,
  Expert).
- **`years` in Experience.** Kept as a single field (matching the assignment's
  own parse-tree example in Section 8) rather than splitting into
  `start_year`/`end_year`, to keep the first version of the grammar simple.
  This can be revisited if a more precise date range is needed.
- **`phone` as optional in Contact.** The assignment's own examples only show
  `email` and `location`/`github` for contact info, so `phone` was added as an
  optional field rather than mandatory, since not every résumé will include
  it.
- **`Classification.label` as a free STRING.** Kept open-ended rather than
  restricted to a fixed set of job categories, to avoid maintaining an
  enumerated list of every possible classification ResumeLens might produce.
  This can be revisited and tightened to a fixed keyword set later if the
  project needs stricter validation on this field.

## 2. Terminals

| Terminal | Type | Description |
|---|---|---|
| `STRING` | pattern | Free quoted text — used for names, descriptions, emails, and the classification label |
| `INT` | pattern | Whole number — used for `years` |
| `"personal"` | keyword | Marks the start of a PersonalInfo block |
| `"contact"` | keyword | Marks the start of a Contact block |
| `"experience"` | keyword | Marks the start of an Experience block |
| `"education"` | keyword | Marks the start of an Education block |
| `"skill"` | keyword | Marks the start of a Skill block |
| `"qualification"` | keyword | Marks the start of a Qualification block |
| `"classification"` | keyword | Marks the start of a Classification block |
| `"Beginner"` \| `"Intermediate"` \| `"Expert"` | keyword set | Fixed values for `Qualification.level` |

## 3. Non-terminals

| Non-terminal | Made of |
|---|---|
| `Resume` | `PersonalInfo`, `Contact`, `Experience*`, `Education*`, `Skill*`, `Qualification*`, `Classification` |
| `PersonalInfo` | `name`, `location` |
| `Contact` | `email`, `github`, `phone` (optional) |
| `Experience` | `position`, `company`, `years`, `description` |
| `Education` | `institution`, `degree`, `description` |
| `Skill` | `name` |
| `Qualification` | `name`, `level` |
| `Classification` | `label` |

## 4. EBNF rules

```
Resume         ::= PersonalInfo Contact Experience* Education* Skill* Qualification* Classification

PersonalInfo   ::= "personal" name:STRING location:STRING

Contact        ::= "contact" email:STRING github:STRING phone:STRING?

Experience     ::= "experience" position:STRING company:STRING years:INT description:STRING

Education      ::= "education" institution:STRING degree:STRING description:STRING

Skill          ::= "skill" name:STRING

Qualification  ::= "qualification" name:STRING level:("Beginner"|"Intermediate"|"Expert")

Classification ::= "classification" label:STRING
```

## 5. Example instances

Two sample texts that a parser built from the rules above should
accept.

**Example 1 — full profile, exercising repeated blocks:**

```
personal "Camila Restrepo" "Medellín, Colombia"

contact "camila.restrepo@correo.com" "camilarestrepo" "+57 300 555 1234"

experience "Backend Developer" "Rappi" 3 "Built and maintained REST APIs for the internal logistics platform."
experience "Software Engineering Intern" "Bancolombia" 1 "Wrote automated test suites for the payments processing module."

education "Universidad ICESI" "B.Sc. in Systems Engineering" "Focused on distributed systems and databases."

skill "Java"
skill "Spring Boot"

qualification "Backend Development" Expert
qualification "Cloud Computing" Intermediate

classification "Backend Developer"
```

**Example 2 — minimal profile (zero experiences, education, skills, and qualifications):**

```
personal "Santiago Gómez" "Popayán, Colombia"

contact "santiago.gomez@correo.com" "santiagogomez"

classification "Data Analyst"
```
