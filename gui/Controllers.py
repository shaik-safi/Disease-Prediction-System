from gui.Views import Login, Signup, DiseasePrediction, Menu, Table
from gui.Models import logindb, signupdb, Model, current_info, fetchinfo, current_patients, patient_selected, fetchlist
from gui.lists import l1, disease


import numpy as np
import time
from abc import ABC, abstractmethod
import tkinter as tk
import tkinter.messagebox as tkmsg
from functools import partial


def msgbox(isError, title, msg, frame):
    if isError:
        tkmsg.showerror(title, msg, parent=frame)
    else:
        tkmsg.showinfo(title, msg, parent=frame)


class Controller(ABC):
    @abstractmethod
    def bind(View):
        raise NotImplementedError


# login controller
class LoginController(Controller):
    def __init__(self):
        self.view = None
        self.root = None
        # self.entries_values = {}

    def bind(self, view, root):
        self.view = view
        self.root = root
        self.view.create_view()

        self.view.buttons["Login"].configure(command=partial(self.login, frame=self.view, entries=self.view.entries))
        self.view.buttons["Clear"].configure(command=self.clear)
        self.view.buttons["Switch To Sign up"].configure(command=self.signup)

    def login(self, frame, entries):
        print("View:login")
        if entries["User Name :"].get() == "" or entries["Password :"].get() == "":
            msgbox(True, "Error", "Enter User Name And Password", frame)
        else:
            try:
                [isSuccess, title, msg] = logindb(entries=entries)
                msgbox(not isSuccess, title=title, msg=msg, frame=frame)
                if isSuccess:
                    self.close()
                    self.menuwin()
            except Exception as es:
                msgbox(isError=True, title="Error", msg=f"Error Due to : {str(es)}", frame=frame)

    def menuwin(self):
        print("View:Switch To Menu")
        menuFrame = tk.Tk()
        menuFrame.configure()
        menuFrame.title('Disease Prediction')
        menuCon = MenuController()
        menuwin = Menu(menuFrame)
        menuCon.bind(view=menuwin, root=menuFrame)

    def close(self):
        self.clear()
        self.root.destroy()

    def clear(self):
        print("View:clear")
        for x in self.view.entries:
            self.view.entries[x].delete(0, 'end')

    def signup(self):
        print("View:Switch To Sign up")
        self.close()

        sc = SignupController()
        signupWin = tk.Tk()
        signupWin.title('Disease Prediction')
        signform = Signup(signupWin)
        sc.bind(view=signform, root=signupWin)


# signup controller
class SignupController(LoginController):
    def __init__(self):
        self.view = None
        self.root = None

    def bind(self, view, root):
        self.view = view
        self.root = root
        self.view.create_view()

        self.view.buttons["Signup"].configure(command=partial(self.action, frame=self.view, entries=self.view.entries,
                                                              gender=self.view.comboboxes["Gender :"]))
        self.view.buttons["Clear"].configure(command=partial(self.clear, iscombobox=True))
        self.view.buttons["Switch To Login"].configure(command=self.switch)

    def action(self, frame, entries, gender):
        if entries["First Name :"].get() == "" or entries["Last Name :"].get() == "" or entries["Age :"].get() == "0" or \
                entries["City :"].get() == "" or entries["Address :"].get() == "" or entries[
            "User Name :"].get() == "" or \
                entries["Password :"].get() == "" or entries["Verify Password :"].get() == "" or gender == "None" or \
                entries["Phone Number :"].get() == "":
            msgbox(True, "Error", "All Fields Are Required", frame)

        elif len(entries["Phone Number :"].get()) != 10:
            msgbox(True, "Error", "Enter Proper Phone Number", frame)

        elif entries["Password :"].get() != entries["Verify Password :"].get():
            msgbox(True, "Error", "Password & Confirm Password Should Be Same", frame)

        else:
            try:
                [isSuccess, title, msg] = signupdb(entries=entries, gender_value=gender)
                msgbox(not isSuccess, title=title, msg=msg, frame=frame)
                if isSuccess:
                    self.clear(iscombobox=True)
                    self.switch()
            except Exception as es:
                msgbox(True, "Error", f"Error Due to : {str(es)}", frame)

    def clear(self, iscombobox):
        super().clear()
        if iscombobox:
            for x in self.view.comboboxes:
                self.view.comboboxes[x].set('None')

    def switch(self):
        self.root.destroy()
        self.loginwin()

    def loginwin(self):
        login_controller = LoginController()
        root = tk.Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.title('Disease Prediction')
        logform = Login(root)
        login_controller.bind(view=logform, root=root)


class MenuController(SignupController):
    def __init__(self):
        self.view = None
        self.root = None
        self.isClockOn = True

    def bind(self, view, root):
        self.view = view
        self.root = root

        self.view.create_view(user_name=self.user_info())
        self.clock(view=self.view)

        self.view.buttons["Disease Prediction"].configure(command=self.dpwin)
        self.view.buttons["List of Disease Predicted"].configure(command=self.listdp)
        self.view.buttons["Switch to Login"].configure(command=partial(self.exit, gotologinwin=True))

    def user_info(self):
        (fname, lname) = fetchinfo()
        full_name = fname + " " + lname
        return full_name

    def dpwin(self):
        self.exit(gotologinwin=False)
        pc = PredictController(Model())
        dpWin = tk.Tk()
        dpWin.title('Disease Prediction')
        form = DiseasePrediction(dpWin)
        self.root.after(800, pc.bind(view=form, root=dpWin))

    def exit(self, gotologinwin):
        self.isClockOn = False
        self.root.after(800, self.root.destroy)

        if gotologinwin:
            self.root.after(800, self.loginwin())

    def listdp(self):
        self.exit(gotologinwin=False)

        tableCon = TableController()
        TableFrame = tk.Tk()
        TableFrame.columnconfigure(0, weight=1)
        TableFrame.rowconfigure(0, weight=1)
        TableFrame.title('Disease Prediction')
        tableform = Table(master=TableFrame)
        self.root.after(800, tableCon.bind(view=tableform, root=TableFrame))

    def clock(self, view):
        hh = time.strftime("%I")
        mm = time.strftime("%M")
        ss = time.strftime("%S")
        ap = time.strftime("%p")
        year = time.strftime("%Y")
        month = time.strftime("%m")
        day = time.strftime("%d")
        view.my_lab.config(text=hh + ":" + mm + ":" + ss + " " + ap)
        if self.isClockOn:
            view.my_lab.after(1000, self.clock, view)
        view.my_lab1.config(text=day + "-" + month + "-" + year)


# predict controller
class PredictController(MenuController):
    def __init__(self, model):
        self.model = model
        self.view = None
        self.root = None
        self.predicted_disease = ""
        self.l2 = None

    def bind(self, view, root):
        self.view = view
        self.root = root
        self.l2 = current_patients()
        self.view.create_view(diseaselist=l1, patient_list=self.l2)
        self.view.buttons["Predict Disease"].configure(
            command=partial(self.predict, frame=self.view, symptoms=self.view.comboboxes,
                            paitentdetails=self.view.entries))
        self.view.buttons["Clear"].configure(command=self.clear)  ###
        self.view.buttons["Switch to Menu"].configure(command=self.exit)
        print(self.view.comboboxes["Already Entered Patients: "])
        self.view.comboboxes["Already Entered Patients: "].bind('<<ComboboxSelected>>', self.patient_changed)

    def predict(self, frame, symptoms, paitentdetails):
        if symptoms["Gender: "].get() == "None" or paitentdetails["Name: "].get() == "" or paitentdetails["Age: "].get() == "0":
            msgbox(True, "Error", "ENTER  PATIENT DETAILS PLEASE", frame)
        elif symptoms["S1En"].get() == "None" and symptoms["S2En"].get() == "None" and symptoms[
            "S3En"].get() == "None" and \
                symptoms["S4En"].get() == "None" and symptoms["S5En"].get() == "None":
            msgbox(True, "Error", "ENTER  SYMPTOMS PLEASE", frame)
        else:
            # NaiveBayes
            self.model.split()
            self.model.fit()

            user_input = self.inputtest(symptoms=self.view.comboboxes)
            self.model.accuracy()
            self.predicted_disease = self.model.predict(inputtest=user_input)
            print(disease[self.predicted_disease])
            h = 'no'
            for a in range(0, len(disease)):
                if disease[self.predicted_disease] == disease[a]:
                    h = 'yes'
                    break

            # print(disease[a])
            # print(a)
            if h == 'yes':
                self.view.diseaseName["text"] = disease[self.predicted_disease]
                try:
                    [isSuccess, title, msg] = current_info.store_db(symptoms, paitentdetails,
                                                                    disease_name=self.view.diseaseName["text"])
                    msgbox(not isSuccess, title=title, msg=msg, frame=frame)
                except Exception as es:
                    msgbox(True, "Error", f"Error Due to : {str(es)}", frame)
            else:
                self.view.diseaseName["text"] = "No Disease"
                # t3.delete("1.0", END)
                # t3.insert(END, "No Disease")

    def patient_changed(self, event):
        self.view.comboboxes["Gender: "].set("None")
        self.view.entries["Name: "].delete(0, 'end')
        self.view.entries["Age: "].delete(0, 'end')
        p_name = self.view.comboboxes["Already Entered Patients: "].get()
        print(p_name)
        (full_name, age, gender) = patient_selected(patient_name=p_name)
        self.view.comboboxes["Gender: "].set(gender)
        self.view.entries["Name: "].insert(0, full_name)
        self.view.entries["Age: "].insert(0, age)

    def exit(self):
        super().exit(gotologinwin=False)
        self.root.after(800, self.menuwin())
        # self.menuwin()

    def clear(self):
        super().clear(iscombobox=True)
        self.view.diseaseName['text'] = "___Disease Name___"

    def inputtest(self, symptoms):
        l2 = []
        for x in range(0, len(l1)):  # [0,...,131]
            l2.append(0)

        psymptoms = [symptoms["S1En"].get(), symptoms["S2En"].get(), symptoms["S3En"].get(), symptoms["S4En"].get(),
                     symptoms["S5En"].get()]

        for k in range(0, len(l1)):
            for z in psymptoms:
                if (z == l1[k]):
                    l2[k] = 1

        return [l2]


class TableController(PredictController):
    def __init__(self):
        self.view = None
        self.root = None

    def bind(self, view, root):
        self.view = view
        self.root = root
        self.view.create_view(data=self.table())
        self.view.buttons["Switch to Menu"].configure(command=self.exit)

    def table(self):
        table_dp = np.array(fetchlist())
        label = np.array(
            ('   Full Name   ', '   Symptom 1   ', '   Symptom 2   ', '   Symptom 3   ', '   Symptom 4   ', 'Symptom '
                                                                                                            '5   ',
             '   Disease Predicted   '))
        if len(table_dp) == 0:
            row = 2
        else:
            row = len(table_dp[:, 0]) + 1
        col = len(label)
        final_table = np.empty(shape=(row, col), dtype='object')
        final_table[0, :] = label
        if len(table_dp) == 0:
            final_table[1:, :] = ('None', 'None', 'None', 'None', 'None', 'None', 'None')
        else:
            final_table[1:, :] = table_dp
        return final_table
