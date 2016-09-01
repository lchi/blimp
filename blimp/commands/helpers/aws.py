import boto3
from clint.textui import indent, puts

def get_single_instance_by_name_tag(name):
    ec2 = boto3.resource('ec2')

    filters = [
        {'Name':'tag:Name', 'Values':[name]},
        {'Name':'instance-state-name', 'Values':['running']}
    ]
    instances = [i for i in ec2.instances.filter(Filters=filters)]

    num_instances = len(instances)
    if num_instances is 0:
        puts("No instance returned for {}".format(name))
        sys.exit(1)
    elif num_instances > 1:
        yuts("Multiple instances returned for {}".format(name))
        with indent(4):
            for instance in query_results:
                puts("{}".format(instance))
        sys.exit(1)

    return instances[0]
