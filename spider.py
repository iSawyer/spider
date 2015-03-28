# -*- coding: utf-8 -*-

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

mail_user = 'dong_sui'
mail_pass = '?x'

def send_mail(send_to,files=[],text='Intern-Apply',send_from="dong_sui@qq.com",subject='Intern-Apply',server="smtp.qq.com"):
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


def get_page(url = 'http://shixi.info/beijing/page/1'):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
    headers = { 'User-Agent' : user_agent }   
    request = urllib2.Request(url, headers = headers)
    myResponse = urllib2.urlopen(request)
    page = myResponse.read()
    unicode_page = page.decode('utf-8')
    return unicode_page

def get_href_title(page):
    items = re.findall('<a.*?href="(.*?)".*?title="(.*?)">.*?</a>',page,re.S)
    # items[0] is href, items[1] is the title
    result_items = []
    for item in items:
        if (item[0][-4:] != 'html'):
            continue
        else:
            str1 = item[0]
            str2 = item[1][0:-16]
            
            result_items.append([str1.replace("\n",""),str2.replace("\n","")])
    return result_items
                            

def get_email(page):
    regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)
    email_list = re.findall(regex,page)
    email_str = ''.join(email_list[0]) 
    return email_str

def run(page_number):
    file_name = time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.txt'
    print 'spider start!!\n'
    fd = open(file_name,'w+')
    href_title_email = []
    total_href_title = []	
    
    for i in range(page_number):
        url = 'http://shixi.info/beijing/page/' + str(i+1)
        main_page = get_page(url)
        
        href_title = get_href_title(main_page)
        for href_title_list in href_title:
            total_href_title.append(href_title_list)
    
    total_href_title.sort(key = lambda x: x[1])
    total_href_title_no_dup = []
    total_href_title_no_dup.append(total_href_title[0])
    
    j = 0
    for i in range(len(total_href_title)):
        if(total_href_title_no_dup[j][1] != total_href_title[i][1]):
            total_href_title_no_dup.append(total_href_title[i])
            j = j + 1
    email_list = []
    for one_href_title in total_href_title_no_dup:
        href = one_href_title[0]
        href_page = get_page(href)
        email = get_email(href_page)
        email_list.append(email)
        fd.write(one_href_title[0] + ' ' + one_href_title[1] + ' ' + email + "\n")
    fd.close()
    # my CV path list

    # then send_mail
    send_mail(

def main():
    try:
        run(2)
    except:
        traceback.print_exc()
        time.sleep(9999)
    finally:
        print "spider finished\n"
        

if __name__ == "__main__":
    main()






        

    
    
