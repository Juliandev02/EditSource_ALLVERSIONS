import subprocess
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import psutil

compiler = Tk()
compiler.title('Edit-Source 0.01.1')
file_path = ''

need_save = "Ein Fehler ist im Hauptprozess aufgetreten \n*******************************************"
started = f"=> Edit Source wurde erfolgreich gestartet!"


def set_file_path(path):
    global file_path
    file_path = path

def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)

def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text=f'{need_save} \nBitte speichere deinen Skript!', height=5, width=40)
        text.pack()
        save_prompt.title('Fehler aufgetreten!')
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0',  error)
    code_output.insert("3.0", "\n")



def close():
    exit("=> IDE was closed")


menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Öffnen', command=open_file)
file_menu.add_command(label='Speichern', command=save_as)
file_menu.add_command(label='Speichern unter', command=save_as)
file_menu.add_command(label='Verlassen', command=close)

menu_bar.add_cascade(label='Datei', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)

menu_bar.add_cascade(label='Ausführen', menu=run_bar)



compiler.config(menu=menu_bar)

editor = Text()
editor.pack()

code_output = Text(height=10, width=100)
code_output.pack()
code_output.insert("1.0", started)

compiler.mainloop()