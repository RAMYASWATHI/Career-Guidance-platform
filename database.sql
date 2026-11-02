-- ==========================================================
-- CAREER GUIDANCE PLATFORM DATABASE SCHEMA & SEED DATA
-- Database Name: career_guidance_db
-- Designed for: College Students, Final-Year Students & Freshers
-- ==========================================================

CREATE DATABASE IF NOT EXISTS career_guidance_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE career_guidance_db;

-- ----------------------------------------------------------
-- 1. USERS TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 2. STUDENT PROFILES TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS student_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    college_name VARCHAR(150),
    degree VARCHAR(100),
    department VARCHAR(100),
    graduation_year INT,
    bio TEXT,
    selected_career VARCHAR(100) DEFAULT 'Undecided',
    current_skills TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 3. CAREERS TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS careers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    category VARCHAR(80) NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT NOT NULL,
    tools_technologies TEXT NOT NULL,
    eligibility TEXT NOT NULL,
    learning_path TEXT NOT NULL,
    job_opportunities TEXT NOT NULL,
    average_salary VARCHAR(60),
    icon VARCHAR(60) DEFAULT 'fas fa-briefcase',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 4. SKILLS TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category ENUM('technical', 'soft') NOT NULL,
    description TEXT NOT NULL,
    importance TEXT NOT NULL,
    how_to_improve TEXT NOT NULL,
    practice_activities TEXT NOT NULL,
    icon VARCHAR(60) DEFAULT 'fas fa-check-circle'
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 5. LEARNING ROADMAPS TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS learning_roadmaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    total_levels INT DEFAULT 3,
    duration VARCHAR(60) DEFAULT '3-6 Months',
    icon VARCHAR(60) DEFAULT 'fas fa-route'
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 6. ROADMAP TOPICS TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS roadmap_topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roadmap_id INT NOT NULL,
    level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    topic_title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    practical_exercises TEXT NOT NULL,
    mini_project TEXT NOT NULL,
    learning_resources TEXT NOT NULL,
    order_index INT DEFAULT 1,
    FOREIGN KEY (roadmap_id) REFERENCES learning_roadmaps(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 7. STUDENT PROGRESS TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS student_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    roadmap_topic_id INT NOT NULL,
    is_completed BOOLEAN DEFAULT TRUE,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_topic (user_id, roadmap_topic_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (roadmap_topic_id) REFERENCES roadmap_topics(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 8. CAREER ASSESSMENTS TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS career_assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    scores_json TEXT NOT NULL,
    recommended_career VARCHAR(100) NOT NULL,
    match_reason TEXT NOT NULL,
    technical_skills TEXT NOT NULL,
    soft_skills TEXT NOT NULL,
    learning_roadmap VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 9. INTERVIEW QUESTIONS TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS interview_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category ENUM('technical', 'hr', 'aptitude') NOT NULL,
    subcategory VARCHAR(80) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT,
    difficulty ENUM('Beginner', 'Intermediate', 'Advanced') DEFAULT 'Beginner'
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 10. LEARNING RESOURCES TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS learning_resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(80) NOT NULL,
    resource_type ENUM('Documentation', 'Course', 'Video', 'Book', 'Practice') NOT NULL,
    url VARCHAR(255) NOT NULL,
    description TEXT,
    is_free BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 11. JOB OPPORTUNITIES TABLE
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS job_opportunities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    company_name VARCHAR(150) NOT NULL,
    location VARCHAR(100) NOT NULL,
    job_type ENUM('Internship', 'Full-time Fresher', 'Entry-level') NOT NULL,
    required_skills TEXT NOT NULL,
    eligibility VARCHAR(150) NOT NULL,
    experience_level VARCHAR(60) DEFAULT 'Fresher / 0-1 Years',
    description TEXT NOT NULL,
    salary_range VARCHAR(80),
    apply_url VARCHAR(255) DEFAULT '#',
    is_verified BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==========================================================
-- SEED INITIAL DATA
-- ==========================================================

-- Admin User: admin@careerguidance.com / Admin@123 (Werkzeug scrypt hash)
INSERT INTO users (id, full_name, email, password_hash, role) VALUES 
(1, 'System Administrator', 'admin@careerguidance.com', 'scrypt:32768:8:1$Kq1Z7c3uT2xW9vE1$f6b4d3f572a12a7a4f9e1e90d3d52c10b779a951c3d0b2f9f592d3b4e78a63dc16a7042a344dcfb9c6a1cf8ef10313f837da6b92be6b4f76269b6dc65e4a05df', 'admin'),
(2, 'Rahul Sharma', 'rahul@student.edu', 'scrypt:32768:8:1$Kq1Z7c3uT2xW9vE1$f6b4d3f572a12a7a4f9e1e90d3d52c10b779a951c3d0b2f9f592d3b4e78a63dc16a7042a344dcfb9c6a1cf8ef10313f837da6b92be6b4f76269b6dc65e4a05df', 'student')
ON DUPLICATE KEY UPDATE id=id;

INSERT INTO student_profiles (user_id, college_name, degree, department, graduation_year, bio, selected_career, current_skills) VALUES 
(2, 'Institute of Engineering & Technology', 'B.Tech', 'Computer Science and Engineering', 2026, 'Final year student enthusiastic about Python and Full Stack Development, aiming for tier-1 campus placements.', 'Python Developer', 'Python, HTML, CSS, SQL, Git')
ON DUPLICATE KEY UPDATE user_id=user_id;

-- Seed Careers (10 required careers)
INSERT INTO careers (id, title, category, description, required_skills, tools_technologies, eligibility, learning_path, job_opportunities, average_salary, icon) VALUES
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
ON DUPLICATE KEY UPDATE id=id;

-- Seed Roadmaps (8 required domains)
INSERT INTO learning_roadmaps (id, title, slug, description, total_levels, duration, icon) VALUES
(1, 'Python Programming', 'python', 'Comprehensive pathway from core Python syntax to object-oriented programming, data handling, and backend web APIs.', 3, '3 Months', 'fab fa-python'),
(2, 'Java Programming', 'java', 'Master modern Core Java, OOP design patterns, enterprise collections, and Spring Boot framework.', 3, '4 Months', 'fab fa-java'),
(3, 'HTML and CSS', 'html-css', 'Build pixel-perfect, accessible, and responsive user interfaces with modern CSS Grid, Flexbox, and animations.', 3, '2 Months', 'fab fa-html5'),
(4, 'JavaScript', 'javascript', 'Deep dive into asynchronous JavaScript, DOM manipulation, ES6+ syntax, and modern API communication.', 3, '3 Months', 'fab fa-js'),
(5, 'Full Stack Development', 'fullstack', 'End-to-end web engineering covering frontend UI, Python/Flask backend, relational databases, and secure deployment.', 3, '5 Months', 'fas fa-layer-group'),
(6, 'SQL & Relational Databases', 'sql', 'Master relational database modeling, complex JOINs, query optimization, indexing, and transactional integrity.', 3, '2 Months', 'fas fa-database'),
(7, 'Data Analytics', 'data-analytics', 'Learn data extraction with SQL, manipulation with Pandas, exploratory data analysis, and dashboard visualization with PowerBI.', 3, '4 Months', 'fas fa-chart-pie'),
(8, 'Artificial Intelligence & ML', 'ai-ml', 'Systematic path from linear algebra to scikit-learn, deep neural architectures, and natural language models.', 3, '6 Months', 'fas fa-robot')
ON DUPLICATE KEY UPDATE id=id;

-- Seed Roadmap Topics (Beginner, Intermediate, Advanced for all 8 roadmaps)
INSERT INTO roadmap_topics (id, roadmap_id, level, topic_title, description, practical_exercises, mini_project, learning_resources, order_index) VALUES
-- Python Roadmap
(1, 1, 'Beginner', 'Python Syntax, Variables & Control Flow', 'Master variables, data types (int, float, str, bool), operators, if-elif-else statements, and loops (for, while).', 'Write programs for prime number checks, Fibonacci series, and string palindrome verifications.', 'Command-Line Student Grade Calculator', 'Official Python Docs (docs.python.org), W3Schools Python', 1),
(2, 1, 'Beginner', 'Data Structures (Lists, Tuples, Dictionaries, Sets)', 'Understand in-memory collections, slicing, indexing, dictionary keys/values, and set operations.', 'Implement a phonebook directory using dictionaries and frequency counter for text files.', 'Terminal-Based Contact Book Application', 'Corey Schafer Python Collections Tutorial', 2),
(3, 1, 'Intermediate', 'Object-Oriented Programming (OOP) in Python', 'Classes, objects, constructors (__init__), encapsulation, inheritance, polymorphism, and magic methods.', 'Design a banking system hierarchy with Savings and Current account classes.', 'Library Book Management System', 'Real Python OOP Guide', 3),
(4, 1, 'Intermediate', 'File Handling, Modules & Exception Handling', 'Reading and writing CSV/JSON files, try-except-finally blocks, custom exceptions, and package management with pip.', 'Parse a CSV dataset, compute statistics, and handle invalid formatting gracefully.', 'CSV Data Report Generator with Logging', 'Automate the Boring Stuff with Python', 4),
(5, 1, 'Advanced', 'Flask Web Framework & REST APIs', 'Routing, request handling, Jinja templates, RESTful API design, HTTP methods, and JSON responses.', 'Build a REST API with GET, POST, PUT, DELETE endpoints connected to a database.', 'Full-featured Student Placement Portal API', 'Flask Official Quickstart Documentation', 5),
(6, 1, 'Advanced', 'Database Integration & Unit Testing', 'Using mysql-connector, parameterized queries, unit testing with unittest/pytest, and virtual environments.', 'Write automated test cases for user authentication and mock database calls.', 'Automated Placement Drive Management System', 'PyTest Documentation & Testing Best Practices', 6),

-- Java Roadmap
(7, 2, 'Beginner', 'Java Basics & Fundamentals', 'JDK/JRE architecture, JVM memory model, primitive types, loops, arrays, and standard input scanner.', 'Implement matrix multiplication, array sorting, and number guessing games.', 'Console Banking System', 'Java Programming on Oracle Docs, Telusko Java', 1),
(8, 2, 'Intermediate', 'OOP & Java Collections Framework', 'Interfaces, abstract classes, ArrayList, HashMap, HashSet, LinkedList, and Comparable/Comparator.', 'Sort custom Student objects by CGPA and Department using Collections.sort().', 'College Student Attendance & Record Tracker', 'Baeldung Java Collections Tutorials', 2),
(9, 2, 'Advanced', 'Spring Boot & RESTful Microservices', 'Dependency Injection, Spring Boot starters, Spring Data JPA, Hibernate ORM, and REST Controllers.', 'Build CRUD endpoints for employee management with MySQL persistence.', 'Online Course Registration REST API', 'Spring.io Official Getting Started Guides', 3),

-- HTML and CSS Roadmap
(10, 3, 'Beginner', 'Semantic HTML5 & Core CSS3', 'Semantic tags (header, nav, main, section, footer), forms, inputs, box model, colors, and typography.', 'Build a semantic personal portfolio page with contact forms and validated inputs.', 'Personal Resume & Portfolio Website', 'MDN Web Docs HTML & CSS Foundations', 1),
(11, 3, 'Intermediate', 'CSS Flexbox, Grid & Responsive Layouts', 'Master one-dimensional Flexbox, two-dimensional CSS Grid, media queries, and mobile-first design.', 'Create a responsive multi-column e-commerce product card grid with hover effects.', 'Responsive College Event Showcase Webpage', 'CSS Tricks Guide to Flexbox & CSS Grid', 2),
(12, 3, 'Advanced', 'CSS Animations, Variables & Modern Design', 'CSS Custom properties (variables), transitions, keyframe animations, glassmorphism, and dark mode.', 'Build an interactive dashboard theme switcher with smooth card flip animations.', 'Modern SaaS Product Landing Page', 'Modern CSS Solutions by Stephanie Eckles', 3),

-- JavaScript Roadmap
(13, 4, 'Beginner', 'JavaScript Basics & DOM Manipulation', 'Variables (let/const), functions, DOM selectors (querySelector), event listeners (click, change, submit).', 'Create an interactive task checklist with add, delete, and strike-through features.', 'Interactive To-Do & Task Manager App', 'JavaScript.info The Modern JS Tutorial', 1),
(14, 4, 'Intermediate', 'ES6+ Features & Asynchronous Programming', 'Arrow functions, destructuring, template literals, Promises, async/await, and Fetch API.', 'Fetch mock user data from JSONPlaceholder API and display in searchable cards.', 'Live Weather & Forecast Web App', 'MDN Async JavaScript Guide', 2),
(15, 4, 'Advanced', 'Form Validation, Web Storage & Modular JS', 'Client-side regex validation, localStorage, sessionStorage, modules (import/export), and error boundaries.', 'Persist multi-step user onboarding data in browser storage with instant validation.', 'Interactive Fresher Resume Builder with PDF Export', 'Frontend Masters JavaScript Hard Parts', 3),

-- Full Stack Roadmap
(16, 5, 'Beginner', 'Frontend Foundations & Backend Routing', 'Connecting HTML/CSS templates with Flask routes, dynamic Jinja rendering, and static asset management.', 'Create a dynamic multi-page website with shared navigation and active page highlights.', 'College Departmental Information Portal', 'Flask Mega-Tutorial by Miguel Grinberg', 1),
(17, 5, 'Intermediate', 'User Authentication, Sessions & MySQL', 'Password hashing with Werkzeug, user registration/login, session security, and relational queries.', 'Implement user login, signup with email verification logic, and protected routes.', 'Secure Campus Placement Registration Portal', 'Real Python Flask Authentication Guide', 2),
(18, 5, 'Advanced', 'Full-Stack CRUD, API Integration & Deployment', 'Full CRUD operations, REST API endpoints, search/filter functionality, error logging, and cloud deploy.', 'Build full lifecycle application with student dashboard, admin management, and MySQL database.', 'Complete Career Guidance & Placement Platform', 'DigitalOcean Python Flask Production Guide', 3),

-- SQL Roadmap
(19, 6, 'Beginner', 'SQL Foundations & Table Design', 'DDL/DML, CREATE, ALTER, INSERT, UPDATE, DELETE, SELECT, WHERE, ORDER BY, and LIMIT.', 'Write queries to filter students by department and graduation year.', 'College Library Database Schema', 'Mode Analytics SQL Tutorial for Beginners', 1),
(20, 6, 'Intermediate', 'Relational JOINS, Grouping & Aggregations', 'INNER JOIN, LEFT JOIN, RIGHT JOIN, COUNT, AVG, SUM, GROUP BY, HAVING, and subqueries.', 'Compute department-wise placement statistics and highest salary packages.', 'Placement Analytics Reporting Queries', 'W3Schools SQL Tutorial & LeetCode SQL 50', 2),
(21, 6, 'Advanced', 'Indexes, Transactions & Query Optimization', 'B-Tree indexes, EXPLAIN query plan, ACID transactions, foreign key constraints, and stored procedures.', 'Optimize slow search queries across 10,000+ mock records with indexing.', 'High-Performance E-commerce Order Ledger', 'Use The Index, Luke! SQL Indexing Guide', 3),

-- Data Analytics Roadmap
(22, 7, 'Beginner', 'Data Analysis with Excel & SQL', 'Advanced Excel functions (INDEX-MATCH, VLOOKUP, Pivot Tables), SQL data aggregation and export.', 'Analyze campus placement records in Excel and summarize by branch and package.', 'Campus Placement Summary Dashboard in Excel', 'Chandoo Excel & SQL Analytics Series', 1),
(23, 7, 'Intermediate', 'Python for Data Analysis (Pandas & NumPy)', 'DataFrames, Series, handling missing data, filtering, grouping, date parsing, and Matplotlib/Seaborn charts.', 'Clean a messy dataset of fresher job postings and plot salary distributions.', 'Fresher Hiring Market Trends Exploratory Report', 'Kaggle Python & Pandas Micro-Courses', 2),
(24, 7, 'Advanced', 'Interactive Business Intelligence Dashboards', 'Power BI / Tableau data modeling, DAX measures, interactive filters, KPI cards, and story creation.', 'Build an interactive 3-page placement performance dashboard for college management.', 'Interactive University Placement KPI Dashboard', 'Microsoft Power BI Guided Learning', 3),

-- AI & ML Roadmap
(25, 8, 'Beginner', 'Math & Statistics for Machine Learning', 'Linear algebra (matrices, vectors), probability distributions, descriptive statistics, and calculus basics.', 'Implement gradient descent from scratch for linear regression in Python.', 'Math Fundamentals for Data Science Workbook', 'Khan Academy Linear Algebra & 3Blue1Brown', 1),
(26, 8, 'Intermediate', 'Supervised & Unsupervised Machine Learning', 'Regression, Classification (Logistic, Decision Trees, Random Forest), Clustering (K-Means), and evaluation metrics.', 'Train models to predict student placement eligibility based on CGPA and coding score.', 'Student Placement Predictor Machine Learning Model', 'Scikit-Learn Official User Guide', 2),
(27, 8, 'Advanced', 'Deep Learning & Natural Language Processing', 'Neural networks, activation functions, backpropagation, CNNs for image classification, and text embeddings.', 'Build an automated resume keyword matcher comparing student skills to job descriptions.', 'AI-Powered Resume to Job Matcher Engine', 'DeepLearning.AI & Fast.ai Practical Deep Learning', 3)
ON DUPLICATE KEY UPDATE id=id;

-- Seed Skills (Technical & Soft Skills)
INSERT INTO skills (id, name, category, description, importance, how_to_improve, practice_activities, icon) VALUES
-- Technical Skills
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

-- Soft Skills
(11, 'Communication', 'soft', 'The ability to clearly, concisely, and persuasively convey technical and non-technical ideas.', 'Vital for clearing HR interviews, participating in group discussions, and team collaboration.', 'Practice speaking in English, record your self-introductions, and participate in technical seminars.', 'Conduct mock interviews with peers and explain a technical concept to a non-technical friend.', 'fas fa-comments'),
(12, 'Teamwork', 'soft', 'Collaborating harmoniously with peers towards a shared goal while respecting diverse viewpoints.', 'Software engineering is a team sport; recruiters prioritize team players over lone wolves.', 'Participate in college hackathons, group projects, and open-source contributions.', 'Work in a group of 3-4 students to build a full-stack semester project.', 'fas fa-users'),
(13, 'Time Management', 'soft', 'Prioritizing tasks and organizing time effectively to meet deadlines without unnecessary stress.', 'Crucial during final year for balancing academics, placement prep, and project deadlines.', 'Use techniques like the Pomodoro method, Eisenhower matrix, and digital calendars.', 'Create a weekly study timetable dividing time between coding, aptitude, and college work.', 'fas fa-clock'),
(14, 'Leadership', 'soft', 'Inspiring, guiding, and supporting others to accomplish collective milestones with accountability.', 'Differentiates exceptional candidates during group discussions and managerial rounds.', 'Take initiative in college clubs, student societies, or project team leadership.', 'Lead a team during an academic workshop, technical fest, or group assignment.', 'fas fa-flag'),
(15, 'Adaptability', 'soft', 'The capacity to adjust quickly to new technologies, changing project scopes, and unfamiliar environments.', 'Technology evolves rapidly; tech companies hire candidates who learn quickly.', 'Step out of your comfort zone, explore new programming paradigms, and welcome feedback.', 'Pick up a new framework or tool (e.g., Docker or Tailwind) over a weekend and build a mini-app.', 'fas fa-sync-alt'),
(16, 'Critical Thinking', 'soft', 'Objective analysis and logical evaluation of facts to form well-reasoned judgments and solutions.', 'Key for root-cause debugging, architectural choices, and behavioral interviews.', 'Question assumptions, evaluate trade-offs between approaches, and avoid cargo-cult programming.', 'Analyze the time/space trade-offs between two different sorting algorithms or system architectures.', 'fas fa-lightbulb'),
(17, 'Presentation Skills', 'soft', 'Structuring and delivering engaging visual and verbal presentations with confidence.', 'Essential for final year project defense, client demonstrations, and campus presentations.', 'Design clean slide decks, avoid walls of text, maintain eye contact, and practice pacing.', 'Deliver a 5-minute presentation on your semester project in front of your friends or mirror.', 'fas fa-chalkboard-teacher')
ON DUPLICATE KEY UPDATE id=id;

-- Seed Interview Questions (Technical, HR, Aptitude)
INSERT INTO interview_questions (id, category, subcategory, question, answer, explanation, difficulty) VALUES
-- Technical - Python
(1, 'technical', 'python', 'What is the difference between list and tuple in Python?', 'Lists are mutable (can be changed after creation), defined using square brackets [], while tuples are immutable (cannot be altered), defined using parentheses (). Tuples are faster and consume less memory.', 'Lists have methods like append(), extend(), and pop(). Tuples cannot be modified once declared, making them ideal for fixed configurations and dictionary keys.', 'Beginner'),
(2, 'technical', 'python', 'Explain Python''s memory management and garbage collection.', 'Python manages memory using a private heap space. It utilizes reference counting as its primary garbage collection mechanism, supplemented by a cyclic garbage collector to detect circular references.', 'When an object''s reference count drops to zero, Python deallocates the memory immediately. The gc module periodically scans for cyclic references.', 'Intermediate'),
(3, 'technical', 'python', 'What are decorators in Python and how do you use them?', 'Decorators are functions that take another function as an argument, extend or modify its behavior without modifying the original code, and return a callable.', 'Commonly used for logging, authentication, timing execution, and route definitions in Flask (e.g., @app.route).', 'Intermediate'),

-- Technical - Java
(4, 'technical', 'java', 'What are the main OOP concepts in Java?', 'The four primary pillars of OOP are: Encapsulation (data hiding via private variables and public getters/setters), Inheritance (code reuse via extends), Polymorphism (method overloading and overriding), and Abstraction (hiding implementation details via abstract classes and interfaces).', 'Every enterprise Java system relies on these pillars for modularity, maintainability, and clean architecture.', 'Beginner'),
(5, 'technical', 'java', 'What is the difference between HashMap and ConcurrentHashMap in Java?', 'HashMap is non-synchronized and not thread-safe. ConcurrentHashMap is thread-safe and allows concurrent read/write operations without locking the entire map by segmenting buckets.', 'In multi-threaded environments, HashMap can lead to infinite loops or corrupted state, whereas ConcurrentHashMap achieves high performance through lock striping.', 'Advanced'),

-- Technical - SQL
(6, 'technical', 'sql', 'What is the difference between WHERE and HAVING clause in SQL?', 'WHERE filters rows before any groupings are applied, and cannot contain aggregate functions. HAVING filters groups after GROUP BY aggregation, and can evaluate aggregate functions like COUNT(), SUM(), AVG().', 'Example: SELECT dept, COUNT(*) FROM emp WHERE salary > 30000 GROUP BY dept HAVING COUNT(*) > 5;', 'Beginner'),
(7, 'technical', 'sql', 'What are the different types of JOINs in SQL?', 'INNER JOIN (returns matching rows in both tables), LEFT JOIN (all rows from left table + matching from right), RIGHT JOIN (all from right + matching from left), and FULL OUTER JOIN (all rows when there is a match in either table).', 'Relational database integrity and query optimization heavily rely on choosing the appropriate JOIN type.', 'Beginner'),

-- Technical - HTML/CSS
(8, 'technical', 'html_css', 'What is the CSS Box Model and what are its components?', 'The CSS Box Model describes the rectangular box generated for elements. From inside out, it consists of: Content (text/images), Padding (space inside border), Border (line around padding), and Margin (transparent space outside border).', 'Setting box-sizing: border-box is modern best practice so width and height include padding and borders.', 'Beginner'),

-- Technical - JavaScript
(9, 'technical', 'javascript', 'Explain the difference between == and === in JavaScript.', '== is the loose equality operator that performs type coercion before comparison. === is the strict equality operator that checks both value and type without coercion.', 'Example: 5 == "5" is true, but 5 === "5" is false because one is number and the other is string.', 'Beginner'),
(10, 'technical', 'javascript', 'What is the Event Loop in JavaScript?', 'JavaScript is single-threaded. The event loop continuously monitors the Call Stack and the Callback/Task Queue. When the Call Stack is empty, it pushes pending callbacks from the queue onto the stack for execution.', 'This enables non-blocking asynchronous operations like setTimeout, Promise resolution, and AJAX requests.', 'Advanced'),

-- HR Questions
(11, 'hr', 'hr', 'Tell me about yourself.', 'Give a structured answer: 1. Present: State your name, college, degree, and current technical specialization. 2. Past: Highlight your key academic achievements, projects, or internships. 3. Future: Explain your passion for software development and why this company is the right step for your career.', 'Keep it concise (1.5 to 2 minutes). Do not repeat your resume line-by-line; focus on your enthusiasm and skills.', 'Beginner'),
(12, 'hr', 'hr', 'What are your greatest strengths and weaknesses?', 'Strength: Mention a work-relevant trait with evidence (e.g., fast learner, analytical problem solver, strong team collaborator). Weakness: Mention a genuine non-fatal developmental area along with the active steps you are taking to overcome it (e.g., getting nervous during large presentations, which you are improving by volunteering for seminar talks).', 'Never say "I have no weaknesses" or "I am a perfectionist" as those sound rehearsed.', 'Beginner'),
(13, 'hr', 'hr', 'Why should we hire you?', 'Align your skills with the company: "As a fresher, I bring strong computer science fundamentals in data structures, Python, and SQL, coupled with hands-on project experience building full-stack applications. I am enthusiastic, quick to adapt, and eager to contribute to your engineering culture."', 'Demonstrate enthusiasm, willingness to learn, and concrete project proof.', 'Beginner'),
(14, 'hr', 'hr', 'Where do you see yourself in 5 years?', '"In 5 years, I see myself as a seasoned software engineer who has developed deep technical expertise in building scalable systems. I want to have led significant feature modules, mentored incoming freshers, and contributed meaningfully to the company''s technological and business growth."', 'Shows ambition, loyalty, and career focus without appearing unrealistic.', 'Beginner'),
(15, 'hr', 'hr', 'Why do you want to join our company?', 'Research the company beforehand: Mention their products, engineering culture, innovation, or recent achievements. "I have followed your work in cloud and enterprise solutions, and I admire your commitment to employee learning and technological excellence. Working here offers me the ideal platform to solve impactful problems."', 'Shows you did your homework and did not just send a generic application.', 'Beginner'),

-- Aptitude - Quantitative
(16, 'aptitude', 'quantitative', 'A train 240 m long passes a pole in 24 seconds. How long will it take to pass a platform 650 m long?', 'Answer: 89 seconds.', 'Speed of train = Distance / Time = 240 / 24 = 10 m/s. Total distance to pass platform = length of train + length of platform = 240 + 650 = 890 m. Time taken = 890 / 10 = 89 seconds.', 'Beginner'),
(17, 'aptitude', 'quantitative', 'If the cost price of 20 articles is equal to the selling price of 16 articles, what is the profit percentage?', 'Answer: 25% profit.', 'Let CP of 1 article = Rs. 1. Then CP of 16 articles = Rs. 16. SP of 16 articles = CP of 20 articles = Rs. 20. Profit = 20 - 16 = Rs. 4. Profit % = (4 / 16) * 100 = 25%.', 'Beginner'),

-- Aptitude - Logical
(18, 'aptitude', 'logical', 'Look at this series: 2, 1, (1/2), (1/4), ... What number should come next?', 'Answer: 1/8.', 'This is a geometric division series. Each number is half of the previous number: 2 / 2 = 1, 1 / 2 = 1/2, (1/2) / 2 = 1/4, (1/4) / 2 = 1/8.', 'Beginner'),
(19, 'aptitude', 'logical', 'Pointing to a photograph of a boy, Suresh said, "He is the son of the only son of my mother." How is Suresh related to that boy?', 'Answer: Father.', 'Suresh''s mother''s only son is Suresh himself. So the boy is the son of Suresh. Hence, Suresh is the father of the boy.', 'Beginner'),

-- Aptitude - Verbal
(20, 'aptitude', 'verbal', 'Choose the correct synonym for CANDID: (A) Secretive (B) Frank (C) Shy (D) Dishonest', 'Answer: (B) Frank.', 'Candid means truthful, straightforward, and sincere in speech, which is synonymous with "frank".', 'Beginner'),
(21, 'aptitude', 'verbal', 'Select the correctly punctuated sentence: (A) Its raining outside. (B) It''s raining outside. (C) Its'' raining outside.', 'Answer: (B) It''s raining outside.', '"It''s" is the contraction for "it is", while "its" is a possessive pronoun.', 'Beginner')
ON DUPLICATE KEY UPDATE id=id;

-- Seed Sample Fresher Jobs & Internships
INSERT INTO job_opportunities (id, title, company_name, location, job_type, required_skills, eligibility, experience_level, description, salary_range, apply_url, is_verified) VALUES
(1, 'Associate Python Software Engineer', 'Cognitive Cloud Labs', 'Bengaluru / Hybrid', 'Full-time Fresher', 'Python, Flask/Django, SQL, Git, REST APIs', 'B.Tech/BE/BCA/MCA (2025/2026 Batch)', 'Fresher / 0-1 Year', 'Join our core platform engineering team to build scalable microservices and backend data pipelines.', 'INR 5.5 - 7.5 LPA', '#', TRUE),
(2, 'Graduate Java Developer Trainee', 'Enterprise Nexus Systems', 'Hyderabad / On-site', 'Full-time Fresher', 'Core Java, Spring Boot, OOP, MySQL', 'B.Tech CS/IT with min 65% aggregate', 'Fresher', 'Responsible for developing enterprise microservices, writing unit tests, and optimizing database queries.', 'INR 4.5 - 6.5 LPA', '#', TRUE),
(3, 'Web Development Intern (Frontend)', 'PixelCraft Studios', 'Remote', 'Internship', 'HTML5, CSS3, JavaScript, Responsive Design', 'Enrolled college students or recent graduates', 'Student / Fresher', 'Work closely with UI/UX designers to translate Figma prototypes into clean, responsive web pages.', 'INR 15,000 - 25,000 / month', '#', TRUE),
(4, 'Data Analytics Intern', 'InsightWave Analytics', 'Pune / Hybrid', 'Internship', 'SQL, Excel, Python (Pandas), Power BI', 'B.Tech / B.Sc / BCA / BBA (Final Year)', 'Fresher', 'Analyze customer behavioral data, create interactive weekly dashboards, and present insights to stakeholders.', 'INR 18,000 - 28,000 / month', '#', TRUE),
(5, 'Junior QA Automation Engineer', 'TestArmor Solutions', 'Chennai / On-site', 'Full-time Fresher', 'Manual Testing, Selenium, Java/Python, SQL', 'Any Engineering or Computer Application graduate', '0-1 Year', 'Design comprehensive test plans, automate regression test suites, and report defects using JIRA.', 'INR 4.0 - 5.5 LPA', '#', TRUE),
(6, 'Cloud & DevOps Associate', 'SkyScale Technologies', 'Gurugram / Hybrid', 'Full-time Fresher', 'Linux, AWS basics, Docker, Bash Scripting', 'B.Tech in CS/IT/ECE (2025/2026)', 'Fresher', 'Support deployment automation pipelines, monitor cloud infrastructure, and maintain containerized workloads.', 'INR 6.0 - 8.5 LPA', '#', TRUE)
ON DUPLICATE KEY UPDATE id=id;
