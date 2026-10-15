#include <iostream>
#include <string>
#include "sqlite3.h"
using namespace std;

int show(void* data, int n, char** values, char** names) {
    for (int i = 0; i < n; i++) {
        cout << names[i] << ": " << (values[i] ? values[i] : "NULL") << "  ";
    }
    cout << endl;
    return 0;
}

int main() {
    sqlite3* db;
    sqlite3_open("tickets.db", &db);

    sqlite3_exec(db,
        "CREATE TABLE IF NOT EXISTS UserRole (UserRoleID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT);"
        "CREATE TABLE IF NOT EXISTS User (UserID INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT, passwordHash TEXT, UserRoleID INTEGER, FOREIGN KEY (UserRoleID) REFERENCES UserRole(UserRoleID));"
        "CREATE TABLE IF NOT EXISTS Request (RequestID INTEGER PRIMARY KEY AUTOINCREMENT, status INTEGER, clientID INTEGER, operatorID INTEGER, comment TEXT, rate INTEGER, FOREIGN KEY (clientID) REFERENCES User(UserID), FOREIGN KEY (operatorID) REFERENCES User(UserID));"
        "INSERT OR IGNORE INTO UserRole (UserRoleID, name, description) VALUES (1, 'Client', 'Creates requests'), (2, 'Operator', 'Handles requests');",
        0, 0, 0);

    int choice = -1;
    while (choice != 0) {
        cout << "\n1 - add user\n2 - add request\n3 - show tables\n0 - exit\n> ";
        cin >> choice;

        if (choice == 1) {
            string login, password, role;
            cout << "login: ";    cin >> login;
            cout << "password: "; cin >> password;
            cout << "role (1 - client, 2 - operator): "; cin >> role;
            string sql = "INSERT INTO User (login, passwordHash, UserRoleID) VALUES ('" + login + "', '" + password + "', " + role + ");";
            sqlite3_exec(db, sql.c_str(), 0, 0, 0);
        }
        if (choice == 2) {
            string client, operatorId, comment;
            cout << "client id: ";   cin >> client;
            cout << "operator id: "; cin >> operatorId;
            cout << "comment: ";     cin >> comment;
            string sql = "INSERT INTO Request (status, clientID, operatorID, comment) VALUES (0, " + client + ", " + operatorId + ", '" + comment + "');";
            sqlite3_exec(db, sql.c_str(), 0, 0, 0);
        }
        if (choice == 3) {
            cout << "--- UserRole ---" << endl;
            sqlite3_exec(db, "SELECT * FROM UserRole;", show, 0, 0);
            cout << "--- User ---" << endl;
            sqlite3_exec(db, "SELECT * FROM User;", show, 0, 0);
            cout << "--- Request ---" << endl;
            sqlite3_exec(db, "SELECT * FROM Request;", show, 0, 0);
        }
    }

    sqlite3_close(db);
    return 0;
}