import smtplib
from email.mime.text import MIMEText

from email.header import Header
def post_message(text):
    msg = MIMEText('you have a new lesson', 'plain', 'utf-8')
    message = MIMEText(text, 'plain', 'utf-8')
    message['from'] = "222<hudongmeisunyiwei@126.com>"
    message['to'] = "sunyiwei24601@163.com"

    subject = '课程通知'
    message['Subject'] = Header(subject, 'utf-8')

    # 输入Email地址和口令:
    #from_addr = input('From: ')
    from_addr="hudongmeisunyiwei@126.com"
    #password = input('Password: ')
    password='952733'
    # 输入SMTP服务器地址:
    #smtp_server = input('SMTP server: ')
    smtp_server='smtp.126.com'
    # 输入收件人地址:
    #to_addr =input('To: ')
    to_addr="sunyiwei24601@163.com"
    import smtplib
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], message.as_string())
    server.quit()