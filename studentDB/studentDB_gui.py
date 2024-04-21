from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import requests

# Front End GUI
root= Tk()
root.title("Login System")
root.geometry("1000x600")

# adding image to root window
image=ImageTk.PhotoImage(file="/Users/miaxu/Desktop/UT/SP24/360/Project1/LoginApp/1.jpeg")
label=Label(root, image=image)  #added image on label
label.pack()

openeye = PhotoImage(file="/Users/miaxu/Desktop/UT/SP24/360/Project1/LoginApp/openeye.png")
openeye = openeye.subsample(12, 12)
closeeye = PhotoImage(file="/Users/miaxu/Desktop/UT/SP24/360/Project1/LoginApp/close.png")
closeeye = closeeye.subsample(12, 12)


# CREATING HEADING FOR ROOT WINDOW
lbel=Label(root, text="LOGIN SYSTEM",font=("times new roman",15,'bold'),bg='gold2')
lbel.place(x=0,y=5,width=1000,height=100)


#creating  frame on root window
frame=Frame(root)
frame.place(x=30, y=120, width=400, height=450)


#creating labels and entrybox on frame
userlabel = Label(frame, text="Student ID", font=("Microsoft Yahei UI Light", 15, 'bold'), bg='white', fg='gray')
userlabel.place(x=80, y=50)

entry1 = Entry(frame, font=("Microsoft Yahei UI Light", 15))  #creating entry box
entry1.place(x=80, y=80, width=250)

passlabel = Label(frame, text="Password", font=("Microsoft Yahei UI Light", 15 ,'bold'), bg='white', fg='gray')#password
passlabel.place(x=80, y=120)

entry2 = Entry(frame, font=("Microsoft Yahei UI Light", 15), show='*')
entry2.place(x=80, y=150, width=250)

eyeButton = Button(frame, image = closeeye, command = lambda: hide(), bg = "white", bd =0, cursor='hand')
eyeButton.place(x=300, y=155 )

def hide():
    if entry2.cget('show') == '*':
        eyeButton.config(image= openeye)
        entry2.config(show = '')
    else:
        eyeButton.config(image= closeeye)
        entry2.config(show = '*')

# login button
button = Button(frame, text='LOGIN', activebackground="#00B0F0", activeforeground='white', fg='gray',
                    bg="#F0F8FF", font=("Arial", 15, 'bold'), command=lambda: login())
button.place(x=80, y=230, width=250)


# session = requests.session()
def login():
    if entry1.get() and entry2.get():
        url = 'http://127.0.0.1:5000/login'
        resp = requests.post(url, data={'id':entry1.get(), 'password':entry2.get()})
        if resp.ok:
            messagebox.showinfo("Success", "Login Succesfully")

            #To return a protected page for authenticated user; NEED a session!
            protected_page = Toplevel()
            url = 'http://127.0.0.1:5050/index'
            msg = requests.get(url).text
            text = Label(protected_page, text=msg, font=('Algerian', 14))
            text.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            
        elif resp.status_code == 401:
            messagebox.showerror("Warning", "User Not Found. Please Double Check your Student ID")
        else:
            messagebox.showerror("Warning", "Incorrect Password")
    else:
         messagebox.showerror("Warning", "Please enter username and password.")

root.mainloop()