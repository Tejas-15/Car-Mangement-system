#Imports

import sqlite3




# Connect to SQLite3 Database
conn = sqlite3.connect('Car_Management.db')

# Create a cursor
c = conn.cursor()

#create a table 
c.execute("CREATE TABLE IF NOT EXISTS slot (first_name text,car_model_name text,Car_no text,slot_name text)")

#insert
many_slot=[
 				('','','','A1'),
 				('','','','A2'),
 				('','','','A3'),
 				('','','','A4'),
 				('','','','A5'),
 				('','','','A6'),
 				('','','','A7'),
 				('','','','A8'),
 				('','','','A9'),
 				('','','','A10'),
 				('','','','A11'),
 				('','','','A12'),
 				('','','','A13'),
 				('','','','A14'),
 				('','','','A15'),
 				('','','','A16'),
 				('','','','A17'),
 				('','','','A18'),
 				('','','','A19'),
 				('','','','A20'),
 				('','','','A21'),
 				('','','','A22'),
 				('','','','A23'),
 				('','','','A24'),
 				('','','','B1'),
 				('','','','B2'),
 				('','','','B3'),
 				('','','','B4'),
 				('','','','B5'),
 				('','','','B6'),
 				('','','','B7'),
 				('','','','B8'),
 				('','','','B9'),
 				('','','','B10'),
 				('','','','B11'),
 				('','','','B12'),
 				('','','','B13'),
 				('','','','B14'),
 				('','','','B15'),
 				('','','','B16'),
 				('','','','B17'),
 				('','','','C1'),
 				('','','','C2'),
 				('','','','C3'),
 				('','','','C4'),
 				('','','','C5'),
 				('','','','C6'),
 				('','','','C7'),
 				('','','','C8'),
 				('','','','C9'),
 				('','','','C10'),
 				('','','','C11'),
 				('','','','C12'),
 				]

c.executemany("INSERT INTO slot VALUES (?,?,?,?)", many_slot)

c.execute("SELECT rowid, * FROM slot")


items=c.fetchall()


for item in items:
	print(str(item[0]) + "\t\t" + item[1] + "\t\t" + item[2] + "  \t\t\t" + str(item[3]) + "  \t\t" + str(item[4])) 
	
#commit our command 
conn.commit()

#close connection
conn.close()

