from calc import Calculator
from tkinter import *


if __name__ == '__main__':
    root = Tk()
    root["bg"] = "#DDD"
    root.geometry("370x475+500+200")
    root.title("Калькулятор")
    root.resizable(False, False)
    app = Calculator(root)
    app.pack()
    root.bind_all('<Key>', app.key)
    root.mainloop()
