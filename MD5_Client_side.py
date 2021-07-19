import socket, multiprocessing, hashlib, threading

# host IP address
IP = '127.0.0.1'
PORT = 5000
stop = True

class Listener(threading.Thread):
    def __init__(self, server_socket):
        """ constructor, setting initial variables """
        threading.Thread.__init__(self)
        self.server_socket = server_socket

    def run(self):
        global stop
        message = self.server_socket.recv(1024).decode()
        print(message)
        stop=False


class Client:
    def __init__(self):
        self.client=socket.socket()
        self.client.connect((IP,PORT))
        self.md5_string = self.client.recv(1024).decode()
        self.client.send(str(multiprocessing.cpu_count()).encode())

    def get_socket(self):
        return self.client

    def send(self,data):
        self.client.send(data.encode())

    def receiving(self):
        data =self.client.recv(1024).decode()
        return data

    def close_socket(self):
        self.client.close()

    def check(self, ranges, thread):
        global stop
        min = ranges.split(',')[0]
        max = ranges.split(',')[1]
        thread.start()

        for x in range (int(min),int(max)):
            if stop:
                if (hashlib.md5(str(x).encode()).hexdigest()) == self.md5_string:
                    print(x)
                    self.client.send(str(x).encode())
                    break
            else:
                self.client.close()
                break

if __name__ == "__main__":
    client_object = Client()
    listener_object = Listener(client_object.get_socket())
    client_object.check(client_object.receiving(), listener_object)



