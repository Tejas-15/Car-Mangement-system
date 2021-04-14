#Imports
import sqlite3

# Connect to SQLite3 Database
conn = sqlite3.connect('Car_Management.db')

# Create a cursor
c = conn.cursor()

#create a table 
c.execute("CREATE TABLE IF NOT EXISTS User_data (first_name text ,user_name text PRIMARY KEY ,email_id text ,password text ,car_model_name text ,Car_no text)")

#insert
many_Car_Management=[
 				('tejas','tej@24','tkadam252@gmail.com','tejas123','AUDI','MH04BG7788'),
 				('manish','mj@11','manishjalui11@gmail.com','manish123','i20','MH05AS5650'),
 				('kartik','shade@11','karkerakartik27@gmail.com','kartik23','BMW','MH06GH0595'),
 				('rushank','Rwani@15','Rushankrush@gmail.com','rushank123','AUDI','MH92DF5654'),
 				('pranavi','pranavi@08','pranavibhambare8@gmail.com','pranavi123','JEEP COMPASS','MH05QW0046'),
 				('Saniya','js','saniyazad75@gmail.com','0','JEEP ','MH05QW0056')
 				]
c.executemany("INSERT INTO User_data VALUES (?,?,?,?,?,?)", many_Car_Management)
conn.commit()
# #Display
c.execute("SELECT rowid, * FROM User_data")

items=c.fetchall()

# print("No" + "\t\tDATE" + "\t\tNAME" + "\t\tUserid" + "\t\tPassword " + "\t\tCar_Model_Name" + "\t\tCar_no" + "\t\ttime_in" + "\t\ttime_out" )
# print("-----"  + "\t\t------" + "\t\t------" + "\t\t-----------" + "\t\t----------" + "\t---------" + "\t----------")
for item in items:
	print(str(item[0]) + "\t\t" + item[1] + "\t\t" + item[2] + "  \t\t\t" + str(item[3]) + "  \t\t" + str(item[4]) + "  \t\t" + str(item[5])) 
	
#commit our command 
conn.commit()

#close connection
conn.close()



