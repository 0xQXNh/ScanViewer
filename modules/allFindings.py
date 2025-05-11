import base64, json, os, regex, operator

from modules.finding import finding
from sys import platform

if platform == "win32":
    import msvcrt
    CLEAR_COMMAND = "cls"

else:
    import getch as msvcrt
    CLEAR_COMMAND = "clear"

class allFindings:
    _AllValues: list = []
    _values: list = []
    _loadedId: int = -1
    _loadedSessionName: str = "_"
    _comments: bool = True

    _debug: bool = False

    def __init__(self) -> None:
        self._values = []

        if os.path.exists("scanViewer.config"):
            with open("scanViewer.config", "r") as f:
                for line in f.readlines():
                    line = line.rstrip()
                    setting = line.split(":")[0].lower()
                    value = line.split(":")[-1].lower()

                    match setting:
                        case "_debug":
                            self._debug = True if value == "true" else False

                        case "_comments":
                            self._comments = True if value == "true" else False

                        case "_lastsession":
                            self._import(int(value))

    def _addFinding(self, data: finding) -> None:
        for finding in self._values:
            if data._ip == finding._ip and data._port == finding._port:
                
                os.system(CLEAR_COMMAND)

                print(f"{'IP:':<10} {data._ip:<30}{finding._ip}")
                print(f"{'Port:':<10} {data._port:<30}{finding._port}")
                print(f"{'Service:':<10} {data._service:<30}{finding._service}")
                print(f"{'Filename:':<10} {data._filename:<30}{finding._filename}")
                print(f"{'Datetime:':<10} {str(data._datetime):<30}{str(finding._datetime)}")

                inp = input("Finding already exists. Overwrite finding? [(y)es/(N)o] >").lower()

                if inp == "y":
                    self._removeId(finding._id)

                elif inp == "n" or inp == "":
                    return

                else:
                    print("Invalid option.")
                    return
        
        self._values.append(data)
        self._AllValues.append(data)

    def _updateConfig(self, setting: str, value: bool) -> None:
        if not os.path.exists("scanViewer.config"):
            open("scanViewer.config", "w")

        configLines = []
        with open("scanViewer.config", "r") as f:
            for line in f.readlines():
                configLines.append(line.rstrip())

        found = False
        for _line in range(len(configLines)):
            line = configLines[_line]
            if setting in line:
                configLines[_line] = f"{setting}:{value}"
                found = True

        if not found:
            configLines.append(f"{setting}:{value}")

        with open("scanViewer.config", "w") as f:
            for line in configLines:
                f.write(line)
                f.write("\n")

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
            data['datetime'] = str(value._datetime)
            data['filename'] = value._filename

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
        
        if _sessionName == "_" and self._loadedSessionName != "_":
            _sessionName = self._loadedSessionName

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

    def _import(self, id: int = -1) -> None:
        if not "config.svs" in os.listdir():
            print("No config file exists. A session must be exported first")
            return

        with open("config.svs", "r") as f:
            lines = f.readlines()
            _id = len(lines) - 1

            if id != -1:
                entries = lines[id].split(":")[1] # get the base64 part of the line
                entries = json.loads(base64.b64decode(entries.encode("ascii"))) # Convert back into json

                for entry in entries:
                    _finding = finding()
                    _finding._id = entry['id']
                    _finding._ip = entry['ip']
                    _finding.setPort(entry['port'])
                    _finding._service = entry['service']
                    _finding._description = entry['description']
                    _finding._datetime = entry['datetime']
                    _finding._filename = entry['filename']
                        
                    for section in entry['comments']:
                        _finding._comments.append(section)

                    self._values.append(_finding)

                self._AllValues = self._values
                self._loadedId = id

                _name = lines[id].split(":")[0].split(",")[-1][:-1]
                self._loadedSessionName = _name

                print(f"Loaded {_id}{": '" + _name + "'" if _name != "_" else ""} from config with {self._getLoadedIps()} ips")
                return

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
                        return

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
            self._loadedSessionName = _name

            print(f"Loaded {_id}{": '" + _name + "'" if _name != "_" else ""} from config")

            for entry in entries:
                _finding = finding()
                _finding._id = entry['id']
                _finding._ip = entry['ip']
                _finding.setPort(entry['port'])
                _finding._service = entry['service']
                _finding._description = entry['description']
                _finding._datetime = entry['datetime']
                _finding._filename = entry['filename']
                    
                for section in entry['comments']:
                    _finding._comments.append(section)

                self._values.append(_finding)

            self._AllValues = self._values

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
        self._AllValues = []
        self._loadedId = -1
        self._loadedSessionName = "_"

    def _orderFindings(self) -> None:
        self._values = sorted(self._values, key=operator.attrgetter('_port'))
        self._values = sorted(self._values, key=operator.attrgetter('_ip'))

    def _removeId(self, id: int) -> None:
        tempFindings = []
        for finding in range(len(self._values)):
            if self._values[finding]._id != id:
                tempFindings.append(self._values[finding])
            else:
                print(f"Removed {self._values[finding]._id}")
        self._values = tempFindings
        
    def showAll(self) -> None:
        if len(self._values) == 0:
            print("No values to display")

        previousIp = ""
        for value in self._values:
            if previousIp != value._ip:
                print(f"{value._ip}")
                previousIp = value._ip

            print(f"\t{value._port if value._port != -1 else ''}{'/' + value._protocol if value._protocol != '' else ''} {value._service if value._service != '' else ''}")
            if value._description != "":
                print(f"\t{value._description}")

            if self._comments:
                if type(value._comments) is str:
                    print(f"\t{value._comments}")

                else:
                    for entry in value._comments:
                        print(f"\t{entry}")

            if self._debug:
                print("\t" + str(value._id), str(value._datetime), value._filename)

            print()

    def showPorts(self) -> None:
        if len(self._values) == 0:
            print("No values to display")

        for value in range(len(self._values)):
            if value != 0 and self._values[value-1]._ip != self._values[value]._ip:
                print(f"{self._values[value]._ip}: ")
            elif value == 0:
                print(f"{self._values[value]._ip}: ")

            print(f"\t{self._values[value]._port}")

    def showIps(self) -> None:
        if len(self._values) == 0:
            print("No values to display")

        ips = {}
        for entry in self._values:
            if not entry._ip in ips:
                ips[entry._ip] = {}

        for ip in ips.keys():
            print(ip)

    def search(self, search_value: str = "ip") -> None:
        _searching: bool = True
        ipMap: dict = {}
        searchTerm: str = ""
        char: bytes = b""

        for pos in range(len(self._values)):
            if not self._values[pos]._ip in ipMap.keys():
                ipMap[self._values[pos]._ip] = []
                ipMap[self._values[pos]._ip].append(self._values[pos])

            else:
                ipMap[self._values[pos]._ip].append(self._values[pos])

        os.system(CLEAR_COMMAND)
        while _searching:
            try:
                char = char.decode('ascii')

            except:
                pass

            match char:
                case ("\x03" | "\r" | "\n"):
                    _searching = False
                    self._values = valuesInScope
                    break

                case ("\x08" | "\x7f"):
                    searchTerm = searchTerm[:-1]

                case _:
                    searchTerm += char

            valuesInScope = []
            for ipKey in ipMap.keys():
                for entry in ipMap[ipKey]:
                    if searchTerm == "":
                        valuesInScope.append(entry)
                
                    elif searchTerm in entry._ip and search_value == "ip":
                        valuesInScope.append(entry)

                    elif searchTerm in str(entry._port) and search_value == "port":
                        valuesInScope.append(entry)
            
                    elif searchTerm in entry._service and search_value == "service":
                        valuesInScope.append(entry)
            
            for value in valuesInScope:
                if search_value == "port":
                    print(value._ip, value._port)

                elif search_value == "service":
                    print(value._ip, value._service)
                
                else:
                    print(value._ip)    

            print(f"[Search by {search_value}] > {searchTerm}")

            char = msvcrt.getch()
            os.system(CLEAR_COMMAND)