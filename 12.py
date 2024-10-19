from datetime import datetime
import asyncio
import random

# Паттерн "Команда" для инкапсуляции каждой задачи в виде отдельного объекта с функцией выполнения
class Task:
    __task_id = 0
    def __init__(self, specification: str):
        self._specification = specification
        self._task_id = Task.__task_id
        self._created_date = datetime.now()
        Task.__task_id += 1

    def __str__(self) -> str:
        return f"Описание: {self._specification}, id: {self._task_id}, дата создания: {self._created_date}"

    async def execute(self):
        delay = round(random.random() * 10, 2)
        await asyncio.sleep(delay)
        print(f"{self} - выполнена за: {delay} сек.")

    @property
    def task_id(self) -> int:
        return self._task_id

    @property
    def created_date(self) -> datetime:
        return self._created_date

# Патерн одиночка для глобальной очереди заданий
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

class GlobalTasksQueue(metaclass=SingletonMeta):
    """
    Класс GlobalTasksQueue использует метакласс SingletonMeta.
    """
    def __init__(self):
        self._queue = []

    def __sort(self) -> list[Task]:
        tasks = self._queue
        for i in range(len(tasks)-1):
            for j in range(len(tasks)-1-i):
                if tasks[j].created_date > tasks[j+1].created_date:
                    tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]
        return tasks

    def __str__(self) -> None:
        result = ''
        for task in self._queue:
            result += f"{task}\n"
        return result

    def show_tasks(self) -> None:
        for task in self.__sort():
            print(task)

    def add_task(self, task: Task) -> None:
        self._queue.append(task)

    async def execute_tasks(self) -> None:
        tasks = [task.execute() for task in self._queue]
        await asyncio.gather(*tasks)

    def find_task_by_id(self, task_id: int) -> None:
        for task in self._queue:
            if task.task_id == task_id:
                print(f"Найдена задача - ({task})")
                return
        print(f"Задачи с id: {task_id} не найдено!")

    def delete_task_by_id(self, task_id: int) -> None:
        for task in self._queue:
            if task.task_id == task_id:
                self._queue.remove(task)
                print(f"Задачи с id: {task_id} удалена!")
                return
        print(f"Не удалось удалить задачу с id: {task_id} (id не найден)!")


async def main():
    tasks = GlobalTasksQueue()
    while True:
        print("1. Добавление задачи: \n2. Удаление задачи по ID: \n3. Запуск задач: \n4. Просмотр списка задач: \n"
              "5. Поиск задачи по ID: \n6. Выйти из программы")
        cmd = input("Введите номер команды: ")

        if cmd == "1":
            task_specification = input("Для добавления задачи введите ее описание : ")
            task = Task(task_specification)
            tasks.add_task(task)
            print(f"Добавлена задача - ({task})")
        elif cmd == "2":
            task_id = int(input("Для удаления задачи введите ее id : "))
            tasks.delete_task_by_id(task_id)
        elif cmd == "3":
            print("Запуск задач:")
            await tasks.execute_tasks()
        elif cmd == "4":
            print("Список задач:")
            tasks.show_tasks()
        elif cmd == "5":
            task_id = int(input("Для поиска задачи введите ее id : "))
            tasks.find_task_by_id(task_id)
        elif cmd == "6":
            print("Программа завершина")
            break
        else:
            print("Неверная команда")
        print("_______________________________________")

if __name__ == "__main__":
    asyncio.run(main())


