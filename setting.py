from PyQt6 import uic
from PyQt6.QtWidgets import QApplication,QFileDialog,QWidget ,QMainWindow,QTextEdit,QTableWidget,QTableWidgetItem
import runpy
import sys,os
import subprocess
class settings(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('settingsPI.ui', self)
        self.file= "arp_spoofer.py"
        self.run.clicked.connect(self.files(self.file))
        self.show()
    def get_ip_address(self,interface):
        try:
            # use ifconfig command and find the ip address
            ifconfig_output = subprocess.run(["ifconfig", interface], stdout=subprocess.PIPE)
            ip_address = ifconfig_output.stdout.decode().split("inet ")[1].split(" ")[0]
            return ip_address
        except Exception as e:
            print(e)
    def files(self,file):
        if file=="arp_spoofer.py":
            self.name_file = "./"+ file
            self.ip_address = self.get_ip_address("eth0")
            self.ip_address = self.ipbox.text()
            self.new_ip = self.ip_address[:self.ip_address.rindex('.') + 1] + '2'
            self.arg1 = "-t" + self.ipbox.text()
            self.arg2 = "-s" + self.new_ip
            subprocess.Popen([self.name_file, self.arg1, self.arg2])
        elif file=="mac_changer.py":
            self.name_file = "python3 " + file
            self.arg1 = "-i" + self.ipbox.text()
            subprocess.Popen([self.name_file, self.arg1])
        elif file=="dns_spoofer.py":
            self.name_file = "./" + file
            self.ip_address = self.get_ip_address("eth0")
            ip_address = self.ipbox.text()
        elif file=="network_scanner.py":
            self.name_file = "./" + file
            self.ip_address = self.get_ip_address("eth0")
            ip_address = self.ipbox.text()
        """"
        elif file=="arp_spoofer.py":
            self.name_file = "./" + file
            self.ip_address = self.get_ip_address("eth0")
            ip_address = self.ipbox.text()
        elif file=="arp_spoofer.py":
            self.name_file = "./" + file
            self.ip_address = self.get_ip_address("eth0")
            ip_address = self.ipbox.text()
            """""
app = QApplication(sys.argv)
window = UI()
window.show()
app.exec()

