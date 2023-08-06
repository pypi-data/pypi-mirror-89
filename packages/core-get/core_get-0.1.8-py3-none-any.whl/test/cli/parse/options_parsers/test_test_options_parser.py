from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from unittest import TestCase

from core_get.cli.parse.composite_parser import CompositeParser
from core_get.cli.parse.options_parsers.test_options_parser import TestOptionsParser
from core_get.cli.parse.parser import Parser
from core_get.options.options import Options


@dataclass
class FakeOptions(Options):
    my_option: str


class FakeParser(Parser):
    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('--my-option', default='hej')

    def make_options(self, namespace: Namespace) -> Options:
        return FakeOptions(namespace.my_option)


class TestTestOptionsParser(TestCase):
    def test_fake_parser_parses_fake_argument(self):
        composite_parser = CompositeParser()
        [fake_options, test_options] = composite_parser.parse([FakeParser(), TestOptionsParser()],
                                                              ['--my-option=mos', '--', '--help'])
        self.assertEqual(['--help'], test_options.vunit_arguments)
        self.assertEqual('mos', fake_options.my_option)

    def test_does_not_parse_rest_argument(self):
        composite_parser = CompositeParser()
        [fake_options, test_options] = composite_parser.parse([FakeParser(), TestOptionsParser()],
                                                              ['--', '--help', '--my-option=mos'])
        self.assertEqual(['--help', '--my-option=mos'], test_options.vunit_arguments)
        self.assertEqual('hej', fake_options.my_option)

    def test_parses_correctly_without_vunit_arguments(self):
        composite_parser = CompositeParser()
        [_, test_options] = composite_parser.parse([FakeParser(), TestOptionsParser()],
                                                   ['--my-option=mos'])
        self.assertEqual([], test_options.vunit_arguments)

    def test_fails_on_unrecognized_argument(self):
        composite_parser = CompositeParser()
        with self.assertRaises(SystemExit):
            composite_parser.parse([FakeParser(), TestOptionsParser()], ['--my-bovv=mos'])
