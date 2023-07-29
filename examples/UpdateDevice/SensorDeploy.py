from lib.DeviceAccess import DeviceAccess
import sys
import json

class SensorDeploy(DeviceAccess):

    def get_parser(self):
        if self.argparser is None:
            parser = super().get_parser("SensorDeploy.py","Deploy sensors to the target device for use with SIO")
            parser.add_argument('--sensors',
                                    help='The sensors file to use')
        return self.argparser

    def main(self):
        args = self.get_args()
        if args.sensors is None:
            print(f"Sensors not specified, please specify sensor file to use with upgrade")
            self.get_parser().print_help()
            return -1
        with open(args.sensors) as f:
            self.write_config('sio', 'sensors.json', f.read())
        return 0

if __name__ == '__main__':
    cmd = SensorDeploy()
    sys.exit(cmd.main())