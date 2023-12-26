

import mysql.connector

# Connect to the MySQL server (replace with your actual database credentials)
dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
)

# Create a cursor object
cursorObject = dataBase.cursor()

# Create the database
cursorObject.execute("CREATE DATABASE IF NOT EXISTS menu")

# Close the cursor and connection
cursorObject.close()
dataBase.close()

print("Database 'menu' created successfully!")
