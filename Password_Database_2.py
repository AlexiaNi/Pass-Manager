import sqlite3

connectivity = sqlite3.connect('Master_2.db')

cursor = connectivity.cursor()

cursor.execute("""CREATE TABLE Master_Password_2(
       Master_pass text     
 )""")

connectivity.commit()
connectivity.close()
