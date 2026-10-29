-- Схема базы данных: учёт заявок в техподдержку
-- Выполняется один раз, когда файла tickets.db ещё нет

CREATE TABLE IF NOT EXISTS UserRole (
    UserRoleID  INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS User (
    UserID       INTEGER PRIMARY KEY AUTOINCREMENT,
    login        TEXT NOT NULL UNIQUE,
    passwordHash TEXT NOT NULL,
    UserRoleID   INTEGER NOT NULL,
    FOREIGN KEY (UserRoleID) REFERENCES UserRole(UserRoleID)
);

CREATE TABLE IF NOT EXISTS Request (
    RequestID  INTEGER PRIMARY KEY AUTOINCREMENT,
    status     INTEGER NOT NULL DEFAULT 0,   -- 0 - открыта, 1 - закрыта
    clientID   INTEGER NOT NULL,
    operatorID INTEGER,
    comment    TEXT,
    rate       INTEGER,
    FOREIGN KEY (clientID)   REFERENCES User(UserID),
    FOREIGN KEY (operatorID) REFERENCES User(UserID)
);

-- Тестовые данные
INSERT INTO UserRole (name, description) VALUES
    ('Клиент', 'Создаёт заявки в техподдержку'),
    ('Оператор', 'Обрабатывает заявки клиентов');

-- пароли: ivanov и petrova - 1234, operator1 - oper123
INSERT INTO User (login, passwordHash, UserRoleID) VALUES
    ('ivanov',    '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 1),
    ('petrova',   '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 1),
    ('operator1', '13a93f9a5502e71eed80a806f87bc4424e03e6b0d90acd513ea9d561c853b738', 2);

INSERT INTO Request (status, clientID, operatorID, comment, rate) VALUES
    (0, 1, NULL, 'Не загружается личный кабинет', NULL),
    (0, 2, 3,    'Не приходит письмо с подтверждением', NULL),
    (1, 1, 3,    'Не работает принтер', 5);
