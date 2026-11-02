import os
import sqlite3
import pymysql
import pymysql.cursors
from werkzeug.security import generate_password_hash
from config import Config

DB_BACKEND = 'mysql'
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'career_guidance.db')

def get_mysql_connection(include_db=True):
    """Attempt MySQL connection."""
    try:
        kwargs = {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'connect_timeout': 3,
            'autocommit': True
        }
        if include_db:
            kwargs['database'] = Config.DB_NAME
        conn = pymysql.connect(**kwargs)
        return conn
    except Exception:
        return None

def test_or_switch_backend():
    """Verify MySQL connectivity or switch to SQLite fallback."""
    global DB_BACKEND
    conn = get_mysql_connection(include_db=False)
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            conn.close()
            DB_BACKEND = 'mysql'
            return 'mysql'
        except Exception:
            conn.close()
    
    DB_BACKEND = 'sqlite'
    return 'sqlite'

def get_sqlite_connection():
    """Create a SQLite connection with row dictionary mapping."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    """Get active database connection."""
    global DB_BACKEND
    if DB_BACKEND == 'mysql':
        conn = get_mysql_connection(include_db=True)
        if conn:
            return conn
        DB_BACKEND = 'sqlite'
    return get_sqlite_connection()

def query_db(query, args=(), one=False, commit=False):
    """Execute parameterized SQL query safely."""
    global DB_BACKEND
    conn = get_db()
    
    if DB_BACKEND == 'mysql':
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                if commit:
                    last_id = cursor.lastrowid
                    conn.close()
                    return last_id
                rv = cursor.fetchall()
                conn.close()
                return (rv[0] if rv else None) if one else rv
        except Exception as e:
            conn.close()
            raise e
    else:
        # SQLite mode
        sqlite_query = query.replace('%s', '?')
        try:
            cursor = conn.cursor()
            cursor.execute(sqlite_query, args)
            if commit:
                conn.commit()
                last_id = cursor.lastrowid
                conn.close()
                return last_id
            rv = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return (rv[0] if rv else None) if one else rv
        except Exception as e:
            conn.close()
            raise e

def init_db():
    """Ensure all 11 tables exist and are populated with rich seed data."""
    test_or_switch_backend()
    global DB_BACKEND

    # Dedicated table creation definitions to prevent syntax issues
    tables_ddl = [
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""",
        """CREATE TABLE IF NOT EXISTS student_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            college_name TEXT,
            degree TEXT,
            department TEXT,
            graduation_year INTEGER,
            bio TEXT,
            selected_career TEXT DEFAULT 'Undecided',
            current_skills TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );""",
        """CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            tools_technologies TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            learning_path TEXT NOT NULL,
            job_opportunities TEXT NOT NULL,
            average_salary TEXT,
            icon TEXT DEFAULT 'fas fa-briefcase',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""",
        """CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            importance TEXT NOT NULL,
            how_to_improve TEXT NOT NULL,
            practice_activities TEXT NOT NULL,
            icon TEXT DEFAULT 'fas fa-check-circle'
        );""",
        """CREATE TABLE IF NOT EXISTS learning_roadmaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            total_levels INTEGER DEFAULT 3,
            duration TEXT DEFAULT '3-6 Months',
            icon TEXT DEFAULT 'fas fa-route'
        );""",
        """CREATE TABLE IF NOT EXISTS roadmap_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roadmap_id INTEGER NOT NULL,
            level TEXT NOT NULL,
            topic_title TEXT NOT NULL,
            description TEXT NOT NULL,
            practical_exercises TEXT NOT NULL,
            mini_project TEXT NOT NULL,
            learning_resources TEXT NOT NULL,
            order_index INTEGER DEFAULT 1,
            FOREIGN KEY (roadmap_id) REFERENCES learning_roadmaps(id) ON DELETE CASCADE
        );""",
        """CREATE TABLE IF NOT EXISTS student_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            roadmap_topic_id INTEGER NOT NULL,
            is_completed INTEGER DEFAULT 1,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (user_id, roadmap_topic_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (roadmap_topic_id) REFERENCES roadmap_topics(id) ON DELETE CASCADE
        );""",
        """CREATE TABLE IF NOT EXISTS career_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            scores_json TEXT NOT NULL,
            recommended_career TEXT NOT NULL,
            match_reason TEXT NOT NULL,
            technical_skills TEXT NOT NULL,
            soft_skills TEXT NOT NULL,
            learning_roadmap TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );""",
        """CREATE TABLE IF NOT EXISTS interview_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            explanation TEXT,
            difficulty TEXT DEFAULT 'Beginner'
        );""",
        """CREATE TABLE IF NOT EXISTS learning_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT,
            is_free INTEGER DEFAULT 1
        );""",
        """CREATE TABLE IF NOT EXISTS job_opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company_name TEXT NOT NULL,
            location TEXT NOT NULL,
            job_type TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            experience_level TEXT DEFAULT 'Fresher / 0-1 Years',
            description TEXT NOT NULL,
            salary_range TEXT,
            apply_url TEXT DEFAULT '#',
            is_verified INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    ]

    if DB_BACKEND == 'sqlite':
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        for ddl in tables_ddl:
            cursor.execute(ddl)
        conn.commit()

        # Seed data if careers or job_opportunities are empty
        seed_all_data(cursor, is_sqlite=True)
        cursor.execute("SELECT COUNT(*) FROM job_opportunities")
        if cursor.fetchone()[0] == 0:
            seed_jobs(cursor, is_sqlite=True)
        conn.commit()

        conn.close()
    else:
        # MySQL mode
        conn = get_mysql_connection(include_db=True)
        if conn:
            with conn.cursor() as cursor:
                # Execute database.sql
                sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database.sql')
                if os.path.exists(sql_path):
                    with open(sql_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    statements = [s.strip() for s in content.split(';') if s.strip()]
                    for stmt in statements:
                        if stmt.upper().startswith('CREATE DATABASE') or stmt.upper().startswith('USE '):
                            continue
                        try:
                            cursor.execute(stmt)
                        except Exception:
                            pass
            conn.close()

def seed_jobs(cursor, is_sqlite=True):
    """Seed sample job opportunities."""
    jobs = [
        ('Associate Python Software Engineer', 'Cognitive Cloud Labs', 'Bengaluru / Hybrid', 'Full-time Fresher', 'Python, Flask/Django, SQL, Git, REST APIs', 'B.Tech/BE/BCA/MCA (2025/2026 Batch)', 'Fresher / 0-1 Year', 'Join our core platform engineering team to build scalable microservices and backend data pipelines.', 'INR 5.5 - 7.5 LPA', '#', 1),
        ('Graduate Java Developer Trainee', 'Enterprise Nexus Systems', 'Hyderabad / On-site', 'Full-time Fresher', 'Core Java, Spring Boot, OOP, MySQL', 'B.Tech CS/IT with min 65% aggregate', 'Fresher', 'Responsible for developing enterprise microservices, writing unit tests, and optimizing database queries.', 'INR 4.5 - 6.5 LPA', '#', 1),
        ('Web Development Intern (Frontend)', 'PixelCraft Studios', 'Remote', 'Internship', 'HTML5, CSS3, JavaScript, Responsive Design', 'Enrolled college students or recent graduates', 'Student / Fresher', 'Work closely with UI/UX designers to translate Figma prototypes into clean, responsive web pages.', 'INR 15,000 - 25,000 / month', '#', 1),
        ('Data Analytics Intern', 'InsightWave Analytics', 'Pune / Hybrid', 'Internship', 'SQL, Excel, Python (Pandas), Power BI', 'B.Tech / B.Sc / BCA / BBA (Final Year)', 'Fresher', 'Analyze customer behavioral data, create interactive weekly dashboards, and present insights to stakeholders.', 'INR 18,000 - 28,000 / month', '#', 1),
        ('Junior QA Automation Engineer', 'TestArmor Solutions', 'Chennai / On-site', 'Full-time Fresher', 'Manual Testing, Selenium, Java/Python, SQL', 'Any Engineering or Computer Application graduate', '0-1 Year', 'Design comprehensive test plans, automate regression test suites, and report defects using JIRA.', 'INR 4.0 - 5.5 LPA', '#', 1),
        ('Cloud & DevOps Associate', 'SkyScale Technologies', 'Gurugram / Hybrid', 'Full-time Fresher', 'Linux, AWS basics, Docker, Bash Scripting', 'B.Tech in CS/IT/ECE (2025/2026)', 'Fresher', 'Support deployment automation pipelines, monitor cloud infrastructure, and maintain containerized workloads.', 'INR 6.0 - 8.5 LPA', '#', 1)
    ]
    ph = '?' if is_sqlite else '%s'
    for job in jobs:
        cursor.execute(f"""INSERT INTO job_opportunities 
            (title, company_name, location, job_type, required_skills, eligibility, experience_level, description, salary_range, apply_url, is_verified)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})""", job)

def seed_all_data(cursor, is_sqlite=True):
    """Seed all 10 careers, roadmaps, skills, questions, and default users."""
    ph = '?' if is_sqlite else '%s'
    pwd_hash = generate_password_hash('Admin@123')

    # Seed Admin & Student accounts with Admin@123
    pwd_hash = generate_password_hash('Admin@123')
    cursor.execute(f"INSERT OR IGNORE INTO users (id, full_name, email, password_hash, role) VALUES (1, 'System Administrator', 'admin@careerguidance.com', {ph}, 'admin')", (pwd_hash,))
    cursor.execute(f"UPDATE users SET password_hash = {ph} WHERE email = 'admin@careerguidance.com'", (pwd_hash,))
    
    cursor.execute(f"INSERT OR IGNORE INTO users (id, full_name, email, password_hash, role) VALUES (2, 'Rahul Sharma', 'rahul@student.edu', {ph}, 'student')", (pwd_hash,))
    cursor.execute(f"UPDATE users SET password_hash = {ph} WHERE email = 'rahul@student.edu'", (pwd_hash,))
    
    cursor.execute("INSERT OR IGNORE INTO student_profiles (user_id, college_name, degree, department, graduation_year, bio, selected_career, current_skills) VALUES (2, 'Institute of Engineering & Technology', 'B.Tech', 'Computer Science and Engineering', 2026, 'Final year student enthusiastic about Python and Full Stack Development, aiming for tier-1 campus placements.', 'Python Developer', 'Python, HTML, CSS, SQL, Git')")

    # 10 Careers
    careers = [
        (1, 'Python Developer', 'Software Engineering', 'Builds backend web services, automation scripts, and software solutions using Python.', 'Python, OOP, Data Structures, SQL, REST APIs, Git', 'Django, Flask, FastAPI, Postman, PostgreSQL, Docker', 'B.Tech / B.E / BCA / MCA in CS/IT or related fields', 'Python Basics -> OOP & Data Structures -> Flask/Django -> Database Design -> REST APIs & Deployment', 'Software Engineer, Python Backend Developer, Automation Engineer', 'INR 4.5 - 9.0 LPA', 'fab fa-python'),
        (2, 'Java Developer', 'Software Engineering', 'Develops enterprise-grade scalable applications, microservices, and backend architectures.', 'Core Java, Collections, Multithreading, Spring Boot, Hibernate, SQL', 'IntelliJ IDEA, Maven, Spring Boot, MySQL, JUnit, Docker', 'B.Tech / BCA / MCA with strong fundamentals in OOP', 'Core Java Basics -> Advanced Java & Collections -> Spring Boot & Hibernate -> Microservices & CI/CD', 'Java Software Engineer, Enterprise Application Developer, Backend Associate', 'INR 4.5 - 9.5 LPA', 'fab fa-java'),
        (3, 'Web Developer', 'Web & Mobile', 'Creates modern, responsive, and engaging websites and web user interfaces.', 'HTML5, CSS3, JavaScript (ES6+), Responsive Design, CSS Flexbox & Grid', 'VS Code, Chrome DevTools, Bootstrap, Git, Figma, Netlify', 'Any graduate with passion for web design and programming', 'HTML/CSS Mastery -> Modern JavaScript -> Responsive Layouts -> API Integration -> Web Performance', 'Frontend Developer, UI Developer, Web Designer, Junior Web Engineer', 'INR 3.5 - 7.5 LPA', 'fas fa-code'),
        (4, 'Full Stack Developer', 'Software Engineering', 'End-to-end development handling client-side interfaces, server-side APIs, and database architecture.', 'Frontend (HTML/CSS/JS), Backend (Python/Node/Java), Databases, REST APIs', 'Git, VS Code, Flask/Django/Express, React/Vue, MySQL, Docker, Linux', 'B.Tech / BCA / BSc CS / MCA freshers with multi-tier understanding', 'Frontend Foundations -> Backend Framework -> Relational & NoSQL DBs -> API Security -> Cloud Deployment', 'Full Stack Engineer, Associate Software Developer, Product Engineer', 'INR 5.0 - 11.0 LPA', 'fas fa-layer-group'),
        (5, 'Software Tester', 'Quality Assurance', 'Ensures software quality, reliability, and security through manual and automated testing strategies.', 'Manual Testing, Test Cases, SDLC/STLC, Automation Basics, SQL', 'Selenium WebDriver, Postman, Jira, TestNG, Git, Jenkins', 'B.Tech / BCA / BSc with strong attention to detail and analytical skills', 'Testing Fundamentals & STLC -> Defect Lifecycle & JIRA -> API Testing with Postman -> Selenium Automation', 'QA Engineer, Test Automation Engineer, Software Quality Analyst', 'INR 3.5 - 6.5 LPA', 'fas fa-vial'),
        (6, 'Data Analyst', 'Data & Analytics', 'Transforms raw structured and unstructured data into actionable business intelligence and dashboards.', 'SQL, Excel, Python/R, Data Cleaning, Statistical Analysis, Data Storytelling', 'Power BI, Tableau, Excel (VLOOKUP, Pivot), Pandas, NumPy, MySQL', 'B.Tech / B.Sc / BCA / BBA with affinity for numbers and business logic', 'Excel Mastery -> SQL for Data Analysis -> Python for Data Manipulation -> PowerBI/Tableau Dashboards', 'Data Analyst, Business Intelligence Associate, Junior Data Specialist', 'INR 4.0 - 8.0 LPA', 'fas fa-chart-line'),
        (7, 'Data Scientist', 'Data Science & AI', 'Leverages statistical modeling, machine learning algorithms, and predictive analytics to solve complex problems.', 'Advanced Python, Mathematics & Linear Algebra, Probability, Statistics, Machine Learning', 'Scikit-Learn, Pandas, NumPy, Jupyter, Matplotlib, Seaborn, SQL', 'B.Tech / M.Tech / MCA with strong quantitative and programming background', 'Math & Statistics Foundations -> Python for Data Science -> Supervised & Unsupervised ML -> Deep Learning Basics', 'Associate Data Scientist, Machine Learning Associate, Data Science Trainee', 'INR 6.0 - 12.0 LPA', 'fas fa-brain'),
        (8, 'AI/ML Engineer', 'Artificial Intelligence', 'Designs and builds machine learning systems, deep neural networks, and generative AI models.', 'Python, Linear Algebra, Calculus, Deep Learning, NLP, Computer Vision', 'PyTorch, TensorFlow, Hugging Face, OpenCV, Scikit-learn, CUDA', 'B.Tech CS/IT or Electrical with passion for algorithmic innovation', 'Core Python & Math -> ML Algorithms -> Deep Learning (CNN/RNN/Transformers) -> Model Deployment & MLOps', 'AI Engineer, Machine Learning Developer, Research Associate', 'INR 6.5 - 14.0 LPA', 'fas fa-robot'),
        (9, 'Cloud Engineer', 'Cloud & DevOps', 'Architects, maintains, and scales cloud infrastructure and automated deployment pipelines.', 'Linux Administration, Networking, Cloud Concepts, Shell Scripting, CI/CD, Containerization', 'AWS, Azure, Docker, Kubernetes, Terraform, Git, Jenkins', 'B.Tech / BCA / MCA students interested in systems and cloud platforms', 'Linux & Networking Basics -> AWS/Azure Core Services -> Docker & Containers -> CI/CD & Infrastructure as Code', 'Cloud Support Associate, DevOps Engineer, Junior Cloud Architect', 'INR 5.0 - 10.0 LPA', 'fas fa-cloud'),
        (10, 'Cybersecurity Analyst', 'Information Security', 'Protects IT infrastructure, networks, and confidential data against digital vulnerabilities and cyber attacks.', 'Networking (TCP/IP, DNS), OS Security, Cryptography, Vulnerability Assessment, Security Tools', 'Wireshark, Nmap, Kali Linux, Burp Suite, Metasploit, SIEM tools', 'B.Tech CS/IT with analytical mindset and ethical hacking passion', 'Computer Networks & OS -> Security Fundamentals & Cryptography -> Ethical Hacking & Pentesting -> SOC & Incident Response', 'Information Security Analyst, SOC Analyst, Junior Penetration Tester', 'INR 4.5 - 9.0 LPA', 'fas fa-shield-alt')
    ]
    for c in careers:
        cursor.execute(f"""INSERT OR IGNORE INTO careers 
            (id, title, category, description, required_skills, tools_technologies, eligibility, learning_path, job_opportunities, average_salary, icon)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})""", c)

    # 8 Roadmaps
    roadmaps = [
        (1, 'Python Programming', 'python', 'Comprehensive pathway from core Python syntax to object-oriented programming, data handling, and backend web APIs.', 3, '3 Months', 'fab fa-python'),
        (2, 'Java Programming', 'java', 'Master modern Core Java, OOP design patterns, enterprise collections, and Spring Boot framework.', 3, '4 Months', 'fab fa-java'),
        (3, 'HTML and CSS', 'html-css', 'Build pixel-perfect, accessible, and responsive user interfaces with modern CSS Grid, Flexbox, and animations.', 3, '2 Months', 'fab fa-html5'),
        (4, 'JavaScript', 'javascript', 'Deep dive into asynchronous JavaScript, DOM manipulation, ES6+ syntax, and modern API communication.', 3, '3 Months', 'fab fa-js'),
        (5, 'Full Stack Development', 'fullstack', 'End-to-end web engineering covering frontend UI, Python/Flask backend, relational databases, and secure deployment.', 3, '5 Months', 'fas fa-layer-group'),
        (6, 'SQL & Relational Databases', 'sql', 'Master relational database modeling, complex JOINs, query optimization, indexing, and transactional integrity.', 3, '2 Months', 'fas fa-database'),
        (7, 'Data Analytics', 'data-analytics', 'Learn data extraction with SQL, manipulation with Pandas, exploratory data analysis, and dashboard visualization with PowerBI.', 3, '4 Months', 'fas fa-chart-pie'),
        (8, 'Artificial Intelligence & ML', 'ai-ml', 'Systematic path from linear algebra to scikit-learn, deep neural architectures, and natural language models.', 3, '6 Months', 'fas fa-robot')
    ]
    for r in roadmaps:
        cursor.execute(f"INSERT OR IGNORE INTO learning_roadmaps (id, title, slug, description, total_levels, duration, icon) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})", r)

    # Roadmap topics
    topics = [
        (1, 1, 'Beginner', 'Python Syntax, Variables & Control Flow', 'Master variables, data types, if-elif-else statements, and loops.', 'Write programs for prime number checks and palindrome verifications.', 'Command-Line Student Grade Calculator', 'Official Python Docs (docs.python.org)', 1),
        (2, 1, 'Beginner', 'Data Structures (Lists, Tuples, Dictionaries, Sets)', 'Understand in-memory collections, slicing, indexing, and dictionary keys/values.', 'Implement a phonebook directory using dictionaries.', 'Terminal-Based Contact Book Application', 'Corey Schafer Python Collections Tutorial', 2),
        (3, 1, 'Intermediate', 'Object-Oriented Programming (OOP) in Python', 'Classes, objects, constructors, encapsulation, inheritance, polymorphism.', 'Design a banking system hierarchy with Savings and Current accounts.', 'Library Book Management System', 'Real Python OOP Guide', 3),
        (4, 1, 'Intermediate', 'File Handling, Modules & Exception Handling', 'Reading and writing CSV/JSON files, try-except-finally blocks, and pip.', 'Parse a CSV dataset and compute summary statistics.', 'CSV Data Report Generator with Logging', 'Automate the Boring Stuff with Python', 4),
        (5, 1, 'Advanced', 'Flask Web Framework & REST APIs', 'Routing, request handling, Jinja templates, RESTful API design, and JSON responses.', 'Build a REST API with CRUD endpoints connected to a database.', 'Full-featured Student Placement Portal API', 'Flask Official Documentation', 5),
        (6, 1, 'Advanced', 'Database Integration & Unit Testing', 'Using parameterized queries, unit testing with pytest, and deployment.', 'Write automated test cases for user authentication.', 'Automated Placement Drive Management System', 'PyTest Documentation', 6),
        # Java
        (7, 2, 'Beginner', 'Java Basics & Fundamentals', 'JDK/JRE architecture, JVM memory model, primitive types, loops, and arrays.', 'Implement matrix multiplication and array sorting.', 'Console Banking System', 'Oracle Java Docs', 1),
        (8, 2, 'Intermediate', 'OOP & Java Collections Framework', 'Interfaces, abstract classes, ArrayList, HashMap, and HashSet.', 'Sort custom Student objects by CGPA using Collections.sort().', 'College Student Attendance Tracker', 'Baeldung Java Tutorials', 2),
        (9, 2, 'Advanced', 'Spring Boot & RESTful Microservices', 'Dependency Injection, Spring Data JPA, Hibernate, and REST Controllers.', 'Build CRUD endpoints for employee management with MySQL persistence.', 'Online Course Registration REST API', 'Spring.io Guides', 3),
        # HTML/CSS
        (10, 3, 'Beginner', 'Semantic HTML5 & Core CSS3', 'Semantic tags, forms, inputs, box model, colors, and typography.', 'Build a semantic personal portfolio page with contact forms.', 'Personal Resume & Portfolio Website', 'MDN Web Docs', 1),
        (11, 3, 'Intermediate', 'CSS Flexbox, Grid & Responsive Layouts', 'Master Flexbox, CSS Grid, media queries, and mobile-first design.', 'Create a responsive multi-column product card grid with hover effects.', 'Responsive College Event Showcase Webpage', 'CSS Tricks', 2),
        (12, 3, 'Advanced', 'CSS Animations, Variables & Modern Design', 'Custom properties, transitions, keyframes, glassmorphism, and dark mode.', 'Build an interactive dashboard theme switcher with card animations.', 'Modern SaaS Product Landing Page', 'Modern CSS Solutions', 3),
        # JS
        (13, 4, 'Beginner', 'JavaScript Basics & DOM Manipulation', 'Variables (let/const), functions, DOM selectors, event listeners.', 'Create an interactive task checklist with add and delete features.', 'Interactive To-Do & Task Manager App', 'JavaScript.info', 1),
        (14, 4, 'Intermediate', 'ES6+ Features & Asynchronous Programming', 'Arrow functions, destructuring, Promises, async/await, and Fetch API.', 'Fetch mock user data from API and display in searchable cards.', 'Live Weather & Forecast Web App', 'MDN Async Guide', 2),
        (15, 4, 'Advanced', 'Form Validation, Web Storage & Modular JS', 'Client-side regex validation, localStorage, and modular architecture.', 'Persist multi-step user onboarding data in browser storage.', 'Interactive Fresher Resume Builder with PDF Export', 'Frontend Masters JS', 3),
        # Fullstack
        (16, 5, 'Beginner', 'Frontend Foundations & Backend Routing', 'Connecting HTML/CSS templates with Flask routes and Jinja rendering.', 'Create a dynamic multi-page website with shared navigation.', 'College Departmental Information Portal', 'Flask Mega-Tutorial', 1),
        (17, 5, 'Intermediate', 'User Authentication, Sessions & MySQL', 'Password hashing with Werkzeug, user login, and session security.', 'Implement user login, signup with email verification logic.', 'Secure Campus Placement Registration Portal', 'Real Python Auth', 2),
        (18, 5, 'Advanced', 'Full-Stack CRUD, API Integration & Deployment', 'Full CRUD operations, REST API endpoints, search/filter functionality.', 'Build full lifecycle application with student dashboard and MySQL.', 'Complete Career Guidance & Placement Platform', 'DigitalOcean Production Guide', 3),
        # SQL
        (19, 6, 'Beginner', 'SQL Foundations & Table Design', 'DDL/DML, CREATE, ALTER, INSERT, UPDATE, DELETE, and SELECT.', 'Write queries to filter students by department and graduation year.', 'College Library Database Schema', 'Mode Analytics SQL', 1),
        (20, 6, 'Intermediate', 'Relational JOINS, Grouping & Aggregations', 'INNER/LEFT/RIGHT JOIN, COUNT, AVG, GROUP BY, and HAVING.', 'Compute department-wise placement statistics and highest packages.', 'Placement Analytics Reporting Queries', 'LeetCode SQL 50', 2),
        (21, 6, 'Advanced', 'Indexes, Transactions & Query Optimization', 'B-Tree indexes, EXPLAIN query plan, and ACID transactions.', 'Optimize slow search queries across mock records with indexing.', 'High-Performance E-commerce Order Ledger', 'Use The Index, Luke!', 3),
        # Data Analytics
        (22, 7, 'Beginner', 'Data Analysis with Excel & SQL', 'Advanced Excel (VLOOKUP, Pivot Tables), SQL aggregations.', 'Analyze campus placement records in Excel and summarize by branch.', 'Campus Placement Summary Dashboard in Excel', 'Chandoo Excel Analytics', 1),
        (23, 7, 'Intermediate', 'Python for Data Analysis (Pandas & NumPy)', 'DataFrames, Series, handling missing data, grouping, and charts.', 'Clean a messy dataset of fresher job postings and plot salaries.', 'Fresher Hiring Market Trends Exploratory Report', 'Kaggle Micro-Courses', 2),
        (24, 7, 'Advanced', 'Interactive Business Intelligence Dashboards', 'Power BI / Tableau data modeling, DAX measures, and KPI cards.', 'Build an interactive 3-page placement performance dashboard.', 'Interactive University Placement KPI Dashboard', 'Microsoft Power BI Guide', 3),
        # AI/ML
        (25, 8, 'Beginner', 'Math & Statistics for Machine Learning', 'Linear algebra, probability distributions, descriptive statistics.', 'Implement gradient descent from scratch for linear regression in Python.', 'Math Fundamentals for Data Science Workbook', 'Khan Academy & 3Blue1Brown', 1),
        (26, 8, 'Intermediate', 'Supervised & Unsupervised Machine Learning', 'Regression, Classification, Clustering, and evaluation metrics.', 'Train models to predict student placement eligibility based on CGPA.', 'Student Placement Predictor ML Model', 'Scikit-Learn Guide', 2),
        (27, 8, 'Advanced', 'Deep Learning & Natural Language Processing', 'Neural networks, activation functions, CNNs, and embeddings.', 'Build an automated resume keyword matcher comparing skills to jobs.', 'AI-Powered Resume to Job Matcher Engine', 'DeepLearning.AI', 3)
    ]
    for t in topics:
        cursor.execute(f"""INSERT OR IGNORE INTO roadmap_topics 
            (id, roadmap_id, level, topic_title, description, practical_exercises, mini_project, learning_resources, order_index)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})""", t)

    # Skills
    skills = [
        (1, 'Python', 'technical', 'A high-level, general-purpose language renowned for readable syntax and versatile libraries across web, automation, and AI.', 'Highest demand across freshers for rapid prototyping, data science, and backend development.', 'Code daily on LeetCode/HackerRank, build end-to-end projects, study OOP principles.', 'Build a CLI task tracker, write a web scraper, and solve 30 coding challenges.', 'fab fa-python'),
        (2, 'Java', 'technical', 'A robust, object-oriented, platform-independent language powering high-scale enterprise systems.', 'Heavily asked in service-based and product-based campus recruitment drives (TCS, Infosys, Wipro, Amazon).', 'Master core OOP, memory management, garbage collection, and collections framework.', 'Build a student management system and practice multi-threading programs.', 'fab fa-java'),
        (3, 'C Programming', 'technical', 'A foundational procedural language that teaches direct memory manipulation and low-level computer architecture.', 'Essential for understanding pointers, data structures, and passing technical screening rounds.', 'Write programs using pointers, dynamic memory allocation (malloc/free), and structs.', 'Implement linked lists, stacks, and binary search trees in pure C.', 'fas fa-code'),
        (4, 'HTML', 'technical', 'The standard markup language for creating the foundational structure of web pages.', 'Mandatory starting block for every web developer and full-stack software engineer.', 'Learn semantic HTML5 elements, form validations, and accessibility standards.', 'Create structured forms, accessible tables, and semantic portfolio pages.', 'fab fa-html5'),
        (5, 'CSS', 'technical', 'Cascading Style Sheets used to style, format, and animate the visual presentation of HTML documents.', 'Essential for creating modern, attractive, and responsive user experiences.', 'Learn Flexbox, CSS Grid, media queries, and transition animations.', 'Recreate popular landing pages from scratch without frameworks.', 'fab fa-css3-alt'),
        (6, 'JavaScript', 'technical', 'The core scripting language that enables dynamic interactivity, asynchronous behavior, and modern web applications.', 'The most widely used programming language across the entire web ecosystem.', 'Understand ES6+ features, closures, event loop, Promises, and DOM manipulation.', 'Build a calculator, interactive quiz application, and weather dashboard using fetch API.', 'fab fa-js'),
        (7, 'SQL', 'technical', 'Structured Query Language used to query, update, and manage relational databases.', 'Every software engineering role requires interacting with relational data stores.', 'Practice complex JOINs, aggregate functions, subqueries, and table normalization.', 'Solve SQL problems on LeetCode and design a relational database schema for an e-commerce store.', 'fas fa-database'),
        (8, 'Data Structures', 'technical', 'Techniques for organizing and storing data efficiently in computer memory (Arrays, Stacks, Queues, Trees, Graphs).', 'The central pillar of campus technical interviews at all top tech companies.', 'Understand Big-O time and space complexity, recursion, and traversal algorithms.', 'Implement BFS/DFS on graphs, binary tree traversals, and quicksort.', 'fas fa-project-diagram'),
        (9, 'Problem Solving', 'technical', 'The ability to dissect complex real-world challenges and devise optimized algorithmic solutions.', 'Evaluated via coding rounds and technical interviews to assess critical thinking.', 'Decompose problems into smaller subproblems, write pseudocode, and analyze edge cases.', 'Solve at least 1-2 coding problems daily on platforms like LeetCode and GeeksforGeeks.', 'fas fa-puzzle-piece'),
        (10, 'Git and GitHub', 'technical', 'Distributed version control system to track source code changes and collaborate with engineering teams.', 'Required by every software company to manage codebases and demonstrate open-source projects.', 'Learn branching, merging, pull requests, resolving merge conflicts, and commit conventions.', 'Publish all your college projects with descriptive READMEs and commit histories on GitHub.', 'fab fa-github'),
        (11, 'Communication', 'soft', 'The ability to clearly, concisely, and persuasively convey technical and non-technical ideas.', 'Vital for clearing HR interviews, participating in group discussions, and team collaboration.', 'Practice speaking in English, record your self-introductions, and participate in technical seminars.', 'Conduct mock interviews with peers and explain a technical concept to a non-technical friend.', 'fas fa-comments'),
        (12, 'Teamwork', 'soft', 'Collaborating harmoniously with peers towards a shared goal while respecting diverse viewpoints.', 'Software engineering is a team sport; recruiters prioritize team players over lone wolves.', 'Participate in college hackathons, group projects, and open-source contributions.', 'Work in a group of 3-4 students to build a full-stack semester project.', 'fas fa-users'),
        (13, 'Time Management', 'soft', 'Prioritizing tasks and organizing time effectively to meet deadlines without unnecessary stress.', 'Crucial during final year for balancing academics, placement prep, and project deadlines.', 'Use techniques like the Pomodoro method, Eisenhower matrix, and digital calendars.', 'Create a weekly study timetable dividing time between coding, aptitude, and college work.', 'fas fa-clock'),
        (14, 'Leadership', 'soft', 'Inspiring, guiding, and supporting others to accomplish collective milestones with accountability.', 'Differentiates exceptional candidates during group discussions and managerial rounds.', 'Take initiative in college clubs, student societies, or project team leadership.', 'Lead a team during an academic workshop, technical fest, or group assignment.', 'fas fa-flag'),
        (15, 'Adaptability', 'soft', 'The capacity to adjust quickly to new technologies, changing project scopes, and unfamiliar environments.', 'Technology evolves rapidly; tech companies hire candidates who learn quickly.', 'Step out of your comfort zone, explore new programming paradigms, and welcome feedback.', 'Pick up a new framework or tool (e.g., Docker or Tailwind) over a weekend and build a mini-app.', 'fas fa-sync-alt'),
        (16, 'Critical Thinking', 'soft', 'Objective analysis and logical evaluation of facts to form well-reasoned judgments and solutions.', 'Key for root-cause debugging, architectural choices, and behavioral interviews.', 'Question assumptions, evaluate trade-offs between approaches, and avoid cargo-cult programming.', 'Analyze the time/space trade-offs between two different sorting algorithms or system architectures.', 'fas fa-lightbulb'),
        (17, 'Presentation Skills', 'soft', 'Structuring and delivering engaging visual and verbal presentations with confidence.', 'Essential for final year project defense, client demonstrations, and campus presentations.', 'Design clean slide decks, avoid walls of text, maintain eye contact, and practice pacing.', 'Deliver a 5-minute presentation on your semester project in front of your friends or mirror.', 'fas fa-chalkboard-teacher')
    ]
    for s in skills:
        cursor.execute(f"INSERT OR IGNORE INTO skills (id, name, category, description, importance, how_to_improve, practice_activities, icon) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})", s)

    # Questions
    questions = [
        (1, 'technical', 'python', 'What is the difference between list and tuple in Python?', 'Lists are mutable (can be changed after creation) defined using [], while tuples are immutable defined using (). Tuples are faster and consume less memory.', 'Lists have methods like append() and pop(). Tuples cannot be modified once declared.', 'Beginner'),
        (2, 'technical', 'python', 'Explain Python''s memory management and garbage collection.', 'Python manages memory using a private heap. It utilizes reference counting as its primary garbage collection mechanism, supplemented by a cyclic garbage collector.', 'When reference count drops to zero, Python deallocates the memory immediately.', 'Intermediate'),
        (3, 'technical', 'python', 'What are decorators in Python and how do you use them?', 'Decorators are functions that take another function as an argument, extend or modify its behavior without modifying the original code, and return a callable.', 'Commonly used for logging, authentication, and route definitions in Flask (@app.route).', 'Intermediate'),
        (4, 'technical', 'java', 'What are the main OOP concepts in Java?', 'The four primary pillars of OOP are: Encapsulation (data hiding), Inheritance (code reuse), Polymorphism (overloading/overriding), and Abstraction (interfaces/abstract classes).', 'Every enterprise Java system relies on these pillars for clean architecture.', 'Beginner'),
        (5, 'technical', 'java', 'What is the difference between HashMap and ConcurrentHashMap in Java?', 'HashMap is non-synchronized and not thread-safe. ConcurrentHashMap is thread-safe and allows concurrent read/write operations without locking the entire map.', 'In multi-threaded environments, ConcurrentHashMap achieves high performance through segment locking.', 'Advanced'),
        (6, 'technical', 'sql', 'What is the difference between WHERE and HAVING clause in SQL?', 'WHERE filters rows before groupings are applied and cannot contain aggregate functions. HAVING filters groups after GROUP BY and evaluates aggregate functions like COUNT(), SUM().', 'Example: SELECT dept, COUNT(*) FROM emp WHERE salary > 30000 GROUP BY dept HAVING COUNT(*) > 5;', 'Beginner'),
        (7, 'technical', 'sql', 'What are the different types of JOINs in SQL?', 'INNER JOIN (matching rows in both tables), LEFT JOIN (all rows from left + matching from right), RIGHT JOIN (all from right + matching from left), and FULL OUTER JOIN.', 'Choosing the appropriate JOIN type is essential for data integrity.', 'Beginner'),
        (8, 'technical', 'html_css', 'What is the CSS Box Model and what are its components?', 'The CSS Box Model describes rectangular boxes generated for elements: Content, Padding, Border, and Margin.', 'Setting box-sizing: border-box is modern best practice so width includes padding and borders.', 'Beginner'),
        (9, 'technical', 'javascript', 'Explain the difference between == and === in JavaScript.', '== is the loose equality operator that performs type coercion. === is the strict equality operator that checks both value and type without coercion.', '5 == "5" is true, but 5 === "5" is false.', 'Beginner'),
        (10, 'technical', 'javascript', 'What is the Event Loop in JavaScript?', 'JavaScript is single-threaded. The event loop continuously monitors Call Stack and Callback Queue, pushing queued tasks to the stack when free.', 'This enables non-blocking asynchronous operations like Promises and fetch requests.', 'Advanced'),
        (11, 'hr', 'hr', 'Tell me about yourself.', 'Give a structured answer: 1. Present: Name, degree, and technical specialization. 2. Past: Key academic achievements and hands-on projects. 3. Future: Your passion for software engineering and how you align with the company.', 'Keep it concise (1.5 to 2 minutes). Focus on enthusiasm and technical competencies.', 'Beginner'),
        (12, 'hr', 'hr', 'What are your greatest strengths and weaknesses?', 'Strength: Fast learner, analytical problem solver, strong team collaborator with examples. Weakness: Genuine non-fatal area with active steps you take to improve.', 'Never say "I have no weaknesses" or "I am a perfectionist".', 'Beginner'),
        (13, 'hr', 'hr', 'Why should we hire you?', 'As a fresher, I bring strong computer science fundamentals in data structures, Python, and SQL, coupled with hands-on project experience building full-stack applications. I am enthusiastic and quick to adapt.', 'Demonstrate enthusiasm and concrete project proof.', 'Beginner'),
        (14, 'hr', 'hr', 'Where do you see yourself in 5 years?', 'In 5 years, I see myself as a seasoned software engineer who has developed deep technical expertise in building scalable systems and mentored junior engineers.', 'Shows ambition and career focus without being unrealistic.', 'Beginner'),
        (15, 'hr', 'hr', 'Why do you want to join our company?', 'Research the company beforehand: Mention their engineering culture, products, and innovation. Highlight why their platform provides the best launchpad for your technical skills.', 'Shows preparation and genuine interest.', 'Beginner'),
        (16, 'aptitude', 'quantitative', 'A train 240 m long passes a pole in 24 seconds. How long will it take to pass a platform 650 m long?', 'Answer: 89 seconds.', 'Speed = 240/24 = 10 m/s. Total distance = 240 + 650 = 890 m. Time = 890/10 = 89 seconds.', 'Beginner'),
        (17, 'aptitude', 'quantitative', 'If CP of 20 articles is equal to SP of 16 articles, what is the profit percentage?', 'Answer: 25% profit.', 'Let CP = Rs.1. CP of 16 = 16, SP of 16 = 20. Profit = 4. Profit % = (4/16)*100 = 25%.', 'Beginner'),
        (18, 'aptitude', 'logical', 'Look at this series: 2, 1, (1/2), (1/4), ... What number should come next?', 'Answer: 1/8.', 'Each number is half of the previous number: (1/4)/2 = 1/8.', 'Beginner'),
        (19, 'aptitude', 'logical', 'Pointing to a photograph of a boy, Suresh said, "He is the son of the only son of my mother." How is Suresh related to that boy?', 'Answer: Father.', 'Suresh''s mother''s only son is Suresh himself. So the boy is Suresh''s son.', 'Beginner'),
        (20, 'aptitude', 'verbal', 'Choose the correct synonym for CANDID: (A) Secretive (B) Frank (C) Shy (D) Dishonest', 'Answer: (B) Frank.', 'Candid means straightforward, truthful, and sincere in speech.', 'Beginner'),
        (21, 'aptitude', 'verbal', 'Select the correctly punctuated sentence: (A) Its raining outside. (B) It''s raining outside. (C) Its'' raining outside.', 'Answer: (B) It''s raining outside.', '"It''s" is the contraction for "it is", while "its" is a possessive pronoun.', 'Beginner')
    ]
    for q in questions:
        cursor.execute(f"INSERT OR IGNORE INTO interview_questions (id, category, subcategory, question, answer, explanation, difficulty) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})", q)

    # Seed jobs
    seed_jobs(cursor, is_sqlite)
