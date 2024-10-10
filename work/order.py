from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from tkcalendar import DateEntry
import mysql.connector
from reportlab.lib.pagesizes import A5
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as PILImage 
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
import io

class Order:
    def __init__(self, order1):
        self.order1 = order1
        self.order1.title("Library Management System")
        self.order1.geometry("1500x800+0+0")
        self.order1.resizable(0, 0)
        self.order1.config(bg="#06283D")
        
        oid_var=StringVar()
        date_var=StringVar()
        book_var=StringVar()
        vender_var=StringVar()
        amt_var=StringVar()
        no_var=StringVar()
        total_var=StringVar()    
             
        def update_time():
            current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
            time_label.config(text="Current Time: " + current_time)
            order1.after(1000, update_time)  # Update time every 1 second

        def update_date():
            today_date = datetime.now().strftime("%Y-%m-%d")
            date_label.config(text="Today's Date: " + today_date)
        #================validation====================================
        def order_ID(id):
            if id.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False
        def b_amt(AMT):
            if AMT.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False
        def no_book(N):
            if N.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False
            
        def update_sum():
            try:
                total_var.set((int(amt_var.get().replace(' ', '')) * int(no_var.get().replace(' ', ''))))
            except:
                pass

            self.order1.after(1000, update_sum)  # reschedule the event
            return
        
        #===========================Functions=====================================
        def order_window():
            self.order1.destroy()
            from MDI import mdi_form
            order_window = Tk()
            order_instance = mdi_form(order_window)

        #========================Heading===================================
        lbtitle=Label(self.order1,text='Order Details',fg='white',bg='#06283D',font=('Times 50 italic bold'))
        lbtitle.place(x=580,y=10)

        #==========================database=========================================
        def generate_id():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()  
            mycursor.execute("SELECT MAX(Id) FROM order1")
            max_id = mycursor.fetchone()[0]
            mycursor.close()
            return max_id + 1 if max_id else 1

        def add_entry():
            new_id = generate_id()
            IDEntry.config(state="normal")
            IDEntry.delete(0, END)
            IDEntry.insert(0, new_id)
            mysqldb.close()

        def searchf():
            search = IDEntry1.get()
            try:
                mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
                mycursor=mysqldb.cursor()   
                mycursor.execute("SELECT * FROM order1 WHERE Id = %s", (search,))
                row = mycursor.fetchone()
                if row:
                    id1, date1, b_name, vd1, amt1, qnt1, total1 = row
                    IDEntry.delete(0, END)
                    IDEntry.insert(END, id1)
                    dateEntry.delete(0, END)
                    dateEntry.insert(END, date1)
                    NameEntry.delete(0, END)
                    NameEntry.insert(END, b_name)
                    vd_entry.delete(0, END)
                    vd_entry.insert(END, vd1)
                    amtEntry.delete(0, END)
                    amtEntry.insert(END, amt1)
                    qntyentry.delete(0, END)
                    qntyentry.insert(END, qnt1)
                    totalentry.delete(0, END)
                    totalentry.insert(END, total1)            
                else:
                    messagebox.showinfo("Not Found", f"No record found with ID: {search}")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error searching record: {err}")
            finally:
                mysqldb.commit()

        def Save():
            try:
                id1 = IDEntry.get()
                date1 = dateEntry.get()
                b_name = NameEntry.get()
                vd1 = vd_entry.get()
                amt1 = amtEntry.get()
                qnt1 = qntyentry.get()
                total1 = totalentry.get()
                mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
                mycursor=mysqldb.cursor()   
                sql = "INSERT INTO order1(Id, Date, order_name, vender_name, amount, qnt, total) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (id1, date1, b_name, vd1, amt1, qnt1, total1)
                mycursor.execute(sql, val)
                mycursor.execute("UPDATE stock SET stock = stock + %s WHERE b_name = %s", (qnt1, b_name))
                messagebox.showinfo("Success", f"{qnt1} {b_name}(s) added to stock.")        
                messagebox.showinfo("information", "Record inserted successfully...")
                Clear_button()
                mysqldb.commit()
                fetch_data()             
            except Exception as e:
                print(e)
                mysqldb.commit()
                fetch_data()
                mysqldb.close()      
        
        def update():
            id1 = IDEntry.get()
            date1 = dateEntry.get()
            b_name = NameEntry.get()
            vd1 = vd_entry.get()
            amt1 = amtEntry.get()
            qnt1 = qntyentry.get()
            total1 = totalentry.get()
            if id1:
                mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
                mycursor=mysqldb.cursor()   
                mycursor.execute("SELECT * FROM order1 WHERE Id = %s", (id1,))
                row = mycursor.fetchone()
                if row:
                    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update this record?")
                    if confirm:
                        mycursor.execute("Update  order1 set Date= %s,order_name= %s,vender_name= %s,amount= %s,qnt= %s,total= %s where Id= %s", 
                                 (date1, b_name, vd1, amt1, qnt1, total1, id1))
                        messagebox.showinfo("information", "Record update successfully...")
                        mysqldb.commit()
                        fetch_data()
                else:
                    messagebox.showinfo("Error", "No data found in the database for the given ID")
            else:
                messagebox.showinfo("Error", "Please enter an ID to update")        

        def delete():
            id1 = IDEntry.get()
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
            if id1:
                confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
                if confirm:
                    mycursor.execute("DELETE FROM order1 WHERE id = %s", (id1,))
                    mysqldb.commit()
            else:
                messagebox.showinfo("Error", "Please enter an ID to delete")
            fetch_data()            
              
        def Clear_button():
            IDEntry.delete(0, END)
            dateEntry.delete(0, END)
            NameEntry.delete(0, END)
            vd_entry.delete(0, END)
            amtEntry.delete(0, END)
            qntyentry.delete(0, END)
            totalentry.delete(0, END)
        
        def show():
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
            mycursor.execute("SELECT * FROM order1")
            records = mycursor.fetchall()

            for i, (id1, date1, b_name, vd1, amt1, qnt1, total1) in enumerate(records, start=1):
                library_table.insert("", "end", values=(id1, date1, b_name, vd1, amt1, qnt1, total1))
                mysqldb.close()        

        def fetch_data():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()  
            mycursor.execute("select * from order1")
            rows=mycursor.fetchall()
            if len(rows)!=0:
                library_table.delete(*library_table.get_children())
                for i in rows:
                    library_table.insert("",END,values=i)
                mysqldb.commit()
            mysqldb.close()   

        def pdf_report():
            Rep_ID = IDEntry.get()
            if Rep_ID:
                db = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
                cursor = db.cursor()
                query = "SELECT * FROM order1 WHERE id=%s"
                cursor.execute(query, (Rep_ID,))
                order_data = cursor.fetchone()

                if order_data:
                    doc = SimpleDocTemplate("orderreport2.pdf", pagesize=A5)
                    styles = getSampleStyleSheet()
                    style_normal = styles['Normal']

                    current_time = datetime.now().strftime("%Y-%m-%d  %H:%M:%S %p")
                    time_text = Paragraph(f"Report generated on: {current_time}", styles['Normal'])
                    time_text.hAlign = 'LEFT'
                    title = Paragraph("Order Report", styles['Title'])

                    # Write data directly onto the document with colors
                    report_text = ""
                    for label, value in zip(['ID', 'Date', 'Name', 'Vendor Name', 'Amount', 'Quantity', 'Total'], order_data):
                        report_text += f"<font color='{colors.brown}'><b>{label} : </b></font>&nbsp;&nbsp;<font color='{colors.blueviolet}'> {value}</font><br/><br/>"
                    report_paragraph = Paragraph(report_text, styles['Normal'])

                    image_path = "bkimg.png"
                    logo = PILImage(image_path, width=80, height=60)
                    logo.hAlign = 'CENTER'

                    # Build the PDF
                    elements = [logo, Spacer(1, 1), title, Spacer(1, 1), time_text, Spacer(1, 12), report_paragraph]
                    doc.build(elements)

                    print("PDF report generated successfully.")
                    os.startfile("orderreport2.pdf")
                else:
                    messagebox.showinfo('Error', 'No data found in the database')
            else:
                return
  

        def show_price(event):
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
            selected_book = NameEntry.get()
            mycursor.execute("SELECT amt FROM stock WHERE b_name=%s", (selected_book,))
            result = mycursor.fetchone()
            if result:
                price = result[0]
                amtEntry.delete(0, tk.END)
                amtEntry.insert(tk.END, str(price))
            else:
                amtEntry.delete(0, tk.END)
                amtEntry.insert(tk.END, "Book not found")  
            mysqldb.close()                       
        #=======================================frame==========================================================        
        frameleft=LabelFrame(self.order1,bg='sky blue',bd=10,relief=RIDGE,text="Order Details", font=('Times 15 italic bold'))
        frameleft.place(x=100,y=140,height=300,width=1000)

        frameright=LabelFrame(self.order1,bg='sky blue',bd=10,relief=RIDGE,text="Store Records", font=('Times 15 italic bold'))
        frameright.place(x=100,y=480,height=300,width=1000)
        #======================================data table====================================================           
        #scrollbar and columns   
        xscroll=ttk.Scrollbar(frameright,orient=HORIZONTAL)
        yscroll=ttk.Scrollbar(frameright,orient=VERTICAL)

        style=ttk.Style(frameright)
        style.theme_use('clam')
        style.configure('Treeview',foreground='black',background='sky blue',fieldbackground='sky blue')
        style.map('Treeview',background=[('selected','#1A8F2D')])

        cols = ('ID','Date','Name','Vender Name','Amount','Quantity','Total')
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
            library_table.column(col, width=120, anchor='center')  # Center the column content
            library_table.pack(fill=BOTH, expand=1)
        #======================================Labels=========================================================
         #search by id
        IDEntry1=Entry(order1,font=('Italic',15,'bold'),fg='Black',width=10)
        IDEntry1.place(x=200,y=100)  

        #order_id
        ID=Label(frameleft,text='Order ID',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        ID.place(x=50,y=50)
        IDEntry=Entry(frameleft,font=('Times 13 italic bold'),textvariable=oid_var ,fg='Black')
        IDEntry.place(x=250,y=50)
        validate_id=order1.register(order_ID)
        IDEntry.config(validate='key',validatecommand=(validate_id,'%S'))

        #date
        Date=Label(frameleft,text='Date',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        Date.place(x=50,y=100)
        dateEntry=DateEntry(frameleft,textvariable=date_var,selectmode='day',font=('Times 13 italic bold'),width=18)
        dateEntry.place(x=250,y=100)

        #book_name
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT b_name FROM stock")
        options=mycursor.fetchall()
        Name=Label(frameleft,text='Name Of Book',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        Name.place(x=50,y=150)
        NameEntry=ttk.Combobox(frameleft,textvariable=book_var,values=options,font=('Times 13 italic bold'),width=18)
        NameEntry.place(x=250,y=150)
    
        #vender_name
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT vname FROM vendor")
        options=mycursor.fetchall()
        v_name=Label(frameleft,text='Vendor Name',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        v_name.place(x=50,y=200)
        vd_entry=ttk.Combobox(frameleft,textvariable=vender_var,values=options,font=('Times 13 italic bold'),width=18)
        vd_entry.place(x=250,y=200)
        
        #amount of book
        amount=Label(frameleft,text='Amount Of Book',font=('Times 15 italic bold') ,fg='Black',bg='sky blue')
        amount.place(x=550,y=50)
        amtEntry=Entry(frameleft,textvariable=amt_var,font=('Times 13 italic bold'),fg='Black')
        amtEntry.place(x=750,y=50)
        validate_amt=order1.register(b_amt)
        amtEntry.config(validate='key',validatecommand=(validate_amt,'%S'))

        #number of books
        qnt=Label(frameleft,text='Number Of Books',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        qnt.place(x=550,y=100)
        qntyentry=Entry(frameleft,textvariable=no_var,font=('Times 13 italic bold'),fg='Black')
        qntyentry.place(x=750,y=100)
        validate_qnt=order1.register(no_book)
        qntyentry.config(validate='key',validatecommand=(validate_qnt,'%S'))

        #total amount
        total=Label(frameleft,text='Total Bill',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        total.place(x=550,y=150)
        totalentry=Entry(frameleft,textvariable=total_var,font=('Times 13 italic bold') ,fg='Black')
        totalentry.place(x=750,y=150)
        validate_total=order1.register(update_sum)
        totalentry.config(validate='key',validatecommand=(validate_total,'%S'))
        
        #currentDate 
        date_label = tk.Label(order1, text="", fg="white", bg= "#06283D", font=("Helvetica", 16))
        date_label.place(x=400,y=100)
        
        #currentTime
        time_label = tk.Label(order1, text="", bg= "#06283D", fg="white", font=("Helvetica", 16))
        time_label.place(x=800,y=100)
        
        up=Image.open("vender2.png")
        up=up.resize((190,190),Image.ADAPTIVE)
        self.photo_imgup=ImageTk.PhotoImage(up)
        label = tk.Label(order1,image=self.photo_imgup, bd=5, relief= RIDGE, bg="sky blue")
        label.place(x=1190,y=120,width=200,height=180)

        #====================================Buttons=====================================
        search=Image.open("search.png")
        search=search.resize((50,50),Image.ADAPTIVE)
        self.photo_img1=ImageTk.PhotoImage(search)
        lbimg1=Button(order1,command = searchf,image=self.photo_img1,bg="#06283D",borderwidth=0,cursor="hand2", activebackground="#06283D")
        lbimg1.place(x=330,y=90,width=50,height=50)

        back=Image.open("back2.png")
        back=back.resize((60,60),Image.ADAPTIVE)
        self.photo_img2=ImageTk.PhotoImage(back)
        back1=Button(order1,command=order_window,image=self.photo_img2,borderwidth=0,cursor="hand2",bg="#06283D",activebackground="#06283D")
        back1.place(x=10,y=0,width=100,height=100)

        button=Button(order1,text='Print', command= pdf_report,font=('Times 15 italic bold'),fg='white',bg="green",
                  activebackground="green",activeforeground="#EDEDED",bd=5,relief=RAISED,cursor="hand2",width=15)
        button.place(x=1200,y=325)

        button=Button(order1,command=add_entry,text='Add',font=('Times 15 italic bold'),fg='white',bg="green",
                  activebackground="green",activeforeground="#EDEDED",bd=5,relief=RAISED,cursor="hand2",width=15)
        button.place(x=1200,y=405)

        button=Button(order1,command=Save,text='Save',font=('Times 15 italic bold'),fg='white',bg="green",
                  activebackground="green",activeforeground="#EDEDED",bd=5,relief=RAISED,cursor="hand2",width=15)
        button.place(x=1200,y=485)

        button=Button(order1,command=delete,text='Delete',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="#EDEDED",bd=5,relief=RAISED,cursor="hand2",width=15)
        button.place(x=1200,y=565)

        button=Button(order1,command=update,text='Update',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="#EDEDED",bd=5,relief=RAISED,cursor="hand2",width=15)
        button.place(x=1200,y=645)

        button=Button(order1,text='Clear',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="#EDEDED",bd=5,relief=RAISED,command=Clear_button,cursor="hand2",width=15)
        button.place(x=1200,y=725)

        self.order1.after(1000, update_sum)

        update_date()
        update_time()
        show()  
        adjust_column_widths()

        library_table.bind('<Double-Button-1>')
        NameEntry.bind("<Return>", show_price)
        try:
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect to MySQL: {err}")

if __name__ == "__main__":
    order1=Tk()
    obj=Order(order1)
    order1.mainloop()