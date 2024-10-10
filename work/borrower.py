from tkinter import*
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from tkinter import filedialog
import re
import io


class borrower_form:
    def __init__(self, borrower):
        self.borrower = borrower
        self.borrower.title("Borrower Details")
        self.borrower.geometry("1500x800+0+0")
        self.borrower.config(bg="#06283D")
        self.borrower.resizable(0,0)

        #==================MDI connection====================================

        def MDI_window():
            self.borrower.destroy()
            from MDI import mdi_form
            borrower_window = Tk()
            borrower_instance = mdi_form(borrower_window)

        def update_time():
            current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
            time_label.config(text="Current Time: " + current_time)
            borrower.after(1000, update_time)  # Update time every 1 second

        def update_date():
            today_date = datetime.now().strftime("%Y-%m-%d")
            date_label.config(text="Today's Date: " + today_date)     

        def calculate_penalty(event=None):
            try:
                issue = issueEntry.get_date()
                return_date = returnEntry.get_date()
        
                due_date = issue + timedelta(days=20)  # Example: Due date was 10 days after the issue date
                days_late = max(0, (return_date - due_date).days)  # Calculate days late, minimum 0
                penalty_amount = days_late * 1
        
                # Update penalty entry with the calculated amount
                penaltyEntry.delete(0, END)
                penaltyEntry.insert(END, f"${penalty_amount}")
            except ValueError:
                penaltyEntry.delete(0, END)
                penaltyEntry.insert(END, "Invalid date format")
                
        #========================validation============================================
        def borrower_ID(id):
            if id.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Only numbers can access')
                return False    
        
          
        #=====================veribles===================================    
        ID_var = StringVar()
        name_var = StringVar()
        address_var = StringVar()
        email_var = StringVar()
        mobno_var = StringVar()
        bname_var = StringVar()
        issuedate_var = StringVar()
        return_var = StringVar()
        penalty_var = StringVar()
        v1=IntVar()
        #========================Heading===================================
        lbtitle=Label(self.borrower, text='Borrower Details', fg='white', bg='#06283D', font=('times 50 italic bold'))
        lbtitle.pack(side=TOP,fill='x')
        
        #===================================database=======================================
        def generate_id():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            cursor = mysqldb.cursor()
            cursor.execute("SELECT MAX(br_id) FROM borrower")
            max_id = cursor.fetchone()[0]
            cursor.close()
            return max_id + 1 if max_id else 1
            
        def add_entry():
            new_id = generate_id()
            IDEntry.config(state="normal")
            IDEntry.delete(0, END)
            IDEntry.insert(0, new_id)
            mysqldb.close()

        def upload_photo():
            global resized_image
            filename = filedialog.askopenfilename(initialdir="/", title="Select Photo", filetypes=(("JPEG files", ".jpg"), ("PNG files", ".png"), ("All files", ".")))
            original_image = Image.open(filename)
            resized_image = original_image.resize((150, 150))
            resized_image.save("resized_photo.jpg") 
            display_image(resized_image)

        def image_to_byte_array(image):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        
        def display_image(img):
            global photo_tk
            photo_tk = ImageTk.PhotoImage(img)
            label.config(image=photo_tk)
            label.image = photo_tk        

        def searchf():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            search = IDEntry1.get()
            try:
                mycursor.execute("SELECT * FROM borrower where br_id = %s", (search,))
                row = mycursor.fetchone()
                if row:
                    br_id, b_name, gend, addr, e_mail, mobno, b_book, issu, ret, pen, photo_bytes = row
                    IDEntry.delete(0, END)
                    IDEntry.insert(END, br_id)
                    NameEntry.delete(0, END)
                    NameEntry.insert(END, b_name)
                    v1.delete(0, END)
                    v1.insert(END, gend)
                    AddressEntry.delete(0, END)
                    AddressEntry.insert(END, addr)
                    EmailEntry.delete(0, END)
                    EmailEntry.insert(END, e_mail)
                    MobEntry.delete(0, END)
                    MobEntry.insert(END, mobno)
                    borrow_bookEntry.delete(0, END)
                    borrow_bookEntry.insert(END, b_book)
                    issueEntry.delete(0, END)
                    issueEntry.insert(END, issu)
                    returnEntry.delete(0, END)
                    returnEntry.insert(END, ret)
                    penaltyEntry.delete(0, END)
                    penaltyEntry.insert(END, pen)
                    img = Image.open(io.BytesIO(photo_bytes))
                    img = img.resize((150, 150))
                    display_image(img)
                else:
                    messagebox.showinfo("Not Found", f"No record found with br_id: {search}")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error searching record: {err}")
            finally:
                mysqldb.commit()              

        def Save():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            global resized_image
            br_id = IDEntry.get()
            b_name = NameEntry.get()
            gend=v1.get()
            addr = AddressEntry.get()
            e_mail = EmailEntry.get()
            mobno = MobEntry.get()
            b_book = borrow_bookEntry.get()
            issu = issueEntry.get()
            ret = returnEntry.get()
            pen = penaltyEntry.get()
            if 'resized_image' not in globals():
                messagebox.showerror("Error", "No image uploaded")
                return
            photo_bytes = image_to_byte_array(resized_image)
            if not re.match(r'^[0-9]{10}$', mobno):
                messagebox.showerror("Error", "Please enter a valid 10-digit contact number.")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', e_mail):
                messagebox.showerror("Error", "Please enter a valid email address.")
            elif IDEntry.get()=="" or NameEntry.get()=="" or v1.get()=="" or AddressEntry.get()=="" or EmailEntry.get()=="" or MobEntry.get()=="" or borrow_bookEntry.get()==""or issueEntry.get()=="":
                messagebox.showerror(title='Wrong ',message='Please enter all filds')
            else:
                mycursor.execute("INSERT INTO  borrower(br_id,b_name,gend,addr,e_mail,mobno,b_book,issu,ret,pen,photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", 
                                 (br_id,b_name,gend,addr,e_mail,mobno,b_book,issu,ret,pen,photo_bytes))    
                mycursor.execute("UPDATE stock SET stock = stock - %s WHERE b_name = %s", ( 1,b_book,))
                messagebox.showinfo("Success", f" {b_book}(s) book is less from stock.")        
                mysqldb.commit()
                fetch_data()
                messagebox.showinfo("Saved","Data inserted successfully")  

        def update():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            global photo_bytes
            br_id= IDEntry.get()
            b_name = NameEntry.get()
            gend = v1.get()
            addr = AddressEntry.get()
            e_mail = EmailEntry.get()
            mobno = MobEntry.get()
            b_book = borrow_bookEntry.get()
            issu = issueEntry.get()
            ret = returnEntry.get()
            pen = penaltyEntry.get()
            if br_id:
                mycursor.execute("SELECT * FROM borrower WHERE br_id = %s", (br_id,))
                row = mycursor.fetchone()
                if row:
                    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update this record?")
                    if confirm:
                        photo_bytes = image_to_byte_array(resized_image)
                        img = Image.open(io.BytesIO(photo_bytes))
                        img = img.resize((150, 150))
                        display_image(img)
                        
                        mycursor.execute("Update  borrower set b_name= %s,gend= %s,addr= %s,e_mail= %s,mobno= %s,b_book= %s,issu= %s,ret= %s,pen= %s,photo= %s where br_id= %s"
                                             , (b_name,gend,addr,e_mail,mobno,b_book,issu,ret,pen,photo_bytes,br_id))
                        mysqldb.commit()
                        messagebox.showinfo("Update","Data updated successfully")
                        fetch_data()
                else:
                    messagebox.showinfo("Error", "No data found in the database for the given ID")
            else:
                messagebox.showinfo("Error", "Please enter an ID to update")         

        def delete():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            br_id = IDEntry.get()
            if br_id:
                confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
                if confirm:
                    mycursor.execute("Delete FROM borrower WHERE br_id = %s", (br_id,))
                    mysqldb.commit()
                    fetch_data()
                    messagebox.showinfo("Delete","Data deleted successfully")
            else:
                messagebox.showinfo("Error", "Please enter an ID to delete")  
        
        def Clear():
            IDEntry.delete(0, END)
            NameEntry.delete(0, END)
            v1.delete(0, END)
            AddressEntry.delete(0, END)
            EmailEntry.delete(0, END)
            MobEntry.delete(0, END)
            borrow_bookEntry.delete(0, END)
            issueEntry.delete(0, END)
            returnEntry.delete(0, END)
            penaltyEntry.delete(0, END)
            label.config(image="")
            resized_image = None  
        
        def show():
                mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
                mycursor = mysqldb.cursor()
                mycursor.execute("SELECT * FROM borrower")
                records = mycursor.fetchall()

                for i, (br_id,b_name,gend,addr,e_mail,mobno,b_book,issu,ret,pen,photo_bytes) in enumerate(records, start=1):
                    library_table.insert("", "end", values=(br_id,b_name,gend,addr,e_mail,mobno,b_book,issu,ret,pen,photo_bytes))
                    mysqldb.close()               

        def fetch_data():
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
            mycursor.execute("select * from borrower")
            rows=mycursor.fetchall()
            if len(rows)!=0:
                library_table.delete(*library_table.get_children())
                for i in rows:
                    library_table.insert("",END,values=i)
                mysqldb.commit()
            mysqldb.close()  
        #=======================================frame==========================================================

        frameleft = LabelFrame(self.borrower, bg='sky blue', bd=10, relief=RIDGE,text="Borrower Details", font=('Times 15 italic bold'))
        frameleft.place(x=100,y=150,height=300,width=1000)

        frameright = LabelFrame(self.borrower, bg='sky blue', bd=10, relief=RIDGE,text="Store Records", font=('Times 15 italic bold'))
        frameright.place(x=100,y=480,height=300,width=1000)


        #======================================data table====================================================

        xscroll=ttk.Scrollbar(frameright, orient=HORIZONTAL)
        yscroll=ttk.Scrollbar(frameright, orient=VERTICAL)

        style=ttk.Style(frameright)
        style.theme_use('clam')
        style.configure('Treeview', foreground='black', background='sky blue', fieldbackground='sky blue')
        style.map('Treeview', background=[('selected','#1A8F2D')])
        
        cols = ('ID', 'Name', 'Gender', 'Address', 'Email', 'Contact', 'Book Name', 'Issue Date', 'Return Date', 'Penalty')
        library_table = ttk.Treeview(frameright, columns=cols, show='headings', xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        

        xscroll.pack(side=BOTTOM,fill=X)
        yscroll.pack(side=RIGHT,fill=Y)

        xscroll.config(command=library_table.xview)
        yscroll.config(command=library_table.yview)

        def adjust_column_widths():
            for i, col in enumerate(cols):
                max_width = 0
                for row in library_table.get_children(''):
                    cell_text = library_table.item(row, 'values')[i]
                    max_width = max(max_width, len(str(cell_text)))
                library_table.column(col, width=max_width * 5)  
        

        for col in cols:
            library_table.heading(col, text=col, anchor='center')  # Center the column headings
            library_table.column(col, width=130, anchor='center')  # Center the column content
            library_table.pack(fill=BOTH, expand=1)
        #======================================Labels=========================================================
        #search by id
        IDEntry1=Entry(borrower,font=('times 15 italic bold'),fg='Black',width=10)
        validate_id=borrower.register(id)
        IDEntry1.config(validate='key',validatecommand=(validate_id,'%S'))
        IDEntry1.place(x=200,y=100)    

        ID=Label(frameleft,text=' ID',font=('times 15 italic bold')
               ,fg='Black',bg='sky blue')
        ID.place(x=100,y=10)
        IDEntry=Entry(frameleft,textvariable=ID_var,font=("times 13 italic bold"),fg='Black')
        validate_id = borrower.register(borrower_ID)
        IDEntry.config(validate ='key', validatecommand = (validate_id,'%S'))
        IDEntry.place(x=250,y=10)

        Name=Label(frameleft,text='Name',font=('times 15 italic bold'),fg='Black',bg='sky blue')
        Name.place(x=100,y=60)
        NameEntry=Entry(frameleft,textvariable=name_var,font=("times 13 italic bold"),fg='Black')
        NameEntry.place(x=250,y=60)
        
        gender=Label(frameleft,text='Gender',font=('times 15 italic bold') ,fg='Black',bg='sky blue')
        gender.place(x=100,y=110)
        n = StringVar() 
        v1 = ttk.Combobox(frameleft, textvariable = n ,font=('times 12 italic bold') ) 
        v1['values'] = (' Male', ' Female' )
        v1.place(x=250,y=110)

        Address=Label(frameleft,text='Address',font=('times 15 italic bold') ,fg='Black',bg='sky blue')
        Address.place(x=100,y=160)
        AddressEntry=Entry(frameleft,textvariable=address_var,font=("times 13 italic bold"),fg='Black')
        AddressEntry.place(x=250,y=160)

        Email=Label(frameleft,text='Email ID',font=('times 15 italic bold'),fg='Black',bg='sky blue')
        Email.place(x=100,y=210)
        EmailEntry=Entry(frameleft,textvariable=email_var,font=("times 13 italic bold")  ,fg='Black')
        EmailEntry.place(x=250,y=210)

        Mob=Label(frameleft,text='Mob no',font=('times 15 italic bold'),fg='Black',bg='sky blue')
        Mob.place(x=550,y=10)
        MobEntry=Entry(frameleft,textvariable=mobno_var,font=("times 13 italic bold") ,fg='Black')
        MobEntry.place(x=750,y=10)
        
        #book name
        mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
        c=mysqldb.cursor()
        c.execute("SELECT b_name FROM stock")
        options=c.fetchall()
        borrow_book=Label(frameleft,text='Book Name',font=('times 15 italic bold') ,fg='Black',bg='sky blue')
        borrow_book.place(x=550,y=60)
        borrow_bookEntry=ttk.Combobox(frameleft,textvariable=bname_var,values=options,width=18,font=("times 13 italic bold"))
        borrow_bookEntry.place(x=750,y=60)

        issue=Label(frameleft,text='Issue Date',font=('times 15 italic bold') ,fg='Black',bg='sky blue')
        issue.place(x=550,y=110)
        issueEntry=DateEntry(frameleft,textvariable=issuedate_var,selectmode='day',font=("times 13 italic bold"),fg='Black',width=18)
        issueEntry.bind("<<DateEntrySelected>>", calculate_penalty)
        issueEntry.place(x=750,y=110)

        retern=Label(frameleft,text='Return Date',font=('times 15 italic bold') ,fg='Black',bg='sky blue')
        retern.place(x=550,y=160)
        returnEntry=DateEntry(frameleft,textvariable=return_var,font=("times 13 italic bold"),fg='Black',width=18)
        returnEntry.bind("<<DateEntrySelected>>", calculate_penalty)
        returnEntry.place(x=750,y=160)

        penalty=Label(frameleft,text='Penalty',font=('times 15 italic bold') ,fg='Black',bg='sky blue')
        penalty.place(x=550,y=210)
        penaltyEntry=Entry(frameleft,textvariable=penalty_var,font=("times 13 italic bold") ,fg='Black')
        validate_pen = borrower.register(calculate_penalty )
        IDEntry.config(validate ='key', validatecommand = (validate_pen,'%S'))
        penaltyEntry.place(x=750,y=210)

        #currentDate 
        date_label =Label(self.borrower, text="", fg="white", bg= "#06283D", font=("Helvetica", 16))
        date_label.place(x=400,y=100)
        
        #currentTime
        time_label = Label(self.borrower, text="", bg= "#06283D", fg="white", font=("Helvetica", 16))
        time_label.place(x=800,y=100)

        up=Image.open("loginicon.png")
        up=up.resize((170,170),Image.ADAPTIVE)
        self.photo_imgup=ImageTk.PhotoImage(up)
        label = Label(borrower,image=self.photo_imgup,bd=5, relief= RIDGE, bg= "sky blue")
        label.place(x=1190,y=120,width=180,height=180)
        
        #====================================Buttons=====================================

        search=Image.open("search.png")
        search=search.resize((60,60),Image.ADAPTIVE)
        self.photo_img1=ImageTk.PhotoImage(search)
        lbimg1=Button(borrower,command=searchf,image=self.photo_img1,bg="#06283D",borderwidth=0,cursor="hand2", activebackground="#06283D")
        lbimg1.place(x=330,y=90,width=50,height=50)

        back=Image.open("back2.png")
        back=back.resize((60,60),Image.ADAPTIVE)
        self.photo_img2=ImageTk.PhotoImage(back)
        back1=Button(borrower,command=MDI_window,image=self.photo_img2,borderwidth=0,cursor="hand2",bg="#06283D",activebackground="#06283D")
        back1.place(x=10,y=0,width=100,height=100)


        button=Button(borrower,text='Upload', command=upload_photo,font=('Times 15 italic bold'),fg='white',bg="green",
                  activebackground="green",activeforeground="#EDEDED",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=325)

        button=Button(borrower,text='Add',command= add_entry,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=405)

        button=Button(borrower,text='Save',command= Save,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=485)

        button=Button(borrower,text='Delete',command= delete,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=565)

        button=Button(borrower,text='Update',command= update,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=645)

        button=Button(borrower,text='Clear',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,command= Clear,cursor="hand2",width=15)
        button.place(x=1200,y=725)
        
        #==== SQL connection ====
        try:
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect to MySQL: {err}")
        
        #==== some functions call here=========
        library_table.bind('<Double-Button-1>')
        adjust_column_widths()
        update_date()
        update_time()        
        show()


if __name__ == "__main__" :
    borrower = Tk()
    obj = borrower_form(borrower)
    borrower.mainloop()



























