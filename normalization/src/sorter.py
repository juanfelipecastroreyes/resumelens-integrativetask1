PROFILE_ORDER = {
    "full_stack": [
        "JAVASCRIPT", "TYPESCRIPT", "JAVA", "PYTHON",
        "HTML", "CSS", "REACT", "ANGULAR", "VUE",
        "NODE_JS", "EXPRESS", "SPRING_BOOT", "DJANGO", "FLASK", "REST_API",
        "SQL", "POSTGRESQL", "MYSQL", "MONGODB",
        "DOCKER", "AWS", "CI_CD",
        "GIT",
    ],
    "ml_engineer": [
        "PYTHON", "R_LANG", "SQL", "POSTGRESQL", "MYSQL",
        "PANDAS", "NUMPY",
        "SCIKIT_LEARN", "TENSORFLOW", "PYTORCH", "KERAS",
        "MACHINE_LEARNING", "DEEP_LEARNING", "NLP", "COMPUTER_VISION",
        "MLOPS",
        "DOCKER", "AWS",
        "GIT",
    ],
    "data_scientist": [
        "PYTHON", "R_LANG", "SQL", "POSTGRESQL", "MYSQL",
        "PANDAS", "NUMPY",
        "SCIKIT_LEARN", "MACHINE_LEARNING", "DEEP_LEARNING", "NLP", "COMPUTER_VISION",
        "TENSORFLOW", "PYTORCH", "KERAS",
        "GIT",
    ],
    "cloud_engineer": [
        "LINUX", "PYTHON",
        "AWS", "AZURE", "GCP",
        "DOCKER", "KUBERNETES",
        "TERRAFORM", "CI_CD",
        "GIT",
    ],
}

def sort_tokens(tokens, profile):
    order = PROFILE_ORDER[profile]
    sorted_tokens = []
    for token in order:
        if token in tokens:
            sorted_tokens.append(token)
    others = []
    for token in tokens:
        if token not in order:
            others.append(token)
    return sorted_tokens + others
