import sys
import time
import json
import traceback
from dock import AppEnv
from dock.common import log
app = AppEnv("")
from dock_ebbinghauscalendar.model.scheduler import Scheduler
from dock_ebbinghauscalendar.lib.notify import Notifier

logger = log.get_logger('dock_ebbinghauscalendar.tasklet.notify')


def main():
    args = json.loads(sys.argv[1])
    model = Scheduler()
    while True:
        tasks = model.get_due_tasks()
        for task in tasks:
            post = task.get_post()
            try:
                if Notifier(**args).notify(post):
                    model.archive(task)
            except:
                logger.error(traceback.format_exc())
        time.sleep(60)


if __name__ == '__main__':
    main()
