import socket,threading

# host IP address
IP = '127.0.0.1'
PORT = 5000

threads = []
clients = []
cores_and_clients = []
threads_listen =[]
total_cores = 0
low = 0

md5_string = "827ccb0eea8a706c4c34a16891f84e7b"


class Listener(threading.Thread):
    def __init__(self, client_socket):
        """ constructor, setting initial variables """
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        global  clients
        try:
            number = self.client_socket.recv(1024).decode()
            if number:
                print ("\nThe number is " + number + " !")
            for client in clients:
                if client!= self.client_socket:
                    client.send("STOP".encode())
        except Exception as ex:
            print(ex)

class CoresConNecTer(threading.Thread):
    def __init__(self, client_socket):
        """ constructor, setting initial variables """
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        global cores_and_clients
        global total_cores
        global md5_string
        self.client_socket.send(md5_string.encode())
        num_cores = int(self.client_socket.recv(1024).decode())
        total_cores += num_cores
        cores_and_clients.append((num_cores,self.client_socket))

class Server(object):
    def __init__(self):
        self.socket=socket.socket()
        self.socket.bind((IP,PORT))
        self.socket.listen(3)
        self.socket.settimeout(5)
        self.client_socket = None
        self.client_address = None

    def get_clients(self):
        global clients
        while True:
            try:
                self.client_socket, self.client_address = self.socket.accept()
                print(self.client_address)
                clients.append(self.client_socket)
            except Exception as ex:
                print("time out")
                break

    def send_ranges(self):
        global cores_and_clients
        global total_cores
        global clients
        try:
            unit = int(90000/total_cores)
            start = 9999
            for one_core in cores_and_clients:
                max = start + 1 + one_core[0] * unit
                if max>99999: max = 99999
                message =str(start+1) + ',' + str(max)
                one_core[1].send(message.encode())
                start = max
        except Exception as ex:
            print("No clients have tried to connect")

if __name__ == '__main__':
    server_object = Server()
    server_object.get_clients()

    for client in clients:
        connector_object = CoresConNecTer(client)
        threads.append((connector_object, client))
        connector_object.start()
        connector_object.join()
    server_object.send_ranges()

    for client in clients:
        listener_object = Listener(client)
        threads_listen.append(listener_object)
        listener_object.start()

