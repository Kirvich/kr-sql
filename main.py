import mysql.connector
from datetime import datetime

# Подключение к базе данных
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="Друзья_человека"
)

cursor = db.cursor()

def add_animal():
    animal_type = input("Какое животное вы хотите добавить? (Домашнее/Вьючное): ").strip().lower()
    animal_species = input("Введите вид животного: ").strip()
    birthdate_str = input("Введите дату рождения животного (YYYY-MM-DD): ").strip()
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()  # преобразуем строку в дату
    commands = input("Введите команды, которые выполняет животное: ").strip()

    if animal_type == 'домашнее':
        table_name = "Домашние_Животные"
    elif animal_type == 'вьючное':
        table_name = "Вьючные_животные"
    else:
        print("Неверный выбор!")
        return
    
    # Вставка нового животного в таблицу без имени
    query = f"INSERT INTO {table_name} (species, birthdate, commands) VALUES (%s, %s, %s)"
    values = (animal_species, birthdate, commands)
    cursor.execute(query, values)
    db.commit()
    print(f"Животное добавлено в таблицу {table_name}.")

def teach_new_command(animal_id, new_command):
    try:
        # Получаем текущие команды для животного
        cursor.execute("SELECT commands FROM Домашние_Животные WHERE id = %s", (animal_id,))
        result = cursor.fetchone()
        
        if result:
            current_commands = result[0]
            # Если команд нет, просто присваиваем новую команду
            if current_commands:
                updated_commands = f"{current_commands}, {new_command}"
            else:
                updated_commands = new_command
            
            # Обновляем команды для животного
            query = "UPDATE Домашние_Животные SET commands = %s WHERE id = %s"
            cursor.execute(query, (updated_commands, animal_id))
            db.commit()
            print(f"Животное с ID {animal_id} обучено новой команде: {new_command}")
        else:
            print(f"Животное с ID {animal_id} не найдено.")
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")

def create_young_animals_table():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Молодые_Животные AS
        SELECT id, species, birthdate, commands,
               TIMESTAMPDIFF(MONTH, birthdate, CURDATE()) AS age_in_months
        FROM Домашние_Животные
        WHERE TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) BETWEEN 1 AND 2
        UNION
        SELECT id, species, birthdate, commands,
               TIMESTAMPDIFF(MONTH, birthdate, CURDATE()) AS age_in_months
        FROM Вьючные_животные
        WHERE TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) BETWEEN 1 AND 2;
        """)
        db.commit()
        print("Таблица 'Молодые_Животные' успешно создана и заполнена.")
    except mysql.connector.Error as err:
        print(f"Ошибка при создании таблицы: {err}")

def view_young_animals():
    try:
        cursor.execute("SELECT * FROM Молодые_Животные")
        result = cursor.fetchall()
        print("\nМолодые животные:")
        for row in result:
            print(row)
    except mysql.connector.Error as err:
        print(f"Ошибка при получении данных: {err}")

def main():
    while True:
        print("\nМеню:")
        print("1. Просмотреть всех животных")
        print("2. Добавить новое животное")
        print("3. Обучить животное новой команде")
        print("4. Создать таблицу молодых животных")
        print("5. Просмотреть молодых животных")
        print("6. Выход")
        
        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            cursor.execute("SELECT * FROM Домашние_Животные")
            result = cursor.fetchall()
            print("\nДомашние животные:")
            for row in result:
                print(row)
            
            cursor.execute("SELECT * FROM Вьючные_животные")
            result = cursor.fetchall()
            print("\nВьючные животные:")
            for row in result:
                print(row)
        
        elif choice == '2':
            add_animal()
        
        elif choice == '3':
            animal_id = int(input("Введите ID животного: "))
            new_command = input("Введите новую команду для обучения животного: ")
            teach_new_command(animal_id, new_command)

        elif choice == '4':
            create_young_animals_table()
        
        elif choice == '5':
            view_young_animals()

        elif choice == '6':
            print("Выход из программы...")
            break
        
        else:
            print("Неверный выбор! Пожалуйста, выберите 1, 2, 3, 4, 5 или 6.")

# Вызов функции для запуска программы
main()

# Закрытие соединения с базой данных
db.close()
