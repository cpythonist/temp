import time
import curses as cur
import signal as sig
import objects as objs

stdscr = cur.initscr()
cur.noecho()
cur.cbreak()
stdscr.keypad(True)

global objArr
objArr: list[objs.Obj] = []
allCommands: list[str] = []
appObj = objArr.append
appComms = allCommands.append


def consScr(objArr: list[objs.Obj]) -> None:
    stdscr.addstr(0, 0, '#' * (cur.COLS - 1))
    stdscr.addstr(cur.LINES - 2, 0, '#' * (cur.COLS - 1))
    for obj in objArr:
        # stdscr.addstr(round(obj.pos[1]), round(obj.pos[0]), ' ' * (cur.COLS - 2 * len(obj.txt.splitlines()[0])) + obj.txt + ' ' * (cur.COLS - 2 * len(obj.txt.splitlines()[0])))
        stdscr.addstr(round(obj.pos[1]), round(obj.pos[0]), obj.txt)


def update(dt: float):
    for obj in objArr:
        obj.pos[0] += obj.vel[0] * dt
        obj.pos[1] += obj.vel[1] * dt


try:
    command = ''
    f = open("log.log", 'w')
    obj1 = objs.Sq("koti", 85, [0, 10], [1, 0], 3)
    obj2 = objs.Sq("thiru", 62, [0, 5], [0, 0], 2)
    obj3 = objs.Sq("abhi", 58, [0, 1], [0, 0], 1)
    appObj(obj1)
    appObj(obj2)
    appObj(obj3)
    count = 0
    last = time.time()
    while True:
        try:
            consScr(objArr)
            overflow = False if len(command) < cur.COLS - 1 else True
            key = stdscr.getch()
            # ^Z key
            if key == 26:
                break
            # Backspace and delete keys
            elif key in (8, 330):
                command = command[:-1]
            # Return key
            elif key == 10:
                appComms(command)
                command = ''
            elif not overflow:
                command += chr(key)
            stdscr.addstr(cur.LINES - 1, 0, ' ' * (cur.COLS - 1))
            stdscr.addstr(cur.LINES - 1, 0, "$ " + command)
            stdscr.refresh()

        except cur.error:
            print("Command too long")

        except KeyboardInterrupt:
            break

        except:
            # TODO: Remove this!
            import traceback as tb
            tb.print_exc()

except Exception as e:
    import traceback as tb
    tb.print_exc()

finally:
    cur.nocbreak()
    stdscr.keypad(False)
    cur.echo()
    cur.endwin()
    allCommands = [comm for comm in allCommands if comm.strip()]
    print("All commands:", allCommands)
    f.close()
