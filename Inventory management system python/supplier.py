from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class supplierClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # All variables
        self.var_searchBy = StringVar()
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        
        # Search Frame
        # Options
        lbl_search = Label(self.root,text="Invoice No.",bg='white',font=('times new roman',15))
        lbl_search.place(x=670,y=80)

        txt_search = Entry(self.root,textvariable=self.var_searchtxt,font=('goudy old style',15),
                           bg='lightyellow').place(x=770,y=80)

        btn_search = Button(self.root,text='Search',command=self.search,
                            font=('goudy old style',15),bg='#4caf50',fg='white',
                            cursor='hand2').place(x=980,y=79,width=100,height=27)
        
        # Title
        title = Label(self.root, text='Supplier Details',font=('goudy old style',20,'bold'),
                      bg='#0f4d7d',fg='white').place(x=50,y=10,width=1000,height=40)
        
        # contents
        # Row 1
        lbl_sup_invoice = Label(self.root, text='Invoice No.',font=('goudy old style',15,'bold'),
                      bg='white').place(x=50,y=80)
        
        txt_sup_invoice = Entry(self.root,textvariable=self.var_sup_invoice, font=('goudy old style',15,'bold'),
                      bg='lightyellow').place(x=180,y=80,width=180)
        
        # Row 2
        lbl_name = Label(self.root, text='Name',font=('goudy old style',15,'bold'),
                      bg='white').place(x=50,y=120)
        
        txt_name = Entry(self.root,textvariable=self.var_name, font=('goudy old style',15,'bold'),
                      bg='lightyellow').place(x=180,y=120,width=180)
        
        # Row 3
        lbl_contact = Label(self.root, text='Contact',font=('goudy old style',15,'bold'),
                      bg='white').place(x=50,y=160)
        
        txt_contact = Entry(self.root,textvariable=self.var_contact, font=('goudy old style',15,'bold'),
                      bg='lightyellow').place(x=180,y=160,width=180)

        # Row 4
        lbl_description = Label(self.root, text='Description',font=('goudy old style',15,'bold'),
                      bg='white').place(x=50,y=200)
        
        self.txt_description = Text(self.root,font=('goudy old style',15,'bold'),bg='lightyellow')
        self.txt_description.place(x=180,y=200,width=470,height=120)
        

        # Buttons
        btn_add = Button(self.root,text='Save',font=('goudy old style',15,'bold'),command=self.add,bg='#2196f3',fg='white',
                            cursor='hand2').place(x=180,y=370,width=110,height=35)
        
        btn_update = Button(self.root,text='Update',font=('goudy old style',15,'bold'),command=self.update,
                            bg='#4caf50',fg='white',
                            cursor='hand2').place(x=300,y=370,width=110,height=35)
        
        btn_delete = Button(self.root,text='Delete',font=('goudy old style',15,'bold'),command=self.delete,
                            bg='#f44336',fg='white',
                            cursor='hand2').place(x=420,y=370,width=110,height=35)
        
        btn_clear = Button(self.root,text='Clear',font=('goudy old style',15,'bold'),command=self.clear,bg='#607d8b',fg='white',
                            cursor='hand2').place(x=540,y=370,width=110,height=35)
        

        # Supplier Details
        sup_frame = Frame(self.root, bd=3, relief=RIDGE)
        sup_frame.place(x=700,y=120,width=390,height=350)

        scroll_y = Scrollbar(sup_frame,orient=VERTICAL)
        scroll_x = Scrollbar(sup_frame,orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(sup_frame,columns=("invoice","name","contact","description"),
                                          yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.supplierTable.xview)
        scroll_y.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Invoice")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("description",text="Description")

        self.supplierTable['show'] = 'headings'

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("description",width=100)
        
        self.supplierTable.pack(fill=BOTH,expand=1)

        self.supplierTable.bind('<ButtonRelease-1>',self.getData)

        self.show()

#---------------------------------------------------------------------------------------------------------
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice Must be required",parent=self.root)

            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Supplier Name Must be required",parent=self.root)

            elif self.var_contact.get() == "":
                messagebox.showerror("Error", "Contact Must be required",parent=self.root)
            
            else:
                cur.execute('Select * from supplier where invoice=?',(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Invoice no. is already assigned, try different",parent=self.root)
                else:
                    cur.execute("Insert into supplier(invoice,name,contact,description) values(?,?,?,?)",(
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_description.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute('select * from supplier')
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def getData(self,ev):
        f = self.supplierTable.focus()
        content = (self.supplierTable.item(f))
        row = content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_description.delete('1.0',END),
        self.txt_description.insert(END,row[3])


    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice Must be required",parent=self.root)

            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Supplier Name Must be required",parent=self.root)

            elif self.var_contact.get() == "":
                messagebox.showerror("Error", "Contact Must be required",parent=self.root)
            
            else:
                cur.execute('Select * from supplier where invoice=?',(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice no.",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,description=? where invoice=?",(
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_description.get('1.0',END),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice Must be required",parent=self.root)

            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Supplier Name Must be required",parent=self.root)

            elif self.var_contact.get() == "":
                messagebox.showerror("Error", "Contact Must be required",parent=self.root)
            
            else:
                cur.execute('Select * from supplier where invoice=?',(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice no.",parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Supplier Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_description.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()


    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
            
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)

                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

if __name__ == '__main__':
   root = Tk()
   obj = supplierClass(root)
   root.mainloop()