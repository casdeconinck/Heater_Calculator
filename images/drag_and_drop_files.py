import tkinter as tk

from TkinterDnD2 import DND_FILES, TkinterDnD
PATH = ""


def drop_inside_list_box(event):
    global PATH
    listb.insert("end", event.data)
    PATH = event.data


def start():
    global PATH
    if PATH == "":
        print("No file was found")
    else:
        f = open(PATH, "r")
        print(f.read())


window = TkinterDnD.Tk()
window.geometry("800x500")
listb = tk.Listbox(window, selectmode=tk.SINGLE, background="green")
listb.pack(fill=tk.X)
listb.drop_target_register(DND_FILES)
listb.dnd_bind("<<Drop>>", drop_inside_list_box)

b = tk.Button(text="go", command=start)
b.pack()

window.mainloop()
