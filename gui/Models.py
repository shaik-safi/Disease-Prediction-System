from gui.lists import l1, replace
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

import pymysql
import pandas as pd
import numpy as np
import time as t


class Model:
    def __init__(self, training_datafile="gui/Training.csv", testing_datafile="gui/Testing.csv"):
        self.df = pd.read_csv(training_datafile)
        self.tr = pd.read_csv(testing_datafile)
        self.naive_bayes = MultinomialNB()
        self.X = None
        self.y = None
        self.X_test = None
        self.y_test = None
        self.model = None
        self.y_pred = None

    def split(self):
        # TRAINING DATA
        replace(self.df)
        self.X = self.df[l1]
        self.y = self.df[["prognosis"]]

        # TESTING DATA
        replace(self.tr)
        self.X_test = self.tr[l1]
        self.y_test = self.tr[["prognosis"]]

    def fit(self):
        # Creating Model
        self.model = self.naive_bayes.fit(self.X, np.ravel(self.y))

    def predict(self, inputtest):
        # Predict disease
        result = self.naive_bayes.predict(inputtest)
        return result[0]

    def accuracy(self):
        y_pred = self.naive_bayes.predict(self.X_test)
        print('Model Accuracy:', end=' ')
        print(accuracy_score(self.y_test, y_pred))

#
class CurrentUser:

    def __init__(self):
        self.current_user_id = None
        self.current_patient_id = None
        self.current_symptoms_disease_id = None
        self.current_patients = None

    def set_user_id(self, current_user_id):
        self.current_user_id = current_user_id

    def get_user_id(self):
        return self.current_user_id

    def store_db(self, symptoms, paitentdetails, disease_name):
        [date, time] = self.date_time()

        con = pymysql.connect(host="localhost", user="root", password="shaiksafi2001@gmail.com",
                              database="DiseasepredictionDB")
        cur = con.cursor()
        cur.execute("select * from patient_info where full_name=%s and id=%s",
                    (paitentdetails["Name: "].get(), self.current_user_id))
        row = cur.fetchone()
        print(row)
        if row is None:
            cur.execute(
                "insert into patient_info(full_name,age,gender,id,patient_date,patient_time) "
                "values(%s,%s,%s,%s,%s,%s)",
                (
                    paitentdetails["Name: "].get(),
                    paitentdetails["Age: "].get(),
                    symptoms["Gender: "].get(),
                    self.current_user_id,
                    date,
                    time
                ))
            con.commit()

            cur.execute("select id_2 from patient_info where patient_date=%s and patient_time=%s",
                        (date, time))
            (self.current_patient_id,) = cur.fetchone()

            cur.execute(
                "insert into sym_dis(id_2,symptom_1,symptom_2,symptom_3,symptom_4,symptom_5,disease,sym_date,sym_time)"
                "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    self.current_patient_id,
                    symptoms["S1En"].get(),
                    symptoms["S2En"].get(),
                    symptoms["S3En"].get(),
                    symptoms["S4En"].get(),
                    symptoms["S5En"].get(),
                    disease_name,
                    date,
                    time
                ))
            con.commit()

            cur.execute("(select id_3 from sym_dis where sym_date=%s and sym_time=%s)", (date, time))
            (self.current_symptoms_disease_id,) = cur.fetchone()
        else:
            isDone = True
            while isDone:
                try:
                    cur.execute(
                        "insert into sym_dis(id_2,symptom_1,symptom_2,symptom_3,symptom_4,symptom_5,disease,sym_date,"
                        "sym_time) "
                        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (
                            self.current_patient_id,
                            symptoms["S1En"].get(),
                            symptoms["S2En"].get(),
                            symptoms["S3En"].get(),
                            symptoms["S4En"].get(),
                            symptoms["S5En"].get(),
                            disease_name,
                            date,
                            time
                        ))
                    con.commit()
                    isDone = False
                except Exception as es:
                    self.current_patient_id = row[0]

            cur.execute("(select id_3 from sym_dis where sym_date=%s and sym_time=%s)", (date, time))
            (self.current_symptoms_disease_id,) = cur.fetchone()

        return [True, "Success", "Information Successful Stored"]

    def date_time(self):
        date = t.strftime("%Y-%m-%d")
        time = t.strftime("%H:%M:%S")
        return [date, time]


def patient_selected(patient_name):
    con = pymysql.connect(host="localhost", user="root", password="shaiksafi2001@gmail.com",
                          database="DiseasepredictionDB")
    cur = con.cursor()
    cur.execute("select full_name,age,gender from patient_info where id=%s and full_name=%s",
                (current_info.get_user_id(), patient_name))
    row = cur.fetchone()
    print(row)
    return row


def current_patients():
    con = pymysql.connect(host="localhost", user="root", password="shaiksafi2001@gmail.com",
                          database="DiseasepredictionDB")
    cur = con.cursor()
    cur.execute("select full_name from patient_info where id=%s", (current_info.get_user_id()))
    row = cur.fetchall()
    print(row)
    return row


def fetchinfo():
    con = pymysql.connect(host="localhost", user="root", password="shaiksafi2001@gmail.com",
                          database="DiseasepredictionDB")
    cur = con.cursor()

    cur.execute("select first_name,last_name from user_information where id = %s", current_info.get_user_id())
    row = cur.fetchone()

    print(row)
    con.close()
    return row


def fetchlist():
    con = pymysql.connect(host="localhost", user="root", password="shaiksafi2001@gmail.com",
                          database="DiseasepredictionDB")
    cur = con.cursor()
    cur.execute("select p.full_name, s.symptom_1, s.symptom_2, s.symptom_3, s.symptom_4, s.symptom_5, s.disease from "
                "patient_info p, sym_dis s where p.id_2 = s.id_2 and p.id = %s", current_info.get_user_id())
    row = cur.fetchall()

    print(row)
    con.close()
    return row


##
current_info = CurrentUser()


def logindb(entries):
    con = pymysql.connect(host="localhost", user="root", password="shaiksafi2001@gmail.com",
                          database="DiseasepredictionDB")
    cur = con.cursor()

    cur.execute("select * from user_information where username=%s and password = %s",
                (entries["User Name :"].get(), entries["Password :"].get()))
    row = cur.fetchone()

    if row is None:
        return [False, "Error", "Invalid User Name And Password"]

    else:
        current_info.set_user_id(current_user_id=row[0])  # ####

        con.close()
        return [True, "Success", "Successfully Login"]


# signup database connect
def signupdb(entries, gender_value):
    con = pymysql.connect(host="localhost", user="root", password="shaiksafi2001@gmail.com",
                          database="DiseasepredictionDB")
    cur = con.cursor()
    cur.execute("select * from user_information where username=%s", entries["User Name :"].get())
    row = cur.fetchone()
    if row is not None:
        return [False, "Error", "User Name Already Exits"]
    else:
        cur.execute(
            "insert into user_information(first_name,last_name,age,gender,phone_number,city,address,username,"
            "password) "
            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                entries["First Name :"].get(),
                entries["Last Name :"].get(),
                entries["Age :"].get(),
                gender_value.get(),
                entries["Phone Number :"].get(),
                entries["City :"].get(),
                entries["Address :"].get(),
                entries["User Name :"].get(),
                entries["Password :"].get()
            ))
        con.commit()
        con.close()
        return [True, "Success", "Registration Successful"]
