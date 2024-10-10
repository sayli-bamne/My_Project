from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class login_form:
    def __init__(self,root) :
        
        self.root = root
        self.root.title("Login Page")
        self.root.geometry('1500x870')
        self.root.resizable(0,0)


        #==============Background image==================================

        # FUNCTIONS
        def cancel():
            if messagebox.askyesno("Exit", "Do you want to exit?"):
                root.destroy()

        def login():
            userName='Sayali' 
            Password='sayali@12345'
            if userNameEntry.get()==userName and PasswordEntry.get()==Password:
                messagebox.showinfo(title='Login Successful',message='You have successfully logged in')
                root.destroy()
                from MDI import mdi_form
                mdi_window = Tk()
                mdi_instance = mdi_form(mdi_window) 
            elif userNameEntry.get()==userName and PasswordEntry.get()!=Password:
                messagebox.showerror(title='Wrong password',message='Please check your password')
            elif userNameEntry.get()!=userName and PasswordEntry.get()==Password:
                messagebox.showerror(title='Wrong password',message='Please check your username')
            elif userNameEntry.get()=="" and PasswordEntry.get()=="":
                messagebox.showerror(title='Errower',message='please fill all entrys')   
       
            else:
                messagebox.showerror(title='Login Failed',message='Invalid Username and password')   

        def eyeButton():
            if PasswordEntry.cget('show') == '':
                PasswordEntry.config(show='*')
                eye_button.config(image=eye_photo_closed)
            else:
                PasswordEntry.config(show='')
                eye_button.config(image=eye_photo_open)             

        #==================frame=================================================
        frame1=Frame(root,bg='powder blue')
        frame1.place(x=0,y=0,height=800,width=900)

        frame=Frame(root,bg='powder blue')
        frame.place(x=900,y=2,height=800,width=600)
        
        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image = photo)
            label.image = photo 

        image = Image.open('FDPbYbUWEAMEWg6.jpg')
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(frame1, image = photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=BOTH, expand = YES)

        
        #ICONS
        img1=Image.open("loginicon2.png")
        img1=img1.resize((150,150),Image.ADAPTIVE)
        self.photo_img1=ImageTk.PhotoImage(img1)
        lbimg1=Label(root,image= self.photo_img1,bg="powder blue",borderwidth=0)
        lbimg1.place(x=1150,y=100,width=150,height=150)


        # LABEL AND ENTRY
        headLabel=Label(frame,text='USER LOGIN',font=('Times 45 italic bold'),fg='red',bg='powder blue')
        headLabel.place(x=130,y=280)

        userName=Label(frame,text='User Name',font=('Times 20 italic bold'),fg='black',bg='powder blue' )
        userName.place(x=130,y=430)
        userNameEntry=Entry(frame,font=('Times 15 italic bold'),fg='black' )
        userNameEntry.place(x=300,y=435)

        Password=Label(frame,text='Password',font=('Times 20 italic bold'),fg='black' ,bg='powder blue')
        Password.place(x=130,y=550)
        PasswordEntry=Entry(frame,show='*',font=('Times 15 italic bold') ,fg='black' )
        PasswordEntry.place(x=300,y=555)

        # Eye Button
        eye_icon_open = Image.open("OIP (2).jpeg")
        eye_icon_open = eye_icon_open.resize((20, 20), Image.ADAPTIVE)
        eye_photo_open = ImageTk.PhotoImage(eye_icon_open)

        eye_icon_closed = Image.open("OIP (3).jpeg")
        eye_icon_closed = eye_icon_closed.resize((20, 20), Image.ADAPTIVE)
        eye_photo_closed = ImageTk.PhotoImage(eye_icon_closed)

        eye_button = Button(PasswordEntry, image=eye_photo_closed, bg='white', bd=0, command=eyeButton)
        eye_button.place(x=175,y=2)

        # BUTTONS
        button=Button(frame,text='Login',font=('Times 15 italic bold'),bg='red',fg='white',bd=5
                        ,cursor="hand2",activeforeground='white',activebackground='red',width=16,command=login)
        button.place(x=100,y=650)

        button2=Button(frame,text='Cancel',font=('Times 15 italic bold'),bg='red',fg='white',bd=5
                        ,cursor="hand2",activeforeground='white',activebackground='red',width=16,command=cancel)
        button2.place(x=350,y=650)

if __name__ == "__main__":
    root = Tk()
    obj = login_form(root)
    root.mainloop()