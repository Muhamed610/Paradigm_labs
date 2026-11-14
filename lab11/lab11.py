import tkinter as tk
from tkinter import ttk, messagebox

# Создание корневого окна
root = tk.Tk()
root.title('Запись на факультатив')
root.geometry('650x430')

# Переменные интерфейса (состояние)
student_var = tk.StringVar()
course_var = tk.StringVar(value='Веб-разработка')
status_var = tk.StringVar(value='Готово')
count_var = tk.StringVar(value='Регистраций: 0')

# Модель данных (обычный список Python)
registrations = []

# Функции управления статусом через after
def reset_status():
    status_var.set('Готово')

def set_status(text):
    status_var.set(text)
    root.after(2500, reset_status)

# Основная бизнес-логика регистрации
def register():
    student = student_var.get().strip()
    course = course_var.get()
    
    if len(student) < 2:
        messagebox.showwarning('Проверка', 'Введите имя студента')
        student_entry.focus_set()
        return
        
    item = (student, course)
    if item in registrations:
        set_status('Такая запись уже существует')
        return
        
    registrations.append(item)
    result_list.insert(tk.END, f'{student} — {course}')
    count_var.set(f'Регистраций: {len(registrations)}')
    set_status('Запись добавлена')
    
    student_var.set('')
    student_entry.focus_set()

# Адаптер для вызова из событий (Enter)
def register_from_event(event):
    register()

# Функция удаления выбранной записи (Вариант 1)
def delete_selected(event=None):
    selected_indices = result_list.curselection()
    if not selected_indices:
        set_status('Выберите запись для удаления')
        return
    
    index = selected_indices[0]
    removed_item = registrations.pop(index)
    result_list.delete(index)
    
    count_var.set(f'Регистраций: {len(registrations)}')
    set_status(f'Удалено: {removed_item[0]}')
    student_entry.focus_set()

# Функция очистки всего списка
def clear_all():
    if not registrations:
        set_status('Список уже пуст')
        return
    if not messagebox.askyesno('Подтверждение', 'Удалить все записи?'):
        return
    registrations.clear()
    result_list.delete(0, tk.END)
    count_var.set('Регистраций: 0')
    set_status('Список очищен')
    student_entry.focus_set()

# Создание интерфейса
frame = ttk.Frame(root, padding=16)
frame.pack(fill='both', expand=True)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)

# Метки и поле ввода имени
ttk.Label(frame, text='ФИО студента').grid(row=0, column=0, sticky='w', pady=5)
student_entry = ttk.Entry(frame, textvariable=student_var)
student_entry.grid(row=0, column=1, columnspan=3, sticky='ew', padx=8, pady=5)

# Выпадающий список факультативов
ttk.Label(frame, text='Факультатив').grid(row=1, column=0, sticky='w', pady=5)
course_box = ttk.Combobox(
    frame, textvariable=course_var, state='readonly',
    values=['Веб-разработка', 'Алгоритмы ИИ', 'Кибербезопасность', 'Мобильная разработка']
)
course_box.grid(row=1, column=1, columnspan=3, sticky='ew', padx=8, pady=5)

# Кнопки управления (теперь три кнопки: Регистрация, Удалить выбранное, Очистить всё)
register_button = ttk.Button(frame, text='Зарегистрировать', command=register)
register_button.grid(row=2, column=1, sticky='ew', padx=4, pady=8)

delete_button = ttk.Button(frame, text='Удалить выбранное', command=delete_selected)
delete_button.grid(row=2, column=2, sticky='ew', padx=4, pady=8)

clear_button = ttk.Button(frame, text='Очистить список', command=clear_all)
clear_button.grid(row=2, column=3, sticky='ew', padx=4, pady=8)

# Список результатов (Listbox)
result_list = tk.Listbox(frame, height=10)
result_list.grid(row=3, column=0, columnspan=4, sticky='nsew', pady=8)

# Строка состояния и счетчик
ttk.Label(frame, textvariable=count_var).grid(row=4, column=0, sticky='w')
ttk.Label(frame, textvariable=status_var).grid(row=4, column=1, columnspan=3, sticky='e')

# Регистрация событий (bind и фокус)
root.bind('<Return>', register_from_event)
result_list.bind('<Delete>', delete_selected)  # Дублируем удаление по клавише Delete
student_entry.focus_set()

# Запуск главного цикла
root.mainloop()