# Scan Viewer

Port scanner parser for easier reading of information.
Supports: .gnmap, .nmap, .nessus, .naabu

# Commands
- `load {filename}` To load an .nmap file into the session
- `show {all|ports|ips}` To display the contents of the .nmap file(s) in the session
- `no-comments` Toggles the display of comments when using the show command
- `export` To save the current session to be imported later
- `import` To load a saved session
---
- `delete` Lists all saved sessions for the selection of one to delete
- `new` Empties the current session to allow new data
---
- `help` Displays these commands and more in the script
