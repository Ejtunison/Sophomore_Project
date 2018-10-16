import firebase_admin as fba
from firebase_admin import firestore
#from google.cloud import firestore
cred=fba.credentials.Certificate('./serviceaccountkey.json')
mainapp=fba.initialize_app(cred)
db=firestore.client()

class Group:
	def __init__(self, name, goals):
		self.name = name
		self.goals = goals

class Task:
	def __init__(self, description, leader, progress, name, priority, createTime, dueTime, hasSub, subTasks, isGoal):
		self.description = description
		self.leader=leader
		self.progress = progress
		self.name = name
		self.priority = priority
		self.createTime = createTime
		self.dueTime = dueTime
		self.hasSub = hasSub
		self.subTasks = subTasks
		self.isGoal = isGoal

#when a top-layer goal is added, n will be passed with value 1, otherwise n is passed with value 0
def getTasks(doc, n):
    newTasks = [Task(None,None,None) for i in range(100)]
    j = 0
    for i in doc:
        description = i.to_dict()['Task_discr']
        leader = i.to_dict()['Task_leader']
        progress = i.to_dict()['progress']
	name = i.to_dict()['Task_name']
	priority = i.to_dict()['Task_prior']
	createTime = i.to_dict()['Time_Es']
	dueTime = i.to_dict()['Time_due']
	hasSub = i.to_dict()['Has_subtask']
	is hasSub == False:
		subTasks = None
	else:
		subTasks = getTasks(i.collection(u'Subtasks'))
	if n == 1:
		isGoal = True
	else:
		isGoal = False
        newTasks[j] = Task(description, leader, progress, name, priority, createTime, dueTime, hasSub, subTasks, isGoal)
        j+=1
    return newTasks


#Example of getting data for group named groupname
name="groupname"
ref = db.collection(u'Task').where(u'group', u'==', name).get()
task=getTasks(ref, 1)
group=Group(name,task)
print(group.goals[0].description)
