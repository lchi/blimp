def launch(config):
    print config
    pass

def _register_launch(subparsers):
    parser_launch = subparsers.add_parser('launch', help='launch help')
    parser_launch.add_argument('role', type=str,
            help='Role of the EC2 instance to launch')
