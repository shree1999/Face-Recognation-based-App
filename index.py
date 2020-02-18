import tkinter as tk
from tkinter import *
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
        bg="yellow",
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
        bg="yellow",
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

root.mainloop()