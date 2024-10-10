from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime
import re

class Vendor:
    def __init__(self,vend) :
        self.vend = vend
        self.vend.title("Staff")
        self.vend.geometry('1500x1500')
        self.vend.config(bg="#06283D")
        self.vend.resizable(0,0)
        
        #DATABASE CONNECTION
        mysqldb = mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
        mycursor = mysqldb.cursor()

        #==================Functions=====================================

        def MDI_window():
            self.vend.destroy()
            from MDI import mdi_form
            Vendor_window = Tk()
            Vendor_instance = mdi_form(Vendor_window)

        def update_time():
            current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
            time_label.config(text="Current Time: " + current_time)
            vend.after(1000, update_time)  # Update time every 1 second

        def update_date():
            today_date = datetime.now().strftime("%Y-%m-%d")
            date_label.config(text="Today's Date: " + today_date)     

        #================validation====================================
        def id(id):
            if id.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False
            
        def AC(AC):
            if AC.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False   
        def v_payment(pay):
            if pay.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False
            
        #==================================database=======================================
        def generate_id():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            cursor = mysqldb.cursor()
            cursor.execute("SELECT MAX(Id) FROM vendor")
            max_id = cursor.fetchone()[0]
            cursor.close()
            return max_id + 1 if max_id else 1
            

        def add_entry():
            new_id = generate_id()
            IDEntry.config(state="normal")
            IDEntry.delete(0, END)
            IDEntry.insert(0, new_id)
            IDEntry.focus_set()

        
        
        def searchf():
            search = IDEntry1.get()
            try:
                mysqldb = mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
                mycursor = mysqldb.cursor()
                mycursor.execute("SELECT * FROM vendor WHERE Id = %s", (search,))
                row = mycursor.fetchone()
                if row:
                    id1, v_name, adddress, v_email, cont, ac, pay, dt = row
                    IDEntry.delete(0, END)
                    IDEntry.insert(END, id1)
                    NameEntry.delete(0, END)
                    NameEntry.insert(END, v_name)
                    AddressEntry.delete(0, END)
                    AddressEntry.insert(END, adddress)
                    EmailEntry.delete(0, END)
                    EmailEntry.insert(END, v_email)
                    MobEntry.delete(0, END)
                    MobEntry.insert(END, cont)
                    acEntry.delete(0, END)
                    acEntry.insert(END, ac)
                    paymentEntry.delete(0, END)
                    paymentEntry.insert(END, pay)
                    dateEntry.delete(0, END)
                    dateEntry.insert(END, dt)
                    
                else:
                    messagebox.showinfo("Not Found", f"No record found with ID: {search}")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error searching record: {err}")
            finally:
                mysqldb.commit()       

        
        def Save():
            
            id1=IDEntry.get()
            v_name = NameEntry.get()
            adddress = AddressEntry.get()
            v_email = EmailEntry.get()
            cont= MobEntry.get()
            ac=acEntry.get()
            pay=paymentEntry.get()
            dt=dateEntry.get()

            mysqldb = mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor = mysqldb.cursor()
            
            if not re.match(r'^[0-9]{10}$', cont):
                messagebox.showerror("Error", "Please enter a valid 10-digit contact number.")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v_email):
                messagebox.showerror("Error", "Please enter a valid email address.")
            elif IDEntry.get()=="" or NameEntry.get()==""  or AddressEntry.get()=="" or EmailEntry.get()=="" or MobEntry.get()=="" or acEntry.get()==""or paymentEntry.get()=="" or dateEntry.get()=="" :
               messagebox.showerror(title='Wrong ',message='Please enter all filds')
            else:
                mycursor.execute("INSERT INTO vendor(Id,vname,address,email,contact,account,Pay,date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                                 (id1,v_name,adddress,v_email,cont,ac,pay,dt))
                mysqldb.commit()
                fetch_data()
                messagebox.showinfo("Saved","Data inserted successfully")             

        
        def update():
            
            id1=IDEntry.get()
            v_name = NameEntry.get()
            adddress = AddressEntry.get()
            v_email = EmailEntry.get()
            cont= MobEntry.get()
            ac=acEntry.get()
            pay=paymentEntry.get()
            dt=dateEntry.get()
            mysqldb = mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor = mysqldb.cursor()
            if id1:
                mycursor.execute("SELECT * FROM vendor WHERE Id = %s", (id1,))
                row = mycursor.fetchone()
                if row:
                    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update this record?")
                    if confirm:
                       
                        mycursor.execute("Update  vendor set vname= %s,address= %s,email= %s,contact= %s,account= %s,Pay= %s,date= %s where Id=%s"
                                             , (v_name,adddress,v_email,cont,ac,pay,dt,id1))
                        mysqldb.commit()
                        messagebox.showinfo("Update","Data updated successfully")
                        fetch_data()
                else:
                    messagebox.showinfo("Error", "No data found in the database for the given ID")
            else:
                messagebox.showinfo("Error", "Please enter an ID to update")       

        
        def delete():
            id_val = IDEntry.get()
            mysqldb = mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor = mysqldb.cursor()
            if id_val:
                confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
                if confirm:
                    mycursor.execute("DELETE FROM vendor WHERE Id = %s", (id_val,))
                    mysqldb.commit()
                    fetch_data()
                    messagebox.showinfo("Delete","Data deleted successfully")
            else:
                messagebox.showinfo("Error", "Please enter an ID to delete")        
                      

        def Clear():
            IDEntry.delete(0, END)
            NameEntry.delete(0, END)
            AddressEntry.delete(0, END)
            EmailEntry.delete(0, END)
            MobEntry.delete(0, END)
            acEntry.delete(0, END)
            paymentEntry.delete(0, END)
            dateEntry.delete(0, END) 
                 

        def show():
            mysqldb = mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor = mysqldb.cursor()
            mycursor.execute("SELECT * FROM vendor")
            records = mycursor.fetchall()

            for i, (id1,v_name ,adddress, v_email,cont,ac,pay,date) in enumerate(records, start=1):
                library_table.insert("", "end", values=(id1,v_name ,adddress, v_email,cont,ac,pay,date))
                mysqldb.close()

        def fetch_data():
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
            mycursor.execute("select * from vendor")
            rows=mycursor.fetchall()
            if len(rows)!=0:
                library_table.delete(*library_table.get_children())
                for i in rows:
                    library_table.insert("",END,values=i)
                mysqldb.commit()
            mysqldb.close()     
    
        #================veriables============================================    
        id_var = StringVar()
        Name_var = StringVar()
        Address_var = StringVar()
        Email_var = StringVar()
        Mob_var = StringVar()
        account_var = StringVar()
        payment_var = StringVar()
        date_var = StringVar()

        #========================Heading===================================
        lbtitle=Label(self.vend, text='Vendor Details',fg='white',bg='#06283D',font=('Times 50 italic bold'))
        lbtitle.place(x=580,y=10)
        #=======================================frame==========================================================

        frameleft = LabelFrame(self.vend, bg='sky blue', bd=10, relief=RIDGE,text="Vendor Details", font=('Times 15 italic bold'))
        frameleft.place(x=100,y=150,height=300,width=1000)

        frameright = LabelFrame(self.vend, bg='sky blue', bd=10, relief=RIDGE,text="Store Records", font=('Times 15 italic bold'))
        frameright.place(x=100,y=480,height=300,width=1000)

        #======================================data table====================================================

        xscroll = ttk.Scrollbar(frameright,orient=HORIZONTAL)
        yscroll = ttk.Scrollbar(frameright,orient=VERTICAL)

        style = ttk.Style(frameright)
        style.theme_use('clam')
        style.configure('Treeview',foreground='black',background='sky blue',fieldbackground='sky blue')
        style.map('Treeview',background=[('selected','black')])
        cols = ('Id','Vendor Name','Address','Email ID','Contact','Account No.','Payments','Date')
        library_table = ttk.Treeview(frameright, columns = cols, xscrollcommand = xscroll.set, yscrollcommand = yscroll.set)

        xscroll.pack(side = BOTTOM, fill = X)
        yscroll.pack(side = RIGHT, fill = Y)
        xscroll.config(command = library_table.xview)
        yscroll.config(command = library_table.yview)
        library_table['show'] ='headings'
        library_table.pack(fill = BOTH, expand = 1)

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
        #======================================Labels=======================================================
        #search by id
        IDEntry1=Entry(vend,font=('Times 15 italic bold'),fg='Black',width=10)
        validate_id=vend.register(id)
        IDEntry1.config(validate='key',validatecommand=(validate_id,'%S'))
        IDEntry1.place(x=200,y=100) 
    

        ID = Label(frameleft, text = 'Vendor ID', font = ('Times 15 italic bold'), fg = 'Black', bg = 'sky blue')
        ID.place(x = 80, y = 50)
        IDEntry = Entry(frameleft, textvariable = id_var, font = ('Times 13 italic bold'),fg = 'Black')
        IDEntry.place(x = 220, y = 50)
        validate_id = vend.register(id)
        IDEntry.config(validate = 'key', validatecommand = (validate_id,'%S'))


        Name = Label(frameleft, text = 'Name', font = ('Times 15 italic bold'),fg = 'Black', bg = 'sky blue')
        Name.place(x = 80, y = 100)
        NameEntry = Entry(frameleft, textvariable = Name_var, font = ('Times 13 italic bold'),fg = 'Black')
        NameEntry.place(x = 220, y = 100)

        Address = Label(frameleft, text = 'Address', font = ('Times 15 italic bold'), fg= 'Black', bg = 'sky blue')
        Address.place(x = 80, y = 150)
        AddressEntry = Entry(frameleft, textvariable=Address_var, font = ('Times 13 italic bold'), fg = 'Black')
        AddressEntry.place(x = 220, y = 150)

        Email=Label(frameleft,text='Email ID',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        Email.place(x=80,y=200)
        EmailEntry=Entry(frameleft,textvariable=Email_var,font=('Times 13 italic bold'),fg='Black')
        EmailEntry.place(x=220,y=200)

        Mob=Label(frameleft,text='Contact No.',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        Mob.place(x=550,y=50)
        MobEntry=Entry(frameleft,textvariable=Mob_var,font=('Times 13 italic bold') ,fg='Black')
        MobEntry.place(x=750,y=50)

        ac=Label(frameleft,text='Account No.',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        ac.place(x=550,y=100)
        acEntry=Entry(frameleft,textvariable=account_var,font=('Times 13 italic bold'),fg='Black')
        acEntry.place(x=750,y=100)
        validate_ac=vend.register(AC)
        acEntry.config(validate='key',validatecommand=(validate_ac,'%S'))

        payment=Label(frameleft,text='Payment',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        payment.place(x=550,y=150)
        paymentEntry=Entry(frameleft,textvariable=payment_var,font=('Times 13 italic bold'),fg='Black')
        paymentEntry.place(x=750,y=150)
        validate_payment=vend.register(v_payment)
        paymentEntry.config(validate='key',validatecommand=(validate_payment,'%S'))

        date=Label(frameleft,text='Date',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        date.place(x=550,y=200)
        dateEntry=DateEntry(frameleft,textvariable=date_var,font=('Times 13 italic bold'),fg='Black',width=18)
        dateEntry.place(x=750,y=200)

        #currentDate 
        date_label =Label(self.vend, text="", fg="white", bg= "#06283D", font=("Helvetica", 16))
        date_label.place(x=400,y=100)
        
        #currentTime
        time_label = Label(self.vend, text="", bg= "#06283D", fg="white", font=("Helvetica", 16))
        time_label.place(x=800,y=100)
        

        up=Image.open("vender.png")
        up=up.resize((150,150),Image.ADAPTIVE)
        self.photo_imgup=ImageTk.PhotoImage(up)
        label = Label(vend,image=self.photo_imgup, bd=5, bg= "sky blue", relief= RIDGE)
        label.place(x=1190,y=120,width=190,height=180)

        #====================================Buttons=====================================

        search=Image.open("search.png")
        search=search.resize((60,60),Image.ADAPTIVE)
        self.photo_img1=ImageTk.PhotoImage(search)
        lbimg1=Button(vend,command=searchf,image=self.photo_img1,bg="#06283D",borderwidth=0,cursor="hand2", activebackground="#06283D")
        lbimg1.place(x=330,y=90,width=50,height=50)

        back=Image.open("back2.png")
        back=back.resize((60,60),Image.ADAPTIVE)
        self.photo_img2=ImageTk.PhotoImage(back)
        back1=Button(vend,command=MDI_window,image=self.photo_img2,borderwidth=0,cursor="hand2",bg="#06283D",activebackground="#06283D")
        back1.place(x=10,y=0,width=100,height=100)

        button=Button(vend,text='Add',command= add_entry,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=350)

        button=Button(vend,text='Save',command= Save,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=440)

        button=Button(vend,text='Delete',command= delete,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=530)

        button=Button(vend,text='Update',command= update,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,cursor="hand2",width=15)
        button.place(x=1200,y=620)

        button=Button(vend,text='Clear',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=2,command= Clear,cursor="hand2",width=15)
        button.place(x=1200,y=710)
        
        #====================================some functions call here================================
        library_table.bind('<Double-Button-1>')
        adjust_column_widths()
        update_date()
        update_time()
        show()
        
       
if __name__ == "__main__":
    vend=Tk()
    obj=Vendor(vend)
    vend.mainloop()

