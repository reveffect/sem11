import json, csv
from datetime import datetime


# Константы для файлов
FILES = {
    'notes': 'notes.json',
    'tasks': 'tasks.json',
    'contacts': 'contacts.json',
    'finance': 'finance_records.json'
}


# Класс для заметок
class Note:
    def __init__(self, note_id, title, content, timestamp=None):
        self.id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return vars(self)


# Класс для задач
class Task:
    def __init__(self, task_id, title, description, done=False, priority="Средний", due_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return vars(self)


# Класс для контактов
class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return vars(self)


# Класс для финансовых записей
class FinanceRecord:
    def __init__(self, record_id, amount, category, date, description):
        self.id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return vars(self)


# Главный класс персонального помощника
class PersonalAssistant:
    def __init__(self):
        self.notes = self.load_data(FILES['notes'])
        self.tasks = self.load_data(FILES['tasks'])
        self.contacts = self.load_data(FILES['contacts'])
        self.finances = self.load_data(FILES['finance'])

    # Главное меню
    def main_menu(self):
        while True:
            print("\nДобро пожаловать в Персональный помощник!")
            options = [
                "Управление заметками",
                "Управление задачами",
                "Управление контактами",
                "Управление финансовыми записями",
                "Калькулятор",
                "Выход"
            ]
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            action = input("Выберите действие: ")
            if action == "1":
                self.notes_menu()
            elif action == "2":
                self.tasks_menu()
            elif action == "3":
                self.contacts_menu()
            elif action == "4":
                self.finance_menu()
            elif action == "5":
                self.calculator()
            elif action == "6":
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    # Меню управления заметками
    def notes_menu(self):
        while True:
            print("\nУправление заметками:")
            options = [
                "Создать заметку",
                "Просмотреть список заметок",
                "Просмотреть заметку",
                "Редактировать заметку",
                "Удалить заметку",
                "Экспортировать заметки в CSV",
                "Импортировать заметки из CSV",
                "Назад"
            ]
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            action = input("Выберите действие: ")
            if action == "1":
                self.create_note()
            elif action == "2":
                self.get_notes_list()
            elif action == "3":
                self.view_note()
            elif action == "4":
                self.edit_note()
            elif action == "5":
                self.delete_note()
            elif action == "6":
                try:
                    self.export_notes_to_csv()
                except ValueError as e:
                    print(e)
            elif action == "7":
                self.import_notes_from_csv()
            elif action == "8":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    # Создание новой заметки
    def create_note(self):
        title = input("Введите заголовок заметки: ")
        content = input("Введите содержимое заметки: ")
        note_id = len(self.notes) + 1  # Генерация ID на основе текущего количества

        new_note = Note(note_id, title, content)
        self.notes.append(new_note.to_dict())
        self.save_data(FILES['notes'], self.notes)
        print("Заметка успешно создана.")

    # Просмотр списка заметок
    def get_notes_list(self):
        print("\nСписок заметок:")
        for note in self.notes:
            print(f"ID: {note['id']}, Заголовок: {note['title']}, Дата: {note['timestamp']}")

    # Просмотр заметки по ID
    def view_note(self):
        note_id = int(input("Введите ID заметки для просмотра: "))
        note = next((n for n in self.notes if n['id'] == note_id), None)

        if note:
            print(f"Заголовок: {note['title']}")
            print(f"Содержимое: {note['content']}")
            print(f"Дата: {note['timestamp']}")
        else:
            print("Заметка не найдена.")

    # Редактирование заметки по ID
    def edit_note(self):
        note_id = int(input("Введите ID заметки для редактирования: "))
        note = next((n for n in self.notes if n['id'] == note_id), None)

        if note:
            note['title'] = input(f"Введите новый заголовок (текущий: {note['title']}): ")
            note['content'] = input(f"Введите новое содержимое (текущее: {note['content']}): ")
            note['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_data(FILES['notes'], self.notes)
            print("Заметка успешно обновлена.")
        else:
            print("Заметка не найдена.")

    # Удаление заметки по ID
    def delete_note(self):
        note_id = int(input("Введите ID заметки для удаления: "))
        self.notes = [n for n in self.notes if n['id'] != note_id]
        self.save_data(FILES['notes'], self.notes)
        print("Заметка успешно удалена.")

    # Импортирование заметок из CSV файла
    def import_notes_from_csv(self):
        filename = "notes.csv"

        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Приведение данных
                for row in reader:
                    row['id'] = int(row['id'])
                    row['timestamp'] = row.get('timestamp', datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                    self.notes.append(row)

            self.save_data(FILES['notes'], self.notes)
            print(f"Заметки импортированы из файла {filename}.")

        except FileNotFoundError:
            print("Файл не найден.")

    # Экспортирование заметок в CSV файл
    def export_notes_to_csv(self):
        if not self.notes:
            raise ValueError("Данные для экспортирования отсутствуют. Заметки пустые.")

        with open('notes_export.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.notes[0].keys())
            writer.writeheader()
            writer.writerows(self.notes)

        print(f"Заметки экспортированы в файл notes_export.csv.")

    # Меню управления задачами
    def tasks_menu(self):
        while True:
            print("\nУправление задачами:")
            options = [
                "Добавить задачу",
                "Просмотреть задачи",
                "Отметить задачу как выполненную",
                "Удалить задачу",
                "Экспортировать задачи в CSV",
                "Импортировать задачи из CSV",
                "Назад"
            ]
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            action = input("Выберите действие: ")

            if action == "1":
                self.create_task()
            elif action == "2":
                self.list_tasks()
            elif action == "3":
                self.mark_task_done()
            elif action == "4":
                self.delete_task()
            elif action == "5":
                try:
                    self.export_tasks_to_csv()
                except ValueError as e:
                    print(e)
            elif action == "6":
                self.import_tasks_from_csv()
            elif action == "7":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    # Создание новой задачи
    def create_task(self):
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        priority = input("Введите приоритет (Высокий/Средний/Низкий): ")
        due_date_str = input("Введите срок выполнения (в формате DD-MM-YYYY): ")
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, False, priority.capitalize(), due_date_str)
        self.tasks.append(new_task.to_dict())
        self.save_data(FILES['tasks'], self.tasks)
        print("Задача успешно добавлена.")

    # Просмотр списка задач
    def list_tasks(self):
        if not self.tasks:
            print("\nСписок задач пуст.")
            return

        print("\nСписок задач:")
        for task in sorted(self.tasks, key=lambda x: x["due_date"]):  # Сортировка по сроку выполнения
            status = "Выполнено" if task["done"] else "Не выполнено"
            print(f"ID: {task['id']}, Название: {task['title']}, Статус: {status}, Приоритет: {task['priority']}, Срок: {task['due_date']}")

    # Отметка задачи как выполненной
    def mark_task_done(self):
        task_id = int(input("Введите ID задачи для отметки как выполненной: "))
        task = next((task for task in self.tasks if task["id"] == task_id), None)

        if task is not None:
            task["done"] = True
            self.save_data(FILES["tasks"], self.tasks)
            print("Задача отмечена как выполненная.")
        else:
            print("Задача не найдена.")

    # Удаление задачи по ID
    def delete_task(self):
        task_id = int(input("Введите ID задачи для удаления: "))
        tasks_after_deletion = [task for task in self.tasks if task["id"] != task_id]

        if len(tasks_after_deletion) < len(self.tasks):
            self.tasks = tasks_after_deletion
            self.save_data(FILES["tasks"], self.tasks)
            print("Задача успешно удалена.")
        else:
            print("Задача не найдена.")

    # Импортирование задач из CSV файла
    def import_tasks_from_csv(self):
        filename = "tasks.csv"

        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    row['id'] = int(row['id'])
                    row['done'] = row.get('done', 'False') == 'True'
                    self.tasks.append(row)

            self.save_data(FILES["tasks"], self.tasks)
            print(f"Задачи импортированы из файла {filename}.")
        except FileNotFoundError:
            print("Файл не найден.")

    # Экспортирование задач в CSV файл
    def export_tasks_to_csv(self):
        if not self.tasks:
            raise ValueError("Нет данных для экспорта. Список задач пуст.")

        with open('tasks_export.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.tasks[0].keys())
            writer.writeheader()
            writer.writerows(self.tasks)

        print(f"Задачи экспортированы в файл tasks_export.csv.")

    # Меню управления контактами
    def contacts_menu(self):
        while True:
            print("\nУправление контактами:")
            options = [
                "Добавить контакт",
                "Просмотреть контакты",
                "Удалить контакт",
                "Экспортировать контакты в CSV",
                "Импортировать контакты из CSV",
                "Назад"
            ]
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            action = input("Выберите действие: ")

            if action == "1":
                self.add_contact()
            elif action == "2":
                self.list_contacts()
            elif action == "3":
                self.delete_contact()
            elif action == "4":
                try:
                    self.export_contacts_to_csv()
                except ValueError as e:
                    print(e)
            elif action == "5":
                self.import_contacts_from_csv()
            elif action == "6":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    # Добавление нового контакта
    def add_contact(self):
        name = input("Введите имя контакта: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите адрес электронной почты: ")
        contact_id = len(self.contacts) + 1

        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact.to_dict())
        self.save_data(FILES["contacts"], self.contacts)
        print("Контакт успешно добавлен.")

    # Просмотр списка контактов
    def list_contacts(self):
        if not self.contacts:
            print("\nСписок контактов пуст.")
            return

        print("\nСписок контактов:")
        for contact in self.contacts:
            print(f"ID: {contact['id']}, Имя: {contact['name']}, Телефон: {contact['phone']}, Email: {contact['email']}")

    # Удаление контакта по ID
    def delete_contact(self):
        contact_id = int(input("Введите ID контакта для удаления: "))
        contacts = [c for c in self.contacts if c['id'] != contact_id]

        if len(contacts) < len(self.contacts):
            self.contacts = contacts
            self.save_data(FILES["contacts"], self.contacts)
            print("Контакт успешно удален.")
        else:
            print("Контакт не найден.")

    # Импортирование контактов из CSV файла
    def import_contacts_from_csv(self):
        filename = "contacts.csv"

        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.contacts = [row for row in reader]
            self.save_data(FILES["contacts"], self.contacts)
            print(f"Контакты импортированы из файла {filename}.")
        except FileNotFoundError:
            print("Файл не найден.")

    # Экспортирование контактов в CSV файл
    def export_contacts_to_csv(self):
        if not self.contacts:
            raise ValueError("Нет данных для экспорта. Список контактов пуст.")

        with open('contacts_export.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.contacts[0].keys())
            writer.writeheader()
            writer.writerows(self.contacts)
        print(f"Контакты экспортированы в файл 'contacts_export.csv'.")

    # Меню управления финансами
    def finance_menu(self):
        while True:
            print("\nУправление финансовыми записями:")
            options = [
                'Добавить запись',
                'Просмотреть записи',
                'Экспортировать в CSV',
                'Импортировать из CSV',
                'Назад']
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            action = input("Выберите действие: ")

            if action == "1":
                self.add_finance_record()
            elif action == "2":
                self.list_finance_records()
            elif action == "3":
                try:
                    self.export_finances_to_csv()
                except ValueError as e:
                    print(e)
            elif action == "4":
                self.import_finances_from_csv()
            elif action == "5":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    # Добавление финансов
    def add_finance_record(self):
        amount = float(input("Введите сумму: "))
        category = input("Введите категорию (доход/расход): ")
        date = input("Введите дату (в формате DD-MM-YYYY): ")
        description = input("Введите описание: ")
        record_id = len(self.finances) + 1
        new_record = FinanceRecord(record_id, amount, category, date, description)
        self.finances.append(new_record.to_dict())
        self.save_data(FILES["finance"], self.finances)
        print("Финансовая запись добавлена.")

    # Просмотр списка финансов
    def list_finance_records(self):
        if not self.finances:
            print("\nСписок финансовых записей пуст.")
            return

        print("\nСписок финансовых записей:")
        for record in self.finances:
            print(f"ID: {record['id']}, Сумма: {record['amount']}, Категория: {record['category']}, Дата: {record['date']}, Описание: {record['description']}")

    # Импортирование финансов из CSV файла
    def import_finances_from_csv(self):
        filename = 'finance_records.csv'

        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.finances = [row for row in reader]
            self.save_data(FILES["finance"], self.finances)
            print(f"Финансовые записи импортированы из файла {filename}.")
        except FileNotFoundError:
            print("Файл не найден.")

    # Экспортирование финансов из CSV файла
    def export_finances_to_csv(self):
        if not self.finances:
            raise ValueError("Нет данных для экспорта. Список финансовых записей пуст.")

        with open('finance_export.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.finances[0].keys())
            writer.writeheader()
            writer.writerows(self.finances)
        print(f"Финансовые записи экспортированы в файл 'finance_export.csv'.")

    # Общие функции для загрузки/сохранения
    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self, filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def calculator(self):
        print("\nКалькулятор:")
        expression = input("Введите математическое выражение: ")
        try:
            result = eval(expression)
            print(f"Результат: {result}")
        except Exception as err:
            print(f"Ошибка: {err}")


if __name__ == "__main__":
    app = PersonalAssistant()
    app.main_menu()
