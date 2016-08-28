import boto3
from clint.textui import indent, puts

def ls(args, config):
    ec2 = boto3.resource('ec2')

    filters = [
        {'Name':'instance-state-name', 'Values':['running']}
    ]
    instances = [i for i in ec2.instances.filter(Filters=filters)]
    print len(instances)

def _register_ls(subparsers):
    parser_terminate = subparsers.add_parser('ls')
