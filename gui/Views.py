import tkinter as tk
from abc import abstractmethod
from tkinter import ttk


class View(tk.Frame):
    @abstractmethod
    def create_view(self):
        raise NotImplementedError


class Login(View):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.entries = {}
        self.buttons = {}
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=1, column=1, padx=25, pady=20, sticky=tk.N + tk.S + tk.E + tk.W)

    def create_view(self):
        control_frame = tk.LabelFrame(master=self, text="Login", font='Verdana 25 bold')
        control_frame.rowconfigure(0, weight=1)
        control_frame.columnconfigure(0, weight=1)
        control_frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.create_entry(
            control_frame, "User Name :", row=1, column=0, textvar=tk.StringVar()
        )

        self.create_entry(
            control_frame, "Password :", row=2, column=0, textvar=tk.StringVar()
        )

        self.create_button(control_frame, "Login", row=3, column=1, height=2, width=10)
        self.create_button(control_frame, "Clear", row=3, column=2, height=2, width=10)
        self.create_button(control_frame, "Switch To Sign up", row=0, column=2, height=2, width=20)

    def create_entry(self, frame, label, row, column, textvar):
        label_frame = tk.LabelFrame(frame, text=label)
        self.entries[label] = tk.Entry(label_frame, width=25, textvariable=textvar)
        self.entries[label].grid(row=1, column=1)
        label_frame.grid(row=row, column=column, sticky=tk.N + tk.S + tk.E + tk.W)

    def create_button(self, frame, name, row, column, height, width):
        self.buttons[name] = tk.Button(frame)
        self.buttons[name]["text"] = name
        self.buttons[name].grid(row=row, column=column)
        self.buttons[name]["height"] = height
        self.buttons[name]["width"] = width



class Signup(Login):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.comboboxes = {}
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=1, column=1, padx=25, pady=20, sticky=tk.N + tk.S + tk.E + tk.W)

    def create_view(self):
        control_frame = tk.LabelFrame(master=self, text="Signup", font='Verdana 20 bold')
        control_frame.rowconfigure(0, weight=1)
        control_frame.columnconfigure(0, weight=1)
        control_frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.create_entry(
            control_frame, "First Name :", row=1, column=0, textvar=tk.StringVar()
        )

        self.create_entry(
            control_frame, "Last Name :", row=2, column=0, textvar=tk.StringVar()
        )

        self.create_entry(
            control_frame, "Age :", row=3, column=0, textvar=tk.IntVar(value=0)  # Check
        )

        self.create_combobox(
            control_frame, "Gender :", row=4, column=0, values=["Male", "Female"]
        )

        self.create_entry(
            control_frame, "Phone Number :", row=5, column=0, textvar=tk.StringVar()  # No
        )

        self.create_entry(
            control_frame, "City :", row=6, column=0, textvar=tk.StringVar()
        )

        self.create_entry(
            control_frame, "Address :", row=7, column=0, textvar=tk.StringVar()
        )

        self.create_entry(
            control_frame, "User Name :", row=8, column=0, textvar=tk.StringVar()
        )

        self.create_entry(
            control_frame, "Password :", row=9, column=0, textvar=tk.StringVar()
        )

        self.create_entry_show(
            control_frame, "Verify Password :", row=10, column=0, textvar=tk.StringVar()
        )

        self.create_button(control_frame, "Signup", row=12, column=1, height=2, width=10)
        self.create_button(control_frame, "Clear", row=12, column=4, height=2, width=10)
        self.create_button(control_frame, "Switch To Login", row=0, column=4, height=2, width=20)

    def create_combobox(self, frame, label, values, row, column):
        label_frame = tk.LabelFrame(frame, text=label)
        self.comboboxes[label] = ttk.Combobox(label_frame, values=values)
        self.comboboxes[label]['state'] = 'readonly'  ##
        self.comboboxes[label].set('None')
        self.comboboxes[label].grid(row=1, column=1)
        label_frame.grid(row=row, column=column, sticky=tk.N + tk.S + tk.E + tk.W)

    def create_entry_show(self, frame, label, row, column, textvar):
        label_frame = tk.LabelFrame(frame, text=label)
        self.entries[label] = tk.Entry(label_frame, width=25, textvariable=textvar, show="*")
        self.entries[label].grid(row=1, column=1)
        label_frame.grid(row=row, column=column, sticky=tk.N + tk.S + tk.E + tk.W)


class DiseasePrediction(Signup):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.diseaseName = None

    def create_view(self, diseaselist, patient_list):
        diseaselist = sorted(diseaselist)
        control_frame = tk.LabelFrame(master=self, text="Enter Symptoms", font='Verdana 15 bold')
        control_frame.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.create_label(control_frame, row=7, col=0, text="Symptom 1", justify='center', font="Elephant", fontsize=20,
                          padx=18, pady=25)
        self.create_label(control_frame, row=7, col=1, text="Symptom 2", justify='center', font="Elephant", fontsize=20,
                          padx=18, pady=25)
        self.create_label(control_frame, row=7, col=2, text="Symptom 3", justify='center', font="Elephant", fontsize=20,
                          padx=18, pady=25)
        self.create_label(control_frame, row=7, col=3, text="Symptom 4", justify='center', font="Elephant", fontsize=20,
                          padx=18, pady=25)
        self.create_label(control_frame, row=7, col=4, text="Symptom 5", justify='center', font="Elephant", fontsize=20,
                          padx=18, pady=25)

        self.create_combobox(
            control_frame, "S1En", row=8, column=0, values=diseaselist
        )
        self.create_combobox(
            control_frame, "S2En", row=8, column=1, values=diseaselist
        )
        self.create_combobox(
            control_frame, "S3En", row=8, column=2, values=diseaselist
        )
        self.create_combobox(
            control_frame, "S4En", row=8, column=3, values=diseaselist
        )
        self.create_combobox(
            control_frame, "S5En", row=8, column=4, values=diseaselist
        )

        self.create_label(control_frame, row=9, col=0, text="", justify='center', font="Elephant", fontsize=20, padx=25,
                          pady=0)

        self.create_label(control_frame, row=10, col=0, text="", justify='center', font="Elephant", fontsize=20,
                          padx=25, pady=30)

        # Button
        self.create_button(control_frame, name="Predict Disease", row=11, column=2, height=3, width=20)

        self.create_button(control_frame, name="Clear", row=11, column=4, height=2, width=15)

        # control_frame_2
        control_frame_2 = tk.LabelFrame(master=self, text="Disease Predicted", font='Verdana 15 bold')
        control_frame_2.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.diseaseName = self.create_label(control_frame_2, row=0, col=0, justify='left', text="___Disease Name___",
                                             font="Elephant", fontsize=20, padx=0, pady=10)

        # control_frame_3
        control_frame_3 = tk.LabelFrame(master=self, text="Patient Details", font='Verdana 15 bold')
        control_frame_3.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # self.create_label(control_frame_3, row=0, col=0, justify='left', text="___Details___",
        #                   font="Elephant", fontsize=10, padx=0, pady=5)

        self.create_entry(
            control_frame_3, "Name: ", row=0, column=0, textvar=tk.StringVar()
        )
        self.create_entry(
            control_frame_3, "Age: ", row=0, column=1, textvar=tk.IntVar(value=0)
        )
        super().create_combobox(
            control_frame_3, "Gender: ", row=0, column=2, values=["Male", "Female"]
        )
        super().create_combobox(
            control_frame_3, "Already Entered Patients: ", row=0, column=3, values=patient_list
        )
        self.create_label(control_frame_3, row=0, col=4, justify='left', text="                                                                                    ",
                          font="Elephant", fontsize=10, padx=0, pady=5)
        self.create_button(control_frame_3, name="Switch to Menu", row=0, column=5, height=2, width=15)

    def create_combobox(self, frame, label, values, row, column):
        self.comboboxes[label] = ttk.Combobox(frame, values=values)
        self.comboboxes[label]['state'] = 'readonly'
        self.comboboxes[label].set('None')
        self.comboboxes[label].grid(row=row, column=column, sticky=tk.N + tk.S + tk.E + tk.W)

    def create_label(self, frame, row, col, justify, text, font, fontsize, padx, pady):
        label = tk.Label(frame, justify=justify, text=text)
        label.config(font=(font, fontsize))
        label.grid(row=row, column=col, padx=padx, pady=pady, sticky=tk.N + tk.S + tk.E + tk.W)
        return label


class Menu(DiseasePrediction):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.user_name = None
        self.my_lab = None #time
        self.my_lab1 = None #date

    def create_view(self, user_name):
        self.user_name = user_name
        control_frame = tk.LabelFrame(master=self, text="", font='Verdana 15 bold')
        control_frame.rowconfigure(0, weight=1)
        control_frame.columnconfigure(0, weight=1)
        control_frame.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        control_frame_3 = tk.LabelFrame(control_frame, text="Welcome", font='Verdana 15 bold')
        control_frame_3.rowconfigure(0, weight=2)
        control_frame_3.columnconfigure(0, weight=2)
        control_frame_3.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.create_label(control_frame_3, row=0, col=0, justify='left', text=self.user_name,
                          font="Elephant", fontsize=20, padx=0, pady=5)

        self.create_label(control_frame, row=1, col=0, justify='left', text="              ",
                          font="Elephant", fontsize=20, padx=0, pady=5)
        self.create_label(control_frame, row=0, col=2, justify='left', text="              ",
                          font="Elephant", fontsize=20, padx=0, pady=5)
        self.create_button(control_frame, name="Switch to Login", row=0, column=3, height=2, width=15)

        self.create_button(control_frame, name="Disease Prediction", row=2, column=1, height=3, width=20)
        self.create_button(control_frame, name="List of Disease Predicted", row=3, column=1, height=3, width=20)

        control_frame_2 = tk.LabelFrame(control_frame, text="", font='Verdana 15 bold')
        control_frame_2.rowconfigure(0, weight=1)
        control_frame_2.columnconfigure(0, weight=1)
        control_frame_2.grid(row=5, column=3, sticky=tk.N + tk.S + tk.E + tk.W)

        # self.create_label(control_frame_2, row=0, col=0, justify='left', text="Date and Time",
        #                   font="Elephant", fontsize=10, padx=0, pady=5)
        self.my_lab = tk.Label(control_frame_2, text="", font=("sans-serif", 10), fg="red")
        self.my_lab1 = tk.Label(control_frame_2, text="", font=("Helvetica", 10), fg="blue")

        self.my_lab.grid(row=0, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.my_lab1.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)


class Table(DiseasePrediction):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    def create_view(self, data):
        frame = tk.Frame(self)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        total_rows = len(data)
        total_columns = len(data[0])
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.create_button(frame, name="Switch to Menu", row=total_rows + 1, column=total_columns - 1, height=2,
                           width=20)
        for row in range(total_rows):
            for col in range(total_columns):
                entry = tk.Entry(frame, width=20)

                entry.grid(row=row + 1, column=col, sticky=tk.N + tk.S + tk.E + tk.W)
                entry.rowconfigure(0, weight=1)
                entry.columnconfigure(0, weight=1)
                entry.insert(tk.END, data[row][col])
