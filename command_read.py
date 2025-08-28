# SPDX-License-Identifier: MIT
# Copyright (c) 2025 PRATS Tommy 
from categories import Category
import curses
from os import path
from sys import stderr

class Command_reader:

    history : list[str]
    current : str
    shortcuts : dict [str, str]

    def __init__(self):
        self.history = []
        self.current = ""
        self.read_shortcut()

    def read_shortcut(self) -> None:
        self.shortcuts = {
                "n" : "next",
                "c" : "cont",
                "s" : "step",
                "l" : "list"
                }
        if not path.exists("jdb_shortcut.txt"):
            return
        with open("jdb_shortcut.txt", "r") as f:
            content = f.read()
        content = content.split("\n")
        for line_number, line in enumerate(content):
            if line == "":
                continue
            try:
                key, value = line.split("&")
            except:
                curses.endwin()
                print(f"wrong shortcut line found at line number {line_number + 1}.\nFormat exepected : key & value. Found {line}.\nActual shortcuts found : {self.shortcuts}.\n{content=}", file=stderr)
                exit(1)
            while key.endswith(" "):
                key = key.removesuffix(" ")
            while value[0] == " ":
                value = value.removeprefix(" ")
            self.shortcuts[key] = value

    def get_input_from_user(self, stdscr, categories : dict[str, Category]) -> str:
        result : str = ""
        y, _ = categories["JDB interaction"].get_position_to_write()
        line, column = categories["JDB interaction"].get_position_to_write()
        if line == stdscr.getmaxyx()[0]:
            line -= 1
            y -= 1
            for col in range(column):
                stdscr.move(line, col)
                stdscr.delch()
            column = 5
        index : int = 0
        current_history_position : int = len(self.history) - 1
        tmp_command : str = ""
        while True:
            key = stdscr.getch()

            if key in (curses.KEY_ENTER, 10, 13): 
                break

            elif key in (curses.KEY_BACKSPACE, 127):
                if index > 0:
                    result = result[0:index - 1] + result[index:]
                    index -= 1
                    stdscr.move(y, index + column)
                    stdscr.delch()

            elif key == curses.KEY_LEFT:
                index = max( index - 1, 0)
            
            elif key == curses.KEY_RIGHT:
                index = min(index + 1, len(result))
            
            elif key == curses.KEY_UP:
                if current_history_position != -1:
                    if current_history_position == len(self.history) - 1:
                        tmp_command = result
                    result = self.history[current_history_position]
                    current_history_position -= 1
                index = len(result) 

            elif key == curses.KEY_DOWN:
                if current_history_position + 1 < len(self.history):
                    result = self.history[current_history_position + 1]
                    current_history_position += 1
                else:
                    if tmp_command:
                        result = tmp_command
                index = len(result) 
                 
            elif key == curses.KEY_DC:
                result = result[0:index ] + result[index + 1:]
                stdscr.move(y, index + column)
                stdscr.delch()

            else:
                result = result[:index] + chr(key) + result[index:]
                index += 1

            stdscr.addstr(line, column, result )
            stdscr.move(y, index  + column)
        if self.shortcuts.get(result):
            result = self.shortcuts[result]
        if result == "":
            if len(self.history) != 0:
                result = self.history[-1]
            else:
                return self.get_input_from_user(stdscr, categories)
        else:
            self.history.append(result)

        return result
