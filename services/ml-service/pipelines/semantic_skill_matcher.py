from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from models.embedding_model import MODEL as model



def find_semantic_skill_matches(resume_skills, jd_skills, threshold=0.6):
    """
    Finds semantically similar skills between resume and job description.
    Returns list of matched skill pairs.
    """

    matches = []

    if not resume_skills or not jd_skills:
        return matches

    resume_embeddings = model.encode(resume_skills)
    jd_embeddings = model.encode(jd_skills)

    for i, r_emb in enumerate(resume_embeddings):
        for j, j_emb in enumerate(jd_embeddings):
            similarity = cosine_similarity([r_emb], [j_emb])[0][0]

            if similarity >= threshold and resume_skills[i] != jd_skills[j]:
                matches.append(
                    {
                        "resume_skill": resume_skills[i],
                        "jd_skill": jd_skills[j],
                        "similarity": round(float(similarity), 3)
                    }
                )

    return matches