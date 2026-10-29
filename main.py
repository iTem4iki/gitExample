from database.database import init_db
from models.user_role import OPERATOR_ROLE_ID
from ui import auth
from ui.client_menu import client_menu
from ui.operator_menu import operator_menu


def main():
    init_db()
    while True:
        print("\n===== Учёт заявок в техподдержку =====")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            user = auth.login()
            if user:
                if user.user_role_id == OPERATOR_ROLE_ID:
                    operator_menu(user)
                else:
                    client_menu(user)
        elif choice == "2":
            auth.register()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")


if __name__ == "__main__":
    main()
