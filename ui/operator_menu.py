from services import request_service
from ui import auth
from ui.common import ask_int, print_requests


def operator_menu(user):
    while True:
        print(f"\n===== Оператор ({user.login}) =====")
        print("1. Все заявки")
        print("2. Взять заявку в работу")
        print("3. Добавить комментарий")
        print("4. Закрыть заявку")
        print("5. Добавить оператора")
        print("0. Выход")
        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print_requests(request_service.get_all_requests(user.user_id))
            elif choice == "2":
                request_id = ask_int("Номер заявки: ")
                request_service.take_request(user.user_id, request_id)
                print("Заявка взята в работу")
            elif choice == "3":
                request_id = ask_int("Номер заявки: ")
                text = input("Комментарий: ")
                request_service.add_comment(user, request_id, text)
                print("Комментарий добавлен")
            elif choice == "4":
                request_id = ask_int("Номер заявки: ")
                request_service.close_request(user.user_id, request_id)
                print("Заявка закрыта")
            elif choice == "5":
                auth.add_operator(user)
            elif choice == "0":
                break
            else:
                print("Нет такого пункта")
        except Exception as e:
            print("Ошибка:", e)
