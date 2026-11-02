import json
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database.db import query_db
from services.recommendation import ASSESSMENT_QUESTIONS, evaluate_assessment

student_bp = Blueprint('student', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access your student dashboard and features.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@student_bp.route('/dashboard')
@login_required
def dashboard():
    """Render personalized student dashboard with profile, progress, and recommendations."""
    user_id = session.get('user_id')
    
    # Fetch student and profile records
    student = query_db("SELECT id, full_name, email, role FROM users WHERE id = %s", (user_id,), one=True)
    profile = query_db("SELECT * FROM student_profiles WHERE user_id = %s", (user_id,), one=True)
    
    if not profile:
        # Create default empty profile if none exists
        query_db("INSERT INTO student_profiles (user_id, selected_career) VALUES (%s, %s)", (user_id, 'Undecided'), commit=True)
        profile = query_db("SELECT * FROM student_profiles WHERE user_id = %s", (user_id,), one=True)

    # Fetch latest career assessment
    latest_assessment = query_db(
        "SELECT * FROM career_assessments WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
        (user_id,), one=True
    )

    # Calculate overall roadmap topic completion
    total_topics_row = query_db("SELECT COUNT(*) as total FROM roadmap_topics", one=True)
    total_topics_count = total_topics_row['total'] if total_topics_row else 1
    
    completed_topics_row = query_db(
        "SELECT COUNT(*) as completed FROM student_progress WHERE user_id = %s AND is_completed = TRUE",
        (user_id,), one=True
    )
    completed_topics_count = completed_topics_row['completed'] if completed_topics_row else 0
    progress_pct = int((completed_topics_count / max(1, total_topics_count)) * 100)

    # Fetch all careers for dropdown
    all_careers = query_db("SELECT id, title FROM careers ORDER BY title ASC")

    # Fetch active roadmaps
    active_roadmaps = query_db("SELECT * FROM learning_roadmaps LIMIT 3")

    # Fetch sample jobs
    sample_jobs = query_db("SELECT * FROM job_opportunities LIMIT 3")
    jobs_count_row = query_db("SELECT COUNT(*) as cnt FROM job_opportunities", one=True)
    jobs_count = jobs_count_row['cnt'] if jobs_count_row else 0

    return render_template(
        'dashboard.html',
        student=student,
        profile=profile,
        latest_assessment=latest_assessment,
        all_careers=all_careers,
        active_roadmaps=active_roadmaps,
        sample_jobs=sample_jobs,
        jobs_count=jobs_count,
        total_topics_count=total_topics_count,
        completed_topics_count=completed_topics_count,
        progress_pct=progress_pct
    )


@student_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update student education details, current skills, bio, and target career."""
    user_id = session.get('user_id')
    college_name = request.form.get('college_name', '').strip()
    selected_career = request.form.get('selected_career', '').strip()
    degree = request.form.get('degree', '').strip()
    department = request.form.get('department', '').strip()
    current_skills = request.form.get('current_skills', '').strip()
    bio = request.form.get('bio', '').strip()

    query_db(
        """UPDATE student_profiles 
           SET college_name = %s, selected_career = %s, degree = %s, department = %s, current_skills = %s, bio = %s 
           WHERE user_id = %s""",
        (college_name, selected_career, degree, department, current_skills, bio, user_id),
        commit=True
    )

    flash('Your student profile has been updated successfully!', 'success')
    return redirect(url_for('student.dashboard'))


@student_bp.route('/career-assessment')
def career_assessment_view():
    """Render interactive career assessment questionnaire."""
    return render_template('career_assessment.html', questions=ASSESSMENT_QUESTIONS)


@student_bp.route('/career-assessment/submit', methods=['POST'])
def career_assessment_submit():
    """Process assessment answers and generate tailored recommendation."""
    answers = {}
    for q in ASSESSMENT_QUESTIONS:
        val = request.form.get(q['id'])
        if val:
            answers[q['id']] = val

    if not answers:
        flash('Please complete the questionnaire to receive your recommendation.', 'warning')
        return redirect(url_for('student.career_assessment_view'))

    # Run recommendation algorithm
    results = evaluate_assessment(answers)
    scores_json_str = json.dumps(results['all_scores'])

    user_id = session.get('user_id')
    assessment_id = None

    if user_id:
        try:
            assessment_id = query_db(
                """INSERT INTO career_assessments 
                   (user_id, scores_json, recommended_career, match_reason, technical_skills, soft_skills, learning_roadmap) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    user_id,
                    scores_json_str,
                    results['recommended_career'],
                    results['match_reason'],
                    results['technical_skills'],
                    results['soft_skills'],
                    results['learning_roadmap']
                ),
                commit=True
            )
            # Update target career in student profile if undecided
            query_db(
                "UPDATE student_profiles SET selected_career = %s WHERE user_id = %s AND (selected_career IS NULL OR selected_career = 'Undecided')",
                (results['recommended_career'], user_id),
                commit=True
            )
        except Exception as e:
            print(f"[Assessment DB Save Error]: {e}")

    # Pass in session for guest view or redirect to assessment result
    session['temp_results'] = results
    if assessment_id:
        return redirect(url_for('student.career_results', assessment_id=assessment_id))
    else:
        return redirect(url_for('student.career_results', assessment_id=0))


@student_bp.route('/career-results')
@student_bp.route('/career-results/<int:assessment_id>')
def career_results(assessment_id=0):
    """Render assessment results with reasons, technical & soft skills, and roadmap."""
    assessment = None
    if assessment_id > 0:
        assessment = query_db("SELECT * FROM career_assessments WHERE id = %s", (assessment_id,), one=True)

    top_rankings = []
    match_percent = 96
    roadmap_slug = 'python'

    if not assessment and 'temp_results' in session:
        temp = session['temp_results']
        assessment = {
            'recommended_career': temp['recommended_career'],
            'match_reason': temp['match_reason'],
            'technical_skills': temp['technical_skills'],
            'soft_skills': temp['soft_skills'],
            'learning_roadmap': temp['learning_roadmap']
        }
        top_rankings = temp.get('top_rankings', [])
        match_percent = temp.get('match_percent', 96)
        roadmap_slug = temp.get('roadmap_slug', 'python')
    elif assessment:
        # Re-derive roadmap slug
        career_rec = query_db("SELECT * FROM careers WHERE title = %s", (assessment['recommended_career'],), one=True)
        # Map common slugs
        title_to_slug = {
            'Python Developer': 'python',
            'Java Developer': 'java',
            'Web Developer': 'html-css',
            'Full Stack Developer': 'fullstack',
            'Data Analyst': 'data-analytics',
            'Data Scientist': 'data-analytics',
            'AI/ML Engineer': 'ai-ml',
            'Software Tester': 'fullstack',
            'Cloud Engineer': 'fullstack',
            'Cybersecurity Analyst': 'fullstack'
        }
        roadmap_slug = title_to_slug.get(assessment['recommended_career'], 'python')
        match_percent = 95
        top_rankings = [
            {'career': assessment['recommended_career'], 'match_percent': 95, 'category': 'Software Engineering', 'roadmap_slug': roadmap_slug},
            {'career': 'Full Stack Developer', 'match_percent': 88, 'category': 'Software Engineering', 'roadmap_slug': 'fullstack'},
            {'career': 'Data Analyst', 'match_percent': 82, 'category': 'Data & Analytics', 'roadmap_slug': 'data-analytics'}
        ]

    if not assessment:
        flash('No recent assessment found. Please complete the assessment questionnaire.', 'info')
        return redirect(url_for('student.career_assessment_view'))

    return render_template(
        'career_results.html',
        assessment=assessment,
        top_rankings=top_rankings,
        match_percent=match_percent,
        roadmap_slug=roadmap_slug
    )


@student_bp.route('/api/progress/toggle', methods=['POST'])
def toggle_progress():
    """AJAX API endpoint for students to mark roadmap topics completed or pending."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    data = request.get_json() or {}
    topic_id = data.get('topic_id')
    is_completed = data.get('completed', False)

    if not topic_id:
        return jsonify({'success': False, 'message': 'Missing topic_id'}), 400

    try:
        if is_completed:
            # Check if record already exists
            existing = query_db(
                "SELECT id FROM student_progress WHERE user_id = %s AND roadmap_topic_id = %s",
                (user_id, topic_id), one=True
            )
            if not existing:
                query_db(
                    "INSERT INTO student_progress (user_id, roadmap_topic_id, is_completed) VALUES (%s, %s, %s)",
                    (user_id, topic_id, True),
                    commit=True
                )
        else:
            query_db(
                "DELETE FROM student_progress WHERE user_id = %s AND roadmap_topic_id = %s",
                (user_id, topic_id),
                commit=True
            )

        # Recalculate completion percentage
        total_topics_row = query_db("SELECT COUNT(*) as total FROM roadmap_topics", one=True)
        total_count = total_topics_row['total'] if total_topics_row else 1
        
        completed_row = query_db(
            "SELECT COUNT(*) as completed FROM student_progress WHERE user_id = %s AND is_completed = TRUE",
            (user_id,), one=True
        )
        completed_count = completed_row['completed'] if completed_row else 0
        new_pct = int((completed_count / max(1, total_count)) * 100)

        return jsonify({
            'success': True,
            'completed': is_completed,
            'progress_percentage': new_pct
        })

    except Exception as e:
        print(f"[Progress API Error]: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
