import time
import curses as cur
import objects as objs
import parser as par

stdscr = cur.initscr()
cur.noecho()
cur.cbreak()
stdscr.keypad(True)

global objArr
objArr: list[objs.Obj] = []
allCommands: list[str] = []
appObj = objArr.append
appComms = allCommands.append
parser = par.Parser()


def parseComm(command: str) -> None:
    command.lower().split()
    pass


def consScr(objArr: list[objs.Obj]) -> None:
    stdscr.addstr(0, 0, '█' * (cur.COLS - 1))
    stdscr.addstr(cur.LINES - 2, 0, '█' * (cur.COLS - 1))
    for i in range(1, cur.LINES - 2):
        stdscr.addstr(i, 0, ' ' * (cur.COLS - 2))
    for obj in objArr:
        stdscr.addstr(round(obj.pos[1]), round(obj.pos[0]),
                      ' ' * (cur.COLS - obj.side // 2) + obj.txt 
                      + ' ' * (obj.side // 2))


def update(dt: float):
    for obj in objArr:
        if obj.pos[0] >= cur.COLS - 2 or obj.pos[0] < 0:
            continue
        if obj.pos[1] >= cur.LINES - 4 or obj.pos[1] < 0:
            continue
        obj.pos[0] += obj.vel[0] * dt
        obj.pos[1] += (obj.vel[1] * dt + 0.5 * 200 * dt ** 2)


try:
    command = ''
    f = open("log.log", 'w')
    obj1 = objs.Sq("koti", 85, [0, 10], [20, 0], 3)
    obj2 = objs.Sq("thiru", 62, [0, 5], [40, 0], 2)
    obj3 = objs.Sq("abhi", 58, [0, 1], [30, 0], 1)
    appObj(obj1)
    appObj(obj2)
    appObj(obj3)
    count = 0
    commErr = 0
    stdscr.timeout(10)
    cur.curs_set(0)
    last = time.time()
    while True:
        try:
            update((now := time.time()) - last)
            last = now
            consScr(objArr)
            overflow = False if len(command) < cur.COLS - 1 else True
            key = stdscr.getch()
            # ^Z key
            if key == -1:
                pass
            elif key == 26:
                break
            # Backspace and delete keys
            elif key in (8, 330):
                command = command[:-1]
            # Return key
            elif key == 10:
                parser.src = command
                all = parser.parse()
                print(all)
                command = ''
            elif not overflow:
                command += chr(key)
            stdscr.addstr(cur.LINES - 1, 0, ' ' * (cur.COLS - 1))
            stdscr.addstr(cur.LINES - 1, 0, f"[{'.' if not commErr else 'X'}] $ " + command)
            stdscr.refresh()

        except cur.error:
            print("Command too long/String out of bounds")

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
    f.close()
