from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import Job
from math import ceil


def recommend_jobs_from_db(
    user,
    db,
    page,
    limit,
    min_salary=None,
    max_salary=None,
    experience=None,
    skills=None
):
    jobs = db.query(Job).all()

    job_skills = [job.skills.replace(",", " ") for job in jobs]
    user_skills = user.skills.replace(",", " ")

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([user_skills] + job_skills)

    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])[0]

    filter_skills = skills.split(",") if skills else []

    filtered = []

    for i, score in enumerate(similarity_scores):
        job = jobs[i]

        if score < 0.25:
            continue

        if experience is not None and job.experience > experience:
            continue

        if min_salary is not None and job.salary < min_salary:
            continue

        if max_salary is not None and job.salary > max_salary:
            continue

        if filter_skills:
            if not set(filter_skills).intersection(job.skills.split(",")):
                continue

        filtered.append({
            "id": job.id,
            "title": job.title,
            "skills": job.skills.split(","),
            "education": job.education,
            "experience": job.experience,
            "description": job.description,
            "salary": job.salary,
            "score": round(score, 2)
        })

    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit

    return {
        "data": filtered[start:end],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": ceil(total / limit)
        }
    }
