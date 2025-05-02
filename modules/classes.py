import base64, json, os, msvcrt

class nmapFindings:
    _values: list = []
    _loadedId: int = 0

    def __init__(self) -> None:
        self._values = []

    def _export(self, _sessionName: str = "_") -> None:
        _output = []

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

        with open("config.nmapParse", "r") as f:
            _id = len(f.readlines())

        with open("config.nmapParse", "a") as f:
            f.write(f"[{_id},{_sessionName}]: ")
            f.write(data.decode('ascii'))
            f.write("\n")

    def _import(self) -> None:
        with open("config.nmapParse", "r") as f:
            lines = f.readlines()
            _id = len(lines) - 1

            sessions = {}

            for line in lines:
                data = list(str(line.split(":")[0])[1:-1].split(","))
                sessions[data[0]] = data[1]

            if _id >= 1:
                print("Select by ID or Name:")
                for sessionId, sessionName in sessions.items():
                    print(f"{sessionId}: {sessionName}")

                _id = str(input(">"))

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

            entries = lines[_id].split(":")[1] # get the base64 part of the line
            entries = json.loads(base64.b64decode(entries.encode("ascii"))) # Convert back into json

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
        with open("config.nmapParse", "r") as f:
            lines = f.readlines()
            _id = len(lines) - 1

            sessions = {}

            for line in lines:
                data = list(str(line.split(":")[0])[1:-1].split(","))
                sessions[data[0]] = data[1]

            print("Select by ID or Name:")
            for sessionId, sessionName in sessions.items():
                print(f"{sessionId}: {sessionName}")

            _id = str(input(">"))

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
    
        with open("config.nmapParse", "w+") as f:
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

                pos += 1

    def _clear(self) -> None:
        self._values = []

    def showAll(self) -> None:
        for value in self._values:
            for entry in [value._ip, value._port, value._service, value._description]:
                print(entry, end=" ")
            print()

            for entry in value._comments:
                print(entry)

    def showPorts(self) -> None:
        for value in range(len(self._values)):
            if value != 0 and self._values[value-1]._ip != self._values[value]._ip:
                print(f"{self._values[value]._ip}: ")
            elif value == 0:
                print(f"{self._values[value]._ip}: ")

            print(f"\t{self._values[value]._port}")

    def showIps(self) -> None:
        for entry in self._values:
            print(entry._ip)

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

        os.system('cls')
        while _searching:
            char = char.decode('ascii')

            match char:
                case ("\x03" | "\r"):
                    _searching = False
                    break

                case "\x08":
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
            os.system('cls')

class finding:
    _id: int = 0
    _ip: str = ""
    _port: str = ""
    _service: str = ""
    _description: str = ""
    _comments: list = []

    def __init__(self):
        self._ip = ""
        self._port = ""
        self._service = ""
        self._description = ""
        self._comments = []