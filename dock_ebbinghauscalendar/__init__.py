import dock
version_info = (1, 0, 0)
__version__ = '.'.join(map(str, version_info))

logger_name = 'ebbinghaus_calendar'
logger = dock.log.get_logger(logger_name)


def init(app):
    from view import ebbinghaus_calendar
    return [ebbinghaus_calendar.blueprint]
