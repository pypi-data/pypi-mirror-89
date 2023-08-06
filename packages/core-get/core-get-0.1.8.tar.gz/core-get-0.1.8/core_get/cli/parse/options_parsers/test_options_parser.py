from argparse import ArgumentParser, Namespace, REMAINDER
from dataclasses import dataclass
from typing import List

from core_get.actions.test.test_options import TestOptions
from core_get.cli.parse.parser import Parser
from core_get.options.options import Options


@dataclass
class TestOptionsParser(Parser):
    name: str = 'test'
    usage: str = '-- <vunit-args>'
    description: str = 'Run VUnit tests'

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('args', nargs=REMAINDER, help='VUnit options')

    def make_options(self, namespace: Namespace) -> Options:
        return TestOptions(self._make_rest_args(namespace.args))

    def _make_rest_args(self, args: List[str]) -> List[str]:
        if len(args) == 0:
            return []

        assert args[0] == '--'
        return args[1:]
