from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from database.db import query_db

career_bp = Blueprint('career', __name__)

@career_bp.route('/')
def index():
    """Render home landing page."""
    featured_careers = query_db("SELECT * FROM careers LIMIT 4")
    return render_template('index.html', featured_careers=featured_careers)


@career_bp.route('/about')
def about():
    """Render About Us page."""
    return render_template('about.html')


@career_bp.route('/contact')
def contact():
    """Render Contact Us page."""
    return render_template('contact.html')


@career_bp.route('/contact/submit', methods=['POST'])
def contact_submit():
    """Process contact form inquiry."""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', 'General')
    message = request.form.get('message', '').strip()

    if not name or not email or not message:
        flash('Please fill in all required fields.', 'warning')
        return redirect(url_for('career.contact'))

    flash(f'Thank you, {name}! Your message regarding "{subject}" has been received. Our career counseling team will get back to you shortly.', 'success')
    return redirect(url_for('career.contact'))


@career_bp.route('/careers')
def careers_list():
    """Render 10 In-Demand Tech Careers with filters."""
    careers = query_db("SELECT * FROM careers ORDER BY id ASC")
    return render_template('careers.html', careers=careers)


@career_bp.route('/careers/<int:career_id>')
def career_detail(career_id):
    """Render comprehensive view of a specific career track."""
    career = query_db("SELECT * FROM careers WHERE id = %s", (career_id,), one=True)
    if not career:
        flash('The requested career track could not be found.', 'warning')
        return redirect(url_for('career.careers_list'))
    return render_template('career_detail.html', career=career)


@career_bp.route('/roadmaps')
@career_bp.route('/roadmaps/<slug>')
def roadmaps_list(slug='python'):
    """Render interactive learning roadmap by slug with tiered topics and checkboxes."""
    all_roadmaps = query_db("SELECT * FROM learning_roadmaps ORDER BY id ASC")
    
    active_roadmap = query_db("SELECT * FROM learning_roadmaps WHERE slug = %s", (slug,), one=True)
    if not active_roadmap and all_roadmaps:
        active_roadmap = all_roadmaps[0]

    # Fetch topics for active roadmap
    all_topics = query_db(
        "SELECT * FROM roadmap_topics WHERE roadmap_id = %s ORDER BY order_index ASC",
        (active_roadmap['id'],)
    )

    beginner_topics = [t for t in all_topics if t['level'] == 'Beginner']
    intermediate_topics = [t for t in all_topics if t['level'] == 'Intermediate']
    advanced_topics = [t for t in all_topics if t['level'] == 'Advanced']

    # Fetch user's completed topic IDs
    user_id = session.get('user_id')
    completed_topic_ids = set()
    if user_id:
        completed_rows = query_db(
            "SELECT roadmap_topic_id FROM student_progress WHERE user_id = %s AND is_completed = TRUE",
            (user_id,)
        )
        completed_topic_ids = {row['roadmap_topic_id'] for row in completed_rows}

    # Calculate completion percentage for this specific roadmap
    total_roadmap_topics = len(all_topics)
    completed_roadmap_topics = sum(1 for t in all_topics if t['id'] in completed_topic_ids)
    progress_pct = int((completed_roadmap_topics / max(1, total_roadmap_topics)) * 100)

    return render_template(
        'roadmap.html',
        all_roadmaps=all_roadmaps,
        active_roadmap=active_roadmap,
        all_topics=all_topics,
        beginner_topics=beginner_topics,
        intermediate_topics=intermediate_topics,
        advanced_topics=advanced_topics,
        completed_topic_ids=completed_topic_ids,
        progress_pct=progress_pct
    )


@career_bp.route('/roadmap/<slug>')
def roadmap_detail(slug):
    """Direct alias for roadmaps."""
    return redirect(url_for('career.roadmaps_list', slug=slug))


@career_bp.route('/skills')
def skills_view():
    """Render technical and soft skills frameworks."""
    technical_skills = query_db("SELECT * FROM skills WHERE category = 'technical' ORDER BY id ASC")
    soft_skills = query_db("SELECT * FROM skills WHERE category = 'soft' ORDER BY id ASC")
    return render_template('skills.html', technical_skills=technical_skills, soft_skills=soft_skills)


@career_bp.route('/interview')
def interview_prep():
    """Render technical, HR, and aptitude interview preparation bank."""
    cat = request.args.get('cat', 'all')
    if cat == 'all':
        questions = query_db("SELECT * FROM interview_questions ORDER BY category, id ASC")
    else:
        questions = query_db("SELECT * FROM interview_questions WHERE category = %s ORDER BY id ASC", (cat,))
    return render_template('interview.html', questions=questions, current_cat=cat)


@career_bp.route('/resume')
def resume_guide():
    """Render fresher resume guidance and interactive live resume builder."""
    return render_template('resume.html')


@career_bp.route('/jobs')
def jobs_list():
    """Render verified fresher jobs and internships directory."""
    jobs = query_db("SELECT * FROM job_opportunities ORDER BY created_at DESC")
    return render_template('jobs.html', jobs=jobs)
