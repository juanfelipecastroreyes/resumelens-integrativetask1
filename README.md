# ResumeLens: Formal Language-Based Resume Screening

Integrative Task 1 of Computing and Discrete Structures III (CyED3), 2026-2, ICESI.

Authors: Juan Felipe Castro Reyes and Sebastián Mejía.

ResumeLens reads a plain-text résumé and decides which job profile fits the candidate. It does this only with tools from formal language theory: regular expressions, finite-state transducers, finite automata and a domain-specific language.

## How it works

```
resume (.txt) -> 1. Extraction -> 2. Normalization -> 3. Classification -> 4. DSL (.resume) -> Markdown
                  regex            transducers         finite automata      textX
```

| Stage | What it does | Tool | Folder |
|---|---|---|---|
| 1. Extraction | Finds contact data, experience, education and skills in raw text | Python `re` | `extraction/` |
| 2. Normalization | Turns each skill, as written, into one standard token and sorts the tokens by profile | pyformlang `FST` | `normalization/` |
| 3. Classification | Accepts or rejects the token sequence for each job profile | pyformlang finite automata | `classification/` |
| 4. DSL | Describes the final candidate profile and generates a Markdown report | textX | `dsl/` |

Stage 3 and the full pipeline are still in progress.

## Project structure

```
.
├── docs/
│   ├── tokens.md          skill token vocabulary
│   ├── regex.md           Stage 1: regular expressions
│   ├── formalization.md   Stage 2: transducers as 7-tuples
│   ├── grammar.md         Stage 4: EBNF grammar
│   ├── metamodel.md       Stage 4: textX metamodel
│   ├── ai-usage.md        AI usage log
│   └── diagrams/          transducer, automata and parse-tree diagrams
├── extraction/            src, tests, examples, output
├── normalization/         src, tests
└── dsl/                   grammar, src, examples, output, tests
```

## Requirements

- Python 3.10 or newer
- The packages in `requirements.txt` (textX and pyformlang)

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run every command from the root of the repository.

**Stage 1: extract data from a résumé**

```
python3 extraction/src/extractor.py extraction/examples/fullstack_01.txt
```

The result is printed and saved as JSON in `extraction/output/`.

**Stage 2: normalize and sort skills**

```
python3 -c "
import sys
sys.path.insert(0, 'normalization/src')
from transducers import normalize
from sorter import sort_tokens
result = normalize(['Node.js', 'ReactJS', 'JS', 'Postgres', 'Docker'])
print(result)
print(sort_tokens(result['tokens'], 'full_stack'))
"
```

**Stage 4: validate a `.resume` file and generate Markdown**

```
python3 dsl/src/validator.py dsl/examples/resume_01.resume
python3 dsl/src/markdown_generator.py dsl/examples/resume_01.resume
```

The report is saved in `dsl/output/`.

## Tests

The tests use `unittest`.

```
python3 -m unittest discover -s extraction/tests
python3 -m unittest discover -s normalization/tests
python3 -m unittest discover -s dsl/tests
```

## Documentation

- [Skill tokens](docs/tokens.md)
- [Regular expressions](docs/regex.md)
- [Transducer formalization](docs/formalization.md)
- [DSL grammar](docs/grammar.md)
- [DSL metamodel](docs/metamodel.md)
- [AI usage log](docs/ai-usage.md)

## AI usage

AI assistance (Claude) was used in this project at level 3. Every use is recorded in [docs/ai-usage.md](docs/ai-usage.md).
