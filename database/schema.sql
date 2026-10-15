
DROP TABLE IF EXISTS Request;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserRole;

CREATE TABLE UserRole (
    UserRoleID  INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT
);

CREATE TABLE User (
    UserID       INTEGER PRIMARY KEY AUTOINCREMENT,
    login        TEXT NOT NULL UNIQUE,
    passwordHash TEXT NOT NULL,
    UserRoleID   INTEGER NOT NULL,
    FOREIGN KEY (UserRoleID) REFERENCES UserRole(UserRoleID)
);

CREATE TABLE Request (
    RequestID  INTEGER PRIMARY KEY AUTOINCREMENT,
    status     INTEGER NOT NULL DEFAULT 0, 
    clientID   INTEGER NOT NULL,
    operatorID INTEGER,
    comment    TEXT,
    rate       INTEGER,
    FOREIGN KEY (clientID)   REFERENCES User(UserID),
    FOREIGN KEY (operatorID) REFERENCES User(UserID)
);


INSERT INTO UserRole (name, description) VALUES
    ('Клиент', 'Пользователь, создающий заявки в техподдержку'),
    ('Оператор', 'Сотрудник, обрабатывающий заявки клиентов');

INSERT INTO User (login, passwordHash, UserRoleID) VALUES
    ('ivanov',   'hash_1', 1),  
    ('petrova',  'hash_2', 1),  
    ('sidorov',  'hash_3', 2);  

INSERT INTO Request (status, clientID, operatorID, comment, rate) VALUES
    (0, 1, NULL, 'Не загружается личный кабинет', NULL),       
    (1, 2, 3,    'Проблема решается, ждём подтверждения', NULL), 
    (1, 1, 3,    'Проблема решена, спасибо за помощь', 5);       
