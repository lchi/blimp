import boto3
import time
from clint.textui import indent, puts

def _launch_args(args, config):

    role_config = config['roles'][args.role]

    return {
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

def launch(args, config):
    ec2 = boto3.resource('ec2')

    launch_config = _launch_args(args, config)
    instance = ec2.create_instances(**launch_config)[0]

    puts('New instance id: {}'.format(instance.id))

    with indent(4):
        while instance.state['Code'] is not 16:
            puts("Instance state:{}, sleeping for five seconds".format(instance.state['Name']))
            time.sleep(5)
            instance.load()

    puts('Tagging {} with the name {}'.format(instance.id, args.hostname))
    tags = [{
        'Key': 'Name',
        'Value': args.hostname,
    }]
    instance.create_tags(Tags=tags)

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
