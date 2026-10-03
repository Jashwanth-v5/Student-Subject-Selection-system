from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import random
import os

app = Flask(__name__)

DATABASE = "college.db"

COLLEGE_NAME = "MALLA REDDY VISHWA VIDYAPEETH"

# ---------------------------------------------------------
# COURSE DATA
# ---------------------------------------------------------

COURSES = {
    "AIML": [
        ("Artificial Intelligence", 4, 5, 95),
        ("Machine Learning", 4, 5, 92),
        ("Deep Learning", 4, 5, 90),
        ("Data Mining", 4, 4, 88),
        ("Natural Language Processing", 3, 4, 91),
        ("Computer Vision", 3, 4, 87)
    ],

    "CSE-GENERAL": [
        ("Data Structures", 4, 5, 95),
        ("Database Management Systems", 4, 5, 93),
        ("Operating Systems", 4, 5, 90),
        ("Computer Networks", 4, 4, 88),
        ("Software Engineering", 3, 4, 85),
        ("Web Technologies", 3, 4, 89)
    ],

    "CSE-DS": [
        ("Data Science", 4, 5, 95),
        ("Statistics for Data Science", 4, 4, 90),
        ("Big Data Analytics", 4, 5, 92),
        ("Data Visualization", 3, 3, 88),
        ("Predictive Analytics", 3, 4, 91),
        ("Data Mining", 4, 5, 89)
    ],

    "IOT": [
        ("Internet of Things", 4, 5, 95),
        ("Embedded Systems", 4, 5, 90),
        ("Sensors and Actuators", 3, 4, 87),
        ("IoT Communication", 3, 4, 85),
        ("Cloud IoT", 4, 5, 92),
        ("IoT Security", 3, 4, 88)
    ],

    "IT": [
        ("Information Technology Fundamentals", 4, 4, 90),
        ("Cloud Computing", 4, 5, 94),
        ("Cyber Security", 4, 5, 96),
        ("Web Development", 3, 4, 89),
        ("Mobile Application Development", 3, 4, 88),
        ("IT Service Management", 3, 3, 82)
    ],

    "ECE": [
        ("Digital Electronics", 4, 5, 92),
        ("Microprocessors", 4, 5, 90),
        ("Communication Systems", 4, 5, 91),
        ("Signal Processing", 4, 5, 88),
        ("VLSI Design", 3, 4, 89),
        ("Embedded Systems", 3, 4, 93)
    ],

    "EEE": [
        ("Electrical Machines", 4, 5, 92),
        ("Power Systems", 4, 5, 94),
        ("Control Systems", 4, 4, 90),
        ("Power Electronics", 4, 5, 91),
        ("Electrical Measurements", 3, 4, 86),
        ("Renewable Energy Systems", 3, 4, 89)
    ],

    "Mechanical": [
        ("Engineering Mechanics", 4, 5, 90),
        ("Thermodynamics", 4, 5, 92),
        ("Fluid Mechanics", 4, 5, 88),
        ("Machine Design", 4, 5, 94),
        ("Manufacturing Technology", 3, 4, 89),
        ("Robotics and Automation", 3, 4, 95)
    ]
}


# ---------------------------------------------------------
# STUDENT NAMES
# ---------------------------------------------------------

FIRST_NAMES = [
    "Aarav", "Aditi", "Arjun", "Ananya", "Aditya",
    "Rahul", "Riya", "Rohan", "Sneha", "Kiran",
    "Varun", "Pooja", "Sai", "Sanjana", "Vishal",
    "Neha", "Nikhil", "Harsha", "Pranav", "Kavya",
    "Manoj", "Keerthi", "Akash", "Divya", "Teja",
    "Abhinav", "Bhavya", "Charan", "Deepak", "Ishita",
    "Lokesh", "Meghana", "Naveen", "Pallavi", "Sandeep",
    "Shreya", "Tarun", "Vaishnavi", "Yash", "Zoya",
    "Madhav", "Sowmya", "Vivek", "Lavanya", "Rakesh",
    "Anil", "Swathi", "Karthik", "Nandini", "Ravi"
]

LAST_NAMES = [
    "Reddy", "Kumar", "Sharma", "Patel", "Rao",
    "Varma", "Naidu", "Chowdary", "Singh", "Verma"
]

SECTIONS = ["A", "B", "C", "D"]


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT,
            name TEXT,
            credits INTEGER,
            workload INTEGER,
            preference INTEGER,
            importance TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT,
            section TEXT,
            name TEXT,
            roll_no TEXT,
            email TEXT,
            phone TEXT,
            year TEXT,
            marks INTEGER,
            attendance INTEGER,
            feedback TEXT
        )
    """)

    conn.commit()

    # -----------------------------------------------------
    # ADD SUBJECTS
    # -----------------------------------------------------

    count = cur.execute(
        "SELECT COUNT(*) FROM subjects"
    ).fetchone()[0]

    if count == 0:

        for course, subjects in COURSES.items():

            for subject in subjects:

                importance = (
                    f"{subject[0]} is an important subject for {course} "
                    "students because it develops technical knowledge, "
                    "problem-solving ability and industry-oriented skills."
                )

                cur.execute("""
                    INSERT INTO subjects
                    (course, name, credits, workload, preference, importance)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    course,
                    subject[0],
                    subject[1],
                    subject[2],
                    subject[3],
                    importance
                ))

    # -----------------------------------------------------
    # ADD STUDENTS
    # 50 students for every course
    # -----------------------------------------------------

    student_count = cur.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    if student_count == 0:

        random.seed(20)

        student_id = 1

        for course in COURSES:

            for i in range(50):

                first = FIRST_NAMES[i % len(FIRST_NAMES)]
                last = LAST_NAMES[(i // len(FIRST_NAMES)) % len(LAST_NAMES)]

                name = f"{first} {last}"

                section = SECTIONS[i % len(SECTIONS)]

                roll_no = (
                    f"MRV-{course[:3].upper()}-"
                    f"{2026}-{i+1:03d}"
                )

                email = (
                    f"{first.lower()}.{last.lower()}"
                    f"{i+1}@mrvv.edu.in"
                )

                phone = f"9{random.randint(100000000,999999999)}"

                marks = random.randint(55, 98)

                attendance = random.randint(75, 99)

                feedback = random.choice([
                    "The subject is very useful and interesting.",
                    "The subject helped me improve my technical skills.",
                    "The concepts are useful for placements and projects.",
                    "I enjoyed learning this subject.",
                    "The practical sessions were very helpful.",
                    "The subject improved my problem-solving skills."
                ])

                cur.execute("""
                    INSERT INTO students
                    (course, section, name, roll_no, email,
                     phone, year, marks, attendance, feedback)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    course,
                    section,
                    name,
                    roll_no,
                    email,
                    phone,
                    "2026-27",
                    marks,
                    attendance,
                    feedback
                ))

                student_id += 1

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# 0/1 KNAPSACK + DYNAMIC PROGRAMMING
# ---------------------------------------------------------

def optimize_subjects(subjects, max_credits=12, max_workload=15):

    n = len(subjects)

    # dp[i][c][w] = maximum preference score
    dp = [
        [
            [0 for _ in range(max_workload + 1)]
            for _ in range(max_credits + 1)
        ]
        for _ in range(n + 1)
    ]

    # Build DP table
    for i in range(1, n + 1):

        subject = subjects[i - 1]

        credits = subject["credits"]
        workload = subject["workload"]
        preference = subject["preference"]

        for c in range(max_credits + 1):

            for w in range(max_workload + 1):

                # Do not select subject
                dp[i][c][w] = dp[i - 1][c][w]

                # Select subject
                if c >= credits and w >= workload:

                    selected_score = (
                        dp[i - 1][c - credits][w - workload]
                        + preference
                    )

                    if selected_score > dp[i][c][w]:
                        dp[i][c][w] = selected_score

    # -----------------------------------------------------
    # RECONSTRUCT SELECTED SUBJECTS
    # -----------------------------------------------------

    selected = []

    c = max_credits
    w = max_workload

    for i in range(n, 0, -1):

        if dp[i][c][w] != dp[i - 1][c][w]:

            subject = subjects[i - 1]

            selected.append(subject)

            c -= subject["credits"]
            w -= subject["workload"]

    selected.reverse()

    selected_ids = {
        s["id"] for s in selected
    }

    rejected = [
        s for s in subjects
        if s["id"] not in selected_ids
    ]

    total_credits = sum(
        s["credits"] for s in selected
    )

    total_workload = sum(
        s["workload"] for s in selected
    )

    total_score = sum(
        s["preference"] for s in selected
    )

    return {
        "selected": selected,
        "rejected": rejected,
        "credits": total_credits,
        "workload": total_workload,
        "score": total_score,
        "max_score": dp[n][max_credits][max_workload],
        "states": (n + 1) * (max_credits + 1) * (max_workload + 1)
    }


# ---------------------------------------------------------
# BASE TEMPLATE
# ---------------------------------------------------------

BASE = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{{ title }} | MRVV</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet">

<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<style>

body {
    background: #f5f8fc;
    font-family: Arial, sans-serif;
}

.navbar {
    background: linear-gradient(135deg,#062e61,#0879c9);
    box-shadow: 0 4px 15px rgba(0,0,0,.15);
}

.navbar-brand {
    font-weight: 800;
    letter-spacing: .5px;
}

.nav-link {
    color: white !important;
    font-weight: 600;
    margin-left: 8px;
}

.hero {
    min-height: 520px;
    display:flex;
    align-items:center;
    background:
    linear-gradient(135deg,rgba(4,42,89,.94),rgba(0,119,190,.85)),
    url("https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1600&q=80");
    background-size:cover;
    background-position:center;
    color:white;
}

.hero h1 {
    font-size: clamp(38px,6vw,70px);
    font-weight:900;
}

.hero p {
    font-size:20px;
}

.btn-main {
    background:white;
    color:#075ca8;
    border:none;
    font-weight:700;
    padding:12px 25px;
    border-radius:30px;
}

.section-title {
    font-weight:800;
    color:#073b70;
}

.card {
    border:none;
    border-radius:18px;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
    transition:.3s;
}

.card:hover {
    transform:translateY(-7px);
    box-shadow:0 15px 35px rgba(0,0,0,.14);
}

.course-card {
    cursor:pointer;
    min-height:210px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.course-icon {
    font-size:50px;
    color:#0879c9;
}

.subject-card {
    cursor:pointer;
}

.student-card {
    cursor:pointer;
}

.page-header {
    background:linear-gradient(135deg,#073b70,#0793dc);
    color:white;
    padding:55px 0;
}

.badge-custom {
    background:#e8f4ff;
    color:#0765ae;
    padding:8px 14px;
    border-radius:20px;
}

.stat {
    font-size:32px;
    font-weight:800;
    color:#086bb5;
}

.animate {
    animation:fadeUp .7s ease both;
}

@keyframes fadeUp {
    from {
        opacity:0;
        transform:translateY(25px);
    }

    to {
        opacity:1;
        transform:translateY(0);
    }
}

.course-card:nth-child(2) {
    animation-delay:.08s;
}

.course-card:nth-child(3) {
    animation-delay:.16s;
}

.course-card:nth-child(4) {
    animation-delay:.24s;
}

.course-card:nth-child(5) {
    animation-delay:.32s;
}

.course-card:nth-child(6) {
    animation-delay:.40s;
}

.course-card:nth-child(7) {
    animation-delay:.48s;
}

.course-card:nth-child(8) {
    animation-delay:.56s;
}

footer {
    background:#062e61;
    color:white;
    padding:30px;
}

table {
    background:white;
}

</style>

</head>

<body>

<nav class="navbar navbar-expand-lg navbar-dark sticky-top">

<div class="container">

<a class="navbar-brand" href="/">
<i class="bi bi-mortarboard-fill"></i>
MRVV
</a>

<button class="navbar-toggler"
data-bs-toggle="collapse"
data-bs-target="#nav">
<span class="navbar-toggler-icon"></span>
</button>

<div class="collapse navbar-collapse" id="nav">

<ul class="navbar-nav ms-auto">

<li class="nav-item">
<a class="nav-link" href="/">
<i class="bi bi-house"></i> Home
</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/courses">
<i class="bi bi-book"></i> Courses
</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/fees">
<i class="bi bi-cash-stack"></i> Fees
</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/students">
<i class="bi bi-people"></i> Student Details
</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/optimizer">
<i class="bi bi-cpu"></i> DAA Optimizer
</a>
</li>

</ul>

</div>
</div>
</nav>

{{ content|safe }}

<footer class="mt-5">

<div class="container text-center">

<h5>{{ college }}</h5>

<p class="mb-0">
Student Subject Selection System |
0/1 Knapsack + Dynamic Programming
</p>

<p class="small mt-2">
Academic Portal Prototype
</p>

</div>

</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
"""


def render_page(title, content, **kwargs):

    return render_template_string(
        BASE,
        title=title,
        content=content,
        college=COLLEGE_NAME,
        **kwargs
    )


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
def home():

    conn = get_db()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_subjects = conn.execute(
        "SELECT COUNT(*) FROM subjects"
    ).fetchone()[0]

    conn.close()

    content = """

<section class="hero">

<div class="container">

<div class="row">

<div class="col-lg-8 animate">

<span class="badge bg-light text-primary mb-3">
Academic Student Portal
</span>

<h1>MALLA REDDY<br>VISHWA VIDYAPEETH</h1>

<p>
Welcome to the Student Academic Management and
Subject Selection System.
</p>

<p>
Explore courses, subjects, student performance,
fees and intelligent subject selection using
0/1 Knapsack and Dynamic Programming.
</p>

<a href="/courses" class="btn btn-main mt-3">
Explore Courses <i class="bi bi-arrow-right"></i>
</a>

</div>

</div>

</div>

</section>


<section class="py-5">

<div class="container">

<div class="text-center mb-5">

<h2 class="section-title">
Our Academic Portal
</h2>

<p class="text-muted">
A centralized platform for students and academic management.
</p>

</div>


<div class="row g-4">

<div class="col-md-4">

<div class="card p-4 text-center">

<i class="bi bi-book-half course-icon"></i>

<h4 class="mt-3">Courses & Subjects</h4>

<p>
Explore different engineering courses
and their subjects.
</p>

<a href="/courses" class="btn btn-outline-primary">
View Courses
</a>

</div>

</div>


<div class="col-md-4">

<div class="card p-4 text-center">

<i class="bi bi-people-fill course-icon"></i>

<h4 class="mt-3">Student Information</h4>

<p>
View student profiles, marks,
attendance and feedback.
</p>

<a href="/students" class="btn btn-outline-primary">
Student Details
</a>

</div>

</div>


<div class="col-md-4">

<div class="card p-4 text-center">

<i class="bi bi-cpu-fill course-icon"></i>

<h4 class="mt-3">Smart Subject Selection</h4>

<p>
Select subjects using
Dynamic Programming optimization.
</p>

<a href="/optimizer" class="btn btn-outline-primary">
Run Optimizer
</a>

</div>

</div>

</div>


<div class="row mt-5 g-4 text-center">

<div class="col-md-6">

<div class="card p-4">

<div class="stat">
""" + str(total_students) + """+
</div>

<p class="mb-0">Student Records</p>

</div>

</div>


<div class="col-md-6">

<div class="card p-4">

<div class="stat">
""" + str(total_subjects) + """
</div>

<p class="mb-0">Subjects</p>

</div>

</div>

</div>

</div>

</section>
"""

    return render_page("Home", content)


# ---------------------------------------------------------
# COURSES
# ---------------------------------------------------------

@app.route("/courses")
def courses():

    icons = [
        "bi-robot",
        "bi-code-slash",
        "bi-bar-chart-fill",
        "bi-cpu-fill",
        "bi-cloud-fill",
        "bi-broadcast",
        "bi-lightning-charge-fill",
        "bi-gear-fill"
    ]

    html = """

<section class="page-header">

<div class="container text-center">

<h1>Academic Courses</h1>

<p>
Explore our undergraduate engineering programmes
</p>

</div>

</section>

<div class="container py-5">

<div class="row g-4">
"""

    for index, course in enumerate(COURSES):

        html += f"""

<div class="col-md-6 col-lg-3 animate">

<a href="/course/{course}"
style="text-decoration:none;color:inherit">

<div class="card course-card text-center p-4">

<i class="bi {icons[index]} course-icon"></i>

<h4 class="mt-3">
{course}
</h4>

<p class="text-muted">
6 Academic Subjects
</p>

<span class="badge-custom">
View Subjects →
</span>

</div>

</a>

</div>
"""

    html += """

</div>

</div>
"""

    return render_page("Courses", html)


# ---------------------------------------------------------
# COURSE SUBJECTS
# ---------------------------------------------------------

@app.route("/course/<course>")
def course_page(course):

    if course not in COURSES:
        return "Course not found", 404

    conn = get_db()

    subjects = conn.execute("""
        SELECT * FROM subjects
        WHERE course=?
    """, (course,)).fetchall()

    conn.close()

    html = f"""

<section class="page-header">

<div class="container">

<h1>{course}</h1>

<p>
Six subjects offered under the {course} programme.
</p>

</div>

</section>


<div class="container py-5">

<div class="row g-4">
"""

    for subject in subjects:

        html += f"""

<div class="col-md-6 col-lg-4">

<a href="/subject/{subject['id']}"
style="text-decoration:none;color:inherit">

<div class="card subject-card p-4 h-100">

<div class="d-flex justify-content-between">

<i class="bi bi-journal-code course-icon"></i>

<span class="badge-custom">
{subject['credits']} Credits
</span>

</div>

<h4 class="mt-4">
{subject['name']}
</h4>

<p class="text-muted">
Workload: {subject['workload']}
</p>

<p>
Preference Score:
<strong>{subject['preference']}</strong>
</p>

<span class="text-primary">
View Students →
</span>

</div>

</a>

</div>
"""

    html += """

</div>

<div class="text-center mt-5">

<a href="/optimizer"
class="btn btn-primary btn-lg">

<i class="bi bi-cpu"></i>
Use This Data in DAA Optimizer

</a>

</div>

</div>
"""

    return render_page(course, html)


# ---------------------------------------------------------
# SUBJECT PAGE
# ---------------------------------------------------------

@app.route("/subject/<int:subject_id>")
def subject_page(subject_id):

    conn = get_db()

    subject = conn.execute(
        "SELECT * FROM subjects WHERE id=?",
        (subject_id,)
    ).fetchone()

    if not subject:
        conn.close()
        return "Subject not found", 404

    students = conn.execute("""
        SELECT * FROM students
        WHERE course=?
        ORDER BY section, name
        LIMIT 25
    """, (subject["course"],)).fetchall()

    conn.close()

    html = f"""

<section class="page-header">

<div class="container">

<span class="badge bg-light text-primary">
{subject['course']}
</span>

<h1 class="mt-3">
{subject['name']}
</h1>

<p>
Subject information and student performance
</p>

</div>

</section>


<div class="container py-5">

<div class="row g-4">

<div class="col-lg-8">

<div class="card p-4">

<h3>
<i class="bi bi-info-circle"></i>
Subject Overview
</h3>

<hr>

<p>
<strong>Course:</strong>
{subject['course']}
</p>

<p>
<strong>Credits:</strong>
{subject['credits']}
</p>

<p>
<strong>Workload:</strong>
{subject['workload']}
</p>

<p>
<strong>Academic Preference Score:</strong>
{subject['preference']}
</p>

<h5 class="mt-4">
Importance of this Subject
</h5>

<p class="text-muted">
{subject['importance']}
</p>

</div>

</div>


<div class="col-lg-4">

<div class="card p-4 text-center">

<i class="bi bi-people-fill course-icon"></i>

<h4>
Students
</h4>

<p>
View student performance and feedback
for this course.
</p>

<a href="/students/course/{subject['course']}"
class="btn btn-primary">

View All Students

</a>

</div>

</div>

</div>


<div class="card mt-5 p-4">

<h3>
Student Performance
</h3>

<p class="text-muted">
More than 20 students are displayed for this subject.
Click a student to view complete details.
</p>

<div class="table-responsive">

<table class="table table-hover align-middle">

<thead class="table-primary">

<tr>
<th>Name</th>
<th>Roll Number</th>
<th>Section</th>
<th>Marks</th>
<th>Attendance</th>
<th>Details</th>
</tr>

</thead>

<tbody>
"""

    for student in students:

        html += f"""

<tr>

<td>
<strong>{student['name']}</strong>
</td>

<td>
{student['roll_no']}
</td>

<td>
<span class="badge bg-primary">
{student['section']}
</span>
</td>

<td>
<strong>{student['marks']}</strong>/100
</td>

<td>
{student['attendance']}%
</td>

<td>

<a href="/student/{student['id']}"
class="btn btn-sm btn-outline-primary">

View

</a>

</td>

</tr>
"""

    html += """

</tbody>

</table>

</div>

</div>

</div>
"""

    return render_page(subject["name"], html)


# ---------------------------------------------------------
# STUDENT DETAILS HOME
# ---------------------------------------------------------

@app.route("/students")
def students_home():

    html = """

<section class="page-header">

<div class="container text-center">

<h1>Student Details</h1>

<p>
Select a course to view sections and students.
</p>

</div>

</section>


<div class="container py-5">

<div class="row g-4">
"""

    for course in COURSES:

        html += f"""

<div class="col-md-6 col-lg-3">

<a href="/students/course/{course}"
style="text-decoration:none;color:inherit">

<div class="card course-card text-center p-4">

<i class="bi bi-person-vcard course-icon"></i>

<h4 class="mt-3">
{course}
</h4>

<p class="text-muted">
Sections A, B, C & D
</p>

<span class="badge-custom">
View Students →
</span>

</div>

</a>

</div>
"""

    html += """

</div>

</div>
"""

    return render_page("Student Details", html)


# ---------------------------------------------------------
# STUDENTS BY COURSE
# ---------------------------------------------------------

@app.route("/students/course/<course>")
def students_course(course):

    if course not in COURSES:
        return "Course not found", 404

    conn = get_db()

    students = conn.execute("""
        SELECT * FROM students
        WHERE course=?
        ORDER BY section, name
    """, (course,)).fetchall()

    conn.close()

    html = f"""

<section class="page-header">

<div class="container">

<h1>{course}</h1>

<p>
Student records grouped by section.
</p>

</div>

</section>


<div class="container py-5">

"""

    for section in SECTIONS:

        section_students = [
            s for s in students
            if s["section"] == section
        ]

        html += f"""

<div class="card mb-5 p-4">

<div class="d-flex justify-content-between
align-items-center mb-3">

<div>

<h3>
Section {section}
</h3>

<p class="text-muted mb-0">
{len(section_students)} students
</p>

</div>

<span class="badge bg-primary fs-6">
{course} - {section}
</span>

</div>

<div class="table-responsive">

<table class="table table-hover">

<thead class="table-primary">

<tr>

<th>Name</th>
<th>Roll Number</th>
<th>Email</th>
<th>Marks</th>
<th>Attendance</th>
<th></th>

</tr>

</thead>

<tbody>
"""

        for student in section_students:

            html += f"""

<tr>

<td>
<strong>{student['name']}</strong>
</td>

<td>
{student['roll_no']}
</td>

<td>
{student['email']}
</td>

<td>
{student['marks']}
</td>

<td>
{student['attendance']}%
</td>

<td>

<a href="/student/{student['id']}"
class="btn btn-sm btn-outline-primary">

Details

</a>

</td>

</tr>
"""

        html += """

</tbody>

</table>

</div>

</div>

"""

    html += """

</div>
"""

    return render_page(
        f"{course} Students",
        html
    )


# ---------------------------------------------------------
# INDIVIDUAL STUDENT
# ---------------------------------------------------------

@app.route("/student/<int:student_id>")
def student_page(student_id):

    conn = get_db()

    student = conn.execute("""
        SELECT * FROM students
        WHERE id=?
    """, (student_id,)).fetchone()

    conn.close()

    if not student:
        return "Student not found", 404

    html = f"""

<section class="page-header">

<div class="container">

<h1>
Student Profile
</h1>

<p>
Complete academic information
</p>

</div>

</section>


<div class="container py-5">

<div class="row justify-content-center">

<div class="col-lg-9">

<div class="card p-5">

<div class="text-center mb-4">

<div style="
width:110px;
height:110px;
border-radius:50%;
background:#e5f3ff;
display:flex;
align-items:center;
justify-content:center;
margin:auto;
">

<i class="bi bi-person-fill"
style="font-size:65px;color:#0879c9"></i>

</div>

<h2 class="mt-3">
{student['name']}
</h2>

<span class="badge bg-primary">
{student['course']}
</span>

<span class="badge bg-secondary">
Section {student['section']}
</span>

</div>


<div class="row g-4">

<div class="col-md-6">

<div class="card p-3 bg-light">

<strong>
Roll Number
</strong>

<p class="mb-0">
{student['roll_no']}
</p>

</div>

</div>


<div class="col-md-6">

<div class="card p-3 bg-light">

<strong>
Email
</strong>

<p class="mb-0">
{student['email']}
</p>

</div>

</div>


<div class="col-md-6">

<div class="card p-3 bg-light">

<strong>
Phone
</strong>

<p class="mb-0">
{student['phone']}
</p>

</div>

</div>


<div class="col-md-6">

<div class="card p-3 bg-light">

<strong>
Academic Year
</strong>

<p class="mb-0">
{student['year']}
</p>

</div>

</div>

</div>


<hr class="my-5">


<div class="row text-center g-4">

<div class="col-md-6">

<div class="card p-4">

<div class="stat">
{student['marks']}/100
</div>

<p>
Academic Marks
</p>

</div>

</div>


<div class="col-md-6">

<div class="card p-4">

<div class="stat">
{student['attendance']}%
</div>

<p>
Attendance
</p>

</div>

</div>

</div>


<div class="mt-5">

<h4>
<i class="bi bi-chat-quote"></i>
Student Feedback
</h4>

<div class="alert alert-info mt-3">

"{student['feedback']}"

</div>

</div>


<div class="mt-4">

<h4>
<i class="bi bi-lightbulb"></i>
Academic Information
</h4>

<p class="text-muted">

The student's academic performance, attendance
and feedback can be used by faculty and
administrators to understand student engagement
and subject preferences.

</p>

</div>

</div>

</div>

</div>

</div>
"""

    return render_page(
        student["name"],
        html
    )


# ---------------------------------------------------------
# FEES
# ---------------------------------------------------------

@app.route("/fees")
def fees():

    fee_data = {
        "AIML": "₹1,50,000",
        "CSE-GENERAL": "₹1,45,000",
        "CSE-DS": "₹1,50,000",
        "IOT": "₹1,40,000",
        "IT": "₹1,40,000",
        "ECE": "₹1,35,000",
        "EEE": "₹1,30,000",
        "Mechanical": "₹1,25,000"
    }

    html = """

<section class="page-header">

<div class="container text-center">

<h1>Course Fees</h1>

<p>
Academic fee overview
</p>

</div>

</section>


<div class="container py-5">

<div class="row g-4">
"""

    for course, fee in fee_data.items():

        html += f"""

<div class="col-md-6 col-lg-3">

<div class="card p-4 text-center">

<i class="bi bi-wallet2 course-icon"></i>

<h4 class="mt-3">
{course}
</h4>

<h3 class="text-primary">
{fee}
</h3>

<p class="text-muted">
Approximate annual fee
</p>

<button class="btn btn-outline-primary">
View Fee Details
</button>

</div>

</div>
"""

    html += """

</div>


<div class="alert alert-warning mt-5">

<strong>Note:</strong>
The fee values shown here are prototype/demo
values for the project. Actual institutional
fees can be connected to the database.

</div>

</div>
"""

    return render_page("Fees", html)


# ---------------------------------------------------------
# DAA OPTIMIZER
# ---------------------------------------------------------

@app.route("/optimizer")
def optimizer():

    conn = get_db()

    subjects = conn.execute("""
        SELECT * FROM subjects
        ORDER BY course, preference DESC
    """).fetchall()

    conn.close()

    html = """

<section class="page-header">

<div class="container">

<h1>
Smart Subject Selection
</h1>

<p>
0/1 Knapsack + Dynamic Programming
</p>

</div>

</section>


<div class="container py-5">

<div class="card p-4 mb-5">

<h3>
Problem Configuration
</h3>

<p class="text-muted">

The algorithm selects subjects so that the
total credits and workload remain within
the student's limits while maximizing the
academic preference score.

</p>

<form method="POST"
action="/optimizer/run">

<div class="row">

<div class="col-md-4">

<label class="form-label">
Maximum Credits
</label>

<input type="number"
name="max_credits"
value="12"
min="1"
class="form-control">

</div>


<div class="col-md-4">

<label class="form-label">
Maximum Workload
</label>

<input type="number"
name="max_workload"
value="15"
min="1"
class="form-control">

</div>


<div class="col-md-4 d-flex align-items-end">

<button class="btn btn-primary w-100">

<i class="bi bi-cpu"></i>

Run Dynamic Programming

</button>

</div>

</div>

</form>

</div>


<div class="row g-4">

<div class="col-md-4">

<div class="card p-4 text-center">

<div class="stat">
{}</div>

<p>
Available Subjects
</p>

</div>

</div>


<div class="col-md-4">

<div class="card p-4 text-center">

<div class="stat">
0/1</div>

<p>
Selection Method
</p>

</div>

</div>


<div class="col-md-4">

<div class="card p-4 text-center">

<div class="stat">
DP</div>

<p>
Optimization Technique
</p>

</div>

</div>

</div>

</div>
""".format(len(subjects))

    return render_page(
        "DAA Optimizer",
        html
    )


@app.route("/optimizer/run", methods=["POST"])
def optimizer_run():

    max_credits = int(
        request.form.get("max_credits", 12)
    )

    max_workload = int(
        request.form.get("max_workload", 15)
    )

    conn = get_db()

    subjects = conn.execute("""
        SELECT * FROM subjects
    """).fetchall()

    conn.close()

    result = optimize_subjects(
        subjects,
        max_credits,
        max_workload
    )

    html = f"""

<section class="page-header">

<div class="container">

<h1>
Optimization Result
</h1>

<p>
Generated using 0/1 Knapsack and Dynamic Programming
</p>

</div>

</section>


<div class="container py-5">


<div class="row g-4">

<div class="col-md-3">

<div class="card p-4 text-center">

<div class="stat">
{result['score']}
</div>

<p>
Maximum Preference Score
</p>

</div>

</div>


<div class="col-md-3">

<div class="card p-4 text-center">

<div class="stat">
{result['credits']}
</div>

<p>
Selected Credits
</p>

</div>

</div>


<div class="col-md-3">

<div class="card p-4 text-center">

<div class="stat">
{result['workload']}
</div>

<p>
Workload Used
</p>

</div>

</div>


<div class="col-md-3">

<div class="card p-4 text-center">

<div class="stat">
{result['states']}
</div>

<p>
DP States
</p>

</div>

</div>

</div>


<div class="card p-4 mt-5">

<h3 class="text-success">

<i class="bi bi-check-circle-fill"></i>

Selected Subjects

</h3>

<p class="text-muted">

These subjects form the optimized selection
under the specified constraints.

</p>

<div class="table-responsive">

<table class="table table-hover">

<thead class="table-success">

<tr>

<th>Course</th>
<th>Subject</th>
<th>Credits</th>
<th>Workload</th>
<th>Preference</th>

</tr>

</thead>

<tbody>
"""

    for s in result["selected"]:

        html += f"""

<tr>

<td>
{s['course']}
</td>

<td>
<strong>
{s['name']}
</strong>
</td>

<td>
{s['credits']}
</td>

<td>
{s['workload']}
</td>

<td>
{s['preference']}
</td>

</tr>
"""

    html += """

</tbody>

</table>

</div>

</div>


<div class="card p-4 mt-5">

<h3>
Rejected / Not Selected Subjects
</h3>

<p class="text-muted">

These subjects were not included in the
optimal combination because of the resource
constraints and preference optimization.

</p>

<div class="table-responsive">

<table class="table table-hover">

<thead>

<tr>

<th>Course</th>
<th>Subject</th>
<th>Credits</th>
<th>Workload</th>
<th>Preference</th>

</tr>

</thead>

<tbody>
"""

    for s in result["rejected"]:

        html += f"""

<tr>

<td>{s['course']}</td>

<td>{s['name']}</td>

<td>{s['credits']}</td>

<td>{s['workload']}</td>

<td>{s['preference']}</td>

</tr>
"""

    html += """

</tbody>

</table>

</div>

</div>


<div class="card p-4 mt-5">

<h3>
<i class="bi bi-diagram-3"></i>
How Dynamic Programming Made the Decision
</h3>

<div class="row mt-4">

<div class="col-md-3">

<div class="alert alert-primary">

<strong>1. Input</strong>

<p class="mb-0">
Subjects with credits, workload and
preference scores.
</p>

</div>

</div>


<div class="col-md-3">

<div class="alert alert-info">

<strong>2. Subproblems</strong>

<p class="mb-0">
Each subject creates smaller
optimization states.
</p>

</div>

</div>


<div class="col-md-3">

<div class="alert alert-warning">

<strong>3. DP Table</strong>

<p class="mb-0">
Best score is stored for each
credit/workload state.
</p>

</div>

</div>


<div class="col-md-3">

<div class="alert alert-success">

<strong>4. Reconstruction</strong>

<p class="mb-0">
The final selected subjects are
reconstructed from the stored states.
</p>

</div>

</div>

</div>

</div>


<div class="card p-4 mt-5">

<h3>
Algorithm Explanation
</h3>

<p>

<strong>0/1 Knapsack:</strong>
Each subject can either be selected (1)
or not selected (0). The objective is to
maximize preference score without exceeding
the available credits and workload.

</p>

<p>

<strong>Dynamic Programming:</strong>
The system stores the best result for
smaller credit/workload combinations.
Instead of solving the same subproblem
again, the stored result is reused.

</p>

<p>

<strong>Time Complexity:</strong>
O(n × C × W)

</p>

<p>

where <strong>n</strong> is the number of subjects,
<strong>C</strong> is the credit capacity and
<strong>W</strong> is the workload capacity.

</p>

</div>


<div class="text-center mt-5">

<a href="/optimizer"
class="btn btn-outline-primary">

Run Again

</a>

</div>

</div>
"""

    return render_page(
        "Optimization Result",
        html
    )


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

    init_db()

    print("=" * 60)
    print("MALLA REDDY VISHWA VIDYAPEETH")
    print("Student Subject Selection System")
    print("=" * 60)
    print("Website: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(debug=True)