from modules.allFindings import allFindings
from modules.parser import parser
from modules.cli import cli

_parser = parser()
_findings = allFindings()

_cli = cli(_findings, _parser)
_cli._start()
