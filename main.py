import sys
from functools import partial
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication,QMainWindow,QWidget,QMessageBox,QPushButton
import runpy
import subprocess
class settings(QtWidgets.QWidget):
    def __init__(self,arg):
        super().__init__()
        uic.loadUi('settingsPI.ui', self)
        self.file= arg
        self.run.clicked.connect(partial(self.files,self.file))
        self.show()
    def get_ip_address(self,interface):
        try:
            # use ifconfig command and find the ip address
            ifconfig_output = subprocess.run(["ifconfig", interface], stdout=subprocess.PIPE)
            ip_address = ifconfig_output.stdout.decode().split("inet ")[1].split(" ")[0]
            return ip_address
        except Exception as e:
            print(e)

    @pyqtSlot()
    def files(self,file):
        self.ip_address = self.get_ip_address("eth0")
        if self.ipbox.text() != "":
            if file=="arp_spoofer.py":
                self.name_file = "./"+ file
                self.ip_address = self.ipbox.text()
                self.new_ip = self.ip_address[:self.ip_address.rindex('.') + 1] + '2'
                self.arg1 = "-t" + self.ipbox.text()
                self.arg2 = "-s" + self.new_ip
                subprocess.Popen([self.name_file, self.arg1, self.arg2])
            elif file=="mac_changer.py":
                self.name_file =file
                self.arg1 = "-i" + "eth0"
                subprocess.Popen(["python3",self.name_file, self.arg1])
            elif file=="network_scanner.py":
                self.name_file = file
                self.ip_address = self.ipbox.text()
                self.new_ip = self.ip_address[:self.ip_address.rindex('.') + 1] + '0'
                self.arg1 = "-t"+self.new_ip+"/24"
                subprocess.Popen(["python3", self.name_file, self.arg1])
            elif file=="listener.py":
                self.name_file = file
                self.arg1 = "-t" + self.ipbox.text()
                self.arg2="-p"+self.portbox.text()
                subprocess.Popen(["python", self.name_file, self.arg1,self.arg2])
                """"
            elif file=="arp_spoofer.py":
                self.name_file = "./" + file
                self.ip_address = self.get_ip_address("eth0")
                ip_address = self.ipbox.text()
                """""
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill the IP Address box before proceed.")
class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('meniuPI.ui', self)
        try:
            self.arpspoof.clicked.connect(self.arpspoofer)
            self.dnspoof.clicked.connect(self.dnspoofer)
            self.mac.clicked.connect(self.macchanger)
            self.netscanner.clicked.connect(self.netscann)
            self.malware.clicked.connect(self.malware_listener)
            self.packetsniffer.clicked.connect(self.packetsniff)
        except KeyboardInterrupt:
            print("Exit....")
    def arpspoofer(self):
        print("Starting ARP SPOOFING")
        argument = "arp_spoofer.py"
        self.settings_widget = settings(argument)
        self.settings_widget.show()
    def macchanger(self):
        print("Starting MAC CHANGER")
        argument = "mac_changer.py"
        self.settings_widget = settings(argument)
        self.settings_widget.show()
    def dnspoofer(self):
        print("Starting DNS SPOOFER")
        self.argument = "dns_spoofer.py"
        subprocess.Popen(["python3",self.argument])
    def netscann(self):
        print("Starting Network Scanner")
        argument = "network_scanner.py"
        self.settings_widget = settings(argument)
        self.settings_widget.show()
    def malware_listener(self):
        print("Starting Listener")
        argument = "listener.py"
        self.settings_widget = settings(argument)
        self.settings_widget.show()
    def packetsniff(self):
        print("Starting packet sniffer")
        self.argument = "packet_sniffer.py"
        subprocess.Popen(["python",self.argument])
app = QApplication(sys.argv)
window = UI()
window.show()
app.exec()


