import tkinter as tk
from gui.Controllers import LoginController
from gui.Views import Login

if __name__ == "__main__":

    def loginroot():
        login_controller = LoginController()
        root = tk.Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.title('Disease Prediction')

        logform = Login(root)

        login_controller.bind(view=logform, root=root)

        root.mainloop()

    loginroot()


