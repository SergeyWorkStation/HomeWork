class Employee:
    def __init__(self, lastname: str, age: int, salary: float) -> None:
        self._lastname = lastname
        self._age = age
        self._salary = salary

    def __repr__(self) -> str:
        return f"Lastname:{self._lastname}, age:{self._age}, salary:{self._salary}"

    def get_by_criterion(self, criterion: str) -> str | int | float:
        if criterion.lower() == 'lastname':
            return self._lastname
        if criterion.lower() == 'age':
            return self._age
        if criterion.lower() == 'salary':
            return self._salary
        raise ValueError(f"incorrect criterion: '{criterion}'")


class Shell:
    def __init__(self, args: list[Employee]) -> None:
        self._args = args

    def __repr__(self) -> str:
        return '\n'.join(self._args)

    def sort(self, criterion: str) -> list:
        try:
            arr = self._args.copy()
            n = len(arr)
            gap = n // 2

            while gap > 0:
                for i in range(gap, n):
                    temp = arr[i]
                    j = i
                    while j >= gap and arr[j - gap].get_by_criterion(criterion) > temp.get_by_criterion(criterion):
                        arr[j] = arr[j - gap]
                        j -= gap
                    arr[j] = temp
                gap //= 2

            return arr
        except ValueError as e:
            return e


arr = [
    Employee('Sidorov', 45, 54442.557),
    Employee('Ivanov', 32, 5415652.24),
    Employee('Petrov', 18, 772.35)
]


print(arr)
print(Shell(arr).sort('lastname'))
print(Shell(arr).sort('AGE'))
print(Shell(arr).sort('Salary'))
