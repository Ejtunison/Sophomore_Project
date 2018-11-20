import DatabasePush
import PyQt5
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import ctypes
import MainTaskWindow
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		self.setFixedSize(450,280)
		self.setWindowIcon(QtGui.QIcon('./resource/task.png'))
		global ui,save_info
		ui = uic.loadUi('Login.ui',self)
		self.info_load()
		ui.Login.clicked.connect(self.login)
		ui.CreateAccount.clicked.connect(self.create_account)
		ui.Email.returnPressed.connect(self.change_cursor)
		ui.Passward.returnPressed.connect(self.login)
		ui.CreateAccountButton.clicked.connect(self.create_account_pressed)
	def info_load(self):
		try:
			with open('loginfo','r+') as f:
				global save_info
				save_info=f.readlines()
		except IOError:
			return
		for i in range(0, len(save_info)):
			save_info[i] = save_info[i].rstrip('\n')
		if save_info[0] == '2':
			ui.checkBox.setCheckState(2)
			ui.Email.setText(save_info[1])
			ui.Passward.setText(save_info[2])
	def login(self):
		mail=ui.Email.text()
		pwd=ui.Passward.text()
		if mail == '' or pwd == '':
			self.msgBox(QMessageBox.Warning,'Warning:','Email or Passward is Empty!')
			return
		try:
			user = DatabasePush.user_login(mail,pwd)
		except:
			self.msgBox(QMessageBox.Warning,'Warning:','Email or Passward Incorrect!')
			return
		save_info=[]
		save_info.append(str(ui.checkBox.checkState())+'\n')
		save_info.append(mail+'\n')
		if len(pwd) == 32:
			save_info.append(pwd+'\n')
		else:
			save_info.append(DatabasePush.md5(pwd)+'\n')
		with open('loginfo','w+') as f:
			f.writelines(save_info)
		self.close()
		self.main=MainTaskWindow.MainWindow(user.id)
		self.main.show()	
	def create_account(self):
		self.setFixedSize(450,615)
	def change_cursor(self):
		ui.Passward.setFocus()
	def msgBox(self,icon,title,message):
		msg=QMessageBox()
		msg.setIcon(icon)
		msg.setText(message)
		msg.setWindowTitle(title)
		retval=msg.exec_()
	def create_account_pressed(self):
		mail = ui.Email_2.text()
		nickname = ui.NickName.text()
		pwd1 = ui.Passward_2.text()
		pwd2 = ui.Passward_3.text()
		if mail == '' or nickname == '' or pwd1 == '' or pwd2 == '':
			self.msgBox(QMessageBox.Warning,'Warning:','Incomplete Information: Field Still Empty!')
		elif pwd1 != pwd2:
			self.msgBox(QMessageBox.Warning,'Warning:','Error: Password inconsistency, comfirm the password again')
		else:
			try:
				DatabasePush.user_add(mail,pwd1,nickname)
			except:
				self.msgBox(QMessageBox.Warning,'Warning:','Error: Email Already Exists, Please Login')
			else:
				self.msgBox(QMessageBox.Information,'Congratulation:','Account Creates Successful, Please Login')
def main():
	import sys
	app = QtWidgets.QApplication(sys.argv)
	mWindow = MainWindow()
	mWindow.show()
	sys.exit(app.exec_())
main()