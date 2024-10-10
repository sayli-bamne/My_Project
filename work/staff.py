from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import filedialog
import mysql.connector
import io
import re


class staff_form:
    def __init__(self, staff):
        self.staff=staff
        self.staff.title("Staff Form")
        self.staff.geometry("1500x1500")
        self.staff.config(bg="#06283D")
        self.staff.config(bg="#06283D")

        try :
            import tkinter as tk # Python 3
        except :
            import tkinter as tk # Python 2

        #database connection
        mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
        mycursor=mysqldb.cursor()    
        


        ID_var=StringVar()
        date_var=StringVar()
        name_var=StringVar()
        address_var=StringVar()
        Email_var=StringVar()
        contact_var=StringVar()
        salary_var=StringVar()
        
        
        def update_time():
            current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
            time_label.config(text="Current Time: " + current_time)
            staff.after(1000, update_time)  # Update time every 1 second

        def update_date():
            today_date = datetime.now().strftime("%Y-%m-%d")
            date_label.config(text="Today's Date: " + today_date)
        #================validation====================================
        def staff_ID(id):
            if id.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Only numbers can access')
                return False    
        
        def staff_salary(s):
            if s.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid salaryEntry')
                return False  
        
        #===========================Functions=====================================
        
        def staff_window():
            self.staff.destroy()
            from MDI import mdi_form
            mdi_window = Tk()
            staff_instance = mdi_form(mdi_window)
    
        #========================Heading===================================
        lbtitle=Label(self.staff,text='Staff Details',fg='white',bg='#06283D',font=('Times 50 italic bold'))
        lbtitle.place(x=580,y=10)

        #==========================database=========================================
        def generate_id():
            mycursor.execute("SELECT MAX(s_id) FROM staff")
            max_id = mycursor.fetchone()[0]
            mycursor.close()
            return max_id + 1 if max_id else 1

        def add_entry():
            new_id = generate_id()
            self.IDEntry.config(state="normal")
            self.IDEntry.delete(0, END)
            self.IDEntry.insert(0, new_id)
            mysqldb.close()

        def searchf():
            search = IDEntry1.get()
            try:
                mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
                mycursor=mysqldb.cursor() 
                mycursor.execute("SELECT * FROM staff WHERE s_id = %s", (search,))
                row = mycursor.fetchone()
                if row:
                    id1, date1, s_name, gend, add1, Email1, cont1, salary1, photo_bytes = row
                    self.IDEntry.delete(0, END)
                    self.IDEntry.insert(END, id1)
                    self.dateEntry.delete(0, END)
                    self.dateEntry.insert(END, date1)
                    self.NameEntry.delete(0, END)
                    self.NameEntry.insert(END, s_name)
                    self.genderchoosen.delete(0, END)
                    self.genderchoosen.insert(END, gend)
                    self.AddressEntry.delete(0, END)
                    self.AddressEntry.insert(END, add1)
                    self.EmailEntry.delete(0, END)
                    self.EmailEntry.insert(END, Email1)
                    self.contEntry.delete(0, END)
                    self.contEntry.insert(END, cont1)
                    self.salaryEntry.delete(0, END)
                    self.salaryEntry.insert(END, salary1)
                    img = Image.open(io.BytesIO(photo_bytes))
                    img = img.resize((170, 160))
                    display_image(img)
                else:
                    messagebox.showinfo("Not Found", f"No record found with ID: {search}")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error searching record: {err}")
            finally:
                mysqldb.commit()

        def Save():
            id1 = self.IDEntry.get()
            date1= self.dateEntry.get()
            s_name = self.NameEntry.get()
            gend = self.genderchoosen.get()
            add1 = self.AddressEntry.get()
            Email1 = self.EmailEntry.get()
            cont1 = self.contEntry.get()
            salary1 = self.salaryEntry.get()
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor() 
            if not re.match(r'^[0-9]{10}$', cont1):
                messagebox.showerror("Error", "Please enter a valid 10-digit contact number.")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', Email1):
                messagebox.showerror("Error", "Please enter a valid email address.")
            elif id1=="" or s_name==""  or add1=="" or Email1=="" or cont1==""  or gend==""or salary1=="" or date1=="" :
                messagebox.showerror(title='Wrong ',message='Please enter all filds')
            else:
                try:
                    if 'resized_image' not in globals():
                        messagebox.showerror("Error", "No image uploaded")
                        return

                    photo_bytes = image_to_byte_array(resized_image)

                    sql = "INSERT INTO  staff(s_id,date,s_name,gender,address,email_id,contact,salary,photo) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)"
                    val = (id1, date1, s_name, gend, add1, Email1, cont1, salary1, photo_bytes)

                    mycursor.execute(sql, val)
                    mysqldb.commit()
                    fetch_data()
                    messagebox.showinfo("information", "Employee inserted successfully...")
                    Clear_button()
                    mysqldb.update()
                except Exception as e:
                    print(e)
                    mysqldb.close()            

        def upload_photo():
            global resized_image
            filename = filedialog.askopenfilename(initialdir="/", title="Select Photo", filetypes=(("JPEG files", ".jpg"), ("PNG files", ".png"), ("All files", ".")))
            original_image = Image.open(filename)
            resized_image = original_image.resize((170, 160))
            resized_image.save("resized_photo.jpg") 
            display_image(resized_image)

        def image_to_byte_array(image):
            global resized_image
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        
        def display_image(img):
            global photo_tk
            photo_tk = ImageTk.PhotoImage(img)
            label.config(image=photo_tk)
            label.image = photo_tk
         
        def update():
            global photo_bytes
            id1 = self.IDEntry.get()
            date1= self.dateEntry.get()
            s_name = self.NameEntry.get()
            gend = self.genderchoosen.get()
            add1 = self.AddressEntry.get()
            Email1 = self.EmailEntry.get()
            cont1 = self.contEntry.get()
            salary1 = self.salaryEntry.get()
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor() 
            if id1:
                mycursor.execute("SELECT * FROM staff WHERE s_id = %s", (id1,))
                row = mycursor.fetchone()
                if row:
                    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update this record?")
                    if confirm:
                        
                        if 'resized_image' not in globals():
                            messagebox.showerror("Error", "No image uploaded")
                            return
                        photo_bytes = image_to_byte_array(resized_image)
                        mycursor.execute("Update  staff set date= %s,s_name= %s,gender= %s,address= %s,email_id= %s,contact= %s,salary= %s, photo= %s where s_id= %s", 
                                         (date1, s_name, gend, add1, Email1, cont1, salary1, photo_bytes, id1))
                        
                        mysqldb.commit()
                        fetch_data()
                else:
                    messagebox.showinfo("Error", "No data found in the database for the given ID")
            else:
                messagebox.showinfo("Error", "Please enter an ID to update")

        def delete():
            id1 = self.IDEntry.get()
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor() 
            mycursor.execute("SELECT * FROM staff WHERE s_id = %s", (id1,))
            row = mycursor.fetchone()
            if id1:
                confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
                if confirm:
                    mycursor.execute("DELETE FROM staff WHERE s_id = %s", (id1,))
                    messagebox.showinfo("information", "Employee inserted successfully...")
                    mysqldb.commit()
            else:
                messagebox.showinfo("Error", "Please enter an ID to delete")
            fetch_data()
            
              
        def Clear_button():
            self.IDEntry.delete(0, END)
            self.dateEntry.delete(0, END)
            self.NameEntry.delete(0, END)
            self.genderchoosen.delete(0, END)
            self.AddressEntry.delete(0, END)
            self.EmailEntry.delete(0, END)
            self.contEntry.delete(0, END)
            self.salaryEntry.delete(0, END)
            label.config(image="")
            resized_image = None  

        def show():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor() 
            mycursor.execute("SELECT * FROM staff")
            records = mycursor.fetchall()

            for i, (id1,date1,s_name,gender,add1,Email1,cont1,salary1,photo_byte) in enumerate(records, start=1):
                library_table.insert("", "end", values=(id1,date1,s_name,gender,add1,Email1,cont1,salary1,photo_byte))
                mysqldb.close()

        def fetch_data():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor() 
            mycursor.execute("select * from staff")
            rows=mycursor.fetchall()
            if len(rows)!=0:
                library_table.delete(*library_table.get_children())
                for i in rows:
                    library_table.insert("",END,values=i)
                mysqldb.commit()
            mysqldb.close()   
     
        #=======================================frame==========================================================
        
        frameleft=LabelFrame(self.staff,bg='sky blue',bd=10,relief=RIDGE,text="Staff Details", font=('Times 15 italic bold'))
        frameleft.place(x=100,y=140,height=300,width=1000)

        frameright=LabelFrame(self.staff,bg='sky blue',bd=10,relief=RIDGE,text="Store Details", font=('Times 15 italic bold'))
        frameright.place(x=100,y=480,height=300,width=1000)

        #======================================data table====================================================        
           
        #scrollbar and columns   
        xscroll=ttk.Scrollbar(frameright,orient=HORIZONTAL)
        yscroll=ttk.Scrollbar(frameright,orient=VERTICAL)

        style=ttk.Style(frameright)
        style.theme_use('clam')
        style.configure('Treeview',foreground='black',background='sky blue',fieldbackground='sky blue')
        style.map('Treeview',background=[('selected','#1A8F2D')])

        cols = ('Staff_ID','Date','Staff Name','Gender','Address','Email_ID','Contact_No.',"Salary")
        library_table = ttk.Treeview(frameright, columns=cols, show='headings', xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    
        xscroll.pack(side=BOTTOM,fill=X)
        yscroll.pack(side=RIGHT,fill=Y)

        xscroll.config(command=library_table.xview)
        yscroll.config(command=library_table.yview)

        library_table['show']='headings'
        library_table.pack(fill=BOTH,expand=1)

        def adjust_column_widths():
            for i, col in enumerate(cols):
                max_width = 0
                for row in library_table.get_children(''):
                    cell_text = library_table.item(row, 'values')[i]
                    max_width = max(max_width, len(str(cell_text)))
                library_table.column(col, width=max_width * 5)  
        

        for col in cols:
            library_table.heading(col, text=col, anchor='center')  # Center the column headings
            library_table.column(col, width=150, anchor='center')  # Center the column content
            library_table.pack(fill=BOTH, expand=1)

        #======================================Labels=========================================================
         #search by id
        IDEntry1=Entry(staff,font=('Italic',15,'bold'),fg='Black',width=10)
        IDEntry1.place(x=200,y=100)  

        #staff ID
        ID = Label(frameleft, text = 'Staff ID', font = ('Times 15 italic bold'), fg='Black', bg = 'sky blue')
        ID.place(x=80, y=50)
        self.IDEntry = Entry (frameleft, textvariable = ID_var, font = ('Times 13 italic bold'), fg = 'Black')
        self.IDEntry.place(x=250, y=50)
        validate_id = staff.register(staff_ID)
        self.IDEntry.config(validate='key', validatecommand = (validate_id,'%S'))

        #staff name
        Name = Label(frameleft, text = 'Name', font = ('Times 15 italic bold') ,fg = 'Black', bg = 'sky blue')
        Name.place(x = 80, y = 100)
        self.NameEntry = Entry(frameleft, textvariable = name_var, font = ('Times 13 italic bold'), fg = 'Black')
        self.NameEntry.place(x=250,y=100)
        
        #gender
        gender=Label(frameleft,text='Gender',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        gender.place(x=80,y=150)
        n = tk.StringVar() 
        self.genderchoosen = ttk.Combobox(frameleft, textvariable = n, font = ('Times 12 italic bold')) 
        self.genderchoosen['values'] = (' Male', ' Female' )
        self.genderchoosen.place(x=250,y=150)

        #address
        Address=Label(frameleft,text='Address',font=('Times 15 italic bold') ,fg='Black',bg='sky blue')
        Address.place(x=80,y=200)
        self.AddressEntry=Entry(frameleft,textvariable=address_var,font=('Times 13 italic bold'),fg='Black')
        self.AddressEntry.place(x=250,y=200)

        #email
        Email=Label(frameleft,text='Email ID',font=('Times 15 italic bold') ,fg='Black',bg='sky blue')
        Email.place(x=500,y=50)
        self.EmailEntry=Entry(frameleft,textvariable=Email_var,font=('Times 13 italic bold'),fg='Black')
        self.EmailEntry.place(x=700,y=50)   
        
        #contact
        cont=Label(frameleft,text='Contact Number',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        cont.place(x=500,y=100)
        self.contEntry=Entry(frameleft,textvariable=contact_var,font=('Times 13 italic bold'),fg='Black')
        self.contEntry.place(x=700,y=100)
    
        #selary
        salary=Label(frameleft,text='Salary',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        salary.place(x=500,y=150)
        self.salaryEntry=Entry(frameleft,textvariable=salary_var,font=('Times 13 italic bold'),fg='Black')
        validate_salary=staff.register(staff_salary)
        self.salaryEntry.place(x=700,y=150)
        self.salaryEntry.config(validate='key',validatecommand=(validate_salary,'%S'))

        #date
        date=Label(frameleft,text='Date',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        date.place(x=500,y=200)
        self.dateEntry=DateEntry(frameleft,selectmode='day',textvariable=date_var, width=18, font = ('Times 13 italic bold'))
        self.dateEntry.place(x=700,y=200)

        #currentDate 
        date_label = tk.Label(staff, text="", fg="white", bg= "#06283D", font=("Helvetica", 16))
        date_label.place(x=400,y=100)
        
        #currentTime
        time_label = tk.Label(staff, text="", bg= "#06283D", fg="white", font=("Helvetica", 16))
        time_label.place(x=800,y=100)
        
        up=Image.open("loginicon.png")
        up=up.resize((190,180),Image.ADAPTIVE)
        self.photo_imgup=ImageTk.PhotoImage(up)
        label = tk.Label(staff,image=self.photo_imgup, bd=5, relief= RIDGE, bg="sky blue")
        label.place(x=1190,y=120,width=200,height=180)

        #====================================Buttons=====================================
        search=Image.open("search.png")
        search=search.resize((50,50),Image.ADAPTIVE)
        self.photo_img1=ImageTk.PhotoImage(search)
        lbimg1=Button(staff,command = searchf,image=self.photo_img1,bg="#06283D",borderwidth=0,cursor="hand2", activebackground="#06283D")
        lbimg1.place(x=330,y=90,width=50,height=50)

        back=Image.open("back2.png")
        back=back.resize((60,60),Image.ADAPTIVE)
        self.photo_img2=ImageTk.PhotoImage(back)
        back1=Button(staff,command=staff_window,image=self.photo_img2,borderwidth=0,cursor="hand2",bg="#06283D",activebackground="#06283D")
        back1.place(x=10,y=0,width=100,height=100)


        button=Button(staff,text='Upload',command=upload_photo,font=('Times 15 italic bold'),fg='white',bg="green",
                  activebackground="green",activeforeground="#EDEDED",bd=4,cursor="hand2",width=15)
        button.place(x=1200,y=325)

        button=Button(staff,command=add_entry,text='Add',font=('Times 15 italic bold'),fg='white',bg="green",
                  activebackground="green",activeforeground="#EDEDED",bd=4,cursor="hand2",width=15)
        button.place(x=1200,y=405)

        button=Button(staff,command=Save,text='Save',font=('Times 15 italic bold'),fg='white',bg="green",
                  activebackground="green",activeforeground="#EDEDED",bd=4,cursor="hand2",width=15)
        button.place(x=1200,y=485)

        button=Button(staff,command=delete,text='Delete',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="#EDEDED",bd=4,cursor="hand2",width=15)
        button.place(x=1200,y=565)

        button=Button(staff,command=update,text='Update',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="#EDEDED",bd=4,cursor="hand2",width=15)
        button.place(x=1200,y=645)

        button=Button(staff,text='Clear',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="#EDEDED",bd=4,command=Clear_button,cursor="hand2",width=15)
        button.place(x=1200,y=725)

        
        update_date()
        update_time()
        show()
        library_table.bind('<Double-Button-1>')
        adjust_column_widths()
        try:
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect to MySQL: {err}")

if __name__ == "__main__":
    staff=Tk()
    obj=staff_form(staff)
    staff.mainloop()