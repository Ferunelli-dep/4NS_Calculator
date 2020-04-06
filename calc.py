from tkinter import *
from tkinter import messagebox as messagebox


class Calculator(Frame):
    lbl: Label
    formula: str

    def __init__(self, root):
        super(Calculator, self).__init__(root)
        self.root = root
        self.result = "+"
        self.build()

    def build(self):
        self.formula = "0"
        self.lbl = Label(text=self.formula, font=("Times New Roman", 21, "bold"), bg="#DDD", foreground="#333")
        self.lbl.place(x=11, y=50)

        btns = [
            "C", "DEL", "+",
            "1", "2", "-",
            "0", "3", ".",
            "="
        ]

        x = 10
        y = 140
        for bt in btns:
            com = lambda x=bt: self.logicalc(x)
            if bt != "=":
                Button(text=bt, bg="#333333",
                       font=("Times New Roman", 15),
                       fg = "#DDD",
                       command=com).place(x=x, y=y,
                                          width=115,
                                          height=79)
            else:
                Button(text=bt, bg="#333333",
                       font=("Times New Roman", 15),
                       fg = "#DDD",
                       command=com).place(x=x, y=y,
                                          width=350,
                                          height=79)
            x += 117
            if x > 280:
                x = 10
                y += 81
        mainmenu = Menu(self.root)
        self.root.config(menu=mainmenu)
        option_menu = Menu(mainmenu, tearoff=0)
        mainmenu.add_cascade(label="Команды", menu=option_menu)
        option_menu.add_command(label="Сложение (+)", command=lambda: self.logicalc('+'))
        option_menu.add_command(label="Вычитание (-)", command=lambda: self.logicalc('-'))
        option_menu.add_command(label="Результат (=)", command=lambda: self.logicalc('='))
        option_menu.add_command(label="Выход", command=self.onQuit)
        mainmenu.add_command(label="О программе", command=self.info)

    @staticmethod
    def translate_to(number):
        nums, flag_dot, sign = [i for i in str(number)], False, 1
        if nums[0] == "-":
            sign = -1
            nums.remove("-")
        try:
            max_power = nums.index(".") - 1
            flag_dot = True
        except ValueError:
            max_power = len(nums) - 1
        if max_power == -1:
            nums.insert(0, "0")
            max_power = 0

        if flag_dot and len(nums) == (max_power + 3) and nums[-1] == "0":
            min_power = 0
        elif flag_dot:
            min_power = -(len(nums) - max_power - 2)
        else:
            min_power = 0
        try:
            nums.remove(".")
        except:
            pass
        res = 0
        n = 0
        for i in range(max_power, min_power - 1, -1):
            res += int(nums[n]) * 4 ** i
            n += 1
        return res * sign

    @staticmethod
    def calc_and_trans(expr):
        try:
            num = str(eval(expr))
        except:
            return
        sign = 1
        nums = num.split(".")
        if nums[0][0] == '-':
            sign = -1
            nums[0] = str(abs(int(nums[0])))
        int_part = int(nums[0])
        mods = []
        while int_part != 0:
            mods.append(str(int_part % 4))
            int_part //= 4
        mods.reverse()
        try:
            int_part = int("".join(mods))
        except ValueError:
            int_part = 0
        if len(nums) == 1:
            return str(sign * int_part)
        else:
            float_part = float("0." + nums[1])
            n = 0
            float_nums = []
            while float_part != 0.0 or n < 8:
                float_part *= 4
                if float_part >= 1:
                    float_nums.append(str(int(float_part)))
                    float_part -= int(float_part)
                else:
                    float_nums.append('0')
                n += 1
            float_part = '0.' + "".join(float_nums)
            try:
                result = sign * (float(int_part) + float(float_part))
            except ValueError:
                try:
                    result = sign * (0.0 + float(float_part))
                except ValueError:
                    result = 0
            return str(result)

    def logicalc(self, operation):
        if operation == "C":
            self.formula = ""
        elif operation == "DEL":
            self.formula = self.formula[0:-1]
        elif operation == "=":
            self.result += str(self.translate_to(self.formula))
            self.formula = self.calc_and_trans(self.result)
            self.result = ""
        elif operation == "+":
            if self.formula == "0":
                pass
            else:
                self.result += str(self.translate_to(self.formula)) + " + "
                self.formula = "0"
        elif operation == "-" and self.formula != "0":
            self.result += str(self.translate_to(self.formula)) + " - "
            self.formula = "0"
        else:
            if self.formula == "0":
                self.formula = ""
            if operation != "." or self.formula.count(".") < 1:
                self.formula += operation
            if len(self.result) == 0:
                self.formula = ""
                self.result += "+"
                self.formula += operation
        self.update()

    def key(self, event):
        if event.char in ["0", "1", "2", "3", "-", ".", "+", "="] or event.keysym == "BackSpace":
            if event.keysym == "BackSpace":
                event.char = "DEL"
            if event.char == "." and self.formula.count(".") < 1 or event.char != ".":
                self.logicalc(event.char)

    def update(self):
        if self.formula == "":
            self.formula = "0"
        if len(self.formula) < 24:
            self.lbl.configure(text=self.formula)

    @staticmethod
    def info():
        messagebox.showinfo(message='Калькулятор вычитает и складывает в четверичной СС')

    def onQuit(self):
        self.quit()
