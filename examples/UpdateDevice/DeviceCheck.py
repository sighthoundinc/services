from lib.DeviceAccess import DeviceAccess
import sys

class DeviceCheck(DeviceAccess):
    def main(self):
        if self.get_free_space_data_part_mb() < 100:
            print(f"Device is almost out of data space, only {self.get_free_space_data_part_mb()} MB remaining")
            return -1
        return 0

if __name__ == '__main__':
    cmd = DeviceCheck()
    sys.exit(cmd.main())