# Stage 1: Information Extraction with Regular Expressions

## 1. What this stage does

This stage reads the text of a résumé and finds pieces of information that
can be useful later. It does not decide if two skills are the same, and it
does not decide if the candidate fits a job profile. Those jobs belong to
Stage 2 (normalization) and Stage 3 (classification).

The code is in `extraction/src/extractor.py` and `extraction/src/skills.py`.
It uses Python's `re` module. The result is a dictionary that is saved as a
JSON file in `extraction/output/`.

## 2. How to run it

```
python extraction/src/extractor.py extraction/examples/fullstack_01.txt
```

The tests are in `extraction/tests/`:

```
python -m unittest discover -s extraction/tests
```

## 3. Expressions

In the tables, "accepts" means a text that the expression finds and
"rejects" means a text that it does not find.

### 3.1 Contact information

| Data | Expression | Language it recognizes | Accepts | Rejects |
|---|---|---|---|---|
| Email | `[\w.+-]+@[\w-]+\.[\w.-]+` | One or more letters, digits, `_`, `.`, `+` or `-`, then `@`, then a domain with at least one dot | `wednesday.addams@correo.com` | `correo.com` |
| Phone with country code | `\+\d{1,3} \d{3} \d{3} \d{4}` | `+`, 1 to 3 digits, then three groups of digits separated by spaces | `+57 312 400 5566` | `57 312 400 5566` |
| Phone with area code | `\(\d{3}\) \d{3} \d{4}` | Three digits in parentheses, then two groups of digits | `(601) 555 0199` | `601 555 0199` |
| Phone with spaces or dashes | `\d{3}[ -]\d{3}[ -]\d{4}` | Three groups of digits, separated by a space or a dash | `312-400-5566` | `2019 - 2022` |
| Phone without separators | `\d{10}` | Exactly ten digits in a row | `3124005566` | `2020` |
| GitHub | `github\.com/[A-Za-z0-9-]+` | The text `github.com/` and then a user name | `github.com/mjwatson` | `github.com/` |
| LinkedIn | `linkedin\.com/in/[A-Za-z0-9_-]+` | The text `linkedin.com/in/` and then a profile name | `linkedin.com/in/gwenstacy` | `linkedin.com/gwenstacy` |

The code keeps only the user name for GitHub and LinkedIn. If the same
phone or email appears more than once, it is saved only once.

### 3.2 Professional experience

| Data | Expression | Language it recognizes | Accepts | Rejects |
|---|---|---|---|---|
| Years of experience | `\d+\+? years? of experience` | A number, an optional `+`, the word `year` or `years`, and `of experience` | `3 years of experience`, `10+ years of experience` | `years of experience` |
| Years (long form) | `\d+\+? years? of professional experience` | Same as above with the word `professional` | `5 years of professional experience` | `five years of professional experience` |
| Years (Spanish) | `\d+\+? años? de experiencia` | Same idea in Spanish | `5 años de experiencia` | `cinco años de experiencia` |
| Job title | Fixed list of titles, with optional `Senior`, `Junior` or `Lead` before the title | One of the titles in the list, written with capital letters as in the list | `Senior Backend Developer` | `Systems Engineering` |

The code keeps only the number for the years.

### 3.3 Education

| Data | Expression | Language it recognizes | Accepts | Rejects |
|---|---|---|---|---|
| Degree | `Bachelor[A-Za-z. ]*`, `Master[A-Za-z. ]*`, `B\.Sc\.[A-Za-z. ]*`, `M\.Sc\.[A-Za-z. ]*`, `Ph\.D\.[A-Za-z. ]*` | A degree word at the start, followed by letters, dots and spaces on the same line | `B.Sc. in Systems Engineering` | `bachelor` in lowercase |
| Institution in Spanish | `Universidad [A-Z]\w* de [A-Z]\w*`, `Universidad del? [A-Z]\w*`, `Universidad [A-Z]\w*` | `Universidad` and then capitalized names | `Universidad Nacional de Colombia`, `Universidad ICESI` | `universidad icesi` |
| Institution in English | `University of [A-Z]\w*`, `[A-Z]\w* University` | `University of` and a capitalized name, or a capitalized name and `University` | `University of Toronto` | `the university` |

### 3.4 Skills

The skills are in `skills.py`. The code first removes emails, links and the
job title `Machine Learning Engineer` from the text, so that
`github.com/user` is not read as the skill `Git` and a job title is not
read as a skill.

Each skill is a short expression. Two rules are used for all of them:

- The skill must not be inside another word. In the code this is a check
  before and after the match. For example, `SQL` is not found inside
  `MySQL`, and `JS` is not found inside `Node.js`.
- Most skills ignore capital letters. Short names do not: `R`, `TS`, `TF`,
  `ML`, `CV`, `REST` and `Express` are found only with exactly these capital
  letters. This avoids matching normal words such as "rest" or "express".

| Group | Skills that are looked for |
|---|---|
| Languages | Python, Java, JavaScript, JS, TypeScript, TS, SQL, R |
| Frontend | HTML, CSS, React, Angular, Vue |
| Backend | Node, Express, Spring Boot, Django, Flask, REST APIs |
| Databases | PostgreSQL, MySQL, MongoDB |
| DevOps | Docker, Git, AWS, CI/CD |
| Data and ML | Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, Keras, machine learning, deep learning, NLP, computer vision, MLOps |
| Cloud | Linux, Azure, GCP, Google Cloud, Kubernetes, K8s, Terraform |

The code returns each skill as it was written in the résumé, for example
`NodeJS`, `Tensor Flow` or `sklearn`. It does not change the spelling. The
spelling is changed in Stage 2. The list of final names is in
`docs/tokens.md`.

## 4. Output

`extract` returns a dictionary with four groups:

```
{
  "contact":    {"emails": [], "phones": [], "github": [], "linkedin": []},
  "experience": {"years": [], "positions": []},
  "education":  {"degrees": [], "institutions": []},
  "skills":     []
}
```

`extract_file` reads a text file and saves the same dictionary as JSON in
`extraction/output/`. The `skills` list is the input of Stage 2.

## 5. Known limits

- The job titles, degrees and institutions come from fixed patterns, so a
  title that is not in the list is not found.
- The résumés are in English, with a few Spanish words for the years.
- A short name written in capitals can match a normal word, for example `CV`
  in "attached CV". We accepted this on purpose.
