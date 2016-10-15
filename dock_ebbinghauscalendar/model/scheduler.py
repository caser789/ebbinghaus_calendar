import time
import redis
from dock.common import log
from .post import Post

logger = log.get_logger('ebbinghaus_calendar.model.user')

server = redis.Redis()

ts_list = [
    1 * 60 * 60 * 1000,
    6 * 60 * 60 * 1000,
    24 * 60 * 60 * 1000,
    3 * 24 * 60 * 60 * 1000,
    7 * 24 * 60 * 60 * 1000,
    14 * 24 * 60 * 60 * 1000,
    30 * 24 * 60 * 60 * 1000,
    60 * 24 * 60 * 60 * 1000,
]


class Scheduler(object):

    def __init__(self):
        self.key = "ebbinghaus:schedule:zset"

    def schedule(self, post):
        ts = int(post.ts)
        for i, t in enumerate(ts_list):
            value = '{}::{}'.format(i, post.id)
            server.zadd(self.key, value, ts + t)

    def get_due_tasks(self):
        ts = int(time.time() * 1000)
        ids = server.zrangebyscore(self.key, 0, ts, withscores=True)
        return [Task(id) for id, _ in ids]

    def archive(self, task):
        server.zrem(self.key, task.id)


class Task(object):

    def __init__(self, id):
        self.id = id

    def get_post(self):
        post_id = self.id.split('::')[-1]
        return Post.from_id(post_id)
