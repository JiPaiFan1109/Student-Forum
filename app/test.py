#coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = '1483511346@qq.com'
receiver = '1483511346@qq.com'
subject = '离崩溃一线之遥'
smtpserver = 'smtp.qq.com'
username = '1483511346@qq.com'
password = 'bamtipnyrhucjahh'

msg = MIMEText( 'Hello Python', 'text', 'utf-8' )
msg['Subject'] = Header( subject, 'utf-8' )

smtp = smtplib.SMTP()
smtp.connect( smtpserver )
smtp.login( username, password )
smtp.sendmail( sender, receiver, msg.as_string() )
smtp.quit()