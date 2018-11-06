from tkinter import *

import firebase_admin as fba
from firebase_admin import firestore
from firebase_admin import auth
import datetime
import pytz
import hashlib
__accountname__=''
#init database
cred = fba.credentials.Certificate('./serviceaccountkey.json')
mainapp = fba.initialize_app(cred)
db = firestore.client()
task = db.collection(u'Task')
users=db.collection(u'User')
groups=db.collection(u'Group')

def md5(str):
	#used for password varification
	hmd5 = hashlib.md5()
	hmd5.update(str.encode(encoding='utf-8'))
	return hmd5.hexdigest()

def user_login(email,pwd):
    #user login system, return a referance of one user if success
    #global var account name will be reset to this user id
    if len(list(users.where(u'User_email','==',email).get()))==0:
        print('Failed: Email incorrect')
        return None
    user=list(users.where(u'User_email', '==', email).get())[0]
    if user.to_dict()['User_pwd']!= md5(pwd):
        print('Failed: Password incorrect')
        return None
    global __accountname__
    __accountname__=user.id
    user=users.document(__accountname__)
    user.update({'Is_login':True,'Last_login':datetime.datetime.utcnow()})
    return user

def user_add(email,username, pwd):
	#add a new user to database system, passward encrypted.
	#will reject creation if username already exict(return a string to indicate that)
    if len(list(users.where(u'User_email','==',email).get()))>=1:
        print("Email already exists")
        return None
    user_dict={u'User_email':email,u'User_pwd':md5(pwd),u'User_name':username,u'Last_login':None,u'Is_login':False}
    return users.add(user_dict)[1]

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





c1 = Button(gui, background="#6666ee", text="LOGIN", command=lambda: user_login(email.get(),pwd.get())).grid(row=6, column=1)
g = Button(gui,background="#6666ee", text="Create Account", command = lambda: user_add(email.get(),usr.get(),pwd.get())).grid(row=6,column = 4)

gui.mainloop()