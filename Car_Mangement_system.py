#Imports
import sqlite3

# Connect to SQLite3 Database
conn = sqlite3.connect('Car_Management.db')

# Create a cursor
c = conn.cursor()

#create a table 
c.execute("CREATE TABLE IF NOT EXISTS User_data (first_name text ,user_name text PRIMARY KEY ,email_id text ,password text ,car_model_name text ,Car_no text)")

conn.commit()

#close connection
conn.close()
