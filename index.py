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

# function to get images from the folder Training Image folder...
def getImagesAndLabels(path):
    imagePath = []
    faces = []
    Ids = []

    for picture in os.listdir(path):
        imagePath.append(os.path.join(path, picture))

    # output-> ['TrainingImage\\Rakshith.1.1', ...]

    for path in imagePath:
        # converting the image into gray scale using ITU-R 601-2 luma transform:
        # L = R * 299/1000 + G * 587/1000 + B * 114/1000
        pilImage = Image.open(path).convert('L')
        imageNp = np.array(pilImage)
        Id = int(os.path.split(path)[-1].split('.')[1])
        faces.append(imageNp)
        Ids.append(Id)
    
    return faces, Ids

# function to train images collected from the students.
def trainImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt2.xml')
    try:
        Faces, Id = getImagesAndLabels('TrainingImage')
    except Exception as e:
        res = 'Please make "TrainingImage" folder & put Images'
        notifications.configure(
            text=res,
            bg="SpringGreen3",
            width=50, 
            font=('times', 18, 'bold')
        )
        notifications.place(x=250, y=400)
    
    recognizer.train(Faces, np.array(Id))
    recognizer.save("./TrainingImageLabel/Trainer.yml")
    res = "Image Trained"
    notifications.configure(
            text=res,
            bg="SpringGreen3",
            width=50, 
            font=('times', 18, 'bold')
        )
    notifications.place(x=250, y=400)


# function to show error if label is not present 
def deleteErrorScreen():
    screen.destroy()

def showErrorScreen():
    global screen 
    screen = tk.Tk()
    screen.geometry('300x100')
    screen.iconbitmap('./logo.ico')
    screen.title('Warning!!')
    screen.configure(background='snow')
    tk.Label(
        screen,
        text='Enrollment & Name required!!!',
        fg='red',
        bg='white',
        font=('times', 16, ' bold ')
        ).pack()

    tk.Button(
        screen,
        text='OK',
        command=deleteErrorScreen,
        fg="black",
        bg="lawn green",
        width=9,
        height=1, 
        activebackground="Red",
        font=('times', 15, ' bold ')
        ).place(x=90,y= 50)

# function to provide student to take image
def takeStudentImage():
    rollNumber = text1.get()
    studentName = text2.get()
    if rollNumber == '' or studentName == '':
        showErrorScreen()
    else:
        cam = cv2.VideoCapture(0)
        cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt2.xml')
        sampleImages = 0
        while True:
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                sampleImages = sampleImages + 1
                cv2.imwrite("./TrainingImage/" + studentName + "." + rollNumber + '.' + str(sampleImages) + ".jpg",
                                gray[y:y + h, x:x + w])
                

                cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif sampleImages > 100:
                break

        cam.release()
        cv2.destroyAllWindows()

        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        Time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        row = [rollNumber, studentName, Date, Time]
        with open('./StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(row)
            csvFile.close()
        res = "Images Saved for Enrollment : " + rollNumber + " Name : " + studentName
        notifications.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        notifications.place(x=250, y=400)

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

notifications = tk.Label(
        root,
        text="All Things are Set",
        bg="green",
        fg="white",
        width=15,
        height=3,
        font=('times', 17, 'bold')
    )

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

takeImageButton = tk.Button(
        root,
        text="Take Image",
        bg="yellow",
        fg="black",
        command=takeStudentImage,
        width=10,
        height=1,
        activebackground="Red",
        font=('times', 15, 'bold')
    )
takeImageButton.place(x=40, y=550)

trainImageButton = tk.Button(
        root,
        text="Train Image",
        bg="yellow",
        fg="black",
        command=trainImage,
        width=10,
        height=1,
        activebackground="Red",
        font=('times', 15, 'bold')
    )
trainImageButton.place(x=200, y=550)

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