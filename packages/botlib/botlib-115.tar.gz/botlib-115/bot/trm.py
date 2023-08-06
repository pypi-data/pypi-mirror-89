# BOTLIB - trm.py
#
# this file is placed in the public domain

"terminal (trm)"

import atexit
import sys
import termios

from bot.thr import get_exception

resume = {}

class EWRONG(Exception):

    "wrong assumption"

def execute(main):
    "provide context for funcion"
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except Exception as ex:
        print(get_exception())
    finally:
        termreset()

def termsetup(fd):
    "setup terminal"
    return termios.tcgetattr(fd)

def termreset():
    "reset terminal"
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def termsave():
    "save terminal state"
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = termsetup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass
