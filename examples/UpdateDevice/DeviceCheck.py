from lib.DeviceAccess import DeviceAccess
import sys

class DeviceCheck(DeviceAccess):
    def main(self):
        rc = 0
        if self.get_free_space_data_part_mb() < 100:
            print(f"Device {self.get_device_name()} is almost out of data space, only {self.get_free_space_data_part_mb()} MB remaining")
            rc = -1
        services = self.get_services_ps()
        for service in services:
            if services[service]['enabled']:
                if not services[service]['running']:
                    print(f"Device {self.get_device_name()} service {service} is enabled but not running")
                    rc = -1

        return rc

if __name__ == '__main__':
    cmd = DeviceCheck()
    sys.exit(cmd.main())