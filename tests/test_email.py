# coding: utf-8
# from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(
        (
            Header(name, 'utf-8').encode(),
            addr.encode('utf-8') if isinstance(addr, unicode) else addr
        )
    )


smtp_server = 'smtp.163.com'
from_addr = 'm13488699851@163.com'
to_addr = '15011272359@139.com'
password = '19880212xj'

# msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg = MIMEText(
    """
    <html><body><h1>Hello</h1>
    <h2>I am Xuejiao</h2>
    <p>send by <a href="http://www.python.org">Python</a>...</p>
    </body></html>
    """,
    'html',
    'utf-8'
)
msg['From'] = _format_addr(u'管理员 <{}>'.format(from_addr))
msg['To'] = _format_addr(u'Python 爱好者<{}>'.format(to_addr))
msg['Subject'] = Header(u'来自SMTP的问候', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
res = server.quit()
print 'fuck: ', type(res[0])  # int
