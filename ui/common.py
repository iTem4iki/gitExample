def ask_int(text: str) -> int:
    value = input(text)
    if not value.isdigit():
        raise Exception("Нужно ввести число")
    return int(value)


def print_requests(requests):
    if not requests:
        print("Заявок нет")
        return
    for r in requests:
        print(f"\n#{r.request_id} [{r.status_text}]  клиент: {r.client_login}, "
              f"оператор: {r.operator_login or '-'}, оценка: {r.rate or '-'}")
        print(f"   {r.comment}")
