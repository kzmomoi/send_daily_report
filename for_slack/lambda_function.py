import json
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP
from ssl import create_default_context
from time import localtime
from urllib.parse import unquote_plus

import requests

FROM_ADDR = 'sample@gmail.com'
GMAIL_PASSWORD = 'password'
TO_ADDR = ['to_addr@gmail.com']
CC_ADDR = ['cc_addr1@gmail.com', 'cc_addr2@yahoo.co.jp']
BCC_ADDR = []
SUBJECT = f'【業務報告(日報)】 {datetime.today().strftime("%Y/%m/%d")} 山田太郎'
WEBHOOK_URL = 'Webhookのurl'
SLASH_TOKEN = 'スラッシュコマンドのTOKEN'


def create_message(body):
    msg = MIMEText(body)
    msg['Subject'] = SUBJECT
    # メール送信者の名前。好きな名前にできる（e.g. '山田太郎'）
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


def lambda_handler(event, context):
    if event['token'] != SLASH_TOKEN:
        return 'invalid token.'

    # URLエンコードされたリクエストパラメータを元に戻す
    decode_msg = unquote_plus(event['text'])

    # Slackにメッセージ結果をポストする（スラッシュコマンド の場合、Slackに履歴が残らないため）
    params = {'text': decode_msg}
    requests.post(WEBHOOK_URL, json.dumps(params))

    # メール送信
    msg = create_message(decode_msg)
    send(msg)
