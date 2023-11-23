from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class productClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        product_Frame = Frame(self.root, bd=2, relief=RIDGE,bg='white')
        product_Frame.place(x=10,y=10,width=450,height=480)

        # Variables
        self.var_searchBy = StringVar()
        self.var_searchtxt = StringVar()
        
        self.var_pid = StringVar()

        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_lst = []
        self.sup_lst = []
        self.fetch_cat_sup()
        self.var_prod = StringVar()
        self.var_price = StringVar()
        self.var_quan = StringVar()
        self.var_status = StringVar()

        # Title
        title = Label(product_Frame, text='Manage Product Details',font=('goudy old style',18,'bold'),
                      bg='#0f4d7d',fg='white').pack(side=TOP,fill=X)
        

        # column 1
        lbl_category = Label(product_Frame, text='Category',font=('goudy old style',18,'bold'),
                      bg='white').place(x=30,y=60)
        
        lbl_supplier = Label(product_Frame, text='Supplier',font=('goudy old style',18,'bold'),
                      bg='white').place(x=30,y=110)
        
        lbl_product = Label(product_Frame, text='Name',font=('goudy old style',18,'bold'),
                      bg='white').place(x=30,y=160)
        
        lbl_price = Label(product_Frame, text='Price',font=('goudy old style',18,'bold'),
                      bg='white').place(x=30,y=210)
        
        lbl_quantity = Label(product_Frame, text='Quantity',font=('goudy old style',18,'bold'),
                      bg='white').place(x=30,y=260)
        
        lbl_status = Label(product_Frame, text='Status',font=('goudy old style',18,'bold'),
                      bg='white').place(x=30,y=310)
        

        # column 2
        cmb_cat = ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_lst,
                                  state='readonly',justify=CENTER,font=('times new roman',15))
        cmb_cat.place(x=150,y=65,width=200)
        cmb_cat.current(0)


        cmb_sup = ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_lst,
                                  state='readonly',justify=CENTER,font=('times new roman',15))
        cmb_sup.place(x=150,y=115,width=200)
        cmb_sup.current(0)


        txt_name = Entry(product_Frame,textvariable=self.var_prod,
                         font=('times new roman',15),bg='lightyellow').place(x=150,y=165,width=200)
        
        txt_price = Entry(product_Frame,textvariable=self.var_price,
                         font=('times new roman',15),bg='lightyellow').place(x=150,y=215,width=200)
        
        txt_quan = Entry(product_Frame,textvariable=self.var_quan,
                         font=('times new roman',15),bg='lightyellow').place(x=150,y=265,width=200)

        cmb_status = ttk.Combobox(product_Frame,textvariable=self.var_status,values=('Select','Active','Inactive'),
                                  state='readonly',justify=CENTER,font=('times new roman',15))
        cmb_status.place(x=150,y=315,width=200)
        cmb_status.current(0)

        # Buttons
        btn_add = Button(product_Frame,text='Save',font=('goudy old style',15,'bold'),command=self.add,bg='#2196f3',fg='white',
                            cursor='hand2').place(x=10,y=400,width=100,height=40)
        
        btn_update = Button(product_Frame,text='Update',font=('goudy old style',15,'bold'),command=self.update,bg='#4caf50',
                            fg='white',
                            cursor='hand2').place(x=120,y=400,width=100,height=40)
        
        btn_delete = Button(product_Frame,text='Delete',font=('goudy old style',15,'bold'),command=self.delete,bg='#f44336',
                            fg='white',
                            cursor='hand2').place(x=230,y=400,width=100,height=40)
        
        btn_clear = Button(product_Frame,text='Clear',font=('goudy old style',15,'bold'),command=self.clear,bg='#607d8b',
                           fg='white',
                            cursor='hand2').place(x=340,y=400,width=100,height=40)
        

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Product",
                                 font=('times new roman',12,'bold'),bd=2,relief=RIDGE, bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        # Options
        cmb_search = ttk.Combobox(SearchFrame,textvariable=self.var_searchBy,values=('Select','Category','Supplier','Name'),
                                  state='readonly',justify=CENTER,font=('times new roman',15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt,font=('goudy old style',15),
                           bg='lightyellow').place(x=200,y=10)

        btn_search = Button(SearchFrame,text='Search',command=self.search,
                            font=('goudy old style',15),bg='#4caf50',fg='white',
                            cursor='hand2').place(x=410,y=9,width=150,height=30)
        
        # Product Details
        prod_frame = Frame(self.root, bd=3, relief=RIDGE)
        prod_frame.place(x=480,y=100,width=600,height=390)

        scroll_y = Scrollbar(prod_frame,orient=VERTICAL)
        scroll_x = Scrollbar(prod_frame,orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(prod_frame,columns=("pid","Category","Supplier","name","price","quantity","status"),
                                         yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.ProductTable.xview)
        scroll_y.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid",text="Product ID")
        self.ProductTable.heading("Category",text="category")
        self.ProductTable.heading("Supplier",text="supplier")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("quantity",text="Quantity")
        self.ProductTable.heading("status",text="Status")

        self.ProductTable['show'] = 'headings'

        self.ProductTable.column("pid",width=90)
        self.ProductTable.column("Category",width=100)
        self.ProductTable.column("Supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("quantity",width=100)
        self.ProductTable.column("status",width=100)
        
        self.ProductTable.pack(fill=BOTH,expand=1)

        self.ProductTable.bind('<ButtonRelease-1>',self.getData)

        self.show()
        

#---------------------------------------------------------------------------------------------------------
    
    def fetch_cat_sup(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        self.cat_lst.append("Empty")
        self.sup_lst.append("Empty")
        try:
            cur.execute('Select name from category')
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_lst[:]
                self.cat_lst.append("Select")
                for i in cat:
                    self.cat_lst.append(i[0])

            cur.execute('Select name from supplier')
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_lst[:]
                self.sup_lst.append("Select")
                for i in sup:
                    self.sup_lst.append(i[0])



        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty":
                messagebox.showerror("Error", "Please select the category",parent=self.root)

            elif self.var_sup.get() == "Select" or self.var_sup.get() == "Empty":
                messagebox.showerror("Error", "Please select the supplier",parent=self.root)

            elif self.var_prod.get() == "":
                messagebox.showerror("Error", "Product Name Must be required",parent=self.root)

            elif self.var_price.get() == "":
                messagebox.showerror("Error", "Product Price Must be required",parent=self.root)

            elif self.var_quan.get() == "":
                messagebox.showerror("Error", "Product Quantity Must be required",parent=self.root)

            elif self.var_status.get() == "Select":
                messagebox.showerror("Error", "Please Select The Product Status",parent=self.root)
            
            else:
                cur.execute('Select * from product where name=?',(self.var_prod.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Product is already present, try different",parent=self.root)
                else:
                    cur.execute("Insert into product(Category,Supplier,name,price,quantity,status) values(?,?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_prod.get(),
                        self.var_price.get(),
                        self.var_quan.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully",parent=self.root)
                    self.show()
            

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute('select * from product')
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def getData(self,ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_prod.set(row[3])
        self.var_price.set(row[4])
        self.var_quan.set(row[5])
        self.var_status.set(row[6])



    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            
            else:
                cur.execute('Select * from product where pid=?',(self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product",parent=self.root)
                else:
                    # Category,Supplier,name,price,quantity,status
                    cur.execute("Update product set Category=?,Supplier=?,name=?,price=?,quantity=?,status=? where pid=?",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_prod.get(),
                        self.var_price.get(),
                        self.var_quan.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully",parent=self.root)
                    self.show()
            

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error","Please select product from list",parent=self.root)

            else:
                cur.execute('Select * from product where pid=?',(self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product",parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Product Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_prod.set("")
        self.var_price.set("")
        self.var_quan.set("")
        self.var_status.set("Select")
        self.var_searchBy.set("Select")
        self.var_searchtxt.set("")
        self.show()


    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchBy.get() == "Select":
                messagebox.showerror("Error","Select Search By Option",parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            
            else:
                cur.execute("select * from product where "+self.var_searchBy.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)

                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__ == '__main__':
   root = Tk()
   obj = productClass(root)
   root.mainloop()