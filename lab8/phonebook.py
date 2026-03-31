from connect import connect

def create_table():
    # В Practice 7 мы создали таблицу contacts без ID, 
    # оставляем структуру как была, чтобы не было конфликтов.
    query = """
    CREATE TABLE IF NOT EXISTS contacts (
        first_name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

def call_upsert_contact():
    username = input("Введите имя: ").strip()
    phone = input("Введите телефон: ").strip()

    if not username or not phone:
        print("Имя и телефон не должны быть пустыми.")
        return

    # Вызываем ПРОЦЕДУРУ через CALL
    query = "CALL upsert_contact(%s, %s)"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (username, phone))
            # В процедурах обязательно нужно делать commit, если connect() его не делает сам
            conn.commit() 

    print("Контакт добавлен или обновлён.")

def search_contacts_by_pattern():
    pattern = input("Введите шаблон для поиска (имя или номер): ").strip()

    if not pattern:
        print("Шаблон не должен быть пустым.")
        return

    # Вызываем ФУНКЦИЮ через SELECT
    query = "SELECT * FROM search_contacts(%s)"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (pattern,))
            rows = cur.fetchall()

    if rows:
        print("\nРезультаты поиска:")
        for row in rows:
            print(f"Имя: {row[0]}, Телефон: {row[1]}")
    else:
        print("Ничего не найдено.")

def show_paginated_contacts():
    limit_value = input("Сколько записей показать (LIMIT): ").strip()
    offset_value = input("Сколько пропустить (OFFSET): ").strip()

    if not limit_value.isdigit() or not offset_value.isdigit():
        print("LIMIT и OFFSET должны быть числами.")
        return

    # Вызываем ФУНКЦИЮ через SELECT
    query = "SELECT * FROM get_contacts_paginated(%s, %s)"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (int(limit_value), int(offset_value)))
            rows = cur.fetchall()

    if rows:
        print("\nКонтакты (страница):")
        for row in rows:
            print(f"Имя: {row[0]}, Телефон: {row[1]}")
    else:
        print("На этой странице данных нет.")

def call_delete_contact():
    value = input("Введите имя или номер для удаления: ").strip()

    if not value:
        print("Поле не должно быть пустым.")
        return

    # Вызываем ПРОЦЕДУРУ через CALL
    query = "CALL delete_contact(%s)"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (value,))
            conn.commit()

    print(f"Запись '{value}' удалена (если она существовала).")

def show_all_contacts():
    # Так как ID нет, сортируем по алфавиту (first_name)
    query = "SELECT * FROM contacts ORDER BY first_name"

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    if rows:
        print("\nВсе контакты в базе:")
        for row in rows:
            print(f"Имя: {row[0]}, Телефон: {row[1]}")
    else:
        print("Телефонная книга пуста.")

def menu():
    create_table()

    while True:
        print("\n===== PHONEBOOK PRACTICE 8 (Procedures/Functions) =====")
        print("1 - Добавить/Обновить (Upsert Procedure)")
        print("2 - Поиск по шаблону (Function)")
        print("3 - Пагинация (Function)")
        print("4 - Удалить (Procedure)")
        print("5 - Показать всех")
        print("0 - Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            call_upsert_contact()
        elif choice == "2":
            search_contacts_by_pattern()
        elif choice == "3":
            show_paginated_contacts()
        elif choice == "4":
            call_delete_contact()
        elif choice == "5":
            show_all_contacts()
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Неправильный ввод.")

if __name__ == "__main__":
    menu()