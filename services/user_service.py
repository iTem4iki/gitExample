import hashlib
from repositories import user_repository
from models.user_role import CLIENT_ROLE_ID, OPERATOR_ROLE_ID


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register(login: str, password: str, role_id: int = CLIENT_ROLE_ID):
    if not login.strip():
        raise Exception("Логин не может быть пустым")
    if len(password) < 4:
        raise Exception("Пароль должен быть не короче 4 символов")
    if user_repository.get_by_login(login.strip()):
        raise Exception("Такой логин уже занят")
    user_repository.create(login.strip(), hash_password(password), role_id)


def authenticate(login: str, password: str):
    user = user_repository.get_by_login(login.strip())
    if user and user.password_hash == hash_password(password):
        return user
    return None


def add_operator(current_user, login: str, password: str):
    if current_user.user_role_id != OPERATOR_ROLE_ID:
        raise Exception("Добавлять операторов может только оператор")
    register(login, password, OPERATOR_ROLE_ID)
