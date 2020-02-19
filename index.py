import tkinter as tk
from tkinter import messagebox
import pandas as pd
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import datetime
import time

root = tk.Tk()
root.title("Face Attendance Management System-FAMS")

root.geometry("1280x720")
root.configure(background="snow")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.iconbitmap('./logo.ico')


# functions to provide clear respones by the user in input field
def clearRollNumber():
    text1.delete(first=0, last=22)


def clearName():
    text2.delete(first=0, last=50)

# function for seeing registered students
def showStudents():
    window = tk.Tk()
    window.title("FAMS - Admin-Pannel")
    window.iconbitmap('./logo.ico')
    window.geometry("720x480")

    def adminLoginOption():
        username = text1.get()
        password = text2.get()

        if username == "admin":
            if password == "admin1234":
                window.destroy()

                win = tk.Tk()
                win.title("Students Register")
                win.configure(background="snow")
                location = './StudentDetails/StudentDetails.csv'
                with open(location, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tk.Label(
                                win, 
                                width=8, 
                                height=1, 
                                fg="black", 
                                font=('times', 15, ' bold '),
                                bg="lawn green", 
                                text=row, 
                                relief=tk.RIDGE
                            )
                            label.grid(row=r, column=c)
                            c = c + 1
                        r = r + 1
                win.mainloop()
            else:
                valid = "Wrong Password"
                messagebox.showwarning(title=None, message=valid)
        else:
            valid = "Wrong Username"
            messagebox.showwarning(title=None, message=valid)
    
    def clearAdminName():
        text1.delete(first=0, last=50)
    
    def clearAdminPassword():
        text2.delete(first=0, last=50)

    label1 = tk.Label(
        window,
        text="Username",
        bg="deep pink", 
        fg="black", 
        width=15,
        height=2,
        font=('times', 15, 'bold')
    )
    label1.place(x=30, y=40)

    text1 = tk.Entry(
        window,
        bg="white",
        fg="red",
        font=('times', 25, 'bold'),
        width=15
    )
    text1.place(x=250, y=40)

    clear1 = tk.Button(
        window,
        command=clearAdminName,
        bg="deep pink",
        fg="black",
        text="clear",
        width=10,
        height=1,
        activebackground="Red",
        font=('times', 15, 'bold')
    )
    clear1.place(x=550, y=40)

    label2 = tk.Label(
        window,
        text="Password",
        bg="deep pink", 
        fg="black", 
        width=15,
        height=2,
        font=('times', 15, 'bold')
    )
    label2.place(x=30, y=140)

    text2 = tk.Entry(
        window,
        bg="white",
        fg="red",
        font=('times', 25, 'bold'),
        width=15,
        show="*"
    )
    text2.place(x=250, y=140)

    clear2 = tk.Button(
        window,
        command=clearAdminPassword,
        bg="deep pink",
        fg="black",
        text="clear",
        width=10,
        height=1,
        activebackground="Red",
        font=('times', 15, 'bold')
    )
    clear2.place(x=550, y=140)

    loginButton = tk.Button(
        window,
        command=adminLoginOption,
        bg="deep pink",
        fg="black",
        width=10,
        height=1,
        text="Login",
        activebackground="Red",
        font=('times', 15, 'bold')
    )
    loginButton.place(x=300, y=310)

# function to provide closing of FAMS
def onClosingApplication():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol(name="WM_DELETE_WINDOW", func=onClosingApplication)

# function to validate whether the roll number is numeric or not
def entryValidation(element, acttype):
    if acttype == '1':
        if not element.isdigit():
            return False
    return True


# Creating all the required enteries for our gui app
topic = tk.Label(
        root, 
        text="Face-Recognition-Based-Attendance-Management-System",
        bg="cyan",
        fg="black",
        width=50,
        height=3,
        font=('times', 30, 'italic bold')
    )
topic.place(x=50, y=20)

notifications = tk.Label(
        root,
        text="All Things are Set",
        bg="green",
        fg="white",
        width=15,
        height=3,
        font=('times', 17, 'bold')
    )

label1 = tk.Label(
        root,
        text="Enter Roll-Number",
        bg="deep pink", 
        fg="black", 
        width=20,
        height=2,
        font=('times', 15, 'bold')
    )
label1.place(x=150, y=200)

text1 = tk.Entry(
        root,
        bg="white",
        fg="red",
        font=('times', 25, 'bold'),
        validate="key",
        width=20
    )
text1['validatecommand'] = (text1.register(func=entryValidation), '%P', '%d')
text1.place(x=500, y=210)

label2 = tk.Label(
        root,
        text="Enter Name",
        bg="deep pink", 
        fg="black", 
        width=20,
        height=2,
        font=('times', 15, 'bold')
    )

label2.place(x=150, y=290)

text2 = tk.Entry(
        root,
        bg="white",
        fg="red",
        font=('times', 25, 'bold'),
        width=20
    )
text2.place(x=500, y=300)

clearRollButton = tk.Button(
        root, 
        text="Clear",
        command=clearRollNumber,
        fg="black",
        bg="deep pink",
        width=10,
        height=1,
        activebackground="Red",
        font=('times', 15, 'bold')
    )
clearRollButton.place(x=900, y=210)

clearNameButton = tk.Button(
        root,
        text="Clear",
        command=clearName,
        fg="black",
        bg="deep pink",
        width=10,
        height=1,
        activebackground="Red",
        font=('times', 15, 'bold')
    )
clearNameButton.place(x=900, y=300)

registeredStudents = tk.Button(
        root,
        text="Registered Students",
        command=showStudents,
        fg="black",
        bg="deep pink",
        width=20,
        height=1,
        activebackground="Red",
        font=('times', 15, 'bold')
    )
registeredStudents.place(x=990, y=550)

root.mainloop()