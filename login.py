from tkinter import*
from PIL import Image,ImageTk
from tkinter import messagebox
from dashboard import GMS
import sqlite3
import os
import smtplib
import email_pass
import time
class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System | Developed By Abhijit")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        self.otp=''
        #=====Title=======
        self.icon_title=ImageTk.PhotoImage(file="images/logo1.png")
        title=Label(self.root,image=self.icon_title,text="Grocery Store Management System",compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20)
        title.place(x=0,y=0,relwidth=1,height=70)
        #===images====
        self.phone=Image.open("images/phone.png")
        self.phone=self.phone.resize((350,460),Image.LANCZOS)
        self.phone=ImageTk.PhotoImage(self.phone)
        self.lbl_phone=Label(self.root,image=self.phone,bd=0)
        self.lbl_phone.place(x=300,y=90)
        #===LoginFrame===
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)
        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=20,relwidth=1)
        lbl_user=Label(login_frame,text="Username",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=90)
        self.username=StringVar()
        self.password=StringVar()
        txt_username=Entry(login_frame,textvariable=self.username,font=("times new roman",15),bg="#ECECEC").place(x=50,y=130,width=220)
        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=190)
        txt_password=Entry(login_frame,textvariable=self.password,show="x",font=("times new roman",15),bg="#ECECEC").place(x=50,y=230,width=220)
        btn_login=Button(login_frame,command=self.login,text="Log In",font=("Aerial Rounded MT Bold",15),bg="#00B0f0",activebackground="#00B0f0",fg="white",activeforeground="white").place(x=50,y=290,width=220,height=32)
        hr=Label(login_frame,bg="lightgray").place(x=50,y=360,width=220,height=2)
        or_=Label(login_frame,bg="white",fg="gray",text="OR",font=("times new roman",13,"bold")).place(x=140,y=347)
        btn_forget=Button(login_frame,command=self.forget_window,text="Forget Password?",font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=90,y=380)
        #===RegisterFrame=====
       # register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
       # register_frame.place(x=650,y=565,width=350,height=60)
       # lbl_reg=Label(register_frame,text="For any queries contact 989242xxxx",font=("times new roman",15),bg="white",fg="green").place(x=0,y=20,relwidth=1)
        #====Animation Images===
        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")
        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=434,y=169,width=186,height=320)
        self.animate()
        #====Footer===
        lbl_footer=Label(self.root,text="Grocery Store Mangement System | Developed By Abhijit\nFor any Technical Issue Contact: 989xxxxx59",font=("times new roman",12),bg="#4d636d",fg="white")
        lbl_footer.pack(side=BOTTOM,fill=X) 
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)
        

    def login(self):
     con=sqlite3.connect(database=r'gms.db')
     cur=con.cursor()
     try:
        if self.username.get()=="" or self.password.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
           cur.execute("select utype from employee where eid=? AND pass=?",(self.username.get(),self.password.get()))
           user=cur.fetchone()
           if user==None:
             messagebox.showerror("Error","Invalid USERNAME or PASSWORD?",parent=self.root)
           else:
             if user[0]=="Admin":
                self.root.destroy()
                os.system("python dashboard.py")
             else:
                self.root.destroy()
                os.system("python billing.py")     
     except Exception as ex:
           messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def forget_window(self):
       con=sqlite3.connect(database=r'gms.db')
       cur=con.cursor()
       try:
        if self.username.get()=="":
             messagebox.showerror("Error","Employee ID must be required",parent=self.root)
        else:
           cur.execute("select email from employee where eid=?",(self.username.get(),))
           email=cur.fetchone()
           if email==None:
              messagebox.showerror("Error","Invalid Employee ID,try again",parent=self.root)
           else:
              #======Forget Window====
              self.var_otp=StringVar()
              self.var_new_pass=StringVar()
              self.var_conf_pass=StringVar()
              #call send_email_function()
              chk=self.send_email(email[0])
              if chk=='f':
                 messagebox.showerror("Error","Connection Error,try again",parent=self.root)
              else:
                self.forget_win=Toplevel(self.root)
                self.forget_win.title("RESET PASSWORD")
                self.forget_win.geometry("400x350+500+100")
                self.forget_win.focus_force()
                title=Label(self.forget_win,text="Reset Password",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                lbl_reset=Label(self.forget_win,text="Enter OTP sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
                txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=240,height=30)
                self.btn_reset=Button(self.forget_win,command=self.validate_otp,text="Submit",font=("times new roman",15),bg="lightblue")
                self.btn_reset.place(x=270,y=100,width=90,height=30)
                new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=240,height=30)
                conf_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=220)
                txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=250,width=240,height=30)
                self.btn_update=Button(self.forget_win,command=self.update_password,text="Update",font=("times new roman",15),bg="lightblue",state=DISABLED)
                self.btn_update.place(x=150,y=300,width=90,height=30)
       except Exception as ex:
         messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def update_password(self):
       if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
          messagebox.showerror("Error","Password is required",parent=self.forget_win)
       elif self.var_new_pass.get()!= self.var_conf_pass.get():
          messagebox.showerror("Error","Password & Confirm password should be same",parent=self.forget_win)
       else:  
          con=sqlite3.connect(database=r'gms.db')
          cur=con.cursor()
          try:
             cur.execute("Update employee set pass=? where eid=?",(self.var_new_pass.get(),self.username.get()))
             con.commit()
             messagebox.showinfo("Success","Password updated sucessfully",parent=self.root)
             self.forget_win.destroy()
          except Exception as ex:
           messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def validate_otp(self):
       if int(self.otp)==int(self.var_otp.get()):
          self.btn_update.config(state=NORMAL)
          self.btn_reset.config(state=DISABLED)
       else:    
          messagebox.showerror("Error","Invalid OTP, Try again",parent=self.forget_win)

    def send_email(self,to_):
       s=smtplib.SMTP('smtp.gmail.com',587)
       s.starttls()
       email_=email_pass.email_
       pass_=email_pass.pass_
       s.login(email_,pass_)
       self.otp=int(time.strftime("%H%M%S"))+int(time.strftime("%S"))
       subj='GMS-Reset Password OTP'
       msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nwith Regards,\nGMS Team'
       msg="Subject:{}\n\n{}".format(subj,msg)
       s.sendmail(email_,to_,msg)
       chk=s.ehlo()
       if chk[0]==250:
          return 's'
       else:
          return 'f'
if __name__=="__main__":  
   import create_db
   root=Tk()
   obj=Login_System(root)
   root.mainloop()    