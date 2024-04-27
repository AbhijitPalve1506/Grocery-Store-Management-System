from tkinter import*
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import sqlite3
import time
import smtplib
import email_pass
import os, sys
import tempfile
def resource_path(relative_path):
   try:
      base_path=sys._MEIPASS
   except Exception:
      base_path=os.path.abspath(".")
   return os.path.join(base_path,relative_path)
class BillClass(Frame):
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")  
        self.root.title("Grocery Store Management System | Developed By Abhijit")   
        self.root.config(bg="black")
        self.cart_list=[]
        self.chk_print=0
        #=====Title=======
        self.icon_title=Image.open(resource_path("images/logo1.png"))
        self.icon_title=ImageTk.PhotoImage(self.icon_title)
        title=Label(self.root,image=self.icon_title,text="Grocery Store Management System",compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20)
        title.place(x=0,y=0,relwidth=1,height=70)
        #=====btn logout===
        btn_logout=Button(self.root,text="Logout",comman=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2")
        btn_logout.place(x=1100,y=10,height=50,width=150)
        #=====clock=======
        self.lbl_clock=Label(self.root,text="Welcome to Grocery Store Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        #=====Product_Frame====
        self.var_search=StringVar()
        ProductFrame1=Frame(self.root,bd=0,relief=RIDGE,bg="black")
        ProductFrame1.place(x=6,y=110,width=400,height=520)
        pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#184a45",fg="white").pack(side=TOP,fill=X)
        #====Product Search Frame=========
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=0,relief=RIDGE,bg="black")
        ProductFrame2.place(x=6,y=42,width=380,height=90)
        lbl_search=Label(ProductFrame2,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="black",fg="lightgreen").place(x=2,y=5)
        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="black",fg="white").place(x=5,y=45) 
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=140,y=47,width=150,height=22)   
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=300,y=45,width=70,height=24)
        btn_show_all=Button(ProductFrame2,text="Show All",font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=290,y=10,width=80,height=24)
        #====Product Details Frame=========
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=4,y=140,width=380,height=345)
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid",text="P ID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="Quantity")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=60)
        self.product_Table.column("qty",width=60)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="Note: Enter 0 Quantity to remove product from the cart",font=("goudy old style",13),anchor="w",bg="black",fg="red").pack(side=BOTTOM,fill=X)
        #=====CustomerFrame====
        self.var_cname=StringVar()
        self.var_cmail=StringVar()  
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=0,relief=RIDGE,bg="black")
        CustomerFrame.place(x=420,y=110,width=500,height=120)
        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15,"bold"),bg="black",fg="white").place(x=5,y=32) 
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",15),bg="lightyellow").place(x=70,y=35,width=120,height=20) 
        lbl_contact=Label(CustomerFrame,text="Email",font=("times new roman",15,"bold"),bg="black",fg="white").place(x=220,y=32) 
        txt_contact=Entry(CustomerFrame,textvariable=self.var_cmail,font=("times new roman",15),bg="lightyellow").place(x=290,y=35,width=185,height=20)   
        lbl_name=Label(CustomerFrame,text="Contact no",font=("times new roman",15,"bold"),bg="black",fg="white").place(x=5,y=65) 
        txt_name=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",15),bg="lightyellow").place(x=115,y=70,width=160,height=20) 
        #====Cal Cart Frame=========
        Cal_Cart_Frame=Frame(self.root,bd=0,relief=RIDGE,bg="black")
        Cal_Cart_Frame.place(x=420,y=215,width=500,height=300)
        #====Calculator Frame=========
        self.var_cal_input=StringVar()
        Cal_Frame=Frame(Cal_Cart_Frame,bd=8,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=3,width=268,height=287)
        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=("aerial",15,"bold"),bd=10,relief=GROOVE,width=21,state="readonly",justify="right")
        txt_cal_input.grid(row=0,columnspan=4)
        btn_7=Button(Cal_Frame,text="7",command=lambda:self.get_input(7),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text="8",command=lambda:self.get_input(8),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text="9",command=lambda:self.get_input(9),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text="+",command=lambda:self.get_input('+'),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=1,column=3)
        btn_4=Button(Cal_Frame,text="4",command=lambda:self.get_input(4),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text="5",command=lambda:self.get_input(5),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text="6",command=lambda:self.get_input(6),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text="-",command=lambda:self.get_input('-'),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=2,column=3)
        btn_1=Button(Cal_Frame,text="1",command=lambda:self.get_input(1),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text="2",command=lambda:self.get_input(2),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text="3",command=lambda:self.get_input(3),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text="*",command=lambda:self.get_input('*'),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=3,column=3)
        btn_0=Button(Cal_Frame,text="0",command=lambda:self.get_input(0),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text="c",command=self.clear_cal,font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text="=",command=self.perform_cal,font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text="/",command=lambda:self.get_input('/'),font=("aerial",15,"bold"),bd=5,width=4,pady=5,cursor="hand2").grid(row=4,column=3)
        #====Cart Frame=========
        cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=275,y=3,width=215,height=287)
        self.cartTitle=Label(cart_Frame,text="Cart \t Total Product: [0]",font=("goudy old style",12),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)
        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)
        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid",text="P ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Quantity")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=60)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        #=====Add Cart Widgets Frame=====
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        Add_CartWidgetsFrame=Frame(self.root,bd=0,relief=RIDGE,bg="black")
        Add_CartWidgetsFrame.place(x=420,y=530,width=500,height=100)
        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",14),bg="black",fg="white").place(x=5,y=2)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",14),bg="lightgray",state="readonly").place(x=5,y=30,width=190,height=22)
        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",14),bg="black",fg="white").place(x=210,y=2)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",14),bg="lightgray",state="readonly").place(x=210,y=30,width=120,height=22)
        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",14),bg="black",fg="white").place(x=350,y=2)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",14),bg="lightyellow").place(x=350,y=30,width=120,height=22)
        self.lbl_instock=Label(Add_CartWidgetsFrame,text="In Stock",font=("goudy old style",14,"bold"),bg="black",fg="white")
        self.lbl_instock.place(x=0,y=55,width=120,height=40)
        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",14,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=60,width=100,height=25)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",14,"bold"),bg="lightgray",cursor="hand2").place(x=300,y=60,width=160,height=25)
        #==========billing area========
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=930,y=110,width=330,height=380)
        bTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",18,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        #==========billing buttons======
        billMenuFrame=Frame(self.root,bd=0,relief=RIDGE,bg="black")
        billMenuFrame.place(x=930,y=500,width=330,height=130)
        self.lbl_amt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",14,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amt.place(x=3,y=5,width=100,height=60)
        self.lbl_disc=Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",14,"bold"),bg="#8bc34a",fg="white")
        self.lbl_disc.place(x=113,y=5,width=100,height=60)
        self.lbl_netPay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",14,"bold"),bg="#607d8b",fg="white")
        self.lbl_netPay.place(x=223,y=5,width=100,height=60)
        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white",cursor="hand2")
        btn_print.place(x=2,y=75,width=100,height=50)
        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,font=("goudy old style",14,"bold"),bg="#8bc34a",fg="white",cursor="hand2")
        btn_clear_all.place(x=113,y=75,width=100,height=50)
        btn_generate=Button(billMenuFrame,text="Generate/Save\nBill",command=self.generate_bill,font=("goudy old style",12,"bold"),bg="#607d8b",fg="white",cursor="hand2")
        btn_generate.place(x=223,y=75,width=100,height=50)
        self.show()      
        #self.bill_top()
        self.update_date_time()
#=====================All Function=====
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self): 
        self.var_cal_input.set('')   

    def perform_cal(self):
        result=self.var_cal_input.get()   
        self.var_cal_input.set(eval(result)) 
  
    def show(self):
         con=sqlite3.connect(database=r'gms.db')
         cur=con.cursor()
         try:
              cur.execute("select pid,name,price,qty,status from product where status='Active'")
              rows=cur.fetchall()
              self.product_Table.delete(*self.product_Table.get_children())
              for row in rows:
                   self.product_Table.insert('',END,values=row)
         except Exception as ex:
              messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def search(self):
         con=sqlite3.connect(database=r'gms.db')
         cur=con.cursor()
         try: 
              if self.var_search.get()=="": 
                 messagebox.showerror("Error","search input should be required",parent=self.root)                     
              else:
                 cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                 rows=cur.fetchall()
                 if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                 else:
                      messagebox.showerror("Error","No record found!!!",parent=self.root)      
         except Exception as ex:
              messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev): 
         f=self.product_Table.focus() 
         content=(self.product_Table.item(f))
         row=content['values']
         self.var_pid.set(row[0])
         self.var_pname.set(row[1])
         self.var_price.set(row[2])                   
         self.var_stock.set(row[3])
         self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
         self.var_qty.set('1')

    def get_data_cart(self,ev): 
         f=self.CartTable.focus() 
         content=(self.CartTable.item(f))
         row=content['values']
         self.var_pid.set(row[0])
         self.var_pname.set(row[1])
         self.var_price.set(row[2])
         self.var_qty.set(row[3])                    
         self.var_stock.set(row[4])
         self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")    

    def add_update_cart(self):
         con=sqlite3.connect(database=r'gms.db')
         cur=con.cursor()
         try:
              if self.var_pid.get()=='':
                 messagebox.showerror("Error","Please select product from the list",parent=self.root) 
              elif self.var_qty.get()=='':
                 messagebox.showerror("Error","Quantity is Required",parent=self.root)
              elif int(self.var_qty.get())>int(self.var_stock.get()):
                 messagebox.showerror("Error","Invalid Quantity",parent=self.root)  
              else:    
                 #price_cal=(int(self.var_qty.get())*float(self.var_price.get()))
                 #price_cal=float(price_cal) 
                 cur.execute("Insert into customer (name,mail) values(?,?)",(
                            self.var_cname.get(),
                            self.var_cmail.get()))
                 con.commit()
                 price_cal=self.var_price.get()
                 cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
                 #=======Update_cart=====
                 present='no'
                 index_=0
                 for row in self.cart_list:
                     if self.var_pid.get()==row[0]:        
                         present='yes'
                         break
                     index_+=1
                 #print(present,index_)
              if present=='yes':
                 op=messagebox.askyesno("confirm","Product already present\nDo you want to Update| Remove from the Cart List",parent=self.root)    
                 if op==True:
                     if self.var_qty.get()=="0":
                         self.cart_list.pop(index_)
                     else:
                         #self.cart_list[index_][2]=price_cal #price
                         self.cart_list[index_][3]=self.var_qty.get() #qty    
              else:          
                 self.cart_list.append(cart_data)
              self.show_cart()
              self.bill_update()
         except Exception as ex:
              messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)          

    def bill_update(self):
         self.bill_amt=0
         self.net_pay=0
         self.discount=0
         for row in self.cart_list:
            self.bill_amt=self.bill_amt+(float(row[2])*int(row[3]))
         self.discount=(self.bill_amt*5)/100   
         self.net_pay=self.bill_amt-(self.bill_amt*5)/100
         self.lbl_amt.config(text=f'Bill Amt\n{str(self.bill_amt)}')
         self.lbl_netPay.config(text=f'Net Pay\n{str(self.net_pay)}')
         self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
         try:     
              self.CartTable.delete(*self.CartTable.get_children())
              for row in self.cart_list:
                   self.CartTable.insert('',END,values=row)
         except Exception as ex:
              messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def generate_bill(self):
        con=sqlite3.connect(database=r'gms.db')
        cur=con.cursor()
        try:
          if self.var_cname.get()=='' or self.var_cmail.get()=='' or self.var_contact.get()=='':
              messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
          elif len(self.cart_list)==0:
              messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)    
          else:
             cur.execute("select mail from customer where name=?",(self.var_cname.get(),))
             mail=cur.fetchone()
             if mail==None:
                 messagebox.showerror("Error","Invalid Email,try again",parent=self.root)
             chk=self.send_email(mail[0])
             if chk=='f':
                  messagebox.showerror("Error","Connection Error,try again",parent=self.root)  
             else:
                  #===Bill Top======
                  self.bill_top()         
                  #===Bill Middle===
                  self.bill_middle()
                  #===Bill Bottom===
                  self.bill_bottom()
                  fp=open(f'bill/{str(self.invoice)}.txt','w')
                  fp.write(self.txt_bill_area.get('1.0',END))
                  fp.close()
                  messagebox.showinfo('Saved',"Bill has been generated/saved in Backend",parent=self.root)
                  self.chk_print=1
        except Exception as ex:
         messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    

    def bill_top(self):
        #print(invoice)
        bill_top_temp=f'''
\tXYZ-Grocery Store,
\tMumbai-400033  
{str("="*38)}
 Customer Name: {self.var_cname.get()}
 Email: {self.var_cmail.get()}
 Ph No.: {self.var_contact.get()}
 Bill No.{str(self.invoice)}\t\tDate:{str(time.strftime("%d/%m/%Y"))}   
{str("="*38)}
 Product Name\t\tQTY\tPrice
{str("="*38)}'''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'gms.db')
        cur=con.cursor()
        try:
          for row in self.cart_list:            
            pid=row[0]
            name=row[1]
            qty=int(row[4])-int(row[3])
            if int(row[3])==int(row[4]):
                status='Inactive'
            if int(row[3])!=int(row[4]):
                status='Active'    
            price=float(row[2])*int(row[3])
            price=str(price)
            self.txt_bill_area.insert(END,"\n "+name+"\t\t"+row[3]+"\tRs."+price)
            #====Update qty in product table====
            cur.execute("update product set qty=?,status=? where pid=?",(
               qty,
               status,
               pid
            ))
            con.commit()
          con.close()
          self.show()            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*38)}
 Bill Amount\t\tRs.{self.bill_amt}
 Discount\t\tRs.{self.discount}
 Net Pay\t\tRs.{self.net_pay}
{str("="*38)}\n
'''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')                    
        self.var_stock.set('')
        self.lbl_instock.config(text=f"In Stock")

    def clear_all(self):
        del self.cart_list[:]  
        self.var_cname.set('')
        self.var_cmail.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Grocery Store Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showinfo('print',"Please generate bill, to print the receipt",parent=self.root)      
    
    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def send_email(self,to_):
       self.invoice=str(int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y")))
       s=smtplib.SMTP('smtp.gmail.com',587)
       s.starttls()
       email_=email_pass.email_
       pass_=email_pass.pass_
       s.login(email_,pass_)
       subj='GMS-Customer Order'
       msg=f'Dear Customer,\n\nYour bill {str(self.invoice)} has been successfully generated.\n\nwith Regards,\nGMS Team'
       msg="Subject:{}\n\n{}".format(subj,msg)
       s.sendmail(email_,to_,msg)
       chk=s.ehlo()
       if chk[0]==250:
          return 's'
       else:
          return 'f'    

if __name__=="__main__":
        root=Tk()  
        obj=BillClass(root)        
        root.mainloop()      