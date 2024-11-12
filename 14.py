import psycopg2

class SingletonMeta(type):
    """
    Это метакласс для реализации паттерна Singleton.
    Он управляет созданием единственного экземпляра класса.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class StudentDB(metaclass=SingletonMeta):

    def __database_request(self, query):
        try:
            conn = psycopg2.connect(
                user="root",
                password="MyPassword",
                host="127.0.0.1",
                port="5432",
                database="my_db"
            )
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(query=query)
        except Exception as error:
            print("Ошибка при подключении к PostgreSQL", error)
        finally:
            if conn:
                conn.close()


    def __database_response(self, query):
        try:
            conn = psycopg2.connect(
                user="root",
                password="MyPassword",
                host="127.0.0.1",
                port="5432",
                database="my_db"
            )
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(query=query)
                return cursor.fetchall()
        except Exception as error:
            print("Ошибка при подключении к PostgreSQL", error)
        finally:
            if conn:
                conn.close()


    def create_table(self):
        self.__database_request("""CREATE TABLE IF NOT EXISTS students( 
                                   students_id serial PRIMARY KEY,
                                   firstname_students varchar(30) NOT NULL,
                                   lastname_students varchar(30),
                                   course_number int NOT NULL,
                                   age int NOT NULL);
                                """
                                )
        print("Таблица создана")

    def insert_student(self, firstname_students, lastname_students, course_number, age):
        self.__database_request(f"""INSERT INTO students(firstname_students, lastname_students, course_number, age)
                                VALUES ('{firstname_students}', '{lastname_students}', {course_number}, {age});
                                """
                                )
        print("Студент добавлен")

    def __str__(self) -> None:
        result = "id, firstname, lastname, course, age\n"
        students = self.__database_response(f"""SELECT * FROM students ORDER BY students_id;""")
        for student in students:
            result += f"{student[0]}, \t{student[1]}, \t{student[2]}, \t{student[3]}, \t{student[4]}\n"
        return result

    def delete_student_by_id(self, student_id):
        self.__database_request(f"""DELETE FROM students
                                WHERE students_id={int(student_id)};""")
        print(f"Студент с id: {student_id} удален")

    def update_student_by_id(self, student_id, firstname_students, lastname_students, course_number, age):
        self.__database_request(f"""UPDATE students
                                SET firstname_students='{firstname_students}', 
                                lastname_students='{lastname_students}', 
                                course_number={course_number}, 
                                age={age}
                                WHERE students_id={int(student_id)};""")
        print(f"Студент с id: {student_id} изменен")


students = StudentDB()
students.create_table()
while True:
    print("1. Добавить студента: \n2. Удалить студента по ID: \n3. Изменить запись о студенте: "
          "\n4. Вывести список студентов \n5. Выйти из программы")
    cmd = input("Введите номер команды: ")

    if cmd == "1":
        firstname_students = input("Введите имя студента : ")
        lastname_students = input("Введите фамилию студента : ")
        course_number = int(input("Введите номер группы студента : "))
        age = int(input("Введите возраст студента : "))
        students.insert_student(firstname_students, lastname_students, course_number, age)
    elif cmd == "2":
        student_id = int(input("Для удаления студента введите его id : "))
        students.delete_student_by_id(student_id)
    elif cmd == "3":
        student_id = input("Введите id студента : ")
        firstname_students = input("Введите имя студента : ")
        lastname_students = input("Введите фамилию студента : ")
        course_number = int(input("Введите номер группы студента : "))
        age = int(input("Введите возраст студента : "))
        students.update_student_by_id(student_id, firstname_students, lastname_students, course_number, age)
    elif cmd == "4":
        print("Список студентов:\n")
        print(students)
    elif cmd == "5":
        print("Программа завершена")
        break
    else:
        print("Неверная команда")
    print("_______________________________________")




