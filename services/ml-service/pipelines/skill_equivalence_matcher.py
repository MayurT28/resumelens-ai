from sentence_transformers import SentenceTransformer, util

# Load once globally
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def find_semantic_skill_matches(resume_skills, jd_skills, threshold=0.65):
    """
    Match resume skills to JD skills using embedding similarity.
    """

    if not resume_skills or not jd_skills:
        return []

    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)

    similarity_matrix = util.cos_sim(resume_embeddings, jd_embeddings)

    matches = []

    for i, resume_skill in enumerate(resume_skills):
        for j, jd_skill in enumerate(jd_skills):

            similarity_score = similarity_matrix[i][j].item()

            if similarity_score >= threshold:

                matches.append({
                    "resume_skill": resume_skill,
                    "jd_skill": jd_skill,
                    "similarity": round(similarity_score, 3)
                })

    return matches