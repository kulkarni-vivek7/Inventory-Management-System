from tkinter import *
from PIL import Image, ImageTk
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
        
        # clock
        self.lbl_clock = Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=('times new roman',15),bg="#4d636d",
                               fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        # Left Menu
        self.Menu_logo = Image.open("images/menu_im.png")
        self.Menu_logo = self.Menu_logo.resize((200,500),Image.LANCZOS)
        self.Menu_logo = ImageTk.PhotoImage(self.Menu_logo)

        Left_menu = Frame(self.root, bd=2, relief=RIDGE,bg="white")
        Left_menu.place(x = 0, y = 102, width=300, height=500)

        lbl_menulogo = Label(Left_menu, image=self.Menu_logo)
        lbl_menulogo.pack(side=TOP,fill=X)

        #-----Menu--------
        M_Frame = LabelFrame(self.root, text="Menus", font=("times new roman",15),bg="white")
        M_Frame.place(x=320, y=130, width=1000, height=80)

        btn_Admin_login = Button(M_Frame, text="Admin Login", 
                                 font=("goudy old style",15,"bold"),bg="#0b5377",
                                 fg="white",cursor="hand2",command=self.admin_log).place(x=15,y=5,width=270,height=40)
        btn_emp_login = Button(M_Frame, text="Employee Login", font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",
                               cursor="hand2",command=self.employee_log).place(x=360,y=5,width=270,height=40)
        btn_Exit = Button(M_Frame, text="Exit", font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",
                          command=self.exit).place(x=710,y=5,width=270,height=40)
        
        # footer
        lbl_footer = Label(self.root,text="IMS-Inventory Management System | Developed By Vivek Kulkarni\nFor Any Technical Issues Contact: 7975251112",
                      font=('times new roman',12,'bold'),bg="#4d636d", 
                      fg="white").pack(side=BOTTOM,fill=X)
        
        self.update_content()
        
# functions -------------------------------------------------------------------------------------------

    def update_content(self):
        time_ = time.strftime('%I:%M:%S')
        date_ = time.strftime('%d-%m-%Y')
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_content)

    def admin_log(self):
        self.root.destroy()
        os.system('python Admin_Login.py')

    def employee_log(self):
        self.root.destroy()
        os.system('python Employee_Login.py')

    def exit(self):
        self.root.destroy()


if __name__ == '__main__':
   root = Tk()
   obj = IMS(root)
   root.mainloop()