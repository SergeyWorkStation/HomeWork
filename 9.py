from functools import partial


def hours_per_day(hours: int):
    return lambda day: hours*day

# Пример использования
result = hours_per_day(8)(20)  # 160
print(result)


def bonus_percentage(percentage):
    return lambda salary: percentage*salary//100

# Пример использования
result = bonus_percentage(10)(3000)  # 300
print(result)


def net_salary(gross_salary, tax_rate):
    return int(gross_salary-(gross_salary*tax_rate))

# Создаем функцию с фиксированным налогом 20%
tax_20 = partial(net_salary, tax_rate=0.20)
result = tax_20(5000)  # 5000 - (5000 * 0.20) = 4000
print(result)


def final_salary(base_salary, bonus):
    return base_salary + bonus

# Создаем функцию с фиксированным бонусом 500
bonus_500 = partial(final_salary, bonus=500)
result = bonus_500(3000)  # 3000 + 500 = 3500
print(result)


def calculate_hours(hours_per_day, days):
    return hours_per_day*days

def calculate_gross_salary(hours, hourly_rate):
    return hours*hourly_rate

def composed_salary_function(hours_per_day, days, hourly_rate):
    return calculate_gross_salary(calculate_hours(hours_per_day, days), hourly_rate)

# Пример использования
result = composed_salary_function(8, 20, 25)  # (8 * 20) * 25 = 4000
print(result)


def calculate_net_salary(gross_salary):
    return int(gross_salary-(gross_salary*0.20))

def apply_bonus(salary, bonus):
    return salary+bonus

def final_salary_composition(gross_salary, bonus):
    return calculate_net_salary(apply_bonus(gross_salary, bonus))

# Пример использования

result = final_salary_composition(4000, 300)  # (4000 + 300) - ((4000 + 300) * 0.20) = 3440
print(result)
