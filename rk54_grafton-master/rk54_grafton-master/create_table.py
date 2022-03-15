import sqlite3
connection=sqlite3.connect('data.db')
cursor=connection.cursor()
# create_table="CREATE TABLE hotspot (criminal_name text(25), Ip_Cam text(50))"
# cursor.execute(create_table)

select_query="SELECT * FROM hotspot"
result=cursor.execute(select_query)
for row in result:
    print(row)

connection.commit()
connection.close()