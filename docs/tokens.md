# Skill Token Vocabulary

## 1. Purpose

A token is the single canonical name for a skill, no matter how the résumé
spells it. The extraction stage finds the raw skill text, the transducers
(Stage 2) convert every spelling into one token, and the finite automata
(Stage 3) read sequences of tokens. The set of tokens is therefore the input
alphabet of the automata, and all modules must use exactly these names.

## 2. Format

- UPPERCASE letters and digits only.
- Words separated by an underscore.
- No spaces, dots, slashes or hyphens inside a token.

Example: `Node.js`, `NodeJS` and `node` all become `NODE_JS`.

## 3. Tokens

| Category | Token | Accepted spellings |
|---|---|---|
| Languages | `PYTHON` | python, python3 |
| Languages | `JAVA` | java |
| Languages | `JAVASCRIPT` | javascript, js |
| Languages | `TYPESCRIPT` | typescript, ts |
| Languages | `SQL` | sql |
| Languages | `R_LANG` | R |
| Frontend | `HTML` | html, html5 |
| Frontend | `CSS` | css, css3 |
| Frontend | `REACT` | react, react.js, reactjs |
| Frontend | `ANGULAR` | angular |
| Frontend | `VUE` | vue, vue.js |
| Backend | `NODE_JS` | node, node.js, nodejs |
| Backend | `EXPRESS` | express, express.js |
| Backend | `SPRING_BOOT` | spring, spring boot |
| Backend | `DJANGO` | django |
| Backend | `FLASK` | flask |
| Backend | `REST_API` | rest, restful, rest api |
| Databases | `POSTGRESQL` | postgres, postgresql |
| Databases | `MYSQL` | mysql |
| Databases | `MONGODB` | mongo, mongodb |
| DevOps | `DOCKER` | docker |
| DevOps | `GIT` | git |
| DevOps | `AWS` | aws, amazon web services |
| DevOps | `CI_CD` | ci/cd, cicd |
| Data and ML | `PANDAS` | pandas |
| Data and ML | `NUMPY` | numpy |
| Data and ML | `SCIKIT_LEARN` | scikit-learn, sklearn |
| Data and ML | `TENSORFLOW` | tensorflow, tf |
| Data and ML | `PYTORCH` | pytorch, torch |
| Data and ML | `KERAS` | keras |
| Data and ML | `MACHINE_LEARNING` | machine learning, ml |
| Data and ML | `DEEP_LEARNING` | deep learning |
| Data and ML | `NLP` | nlp, natural language processing |
| Data and ML | `COMPUTER_VISION` | computer vision, cv |
| Data and ML | `MLOPS` | mlops |

## 4. Short abbreviations

`R`, `CV`, `TS` and `TF` are short and can match unrelated words. They count
only as whole words written in uppercase, exactly as shown here.

## 5. Profile groups

| Profile | Token groups |
|---|---|
| Full Stack Developer | Languages, Frontend, Backend, Databases, DevOps |
| Machine Learning Engineer | `PYTHON`, `SQL`, Data and ML, `DOCKER`, `GIT`, `AWS` |
| Team profile (software) | Pending |
| Team profile (AI / data) | Pending |

Tokens for the two team profiles will be added in the same format.
