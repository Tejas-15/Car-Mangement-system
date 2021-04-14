#Imports

import sqlite3



# Connect to SQLite3 Database
conn = sqlite3.connect('Car_Management.db')

# Create a cursor
c = conn.cursor()

#create a table 
c.execute("CREATE TABLE IF NOT EXISTS Trans_History (Date_ integer,first_name text,car_model_name text,Car_no text,time_in integer,time_out integer,slot_name text)")




# many_Trans_History=[
#  				('','','','','','','A1'),
#  				('','','','','','','A2'),
#  				]

# c.execute("INSERT INTO Trans_History VALUES (?,?,?,?,?,?,?)",many_Trans_History)

c.execute("SELECT rowid, * FROM Trans_History")


items=c.fetchall()




	
#commit our command 
conn.commit()

#close connection
conn.close()

