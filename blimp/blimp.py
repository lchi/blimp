import os
import yaml
from argparse import ArgumentParser
from clint.textui import indent, puts

def _get_parser():
    default_config_file = os.path.normpath(os.path.expanduser("~/.blimp/config.yaml"))

    parser = ArgumentParser()
    parser.add_argument("-f", "--config-file",
            required=False,
            help="Configuration file to use, default: {}".format(default_config_file),
            default=default_config_file)

    return parser

def _register_subparsers(parser, commands_module):
    subparsers = parser.add_subparsers(help="commands", dest="command")

    register_functions = filter(lambda f: f.startswith('_register'), dir(commands_module))
    for rf in register_functions:
        getattr(commands_module, rf)(subparsers)

def parse_config(config_filename):
    with open(config_filename, 'r') as f:
        return yaml.load(f)

def run_command(commands, args, config):
    getattr(commands, args.command)(args, config)

def main():
    import commands

    parser = _get_parser()
    _register_subparsers(parser, commands)
    args = parser.parse_args()

    config = parse_config(args.config_file)
    run_command(commands, args, config)

if __name__ == '__main__':
    main()
