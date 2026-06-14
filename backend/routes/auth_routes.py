from flask import Blueprint, request
from services.auth_service import AuthService
from utils.helpers import success_response, error_response
from utils.logger import setup_logger
from config import Config

auth_bp = Blueprint('auth', __name__)
logger = setup_logger(Config.LOG_FILE)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    logger.info('Registration attempt for email: %s', data.get('email'))

    user, message = AuthService.register(data)
    if not user:
        logger.warning('Registration failed: %s', message)
        return error_response(message, 400)

    logger.info('User registered successfully: %s', user.email)
    return success_response(user.to_dict(), message, 201)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    logger.info('Login attempt for email: %s', data.get('email'))

    result, message = AuthService.login(data.get('email'), data.get('password'))
    if not result:
        logger.warning('Login failed: %s', message)
        return error_response(message, 401)

    logger.info('User logged in: %s', data.get('email'))
    return success_response(result, message)


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return success_response(message='Logged out successfully')
