import tkinter as t
from tkinter import filedialog
from tkinter import ttk
import pefile
import subprocess
from os import _exit

def run_dll():
    args = entry.get()
    point = combobox.get()
    if (args == ""):
        cmd = f'rundll32.exe "{dll_path}",{point}'
    else:
        cmd = f'rundll32.exe "{dll_path}",{point} {args}'
    try:
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        t.messagebox.showerror("Ошибка запуска", str(e))
def get_exports(path):
    try:
        pe = pefile.PE(path)
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            return [exp.name.decode('utf-8') for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols if exp.name]
    except Exception as e:
        t.messagebox.showerror("Ошибка", "Непредвиденная ошибка, непозволяющая открыть файл!")
        _exit(1)
    return []
def canceled():
    root.destroy()    

def select_file():
    file = filedialog.askopenfilename(title="Выберете библиотеку", filetypes=[("Библиотеки", "*.dll;*.cpl"), ("Все файлы", "*.*")])
    if (file != ""):
        return file
    else:
        t.messagebox.showerror("Парсер DLL", "Файл не выбран!")
        _exit(0)

dll_path = select_file()

root = t.Tk()
root.title("Парсер DLL")
root.geometry("250x200")
root.resizable(False, False)
root.iconbitmap("./res/icon.ico")

dll_commands = get_exports(dll_path)

text1 = ttk.Label(root, text="Выберете точку входа:")
text2 = ttk.Label(root, text="Аргументы командной строки:")
combobox = ttk.Combobox(root, values=dll_commands)
entry = ttk.Entry(root)
сancel = ttk.Button(root, text="Отмена", command=canceled)
launch = ttk.Button(root, text="Запустить!", command=run_dll)

if dll_commands:
    combobox.current(0)

text1.place(x=3, y=3)
combobox.place(x=3, y=23, width=150)
text2.place(x=3, y=53)
entry.place(x=3, y=73, width=150)
launch.place(anchor="se", x=245, y=195)
сancel.place(anchor="se", x=165, y=195)

root.mainloop()

