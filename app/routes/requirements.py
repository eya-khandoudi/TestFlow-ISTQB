from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db
from app.services.istqb_engine import validate_string_length, ISTQBValidationError

requirements_bp = Blueprint('requirements', __name__, url_prefix='/requirements')

@requirements_bp.route('/')
def list_requirements():
    db = get_db()
    reqs = db.execute("""
        SELECT r.*, COUNT(tc.id) as test_case_count
        FROM requirements r
        LEFT JOIN test_cases tc ON r.id = tc.requirement_id
        GROUP BY r.id
        ORDER BY r.req_code
    """).fetchall()
    return render_template('requirements/list.html', requirements=reqs)

@requirements_bp.route('/new', methods=['GET', 'POST'])
def create_requirement():
    db = get_db()
    if request.method == 'POST':
        req_code = request.form.get('req_code', '').strip().upper()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'Functional')
        priority = request.form.get('priority', 'Medium')
        project_id = 1

        try:
            validate_string_length(req_code, 3, 20, "Requirement Code")
            validate_string_length(title, 5, 200, "Title")

            db.execute("""
                INSERT INTO requirements (req_code, title, description, category, priority, project_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (req_code, title, description, category, priority, project_id))
            db.commit()
            flash(f"Requirement {req_code} successfully created.", "success")
            return redirect(url_for('requirements.list_requirements'))
        except (ISTQBValidationError, Exception) as e:
            flash(str(e), "danger")

    return render_template('requirements/form.html', requirement=None)

@requirements_bp.route('/<int:req_id>/edit', methods=['GET', 'POST'])
def edit_requirement(req_id):
    db = get_db()
    req = db.execute("SELECT * FROM requirements WHERE id = ?", (req_id,)).fetchone()
    if not req:
        flash("Requirement not found.", "warning")
        return redirect(url_for('requirements.list_requirements'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'Functional')
        priority = request.form.get('priority', 'Medium')

        try:
            validate_string_length(title, 5, 200, "Title")
            db.execute("""
                UPDATE requirements 
                SET title = ?, description = ?, category = ?, priority = ?
                WHERE id = ?
            """, (title, description, category, priority, req_id))
            db.commit()
            flash("Requirement updated successfully.", "success")
            return redirect(url_for('requirements.list_requirements'))
        except (ISTQBValidationError, Exception) as e:
            flash(str(e), "danger")

    return render_template('requirements/form.html', requirement=req)

@requirements_bp.route('/<int:req_id>/delete', methods=['POST'])
def delete_requirement(req_id):
    db = get_db()
    db.execute("DELETE FROM requirements WHERE id = ?", (req_id,))
    db.commit()
    flash("Requirement removed from repository.", "info")
    return redirect(url_for('requirements.list_requirements'))
