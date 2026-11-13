numbers = [12, 5, 8, 3, 21, 0, 14, -7]

sum_total = 0
sum_positive = 0
count_positive = 0
count_negative = 0
count_zero = 0

for num in numbers:
    sum_total += num
    if num > 0:
        sum_positive += num
        count_positive += 1
    elif num < 0:
        count_negative += 1
    else:
        count_zero += 1

print(f"Сумма всех чисел: {sum_total}")
print(f"Сумма положительных чисел: {sum_positive}")
print(f"Количество положительных: {count_positive}")
print(f"Количество отрицательных: {count_negative}")
print(f"Количество нулей: {count_zero}")