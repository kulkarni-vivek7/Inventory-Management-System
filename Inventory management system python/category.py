from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class categoryClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # Title 
        lbl_title = Label(self.root, text='Manage Product Category',
                          font=('times new roman',30),bg='#184a45',fg='white',bd=3,
                          relief=RIDGE).pack(side=TOP,padx=10,pady=20,fill=X)
        
        lbl_name = Label(self.root, text='Enter Category Name',
                          font=('times new roman',30),bg='white').place(x=50,y=100)
        
        txt_name = Entry(self.root, textvariable=self.var_name,
                          font=('times new roman',18),bg='lightyellow').place(x=50,y=170,width=300)
        
        btn_add = Button(self.root, text='ADD', font=('times new roman',15),bg='#4caf50',fg='white',
                         command=self.add,cursor='hand2').place(x=360,y=170,width=150,height=30)
        
        btn_delete = Button(self.root, text='DELETE',font=('times new roman',15),bg='red',fg='white',
                         command=self.delete,cursor='hand2').place(x=520,y=170,width=150,height=30)
        

         # category Details
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)

        scroll_y = Scrollbar(cat_frame,orient=VERTICAL)
        scroll_x = Scrollbar(cat_frame,orient=HORIZONTAL)

        self.categoryTable = ttk.Treeview(cat_frame,columns=("catid","name"),yscrollcommand=scroll_y.set,
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.categoryTable.xview)
        scroll_y.config(command=self.categoryTable.yview)

        self.categoryTable.heading("catid",text="Cat ID")
        self.categoryTable.heading("name",text="Name")

        self.categoryTable['show'] = 'headings'

        self.categoryTable.column("catid",width=90)
        self.categoryTable.column("name",width=100)
        
        self.categoryTable.pack(fill=BOTH,expand=1)

        self.categoryTable.bind('<ButtonRelease-1>',self.getData)

        # IMages
        # image 1
        self.img1 = Image.open('images/cat.jpg')
        self.img1 = self.img1.resize((500,250),Image.LANCZOS)
        self.img1 = ImageTk.PhotoImage(self.img1)

        self.lbl_img1 = Label(self.root,image=self.img1,bd=2,relief=RAISED)
        self.lbl_img1.place(x=50,y=220)

        # image 2
        self.img2 = Image.open('images/category.jpg')
        self.img2 = self.img2.resize((500,250),Image.LANCZOS)
        self.img2 = ImageTk.PhotoImage(self.img2)

        self.lbl_img2 = Label(self.root,image=self.img2,bd=2,relief=RAISED)
        self.lbl_img2.place(x=580,y=220)

        self.show()

# -------------------------------------Functions----------------------------------------------------------
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name Must be required",parent=self.root)
            
            else:
                cur.execute('Select * from category where name=?',(self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Category is already present, try different",parent=self.root)
                else:
                    cur.execute("Insert into category(name) values(?)",(
                        self.var_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute('select * from category')
            rows = cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('',END,values=row)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def getData(self,ev):
        f = self.categoryTable.focus()
        content = (self.categoryTable.item(f))
        row = content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "please select category from the list",parent=self.root)
            
            else:
                cur.execute('Select * from category where catid=?',(self.var_cat_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "please try again",parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from category where catid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Category Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__ == '__main__':
   root = Tk()
   obj = categoryClass(root)
   root.mainloop()