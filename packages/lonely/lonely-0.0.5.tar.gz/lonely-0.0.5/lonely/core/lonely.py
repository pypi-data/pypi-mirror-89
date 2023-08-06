import os, sys

from lonely import system, cmd

home = "/usr/local/lonely"

# 导入 apps 必须在 home 定义的后面，因为 app 包内依赖 lonely.home
from lonely.app import apps

def exist():
    return os.path.exists(home)

def mkdir():
    if not os.path.exists(home):
        access(system.base)
        os.mkdir(home)
    else:
        access(home)

def access(path=None):
    if path is None:
        path = home
    if not os.access(path, os.W_OK):
        print("Permission denied: %s" % path)
        sys.exit(1)

class Lonely(object):
    def version(self):
        print("lonely version 0.0.5")

    def install(self, app_name):
        app = apps.get(app_name)
        if app != None and hasattr(app, "install"):
            app.install()
        else:
            print("Unsupported app: %s" % app_name)
            sys.exit(1)

    def update(self, app_name):
        app = apps.get(app_name)
        if app != None and hasattr(app, "update"):
            app.update()
        else:
            print("Unsupported app: %s" % app_name)
            sys.exit(1)

    def remove(self, app_name):
        app = apps.get(app_name)
        if app != None and hasattr(app, "remove"):
            app.remove()
        else:
            print("Unsupported app: %s" % app_name)
            sys.exit(1)

    def env_add(self, app_name):
        app = apps.get(app_name)
        if app != None and hasattr(app, "env_add"):
            app.env_add()
        else:
            print("Unsupported app: %s" % app_name)
            sys.exit(1)

    def env_del(self, app_name):
        app = apps.get(app_name)
        if app != None and hasattr(app, "env_del"):
            app.env_del()
        else:
            print("Unsupported app: %s" % app_name)
            sys.exit(1)
