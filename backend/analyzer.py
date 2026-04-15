def analyze_resume(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    common_words = resume_words.intersection(job_words)

    score = len(common_words) / (len(job_words) + 1)

    if score > 0.7:
        level = "Strong Match"
    elif score > 0.4:
        level = "Moderate Match"
    else:
        level = "Weak Match"

    return {
        "details": [{
            "requirement": job_description,
            "score": score,
            "match": level
        }],
        "overall_score": score
    }