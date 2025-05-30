import regex
import xml.etree.ElementTree as ET

from modules.allFindings import allFindings
from modules.finding import finding

class parser:
    def __init__(self):
        return

    def _openFile(self, path: str) -> tuple[list, str]:
        output: list = []

        if not path.split(".")[-1] in ["nmap", "nessus", "naabu", "gnmap", "xml"]:
            print("Wrong file extension. Please use a .nmap file.")

        extension = path.split(".")[-1]

        if extension == "nessus":
            return ([], extension)

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
        if "/" in path:
            filename = path.split("/")[-1]

        elif "\\" in path:
            path = path.replace("\\", "/")
            filename = path.split("/")[-1]

        else:
            filename = path

        _input, extension = self._openFile(path)

        if extension == "nmap":
            _finding = finding()

            locs = self._getPortLocs(_input)
            posCount = 0

            for _line in range(len(_input)):
                if posCount < len(locs)-1 and _line >= locs[posCount+1] or _input[_line] == "":
                    _findings._addFinding(_finding)
                    _finding = finding()
                    _finding._id = len(_findings._values)
                    posCount += 1

                line = _input[_line]

                if regex.match("Nmap scan report for", line):
                    ip = regex.search("([0-9]{1,3}\\.){3}([0-9]{1,3})", line).captures()[0]

                    nextGap = self._getNextGap(_input, _line)

                    entries = False
                    for entry in _input[_line:nextGap]:
                        if entries == False and regex.match("[0-9]{1,5}\\/", entry):
                            entries = True

                    if not entries:
                        _finding._ip = ip

                elif regex.match("[0-9]{1,5}\\/", line):
                    line = line.split(" ")
                    line = self._formatPort(line)
                    
                    Port = line[0].split("/")[0]
                    Protocol = line[0].split("/")[1]
                    Service = line[2]
                    Description = ' '.join(line[3:])
                    
                    _finding._ip = ip
                    _finding.setPort(Port)
                    _finding._service = Service
                    _finding._protocol = Protocol
                    _finding._description = Description

                    _finding._filename = filename

                else:
                    if line.startswith("|"):
                        _finding._comments.append(line)

        elif extension == "naabu":
            for line in _input:
                line = line.split(":")
                
                _finding = finding()

                _finding._id = len(_findings._values)
                _finding._ip = line[0]
                _finding.setPort(line[1])

                _finding._filename = filename

                _findings._addFinding(_finding)

        elif extension == "gnmap":
            for line in _input:
                portsIndex: int = -1
                if "Host" in line and "Ports: " in line:
                    ip = line.split(" ")[1].rstrip()
                    line = line.split("Ports: ")[-1]

                    line = line.split("/,")
                    if "\t" in line[-1]:
                        line = line[:-1] + line[-1].split("\t")[:-1]

                    for entry in line:
                        _finding = finding()
                        _finding._ip = ip
                        _finding._id = len(_findings._values)
                        _finding._filename = filename
                        dataPos: int = 0
                        for data in entry.split("/"):
                            match dataPos:
                                case 0:
                                    _finding._port = int(data)

                                case 2:
                                    _finding._protocol = data

                                case 4:
                                    _finding._service = data

                                case 6:
                                    _finding._description = data

                            dataPos += 1

                        _findings._addFinding(_finding)
                                    
        elif extension == "xml": # I don't want to do this tbh
            pass

        elif extension == "nessus":
            try:
                tree = ET.parse(path)

            except:
                print("Failed to parse file")
                return _findings

            report = tree.find("Report")
            reportHosts = report.findall("ReportHost")

            for reportHost in reportHosts:
                ip = reportHost.attrib['name']
                reportItems = reportHost.findall("ReportItem")

                for reportItem in reportItems:
                    if reportItem.attrib['pluginFamily'] == "Port scanners":
                        data = reportItem.attrib
                        _finding = finding()

                        _finding._ip = ip
                        _finding._id = len(_findings._values)
                        
                        _finding._service = data['svc_name'] if data['svc_name'] != "unknown" else ""
                        _finding._protocol = data['protocol']
                        _finding.setPort(data['port'])
                        _finding._comments = reportItem.find("plugin_output").text

                        _finding._filename = filename

                        _findings._addFinding(_finding)

        return _findings