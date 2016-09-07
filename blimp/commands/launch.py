import time

import boto3
from clint.textui import indent, puts, puts_err
from helpers.aws import json_serialize_instance


def _get_launch_args_and_tags(args, config):

    launch_args = {
        'MinCount': 1,
        'MaxCount': 1,
        'KeyName': config['key_pair'],
        'SubnetId': config['subnets'][args.subnet],
        'InstanceInitiatedShutdownBehavior': 'stop',
    }

    role_config = config['roles'][args.role]
    role_tags = role_config.pop('Tags', [])
    launch_args.update(role_config)

    if args.private_ip_address:
        launch_args['PrivateIpAddress'] = args.private_ip_address

    tags = [{
        'Key': 'Name',
        'Value': args.hostname,
    }]

    for tag in role_tags:
        for k in tag.keys():
            tags.append({'Key': k, 'Value': tag[k]})

    return launch_args, tags


def launch(args, config):
    ec2 = boto3.resource('ec2')

    launch_config, tags = _get_launch_args_and_tags(args, config)
    instance = ec2.create_instances(**launch_config)[0]

    puts_err('New instance id: {}'.format(instance.id))

    with indent(4):
        while instance.state['Code'] is not 16:
            puts_err("Instance state:{}, sleeping for five seconds".format(instance.state['Name']))
            time.sleep(5)
            instance.load()

    puts_err('Tagging {} with the name {}'.format(instance.id, args.hostname))
    instance.create_tags(Tags=tags)

    puts(json_serialize_instance(instance))


def _register_launch(subparsers):
    parser_launch = subparsers.add_parser('launch', help='launch help')
    parser_launch.add_argument('role',
                               type=str,
                               help='Role of the EC2 instance to launch')
    parser_launch.add_argument('-s', '--subnet',
                               type=str,
                               required=True,
                               help='Subnet to launch in')
    parser_launch.add_argument('-n', '--hostname',
                               type=str,
                               required=True,
                               help='Hostname of the new host')
    parser_launch.add_argument('-i', '--private-ip-address',
                               type=str,
                               help='Private ip address to assign')
