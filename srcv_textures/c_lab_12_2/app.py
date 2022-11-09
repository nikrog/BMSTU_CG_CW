import ctypes
import tkinter as tk
import tkinter.messagebox as box

lib = ctypes.CDLL('./libarr.dll')

# void ill_array_prime_num(int *arr, int n)
_fill_array_prime_num = lib.fill_array_prime_num
_fill_array_prime_num.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
_fill_array_prime_num.restype = None


def fill_array_prime_num(n):
    arr = (ctypes.c_int * n)()
    _fill_array_prime_num(arr, n)
    return list(arr)


# int insert_num_after_even(int *src, int n1, int *dst, int *n2, int num)
_insert_num_after_even = lib.insert_num_after_even
_insert_num_after_even.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int,
                                   ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                                   ctypes.c_int)
_insert_num_after_even.restype = ctypes.c_int


def insert_num_after_even(nums, num, fl):
    n = len(nums)
    n_dst = 0
    arr = (ctypes.c_int * n)(*nums)
    if fl == 1:
        n_dst = ctypes.c_int(2 * n)
    elif fl == 2:
        n_dst = ctypes.c_int(0)
        _insert_num_after_even(arr, n, None, n_dst, num)
    dst = (ctypes.c_int * n_dst.value)()
    _insert_num_after_even(arr, n, dst, n_dst, num)
    return n_dst, list(dst)


def clean():
    entry_num.delete(0, tk.END)
    entry_res1.delete(0, tk.END)
    entry_res2.delete(0, tk.END)
    entry_arr.delete(0, tk.END)
    entry_num2.delete(0, tk.END)


def print_arr(arr, n, field):
    field.delete(0, tk.END)
    for i in range(n):
        field.insert('insert', str(arr[i]) + ' ')


def task_1():
    n = entry_num.get()
    try:
        n = int(n)
    except:
        box.showerror('Ошибка', "n должно быть целым положительным числом!")
        return
    if n <= 0:
        box.showerror('Ошибка', "n должно быть целым положительным числом!")
        return

    arr = fill_array_prime_num(n)

    print_arr(arr, len(arr), entry_res1)


def task_2():
    arr_str = entry_arr.get()
    try:
        arr = [int(x) for x in arr_str.split()]
    except:
        box.showerror('Ошибка', "Элементы массива должны быть целыми числами!")
        return
    n = len(arr)
    if n == 0:
        box.showerror('Ошибка', "Массив не должен быть пустым!")
        return
    num = entry_num2.get()
    try:
        num = int(num)
    except:
        box.showerror('Ошибка', "num должно быть целым числом!")
        return
    # обработка
    global fl
    n_res, res = insert_num_after_even(arr, num, fl.get())

    print_arr(res, n_res.value, entry_res2)


# create window
root = tk.Tk()
root.title('Лабораторная работа №12 (Вариант 3) Артюхин Николай ИУ7-31Б')
root.geometry('750x600')
root['bg'] = ('lime')

# task 1
lbl_task1 = tk.Label(root, text='Задача 1. Заполнить массив из n элементов простыми числами.',
                     font='arial 14 bold', justify=tk.LEFT, bd=1, bg='bisque')
lbl_task1.place(x=10, y=10, width=730, height=30, anchor=tk.NW)

lbl_num = tk.Label(root, text='Введите n (целое > 0):',
                   font='arial 13', justify=tk.LEFT, bg='white')
lbl_num.place(x=10, y=50, width=200, height=30, anchor=tk.NW)

entry_num = tk.Entry(root, justify=tk.LEFT,
                     font='arial 13', bg="yellow")
entry_num.place(x=210, y=50, width=80, height=30, anchor=tk.NW)

but_num = tk.Button(root, text='Ввод', font='arial 13', justify=tk.LEFT,
                    command=task_1, bg='green')
but_num.place(x=300, y=50, width=100, height=30)

lbl_res1 = tk.Label(root, text='Результат:',
                    font='arial 13', justify=tk.LEFT, bg='white')
lbl_res1.place(x=10, y=100, width=100, height=30, anchor=tk.NW)

entry_res1 = tk.Entry(root, justify=tk.LEFT,
                      font='arial 13', bg="yellow")
entry_res1.place(x=110, y=100, width=600, height=30, anchor=tk.NW)

# task 2
lbl_task2 = tk.Label(root, text='Задача 2. Добавить после каждого четного элемента массива число num.',
                     font='arial 14 bold', justify=tk.LEFT, bd=1, bg='bisque')
lbl_task2.place(x=10, y=170, width=730, height=30, anchor=tk.NW)

lbl_fl = tk.Label(root, text='Выберите способ выделения памяти под массив:',
                   font='arial 13', justify=tk.LEFT, bd=1, bg='white')
lbl_fl.place(x=10, y=210, width=390, height=30, anchor=tk.NW)

fl = tk.IntVar()

fl1_checkbutton = tk.Radiobutton(text="выполнить оценку  максимально возможный размера массива и выделить память\n"
                                       "с запасом;",
                                  value=1, variable=fl, font='arial 13', justify=tk.LEFT, bd=1, bg='orange')

fl1_checkbutton.place(x=10, y=250, width=670, height=30, anchor=tk.NW)

fl2_checkbutton = tk.Radiobutton(text="cначала вызвать функцию библиотеки, чтобы узнать требуемый размер массива,\n"
                                       "затем выделить память и повторно вызвать функцию.",
                                  value=2, variable=fl, font='arial 13', justify=tk.LEFT, bd=1, bg='orange')
fl2_checkbutton.place(x=10, y=280, width=670, height=60, anchor=tk.NW)
fl2_checkbutton.select()
lbl_num2 = tk.Label(root, text='Введите число num (целое число):', font='arial 13', justify=tk.LEFT, bg='white')
lbl_num2.place(x=10, y=350, width=280, height=30, anchor=tk.NW)
entry_num2 = tk.Entry(root, justify=tk.LEFT, font='arial 13', bg='yellow')
entry_num2.place(x=290, y=350, width=80, height=30, anchor=tk.NW)
lbl_arr = tk.Label(root, text='Введите элементы исходного массива (через пробелы):',
                   font='arial 13', justify=tk.LEFT, bg='mint cream')
lbl_arr.place(x=10, y=400, width=450, height=30, anchor=tk.NW)

entry_arr = tk.Entry(root, justify=tk.LEFT,
                     font='arial 13', bg="yellow")
entry_arr.place(x=10, y=430, width=480, height=30, anchor=tk.NW)

but_arr = tk.Button(root, text='Ввод', font='arial 13', justify=tk.LEFT,
                    command=task_2, bg='green')
but_arr.place(x=500, y=430, width=100, height=30)

lbl_res2 = tk.Label(root, text='Результат:',
                    font='arial 13', justify=tk.LEFT, bg='mint cream')
lbl_res2.place(x=10, y=470, width=100, height=30, anchor=tk.NW)

entry_res2 = tk.Entry(root, justify=tk.LEFT,
                      font='arial 13', bg="yellow")
entry_res2.place(x=110, y=470, width=480, height=30, anchor=tk.NW)

but_clean = tk.Button(root, text='Очистка полей', font='arial 13', justify=tk.LEFT,
                      command=clean, bg='red')
but_clean.place(x=200, y=550, width=160, height=30)

#exit
but_exit = tk.Button(root, text='Выход', font='arial 13', justify=tk.LEFT,
                      command=quit, bg='red')
but_exit.place(x=400, y=550, width=160, height=30)

root.mainloop()
