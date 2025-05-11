from modules.allFindings import allFindings
from modules.parser import parser

from sys import platform

if platform == "win32":
    CLEAR_COMMAND = "cls"

else:
    CLEAR_COMMAND = "clear"

import os

class cli:
    def __init__(self, data: allFindings, parser: parser):
        self._findings = data
        self._parser = parser

    def _start(self):
        while True:
            command = input(">")

            if len(command.split()) < 1:
                pass

            else:
                match command.split()[0].lower():
                    case ("help" | "h" | "?"):
                        print(r"  _____             __      ___                        ")
                        print(r" / ____|            \ \    / (_)                       ")
                        print(r"| (___   ___ __ _ _ _\ \  / / _  _____      _____ _ __ ")
                        print(r" \___ \ / __/ _` | '_ \ \/ / | |/ _ \ \ /\ / / _ \ '__|")
                        print(r" ____) | (_| (_| | | | \  /  | |  __/\ V  V /  __/ |   ")
                        print(r"|_____/ \___\__,_|_| |_|\/   |_|\___| \_/\_/ \___|_|   ")
                        print()
                        print('General:')
                        print('"help", "h", "?" - Prints this help menu')
                        print('"clear", "cls" - Clears the terminal')
                        print('"quit", "exit" - Exits the program')
                        print()
                        print("Session Management:")
                        print('"new" - Starts a new session')
                        print('"load {filename}" - Loads a file into the session')
                        print('"export {session name}" - Exports the session into a config file to be imported. Saves as an ID by default but a session name can be provided')
                        print('"import" - Imports a saved session')
                        print('"delete" - Lists all sessions for selection to be deleted from the config file')
                        print()
                        print("Session Commands")
                        print('"show {arg}" - Prints all when no argument supplied. Arguments:')
                        print('\t"all" - Displays all')
                        print('\t"ports", "port" - Displays all ports')
                        print('\t"ip", "ips" - Displays all ips')
                        print('"no-comments" - Toggles comments on or off for when using the show command')
                        print('"search" - Search through findings in session by ip')

                    case ("clear" | "cls"):
                        os.system(CLEAR_COMMAND)

                    case ("exit" | "quit"):
                        self._findings._updateConfig("_lastsession", self._findings._loadedId)
                        exit()

                    case ("new"):
                        self._findings._clear()

                    case ("load"):
                        if len(command.split()) > 1:
                            self._findings = self._parser.parseFile(self._findings, command.split()[1])
                            print(f"Loaded {self._findings._getLoadedIps()} ips")
                            self._findings._orderFindings()
                            
                        else:
                            print("Please specify a file location")

                    case ("export"):
                        if len(command.split()) > 1:
                            self._findings._export(command.split()[1])
                        
                        else:
                            self._findings._export()

                    case ("import"):
                        self._findings._import()
                        print(f"Loaded {self._findings._getLoadedIps()} ips")

                    case ("delete"):
                        self._findings._delete()

                    case ("show"):
                        if len(command.split()) > 1:
                            match command.split()[1]:
                                case ("all"):
                                    self._findings.showAll()

                                case ("port" | "ports"):
                                    self._findings.showPorts()

                                case ("ip" | "ips"):
                                    self._findings.showIps()

                                case _:
                                    print(f"{command.split()[1]} is not a subcommand of show")
                        
                        else:
                            self._findings.showAll()

                    case ("comments"):
                        self._findings._comments = not self._findings._comments
                        print(f"Comments are {'on' if self._findings._comments else 'off'}")

                        self._findings._updateConfig("_comments", self._findings._comments)

                    case ("debug"):
                        self._findings._debug = not self._findings._debug
                        print(f"Debug is {'on' if self._findings._debug else 'off'}")

                        self._findings._updateConfig("_debug", self._findings._debug)

                    case "clear-search":
                        self._findings._values = self._findings._AllValues

                    case ("settings"):
                        print("Comments:", self._findings._comments)
                        print("Debug:", self._findings._debug)

                    case ("search"):
                        if len(command.split()) > 1:
                            match command.split()[1].lower():
                                case "ip":
                                    self._findings.search("ip")

                                case "port":
                                    self._findings.search("port")

                                case "service":
                                    self._findings.search("service")

                                case _:
                                    print(f"{command.split()[1].lower()} is not a valid option")

                        else:
                            self._findings.search("ip")
                    
                    case _:
                        print(f"{command.rstrip()} is not a command")