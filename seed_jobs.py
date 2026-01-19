import random
from database import SessionLocal
from models import Job

db = SessionLocal()

job_titles = [
    "Python Developer", "Backend Developer", "Software Engineer",
    "Data Analyst", "ML Engineer", "Web Developer",
    "Full Stack Developer", "Junior Developer", "Senior Engineer",
    "Frontend Developer", "Database Administrator",
    "Cloud Engineer", "DevOps Engineer", "AI Engineer",
    "Cyber Security Analyst", "Network Engineer",
    "Mobile App Developer", "System Administrator",
    "IT Support Engineer", "Business Intelligence Analyst"
]

skills_pool = [
    "HTML", "Bootstrap", "PHP", "C", "MySQL", "Linux",
    "Machine Learning", "Excel", "CSS", "React",
    "Python", "C++", "MongoDB", "Networking",
    "Artificial Intelligence", "AWS", "JavaScript",
    "Node.js", "Java", "Git", "Cyber Security",
    "Data Analysis", "Docker"
]

educations = [
    "Matric",
    "Intermediate",
    "Bachelors",
    "Masters",
    "PHD"
]

descriptions = [
    "Responsible for developing backend applications.",
    "Work with databases and APIs.",
    "Collaborate with cross-functional teams.",
    "Maintain scalable systems.",
    "Analyze and optimize performance.",
    "Design and implement secure software solutions.",
    "Participate in system architecture planning.",
    "Ensure application performance and scalability.",
    "Write clean, maintainable, and efficient code.",
    "Troubleshoot and debug production issues."
]

salaries = [
    50000,
    80000,
    15000,
    30000,
    100000,
    110000,
    60000
]

def seed_unique_jobs(total_jobs=550):
    jobs = []
    used_titles = set()

    index = 1
    while len(jobs) < total_jobs:
        base_title = random.choice(job_titles)
        unique_title = f"{base_title} Level {index}"

        if unique_title in used_titles:
            index += 1
            continue

        used_titles.add(unique_title)

        skills = ", ".join(random.sample(skills_pool, random.randint(3, 6)))
        education = random.choice(educations)
        experience = random.randint(0, 8)
        description = random.choice(descriptions)
        salary = random.choice(salaries)

        job = Job(
            title=unique_title,
            skills=skills,
            education=education,
            experience=experience,
            description=description,
            salary=salary
        )

        jobs.append(job)
        index += 1

    db.add_all(jobs)
    db.commit()
    db.close()

    print(f"✅ {total_jobs} UNIQUE jobs inserted successfully!")

seed_unique_jobs()
