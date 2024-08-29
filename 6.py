import time
import heapq

class Task:
    __name: str
    __duration: int

    def __init__(self, name: str, duration: int, priority: int, status: str = 'pending') -> None:
        self.__name = name
        self.__duration = duration
        self.__priority = priority
        self.__status = status

    def __lt__(self, other: "Task"):
        return self.__priority < other.__priority

    def __le__(self, other: "Task"):
        return self.__priority <= other.__priority

    def __gt__(self, other: "Task"):
        return self.__priority > other.__priority

    def __ge__(self, other: "Task"):
        return self.__priority >= other.__priority

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def name(self) -> str:
        return self.__name

    def set_in_progress(self):
        self.__status = 'in progress'

    def set_completed(self):
        self.__status = 'completed'

    def __str__(self):
        return (f'"{self.name}" время выполнения {self.duration} сек., приоритет {'высокий' if not self.__priority else 'низкий'},'
                f'статус - "{self.__status}"')

class TaskScheduler:
    def __init__(self) -> None:
        self.__tasks = []

    def add_task(self, task: Task) -> None:
        heapq.heappush(self.__tasks, task)

    def execute_tasks(self) -> None:
        while self.is_empty():
            try:
                task = heapq.heappop(self.__tasks)
                task.set_in_progress()
                print(task, "| Для отмены нажмите Ctrl+C")
                time.sleep(task.duration)
                task.set_completed()
                print(task)
            except KeyboardInterrupt:
                print('Задача прервана! Переход к следующей задаче.')

    def is_empty(self) -> bool:
        return bool(len(self.__tasks))

    def task_count(self) -> int:
        return len(self.__tasks)

my_scheduler = TaskScheduler()

my_scheduler.add_task(Task('Запуск двигателя', 3, 0))
my_scheduler.add_task(Task('Прогрев двигателя до рабочей температуры', 12, 1))
my_scheduler.add_task(Task('Проверка систем', 7, 1))
my_scheduler.add_task(Task('Подача нагрузки', 2, 0))
my_scheduler.add_task(Task('Работа', 13, 0))

print(my_scheduler.is_empty())

my_scheduler.execute_tasks()
