# AI Usage Log — ResumeLens DSL

This document records the key design decisions and instructions developed
with AI assistance (Claude) during this project, and how those decisions
were verified before being adopted.

## Scope of AI assistance

1. **Conceptual framing** — situating grammars, EBNF, and textX-based DSL
   implementation within the formal language theory covered in this course.
2. **Draft generation** — proposed structures (grammar categories, field
   sets, documentation) produced as a starting point for review, revision,
   or rejection, never adopted without evaluation.

## Verification methodology

- **Requirement traceability.** Every proposed structure is checked against
  the assignment specification directly, not accepted on the AI's authority.
- **Conceptual consistency.** New material is evaluated against material
  already mastered (automata theory) for internal consistency before being
  relied on.
- **Executable verification.** Grammar and parser correctness is confirmed
  by running textX against valid and invalid `.resume` cases and checking
  the accept/reject behavior directly, not by inspection alone.
- **Independent justification.** Design decisions are retained only if they
  can be defended without reference to the AI's original explanation, since
  the design must be presented and defended independently in class.

## Key decisions

| Date | Instruction | Decision reached | Verification |
|---|---|---|---|
| 2026-09-22 | Requested a proposed field set for the seven required grammar categories | Adopted field table distinguishing `Skill` (informal tag) from `Qualification` (normalized, with proficiency level), per assignment Section 3 | Cross-checked against the assignment's own parse-tree and Markdown output examples |
| 2026-09-24 | Asked whether `docs/grammar.md` was redundant with the newly drafted `docs/metamodel.md` | Kept both as separate documents with distinct scopes: `grammar.md` covers design rationale and EBNF rules; `metamodel.md` covers the textX-generated classes and their attributes. No overlapping content between the two | Compared section-by-section content of both drafts before finalizing; confirmed each answers a different question (why the grammar is shaped this way vs. what classes textX derives from it) |
| 2026-09-24 | Requested a review of the documentation set to confirm what was still missing, specifically whether only the Markdown diagram remained | Identified that beyond the diagram, the metamodel doc, a second example file, and an EBNF/grammar.tx consistency check were also outstanding — not just the Markdown diagram | Cross-checked the repository's actual committed files against the assignment's required deliverables (grammar, metamodel, diagram, ≥2 examples) rather than relying on memory of what had been drafted |
| 2026-09-24 | Asked for the end-to-end flow of the program (parser → model → interpreter) to be explained | Adopted the explanation of the pipeline: `resume.tx` grammar → textX metamodel → `.resume` file parsed into a model instance → `parser.py`/`validator.py` consume the model | Verified by tracing the actual code path in `src/parser.py` and `src/validator.py` against the explanation, rather than accepting the description at face value |
| 2026-09-24 | Requested the metamodel diagram be added in Mermaid syntax, as a document separate from `metamodel.md`, using a different presentation than the main doc | Created `docs/metamodel_diagram.md` as a standalone file containing only the Mermaid class diagram, kept out of `metamodel.md` to avoid duplicating the same diagram in two places | Confirmed the diagram's classes and attributes match the class table already verified in `metamodel.md`, so no new content was introduced without cross-checking |
| 2026-09-27 | Asked whether the diagram could be rendered vertically instead of horizontally | Adjusted the Mermaid diagram's layout direction without changing its content (same classes, attributes, and relationships) | Re-rendered the diagram after the change and confirmed it still reflects the same metamodel structure as the horizontal version |
| 2026-09-30 | Requested a full project review against the assignment rubric | Compiled a punch list of what was already complete (markdown generator, tests, diagrams) versus still outstanding (README, grammar/resume.tx consistency) | Cross-checked the actual repository state (via git log and file listing) against each rubric section, rather than relying on earlier assumptions |
| 2026-09-30 | Flagged that `docs/grammar.md`'s `Contact` field order didn't match `grammar/resume.tx` | Corrected the non-terminal table, EBNF rule, and example instances in `grammar.md` to use the real order (`email, github, phone`) | Re-read `grammar/resume.tx` and the actual `.resume` example files to confirm the corrected order matches the executable grammar, not just the documentation |
| 2026-09-30 | Requested a review of the `README.md` draft, written independently, against the rubric's required sections | Identified which required sections (description, team, language, structure, requirements, installation, usage, examples, authors) were present versus missing or incomplete, and suggested targeted additions rather than a rewrite | Compared the draft section-by-section against the assignment's explicit README requirements and the actual repository structure |
| 2026-09-30 | Requested feedback on the parse-tree diagrams for the three examples, iterating on the layout (too horizontal, then artificial-looking, then block-style and vertical) | Refined the diagram layout in stages — from a flat Mermaid class diagram, to a forced single-column layout, to a custom block-tree with short connector lines — based on direct feedback at each step | Rendered and visually reviewed each iteration before presenting it, explaining the width/height trade-offs rather than delivering an unreviewed result |
