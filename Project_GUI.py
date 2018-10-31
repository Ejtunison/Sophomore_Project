from tkinter import *
from New_Task_Window import Call_Window

root = Tk()
root.title("Task Your Life")
root.geometry("200x200")

newBoardButton = Button(root, text="New Task Board", bg="#4ef4f9",fg="black", font="Times 12 bold")
newBoardButton.grid(row=4, column=4)
addTaskButton = Button(root, text="Add New Task", bg="#70fd5a",fg="black", font="Times 12 bold", command=Call_Window)
addTaskButton.grid(row=6, column=4)

root.mainloop()
