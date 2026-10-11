import glob
import os
import sys
import tempfile

import pandas as pd
import streamlit as st

ROOT = os.path.dirname(os.path.abspath(__file__))
for folder in ["extraction", "normalization", "classification", "dsl"]:
    sys.path.insert(0, os.path.join(ROOT, folder, "src"))

from automata import PROFILES
from automata import classify
from extractor import extract
from markdown_generator import generate_markdown
from resume_builder import build_resume
from sorter import sort_tokens
from transducers import build_all, normalize, normalize_skill
from validator import validate

NOT_SPECIFIED = "Not specified"
EXAMPLES = sorted(glob.glob(os.path.join(ROOT, "extraction", "examples", "*.txt")))
DIAGRAMS = os.path.join(ROOT, "docs", "diagrams", "automata")

st.set_page_config(page_title="ResumeLens", page_icon=":mag:", layout="wide")


@st.cache_resource
def get_transducers():
    return build_all()


def read_header(text):
    rows = text.split("\n")
    name = NOT_SPECIFIED
    location = NOT_SPECIFIED
    if len(rows) > 0 and rows[0].strip() != "":
        name = rows[0].strip()
    if len(rows) > 1 and rows[1].strip() != "":
        location = rows[1].strip()
    return name, location


def validate_text(content):
    with tempfile.NamedTemporaryFile("w", suffix=".resume", delete=False, encoding="utf-8") as f:
        f.write(content)
        path = f.name
    valid, model = validate(path)
    os.remove(path)
    return valid, model


st.title(":mag: ResumeLens")
st.markdown(
    "Reads a plain-text résumé and decides which job profile fits the candidate, "
    "using regular expressions, finite-state transducers, finite automata and a DSL."
)

st.sidebar.header("Résumé input")
source = st.sidebar.radio("Source", ["Example", "Paste text", "Upload .txt"])

text = ""
if source == "Example":
    names = []
    for path in EXAMPLES:
        names.append(os.path.basename(path))
    choice = st.sidebar.selectbox("Example résumé", names)
    with open(os.path.join(ROOT, "extraction", "examples", choice), encoding="utf-8") as f:
        text = f.read()
elif source == "Paste text":
    text = st.sidebar.text_area("Résumé text", height=300)
else:
    uploaded = st.sidebar.file_uploader("Résumé file", type=["txt"])
    if uploaded is not None:
        text = uploaded.getvalue().decode("utf-8")

st.sidebar.markdown("Line 1 is the name and line 2 is the location.")

if text.strip() == "":
    st.info("Choose an example, paste a résumé or upload a .txt file.")
    st.stop()

with st.expander("Résumé text", expanded=False):
    st.text(text)

name, location = read_header(text)
extracted = extract(text)
normalized = normalize(extracted["skills"])
tokens = normalized["tokens"]
results = classify(tokens)
labels = []
for profile in PROFILES:
    if results[profile] == "ACCEPTED":
        labels.append(PROFILES[profile]["label"])

tab1, tab2, tab3, tab4 = st.tabs(
    ["1. Extraction (regex)", "2. Normalization (FST)", "3. Classification (automata)", "4. DSL (textX)"]
)

with tab1:
    st.subheader("Extracted data")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Contact**")
        st.json(extracted["contact"])
    with col2:
        st.markdown("**Experience**")
        st.json(extracted["experience"])
        st.markdown("**Education**")
        st.json(extracted["education"])
    st.markdown("**Skills, as written**")
    st.write(", ".join(extracted["skills"]))

with tab2:
    st.subheader("Skill to token")
    transducers = get_transducers()
    rows = []
    for skill in extracted["skills"]:
        token = normalize_skill(skill, transducers)
        if token is None:
            token = "(unknown)"
        rows.append({"Skill as written": skill, "Token": token})
    st.dataframe(pd.DataFrame(rows))
    st.markdown("**Tokens:** " + ", ".join(tokens))
    if len(normalized["unknown"]) > 0:
        st.warning("Unknown skills: " + ", ".join(normalized["unknown"]))

with tab3:
    st.subheader("Result for each profile")
    for profile in PROFILES:
        label = PROFILES[profile]["label"]
        kind = PROFILES[profile]["type"]
        ordered = sort_tokens(tokens, profile)
        if results[profile] == "ACCEPTED":
            st.success(label + " (" + kind + "): ACCEPTED")
        else:
            st.error(label + " (" + kind + "): REJECTED")
        st.caption("Sorted input: " + " ".join(ordered))
        image_path = os.path.join(DIAGRAMS, profile + ".png")
        if os.path.exists(image_path):
            with st.expander("Automaton diagram - " + label):
                st.image(image_path)

with tab4:
    st.subheader("Candidate profile")
    content = build_resume(name, location, extracted, tokens, labels)
    valid, model = validate_text(content)
    if valid:
        st.success("The .resume file is valid for the grammar.")
    else:
        st.error("The .resume file is not valid.")
        st.text(model)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**.resume file**")
        st.code(content, language="text")
        st.download_button("Download .resume", content, file_name="candidate.resume")
    with col2:
        if valid:
            markdown = generate_markdown(model)
            st.markdown("**Markdown report**")
            st.markdown(markdown)
            st.download_button("Download report", markdown, file_name="candidate.md")
