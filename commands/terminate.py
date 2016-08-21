import boto3
from clint.textui import indent, puts, prompt
from pprint import pformat

def _get_instance_details(instance):
    return {
       'tags': instance.tags,
       'launch_time': instance.launch_time.isoformat(),
       'instance_type': instance.instance_type,
       'state': instance.state,
       'key_name': instance.key_name,
       'public_dns_name': instance.public_dns_name,
       'private_dns_name': instance.private_dns_name,
       'placement': instance.placement,
   }

def terminate(args, config):
    ec2 = boto3.resource('ec2')
    instance_id = args.instance_id
    instance = ec2.Instance(instance_id)

    puts("Instance details:")
    with indent(4):
        puts(pformat(_get_instance_details(instance)))

    confirm = prompt.query("Terminate instance {}? (y/n)".format(instance_id), validators=[])

    if confirm is "y":
        instance.terminate()
        puts("termination request issued".format(instance_id))
    else:
        puts("aborted")

def _register_terminate(subparsers):
    parser_terminate = subparsers.add_parser('terminate', help='terminate help')
    parser_terminate.add_argument('instance_id',
            type=str,
            help='id of the instance to terminate')
