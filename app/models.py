from werkzeug.security import generate_password_hash, check_password_hash
import uuid

# Хранилище пользователей в памяти
users_storage = []


class User:
    def __init__(self, name, password):
        self.id = str(uuid.uuid4())
        self.name = name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_name(cls, name):
        """Поиск пользователя по имени"""
        return next((user for user in users_storage if user.name == name), None)

    @classmethod
    def find_by_id(cls, user_id):
        """Поиск пользователя по ID"""
        return next((user for user in users_storage if user.id == user_id), None)

    @classmethod
    def create(cls, name, password):
        """Создание нового пользователя"""
        if cls.find_by_name(name):
            return None  # Пользователь уже существует

        new_user = cls(name, password)
        users_storage.append(new_user)
        return new_user

    @classmethod
    def get_all_users(cls):
        """Получение всех пользователей"""
        return users_storage