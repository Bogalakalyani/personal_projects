import datetime
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import cv2
import face_recognition
import dlib
import os
import csv

root = tk.Tk()
root.title("")
root.geometry("1100x700")

detector = dlib.get_frontal_face_detector()

path = "C:\\Users\\Kalyani_Reddy\\Desktop\\star bucks\\new\\images"

known_encodings = {}

for file in os.listdir(path):
    image = os.path.join(path,file)
    known_image = face_recognition.load_image_file(image)
    file_name,extension = os.path.basename(os.path.normpath(image)).split(".")
    known_encoding = face_recognition.face_encodings(known_image)
    known_encodings[file_name] = known_encoding


def launch_camera():
    global cap, image_label
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open the camera")
        return
    def show_camera():
        ret, frame = cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            image = ImageTk.PhotoImage(pil_image)
            image_label.configure(image=image,width=800, height=400)
            image_label.image = image
        image_label.after(10, show_camera)
    show_camera()

    myButton1.configure(text="Capture Image",command = capture_frames,fg = "black")

def back():
    global image_label, myButton1

    myLabel.config(text="Attendance Tracking System")

    for widget in frame1.winfo_children():
        widget.pack_forget()
    for widget in frame2.winfo_children():
        widget.pack_forget()

    image = Image.open("C:\\Users\\Kalyani_Reddy\\Downloads\\glitch.jpg")
    image = image.resize((800, 400), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(image)
    image_label.configure(image=tk_image)
    image_label.image = tk_image
    image_label.pack(padx=10, pady=50)

    myButton1.configure(text="Launch Camera", command=launch_camera)
    myButton1.pack(pady=50)

    label2 = tk.Label(frame2, text="", font=("Arial", 16))
    label2.pack(padx=10, pady=10)

def enroll(frame):
    global frame2
    myLabel1 = tk.Label(frame2, text="Please enter your name", width=30, borderwidth=5, fg="blue", font=("Helvetica", 15), anchor="center")
    myLabel1.pack()
    
    e = tk.Entry(frame2, width=50, fg="blue", borderwidth=5)
    e.pack()

    def save_image():
        name = e.get() + ".jpg"
        image_path = "C:\\Users\\Kalyani_Reddy\\Desktop\\star bucks\\new\\images\\" + name
        cv2.imwrite(image_path, frame)

        myLabel1 = tk.Label(frame2, text="You are successfully enrolled", width=30, borderwidth=5, fg="blue", font=("Helvetica", 15), anchor="center")
        myLabel1.pack()

        myButton1.configure(text="Back", command=back, fg="black")

    enroll_button = tk.Button(frame2, text="Enroll", command=save_image, fg="black")
    enroll_button.pack()

def capture_frames():
    global cap, image_label, captured_encoding,frame
    cap = cv2.VideoCapture(0)
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(rgb_frame)
            if len(face_encodings) > 0:
                captured_encoding = face_encodings[0]  # Extract the encoding for the first detected face
                pil_image = Image.fromarray(rgb_frame)
                faces = detector(rgb_frame)
                for face in faces:
                    x = face.left()
                    y = face.top()
                    w = face.width()
                    h = face.height()
                    draw = ImageDraw.Draw(pil_image)
                    draw.rectangle([(x, y), (x + w, y + h)], outline=(255, 255, 0), width=4)
                image = ImageTk.PhotoImage(pil_image)
                image_label.configure(image=image, width=800, height=400)
                image_label.image = image
            else:
                myLabel1 = tk.Label(frame2, text="Please capture your image correctly", width=30, borderwidth=5, fg="blue",font=("Helvetica", 15),anchor="center")
                myLabel1.pack()
                myButton1.configure(text="Launch Camera",command = launch_camera,fg = "black")

        cap.release()
        cap = None
    
    results = {}
    for name, encodings in known_encodings.items():
        match_results = face_recognition.compare_faces(encodings, captured_encoding)
        results[name] = match_results
    print(results)
    
    if all(value == [False] for value in results.values()):
        myLabel1 = tk.Label(frame2, text="You are not enrolled", width=30, borderwidth=5, fg="blue",font=("Helvetica", 15),anchor="center")
        myLabel1.pack()
        myLabel1 = tk.Label(frame2, text="Please click enroll button to enroll.", width=30, borderwidth=5, fg="blue",font=("Helvetica", 15),anchor="center")
        myLabel1.pack()
        myButton1.configure(text="Enroll", command=lambda: enroll(frame), fg="black")

    else:
        for name, match_results in results.items():
            for result in match_results:
                if result:
                    myLabel1 = tk.Label(frame2, text=name, width=30, borderwidth=5, fg="blue",font=("Helvetica", 15),anchor="center")
                    myLabel1.pack()
                    myLabel2 = tk.Label(frame2, text="Attendance Taken Successfully", width=30, borderwidth=5, fg="blue",font=("Helvetica", 10),anchor="center")
                    myLabel2.pack()
                    myButton1.configure(text="Back",command = back,fg = "black")
                    current_date = datetime.date.today()
                    current_time = datetime.datetime.now().time()
                    filename = "C:\\Users\\Kalyani_Reddy\\Desktop\\star bucks\\new\\data.csv"
                    data = [['name','Date','Time'],
                        [name,current_date,current_time]]
                    with open(filename, 'a', newline=" ") as file:
                        writer = csv.writer(file)
                        writer.writerows(data)
                    

myLabel = tk.Label(root, text="Attendance Tracking System", font=('Helvetica', 20))
myLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

frame1 = tk.Frame(root, bd=2, relief="solid")
frame1.grid(row=1, column=0, sticky="nsew")

frame2 = tk.Frame(root, bd=2, relief="solid")
frame2.grid(row=1, column=1, sticky="nsew")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=50)
root.grid_columnconfigure(1, weight=50)

image = Image.open("C:\\Users\\Kalyani_Reddy\\Downloads\\glitch.jpg")
image = image.resize((800, 400), Image.ANTIALIAS)
tk_image = ImageTk.PhotoImage(image)

image_label = tk.Label(frame1, image=tk_image)
image_label.pack(padx=10, pady=50)

myButton1 = tk.Button(frame1, text="Launch Camera", bg = "white",fg = "black",font=('Helvetica', 20,"bold"), width=15, height=2, command=launch_camera,relief="raised", bd=3)
myButton1.pack(pady=50)

label2 = tk.Label(frame2, text="", font=("Arial", 16))
label2.pack(padx=10, pady=10)

root.mainloop()
