from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import query_db

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id') or session.get('role') != 'admin':
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/admin')
@admin_required
def admin_panel():
    """Render comprehensive administration panel with metrics and management tables."""
    # Fetch registered students with profiles
    students = query_db("""
        SELECT u.id, u.full_name, u.email, u.role, u.created_at,
               p.college_name, p.degree, p.department, p.graduation_year, p.selected_career
        FROM users u
        LEFT JOIN student_profiles p ON u.id = p.user_id
        ORDER BY u.id DESC
    """)

    # Metric counts
    careers_count_row = query_db("SELECT COUNT(*) as cnt FROM careers", one=True)
    careers_count = careers_count_row['cnt'] if careers_count_row else 0

    topics_count_row = query_db("SELECT COUNT(*) as cnt FROM roadmap_topics", one=True)
    topics_count = topics_count_row['cnt'] if topics_count_row else 0

    questions_count_row = query_db("SELECT COUNT(*) as cnt FROM interview_questions", one=True)
    questions_count = questions_count_row['cnt'] if questions_count_row else 0

    return render_template(
        'admin_dashboard.html',
        students=students,
        careers_count=careers_count,
        topics_count=topics_count,
        questions_count=questions_count
    )


@admin_bp.route('/admin/student/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_student(user_id):
    """Remove student record."""
    if user_id == session.get('user_id'):
        flash('You cannot delete your own administrative account.', 'warning')
        return redirect(url_for('admin.admin_panel'))

    query_db("DELETE FROM users WHERE id = %s", (user_id,), commit=True)
    flash(f'Student record #{user_id} has been permanently deleted.', 'success')
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route('/admin/career/add', methods=['POST'])
@admin_required
def add_career():
    """Add a new career path to the platform."""
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    required_skills = request.form.get('required_skills', '').strip()
    average_salary = request.form.get('average_salary', '').strip()
    
    if not title or not category or not description:
        flash('Please fill in all mandatory career fields.', 'warning')
        return redirect(url_for('admin.admin_panel'))

    query_db(
        """INSERT INTO careers 
           (title, category, description, required_skills, tools_technologies, eligibility, learning_path, job_opportunities, average_salary, icon)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            title, category, description, required_skills,
            'VS Code, Git, Standard Tooling',
            'B.Tech / BCA / MCA Freshers',
            'Fundamentals -> Core Framework -> Projects',
            f'Associate {title}, Junior {title}',
            average_salary,
            'fas fa-briefcase'
        ),
        commit=True
    )
    flash(f'Career path "{title}" successfully added!', 'success')
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route('/admin/job/add', methods=['POST'])
@admin_required
def add_job():
    """Add new job or internship opportunity."""
    title = request.form.get('title', '').strip()
    company_name = request.form.get('company_name', '').strip()
    location = request.form.get('location', '').strip()
    job_type = request.form.get('job_type', 'Full-time Fresher')
    salary_range = request.form.get('salary_range', '').strip()
    required_skills = request.form.get('required_skills', '').strip()
    description = request.form.get('description', '').strip()

    if not title or not company_name or not required_skills:
        flash('Please fill in the essential job information.', 'warning')
        return redirect(url_for('admin.admin_panel'))

    query_db(
        """INSERT INTO job_opportunities 
           (title, company_name, location, job_type, required_skills, eligibility, experience_level, description, salary_range, apply_url, is_verified)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            title, company_name, location, job_type, required_skills,
            'B.Tech / BCA / MCA (2025/2026 Batch)',
            'Fresher / 0-1 Year',
            description, salary_range, '#', True
        ),
        commit=True
    )
    flash(f'Job listing for "{title}" at {company_name} posted successfully!', 'success')
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route('/admin/interview/add', methods=['POST'])
@admin_required
def add_interview_question():
    """Add a new interview question to the bank."""
    category = request.form.get('category', 'technical')
    subcategory = request.form.get('subcategory', '').strip().lower()
    question = request.form.get('question', '').strip()
    answer = request.form.get('answer', '').strip()
    explanation = request.form.get('explanation', '').strip()

    if not question or not answer:
        flash('Question and Answer text are required.', 'warning')
        return redirect(url_for('admin.admin_panel'))

    query_db(
        """INSERT INTO interview_questions 
           (category, subcategory, question, answer, explanation, difficulty)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (category, subcategory, question, answer, explanation, 'Beginner'),
        commit=True
    )
    flash('New interview question added successfully to the knowledge bank!', 'success')
    return redirect(url_for('admin.admin_panel'))
