import time

import boto3
from clint.textui import indent, puts, puts_err
from helpers.aws import json_serialize_instance


def _get_launch_args_and_tags(args, config):

    role_config = config['roles'][args.role]

    launch_args = {
        'ImageId': role_config['ami_id'],
        'MinCount': 1,
        'MaxCount': 1,
        'KeyName': config['key_pair'],
        'SecurityGroupIds': role_config['security_group_ids'],
        'InstanceType': role_config['instance_type'],
        'Monitoring': {
            'Enabled': role_config['monitoring'],
        },
        'SubnetId': config['network']['availability_zones'][args.availability_zone]['subnet_id'],
        'InstanceInitiatedShutdownBehavior': 'stop',
        'EbsOptimized': role_config['ebs_optimized'],
    }

    if args.private_ip_address:
        launch_args['PrivateIpAddress'] = args.private_ip_address
    if 'iam_instance_profile_arn' in role_config:
        launch_args['IamInstanceProfile'] = {
            'Arn': role_config['iam_instance_profile_arn'],
        }
    if 'block_device_mappings' in role_config:
        launch_args['BlockDeviceMappings'] = role_config['block_device_mappings']

    tags = [{
        'Key': 'Name',
        'Value': args.hostname,
    }]

    for tag in role_config.get('tags', []):
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
    parser_launch.add_argument('-a', '--availability-zone',
                               type=str,
                               required=True,
                               help='Availability zone to launch in')
    parser_launch.add_argument('-n', '--hostname',
                               type=str,
                               required=True,
                               help='Hostname of the new host')
    parser_launch.add_argument('-i', '--private-ip-address',
                               type=str,
                               help='Private ip address to assign')
