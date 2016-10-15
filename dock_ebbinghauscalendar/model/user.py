import redis
from hashlib import md5
from dock.common import log

logger = log.get_logger('ebbinghaus_calendar.model.user')

server = redis.Redis()


class User(object):

    def __init__(self, **kw):
        self.email = kw['email']
        self.password = kw['password']
        self.id = kw['id']

    @classmethod
    def from_form(cls, form):
        form.update(id=md5(form['email']).hexdigest())
        return cls(**form)

    @classmethod
    def from_email(cls, email):
        id = md5(email).hexdigest()
        key = 'ebbinghaus_server:user:{}'.format(id)
        data = server.hgetall(key)
        return cls(**data)

    @classmethod
    def from_id(cls, id):
        key = 'ebbinghaus_server:user:{}'.format(id)
        data = server.hgetall(key)
        return cls(**data)

    def registed(self):
        key = 'ebbinghaus_server:user:{}'.format(self.id)
        return server.exists(key)

    def register(self):
        key = 'ebbinghaus_server:user:{}'.format(self.id)
        server.hmset(key, self.__dict__)

    def valid(self):
        key = 'ebbinghaus_server:user:{}'.format(self.id)
        password = server.hget(key, 'password')
        return self.password == password
