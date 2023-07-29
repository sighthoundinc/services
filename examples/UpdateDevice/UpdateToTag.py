from lib.DeviceAccess import DeviceAccess
from fabric import Connection
import sys
class UpdateToTag(DeviceAccess):
    def get_parser(self):
        if self.argparser is None:
            parser = super().get_parser("UpdateToTag.py","Updates devices to a specific commit reference/tag")
            parser.add_argument('--reference',
                                    help='The commit reference to use with git checkout command, may be a hash or tag')
            parser.add_argument('--remote',
                                    help='The remote to use with git fetch command (default origin)')
        return self.argparser
    def main(self):
        connection = self.get_connection()
        args = self.get_args()
        if args.reference is None:
            print(f"Reference not specified, please specify a reference to upgrade to")
            self.get_parser.print_help()
            return -1
        if args.remote is None:
            args.remote = 'origin'

        rc = 0
        with connection.cd('/data/sighthound/services'):
            try:
                print(f"Stopping services")
                connection.run(f'./scripts/sh-services down all', timeout=60*5)
                print(f"Cleaning media to free space for new docker pulls")
                connection.run(f'./scripts/sh-services clean_media')
                connection.run(f'git fetch {args.remote}', env=self.get_proxy_env())
                connection.run(f'git stash save')
                connection.run(f'git reset --hard {args.reference}')
                print(f"Restarting services")
                connection.run(f'./scripts/sh-services up all', timeout=60*20)
                print(f"Pruning containers and images")
                connection.run(f'docker container prune -f')
                connection.run(f'docker image prune -a -f')
            except Exception as e:
                print(f"Caught exception {e} attempting to update ${args.device}")
                rc = -1

        return rc

if __name__ == '__main__':
    cmd = UpdateToTag()
    sys.exit(cmd.main())