# Test case design

This document explains how the tests are organized and which scenarios they cover. All tests use `unittest`.

## 1. Strategy

| Folder | Stage | Tests | What it checks |
|---|---|---|---|
| `extraction/tests` | 1. Extraction | 25 | Each regular expression, and the example résumés |
| `normalization/tests` | 2. Normalization | 29 | Spelling to token, vocabulary rules and sorting |
| `classification/tests` | 3. Classification | 37 | Automaton types, definitions and accepted or rejected sequences |
| `dsl/tests` | 4. DSL | 21 | Valid and invalid `.resume` files, builder and Markdown report |
| `tests` | Pipeline and app | 23 | The four stages together and the Streamlit interface |

Each test case has three parts: an input, an expected result and the test that checks it. The tests are grouped in classes by scenario.

Run all tests from the root of the repository:

```
python3 -m unittest discover -s extraction/tests
python3 -m unittest discover -s normalization/tests
python3 -m unittest discover -s classification/tests
python3 -m unittest discover -s dsl/tests
python3 -m unittest discover -s tests
```

## 2. End-to-end scenarios

These scenarios run the whole pipeline (`tests/test_pipeline.py`).

| Scenario | Input | Expected result | Test |
|---|---|---|---|
| Full Stack candidate | `fullstack_01.txt` | Full Stack Developer | `test_fullstack_01` |
| Full Stack skills without Git | `fullstack_02.txt` | No profile (`Unclassified`), but the `.resume` file is valid | `test_fullstack_02_has_no_git`, `test_no_accepted_profile_is_unclassified_but_valid` |
| ML candidate | `mlengineer_01.txt` | Machine Learning Engineer and Data Scientist | `test_mlengineer_01` |
| ML candidate with spelling variants | `mlengineer_02.txt` | Machine Learning Engineer and Data Scientist | `test_mlengineer_02` |
| Cloud candidate | `AWS, Docker, Terraform, Git` | Cloud Engineer | `test_cloud_engineer` |
| Empty text | `""` | No labels, valid file | `test_empty_text` |
| Header only | Name and location, no skills | No tokens, valid file | `test_header_only` |
| Skills outside the vocabulary | `Cobol, Fortran` | No tokens, no labels | `test_skills_outside_vocabulary_are_ignored` |
| Extra unknown skill | `Python, Cobol, SQL, Pandas, TensorFlow, Git` | Still accepted as ML Engineer | `test_extra_skills_do_not_block_a_profile` |
| Different skill order | Same skills in two orders | Same labels | `test_skill_order_does_not_change_result` |
| Quotes in the name | `Ana "Pepa" Perez` | Valid `.resume` file | `test_quotes_in_name_keep_the_file_valid` |
| Files are written | `fullstack_01.txt` | `.resume` and Markdown files exist | `test_files_are_written_and_valid` |
| Report content | `fullstack_01.txt` | Markdown has the candidate name | `test_markdown_has_candidate_name` |
| Every label is saved | `mlengineer_01.txt` | `.resume` has one `classification` per label | `test_resume_contains_every_label` |

## 3. Interface scenarios

These scenarios use Streamlit's `AppTest` (`tests/test_pipeline.py`).

| Scenario | Expected result | Test |
|---|---|---|
| The app starts with the first example | No exceptions | `test_app_starts_without_errors` |
| Result of every profile | At least 4 result messages | `test_app_shows_four_profiles` |
| Pasted text | `Cloud Engineer (EPSILON_NFA): ACCEPTED` | `test_app_accepts_pasted_text` |
| No text | An info message asks for input | `test_app_asks_for_input_when_empty` |

## 4. Stage 1: Extraction

| Scenario | Test |
|---|---|
| Email, phone formats, GitHub and LinkedIn | `test_email`, `test_phone_formats`, `test_github_and_linkedin` |
| A year range is not a phone number | `test_year_range_is_not_a_phone` |
| Years of experience in English, with `+` and in Spanish | `test_years_english`, `test_years_with_plus`, `test_years_spanish` |
| Position with level; a degree is not a position | `test_position_with_level`, `test_degree_is_not_a_position` |
| Degree and institution, also with "de" | `test_degree_and_institution`, `test_institution_with_de` |
| Skill variants such as Node | `test_node_variants` |
| One skill inside another is not found: `JS` in `Node.js`, `Java` in `JavaScript`, `SQL` in `MySQL` | `test_js_is_not_found_inside_node_js`, `test_java_is_not_javascript`, `test_sql_is_not_inside_mysql` |
| Short names need capitals; `R` inside "R&D" | `test_short_names_need_capitals`, `test_r_inside_r_and_d` |
| Job titles, links and emails are not skills | `test_job_title_is_not_a_skill`, `test_links_and_emails_are_ignored` |
| `REST API` is one skill; cloud skills | `test_rest_api_is_one_skill`, `test_cloud_skills` |
| The four example résumés | `test_fullstack_01`, `test_fullstack_02`, `test_mlengineer_01`, `test_mlengineer_02` |

## 5. Stage 2: Normalization

| Scenario | Test |
|---|---|
| Symbols and capitals are removed before translating | `test_removes_symbols_and_capitals` |
| Spellings give the right token: JavaScript, React, Node, PostgreSQL, scikit-learn, TensorFlow, PyTorch, REST, cloud skills | `test_javascript`, `test_react`, `test_node`, `test_postgres`, `test_scikit_learn`, `test_tensorflow_and_pytorch`, `test_rest`, `test_cloud` |
| A spelling that is the start of another one | `test_prefix_of_another_spelling` |
| Unknown skill gives `None` | `test_unknown_skill` |
| Every spelling gives its token; no spelling is used twice | `test_every_spelling_gives_its_token`, `test_no_spelling_is_used_twice` |
| Assignment example; repeated spellings give one token; unknown skills are reported | `test_assignment_example`, `test_repeated_spellings_give_one_token`, `test_unknown_skills_are_reported` |
| Sorting for each profile | `test_ml_engineer`, `test_data_scientist`, `test_cloud_engineer`, `test_full_stack_example` |
| Sorting does not depend on the input order | `test_order_does_not_depend_on_input_order` |
| Tokens outside the profile go last; empty list; unknown profile | `test_tokens_outside_the_profile_go_last`, `test_empty_list`, `test_unknown_profile` |
| Order lists only use vocabulary tokens, without repeats | `test_profile_tokens_exist_in_the_vocabulary`, `test_profile_has_no_repeated_token` |
| All example résumés are normalized | `test_all_examples_are_normalized` |

## 6. Stage 3: Classification

| Scenario | Test |
|---|---|
| Examples from the assignment | `test_machine_learning_example`, `test_full_stack_example`, `test_full_stack_example_is_not_the_other_profiles` |
| Automaton types: DFA, DFA, NFA, ε-NFA | `test_full_stack_is_a_dfa`, `test_ml_engineer_is_a_dfa`, `test_data_scientist_is_an_nfa`, `test_cloud_engineer_is_an_epsilon_nfa`, `test_declared_type_matches_the_automaton` |
| Number of states and one start state | `test_number_of_states`, `test_one_start_state` |
| Definitions: tokens belong to the alphabet, no repeats, groups follow the sorting order | `test_group_tokens_belong_to_the_alphabet`, `test_alphabet_has_no_repeated_token`, `test_groups_follow_the_sorting_order`, `test_every_profile_has_a_sorting_order` |
| Minimal sequence accepted; every token of every group accepted | `test_minimal_sequence_is_accepted`, `test_every_token_of_every_group_is_accepted` |
| A missing group or an empty sequence is rejected | `test_missing_group_is_rejected`, `test_empty_sequence_is_rejected` |
| Extra tokens do not change the result; same result every time | `test_extra_tokens_do_not_change_the_result`, `test_repeated_use_gives_the_same_result` |
| Random candidates against a simple rule | `test_random_candidates` |
| Unsorted input is rejected by the automaton; `classify` sorts it | `test_unsorted_input_is_rejected_by_the_automaton`, `test_classify_does_not_depend_on_input_order` |
| Data Scientist routes (NFA) | `test_classic_route`, `test_deep_learning_route`, `test_needs_a_modeling_skill`, `test_does_not_need_a_deep_learning_framework` |
| Cloud Engineer routes (ε-NFA) | `test_each_provider_is_accepted`, `test_needs_a_provider`, `test_kubernetes_and_ci_cd` |
| One candidate, several profiles; no profile; labels | `test_one_candidate_can_fit_two_profiles`, `test_no_profile`, `test_labels` |
| With the previous stages: Full Stack with and without Git, ML examples, cloud skills from text | `test_fullstack_example`, `test_fullstack_example_without_git`, `test_machine_learning_examples`, `test_cloud_skills_from_text` |

## 7. Stage 4: DSL

Test files are in `dsl/tests/valid` and `dsl/tests/invalid`.

| File | Scenario | Expected |
|---|---|---|
| `valid_01_no_optional_phone.resume` | The phone is optional | Valid |
| `valid_02_with_phone_and_multiple_qualifications.resume` | Phone and several qualifications | Valid |
| `valid_03_multiple_classifications.resume` | Several classifications | Valid |
| `invalid_01_missing_mandatory.resume` | A mandatory field is missing | Rejected |
| `invalid_02_wrong_keyword.resume` | A wrong keyword | Rejected |
| `invalid_03_malformed_field.resume` | A malformed field | Rejected |
| `invalid_04_invalid_nesting.resume` | Invalid nesting | Rejected |
| `invalid_05_bad_list_syntax.resume` | Bad list syntax | Rejected |
| `invalid_06_incomplete_profile.resume` | An incomplete profile | Rejected |
| `invalid_07_classification_without_label.resume` | A classification without a label | Rejected |

| Scenario | Test |
|---|---|
| The examples and the valid files pass; the invalid files fail | `test_examples_are_valid`, `test_valid_tests_are_valid`, `test_invalid_tests_are_rejected` |
| One or several classifications; the report lists every one | `test_single_classification`, `test_multiple_classifications`, `test_markdown_lists_every_classification` |
| No classification is invalid; the phone is optional | `test_no_classification_is_invalid`, `test_optional_phone_is_none` |
| Text helpers: quotes are wrapped and inner quotes replaced; level depends on the years | `test_quote_wraps_text`, `test_quote_replaces_inner_quotes`, `test_level_for_years`, `test_level_depends_on_years` |
| Every example builds a valid file | `test_every_example_builds_a_valid_resume` |
| Name, location and contact data come from the résumé | `test_name_and_location_come_from_first_lines`, `test_contact_data_is_copied` |
| Skills keep their spelling; qualifications are tokens | `test_skills_keep_the_original_spelling`, `test_qualifications_are_normalized_tokens` |
| Several labels; empty extraction is still valid; phone is optional; position without years uses 0 | `test_several_labels`, `test_empty_extraction_is_still_valid`, `test_phone_is_optional`, `test_position_without_years_uses_zero` |
