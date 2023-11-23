from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
import os
import time

class IMS:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        # title
        self.icon_title = PhotoImage(file='images/logo1.png')

        title = Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,
                      font=('times new roman',40,'bold'),bg="#010c48", 
                      fg="white", anchor='w',padx=20).place(x=0,y=0,relwidth=1,height=70)
        
        # Button Logout
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, 'bold'),command=self.logout,
                            bg='yellow',cursor="hand2").place(x=1180, y = 10, height = 50, width = 150)
        
        # clock
        self.lbl_clock = Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=('times new roman',15),bg="#4d636d", 
                               fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        # Left Menu
        self.Menu_logo = Image.open("images/menu_im.png")
        self.Menu_logo = self.Menu_logo.resize((200,200),Image.LANCZOS)
        self.Menu_logo = ImageTk.PhotoImage(self.Menu_logo)

        Left_menu = Frame(self.root, bd=2, relief=RIDGE,bg="white")
        Left_menu.place(x = 0, y = 102, width=200, height=565)

        lbl_menulogo = Label(Left_menu, image=self.Menu_logo)
        lbl_menulogo.pack(side=TOP,fill=X)

        self.icon_side = PhotoImage(file='images/side.png')

        lbl_menu =Label(Left_menu, text="Menu", font=("times new roman", 20, 'bold'),
                            bg='#009688').pack(side=TOP, fill=X)
        
        btn_employee =Button(Left_menu, text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",
                              font=("times new roman", 20, 'bold'),
                            bg='white',bd=3,cursor="hand2").pack(side=TOP, fill=X)
        
        btn_supplier =Button(Left_menu, text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",
                              font=("times new roman", 20, 'bold'),
                            bg='white',bd=3,cursor="hand2").pack(side=TOP, fill=X)
        
        btn_category =Button(Left_menu, text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",
                              font=("times new roman", 20, 'bold'),
                            bg='white',bd=3,cursor="hand2").pack(side=TOP, fill=X)
        
        btn_product =Button(Left_menu, text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",
                              font=("times new roman", 20, 'bold'),
                            bg='white',bd=3,cursor="hand2").pack(side=TOP, fill=X)
        
        btn_sales =Button(Left_menu, text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",
                              font=("times new roman", 20, 'bold'),
                            bg='white',bd=3,cursor="hand2").pack(side=TOP, fill=X)
        
        btn_exit =Button(Left_menu, text="Exit",command=self.exit,image=self.icon_side,compound=LEFT,padx=5,anchor="w",
                              font=("times new roman", 20, 'bold'),
                            bg='white',bd=3,cursor="hand2").pack(side=TOP, fill=X)
        
        # Contents
        self.lbl_employee = Label(self.root,text="Total Employees\n[ 0 ]",bd = 5, relief=RIDGE,
                                  bg="#33bbf9",fg="white",font=('times new roman',20,'bold'))
        self.lbl_employee.place(x=300,y = 120,height=150, width=300)

        self.lbl_supplier = Label(self.root,text="Total Suppliers\n[ 0 ]",bd = 5, relief=RIDGE,
                                  bg="#ff5722",fg="white",font=('times new roman',20,'bold'))
        self.lbl_supplier.place(x=650,y = 120,height=150, width=300)

        self.lbl_category = Label(self.root,text="Total Categories\n[ 0 ]",bd = 5, relief=RIDGE,
                                  bg="#009688",fg="white",font=('times new roman',20,'bold'))
        self.lbl_category.place(x=1000,y = 120,height=150, width=300)

        self.lbl_product = Label(self.root,text="Total Products\n[ 0 ]",bd = 5, relief=RIDGE,
                                  bg="#607d8b",fg="white",font=('times new roman',20,'bold'))
        self.lbl_product.place(x=300,y = 300,height=150, width=300)

        self.lbl_sales = Label(self.root,text="Total Sales\n[ 0 ]",bd = 5, relief=RIDGE,
                                  bg="#ffc107",fg="white",font=('times new roman',20,'bold'))
        self.lbl_sales.place(x=650,y = 300,height=150, width=300)

        
        # footer
        lbl_footer = Label(self.root,text="IMS-Inventory Management System | Developed By Vivek Kulkarni\nFor Any Technical Issues Contact: 7975251112",
                      font=('times new roman',12,'bold'),bg="#4d636d",
                      fg="white").pack(side=BOTTOM,fill=X)
        
        self.update_content()
        
# functions -------------------------------------------------------------------------------------------
    
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            cur.execute('select * from product')
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Products\n[ {str(len(product))} ]")

            cur.execute('select * from supplier')
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n[ {str(len(supplier))} ]")

            cur.execute('select * from category')
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Categories\n[ {str(len(category))} ]")

            cur.execute('select * from employee')
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employees\n[ {str(len(employee))} ]")

            bill = len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales\n[ {str(bill)} ]')

            time_ = time.strftime('%I:%M:%S')
            date_ = time.strftime('%d-%m-%Y')
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def logout(self):
        self.root.destroy()
        os.system('python Admin_Login.py')

    def exit(self):
        self.root.destroy()


if __name__ == '__main__':
   root = Tk()
   obj = IMS(root)
   root.mainloop()