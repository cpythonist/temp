import time
import getch
import signal as sig
import typing as ty
import math
import os
import objects as obj


class ExceptionToFlaunt(Exception):
    pass


def sigHandler(signal, frame):
    raise ExceptionToFlaunt("Time out you stupid idiot!")


def consScr(size: os.terminal_size) -> str:
    return '#' * size.columns + '\n' \
        + ('#' + ' ' * (size.columns - 2) + '#' + '\n') * (size.lines - 3) \
        + '#' * size.columns


def timeDiff(last: float):
    if time.time() - last > 0.1:
        return "baa!"

with open("manLog.log", 'w') as f:
    key = '\0'
    string = ''
    while True:
        size = os.get_terminal_size()
        print(consScr(size) + '\n' + string, end='')
        sig.signal(sig.SIGALRM, sigHandler)
        sig.alarm(1)
        try:
            key = getch.getch().decode("utf-8")
        except:
            pass
        
        if ord(key) == 3:
            break
        f.write(key)
        string += key
        os.system("cls")
# temp = obj.Obj("Koti", 85, (0, 0))
# print(temp.name, temp.mass)
