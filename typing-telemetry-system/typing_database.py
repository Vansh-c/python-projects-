import mysql.connector 

# connect MySQL
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vansh2006"   # change according to your MySQL password
)

cursor= con.cursor() 
cursor.execute("CREATE DATABASE IF NOT EXISTS typing_database") 
cursor.execute("use typing_database") 
cursor.execute("CREATE TABLE IF NOT EXISTS typing_stats(sr INT AUTO_INCREMENT PRIMARY KEY , speed FLOAT , accuracy FLOAT)")

def add_data(speed  , accuracy) :
    cursor.execute("INSERT INTO typing_stats(speed, accuracy) values(%s , %s)" , (speed, accuracy))
    con.commit() 


def show_data():
    print("your database")
    cursor.execute("SELECT * FROM typing_stats") 

    for cur in cursor:
        print(cur) 

    print("\n")


def clear_data():
    cursor.execute('TRUNCATE FROM typing_stats') 
    print('table cleared') 


