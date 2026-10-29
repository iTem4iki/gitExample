from services import user_service


def login():
    login_value = input("Логин: ")
    password_value = input("Пароль: ")
    user = user_service.authenticate(login_value, password_value)
    if not user:
        print("Неверный логин или пароль")
        return None
    return user


def register():
    login_value = input("Логин: ")
    password_value = input("Пароль: ")
    try:
        user_service.register(login_value, password_value)
        print("Регистрация прошла успешно, теперь можно войти")
    except Exception as e:
        print("Ошибка:", e)


def add_operator(current_user):
    login_value = input("Логин нового оператора: ")
    password_value = input("Пароль: ")
    try:
        user_service.add_operator(current_user, login_value, password_value)
        print("Оператор добавлен")
    except Exception as e:
        print("Ошибка:", e)
