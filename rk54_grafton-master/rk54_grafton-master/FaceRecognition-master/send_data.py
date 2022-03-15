import sqlite3
import socket
connection=sqlite3.connect('data.db')
cursor=connection.cursor()
host='localhost'
port=3559
_id='1'

data=[]
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)
c,addr=s.accept()
print("connection from: ", str(addr))

select_query="SELECT criminal_name, max(count) FROM hotspot GROUP BY criminal_name"
result=cursor.execute(select_query)
for row in result:
    print(row)
    data.append(row)
data_str=str(data)
c.send(data_str.encode()) 
c.send(_id.encode())   
c.close()

# delete_query="DELETE FROM hotspot"
# cursor.execute(delete_query)

connection.commit()
connection.close()

