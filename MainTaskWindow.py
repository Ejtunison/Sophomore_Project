import DatabasePush
import PyQt5
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import ctypes
import atexit
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
user_id=''
user_dict=None
_group={}
current_group_id=None
_CurrentTasks=[]
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(MainWindow,self).__init__()
		global user_id,ui
		user_id = uid
		ui = uic.loadUi('MainWindow.ui',self)	
		self.layout_init()
		self.enableArea_set('profile')
		self.listener_set()
		self.profile_load()
		self.load_group()
		ui.dateEdit.setDate(datetime.datetime.now().date())		
		self.time_manange()
		ui.GroupView.setCurrentRow(0)
		self.get_group_load_task()
	def layout_init(self):
		self.setFixedSize(730,651)
		self.setWindowIcon(QtGui.QIcon('./resource/task.png'))
		ui.GroupBox.move(290,6)
		ui.ProfileBox.move(290,6)
		#self.setIconSize(QtCore.QSize(48,48))
	def enableArea_set(self,tag):
		if tag == 'profile':
			ui.ProfileBox.setVisible(True)
			ui.GroupBox.setVisible(False)
			ui.TaskArea.setVisible(False)
		elif tag == 'group':
			ui.ProfileBox.setVisible(False)
			ui.GroupBox.setVisible(True)
			ui.TaskArea.setVisible(False)
		elif tag == 'task':
			ui.ProfileBox.setVisible(False)
			ui.GroupBox.setVisible(False)
			ui.TaskArea.setVisible(True)
	def profile_load(self):
		global user_dict
		DatabasePush.__accountname__=user_id
		user_dict=DatabasePush.user_get_dict(user_id)
		ui.AccName.setText("Name:  "+user_dict['User_name'])
		ui.AccEmail.setText("Email:  "+user_dict['User_email'])
	def listener_set(self):
		ui.importanceSlider.valueChanged.connect(self.importance_change)
		ui.StatusSlider.valueChanged.connect(self.status_change)
		ui.dateEdit.dateChanged.connect(self.time_manange)
		ui.timeEdit.timeChanged.connect(self.time_manange)
		ui.dateEdit.dateChanged.connect(self.time_manange)
		ui.timeEdit.timeChanged.connect(self.time_manange)
		ui.CommitButton.clicked.connect(self.commit_task_change)
		ui.GroupView.itemDoubleClicked.connect(self.get_group_load_task)
		ui.TaskView.itemDoubleClicked.connect(self.get_task)
		ui.GrpMemAddButton.clicked.connect(self.group_add_member)
		ui.AddMemText.returnPressed.connect(self.group_add_member)
		ui.GrpMemDelButton.clicked.connect(self.group_del_member)
		ui.GrpCommitButton.clicked.connect(self.commit_group_change)
	def load_group(self):
		global _group
		_group={}
		ui.GroupView.clear()
		temp_Qwi = QtWidgets.QListWidgetItem('Personal',ui.GroupView)
		temp_Qwi.setData(16,user_id)
		temp_Qwi.setIcon(QtGui.QIcon('./resource/personalblue.png'))
		for i in DatabasePush.groups.get():
			if user_id in i.to_dict()['Participants']:
				_group[i.id]=i.to_dict()
				if(_group[i.id]['Leader']==user_id):
					temp_Qwi = QtWidgets.QListWidgetItem(_group[i.id]['Name']+" (Leader)",ui.GroupView)
					temp_Qwi.setData(16,i.id)
					temp_Qwi.setData(17,i.to_dict())
					temp_Qwi.setIcon(QtGui.QIcon('./resource/adminred.png'))
				else:
					temp_Qwi = QtWidgets.QListWidgetItem(_group[i.id]['Name'],ui.GroupView)
					temp_Qwi.setData(16,i.id)
					temp_Qwi.setData(17,i.to_dict())
					temp_Qwi.setIcon(QtGui.QIcon('./resource/membergreen.png'))
		temp_Qwi = QtWidgets.QListWidgetItem('Add New Group',ui.GroupView)
		temp_Qwi.setIcon(QtGui.QIcon('./resource/add.jpg'))
		temp_Qwi.setData(16,"AddGroup")	
	def get_group_load_task(self):
		global current_group_id
		current_group_id = ui.GroupView.currentItem().data(16)
		ui.TaskView.clear()
		for i in DatabasePush.task.where(u'group','==',current_group_id).get():
			self.task_list_add_deal(ui.TaskView,i.id,i.to_dict())
		if  current_group_id != 'AddGroup':
			temp_Qwi = QtWidgets.QListWidgetItem("Add New Task",ui.TaskView)
			temp_Qwi.setIcon(QtGui.QIcon('./resource/add.jpg'))
			temp_Qwi.setData(16,"AddTask")
		if current_group_id=='AddGroup':
			self.group_show_clear()
			self.enableArea_set('group')
		elif current_group_id==user_id:
			self.enableArea_set('profile')
		else:
			self.group_show_update(ui.GroupView.currentItem().data(17))
			self.enableArea_set('group')
		#self.load_group()
	def get_task(self):
		self.enableArea_set('task')
		if ui.TaskView.currentItem().data(16)=="AddTask":
			self.task_show_clear()
		else:
			self.task_show_update(ui.TaskView.currentItem().data(17))
	def importance_change(self):
		imp=["Loose","Normal","Important","Urgent"]
		ui.importanceLabel.setText(imp[ui.importanceSlider.value()])
		c=["color: green","color: black","color: orange","color: red"]
		ui.importanceLabel.setStyleSheet(c[ui.importanceSlider.value()]+';font: 20pt "MV Boli";')
		return ui.importanceSlider.value()
	def status_change(self):
		sta=["Waiting","InProgress","Completed"]
		ui.StatusLabel.setText(sta[ui.StatusSlider.value()])
		c=["color: black","color: red","color: green"]
		ui.StatusLabel.setStyleSheet(c[ui.StatusSlider.value()]+';font: 20pt "MV Boli";')
		return ui.StatusSlider.value()
	def time_manange(self):
		ui.dateEdit.setTime(ui.timeEdit.time())
		return ui.dateEdit.dateTime()
	def commit_task_change(self):
		if ui.TaskName.text() == '':
			self.msgBox(QMessageBox.Warning,'Warning:','Content Incompleted!')
			return
		curr_item=ui.TaskView.currentItem()
		if (curr_item.data(16)=="AddTask"):
			duetime=ui.dateEdit.dateTime().toUTC()
			DatabasePush.task_add(Task_name=ui.TaskName.text(),Task_discr=ui.TaskDes.toPlainText(),\
				Task_leader=user_id,groupid=current_group_id,Task_prior=ui.importanceSlider.value(),\
				progress=ui.StatusSlider.value(),Time_due=duetime.toPyDateTime())
		else:
			duetime=ui.dateEdit.dateTime().toUTC()
			fdict={'Task_name':ui.TaskName.text(),'Task_discr':ui.TaskDes.toPlainText(),\
				'Task_prior':ui.importanceSlider.value(),'progress':ui.StatusSlider.value(),\
				'Time_due':duetime.toPyDateTime()}
			if fdict['progress']==2:
				fdict['Time_accom']=datetime.datetime.utcnow()
			DatabasePush.task_update_alter(curr_item.data(16),fdict)		
		self.get_group_load_task()
		#ui.TaskView.setCurrentItem(curr_item)
	def task_show_update(self,content):
		ui.TaskName.setText(content['Task_name'])
		ui.TaskDes.setPlainText(content['Task_discr'])
		ui.importanceSlider.setValue(content['Task_prior'])
		ui.StatusSlider.setValue(content['progress'])
		ui.dateEdit.setDateTime(self.time_change(content['Time_due']))
		ui.timeEdit.setDateTime(self.time_change(content['Time_due']))
		ui.EsTimeLabel.setText("Establish Time:  " + self.time_change(content['Time_Es']).toString("yyyy/MM/dd hh:mm (ddd)"))
		if content['progress']==2:
			ui.ComTimeLabel.setText("Complete Time:  " + self.time_change(content['Time_accom']).toString("yyyy/MM/dd hh:mm (ddd)"))
		else:
			ui.ComTimeLabel.setText("Complete Time:  This task hasnot completed yet!")
	def task_show_clear(self):
		ui.TaskName.setText("")
		ui.TaskDes.setPlainText("")
		ui.importanceSlider.setValue(1)
		ui.StatusSlider.setValue(0)
		#ui.dateEdit.setDateTime(self.time_change(content['Time_due']))
		#ui.timeEdit.setDateTime(self.time_change(content['Time_due']))
		ui.EsTimeLabel.setText("Establish Time: Will be generated Automatically")
		ui.ComTimeLabel.setText("Complete Time: Will be generated Automatically")
	def time_change(self,time):
		duetime = QtCore.QDateTime(time)
		duetime.setTimeSpec(1)
		duetime = duetime.toLocalTime()
		return duetime
	def group_show_clear(self):
		ui.groupNameText.setText("")
		ui.groupMsgText.setPlainText("")
		ui.groupLeader.setText('Leader:  '+user_dict['User_name']+' (' + user_dict['User_email'] + ')')
		self.set_group_edit(True)
		ui.GrpStatusLabel.setText("New Pending Group!")
		ui.AddMemText.setText("")
		ui.GroupMemView.clear()
		self.group_list_add_deal(ui.GroupMemView,user_id,user_dict)
	def group_show_update(self,content):
		user = DatabasePush.user_get_dict(content['Leader'])
		ui.groupLeader.setText('Leader:  '+user['User_name']+' (' + user['User_email'] + ')')
		ui.groupNameText.setText(content['Name'])
		ui.groupMsgText.setPlainText(content['Message'])
		if content['Leader'] == user_id:
			self.set_group_edit(True)
			ui.GrpStatusLabel.setText("")
		else:
			self.set_group_edit(False)
			ui.GrpStatusLabel.setText("No Privilege: Not Leader")
		ui.GroupMemView.clear()
		for i in content['Participants']:
			user = DatabasePush.user_get_dict(i)
			self.group_list_add_deal(ui.GroupMemView,i,user)
	def set_group_edit(self,boool):
		objs=[ui.groupNameText,ui.groupMsgText,ui.AddMemText,ui.GrpMemAddButton,ui.GrpMemDelButton,\
			ui.GrpCommitButton]
		for i in objs:
			i.setEnabled(boool)
	def group_add_member(self):
		puser=DatabasePush.user_get(ui.AddMemText.text())
		ui.AddMemText.setText("")
		if puser is None:
			ui.GrpStatusLabel.setText("Invalid user!")
			self.msgBox(QMessageBox.Warning,'Warning:','Invalid user! (You could either type the email or the nickname).')
		else:
			for i in range(ui.GroupMemView.count()):
				if puser.id == ui.GroupMemView.item(i).data(16):
					ui.GrpStatusLabel.setText("User already in group!")
					self.msgBox(QMessageBox.Warning,'Warning:','This user is already in the group!')
					return
			user=puser.get().to_dict()
			self.group_list_add_deal(ui.GroupMemView,puser.id,user)
			ui.GrpStatusLabel.setText("Add successful!")
	def group_del_member(self):
		if ui.GroupMemView.currentItem() is None:
			ui.GrpStatusLabel.setText("No user selected!")
		elif ui.GroupMemView.currentItem().data(16)==user_id:			
			ui.GrpStatusLabel.setText("Cannot del yourself!")
			self.msgBox(QMessageBox.Warning,'Warning:','Cannot delete yourself my leader!')
		else:
			ui.GroupMemView.takeItem(ui.GroupMemView.row(ui.GroupMemView.currentItem()))
			ui.GrpStatusLabel.setText("Delete successful!")
	def commit_group_change(self):
		if ui.groupNameText.text() == '':
			self.msgBox(QMessageBox.Warning,'Warning:','Content Incompleted!')
			return
		parti=[]
		for i in range(ui.GroupMemView.count()):
			parti.append(ui.GroupMemView.item(i).data(16))
		if current_group_id=='AddGroup':
			DatabasePush.group_add(name=ui.groupNameText.text(),message=ui.groupMsgText.toPlainText(),\
				leader=user_id,party=parti)
		else:
			DatabasePush.group_update_alter(current_group_id,name=ui.groupNameText.text(),message=ui.groupMsgText.toPlainText(),\
				leader=user_id,party=parti)
		self.load_group()
	def group_list_add_deal(self,grplist,uid,data):
		temp_Qwi = QtWidgets.QListWidgetItem(data['User_name']+' (' + data['User_email'] + ')',grplist)
		temp_Qwi.setData(16,uid)
		temp_Qwi.setData(17,data)
		if data['Is_login']:
			temp_Qwi.setIcon(QtGui.QIcon('./resource/greendot.png'))
		else:
			temp_Qwi.setIcon(QtGui.QIcon('./resource/graydot.png'))
	def task_list_add_deal(self,tsklist,tid,data):
		temp_Qwi = QtWidgets.QListWidgetItem(data['Task_name'],tsklist)
		temp_Qwi.setData(16,tid)
		temp_Qwi.setData(17,data)
		pgs_icon=[QtGui.QIcon('./resource/waiting.jpg'),QtGui.QIcon('./resource/inprogress.jpg'),QtGui.QIcon('./resource/complete.jpg')]
		temp_Qwi.setIcon(pgs_icon[data['progress']])
		imp_color=[QtGui.QColor(0,255,0,60),QtGui.QColor(0,0,0,20),QtGui.QColor(255,192,42,60),QtGui.QColor(255,0,0,60)]
		temp_Qwi.setBackground(QtGui.QBrush(imp_color[data['Task_prior']]))
	def msgBox(self,icon,title,message):
		msg=QMessageBox()
		msg.setIcon(icon)
		msg.setText(message)
		msg.setWindowTitle(title)
		retval=msg.exec_()
def close_logout():
	DatabasePush.user_logout()
def main(uid):
	import sys
	global user_id
	user_id=uid
	app = QtWidgets.QApplication(sys.argv)
	mWindow = MainWindow(uid)
	mWindow.show()
	sys.exit(app.exec_())
atexit.register(close_logout)

if __name__ == '__main__':
	DatabasePush.user_login('renzhili1@gmail.com','123456')
	main('IkXH5TmJQRJi4dRAbuNL')
