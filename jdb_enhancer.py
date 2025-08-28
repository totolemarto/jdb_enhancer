#!/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2025 PRATS Tommy 



from jdb import Jdb_class
from categories import Category
from command_read import Command_reader
import curses
from sys import argv
from argparse import ArgumentParser, Namespace

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

"""
Usage: jdb <options> <class> <arguments>

where options include:
    -? -h --help -help print this help message and exit
    -sourcepath <directories separated by ":">
                      directories in which to look for source files
    -attach <address>
                      attach to a running VM at the specified address using standard connector
    -listen <address>
                      wait for a running VM to connect at the specified address using standard connector
    -listenany
                      wait for a running VM to connect at any available address using standard connector
    -launch
                      launch VM immediately instead of waiting for 'run' command
    -listconnectors   list the connectors available in this VM
    -connect <connector-name>:<name1>=<value1>,...
                      connect to target VM using named connector with listed argument values
    -dbgtrace [flags] print info for debugging jdb
    -trackallthreads  Track all threads, including virtual threads.
    -tclient          run the application in the HotSpot(TM) Client Compiler
    -tserver          run the application in the HotSpot(TM) Server Compiler
    -R<option>        forward <option> to debuggee process if launched by jdb, otherwise ignored

options forwarded to debuggee process if launched by jdb (shorthand instead of using -R):
    -v -verbose[:class|gc|jni]
                      turn on verbose mode
    -D<name>=<value>  set a system property
    -classpath <directories separated by ":">
                      list directories in which to look for classes
    -X<option>        non-standard target VM option

<class> is the name of the class to begin debugging
<arguments> are the arguments passed to the main() method of <class>

"""

def parse_arg() -> dict[str, list[str] | str]:
    arguments = ArgumentParser(prog = "my_jdb", usage='%(prog)s [options] [file] [argument of the file]')
    arguments.add_argument('Java_file_to_debug', type=str, help='A required string positional argument for the file to debug')
    arguments.add_argument('Java_arguments', nargs='*',  help='Optional positional argument for the java file')
    arguments.add_argument('-sourcepath', nargs="?", type=str, help= "directories in which to look for source files")
    return vars(arguments.parse_args())


def main(stdscr) -> None:
    args : dict[str, list[str] | str] = parse_arg()
    init_curses()
    Jdb : Jdb_class = Jdb_class(args)
    command_reader : Command_reader = Command_reader()
    categories : dict[str, Category] = init_categories(stdscr, Jdb)

    categories["JDB interaction"].add_content(Jdb.read_until_prompt(wait=False) + " ")
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

if __name__ == "__main__":
    curses.wrapper(main)
