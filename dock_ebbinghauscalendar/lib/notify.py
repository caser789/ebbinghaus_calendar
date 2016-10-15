import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from dock.common import config
from jinja2 import Environment
from jinja2 import FileSystemLoader
from ..model.user import User


class Notifier(object):

    def __init__(self, **kw):
        self.from_addr = kw.get('from_addr', 'm13488699851@163.com')
        self.password = kw.get('passwd', '19880212xj')
        self.smtp_server = kw.get('smtp_server', 'smtp.163.com')
        self.smtp_port = kw.get('smtp_port', 25)
        self.host = kw.get('host', 'http://127.0.0.1')

    def notify(self, post):
        email = self.get_email(post.user_id)
        msg = self.get_message(post, email)
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [email], msg.as_string())
        res = server.quit()
        return res[0] == 221

    def get_email(self, user_id):
        user = User.from_id(user_id)
        return user.email

    def get_message(self, post, email):
        question = dict(content=post.question)
        answer = dict(content=post.answer)
        data = dict(question=question, answer=answer)
        content = self.get_message_content('email_question', data)
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = _format_addr(u'Admin <%s>' % self.from_addr)
        msg['To'] = _format_addr(u'Dear <%s>' % email)
        msg['Subject'] = Header(post.question, 'utf-8').encode()
        return msg

    def get_answer_url(self, post):
        return '{host}/answer/{post_id}'.format(
            host=self.host, post_id=post.id)

    @property
    def templates(self):
        return config['ebbinghaus_calendar']['email_templates']

    def _get_template(self, tmpl):
        """
        1. get template from template file
        """
        template_config = self.templates[tmpl]
        template_path, template_file = template_config.rsplit('/', 1)
        env = Environment(loader=FileSystemLoader(template_path))
        return env.get_template(template_file)

    def get_message_content(self, tmpl, data):
        template = self._get_template(tmpl)
        rendered = template.render(
            data=data
        )
        return str(rendered.encode('utf-8'))


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(
        (
            Header(name, 'utf-8').encode(),
            addr.encode('utf-8') if isinstance(addr, unicode) else addr
        )
    )
