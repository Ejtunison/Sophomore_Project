from tkinter import *
from DatabasePush import *


def selectGroup(user):
    root = Tk()
    if groups_get(user) == False:
        a = Label(root, text = "No groups found for this user. Please come back when you are in a group").grid(row = 0, column = 0)
        b = Button(root, text = "Return to Menu", command = root.destroy).grid(row = 2, column = 0)
    else:
        groups = groups_get(user)
        a = [Button(root, text=groups[i].get().to_dict()['Name'], command = lambda: select(groups[i])) for i in range(len(groups))]
        root.mainloop()
        return activeGroup

def select(group):
    global activeGroup
    activeGroup = group
    global root
    root.destroy()
