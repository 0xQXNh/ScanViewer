import datetime

class finding:
    _id: int = 0
    _ip: str = ""
    _port: int = -1
    _service: str = ""
    _protocol: str = ""
    _description: str = ""
    _comments: list = []

    _datetime: datetime.datetime = None
    _file: str = ""

    def __init__(self):
        self._ip = ""
        self._port = -1
        self._service = ""
        self._protocol = ""
        self._description = ""
        self._comments = []

        self._datetime = datetime.datetime.now()
        self._filename = ""

    def setPort(self, port) -> None:
        self._port = int(port)