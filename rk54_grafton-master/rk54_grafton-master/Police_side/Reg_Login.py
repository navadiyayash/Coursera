#import modules

from tkinter import *
import os
from videoTester import multiple_cam,run
from PIL import Image, ImageTk, ImageSequence
# Designing window for registration

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

class App:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = Canvas(parent, width=480, height=270, bg='LightBlue1', highlightbackground='LightBlue1')
        self.canvas.pack()
        self.sequence = [ImageTk.PhotoImage(img)
                            for img in ImageSequence.Iterator(
                                    Image.open(
                                    r'C:\Users\Hello\Documents\Sem 8\Project\image.gif'))]
        self.image = self.canvas.create_image(250,200, image=self.sequence[0])
        self.animate(1)
    def animate(self, counter):
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        self.parent.after(20, lambda: self.animate((counter+1) % len(self.sequence)))


        
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Smart Surveillance")
    register_screen.geometry("300x250")
    register_screen.configure(background='LightBlue1')

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please Enter Details Below to Register", bg="blue", width="300", height="2", font=("Times",18,"bold")).pack()
    Label(register_screen, text="",bg='LightBlue1').pack()
    username_lable = Label(register_screen, text="Username * ",bg='LightBlue1',font='Times 28 bold')
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username, width=60)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ",bg='LightBlue1',font='Times 28 bold')
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*', width=60)
    password_entry.pack()
    Label(register_screen, text="",bg='LightBlue1').pack()
    Button(register_screen, text="Register", width=60, height=2, bg="blue", fg='white', command = register_user).pack()
    app=FullScreenApp(register_screen)
    app=App(register_screen)


# Designing window for login 

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Smart Surveillance")
    login_screen.geometry("300x250")
    login_screen.configure(background='LightBlue1')
    #Label(login_screen, text="Please Enter Details Below to Login",bg='LightBlue1',font='Times 32 bold italic underline').pack()
    Label(login_screen,text="Please Enter Details Below to Login", bg="blue", width="300", height="2", font=("Times",18,"bold")).pack()
    Label(login_screen, text="",bg='LightBlue1').pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ",bg='LightBlue1',font='Times 28 bold').pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify, width=60)
    username_login_entry.pack()
    Label(login_screen, text="",bg='LightBlue1').pack()
    Label(login_screen, text="Password * ",bg='LightBlue1',font='Times 28 bold').pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*',width=60)
    password_login_entry.pack()
    Label(login_screen, text="",bg='LightBlue1').pack()
    Button(login_screen, text="Login", width=60, height=2, bg='blue', fg='white', command = login_verify).pack()
    app=FullScreenApp(login_screen)
    app=App(login_screen)

# Implementing event on register button

def register_user():

    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    success=Label(register_screen, text="Registration Done Successfully!!!", fg="green", bg="LightBlue1", font=("Times", 18,"bold")).pack(pady=15)

# Implementing event on login button 

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
        else:
            password_not_recognised()
    else:
        user_not_found()

# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Smart Surveillance")
    login_success_screen.geometry("150x100")
    login_success_screen.configure(background='LightBlue1')
    Label(login_success_screen, text="Your Are Logged In!!!", bg="blue", width="300", height="2", font=("Times",18,"bold")).pack()
    ok=Button(login_success_screen, text="Get Started", width=60, height=3, bg='blue', fg='white', font=("bold"), command=multiple_cam)
    ok.place(x=400,y=500)

    success=1
    app=FullScreenApp(login_success_screen)
    app=App(login_success_screen)

# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Smart Surveillance")
    password_not_recog_screen.geometry("150x100")
    password_not_recog_screen.configure(background='LightBlue1')
    Label(password_not_recog_screen, text="Invalid Password!!! ", bg="blue", width="300", height="2", font=("Times",18,"bold")).pack()
    ok=Button(password_not_recog_screen, text="OK", width=60, height=3, bg='blue', fg='white', font=("bold"), command=delete_password_not_recognised)
    ok.place(x=400,y=500)
    app=FullScreenApp(password_not_recog_screen)
    app=App(password_not_recog_screen)
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Smart Surveillance")
    user_not_found_screen.geometry("150x100")
    user_not_found_screen.configure(background='LightBlue1')
    Label(user_not_found_screen, text="User Not Found!!! ", bg="blue", width="300", height="2", font=("Times",18,"bold")).pack()
    ok=Button(user_not_found_screen, text="OK", width=60, height=3, bg='blue', fg='white', font=("bold"), command=delete_user_not_found_screen)
    ok.place(x=400,y=500)
    app=FullScreenApp(user_not_found_screen)
    app=App(user_not_found_screen)

# Deleting popups

def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Smart Surveillance")
    main_screen.configure(background='LightBlue1')
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Times",18,"bold")).pack()
    Label(text="", bg='LightBlue1').pack()
    Button(text="Login", height="2", width="60", bg='blue',fg='white', font=("bold"), command = login).pack()
    Label(text="", bg='LightBlue1').pack()
    Button(text="Register", height="2", width="60", bg='blue',fg='white', font=("bold"), command=register).pack()
    app=FullScreenApp(main_screen)
    app=App(main_screen)
    main_screen.mainloop()

success=0
main_account_screen()
if success==1:
        import videoTester
