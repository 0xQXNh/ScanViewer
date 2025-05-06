import base64, json, os, regex

from modules.finding import finding
from sys import platform

if platform == "win32":
    import msvcrt
    CLEAR_COMMAND = "cls"

else:
    import getch as msvcrt
    CLEAR_COMMAND = "clear"

class allFindings:
    _values: list = []
    _loadedId: int = -1
    _comments: bool = True

    def __init__(self) -> None:
        self._values = []

    def _getLoadedIps(self) -> str:
        ips: dict = {}
        for ip in self._values:
            if not ip in ips.keys():
                ips[ip] = {}

        return str(len(ips.keys()))

    def _export(self, _sessionName: str = "_") -> None:
        _output = []

        if len(self._values) == 0:
            _inp = input(f"Session has no entries. Write anyway? [y/N] >")

            if _inp.lower() in ["n", ""]:
                return

            elif _inp.lower() == "y":
                pass

            else:
                print("Invalid argument.")

        for value in self._values:
            data = {}
            data['id'] = value._id
            data['ip'] = value._ip
            data['port'] = value._port
            data['service'] = value._service
            data['description'] = value._description
            data['comments'] = value._comments

            _output.append(data)

        data = base64.b64encode(json.dumps(_output).encode('ascii'))

        if not "config.svs" in os.listdir():
            open("config.svs", "w")

        lines = []

        with open("config.svs", "r") as f:
            allNames = []

            lines = f.readlines()

            for line in lines:
                allNames.append(line.split(':')[0].split(',')[-1][:-1])

            if self._loadedId == -1:
                _id = len(lines)
            else:
                _id = self._loadedId

        if _sessionName in allNames and _sessionName != "_":
            print(f"Session name already exists. Not saved")
            return      

        if self._loadedId == -1:
            with open("config.svs", "a") as f:
                f.write(f"[{_id},{_sessionName}]: ")
                f.write(data.decode('ascii'))
                f.write("\n")
            
            self._loadedId = _id

        else:
            with open("config.svs", "w") as f:
                for line in range(len(lines)):
                    if line == self._loadedId:
                        f.write(f"[{_id},{_sessionName}]: ")
                        f.write(data.decode('ascii'))
                        f.write("\n")
                    else:
                        f.write(lines[line])
                
            print(f"Appending to previously written session: {self._loadedId}")
            pass

        print(f"Written {_id}: {_sessionName} to config")

    def _import(self) -> None:
        if not "config.svs" in os.listdir():
            print("No config file exists. A session must be exported first")
            return

        with open("config.svs", "r") as f:
            lines = f.readlines()
            _id = len(lines) - 1

            sessions = {}

            for line in lines:
                data = list(str(line.split(":")[0])[1:-1].split(","))
                sessions[data[0]] = data[1]

            if _id >= 1:
                for sessionId, sessionName in sessions.items():
                    print(f"{sessionId}: {sessionName}")

                _id = str(input("[Select by ID or Name] >"))

                if regex.findall("^[0-9]+$", _id):
                    _id = int(_id)

                    if _id >= len(lines):
                        print("Value must be in the list")
                        return
                
                else:
                    _id = str(_id)
                    found = False

                    if _id == "_":
                        print("Session name not valid")

                    for sessionId, sessionName in sessions.items():
                        if sessionName == _id:
                            _id = int(sessionId)
                            found = True

                    if not found:
                        print("Session name does not exist")
                        return
                    
            if len(lines) == 0:
                print("No saved sessions to load")
                return

            try:
                entries = lines[_id].split(":")[1] # get the base64 part of the line
                entries = json.loads(base64.b64decode(entries.encode("ascii"))) # Convert back into json

            except:
                print(f"Failed to decode contents of session. Maybe the config file is corrupt.")
                return

            self._loadedId = _id

            _name = lines[_id].split(":")[0].split(",")[-1][:-1]

            print(f"Loaded {_id}{": '" + _name + "'" if _name != "_" else ""} from config")

            for entry in entries:
                _finding = finding()
                _finding._id = entry['id']
                _finding._ip = entry['ip']
                _finding._port = entry['port']
                _finding._service = entry['service']
                _finding._description = entry['description']
                    
                for section in entry['comments']:
                    _finding._comments.append(section)

                self._values.append(_finding)

    def _delete(self) -> None:
        lines = []

        with open("config.svs", "r") as f:
            lines = f.readlines()
            _id = len(lines) - 1

            sessions = {}

            for line in lines:
                data = list(str(line.split(":")[0])[1:-1].split(","))
                sessions[data[0]] = data[1]

            for sessionId, sessionName in sessions.items():
                print(f"{sessionId}: {sessionName}")

            _id = str(input("[Select by ID or name] >"))

            if _id.isdigit():
                _id = int(_id)

                if _id >= len(lines):
                    print("Value must be in the list")
                    return
            
            elif _id.isalpha():
                _id = str(_id)
                found = False

                if _id == "_":
                    print("Session name not valid")

                for sessionId, sessionName in sessions.items():
                    if sessionName == _id:
                        _id = int(sessionId)
                        found = True

                if not found:
                    print("Session name does not exist")
                    return
                
        if _id == self._loadedId:
            self._loadedId = -1

        if _id < self._loadedId:
            self._loadedId -= 1
    
        with open("config.svs", "w+") as f:
            pos: int = 0
            currentId: int = 0

            for line in lines:
                if pos != _id:
                    line = line.strip("\n")

                    sessionData = str(line.split(":")[0])[1:-1].split(",")
                    sessionData[0] = str(currentId)
                    
                    sessionData = ','.join(sessionData)

                    line = '[' + sessionData + ']:' + line.split(":")[1]

                    f.write(line)
                    f.write("\n")

                    currentId += 1

                pos += 1

    def _clear(self) -> None:
        self._values = []
        self._loadedId = -1

    def showAll(self) -> None:
        if len(self._values) == 0:
            print("No values to display")

        for value in self._values:
            for entry in [value._ip, value._port, value._service, value._description]:
                print(entry, end=" ")
            print()

            if self._comments:
                for entry in value._comments:
                    print(entry)

    def showPorts(self) -> None:
        if len(self._values) == 0:
            print("No values to display")

        for value in range(len(self._values)):
            if value != 0 and self._values[value-1]._ip != self._values[value]._ip:
                print(f"{self._values[value]._ip}: ")
            elif value == 0:
                print(f"{self._values[value]._ip}: ")

            print(f"\t{self._values[value]._port}")

    def showIps(self) -> None: #de dupe output list
        if len(self._values) == 0:
            print("No values to display")

        ips = {}
        for entry in self._values:
            if not entry._ip in ips:
                ips[entry._ip] = {}

        for ip in ips.keys():
            print(ip)

    def search(self) -> None:
        _searching: bool = True
        ipMap: dict = {}
        searchTerm: str = ""
        char: bytes = b""

        for pos in range(len(self._values)):
            if not self._values[pos]._ip in ipMap.keys():
                ipMap[self._values[pos]._ip] = []
                ipMap[self._values[pos]._ip].append(pos)

            else:
                ipMap[self._values[pos]._ip].append(pos)

        os.system(CLEAR_COMMAND)
        while _searching:
            try:
                char = char.decode('ascii')

            except:
                pass

            print(repr(char))

            match char:
                case ("\x03" | "\r" | "\n"):
                    _searching = False
                    break

                case ("\x08" | "\x7f"):
                    searchTerm = searchTerm[:-1]

                case _:
                    searchTerm += char

            for ipKey in ipMap.keys():
                if searchTerm == "":
                    print(ipKey)
                
                elif searchTerm in ipKey:
                    print(ipKey)

            print(f"[Search by ip] > {searchTerm}")

            char = msvcrt.getch()
            os.system(CLEAR_COMMAND)