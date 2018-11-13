from NewTaskWindow import Call_Window
from FullScreen import *
from SelectGroup import *

def CallMainWindow(user):
    root = Tk()
    root.title("Task Your Life")
    root.geometry("200x200")

    usr = user

    newBoardButton = Button(root, text="New Task Board", bg="#4ef4f9",fg="black", font="Times 12 bold")
    newBoardButton.grid(row=4, column=4)
    addTaskButton = Button(root, text="Add New Task", bg="#70fd5a",fg="black", font="Times 12 bold", command=Call_Window)
    addTaskButton.grid(row=6, column=4)
    selectGroupButton = Button(root, command = lambda: algo(usr), text = "Select Group", bg = "#4ef4f9", fg = "black", font = "Times 12 bold").grid(row = 8, column = 4)



    gui = FullScreenApp(root)

    root.mainloop()

def algo(usr):
    selectGroup(usr)
