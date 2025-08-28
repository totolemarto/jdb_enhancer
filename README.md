This tools is created in order to improve JDB. By adding more informations directly in the terminal with curses in python.
Here an exemple of how it looks like for the moment:
<img width="1592" height="722" alt="image" src="https://github.com/user-attachments/assets/296b9d8f-3cab-45f8-baa7-b328da4b6895" />

# Actual Feature

    * Display result of list ( source code ), stop ( different breakpoints ), locals ( variables in this frame ) whitout request from user continuous
    * Manage an history of command allow to naviguate througt it with arrows
    * Create shortcuts for most use commands ( next, step, cont )
    * Let user manage his shortcuts with a file to create special shortcuts for different project.

# WIP Feature

    * Create interaction whith python to select in flight which informations to display
    * Send all possible argument for jdb directly with jdb_enhancer like 'classpath'
   
# Create shortcut in a project

To create your personnal shortcut, you need to create a file named "jdb_shortcut.txt" and follow this style:
```
key & value
```
with one pair by line.
The file must be in the same directory where you run the debugger. This allow you to have differents shortcuts for different projects
[Here an exemple](jdb_enhancer/jdb_shortcut.txt)

# How to use

To run the code 
``` bash
    python3 jdb_enhancer.py <File to debug>
```

If you want to access the script from everywhere in your computer 

``` bash
    chmod +x jdb_enhancer.py
    sudo ln -s <absolute path of jdb_enhancer.py> /usr/local/bin
```
with this command you can run it from everywhere ( ensure /usr/local/bin ) is in your PATH
