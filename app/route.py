from flask import jsonify, request
from .models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def hello():
    return jsonify(message="Welcome to the API!")


def create_user():
    """Создание пользователя - теперь БЕЗ требования JWT токена"""
    data = request.get_json()
    if not data or 'name' not in data or 'password' not in data:
        return jsonify(error="Name and password are required"), 400

    user_name = data['name']
    password = data['password']

    # Проверяем, существует ли пользователь
    if User.find_by_name(user_name):
        return jsonify(error="User with this name already exists"), 409

    # Создаем нового пользователя
    new_user = User.create(user_name, password)
    if not new_user:
        return jsonify(error="Failed to create user"), 500

    # Автоматически генерируем токен для нового пользователя
    access_token = create_access_token(identity=new_user.id)

    return jsonify(
        message="User created successfully",
        user_id=new_user.id,
        name=new_user.name,
        access_token=access_token
    ), 201


def login():
    data = request.get_json()
    if not data or 'name' not in data or 'password' not in data:
        return jsonify(error="Name and password are required"), 400

    user_name = data.get('name')
    password = data.get('password')

    # Ищем пользователя
    user = User.find_by_name(user_name)
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(
            access_token=access_token,
            user_id=user.id,
            name=user.name
        ), 200

    return jsonify(error="Invalid credentials"), 401


@jwt_required()
def get_users():
    """Получение списка всех пользователей (требует JWT)"""
    users_list = User.get_all_users()
    users_data = []

    for user in users_list:
        users_data.append({
            'id': user.id,
            'name': user.name
        })

    return jsonify(
        users=users_data,
        count=len(users_data)
    ), 200


@jwt_required()
def get_current_user():
    """Получение информации о текущем пользователе (требует JWT)"""
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)

    if not user:
        return jsonify(error="User not found"), 404

    return jsonify({
        'id': user.id,
        'name': user.name
    }), 200


@jwt_required()
def get_user(user_id):
    """Получение информации о конкретном пользователе (требует JWT)"""
    user = User.find_by_id(user_id)

    if not user:
        return jsonify(error="User not found"), 404

    return jsonify({
        'id': user.id,
        'name': user.name
    }), 200


@jwt_required()
def update_user():
    """Обновление данных пользователя (требует JWT)"""
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify(error="No data provided"), 400

    user = User.find_by_id(current_user_id)
    if not user:
        return jsonify(error="User not found"), 404

    # Обновляем имя, если оно предоставлено
    if 'name' in data and data['name']:
        # Проверяем, не занято ли имя другим пользователем
        existing_user = User.find_by_name(data['name'])
        if existing_user and existing_user.id != current_user_id:
            return jsonify(error="Username already taken"), 409
        user.name = data['name']

    # Обновляем пароль, если он предоставлен
    if 'password' in data and data['password']:
        from werkzeug.security import generate_password_hash
        user.password_hash = generate_password_hash(data['password'])

    return jsonify(
        message="User updated successfully",
        id=user.id,
        name=user.name
    ), 200


@jwt_required()
def delete_user():
    """Удаление пользователя (требует JWT)"""
    current_user_id = get_jwt_identity()

    # Ищем пользователя в хранилище
    for i, user in enumerate(User.get_all_users()):
        if user.id == current_user_id:
            User.get_all_users().pop(i)
            return jsonify(message="User deleted successfully"), 200

    return jsonify(error="User not found"), 404