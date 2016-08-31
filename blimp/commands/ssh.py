import boto3
import subprocess
import sys
from clint.textui import indent, puts
import shlex

def ssh(args, config):
    ec2 = boto3.resource('ec2')

    hostname = args.hostname
    filters = [
        {'Name':'tag:Name', 'Values':[hostname]},
        {'Name':'instance-state-name', 'Values':['running']}
    ]
    instances = [i for i in ec2.instances.filter(Filters=filters)]

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

def _all_running_instances():
    ec2 = boto3.resource('ec2')

    filters = [
        {'Name':'instance-state-name', 'Values':['running']}
    ]
    return [i for i in ec2.instances.filter(Filters=filters)]

def hostname_completer(prefix, **kwargs):
    instance_names = []
    for i in _all_running_instances():
        for tag in i.tags:
            if tag['Key'] == 'Name' and tag['Value'].startswith(prefix):
                instance_names.append(tag['Value'])
                break

    return instance_names

def _register_ssh(subparsers):
    parser_ssh = subparsers.add_parser('ssh')
    hostname_arg = parser_ssh.add_argument('hostname',
            help='"Name" tag of the instance to connect to')
    hostname_arg.completer = hostname_completer
    parser_ssh.add_argument('-u', '--ssh-user',
            type=str,
            help='ssh username to use')
