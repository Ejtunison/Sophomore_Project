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
a = Label(gui, text="username").grid(row=2, column=0)
b = Label(gui, text="password").grid(row=3, column=0)
i = Entry(gui, textvariable = email).grid(row=1,column=1)
e = Entry(gui, textvariable=usr).grid(row=2, column=1)
f = Entry(gui, show="*", textvariable=pwd).grid(row=3, column=1)
xx = Checkbutton(gui, text="remember me").grid(row=4, column=1)
x = 0
y = 0

def log(gui):
    if user_login(email.get(), pwd.get()) != False:
        gui = CallMainWindow(user_login(email.get(), pwd.get()))



c1 = Button(gui, background="#6666ee", text="LOGIN", command=lambda: log(gui)).grid(row=6, column=1)
g = Button(gui,background="#6666ee", text="Create Account", command = lambda: user_add(email.get(),pwd.get(),usr.get())).grid(row=6,column = 4)

gui.mainloop()