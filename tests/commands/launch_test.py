import boto3

from blimp.commands.launch import launch
from moto import mock_ec2
from moto.ec2 import ec2_backends
from unittest import TestCase


# http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python
class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


class TestLaunch(TestCase):

    def get_config(self):
        # Note: looks like moto is resetting after every test?
        # Had trouble doing this in setUp/setUpClass
        backend = ec2_backends['us-east-1']
        vpc = backend.create_vpc('172.20.0.0/16')
        subnet = backend.create_subnet(vpc.id, '172.20.1.0/24', 'us-east-1a')
        security_group = backend.create_security_group('test-sg', 'test sg', vpc.id)

        return {
            'key_pair': 'key-pair-foo',
            'subnets': {
                'subnet-1a': subnet.id
            },
            'roles': {
                'web': {
                    'ImageId': 'ami-1c221e76',
                    'InstanceType': 't2.micro',
                    'SecurityGroupIds': [security_group.id],
                    'EbsOptimized': False,
                    'Monitoring': {
                      'Enabled': True,
                    },
                    'Tags': [
                        {'BillingEnv': 'Development'},
                    ],
                    'BlockDeviceMappings': [{
                        'DeviceName': '/dev/sda1',
                        'Ebs': {
                          'DeleteOnTermination': True,
                          'VolumeType': 'gp2',
                        }
                    }, {
                        'DeviceName': '/dev/sdb',
                        'Ebs': {
                           'VolumeType': 'gp2',
                           'VolumeSize': 30,
                        },
                    }],
                }
            }
        }

    @mock_ec2
    def test_launch(self):
        args = AttributeDict({
            'role': 'web',
            'subnet': 'subnet-1a',
            'hostname': 'test-web',
            'private_ip_address': None,
        })

        config = self.get_config()
        launch(args, config)

        client = boto3.client('ec2')
        instances = client.describe_instances()

        reservations = instances['Reservations'][0]['Instances']
        self.assertEqual(len(reservations), 1)

        instance = reservations[0]

        keys = ['ImageId', 'InstanceType']
        for k in keys:
            self.assertEqual(config['roles']['web'][k], instance[k])
