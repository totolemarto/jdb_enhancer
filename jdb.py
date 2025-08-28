# SPDX-License-Identifier: MIT
# Copyright (c) 2025 PRATS Tommy 
import pty
from os import read
import subprocess 
from time import sleep

class Jdb_class:
    
    input_stream : int
    output_stream : int
    jdb : subprocess.Popen

    def __init__(self, args : dict [str, list[str] | str]):
        self.input_stream, self.output_stream = pty.openpty()
        self.jdb = subprocess.Popen(
            ["jdb", args["Java_file_to_debug"]],
            stdin = subprocess.PIPE,
            stdout = self.output_stream,
            stderr = self.output_stream,
            text=True,
            bufsize=0
        )
 
    def __get_from_jdb(self, number : int = 1024) -> str:
        return read(self.input_stream, number).decode()
   
    def read_until_prompt(self, wait : bool) -> str:
        output : str = ""
        if wait:
            sleep(0.2)
        while True:
            chunk : str = self.__get_from_jdb(4096)
            if not chunk:
                break
            output += chunk
            if output.endswith("> ") or output.endswith("] "):
                break
        return output
    
    def send_command(self, cmd : str, wait : bool = True) -> str:
        if not self.is_alive():
            raise RuntimeError("jdb is not running anymore (process exited)")
        self.jdb.stdin.write(cmd + "\n")
        self.jdb.stdin.flush()
        if cmd == "exit":
            return ""
        return self.read_until_prompt(wait)

    def terminate(self) -> None:
        self.jdb.terminate()
    
    def is_alive(self) -> bool:
        return self.jdb.poll() is None 
