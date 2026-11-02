"""
Career Recommendation Service
Evaluates multi-dimensional questionnaire responses to generate personalized career paths.
"""

# Assessment Questions Definition
ASSESSMENT_QUESTIONS = [
    {
        "id": "q1",
        "category": "Interests & Passion",
        "question": "What kind of technological challenges excite you the most?",
        "options": [
            {"value": "web_ui", "text": "Crafting beautiful, modern, and interactive user interfaces for websites."},
            {"value": "backend_logic", "text": "Designing robust server-side algorithms, business logic, and databases."},
            {"value": "data_stats", "text": "Exploring complex data, discovering hidden patterns, and building charts."},
            {"value": "ai_models", "text": "Experimenting with artificial intelligence, neural networks, and automation."},
            {"value": "qa_testing", "text": "Hunting down bugs, testing edge cases, and ensuring software perfection."},
            {"value": "security_cloud", "text": "Securing digital networks, ethical hacking, and automating cloud servers."}
        ]
    },
    {
        "id": "q2",
        "category": "Technical Knowledge",
        "question": "Which programming language or technology are you most comfortable with or eager to master?",
        "options": [
            {"value": "python", "text": "Python (Simple syntax, great for backend, automation, and data)."},
            {"value": "java", "text": "Java (Strict object-oriented principles, enterprise standards)."},
            {"value": "javascript", "text": "HTML, CSS & JavaScript (Immediate visual feedback in the browser)."},
            {"value": "sql_excel", "text": "SQL, Excel, and database query manipulation."},
            {"value": "testing_tools", "text": "Manual testing, test cases, Postman, or Selenium."},
            {"value": "linux_networks", "text": "Linux operating system, terminal commands, and networking protocols."}
        ]
    },
    {
        "id": "q3",
        "category": "Problem-Solving Style",
        "question": "When faced with a complex software task, how do you approach it?",
        "options": [
            {"value": "visual_user", "text": "I sketch out the user workflow and build a clickable, visually appealing prototype."},
            {"value": "system_arch", "text": "I break the problem into modular classes, functions, and relational database schemas."},
            {"value": "math_data", "text": "I analyze the numbers, compute statistical metrics, and look for correlations."},
            {"value": "investigative", "text": "I systematically stress-test inputs, identify vulnerable paths, and verify boundaries."},
            {"value": "infra_pipes", "text": "I think about scalability, environment setup, and zero-downtime automation."}
        ]
    },
    {
        "id": "q4",
        "category": "Mathematical & Analytical Interest",
        "question": "How do you feel about mathematics, probability, and statistics?",
        "options": [
            {"value": "love_math", "text": "I love math and statistics! Linear algebra and predictive formulas fascinate me."},
            {"value": "practical_math", "text": "I prefer practical numbers like business metrics, averages, percentages, and KPIs."},
            {"value": "logic_math", "text": "I prefer pure logical deduction and algorithmic logic over complex math formulas."},
            {"value": "low_math", "text": "I prefer focusing on visual design, user experience, and styling rather than math."}
        ]
    },
    {
        "id": "q5",
        "category": "Work Preferences",
        "question": "Which final-year capstone project would you be most proud to present to campus recruiters?",
        "options": [
            {"value": "fullstack_app", "text": "An end-to-end web portal with user authentication, dashboard, and database."},
            {"value": "ml_predictor", "text": "An intelligent predictive AI engine trained on a real-world dataset."},
            {"value": "bi_dashboard", "text": "An interactive business intelligence analytics dashboard with data insights."},
            {"value": "automation_suite", "text": "A robust automated test framework validating a live web application."},
            {"value": "cloud_security", "text": "A secure, containerized cloud infrastructure pipeline with vulnerability scanning."}
        ]
    },
    {
        "id": "q6",
        "category": "Soft Skills & Team Role",
        "question": "In a team project, which role do you naturally gravitate towards?",
        "options": [
            {"value": "frontend_designer", "text": "The UI designer and frontend builder who makes everything look sleek."},
            {"value": "core_coder", "text": "The core programmer handling database connections and backend APIs."},
            {"value": "analyst_story", "text": "The data storyteller translating findings into clear slides for stakeholders."},
            {"value": "qa_gatekeeper", "text": "The quality guardian who reviews code, finds flaws, and ensures requirements are met."},
            {"value": "system_admin", "text": "The coordinator who sets up GitHub repositories, deployments, and servers."}
        ]
    },
    {
        "id": "q7",
        "category": "Career Ambition",
        "question": "What is your primary career goal for your first job as a fresher?",
        "options": [
            {"value": "goal_web", "text": "Become a versatile Web / Frontend Developer creating intuitive user applications."},
            {"value": "goal_backend", "text": "Become a high-performing Backend / Full Stack Developer at a top tech company."},
            {"value": "goal_data", "text": "Become a Data Analyst / Data Scientist making sense of corporate big data."},
            {"value": "goal_ai", "text": "Become an AI/ML Engineer building next-generation intelligent applications."},
            {"value": "goal_qa", "text": "Become a Software Tester / QA Automation Engineer ensuring product reliability."},
            {"value": "goal_security", "text": "Become a Cybersecurity Analyst or Cloud DevOps Engineer safeguarding systems."}
        ]
    }
]

CAREER_PROFILES = {
    "Python Developer": {
        "slug": "python",
        "category": "Software Engineering",
        "match_reason": "You have a natural flair for clean programming logic, modular backend design, and versatile application scripting. Python provides you with an ideal springboard for backend web services, automation, and high-demand tech roles.",
        "technical_skills": "Python, OOP, Data Structures, Flask/Django, SQL, REST APIs, Git",
        "soft_skills": "Logical Thinking, Code Readability, Problem Solving, Continuous Learning",
        "learning_roadmap": "Python Programming",
        "roadmap_slug": "python"
    },
    "Java Developer": {
        "slug": "java",
        "category": "Software Engineering",
        "match_reason": "You excel in structured object-oriented thinking, robust enterprise architecture, and high-performance server systems. Java's massive presence in campus recruitment drives makes this a premier career path for you.",
        "technical_skills": "Core Java, OOP Concepts, Java Collections, Spring Boot, MySQL, Multithreading",
        "soft_skills": "Analytical Rigor, Structured Thinking, Team Collaboration, Persistence",
        "learning_roadmap": "Java Programming",
        "roadmap_slug": "java"
    },
    "Web Developer": {
        "slug": "html-css",
        "category": "Web & Mobile",
        "match_reason": "You have an eye for visual aesthetics, intuitive user interfaces, and engaging digital interactions. Web development lets you transform creative design ideas into functional web experiences that users love.",
        "technical_skills": "HTML5, CSS3, JavaScript (ES6+), Responsive Design, CSS Flexbox & Grid, Git",
        "soft_skills": "Creativity, Attention to Visual Detail, Empathy for Users, Effective Communication",
        "learning_roadmap": "HTML and CSS",
        "roadmap_slug": "html-css"
    },
    "Full Stack Developer": {
        "slug": "fullstack",
        "category": "Software Engineering",
        "match_reason": "You enjoy the big picture: connecting beautiful frontends with robust backend APIs and efficient databases. Full-stack engineers are among the most versatile and highly recruited candidates on campus.",
        "technical_skills": "HTML/CSS/JavaScript, Python/Flask or Node.js, SQL Databases, REST APIs, Git",
        "soft_skills": "Versatility, End-to-End Problem Solving, Time Management, Adaptability",
        "learning_roadmap": "Full Stack Development",
        "roadmap_slug": "fullstack"
    },
    "Software Tester": {
        "slug": "software-tester",
        "category": "Quality Assurance",
        "match_reason": "You possess sharp observation skills, methodical analytical thinking, and a dedication to high quality. You enjoy breaking systems to find vulnerabilities and ensuring end-users receive flawless software.",
        "technical_skills": "Manual Testing, Test Case Design, STLC, Selenium WebDriver, Postman API Testing, SQL",
        "soft_skills": "Critical Thinking, Attention to Detail, Inquisitive Mindset, Clear Documentation",
        "learning_roadmap": "Full Stack Development",
        "roadmap_slug": "fullstack"
    },
    "Data Analyst": {
        "slug": "data-analytics",
        "category": "Data & Analytics",
        "match_reason": "You enjoy solving business puzzles with quantitative evidence. You excel at turning spreadsheets and SQL databases into crystal-clear visual stories and actionable business strategies.",
        "technical_skills": "SQL, Excel (Pivot/VLOOKUP), Python (Pandas/NumPy), Power BI / Tableau, Data Cleaning",
        "soft_skills": "Data Storytelling, Commercial Awareness, Active Listening, Clear Presentation",
        "learning_roadmap": "Data Analytics",
        "roadmap_slug": "data-analytics"
    },
    "Data Scientist": {
        "slug": "data-scientist",
        "category": "Data Science & AI",
        "match_reason": "You love deep analytical inquiry, statistical modeling, and algorithmic predictions. You possess the intellectual curiosity needed to extract predictive signals from large datasets.",
        "technical_skills": "Python, Linear Algebra & Probability, Scikit-Learn, Pandas, Statistical Modeling, SQL",
        "soft_skills": "Hypothesis Formulation, Curiosity, Research Mindset, Persuasive Communication",
        "learning_roadmap": "Data Analytics",
        "roadmap_slug": "data-analytics"
    },
    "AI/ML Engineer": {
        "slug": "ai-ml",
        "category": "Artificial Intelligence",
        "match_reason": "You are fascinated by the frontier of artificial intelligence, intelligent systems, and neural networks. Your ambition to build self-learning algorithms aligns perfectly with an AI/ML engineering trajectory.",
        "technical_skills": "Python, Machine Learning Algorithms, Deep Learning, PyTorch / TensorFlow, Math for ML",
        "soft_skills": "Abstract Thinking, Experimental Persistence, Continuous Innovation, Problem Decomposition",
        "learning_roadmap": "Artificial Intelligence & ML",
        "roadmap_slug": "ai-ml"
    },
    "Cloud Engineer": {
        "slug": "cloud-engineer",
        "category": "Cloud & DevOps",
        "match_reason": "You enjoy systems architecture, automation, operating system internals, and cloud networks. Cloud engineers keep the internet running smoothly, making this a future-proof, high-growth discipline.",
        "technical_skills": "Linux Administration, Networking Fundamentals, AWS/Azure, Docker Containers, Bash, CI/CD",
        "soft_skills": "Systems Thinking, Operational Calm, Troubleshooting, Team Coordination",
        "learning_roadmap": "Full Stack Development",
        "roadmap_slug": "fullstack"
    },
    "Cybersecurity Analyst": {
        "slug": "cybersecurity",
        "category": "Information Security",
        "match_reason": "You possess a protective, investigative mindset intrigued by security vulnerabilities, cryptography, and defense mechanisms. Protecting vital systems against cyber threats is both noble and in extreme demand.",
        "technical_skills": "Network Security (TCP/IP), Cryptography, Linux, Vulnerability Assessment, Wireshark, Nmap",
        "soft_skills": "Ethical Judgment, High Integrity, Forensic Curiosity, Stress Management",
        "learning_roadmap": "Full Stack Development",
        "roadmap_slug": "fullstack"
    }
}

def evaluate_assessment(answers):
    """
    Evaluates form responses and returns top recommended career and breakdown scores.
    answers: dict of {question_id: selected_value}
    """
    scores = {career: 10 for career in CAREER_PROFILES.keys()}
    
    # Q1: Interests & Passion
    q1 = answers.get("q1")
    if q1 == "web_ui":
        scores["Web Developer"] += 35
        scores["Full Stack Developer"] += 20
    elif q1 == "backend_logic":
        scores["Python Developer"] += 30
        scores["Java Developer"] += 30
        scores["Full Stack Developer"] += 25
    elif q1 == "data_stats":
        scores["Data Analyst"] += 35
        scores["Data Scientist"] += 30
    elif q1 == "ai_models":
        scores["AI/ML Engineer"] += 40
        scores["Data Scientist"] += 30
    elif q1 == "qa_testing":
        scores["Software Tester"] += 40
    elif q1 == "security_cloud":
        scores["Cybersecurity Analyst"] += 35
        scores["Cloud Engineer"] += 35

    # Q2: Technical Knowledge
    q2 = answers.get("q2")
    if q2 == "python":
        scores["Python Developer"] += 30
        scores["AI/ML Engineer"] += 25
        scores["Data Scientist"] += 25
    elif q2 == "java":
        scores["Java Developer"] += 35
        scores["Full Stack Developer"] += 15
    elif q2 == "javascript":
        scores["Web Developer"] += 35
        scores["Full Stack Developer"] += 25
    elif q2 == "sql_excel":
        scores["Data Analyst"] += 35
        scores["Data Scientist"] += 15
    elif q2 == "testing_tools":
        scores["Software Tester"] += 35
    elif q2 == "linux_networks":
        scores["Cloud Engineer"] += 35
        scores["Cybersecurity Analyst"] += 35

    # Q3: Problem-Solving Style
    q3 = answers.get("q3")
    if q3 == "visual_user":
        scores["Web Developer"] += 25
        scores["Full Stack Developer"] += 15
    elif q3 == "system_arch":
        scores["Java Developer"] += 25
        scores["Python Developer"] += 25
        scores["Full Stack Developer"] += 20
    elif q3 == "math_data":
        scores["Data Analyst"] += 25
        scores["Data Scientist"] += 25
        scores["AI/ML Engineer"] += 20
    elif q3 == "investigative":
        scores["Software Tester"] += 30
        scores["Cybersecurity Analyst"] += 25
    elif q3 == "infra_pipes":
        scores["Cloud Engineer"] += 30

    # Q4: Math & Analytical Interest
    q4 = answers.get("q4")
    if q4 == "love_math":
        scores["Data Scientist"] += 25
        scores["AI/ML Engineer"] += 25
    elif q4 == "practical_math":
        scores["Data Analyst"] += 25
        scores["Python Developer"] += 10
    elif q4 == "logic_math":
        scores["Java Developer"] += 20
        scores["Python Developer"] += 20
        scores["Full Stack Developer"] += 15
    elif q4 == "low_math":
        scores["Web Developer"] += 25
        scores["Software Tester"] += 15

    # Q5: Final Project Preference
    q5 = answers.get("q5")
    if q5 == "fullstack_app":
        scores["Full Stack Developer"] += 30
        scores["Web Developer"] += 20
        scores["Python Developer"] += 20
    elif q5 == "ml_predictor":
        scores["AI/ML Engineer"] += 30
        scores["Data Scientist"] += 25
    elif q5 == "bi_dashboard":
        scores["Data Analyst"] += 30
    elif q5 == "automation_suite":
        scores["Software Tester"] += 30
    elif q5 == "cloud_security":
        scores["Cybersecurity Analyst"] += 25
        scores["Cloud Engineer"] += 25

    # Q6: Team Role
    q6 = answers.get("q6")
    if q6 == "frontend_designer":
        scores["Web Developer"] += 25
    elif q6 == "core_coder":
        scores["Python Developer"] += 20
        scores["Java Developer"] += 20
        scores["Full Stack Developer"] += 20
    elif q6 == "analyst_story":
        scores["Data Analyst"] += 25
    elif q6 == "qa_gatekeeper":
        scores["Software Tester"] += 25
    elif q6 == "system_admin":
        scores["Cloud Engineer"] += 25

    # Q7: Ambition
    q7 = answers.get("q7")
    if q7 == "goal_web":
        scores["Web Developer"] += 35
    elif q7 == "goal_backend":
        scores["Python Developer"] += 25
        scores["Java Developer"] += 25
        scores["Full Stack Developer"] += 30
    elif q7 == "goal_data":
        scores["Data Analyst"] += 30
        scores["Data Scientist"] += 25
    elif q7 == "goal_ai":
        scores["AI/ML Engineer"] += 35
    elif q7 == "goal_qa":
        scores["Software Tester"] += 35
    elif q7 == "goal_security":
        scores["Cybersecurity Analyst"] += 30
        scores["Cloud Engineer"] += 30

    # Sort careers by score descending
    sorted_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_career_name = sorted_careers[0][0]
    top_profile = CAREER_PROFILES.get(top_career_name, {})
    
    # Calculate percentage match relative to max possible score (~200)
    max_score = sorted_careers[0][1]
    results_breakdown = []
    for c_name, c_score in sorted_careers[:4]:
        pct = min(98, max(50, int((c_score / (max_score + 10)) * 96)))
        results_breakdown.append({
            "career": c_name,
            "score": c_score,
            "match_percent": pct,
            "category": CAREER_PROFILES[c_name]["category"],
            "roadmap_slug": CAREER_PROFILES[c_name]["roadmap_slug"]
        })

    return {
        "recommended_career": top_career_name,
        "match_reason": top_profile.get("match_reason", "Strong alignment with your technical interests and career preferences."),
        "technical_skills": top_profile.get("technical_skills", ""),
        "soft_skills": top_profile.get("soft_skills", ""),
        "learning_roadmap": top_profile.get("learning_roadmap", "Full Stack Development"),
        "roadmap_slug": top_profile.get("roadmap_slug", "fullstack"),
        "match_percent": results_breakdown[0]["match_percent"],
        "top_rankings": results_breakdown,
        "all_scores": scores
    }
