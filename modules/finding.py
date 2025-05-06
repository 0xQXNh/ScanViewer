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