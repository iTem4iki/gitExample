from repositories import request_repository, user_repository
from models.user_role import CLIENT_ROLE_ID, OPERATOR_ROLE_ID


def _get_request(request_id: int):
    req = request_repository.get_by_id(request_id)
    if not req:
        raise Exception("Заявка не найдена")
    return req


def _check_operator(user_id: int):
    user = user_repository.get_by_id(user_id)
    if not user or user.user_role_id != OPERATOR_ROLE_ID:
        raise Exception("Это действие доступно только оператору")


def create_request(client_id: int, text: str):
    user = user_repository.get_by_id(client_id)
    if not user or user.user_role_id != CLIENT_ROLE_ID:
        raise Exception("Заявки создают только клиенты")
    if not text.strip():
        raise Exception("Описание проблемы не может быть пустым")
    request_repository.create(client_id, text.strip())


def get_my_requests(client_id: int):
    return request_repository.get_by_client(client_id)


def get_all_requests(user_id: int):
    _check_operator(user_id)
    return request_repository.get_all()


def take_request(operator_id: int, request_id: int):
    _check_operator(operator_id)
    req = _get_request(request_id)
    if req.status == 1:
        raise Exception("Заявка уже закрыта")
    if req.operator_id is not None:
        raise Exception("Заявка уже взята в работу")
    request_repository.take(request_id, operator_id)


def close_request(operator_id: int, request_id: int):
    _check_operator(operator_id)
    req = _get_request(request_id)
    if req.status == 1:
        raise Exception("Заявка уже закрыта")
    if req.operator_id is None:
        raise Exception("Сначала возьмите заявку в работу")
    if req.operator_id != operator_id:
        raise Exception("Заявку ведёт другой оператор")
    request_repository.close(request_id)


def rate_request(client_id: int, request_id: int, rate: int):
    req = _get_request(request_id)
    if req.client_id != client_id:
        raise Exception("Это не ваша заявка")
    if req.status != 1:
        raise Exception("Оценить можно только закрытую заявку")
    if req.rate is not None:
        raise Exception("Заявка уже оценена")
    if rate < 1 or rate > 5:
        raise Exception("Оценка должна быть от 1 до 5")
    request_repository.set_rate(request_id, rate)


def add_comment(user, request_id: int, text: str):
    req = _get_request(request_id)
    if user.user_role_id == CLIENT_ROLE_ID and req.client_id != user.user_id:
        raise Exception("Это не ваша заявка")
    if not text.strip():
        raise Exception("Комментарий не может быть пустым")
    new_comment = f"{user.login}: {text.strip()}"
    if req.comment:
        new_comment = req.comment + " | " + new_comment
    request_repository.update_comment(request_id, new_comment)
