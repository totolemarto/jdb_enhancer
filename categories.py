# SPDX-License-Identifier: MIT
# Copyright (c) 2025 PRATS Tommy 
from jdb import Jdb_class
import curses

class Category:
    name : str
    command : str
    line : int
    jdb : Jdb_class 
    window : curses.window
    content : str

    def __init__(self, name : str, command : str, line : int, jdb : Jdb_class, window : curses.window, color : int):
        self.name = name
        self.content = ""
        self.command = command
        self.line = line
        self.jdb = jdb
        self.window = window
        self.color = color
    
    def draw_separation(self) -> None:
        _, cols = self.window.getmaxyx()
        for column in range(cols):
            self.window.addstr(self.line, column, "-", curses.color_pair(self.color))

    def display(self) -> int:
        
        lines, _ = self.window.getmaxyx()
        if self.line  >= 0:
            self.draw_separation()
            self.window.addstr(self.line + 1, 0, self.name, curses.color_pair(self.color))
        x = 0
        for i, line in enumerate(self.content.split("\n")):
            if self.line + i + 2 >= 0 and self.line + i + 2 < lines:
                self.window.addstr(self.line + i + 2, 0, line, curses.color_pair(self.color))
            x = i
        return self.line + x + 2

    def send_command(self):
        self.clear_content()
        self.add_content(self.jdb.send_command(self.command, wait=False))


    def add_content(self, new_content : str) -> None:
        self.content += new_content
    
    def get_position_to_write(self) -> tuple[int,int]:
        lines = self.content.split("\n")
        line = len(lines) + 1 + self.line
        column = len(lines[-1]) 
        if line >= self.window.getmaxyx()[0]:
            return self.window.getmaxyx()
        return min(line,self.window.getmaxyx()[0] - 1) , column 

    def get_number_of_lines(self) -> int:
        return len(self.content.split("\n"))


    def clear_content(self) -> None:
        self.content = ""
