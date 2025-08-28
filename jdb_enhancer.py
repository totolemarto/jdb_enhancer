from jdb import Jdb_class
from categories import Category
from command_read import Command_reader
import curses
from sys import argv

def display_category(stdscr, categories : dict[str, Category]) -> None:
    lines, _ = stdscr.getmaxyx()
    tot : int = 0
    for value in categories.values():
        tot += value.get_number_of_lines()
    stdscr.clear()
    if tot >= lines:
        categories["JDB interaction"].line = lines - categories["JDB interaction"].get_number_of_lines()
        categories["Variables"].line = categories["JDB interaction"].line - categories["Variables"].get_number_of_lines()
        categories["Breakpoints"].line = categories["Variables"].line - categories["Breakpoints"].get_number_of_lines()
        categories["Source_code"].line = categories["Breakpoints"].line - categories["Source_code"].get_number_of_lines()
        current_line : int = categories["Source_code"].display()
        current_line : int = categories["Variables"].display()
        current_line : int = categories["Breakpoints"].display()
        current_line : int = categories["JDB interaction"].display()
        return         
    categories["Source_code"].line = 0
    current_line : int = categories["Source_code"].display()
    categories["Breakpoints"].line = current_line
    current_line = categories["Breakpoints"].display()
    categories["Variables"].line = current_line
    current_line = categories["Variables"].display()
    categories["JDB interaction"].line = current_line
    categories["JDB interaction"].display()

def update_categories(categories : dict[str, Category]) -> None:
    for key, value  in categories.items():
        if key != "JDB interaction":
            value.send_command()
    
def init_curses() -> None:
    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)

def init_categories(stdscr, Jdb : Jdb_class) -> dict[str, Category]:
    result : dict[str, Category] = {}
    result["Source_code"] =  Category("Source code", "list", 0, Jdb, stdscr, 1)
    result["Breakpoints"] =  Category("Breakpoints", "stop", 2, Jdb, stdscr, 2)
    result["Variables"]  =  Category("Variables", "locals", 4, Jdb, stdscr, 3)
    result["JDB interaction"] = Category("JDB interaction", "list", 8, Jdb, stdscr, 4)
    return result

def main(stdscr) -> None:
    init_curses()
    Jdb : Jdb_class = Jdb_class(argv[1])
    command_reader : Command_reader = Command_reader()
    categories : dict[str, Category] = init_categories(stdscr, Jdb)

    categories["JDB interaction"].add_content(Jdb.read_until_prompt(wait=False) + " ")
    categories["JDB interaction"].add_content(Jdb.send_command("stop at Test.Main.coucou"))
    categories["JDB interaction"].add_content(Jdb.send_command("run"))
    update_categories(categories)
    display_category(stdscr, categories)
    cmd : str = ""
    while cmd != "exit" and Jdb.is_alive() :
        cmd = command_reader.get_input_from_user(stdscr, categories)
        if cmd in ["next", "cont", "step"]:
            categories["JDB interaction"].clear_content() 
        categories["JDB interaction"].add_content(Jdb.send_command(cmd))
        update_categories(categories)
        display_category(stdscr, categories)
    Jdb.terminate()
    exit()

def usage() -> None:
    print(f"usage : python3 {argv[0]} <file to debug>")

if __name__ == "__main__":
    if len(argv) != 2:
        usage()
        exit()
    curses.wrapper(main)
