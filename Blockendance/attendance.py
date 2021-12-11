import tkinter as tk
import csv
import cv2
import os
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

window = tk.Tk()
window.title("STUDENT ATTENDANCE USING FACE RECOGNITION SYSTEM")
window.geometry('800x500')

dialog_title = 'QUIT'
dialog_text = "are you sure?"
window.configure(background='steel blue')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


def clear():
    std_name.delete(0, 'end')
    res = ""
    label4.configure(text=res)


def clear2():
    std_number.delete(0, 'end')
    res = ""
    label4.configure(text=res)


def takeImage():
    name = (std_name.get())
    Id = (std_number.get())
    if name.isalpha():
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.1, 3)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                # store each student picture with its name and id
                cv2.imwrite("TrainingImages\ " + name + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + h])
                cv2.imshow('FACE RECOGNIZER', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # stop the camera when the number of picture exceed 50 pictures for each student
            if sampleNum > 50:
                break

        cam.release()
        cv2.destroyAllWindows()
        # print the student name and id after a successful face capturing
        res = 'Student details saved with: \n Matric number : ' + Id + ' and  Full Name: ' + name

        row = [Id, name]

        with open('studentDetailss.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        label4.configure(text=res)
    else:

        if name.isalpha():
            res = "Enter correct Matric Number"
            label4.configure(text=res)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def trainImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImages")
    recognizer.train(faces, np.array(Id))
    recognizer.save("Trainner.yml")
    res = "Image Trained"
    label4.configure(text=res)


def trackImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("studentDetailss.csv")
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cam = cv2.VideoCapture(0)
    # create a dataframe to hold the student id,name,date and time
    col_names = {'Id', 'Name', 'Date', 'Attendance',}
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            #  a confidence less than 50 indicates a good face recognition
            if conf < 40:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                aa = df.loc[df['ID'] == Id]['NAME'].values
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                row2 = [Id, aa, date,'A']
                #   open the attendance file for update
                with open('AttendanceFile.csv', 'a+', newline='') as csvFile2:
                    writer2 = csv.writer(csvFile2)
                    row2[3]= 'P'
                    writer2.writerow(row2)
                csvFile2.close()
                # print attendance updated on the notification board of the GUI
                res = 'ATTENDANCE UPDATED WITH DETAILS'
                label4.configure(text=res)

            else:
                Id = 'Unknown'
                tt = str(Id)
                #  store the unknown images in the images unknown folder
                if conf > 65:
                    noOfFile = len(os.listdir("ImagesUnknown")) + 1
                    cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", img[y:y + h, x:x + w])
                    res = 'ID UNKNOWN, ATTENDANCE NOT UPDATED'
                    label4.configure(text=res)
            # To avoid duplication in the attendance file.
            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
            # show the student id and name
            cv2.putText(img, str(tt), (x, y + h - 10), font, 0.8, (255, 255, 255), 1)
            cv2.imshow('FACE RECOGNIZER', img)
        if cv2.waitKey(1000) == ord('q'):
            break

        cam.release()
        cv2.destroyAllWindows()
def ListToBlockchain():
    
    file= open("AttendanceFile.csv")
    next(file)

    resultat=[]
    for row in file:
        numb = row.split(',')[0]
        resultat.append(numb)
    print(resultat)
    return resultat



label1 = tk.Label(window, background="steel blue", fg="white", text="Name :", width=10, height=1,
                  font=('Helvetica', 16))
label1.place(x=83, y=40)
std_name = tk.Entry(window, background="white", fg="white", width=25, font=('Helvetica', 14))
std_name.place(x=280, y=41)
label2 = tk.Label(window, background="steel blue",fg="white", text="Matric Number :", width=14, height=1,
                  font=('Helvetica', 16))
label2.place(x=100, y=90)
std_number = tk.Entry(window, background="white", fg="black", width=25, font=('Helvetica', 14))
std_number.place(x=280, y=91)

clearBtn1 = tk.Button(window, background="light sea green", command=clear, fg="white", text="CLEAR", width=8, height=1,
                      activebackground="red", font=('Helvetica', 10))
clearBtn1.place(x=580, y=42)
clearBtn2 = tk.Button(window, background="light sea green", command=clear2, fg="white", text="CLEAR", width=8,
                      activebackground="red", height=1, font=('Helvetica', 10))
clearBtn2.place(x=580, y=92)

label3 = tk.Label(window, background="steel blue", fg="white", text="Notification", width=10, height=1,
                  font=('Helvetica', 20))
label3.place(x=320, y=155)
label4 = tk.Label(window, background="white", fg="black", width=55, height=4, font=('Helvetica', 14, 'italic'))
label4.place(x=95, y=205)

takeImageBtn = tk.Button(window, command=takeImage, background="light sea green", fg="white", text="CAPTURE IMAGE",
                         activebackground="red",
                         width=15, height=3, font=('Helvetica', 12))
takeImageBtn.place(x=80, y=360)
trainImageBtn = tk.Button(window, command=trainImage, background="light sea green", fg="white", text="TRAINED IMAGE",
                          activebackground="red",
                          width=15, height=3, font=('Helvetica', 12))
trainImageBtn.place(x=250, y=360)
trackImageBtn = tk.Button(window, command=trackImage, background="light sea green", fg="white", text="TRACK IMAGE", width=12,
                          activebackground="red", height=3, font=('Helvetica', 12))
trackImageBtn.place(x=420, y=360)
bruhButton = tk.Button(window, command=ListToBlockchain, background="light sea green", fg="white", text="PRESENCE LIST", width=16,
                          activebackground="red", height=3, font=('Helvetica', 12))
bruhButton.place(x=565, y=360)

window.mainloop()
