from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def analyze_resume(resume_text, job_description):

    resume_sentences = [s.strip() for s in resume_text.split('.') if s.strip()]
    job_sentences = [s.strip() for s in job_description.split('.') if s.strip()]

    resume_embeddings = model.encode(resume_sentences)
    job_embeddings = model.encode(job_sentences)

    analysis = []

    for i, job_emb in enumerate(job_embeddings):
        similarities = cosine_similarity([job_emb], resume_embeddings)[0]
        best_score = max(similarities)

        if best_score > 0.7:
            level = "Strong Match"
        elif best_score > 0.4:
            level = "Moderate Match"
        else:
            level = "Weak Match"

        analysis.append({
            "requirement": job_sentences[i],
            "score": float(best_score),
            "match": level
        })

    avg_score = sum([item["score"] for item in analysis]) / len(analysis)

    return {
        "details": analysis,
        "overall_score": avg_score
    }