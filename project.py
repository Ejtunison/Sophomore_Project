class Group:
    def __init__(self, name,goals):
        self.name = name
        self.goals = goals

class Goal:
    def __init__(self, description, tasks):
        self.description = description
        self.tasks = tasks
class Task:
    def __init__(self, description, user, progress):
        self.description = description
        self.user = user
        self.progress = progress

import firebase_admin as fba
from firebase_admin import firestore
#from google.cloud import firestore
cred=fba.credentials.Certificate('./serviceaccountkey.json')
mainapp=fba.initialize_app(cred)
db=firestore.client()

task=db.collection(u'Group')
temp=task.document('Zjyxs1uG9oVN5ecmHUYh')
print(temp.get().to_dict()['name'])
for i in task.get():
	print(i.id)

gr1 = Group(temp.get().to_dict()['name'], "blah")
print("name: "+ gr1.name)

