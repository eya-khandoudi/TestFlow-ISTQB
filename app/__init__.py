from flask import Flask
from app.config import Config
from app.database import close_db, init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register teardown
    app.teardown_appcontext(close_db)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.requirements import requirements_bp
    from app.routes.test_cases import test_cases_bp
    from app.routes.test_runs import test_runs_bp
    from app.routes.defects import defects_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(requirements_bp)
    app.register_blueprint(test_cases_bp)
    app.register_blueprint(test_runs_bp)
    app.register_blueprint(defects_bp)
    app.register_blueprint(api_bp)

    # Custom Jinja template filters for ISTQB UI styling
    @app.template_filter('badge_severity')
    def badge_severity(sev):
        classes = {
            'Blocker': 'bg-danger text-white',
            'Critical': 'bg-danger text-white',
            'Major': 'bg-warning text-dark',
            'Minor': 'bg-info text-dark'
        }
        return classes.get(sev, 'bg-secondary text-white')

    @app.template_filter('badge_status')
    def badge_status(status):
        classes = {
            'Pass': 'bg-success text-white',
            'Fail': 'bg-danger text-white',
            'Blocked': 'bg-warning text-dark',
            'Untested': 'bg-secondary text-white',
            'New': 'bg-primary text-white',
            'Assigned': 'bg-info text-dark',
            'Open': 'bg-danger text-white',
            'Fixed': 'bg-success text-white',
            'Retest': 'bg-warning text-dark',
            'Closed': 'bg-dark text-white',
            'Reopened': 'bg-danger text-white',
            'Deferred': 'bg-secondary text-white',
            'Rejected': 'bg-light text-muted border'
        }
        return classes.get(status, 'bg-secondary text-white')

    @app.template_filter('risk_badge')
    def risk_badge(score):
        try:
            val = int(score)
            if val >= 16:
                return 'badge bg-danger'
            elif val >= 10:
                return 'badge bg-warning text-dark'
            elif val >= 5:
                return 'badge bg-info text-dark'
            return 'badge bg-success'
        except (ValueError, TypeError):
            return 'badge bg-secondary'

    # Auto-initialize DB on startup if not yet created
    with app.app_context():
        init_db(app)

    return app
