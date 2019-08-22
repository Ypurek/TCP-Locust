import socket, random as r

# address
SERVER_ADDRESS = ('0.0.0.0', 8888)
BUFF_SIZE = 128
ENCODING = 'utf-8'

session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
session.bind(SERVER_ADDRESS)
session.listen(10)
print('server started')

while True:
    connection, address = session.accept()
    data = connection.recv(BUFF_SIZE)
    str_data = data.decode(ENCODING)
    if str_data.lower() == 'hello':
        connection.send(bytes('world', encoding=ENCODING))
    elif str_data.lower() == 'get yes':
        connection.send(bytes(r.choice(('yes', 'no')), encoding=ENCODING))
    else:
        connection.send(bytes('default response', encoding=ENCODING))

    connection.close()
