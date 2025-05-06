import regex

from modules.allFindings import allFindings
from modules.finding import finding

class parser:
    def __init__(self):
        return

    def _openFile(self, path: str) -> tuple[list, str]:
        output: list = []

        if not path.split(".")[-1] in ["nmap", "nessus", "naabu"]:
            print("Wrong file extension. Please use a .nmap file.")

        extension = path.split(".")[-1]

        try:
            with open(path, "r") as f:
                for line in f.readlines():
                    output.append(line.rstrip())

        except:
            print(f"Unable to open file: {path}")

        return (output, extension)

    def _formatPort(self, _input: list) -> list:
        _output = []
        for line in _input:
            if line != "":
                _output.append(line)

        return _output

    def _getPortLocs(self, _input: list) -> list[int]:
        locs = []
        for line in range(len(_input)):
            if regex.match("[0-9]{1,5}\\/", _input[line]):
                locs.append(line)
        
        return locs

    def _getNextGap(self, _input: list, currentPos: int) -> int:
        for entry in range(currentPos, len(_input)):
            if _input[entry] == "":
                return entry

    def parseFile(self, _findings: allFindings, path: str) -> allFindings:
        _input, extension = self._openFile(path)

        if extension == "nmap":
            _finding = finding()

            locs = self.getPortLocs(_input)
            posCount = 0

            for _line in range(len(_input)):
                if posCount < len(locs)-1 and _line >= locs[posCount+1] or _input[_line] == "":
                    _findings._values.append(_finding)
                    _finding = finding()
                    _finding._id = len(_findings._values)
                    posCount += 1

                line = _input[_line]

                if regex.match("Nmap scan report for", line):
                    ip = regex.search("([0-9]{1,3}\\.){3}([0-9]{1,3})", line).captures()[0]

                    nextGap = self.getNextGap(_input, _line)

                    entries = False
                    for entry in _input[_line:nextGap]:
                        if entries == False and regex.match("[0-9]{1,5}\\/", entry):
                            entries = True

                    if not entries:
                        _finding._ip = ip

                elif regex.match("[0-9]{1,5}\\/", line):
                    line = line.split(" ")
                    line = self.formatPort(line)
                    
                    Port = line[0]
                    Service = line[2]
                    Description = ' '.join(line[3:])
                    
                    _finding._ip = ip
                    _finding._port = Port
                    _finding._service = Service
                    _finding._description = Description

                else:
                    if line.startswith("|"):
                        _finding._comments.append(line)

        elif extension == "naabu": #Assuming naabu port scan output
            for line in _input:
                line = line.split(":")
                
                _finding = finding()

                _finding._ip = line[0]
                _finding._port = line[1]

                _findings._values.append(_finding)

        return _findings