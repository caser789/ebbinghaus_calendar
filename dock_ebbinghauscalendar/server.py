# -*- coding: utf-8 -*-
from dock.web import DockApp
import dock_ebbinghauscalendar

app = DockApp("")
app.mount(dock_ebbinghauscalendar)
app.flaskapp.config.update(SECRET_KEY="xuejiao")


if __name__ == '__main__':
    app.run()
