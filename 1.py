def avg(values: list[int | float] | tuple[int  | float]) -> float | None:
    total = 0.0
    for value in values:
        if type(value) in (int, float):
            total += value
        else:
            raise TypeError('Invalid data type, enter an integer or float number')
    return round(total/len(values), 2)


try:
    print(avg([3, 1, 4, 1, 5, 9, 2, 6, 5]))
except Exception as e:
    print(e)
