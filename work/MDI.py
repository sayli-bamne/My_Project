from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


class mdi_form():
    def __init__(self,mdi):
        self.mdi=mdi
        self.mdi.title("Staff Form")
        self.mdi.geometry("1500x800")
        self.mdi.resizable(0, 0)

        #========================functions===============================================

        def staff_page():
            self.mdi.destroy()
            from staff import staff_form
            staff_window = Tk()
            staff_instance = staff_form(staff_window)
            
        def vendor_window():
            self.mdi.destroy()
            from vendor import Vendor
            Vender_window = Tk()
            vender_instance = Vendor(Vender_window)

        def borrower_wd():
            self.mdi.destroy()
            from borrower import borrower_form
            borrower_window = Tk()
            borrower_instance = borrower_form(borrower_window)

        def stock_page():
            self.mdi.destroy()
            from stock import stock_form
            stock_window = Tk()
            stock_instance = stock_form(stock_window) 
        
        def order_page():
            self.mdi.destroy()
            from order import Order
            order_window = Tk()
            order_instance = Order(order_window)  

        def exit():
            if messagebox.askyesno("Exit", "Do you want to exit?"):
                self.mdi.destroy()
        
        #===================================Heading====================================

        lbtitle=Label(self.mdi,bd=10,relief=RIDGE,text='LIBRARY MANAGEMENT SYSTEM',fg='red',bg='sky blue',font=('Times 50  bold'))
        lbtitle.pack(side=TOP,fill='x')
        
        #=======================================frame==========================================================

        frameright=Frame(mdi,bg='sky blue',bd=10,relief=RIDGE)
        frameright.place(x=170,y=100,height=700,width=1330)

        frameleft=Frame(mdi,bg='sky blue',bd=10,relief=RIDGE)
        frameleft.place(x=0,y=100,height=700,width=170)  
        
        #==================================menu icons====================================
        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image = photo)
            label.image = photo 

        image = Image.open('img.jpeg')
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(frameright, image = photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=BOTH, expand = YES)

        img1=Image.open("staff2.png")
        img1=img1.resize((110,110))
        self.photo_img1=ImageTk.PhotoImage(img1)
        lbimg1=Button(frameleft,image=self.photo_img1,bd=0,activeforeground='red',activebackground='sky blue',cursor="hand2",command=staff_page, bg="sky blue")
        lbimg1.place(x=10,y=130)

        img2=Image.open("borrower2.png")
        img2=img2.resize((120,120))
        self.photo_img2=ImageTk.PhotoImage(img2)
        lbimg2=Button(frameleft,image=self.photo_img2,bd=0,activeforeground='red',activebackground='sky blue',cursor="hand2",command=borrower_wd ,bg="sky blue")
        lbimg2.place(x=10,y=250)

        img3=Image.open("vender2.png")
        img3=img3.resize((120,120))
        self.photo_img3=ImageTk.PhotoImage(img3)
        lbimg3=Button(frameleft,image=self.photo_img3,bd=0,activeforeground='red',activebackground='sky blue',cursor="hand2",command=vendor_window, bg="sky blue")
        lbimg3.place(x=10,y=0)

        img4=Image.open("bkimg.png")
        img4=img4.resize((110,110))
        self.photo_img4=ImageTk.PhotoImage(img4)
        lbimg4=Button(frameleft,image=self.photo_img4,bd=0,activeforeground='red',activebackground='sky blue',cursor="hand2",command=stock_page, bg="sky blue")
        lbimg4.place(x=10,y=390)

        img5=Image.open("order5.png")
        img5=img5.resize((120,120))
        self.photo_img5=ImageTk.PhotoImage(img5)
        lbimg5=Button(frameleft,image=self.photo_img5,bd=0,activeforeground='red',activebackground='sky blue',cursor="hand2",command=order_page, bg="sky blue")
        lbimg5.place(x=10,y=510)
        
        button2=Button(frameleft,text='Exit',bg='red',fg='white',cursor="hand2",activeforeground='white',activebackground='red',width=15,command=exit)
        button2.place(x=10,y=650)  
        #==============================Labels=============================================

        vender=Label(frameleft,text="VENDOR",font=('Times 15 italic bold'),bg='sky blue',fg='red',borderwidth=0)
        vender.place(x=30,y=100)

        staff=Label(frameleft,text="STAFF",font=('Times 15 italic bold'),bg='sky blue',fg='red')
        staff.place(x=32,y=230)

        borrow=Label(frameleft,text="BORROWER",font=('Times 15 italic bold'),bg='sky blue',fg='red')
        borrow.place(x=11,y=360)

        stock=Label(frameleft,text="STOCK",font=('Times 15 italic bold') ,bg='sky blue',fg='red')
        stock.place(x=30,y=490)

        order=Label(frameleft,text="ORDER",font=('Times 15 italic bold'),bg='sky blue',fg='red')
        order.place(x=30,y=620)
       

if __name__=="__main__":
    mdi=Tk()
    obj=mdi_form(mdi)
    mdi.mainloop()
