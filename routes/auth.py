import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import query_db

auth_bp = Blueprint('auth', __name__)

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle student registration with validation and profile creation."""
    if session.get('user_id'):
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        college_name = request.form.get('college_name', '').strip()
        degree = request.form.get('degree', '').strip()
        department = request.form.get('department', '').strip()
        graduation_year = request.form.get('graduation_year', '').strip()

        # Validation checks
        if not full_name or not email or not password or not confirm_password:
            flash('All required fields must be filled.', 'danger')
            return render_template('register.html')

        if not re.match(EMAIL_REGEX, email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match. Please verify and try again.', 'danger')
            return render_template('register.html')

        # Check for existing user with identical email
        existing_user = query_db("SELECT id FROM users WHERE email = %s", (email,), one=True)
        if existing_user:
            flash('An account with this email address already exists. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        # Secure password hashing
        pwd_hash = generate_password_hash(password)

        try:
            # Insert into users table
            user_id = query_db(
                "INSERT INTO users (full_name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                (full_name, email, pwd_hash, 'student'),
                commit=True
            )

            # Insert into student_profiles table
            grad_year_val = int(graduation_year) if graduation_year.isdigit() else 2026
            query_db(
                """INSERT INTO student_profiles 
                   (user_id, college_name, degree, department, graduation_year, selected_career, current_skills) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (user_id, college_name, degree, department, grad_year_val, 'Undecided', ''),
                commit=True
            )

            # Establish session
            session['user_id'] = user_id
            session['user_name'] = full_name
            session['user_email'] = email
            session['role'] = 'student'

            flash(f'Welcome aboard, {full_name}! Your student account has been created successfully.', 'success')
            return redirect(url_for('student.dashboard'))

        except Exception as e:
            flash(f'An error occurred during registration. Please try again.', 'danger')
            print(f"[Auth Error]: {e}")
            return render_template('register.html')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle student and administrator authentication."""
    if session.get('user_id'):
        if session.get('role') == 'admin':
            return redirect(url_for('admin.admin_panel'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please enter both your email address and password.', 'warning')
            return render_template('login.html')

        user = query_db("SELECT * FROM users WHERE email = %s", (email,), one=True)

        if user and check_password_hash(user['password_hash'], password):
            # Login successful
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            session['user_email'] = user['email']
            session['role'] = user['role']

            flash(f'Welcome back, {user["full_name"]}!', 'success')

            if user['role'] == 'admin':
                return redirect(url_for('admin.admin_panel'))
            return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email address or password. Please try again.', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Terminate current user session."""
    session.clear()
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('career.index'))
