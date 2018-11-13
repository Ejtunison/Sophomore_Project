from tkinter import *
from DatabasePush import *
def Call_Window():
    window = Tk()
    window.title("New Task")
    window.configure(background="#f6e0f4")

    task = Label(window, text="Title:", bg="#f6e0f4", fg="#8b01a5", font="Times 12")
    titleEntry = Entry(window, font="Courier", fg="#8b01a5", bg="white")
    description = Label(window, text="Description:", bg="#f6e0f4", fg="#8b01a5", font="Times 12")
    descriptionEntry = Text(window, height=7, width=25, font="Courier", fg="#8b01a5", bg="white")
    deadline = Label(window, text="Dealine:", bg="#f6e0f4", fg="#8b01a5", font="Times 12")
    deadlineEntry = Entry(window, font="Courier", fg="#8b01a5", bg="white")
    user = Label(window, text="User:", bg="#f6e0f4", fg="#8b01a5", font="Times 12")
    userEntry = Entry(window, font="Courier", fg="#8b01a5", bg="white")

    task.grid(row=1, column=1, sticky=E, padx=3, pady=3)
    description.grid(row=3, column=1, sticky=NE, padx=3, pady=3)
    deadline.grid(row=5, column=1, sticky=E, padx=3, pady=3)
    user.grid(row=7, column=1, sticky=E, padx=3, pady=3)

    titleEntry.grid(row=1, column=2, sticky=W, padx=3, pady=3)
    descriptionEntry.grid(row=3, column=2, sticky=W, padx=3, pady=3)
    deadlineEntry.grid(row=5, column=2, sticky=W, padx=3, pady=3)
    userEntry.grid(row=7, column=2, sticky=W, padx=3, pady=3)

    taskButton = Button(window, text="Add Task", bg="white", fg="#8b01a5", font="Courier 12", highlightcolor="#ea8ce1",
                        relief="raised", activebackground="#8b01a5", activeforeground="white",
                        command = lambda: task_add(titleEntry, deadlineEntry, descriptionEntry,))
    taskButton.grid(row=9, column=4, padx=10, pady=10)