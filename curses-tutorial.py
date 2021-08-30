from curses import wrapper

def main(stdscr):
    stdscr.clear()
    for i in range(0, 10):
        v = i-10
        stdscr.addstr(i, 0, f"10 divided by {v} is {10/v}")

    stdscr.refresh()
    stdscr.getkey()

if __name__ == "__main__":
    wrapper(main)
