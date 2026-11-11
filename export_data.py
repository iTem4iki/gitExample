from database.database import init_db
from services.export_service import export_all


def main():
    init_db()
    for path in export_all("out"):
        print("Создан файл:", path)


if __name__ == "__main__":
    main()
