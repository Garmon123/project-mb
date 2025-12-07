from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .route import (
    hello, create_user, login,
    get_users, get_current_user, get_user,
    update_user, delete_user
)


def create_app():
    app = Flask(__name__)

    # Загружаем конфигурацию
    app.config.from_object(Config)

    # Инициализируем JWT
    jwt = JWTManager(app)

    # Регистрируем маршруты
    app.add_url_rule('/api', 'hello', hello, methods=['GET'])
    app.add_url_rule('/api/users/register', 'create_user', create_user, methods=['POST'])
    app.add_url_rule('/api/users/login', 'login', login, methods=['POST'])
    app.add_url_rule('/api/users', 'get_users', get_users, methods=['GET'])
    app.add_url_rule('/api/users/me', 'get_current_user', get_current_user, methods=['GET'])
    app.add_url_rule('/api/users/<user_id>', 'get_user', get_user, methods=['GET'])
    app.add_url_rule('/api/users/me', 'update_user', update_user, methods=['PUT'])
    app.add_url_rule('/api/users/me', 'delete_user', delete_user, methods=['DELETE'])

    return app