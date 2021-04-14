from tkinter import *
from tkinter import messagebox
import sqlite3
import tkinter.messagebox as MessageBox
import time
# import curses
import smtplib
import cred
from email.message import EmailMessage

	
# object of TK()
root= Tk()
root.title("Parking Management System")
root.geometry("1920x1080")

#icon

p1 = PhotoImage(file = 'mini logo1.png')
root.iconphoto(True, p1)

#******************************************* raise funtion logic *******************************************************

def raise_frame(frame):
	frame.tkraise()

login_frame = LabelFrame(root, text = "LOGIN",fg="White",bg="black")
frame_home = LabelFrame(root, text = "HOME",fg="White",bg="black")
frame_register = LabelFrame(root, text = "REGISTER",fg="White",bg="black")
frame_slot = LabelFrame(root, text = "Book Your Slot",fg="White",bg="black")
frame_check_out = LabelFrame(root, text = "Check Out",fg="White",bg="black")

for frame in (login_frame,frame_home,frame_register,frame_slot,frame_check_out):
	frame.grid(row=0, column=0, sticky='news')

#******************************************* login logic ****************************************************************
def Submit():#sign in logic

	conn = sqlite3.connect('Car_Management.db')
	c = conn.cursor()
	try:
		global username
		username = t_uname.get()
		
		
		c.execute("SELECT user_name FROM User_data WHERE user_name =?",[t_uname.get()])
		uname=c.fetchone()

		c.execute("SELECT password FROM User_data WHERE password =?",[t_pwd.get()])
		password=c.fetchone()
	
		if t_uname.get() == uname[0] and t_pwd.get() == password[0]:
			answer=messagebox.askquestion("login","login in successfull !! Do you want to login ")
		if answer == 'yes':
				search_home()
				raise_frame(frame_slot)
				clock()
		conn.commit()	
		conn.close()		
	except:
		MessageBox.showwarning('showwarning',"Wrong Credential")
	conn.close()	


#******************************************* Register logic ****************************************************************


def check():#bug slove if two same user's name are login
	try:
		conn = sqlite3.connect('Car_Management.db')
		c = conn.cursor()
		

		global usernameregister
		usernameregister = t_uname_register.get()
			
		c.execute("SELECT rowid, * FROM User_data WHERE user_name =?",[usernameregister])
		uname_register=c.fetchall()
		conn.commit()
		Insert()
		raise_frame(login_frame)
	except sqlite3.IntegrityError:
			messagebox.showerror("Show Error", "Username Is Already Taken") 
def Insert():#insert in user table  
	conn = sqlite3.connect('Car_Management.db')
	c = conn.cursor()
	c.execute("INSERT INTO User_data (first_name,email_id,user_name,password,car_model_name,Car_no) VALUES (?,?,?,?,?,?)",[t_name_register.get(),t_email.get(),t_uname_register.get(),t_pwd_register.get(),t_cmodel_register.get(),t_cnumber_register.get()])
	conn.commit()		


#******************************************* search and print on slot page  logic********************************************
def search_home():#to search name of user and print on slot page
	conn = sqlite3.connect('Car_Management.db')
	
	c = conn.cursor()
	
	c.execute("SELECT rowid, * FROM User_data WHERE user_name =?",[username])
	conn.commit()	
	items=c.fetchone()
	query_label=Label(frame_slot,text=items[1],fg="white",bg="black",font=("calibri",25,"bold"))
	query_label.place(x=370 ,y=185) 
	conn.close()
	return

#******************************************* Slot logic ****************************************************************	

# to get difference between book and available slot * * * * * * * * * * * 

def colour():#colour change green red

	conn = sqlite3.connect('Car_Management.db')
	c = conn.cursor()
	c.execute("SELECT first_name FROM slot ")
	uname=c.fetchall()
	

	# print(uname[0][0])
	for i in range(53):
		# print(uname[i][0])
		

		if (uname[i][0]==''):
			LIST[i].config(bg='green',fg='#000000')
		elif (uname[i][0].isalpha()):
			LIST[i].config(bg='red',fg='white',state= DISABLED )
	conn.close()			
def book_slot(btn):
	search()
	global slot
	slot=btn.config('text')[-1]
	if 'A' in slot:
		type=1
		fare=' 40RS/Hr.'
	elif 'B' in slot:
		type=2
		fare=' 60RS/Hr.'
	elif 'C' in slot:
		type=3
		fare=' 80RS/Hr.'
	else : 
		type = 0

	answer3=messagebox.askquestion("Confirm booking", f"name={take_name} \n book={slot} \n fare= {fare}  ")
	if answer3 == 'yes':
				taken_slot_name(btn)
				update_trans()
				colour()
				mail()

	
def taken_slot_name(bttn):#take slot name
	global name1
	name1=bttn.config('text')[-1]

def mail(): #send mail
	search()

	with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
		smtp.login(cred.sender,cred.password)

		msg = EmailMessage()
		msg['From'] = cred.sender
		msg['To'] = email
		msg['subject'] = 'Slot is successfully Book'
		msg.set_content(f"""Dear Customer,
		{take_name} you have successfully parked your car in slot
		with car model name = {take_car_name}
		with car number = {take_car_number}
		on slot number = {slot}
		Thankyou !""")
		smtp.send_message(msg)

#search for getting name,car number, car model from db. * * * * * * 

def search():#search for getting name,car number, car model from db. * * * * * * 
	conn = sqlite3.connect('Car_Management.db')
	
	
	c = conn.cursor()
	
	c.execute("SELECT rowid, * FROM User_data WHERE user_name =?",[username])

	conn.commit()	
	items=c.fetchone()
	
	global take_name
	take_name=(items[1])

	global email
	email=(items[3])
	
	global take_car_name
	take_car_name=(items[5])
	
	global take_car_number
	take_car_number=(items[6])

	global null
	null = " "
	conn.close()


#clock * * * * * * * *

def clock():
	hour = time.strftime("%I:%M:%S %p")
	date = time.strftime("%m/%d/%Y")
	my_label_time = Label(frame_slot, text="",font=("Helvetica",15), fg="black",bg="white")
	my_label_time.place(x=1650,y=30)

	my_label2_date = Label(frame_slot, text="",font=("Helvetica",15), fg="black",bg="white")
	my_label2_date.place(x=1650,y=70)

	

	my_label_time.config(text=hour)
	my_label_time.after(1000, clock)


	date=my_label2_date.config(text=date)

x = time.strftime("%I:%M:%S %p")

global y
y = time.strftime("%m/%d/%Y")
print(y)

global z
z = time.strftime("%I:%M:%S %p")
print(z)


# update slot data 

def update_trans():#update empty slot from empty to user data
	search()

	conn = sqlite3.connect('Car_Management.db')
	c = conn.cursor()


	#Update Records

	c.execute("UPDATE slot SET first_name = ? WHERE slot_name = ? ",[take_name,name1])
	c.execute("UPDATE slot SET car_model_name = ? WHERE slot_name = ? ",[take_car_name,name1])
	c.execute("UPDATE slot SET Car_no = ? WHERE slot_name = ? ",[take_car_number,name1])

	#add in trans history

	many_Trans_History=[
 				('','','','','','','')
 				]

	c.execute("INSERT INTO Trans_History VALUES (?,?,?,?,?,?,?)", [y,take_name,take_car_name,take_car_number,x,null,name1])

	c.execute("SELECT rowid, * FROM Trans_History")

	

	conn.commit()
	conn.close()

#******************************************* check out logic ************************************************************

# recipt name display * *

def check_out():
	search_check_out()
	


	cus_name.config(text = take_name)
	model_name.config(text = take_car_name)
	car_number_name.config(text = take_car_number)
	slot_number_take.config(text = slot_check)


def search_check_out():
	search()

	conn = sqlite3.connect('Car_Management.db')
	
	c = conn.cursor()
	
	c.execute("SELECT rowid, * FROM slot WHERE first_name = ? ",[take_name])
	conn.commit()
	items=c.fetchone()
	
	global name_check
	name_check=(items[1])
	
	global car_name_check
	car_name_check=(items[2])
	
	global number_check
	number_check=(items[3])

	global slot_check
	slot_check=(items[4])
	

	conn.close()

#Update Records * *
def update_check_out():
	search_check_out()
	clock()

	conn = sqlite3.connect('Car_Management.db')
	c = conn.cursor()

	c.execute("UPDATE slot SET first_name ='' WHERE first_name = ? ",[name_check])
	c.execute("UPDATE slot SET car_model_name = '' WHERE car_model_name = ? ",[car_name_check])
	c.execute("UPDATE slot SET Car_no = ''  WHERE Car_no = ? ",[number_check])
	conn.commit()
	conn.close()

#Update Records in trans history* *
def trans_update():
	search()
	clock()
	conn = sqlite3.connect('Car_Management.db')
	c = conn.cursor()

	c.execute("UPDATE Trans_History SET time_out = ?  WHERE first_name = ? and car_model_name = ? and Car_no = ? and date_ = ? ",[z,take_name,take_car_name,take_car_number,y])
	
	print(5)

	conn.commit()
	conn.close()

#********************************************* login PAGE ***************************************************************

#background photo of login frame 
loginimage=PhotoImage(file="back3.png")
label=Label(login_frame,image=loginimage)
label.pack(fill=BOTH,expand=True)

#white frame of login frame
Frame_login=Frame(login_frame,bg="white")
Frame_login.place(x=660,y=170,height=350,width=500)


#label of login frame
# textrunning = "Hello this is an example text. "
title=Label(login_frame,text= "Login form" ,fg="White",bg="#0B090A",font=("calibri",45,"bold"))
title.place(x=780 ,y=30)
uname=Label(login_frame,text="User Name :" ,fg="black",bg="white",font=("bold",13))
uname.place(x=750 ,y=250)
password=Label(login_frame,text="Password :" ,fg="black",bg="white",font=("bold",13))
password.place(x=750 ,y=310)


t_uname=Entry(login_frame)
t_uname.place(x=860 ,y=250)
t_pwd=Entry(login_frame, show = '*')
t_pwd.place(x=860 ,y=310)


#button of login frame
Newlogi=Button(login_frame,text="Sign Up",fg="White" ,bg="blue" ,font=("calibri",20,"bold") ,command=lambda:[raise_frame(frame_register)])
Newlogi.place(x=900 ,y=390,height=40,width=100)
submit=Button(login_frame,text="Sign in",fg="White" ,bg="green" ,font=("calibri",20,"bold") ,command=Submit)
submit.place(x=780 ,y=390,height=40,width=100) 	





#*******************************************  REGISTER PAGE  **************************************************************** 

#background photo of register page
imageregister=PhotoImage(file="back3.png")
label=Label(frame_register,image=imageregister)
label.pack(fill=BOTH,expand=True)

#white Frame of register page
Frame_login=Frame(frame_register,bg="white")
Frame_login.place(x=640,y=130,height=450,width=500)


# label of register page
title=Label(frame_register,text= "Register Your Account" ,bg="#0B090A",fg="white",font=("bold",29))
title.place(x=710 ,y=30)
name=Label(frame_register,text="Name :" ,bg="#fff",fg="black",font=("bold",14))
name.place(x=740 ,y=175)
email=Label(frame_register,text="Email ID :" ,bg="#fff",fg="black",font=("bold",14))
email.place(x=740 ,y=215)
uname=Label(frame_register,text="User Name :",bg="#fff",fg="black",font=("bold",14))
uname.place(x=740 ,y=255)
password=Label(frame_register,text="Password :" ,bg="#fff",fg="black",font=("bold",14))
password.place(x=740 ,y=295)
vdetails=Label(frame_register,text="Vehicle Details" ,bg="#fff",fg="black",font=("bold",22))
vdetails.place(x=760 ,y=330)

cmodel=Label(frame_register,text="Car Model :" ,bg="#fff",fg="black",font=("bold",14))
cmodel.place(x=740 ,y=370)
cnumber=Label(frame_register,text="Car Number :" ,bg="#fff",fg="black",font=("bold",14))
cnumber.place(x=740 ,y=405)


#entry box of register page
t_name_register=Entry(frame_register)
t_name_register.place(x=890 ,y=175)
t_email=Entry(frame_register)
t_email.place(x=890 ,y=215)
t_uname_register=Entry(frame_register)
t_uname_register.place(x=890 ,y=255)
t_pwd_register=Entry(frame_register, show = '*')
t_pwd_register.place(x=890 ,y=295)

t_cmodel_register=Entry(frame_register)
t_cmodel_register.place(x=890 ,y=370)
t_cnumber_register=Entry(frame_register)
t_cnumber_register.place(x=890 ,y=405)

#button of register page
addmore=Button(frame_register,text="Add More",fg="White" ,bg="#003e53")
addmore.place(x=750 ,y=450)



submit=Button(frame_register,text="Sign Up",fg="White" ,bg="green",command=lambda:[check()])
submit.place(x=800 ,y=500,height=50,width=200)

#********************************************* slot PAGE ***************************************************************
#background photo of login frame 
slotimage=PhotoImage(file="back3.png")
label=Label(frame_slot,image=slotimage)
label.pack(fill=BOTH,expand=True)

# # log out button 
login_btn = PhotoImage(file='log out.png')
image_logout =Label(image=login_btn)

#white frame of login frame
Frame_login=Frame(frame_slot,bg="white")
Frame_login.place(x=500,y=280,height=650,width=900)

#white frame of home frame hori
Frame_home_hor=Frame(frame_slot,bg="white",borderwidth = "10")
Frame_home_hor.place(x=0,y=0,height=140,width=1920)

title=Label(frame_slot,text= "Hello" ,fg="red",bg="black",font=("calibri",35,"bold"))
title.place(x=240 ,y=155)

title=Label(frame_slot,text= "Welcome" ,fg="red",bg="White",font=("calibri",30,"bold"))
title.place(x=830 ,y=8)

title=Label(frame_slot,text= "To" ,fg="black",bg="White",font=("calibri",16,"bold"))
title.place(x=895 ,y=60)

title=Label(frame_slot,text= "Parking Management System " ,fg="red",bg="White",font=("calibri",30,"bold"))
title.place(x=675 ,y=83)


#log out button image 
img_button = Button(frame_slot, image=login_btn, bg="white",fg="black", borderwidth=0 ,command=lambda:[raise_frame(login_frame)])
img_button.place(x=1840 , y=10)

title=Label(frame_slot,text= "Parking Slots" ,fg="white",bg="black",font=("calibri",25,"bold"))
title.place(x=820 ,y=200)

#first floor
title=Label(frame_slot,text= "First Floor" ,fg="#0B090A",bg="White",font=("calibri",35,"bold"))
title.place(x=530 ,y=320)

#button of register page
A1=Button(frame_slot,text="A1",fg="#003e53" ,height=2,width=4,command=lambda:[book_slot(A1)])
A1.place(x=530 ,y=390)

A2=Button(frame_slot,text="A2",fg="#003e53" ,height=2,width=4,command=lambda:[book_slot(A2)])
A2.place(x=600 ,y=390)

A3=Button(frame_slot,text="A3",fg="#003e53" ,height=2,width=4,command=lambda:[book_slot(A3)])
A3.place(x=670 ,y=390)

A4=Button(frame_slot,text="A4",fg="#003e53" ,height=2,width=4,command=lambda:[book_slot(A4)])
A4.place(x=740 ,y=390)

A5=Button(frame_slot,text="A5",fg="#003e53" ,height=2,width=4,command=lambda:[book_slot(A5)])
A5.place(x=810 ,y=390)

A6=Button(frame_slot,text="A6",fg="#003e53" ,height=2,width=4,command=lambda:[book_slot(A6)])
A6.place(x=880 ,y=390)

A7=Button(frame_slot,text="A7",fg="#003e53" ,height=2,width=4,command=lambda:[book_slot(A7)])
A7.place(x=950 ,y=390)

A8=Button(frame_slot,text="A8",fg="#003e53" ,height=2,width=4,command=lambda:[book_slot(A8)])
A8.place(x=1020 ,y=390)

A9=Button(frame_slot,text="A9",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A9)])
A9.place(x=1090 ,y=390)

A10=Button(frame_slot,text="A10",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A10)])
A10.place(x=1160 ,y=390)

A11=Button(frame_slot,text="A11",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A11)])
A11.place(x=1230 ,y=390)

A12=Button(frame_slot,text="A12",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A12)])
A12.place(x=1300 ,y=390)
#second row
A13=Button(frame_slot,text="A13",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A13)])
A13.place(x=530 ,y=440)

A14=Button(frame_slot,text="A14",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A14)])
A14.place(x=600 ,y=440)

A15=Button(frame_slot,text="A15",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A15)])
A15.place(x=670 ,y=440)

A16=Button(frame_slot,text="A16",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A16)])
A16.place(x=740 ,y=440)

A17=Button(frame_slot,text="A17",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A17)])
A17.place(x=810 ,y=440)

A18=Button(frame_slot,text="A18",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A18)])
A18.place(x=880 ,y=440)

A19=Button(frame_slot,text="A19",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A19)])
A19.place(x=950 ,y=440)

A20=Button(frame_slot,text="A20",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A20)])
A20.place(x=1020 ,y=440)

A21=Button(frame_slot,text="A21",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A21)])
A21.place(x=1090 ,y=440)

A22=Button(frame_slot,text="A22",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A22)])
A22.place(x=1160 ,y=440)

A23=Button(frame_slot,text="A23",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A23)])
A23.place(x=1230 ,y=440)

A24=Button(frame_slot,text="A24",fg="#003e53" ,bg="White",height=2,width=4,command=lambda:[book_slot(A24)])
A24.place(x=1300 ,y=440)

#second floor 

title=Label(frame_slot,text= "Second Floor" ,fg="#0B090A",bg="White",font=("calibri",35,"bold"))
title.place(x=530 ,y=490)

B1=Button(frame_slot,text="B1",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B1)])
B1.place(x=530 ,y=560)

B2=Button(frame_slot,text="B2",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B2)])
B2.place(x=600 ,y=560)

B3=Button(frame_slot,text="B3",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B3)])
B3.place(x=670 ,y=560)

B4=Button(frame_slot,text="B4",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B4)])
B4.place(x=740 ,y=560)

B5=Button(frame_slot,text="B5",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B5)])
B5.place(x=810 ,y=560)

B6=Button(frame_slot,text="B6",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B6)])
B6.place(x=880 ,y=560)

B7=Button(frame_slot,text="B7",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B7)])
B7.place(x=950 ,y=560)

B8=Button(frame_slot,text="B8",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B8)])
B8.place(x=1020 ,y=560)

B9=Button(frame_slot,text="B9",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B9)])
B9.place(x=1090 ,y=560)

B10=Button(frame_slot,text="B10",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B10)])
B10.place(x=1160 ,y=560)

B11=Button(frame_slot,text="B11",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B11)])
B11.place(x=1230 ,y=560)

B12=Button(frame_slot,text="B12",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B12)])
B12.place(x=1300 ,y=560)
#second row
B13=Button(frame_slot,text="B13",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B13)])
B13.place(x=800 ,y=640)

B14=Button(frame_slot,text="B14",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B14)])
B14.place(x=870 ,y=640)

B15=Button(frame_slot,text="B15",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B15)])
B15.place(x=940 ,y=640)

B16=Button(frame_slot,text="B16",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B16)])
B16.place(x=1010 ,y=640)

B17=Button(frame_slot,text="B17",fg="#003e53" ,bg="White",height=3,width=5,command=lambda:[book_slot(B17)])
B17.place(x=1080 ,y=640)

#third floor 

title=Label(frame_slot,text= "Third Floor" ,fg="#0C090A",bg="White",font=("caliCri",35,"bold"))
title.place(x=530 ,y=690)

C1=Button(frame_slot,text="C1",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C1)])
C1.place(x=620 ,y=760)

C2=Button(frame_slot,text="C2",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C2)])
C2.place(x=730 ,y=760)

C3=Button(frame_slot,text="C3",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C3)])
C3.place(x=840 ,y=760)

C4=Button(frame_slot,text="C4",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C4)])
C4.place(x=950 ,y=760)

C5=Button(frame_slot,text="C5",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C5)])
C5.place(x=1060 ,y=760)

C6=Button(frame_slot,text="C6",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C6)])
C6.place(x=1170 ,y=760)
#second row
C7=Button(frame_slot,text="C7",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C7)])
C7.place(x=620 ,y=830)

C8=Button(frame_slot,text="C8",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C8)])
C8.place(x=730 ,y=830)

C9=Button(frame_slot,text="C9",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C9)])
C9.place(x=840 ,y=830)

C10=Button(frame_slot,text="C10",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C10)])
C10.place(x=950 ,y=830)

C11=Button(frame_slot,text="C11",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C11)])
C11.place(x=1060 ,y=830)

C12=Button(frame_slot,text="C12",fg="#003e53" ,bg="White",height=3,width=8,command=lambda:[book_slot(C12)])
C12.place(x=1170 ,y=830)

#top button
Check_out=Button(frame_slot,text="Check out",fg="#0000ff" ,bg="White",height=1,width=10,padx=10,pady=5,font=("roboto",15,"bold"),borderwidth=0 ,command=lambda:[raise_frame(frame_check_out),check_out()])
Check_out.place(x=20 ,y=60)

# Feed_back=Button(frame_slot,text="Feed back",fg="green" ,bg="White",height=1,width=10,padx=10,pady=5,font=("roboto",10,"bold"),borderwidth=0)
# Feed_back.place(x=135 ,y=60)

# About=Button(frame_slot,text="About",fg="#121212" ,bg="White",height=1,width=10,padx=10,pady=5,font=("roboto",10,"bold"),borderwidth=0)
# About.place(x=250 ,y=60)

LIST=[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,A23,A24,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11,B12,B13,B14,B15,B16,B17,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12]

colour()

#********************************************* Check Out PAGE ***************************************************************

#background photo of login frame 
checkoutimage=PhotoImage(file="back3.png")
label=Label(frame_check_out,image=checkoutimage)
label.pack(fill=BOTH,expand=True)

#white Frame of register page
Frame_login=Frame(frame_check_out,bg="white")
Frame_login.place(x=640,y=130,height=450,width=500)

#labels

vdetails=Label(frame_check_out,text="Receipt" ,bg="#fff",fg="black",font=("bold",40))
vdetails.place(x=780 ,y=165)

name=Label(frame_check_out,text="Customer Name :" ,bg="#fff",fg="black",font=("bold",14))
name.place(x=700 ,y=235)

cus_name=Label(frame_check_out,text= "username" ,bg="#fff",fg="black",font=("bold",14))
cus_name.place(x=870 ,y=235)	

cmodel=Label(frame_check_out,text="Car Model :" ,bg="#fff",fg="black",font=("bold",14))
cmodel.place(x=700 ,y=280)

model_name=Label(frame_check_out,text="Model name :" ,bg="#fff",fg="black",font=("bold",14))
model_name.place(x=870 ,y=280)

cnumber=Label(frame_check_out,text="Car Number :" ,bg="#fff",fg="black",font=("bold",14))
cnumber.place(x=700 ,y=325)

car_number_name=Label(frame_check_out,text="Car Number :" ,bg="#fff",fg="black",font=("bold",14))
car_number_name.place(x=870 ,y=325)

slot_number=Label(frame_check_out,text="Slot NO :" ,bg="#fff",fg="black",font=("bold",14))
slot_number.place(x=700 ,y=355)

slot_number_take=Label(frame_check_out,text="manish" ,bg="#fff",fg="black",font=("bold",14))
slot_number_take.place(x=790 ,y=355)


Payment=Label(frame_check_out,text="Payment Option :" ,bg="#fff",fg="black",font=("bold",14))
Payment.place(x=700 ,y=395)

Payment=Label(frame_check_out,text="Payment Option :" ,bg="#fff",fg="black",font=("bold",14))
Payment.place(x=700 ,y=395)

#button

# # log out button 
Gpay_btn = PhotoImage(file='Gpay.png')
image_Gpay =Label(image=Gpay_btn)

PhonePe_btn = PhotoImage(file='Phonepe.png')
image_PhonePe =Label(image=PhonePe_btn)

Paytm_btn = PhotoImage(file='Paytm.png')
image_Paytm =Label(image=Paytm_btn)

#pay button image 
img_button_Gpay = Button(frame_check_out, image=Gpay_btn, bg="white",fg="black", borderwidth=0 )
img_button_Gpay.place(x=700 , y=425)

img_button_Phonepe = Button(frame_check_out, image=PhonePe_btn, bg="white",fg="black", borderwidth=0 )
img_button_Phonepe.place(x=800 , y=425)

img_button_Paytm = Button(frame_check_out, image=Paytm_btn, bg="white",fg="black", borderwidth=0 )
img_button_Paytm.place(x=900 , y=425)

img_button = Button(frame_check_out, image=login_btn, bg="white",fg="black", borderwidth=0 ,command=lambda:[search_check_out(),update_check_out(),raise_frame(login_frame),trans_update()])
img_button.place(x=1080 , y=130)
raise_frame(login_frame)


# infinte loop till close
root.mainloop()
