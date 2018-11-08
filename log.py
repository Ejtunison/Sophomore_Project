from DatabasePush import *
from MainWindow import *



gui = Tk()
username = 'jia'
password = '1234'
gui.geometry("400x400")
gui.title("LOG IN")
gui.iconbitmap(default = 'favicon.ico')
usr = StringVar()
pwd = StringVar()
email = StringVar()

# pre = Label(gui ,text="LOG IN", background="#6666ee").grid(row=0,column = 0)
h = Label(gui,text = "Email").grid(row=1,column=0)
b = Label(gui, text="password").grid(row=3, column=0)
i = Entry(gui, textvariable = email).grid(row=1,column=1)
f = Entry(gui, show="*", textvariable=pwd).grid(row=3, column=1)
x = 0
y = 0

def log():
    if user_login(email.get(), pwd.get()) != False:
        global gui
        gui.destroy()
        CallMainWindow(user_login(email.get(), pwd.get()))
    else:
        global gui
        a = Label(gui,Text = "Login Failed. Please Try Again").grid(row = 9, column = 0)



def add():
    add = Tk()
    h = Label(add, text="Email").grid(row=1, column=0)
    a = Label(add, text="username").grid(row=2, column=0)
    b = Label(add, text="password").grid(row=3, column=0)
    i = Entry(add, textvariable=email).grid(row=1, column=1)
    e = Entry(add, textvariable=usr).grid(row=2, column=1)
    f = Entry(add, show="*", textvariable=pwd).grid(row=3, column=1)
    button = Button(add, background = "#6666ee",text = "Create Account", command = lambda: algo(add)). grid(row = 4, column = 0)
    add.mainloop()

def algo(frame):
    if user_add(email,pwd,usr) != False:
        frame.destroy()
        global gui
        a = Label(gui,text="Account Created. Please Login").grid(row=9,column=0)
    else:
        frame.destroy()
        global gui
        a = Label(gui,text = "Account Already Exists. Please Login").grid(row = 9, column = 0)


c1 = Button(gui, background="#6666ee", text="Login", command=lambda: log()).grid(row=6, column=1)
g = Button(gui,background="#6666ee", text="Click Here to Create Account", command = lambda: add()).grid(row=8,column = 1)



gui.mainloop()