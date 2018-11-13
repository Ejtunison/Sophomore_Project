from tkinter import *
from New_Task_Window import Call_Window

root = Tk()
root.title("Task Your Life")
root.geometry("600x600")

#Frames
topFrame = Frame(root, bg="#cfd4d3")
topFrame.pack(anchor=N, fill=X, expand=TRUE)
topFrame.grid_columnconfigure(0, weight=1)
topFrame.grid_rowconfigure(0, weight=1)

bottomFrame = Frame(root, bg="white")
bottomFrame.pack(fill=BOTH, expand=TRUE)
bottomFrame.pack_propagate(FALSE)
bottomFrame.grid_columnconfigure(0, weight=1)
bottomFrame.grid_rowconfigure(0, weight=1)

boardButtonFrame = Frame(topFrame)
boardButtonFrame.grid(sticky=NW, padx=10, pady=10)

inProgressFrame = Frame(bottomFrame, bg="white", highlightbackground="#97f4df", highlightcolor="#97f4df",
                        highlightthickness=3, width=500, height=700, bd=0)
inProgressFrame.grid(row=1, column=0)
inProgressFrame.grid_propagate(FALSE)

#Buttons
newBoardButton = Button(boardButtonFrame, text="New Task Board", bg="#4ef4f9", fg="black", font="Courier 12 bold")
newBoardButton.grid(row=0, column=0)

logoutButton = Button(topFrame, text="Log out", bg="#6beec9", fg="black", font="Courier 12 bold")
logoutButton.grid(row=0, column=1, sticky=NW, padx=10, pady=10)

addTaskButton = Button(bottomFrame, text="Add New Task", bg="#70fd5a",fg="black", font="Courier 12 bold",
                       command=Call_Window)
addTaskButton.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

#Labels
complete = Label(bottomFrame, text="Complete", fg="black", bg="white", font="Courier")
complete.grid(row=0, column=0, sticky=N, padx=10, pady=10)

inProgress = Label(bottomFrame, text="In Progress", fg="black", bg="white", font="Courier")
inProgress.grid(row=0, column=1, sticky=NW, padx=10, pady=10)

#Entries



root.mainloop()
