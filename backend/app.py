import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database.db import db
from utils.logger import setup_logger

from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.admin_routes import admin_bp
from routes.consultation_routes import consultation_bp
from routes.compat_routes import compat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        origins=[
            r'http://localhost:\d+',
            r'http://127\.0\.0\.1:\d+'
        ],
        supports_credentials=True
    )
    db.init_app(app)
    JWTManager(app)

    logger = setup_logger(Config.LOG_FILE)
    logger.info('WeCareForYou application starting...')

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(consultation_bp, url_prefix='/api/consultation')
    app.register_blueprint(compat_bp, url_prefix='/api')

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'message': 'WeCareForYou API is running'})

    with app.app_context():
        db.create_all()
        _ensure_schema()
        _seed_admin()

    return app


def _seed_admin():
    import bcrypt
    from models.user_model import User

    if not User.query.filter_by(role='ADMIN').first():
        hashed = bcrypt.hashpw('Admin@123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin = User(name='System Admin', email='admin@wecareforyou.com', password=hashed, role='ADMIN')
        db.session.add(admin)
        db.session.commit()


def _ensure_schema():
    from sqlalchemy import text

    statements = [
        "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS phone VARCHAR(20)",
        "ALTER TABLE patients ADD COLUMN IF NOT EXISTS address VARCHAR(255)",
        "ALTER TABLE appointments ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP",
    ]
    for statement in statements:
        try:
            db.session.execute(text(statement))
        except Exception:
            db.session.rollback()
            return
    db.session.commit()


if __name__ == '__main__':
    application = create_app()
    application.run(debug=Config.DEBUG, host='0.0.0.0', port=5000, use_reloader=False)
