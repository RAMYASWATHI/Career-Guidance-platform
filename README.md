# CAREER GUIDANCE PLATFORM
> **"Explore Your Skills, Discover Your Career, Build Your Future."**

A full-stack web application designed especially for college students, final-year engineering scholars, and freshers who are confused about choosing their career paths and preparing for campus placements.

---

## 🌟 Key Highlights & Features

1. **Intelligent Career Assessment**: Multi-dimensional algorithmic questionnaire evaluating programming interests, problem solving, mathematics, and career ambitions to calculate match scores across 10 in-demand tech roles.
2. **10 In-Demand Tech Career Tracks**:
   - Python Developer
   - Java Developer
   - Web Developer
   - Full Stack Developer
   - Software Tester (QA)
   - Data Analyst
   - Data Scientist
   - AI / ML Engineer
   - Cloud & DevOps Engineer
   - Cybersecurity Analyst
3. **8 Tiered Learning Roadmaps**: Python, Java, HTML/CSS, JavaScript, Full Stack, SQL, Data Analytics, and AI/ML divided into Beginner, Intermediate, and Advanced milestones with practical exercises and mini-projects.
4. **Interactive Topic Tracking**: Students can mark roadmap topics as completed; progress percentages update dynamically via AJAX and persist in MySQL.
5. **Technical & Soft Skills Framework**: 10 core technical disciplines and 7 vital soft skills with explanations, importance, and daily practice routines.
6. **Fresher Interview Preparation Bank**: Curated technical questions (Python, Java, SQL, HTML/CSS, JS), winning HR interview answers, and aptitude solutions (Quantitative, Logical, Verbal).
7. **Fresher Resume Builder**: Live interactive ATS-compliant resume builder with instant preview and print/PDF export.
8. **Fresher Jobs & Internships**: Verified entry-level opportunities with domain filters, eligibility criteria, and application modal.
9. **Role-Based Admin Dashboard**: Administrators can monitor registered students, manage career tracks, add interview questions, and post fresher openings.

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3 (Modern Vanilla Design System with Blue, White & Light-Purple theme), JavaScript (ES6+).
- **Backend**: Python 3, Flask Framework.
- **Database**: MySQL (`career_guidance_db`) with parameterized queries protecting against SQL injection, foreign keys, and cascading relationships.
- **Security**: Werkzeug scrypt password hashing, session-based role authorization, CSRF-safe forms.

---

## 📁 Project Structure

```text
career_guidance_platform/
│
├── app.py                     # Main application entry point & blueprint registration
├── config.py                  # Environment and secret configuration
├── requirements.txt           # Python dependencies (Flask, PyMySQL, etc.)
├── database.sql               # Complete MySQL schema and seed data
├── .env.example               # Example environment variables
├── .env                       # Active environment configuration
│
├── database/
│   └── db.py                  # Database connection manager with parameterized queries
│
├── routes/
│   ├── auth.py                # Student registration, login, logout, password hashing
│   ├── student.py             # Dashboard, profile updates, assessment, progress tracking
│   ├── career.py              # Landing, careers, roadmaps, skills, interview, resume, jobs
│   └── admin.py               # Administrative control panel and student records
│
├── services/
│   └── recommendation.py      # Career recommendation evaluation algorithm
│
├── static/
│   ├── css/
│   │   └── style.css          # Design system, CSS variables, responsive grid, animations
│   ├── js/
│   │   └── script.js          # Client script: AJAX topic toggling, filters, resume preview
│   └── images/                # Static assets & icons
│
└── templates/
    ├── base.html              # Base layout with navbar, flash messages, and footer
    ├── index.html             # Landing page with hero, categories, and workflow
    ├── about.html             # About project & technical architecture
    ├── contact.html           # Student inquiry & campus support form
    ├── register.html          # Student account registration form
    ├── login.html             # Authentication page with demo credentials
    ├── dashboard.html         # Personalized student dashboard & progress tracking
    ├── career_assessment.html # 7-question interactive assessment questionnaire
    ├── career_results.html    # Assessment recommendation results & skill breakdown
    ├── careers.html           # 10 career cards with search & domain filters
    ├── career_detail.html     # Single career track in-depth guide
    ├── roadmap.html           # Tiered roadmap with interactive checkboxes
    ├── skills.html            # Technical & Soft skills frameworks
    ├── interview.html         # Technical, HR & Aptitude question bank
    ├── resume.html            # Fresher resume guide & live interactive builder
    ├── jobs.html              # Verified fresher jobs & internship directory
    └── admin_dashboard.html   # Admin panel for student and platform management
```

---

## 🚀 How to Run on Windows

### 1. Prerequisites
Ensure you have Python 3.10+ and MySQL installed.
```powershell
python --version
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Setup MySQL Database
Open MySQL Workbench or the MySQL Command Line Client, and run:
```sql
SOURCE database.sql;
```
Or configure your `.env` file with your MySQL root password:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_mysql_password
DB_NAME=career_guidance_db
```

### 4. Start the Application
```powershell
python app.py
```
Open your browser and navigate to:
**`http://127.0.0.1:5000`**

---
## Demo Access
Demo login credentials are provided seperately for authorized evaluators.

---
*Created as a B.Tech Computer Science Capstone Project.*
