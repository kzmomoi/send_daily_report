from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP
from ssl import create_default_context
from time import localtime

FROM_ADDR = 'sample@gmail.com'
GMAIL_PASSWORD = 'password'
TO_ADDR = ['to_addr@gmail.com']
CC_ADDR = ['cc_addr1@gmail.com', 'cc_addr2@yahoo.co.jp']
BCC_ADDR = []
SUBJECT = f'【日報】 {datetime.today().strftime("%Y/%m/%d")} 山田太郎'
MESSAGE_FILE = '/Users/yamada_taro/send_daily_report/message.txt'


def create_message(body):
    msg = MIMEText(body)
    msg['Subject'] = SUBJECT
    msg['From'] = FROM_ADDR
    msg['To'] = ','.join(TO_ADDR)
    msg['Cc'] = ','.join(CC_ADDR)
    msg['Bcc'] = ','.join(BCC_ADDR)
    msg['Date'] = formatdate(localtime=True)
    return msg


def send(msg):
    with SMTP(host='smtp.gmail.com', port=587) as smtpobj:
        smtpobj.set_debuglevel(True)
        context = create_default_context()
        smtpobj.starttls(context=context)
        smtpobj.login(FROM_ADDR, GMAIL_PASSWORD)
        receiver = TO_ADDR
        receiver.extend(CC_ADDR)
        receiver.extend(BCC_ADDR)
        smtpobj.sendmail(FROM_ADDR, receiver, msg.as_string())


if __name__ == '__main__':

    with open(MESSAGE_FILE, mode='r') as f:
        body = f.read()

    msg = create_message(body)
    print(msg)
    send(msg)
