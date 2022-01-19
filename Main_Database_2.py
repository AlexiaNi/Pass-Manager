import sqlite3

connectivity = sqlite3.connect('Pass_2.db')
cursor = connectivity.cursor()

cursor.execute("""CREATE TABLE Passes_2(
       Platform text,
       URL text,
       Password text     


  )""")

connectivity.commit()
connectivity.close()