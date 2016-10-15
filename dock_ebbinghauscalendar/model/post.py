import time
import uuid
import redis
from dock.common import log

logger = log.get_logger('ebbinghaus_calendar.model.user')

server = redis.Redis()


class Post(object):

    def __init__(self, **kw):
        self.user_id = kw['user_id']
        self.question = kw['question'].strip()
        self.answer = kw['answer'].strip()
        self.id = kw['id']
        self.ts = kw['ts']

    @classmethod
    def from_form(cls, **form):
        form.update(id=uuid.uuid4().get_hex())
        form.update(ts=int(time.time() * 1000))  # ms
        return cls(**form)

    @classmethod
    def from_id(cls, id):
        key = "ebbinghaus:post:{}".format(id)
        data = server.hgetall(key)
        return cls(**data)

    def dump(self):
        key = "ebbinghaus:post:{}".format(self.id)
        server.hmset(key, self.__dict__)
