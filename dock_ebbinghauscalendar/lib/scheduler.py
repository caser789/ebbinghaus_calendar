import time
from dock_ebbinghauscalendar.model.scheduler import Scheduler as Model


class Scheduler(object):

    def __init__(self):
        self.model = Model()

    def schedule(self):
        while True:
            posts = self.model.get_due_posts()
            print posts
            time.sleep(60)


def main():
    s = Scheduler()
    s.schedule()


if __name__ == '__main__':
    main()
