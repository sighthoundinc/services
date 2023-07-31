from lib.DeviceAccess import DeviceAccess
import sys
import json

class ShServices(DeviceAccess):

    def get_parser(self):
        if self.argparser is None:
            parser = super().get_parser("ShServices.py","Run the sh-services script on a remote device")
            parser.add_argument('--args',
                                    help='Argument list to pass to sh-services on the remote device')
        return self.argparser

    def main(self):
        args = self.get_args()
        rc = 0
        connection = self.get_connection()
        with connection.cd('/data/sighthound/services'):
            try:
                connection.run(f'./scripts/sh-services {args.args}')
            except Exception as e:
                print(f"Caught exception {e} attempting to update ${args.device}")
                rc = -1

        return rc

if __name__ == '__main__':
    cmd = ShServices()
    sys.exit(cmd.main())