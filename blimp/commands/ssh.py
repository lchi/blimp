import boto3
import subprocess
import sys
from clint.textui import indent, puts, prompt
from pprint import pformat
import shlex

def ssh(args, config):
    ec2 = boto3.resource('ec2')

    hostname = args.hostname
    instances = [i for i in ec2.instances.filter(Filters=[{'Name':'tag:Name', 'Values':[hostname]}])]

    num_instances = len(instances)
    if num_instances is 0:
        puts("No instance returned for {}".format(hostname))
        sys.exit(1)
    elif num_instances > 1:
        puts("Multiple instances returned for {}".format(hostname))
        with indent(4):
            for instance in query_results:
                puts("{}".format(instance))
        sys.exit(1)

    instance = instances[0]

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
