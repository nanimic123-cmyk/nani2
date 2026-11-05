
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os
from pathlib import Path

# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATABASE = Path(__file__).resolve().parent / "careerpath.db"

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# CAREER REQUIREMENTS AND COURSE DATA
# --------------------------------------------------

CAREERS = {
    "Data Analyst": {
        "skills": [
            "SQL", "Excel", "Python", "Power BI", "Statistics"
        ],
        "courses": [
            {
                "name": "Google Data Analytics",
                "provider": "Google / Coursera",
                "level": "Beginner",
                "description": "Learn data analysis and visualization."
            },
            {
                "name": "SQL for Data Analysis",
                "provider": "Learning platform",
                "level": "Beginner",
                "description": "Learn SQL queries and databases."
            },
            {
                "name": "Power BI Data Analyst",
                "provider": "Microsoft Learn",
                "level": "Intermediate",
                "description": "Learn dashboards and business intelligence."
            }
        ],
        "certification": "Microsoft Power BI Data Analyst (PL-300)"
    },

    "Data Scientist": {
        "skills": [
            "Python", "SQL", "Statistics",
            "Machine Learning", "Data Visualization"
        ],
        "courses": [
            {
                "name": "Python for Data Science",
                "provider": "Learning platform",
                "level": "Beginner",
                "description": "Python programming and data handling."
            },
            {
                "name": "Machine Learning Specialization",
                "provider": "DeepLearning.AI / Coursera",
                "level": "Intermediate",
                "description": "Machine learning algorithms and models."
            },
            {
                "name": "Statistics for Data Science",
                "provider": "Learning platform",
                "level": "Intermediate",
                "description": "Statistical foundations for data science."
            }
        ],
        "certification": "IBM Data Science Professional Certificate"
    },

    "Software Developer": {
        "skills": [
            "Python", "Java", "Data Structures",
            "Problem Solving", "Git"
        ],
        "courses": [
            {
                "name": "Programming Fundamentals",
                "provider": "Learning platform",
                "level": "Beginner",
                "description": "Learn programming concepts."
            },
            {
                "name": "Data Structures and Algorithms",
                "provider": "Learning platform",
                "level": "Intermediate",
                "description": "Improve algorithmic problem solving."
            },
            {
                "name": "Git and GitHub",
                "provider": "GitHub Skills",
                "level": "Beginner",
                "description": "Learn version control."
            }
        ],
        "certification": "Oracle Java Certification"
    },

    "Web Developer": {
        "skills": [
            "HTML", "CSS", "JavaScript", "React", "Git"
        ],
        "courses": [
            {
                "name": "HTML and CSS Fundamentals",
                "provider": "Learning platform",
                "level": "Beginner",
                "description": "Website structure and styling."
            },
            {
                "name": "JavaScript Essentials",
                "provider": "Learning platform",
                "level": "Beginner",
                "description": "Interactive web development."
            },
            {
                "name": "React Development",
                "provider": "Learning platform",
                "level": "Intermediate",
                "description": "Modern frontend development."
            }
        ],
        "certification": "Meta Front-End Developer Certificate"
    },

    "Cybersecurity Analyst": {
        "skills": [
            "Networking", "Linux", "Python",
            "Security Basics", "Risk Analysis"
        ],
        "courses": [
            {
                "name": "Cybersecurity Fundamentals",
                "provider": "Cisco Networking Academy",
                "level": "Beginner",
                "description": "Learn security fundamentals."
            },
            {
                "name": "Linux Essentials",
                "provider": "Learning platform",
                "level": "Beginner",
                "description": "Learn Linux administration."
            },
            {
                "name": "Network Security",
                "provider": "Learning platform",
                "level": "Intermediate",
                "description": "Understand network protection."
            }
        ],
        "certification": "CompTIA Security+"
    },

    "Cloud Engineer": {
        "skills": [
            "Cloud Fundamentals", "Linux", "Networking",
            "Python", "Security Basics"
        ],
        "courses": [
            {
                "name": "Cloud Fundamentals",
                "provider": "Microsoft Learn",
                "level": "Beginner",
                "description": "Learn cloud computing concepts."
            },
            {
                "name": "AWS Cloud Practitioner Essentials",
                "provider": "AWS Skill Builder",
                "level": "Beginner",
                "description": "Understand AWS cloud services."
            },
            {
                "name": "Linux Administration",
                "provider": "Learning platform",
                "level": "Intermediate",
                "description": "Learn Linux and server basics."
            }
        ],
        "certification": "AWS Certified Cloud Practitioner"
    }
}

# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                education TEXT,
                degree TEXT,
                specialization TEXT,
                graduation_year TEXT,
                role TEXT NOT NULL,
                skills TEXT,
                soft_skills TEXT
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                UNIQUE(email, task)
            )
        """)


# --------------------------------------------------
# DATA HELPERS
# --------------------------------------------------

def student_to_dict(row):
    if not row:
        return None

    data = dict(row)
    data["skills"] = json.loads(data["skills"] or "[]")
    return data


def get_student(email):
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM students WHERE email = ?",
            (email,)
        ).fetchone()

    return student_to_dict(row)


def analyze_student(student):
    role = student.get("role")

    if role not in CAREERS:
        raise ValueError("Invalid career role.")

    required = CAREERS[role]["skills"]

    student_skills = {
        skill.strip().lower()
        for skill in student.get("skills", [])
    }

    matched = [
        skill for skill in required
        if skill.lower() in student_skills
    ]

    missing = [
        skill for skill in required
        if skill.lower() not in student_skills
    ]

    percentage = round(
        len(matched) / len(required) * 100
    )

    return {
        "role": role,
        "required_skills": required,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": percentage,
        "courses": CAREERS[role]["courses"],
        "certification": CAREERS[role]["certification"]
    }


# --------------------------------------------------
# FRONTEND HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# --------------------------------------------------
# HEALTH CHECK API
# --------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "CareerPath AI backend is running."
    })


# --------------------------------------------------
# STUDENT PROFILE API
# --------------------------------------------------

@app.route("/api/profile", methods=["GET"])
def get_profile():
    email = request.args.get("email", "").strip().lower()

    if not email:
        return jsonify({"error": "Email is required."}), 400

    student = get_student(email)

    if not student:
        return jsonify({"error": "Student not found."}), 404

    return jsonify(student)


@app.route("/api/profile", methods=["POST"])
def save_profile():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "name", "email", "education",
        "degree", "specialization", "role"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": f"{field} is required."
            }), 400

    email = data["email"].strip().lower()

    if "@" not in email:
        return jsonify({"error": "Invalid email address."}), 400

    if data["role"] not in CAREERS:
        return jsonify({"error": "Invalid career role."}), 400

    skills = data.get("skills", [])

    if not isinstance(skills, list):
        return jsonify({"error": "Skills must be a list."}), 400

    skills = [
        str(skill).strip()
        for skill in skills
        if str(skill).strip()
    ]

    with get_db() as db:
        db.execute("""
            INSERT INTO students (
                name, email, education, degree,
                specialization, graduation_year,
                role, skills, soft_skills
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(email) DO UPDATE SET
                name = excluded.name,
                education = excluded.education,
                degree = excluded.degree,
                specialization = excluded.specialization,
                graduation_year = excluded.graduation_year,
                role = excluded.role,
                skills = excluded.skills,
                soft_skills = excluded.soft_skills
        """, (
            data["name"].strip(),
            email,
            data["education"],
            data["degree"],
            data["specialization"],
            str(data.get("year", "")),
            data["role"],
            json.dumps(skills),
            data.get("softSkills", "")
        ))

    return jsonify({
        "status": "success",
        "message": "Student profile saved successfully.",
        "student": get_student(email)
    }), 201


# --------------------------------------------------
# CAREER ANALYSIS API
# --------------------------------------------------

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()

    if not email:
        return jsonify({"error": "Email is required."}), 400

    student = get_student(email)

    if not student:
        return jsonify({"error": "Register the student first."}), 404

    return jsonify({
        "status": "success",
        "student": {
            "name": student["name"],
            "role": student["role"]
        },
        "analysis": analyze_student(student)
    })


# --------------------------------------------------
# COURSE RECOMMENDATION API
# --------------------------------------------------

@app.route("/api/courses", methods=["GET"])
def get_courses():
    email = request.args.get("email", "").strip().lower()

    student = get_student(email) if email else None

    if not student:
        return jsonify({"error": "Student not found."}), 404

    analysis = analyze_student(student)

    return jsonify({
        "career": student["role"],
        "courses": analysis["courses"],
        "certification": analysis["certification"]
    })


# --------------------------------------------------
# LEARNING PATHWAY API
# --------------------------------------------------

@app.route("/api/pathway", methods=["GET"])
def get_pathway():
    email = request.args.get("email", "").strip().lower()

    student = get_student(email) if email else None

    if not student:
        return jsonify({"error": "Student not found."}), 404

    analysis = analyze_student(student)

    tasks = [
        "Learn " + skill
        for skill in analysis["missing_skills"]
    ]

    tasks.extend([
        "Course: " + course["name"]
        for course in analysis["courses"]
    ])

    tasks.append(
        "Certification: " + analysis["certification"]
    )

    with get_db() as db:
        rows = db.execute(
            "SELECT task, completed FROM progress WHERE email = ?",
            (email,)
        ).fetchall()

    saved = {
        row["task"]: bool(row["completed"])
        for row in rows
    }

    return jsonify({
        "career": student["role"],
        "tasks": [
            {
                "task": task,
                "completed": saved.get(task, False)
            }
            for task in tasks
        ]
    })


# --------------------------------------------------
# PROGRESS TRACKING API
# --------------------------------------------------

@app.route("/api/progress", methods=["GET"])
def get_progress():
    email = request.args.get("email", "").strip().lower()

    if not get_student(email):
        return jsonify({"error": "Student not found."}), 404

    with get_db() as db:
        rows = db.execute("""
            SELECT task, completed
            FROM progress
            WHERE email = ?
        """, (email,)).fetchall()

    tasks = [
        {
            "task": row["task"],
            "completed": bool(row["completed"])
        }
        for row in rows
    ]

    return jsonify({"progress": tasks})


@app.route("/api/progress", methods=["POST"])
def update_progress():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    task = data.get("task", "").strip()
    completed = data.get("completed")

    if not email or not task or not isinstance(completed, bool):
        return jsonify({
            "error": "Email, task and boolean completed value are required."
        }), 400

    if not get_student(email):
        return jsonify({"error": "Student not found."}), 404

    with get_db() as db:
        db.execute("""
            INSERT INTO progress (email, task, completed)
            VALUES (?, ?, ?)
            ON CONFLICT(email, task)
            DO UPDATE SET completed = excluded.completed
        """, (email, task, int(completed)))

    return jsonify({
        "status": "success",
        "message": "Learning progress updated."
    })


# --------------------------------------------------
# DASHBOARD API
# --------------------------------------------------

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    email = request.args.get("email", "").strip().lower()

    student = get_student(email) if email else None

    if not student:
        return jsonify({"error": "Student not found."}), 404

    analysis = analyze_student(student)

    with get_db() as db:
        row = db.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(completed) AS done
            FROM progress
            WHERE email = ?
        """, (email,)).fetchone()

    total = row["total"] or 0
    done = row["done"] or 0

    progress_percentage = (
        round(done / total * 100) if total else 0
    )

    return jsonify({
        "student_name": student["name"],
        "career": student["role"],
        "career_match": analysis["match_percentage"],
        "matched_skills": len(analysis["matched_skills"]),
        "missing_skills": len(analysis["missing_skills"]),
        "learning_progress": progress_percentage
    })


# --------------------------------------------------
# START SERVER
# --------------------------------------------------

if __name__ == "__main__":
    initialize_database()

    print("CareerPath AI backend starting...")
    print("Open http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
