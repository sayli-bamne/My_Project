from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image as RLImage
import os


class stock_form():
    def __init__(self,stock):
        self.stock=stock
        self.stock.title("Staff Form")
        self.stock.geometry("1500x1500")
        self.stock.config(bg="#06283D")

        ID_var=StringVar()
        Name_var=StringVar()
        author_var=StringVar()
        publisher_var=StringVar()
        stock_var=StringVar()
        amt_var=StringVar()
        #==================Functions=====================================

        def stock_window():
            self.stock.destroy()
            from MDI import mdi_form
            stock_window = Tk()
            stock_instance = mdi_form(stock_window)

        def update_time():
            current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
            time_label.config(text="Current Time: " + current_time)
            stock.after(1000, update_time)  # Update time every 1 second

        def update_date():
            today_date = datetime.now().strftime("%Y-%m-%d")
            date_label.config(text="Today's Date: " + today_date)    
        #====================validation======================================
        def stock_ID(id):
            if id.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False
    
        def avl_stock(avls):
            if avls.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False
    
        def b_amt(BA):
            if BA.isdigit():
                return True
            else:
                messagebox.showerror('Invalid','Invalid Entry')
                return False 
            
        #========================Heading===================================
        lbtitle = Label(self.stock, text ='Stock Details', fg ='white', bg = '#06283D', font = ('Times 50 italic bold'))
        lbtitle.pack(side = TOP, fill ='x')

        #==================================database=======================================
        def generate_id():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            mycursor.execute("SELECT MAX(book_id) FROM stock")
            max_id = mycursor.fetchone()[0]
            mycursor.close()
            return max_id + 1 if max_id else 1

        def Add():
            new_id = generate_id()
            IDEntry.config(state="normal")
            IDEntry.delete(0, END)
            IDEntry.insert(0, new_id)
            mysqldb.close()

        def generate_pdf_report():
            id1 = IDEntry1.get()
            if id1:
                query = "SELECT * FROM stock WHERE book_id = %s"
                mycursor.execute(query, (id1,))
                data = mycursor.fetchone()                
                if data:
                    doc = SimpleDocTemplate(f"report_{id1}.pdf", pagesize=letter)
                    report_data = [['Book ID','Book Name','Author Name','Publisher Name','Available Stock','Amount']]  
                    id1,b_name,vd1,pub,stock1,amt1 = data
                    
                    report_data.append([id1,b_name,vd1,pub,stock1,amt1])                      
                    table = Table(report_data)
                    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), (0.8, 0.8, 0.8)),
                                            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))]))
                    doc.build([table])
                    print(f"PDF report generated successfully for ID {id1}.")   
                    os.startfile(f"report_{id1}.pdf") 
                else:
                    messagebox.showinfo("Error", f"No data found in the database for ID {id1}")
            else:
                messagebox.showinfo("Error", "Please enter an ID")             

        def searchf():
            search = IDEntry1.get()
            try:
                mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
                mycursor=mysqldb.cursor()
                mycursor.execute("SELECT * FROM stock WHERE book_id = %s or b_name= %s", (search,search,))
                row = mycursor.fetchone()
                if row:
                    id1, b_name,vd1,pub,stock1,amt1 = row
                    IDEntry.delete(0, END)
                    IDEntry.insert(END, id1)
                    NameEntry.delete(0, END)
                    NameEntry.insert(END, b_name)
                    vd_entry.delete(0, END)
                    vd_entry.insert(END, vd1)
                    pub_entry.delete(0, END)
                    pub_entry.insert(END, pub)
                    avl_stk.delete(0, END)
                    avl_stk.insert(END, stock1)
                    amt.delete(0, END) 
                    amt.insert(END, amt1)   
                else:
                    messagebox.showinfo("Not Found", f"No record found with : {search}")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error searching record: {err}")
            finally:
                mysqldb.commit()
        
        def Save():
            id1 = IDEntry.get()
            b_name = NameEntry.get()
            vd1 = vd_entry.get()
            pub=pub_entry.get()
            stock1 = avl_stk.get()
            amt1=amt.get()
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            mycursor.execute("INSERT INTO  stock(book_id,b_name,author,publisher,stock,amt) VALUES (%s, %s, %s, %s, %s, %s)"
                             , (id1,b_name,vd1,pub,stock1,amt1))
            mysqldb.commit()
            fetch_data()
            messagebox.showinfo("Saved","Record inserted successfully")

        
        def update():
            
            id1 = IDEntry.get()
            b_name = NameEntry.get()
            vd1 = vd_entry.get()
            pub=pub_entry.get()
            stock1 = avl_stk.get()
            amt1=amt.get()
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            if id1:
                mycursor.execute("SELECT * FROM stock WHERE book_id = %s", (id1,))
                row = mycursor.fetchone()
                if row:
                    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update this record?")
                    if confirm:
                        mycursor.execute("Update  stock set b_name= %s,author= %s,publisher= %s,stock= %s,amt= %s where book_id= %s"
                                             , (b_name,vd1,pub,stock1,amt1,id1))
                        mysqldb.commit()
                        messagebox.showinfo("Update","Data updated successfully")
                        fetch_data()
                else:
                    messagebox.showinfo("Error", "No data found in the database for the given ID")
            else:
                messagebox.showinfo("Error", "Please enter an ID to update")          

        def delete():
            id_val = IDEntry.get()
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            if id_val:
                confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
                if confirm:
                    mycursor.execute("DELETE FROM stock WHERE book_id = %s", (id_val,))
                    mysqldb.commit()
                    fetch_data()
                    messagebox.showinfo("Delete","Data deleted successfully")
            else:
                messagebox.showinfo("Error", "Please enter an ID to delete")        
            
        def Clear():
            IDEntry.delete(0, END)
            NameEntry.delete(0, END)
            vd_entry.delete(0, END)
            pub_entry.delete(0, END)
            avl_stk.delete(0, END)
            amt.delete(0, END)    

        def show():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            mycursor.execute("SELECT * FROM stock")
            records = mycursor.fetchall()

            for i, (id1,b_name,vd1,pub,stock1,amt1) in enumerate(records, start=1):
                library_table.insert("", "end", values=(id1,b_name,vd1,pub,stock1,amt1))
                mysqldb.close()       

        def fetch_data():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="admin@12345678",database="library")
            mycursor=mysqldb.cursor()
            mycursor.execute("select * from stock")
            rows=mycursor.fetchall()
            if len(rows)!=0:
                library_table.delete(*library_table.get_children())
                for i in rows:
                    library_table.insert("",END,values=i)
                mysqldb.commit()
            mysqldb.close()                

        #=======================================frame==========================================================

        frameleft=LabelFrame(self.stock,bg='sky blue',bd=13,relief=RIDGE,text="Books Details", font=('Times 15 italic bold'))
        frameleft.place(x=100,y=140,height=300,width=1000)

        frameright=LabelFrame(self.stock,bg='sky blue',bd=13,relief=RIDGE,text="Stored Details", font=('Times 15 italic bold'))
        frameright.place(x=100,y=480,height=300,width=1000)

        #======================================data table====================================================        
        #SCROLLBAR AND COLUMNS
        xscroll=ttk.Scrollbar(frameright,orient=HORIZONTAL)
        yscroll=ttk.Scrollbar(frameright,orient=VERTICAL)
        style=ttk.Style(frameright)
        style.theme_use('clam')
        style.configure('Treeview',foreground='black',background='sky blue',fieldbackground='sky blue')
        style.map('Treeview',background=[('selected','#1A8F2D')])
        cols=('Book ID','Book Name','Author Name','Publisher Name','Available Stock','Amount')
        library_table=ttk.Treeview(frameright,columns=cols,show='headings',xscrollcommand=xscroll.set,yscrollcommand=yscroll.set)

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
            library_table.column(col, width=130, anchor='center')  # Center the column content
            library_table.pack(fill=BOTH, expand=1)
        #======================================Labels=========================================================
        #search by id
        IDEntry1=Entry(stock,font=('Italic',15,'bold'),fg='Black',width=10)
        IDEntry1.place(x=200,y=100) 

        ID=Label(frameleft,text='Book ID',font=('Times 15 italic bold'), fg='Black',bg='sky blue')
        ID.place(x=50,y=50)
        IDEntry=Entry(frameleft,textvariable=ID_var,font=('Times 13 italic bold'), fg='Black')
        IDEntry.place(x=250,y=50)
        validate_id=stock.register(stock_ID)
        IDEntry.config(validate='key',validatecommand=(validate_id,'%S'))

        #bkko name
        
        Name=Label(frameleft,text='Name Of Book',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        Name.place(x=50,y=110)
        NameEntry=Entry(frameleft, textvariable = Name_var, font = ('Times 13 italic bold'))
        NameEntry.place(x=250,y=110)

        vd_name=Label(frameleft,text='Author Name',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        vd_name.place(x=50,y=170)
        vd_entry=Entry(frameleft,textvariable=author_var,font=('Times 13 italic bold'))
        vd_entry.place(x=250,y=170)

        pub_name=Label(frameleft,text='Publisher Name',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        pub_name.place(x=550,y=50)
        pub_entry=Entry(frameleft,textvariable=publisher_var,font=('Times 13 italic bold'))
        pub_entry.place(x=750,y=50)

        avl_stkl=Label(frameleft,text='Available Stocks',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        avl_stkl.place(x=550,y=110)
        avl_stk=Entry(frameleft,textvariable=stock_var,font=('Times 13 italic bold'))
        avl_stk.place(x=750,y= 110)
        validate_stock=stock.register(avl_stock)
        avl_stk.config(validate='key',validatecommand=(validate_stock,'%S'))

        amtl=Label(frameleft,text='Amount Of Book',font=('Times 15 italic bold'),fg='Black',bg='sky blue')
        amtl.place(x=550,y= 170)
        amt=Entry(frameleft,textvariable=amt_var,font=('Times 13 italic bold'))
        amt.place(x = 750, y = 170)
        validate_payment=stock.register(b_amt)
        amt.config(validate='key',validatecommand=(validate_payment,'%S'))

        #currentDate 
        date_label =Label(stock, text="", fg="white", bg= "#06283D", font=("Helvetica", 16))
        date_label.place(x=400,y=100)
        
        #currentTime
        time_label = Label(stock, text="", bg= "#06283D", fg="white", font=("Helvetica", 16))
        time_label.place(x=800,y=100)
        

        up=Image.open("OIP2.jpeg")
        up=up.resize((220,220),Image.ADAPTIVE)
        self.photo_imgup=ImageTk.PhotoImage(up)
        label = Label(stock,image=self.photo_imgup, bd=5, relief= RIDGE, bg="sky blue")
        label.place(x=1170,y=100,width=220,height=200)

        #====================================Buttons=====================================
        search=Image.open("search.png")
        search=search.resize((60,60),Image.ADAPTIVE)
        self.photo_img1=ImageTk.PhotoImage(search)
        lbimg1=Button(stock,command=searchf,image=self.photo_img1,bd=2,bg="#06283D",borderwidth=0,cursor="hand2", activebackground="#06283D")
        lbimg1.place(x=330,y=90,width=50,height=50)

        back=Image.open("back2.png")
        back=back.resize((60,60),Image.ADAPTIVE)
        self.photo_img2=ImageTk.PhotoImage(back)
        back1=Button(stock,command=stock_window,image=self.photo_img2,borderwidth=0,cursor="hand2",bg="#06283D",activebackground="#06283D")
        back1.place(x=10,y=0,width=100,height=100)


        button=Button(stock,text='Print', command= generate_pdf_report,font=('Times 15 italic bold'),fg='white',bg="green",
                  activebackground="green",activeforeground="#EDEDED",bd=3,cursor="hand2",width=15)
        button.place(x=1200,y=325)

        button=Button(stock,text='Add',command= Add,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=3,cursor="hand2",width=15)
        button.place(x=1200,y=405)

        button=Button(stock,text='Save',command= Save,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=3,cursor="hand2",width=15)
        button.place(x=1200,y=485)

        button=Button(stock,text='Delete',command= delete,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=3,cursor="hand2",width=15)
        button.place(x=1200,y=565)

        button=Button(stock,text='Update',command= update,font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=3,cursor="hand2",width=15)
        button.place(x=1200,y=645)

        button=Button(stock,text='Clear',font=('Times 15 italic bold'),fg='white',bg="green",
              activebackground="green",activeforeground="white",bd=3,command= Clear,cursor="hand2",width=15)
        button.place(x=1200,y=725)

        show()
        library_table.bind('<Double-Button-1>')
        try:
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="admin@12345678", database="library")
            mycursor = mysqldb.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect to MySQL: {err}")

        adjust_column_widths()
        update_date()
        update_time()    
            
if __name__ == "__main__":
    stock=Tk()
    obj=stock_form(stock)
    stock.mainloop()
