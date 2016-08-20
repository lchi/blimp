#!/usr/bin/env python
import os
from argparse import ArgumentParser
from clint.textui import indent, puts


if __name__ == '__main__':
    default_config_file = "{}/blimp_config.yaml".format(
            os.path.dirname(os.path.realpath(__file__)))

    parser = ArgumentParser("Command-line utility for interacting with AWS")
    parser.add_argument('command', type=str, help='command to use')
    parser.add_argument("-f", "--config-file",
            required=False,
            help="Configuration file to use, default: {}".format(default_config_file),
            default=default_config_file)

    args = parser.parse_args()

    import commands
    try:
        getattr(commands, args.command)()
    except AttributeError:
        puts("Command '{}' not found. Available commands:".format(args.command))
        with indent(4):
            all_commands = ["* {}".format(attr) for attr in dir(commands) if not attr.startswith('__')]
            puts("\n".join(all_commands))
