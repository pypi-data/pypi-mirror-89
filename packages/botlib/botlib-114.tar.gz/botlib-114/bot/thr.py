# BOTLIB - thr.py
#
# this file is placed in the public domain

"tasks (tsk)"

import os, queue, sys, threading, traceback

from bot.obj import Default, Object, get_name

class Thr(threading.Thread):

    "task class"

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))
        self.sleep = 0
        self.state = Object()

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

    def run(self):
        "run a task"
        func, args = self._queue.get()
        target = None
        if args:
            target = Default(vars(args[0]))
        self.setName((target and target.txt and target.txt.split()[0]) or self._name)
        self._result = func(*args)

    def wait(self, timeout=None):
        "wait for task to finish"
        super().join(timeout)
        return self._result

def launch(func, *args, **kwargs):
    "start a task"
    name = kwargs.get("name", get_name(func))
    t = Thr(func, *args, name=name, daemon=True)
    t.start()
    return t

def get_exception(txt="", sep=" "):
    "print exception trace"
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        if "python3" in elem[0] or "<frozen" in elem[0]:
            continue
        res = []
        for x in elem[0].split(os.sep)[::-1]:
            if x in ["bot"]:
                break
            res.append(x)
        result.append("%s:%s" % (os.sep.join(res[::-1]), elem[1]))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res
