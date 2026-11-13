score_input = input("Введите балл (0-100): ")

if score_input.isdigit():
    score = int(score_input)
    if 0 <= score <= 100:
        if score >= 90:
            grade = "A"
        elif score >= 75:
            grade = "B"
        elif score >= 50:
            grade = "C"
        else:
            grade = "F"
        print(f"Оценка: {grade}")
    else:
        print("Ошибка: балл должен быть в диапазоне от 0 до 100.")
else:
        print("Ошибка: введено нечисловое значение.")