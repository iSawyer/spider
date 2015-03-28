# -*- coding: utf-8 -*-
import traceback
import urllib2
import re
import urllib
import sys
import time
import traceback
reload(sys) 
sys.setdefaultencoding('utf8')
import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders



def send_mail(send_to,files=[],send_from="111",subject='test',text='111',server="smtp.qq.com"):
    assert type(send_to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Data'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEBase('application',"octet-stream")
        part.set_payload(open(f,"rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.login(mail_user,mail_pass)  
    smtp.sendmail(send_from,send_to,msg.as_string())
    smtp.close()



def main():
    files = ['ToDo.txt']
    send_to = ['1146854318@qq.com']
    try:
        send_mail(send_to,files)
    except:
        #time.sleep(60)
        traceback.print_exc()
        time.sleep(60)
    
if __name__ == "__main__":
    main()

    
