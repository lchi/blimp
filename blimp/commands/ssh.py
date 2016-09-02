import subprocess
import shlex
from helpers.aws import get_single_instance_by_name_tag


def ssh(args, config):
    instance = get_single_instance_by_name_tag(args.hostname)

    ssh_user_arg = "{}@".format(args.ssh_user) if args.ssh_user else ''
    command = "ssh {}{}".format(ssh_user_arg, instance.public_ip_address)
    subprocess.call(shlex.split(command))


def _register_ssh(subparsers):
    parser_terminate = subparsers.add_parser('ssh')
    parser_terminate.add_argument('hostname',
                                  type=str,
                                  help='"Name" tag of the instance to connect to')
    parser_terminate.add_argument('-u', '--ssh-user',
                                  type=str,
                                  help='ssh username to use')
