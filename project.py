class Group:
	def __init__(self, name,goals):
		self.name = name
		self.goals = goals

class Task:
	def __init__(self, description, leader, progress):
		self.description = description
		self.leader=leader
		self.progress = progress

import firebase_admin as fba
from firebase_admin import firestore
#from google.cloud import firestore
cred=fba.credentials.Certificate('./serviceaccountkey.json')
mainapp=fba.initialize_app(cred)
db=firestore.client()

def getTasks(name):
    newTasks = [Task(None,None,None) for i in range(100)]
    ref=db.collection(u'Task').where(u'group', u'==', name).get()
    j = 0
    for i in ref:
        description = i.to_dict()['Task_discr']
        leader = i.to_dict()['Task_leader']
        progress = i.to_dict()['progress']
        newTasks[j] = Task(description, leader, progress)
        j+=1
    return newTasks


#Example of getting data for group named groupname
name="groupname"
task=getTasks(name)
group=Group(name,task)
print(group.goals[0].description)
