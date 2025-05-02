from modules.classes import nmapFindings
from modules.parser import parser
from modules.cli import cli

_parser = parser()
_findings = nmapFindings()

_cli = cli(_findings, _parser)
_cli._start()
