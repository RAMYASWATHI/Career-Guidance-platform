import os
from flask import Flask, render_template
from config import Config
from database.db import init_db

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Register application blueprints
from routes.auth import auth_bp
from routes.student import student_bp
from routes.career import career_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(career_bp)
app.register_blueprint(admin_bp)

# Global context processor for layout templates
@app.context_processor
def inject_global_data():
    return {
        'platform_name': 'CAREER GUIDANCE PLATFORM',
        'platform_tagline': 'Explore Your Skills, Discover Your Career, Build Your Future.'
    }

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', not_found=True), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', server_error=True), 500

# Initialize database schema and seed data on startup
with app.app_context():
    init_db()
    print("[Database Ready] All 11 tables verified and seeded successfully.")

if __name__ == '__main__':
    print("==================================================================")
    print(" CAREER GUIDANCE PLATFORM - WEB SERVER INITIALIZED")
    print(" Heading: CAREER GUIDANCE PLATFORM")
    print(" Tagline: Explore Your Skills, Discover Your Career, Build Your Future.")
    print(" Access URL: http://127.0.0.1:5000")
    print("==================================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
