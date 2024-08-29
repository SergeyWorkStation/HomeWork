import time

class Task:
    __name: str
    __duration: int

    def __init__(self, name: str, duration: int) -> None:
        self.__name = name
        self.__duration = duration

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def name(self) -> str:
        return self.__name


class TaskScheduler:
    def __init__(self) -> None:
        self.__tasks = []

    def add_task(self, task: Task) -> None:
        self.__tasks.append(task)

    def execute_tasks(self) -> None:
        while self.is_empty():
            task = self.__tasks.pop(0)
            time.sleep(task.duration)
            print(f'"{task.name}" выполнено за {task.duration} сек.')

    def is_empty(self) -> bool:
        return bool(len(self.__tasks))

    def task_count(self) -> int:
        return len(self.__tasks)

my_scheduler = TaskScheduler()

my_scheduler.add_task(Task('Запуск двигателя', 3))
my_scheduler.add_task(Task('Прогрев двигателя до рабочей температуры', 15))
my_scheduler.add_task(Task('Проверка систем', 7))
my_scheduler.add_task(Task('Подача нагрузки', 2))
my_scheduler.add_task(Task('Работа', 30))

print(my_scheduler.is_empty())

my_scheduler.execute_tasks()

print(my_scheduler.is_empty())