from services import request_service
from ui.common import ask_int, print_requests


def client_menu(user):
    while True:
        print(f"\n===== Клиент ({user.login}) =====")
        print("1. Мои заявки")
        print("2. Создать заявку")
        print("3. Добавить комментарий")
        print("4. Оценить решение")
        print("0. Выход")
        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print_requests(request_service.get_my_requests(user.user_id))
            elif choice == "2":
                text = input("Опишите проблему: ")
                request_service.create_request(user.user_id, text)
                print("Заявка создана")
            elif choice == "3":
                request_id = ask_int("Номер заявки: ")
                text = input("Комментарий: ")
                request_service.add_comment(user, request_id, text)
                print("Комментарий добавлен")
            elif choice == "4":
                request_id = ask_int("Номер заявки: ")
                rate = ask_int("Оценка (1-5): ")
                request_service.rate_request(user.user_id, request_id, rate)
                print("Спасибо за оценку")
            elif choice == "0":
                break
            else:
                print("Нет такого пункта")
        except Exception as e:
            print("Ошибка:", e)
