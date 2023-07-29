from fabric import Connection
import argparse
from io import BytesIO, StringIO
from lib.DeviceWebAPI import DeviceWebAPI
import json

class DeviceAccess:
    DEFAULT_USER = 'root'
    DEFAULT_PASSWORD = 'baidnncam'
    args = None
    connection = None
    argparser = None
    env_json = None
    web_api = None

    def get_parser(self,parent_test="",parent_description=""):
        if self.argparser is None:
            argparser = argparse.ArgumentParser(prog=parent_test,
                                                usage='%(prog)s [options]',
                                                description=parent_description,
                                                formatter_class=argparse.RawTextHelpFormatter)
            argparser.add_argument('-d',
                                   '--device',
                                   help='The IP address or name of the device')

            argparser.add_argument('-u',
                                   '--user',
                                   help=f"The SSH username (default is {self.DEFAULT_USER})")

            argparser.add_argument('-p',
                                   '--password',
                                   help=f'The SSH password (default is {self.DEFAULT_PASSWORD})')

            argparser.add_argument('-k',
                                   '--key',
                                   help='The SSH key file (used instead of password if specified)')

            self.argparser = argparser
        return self.argparser

    def get_proxy_env(self):
        if self.env_json == None:
            env_json = {}
            try:
                fd = BytesIO()
                conn = self.get_connection()
                conn.get('/tmp/system/proxy.env', fd)
                content = fd.getvalue().decode('utf-8')
                for line in content.splitlines():
                    env = line.split('=')
                    if len(env) == 2:
                        env_json[env[0]] = env[1]
            except Exception as e:
                pass
            print(f"Using proxy env {env_json}")
            self.env_json = env_json
        return self.env_json

    def get_args(self):
        if self.args is None:
            self.args = self.get_parser().parse_args()

            if self.args.user is None:
                print(f"No user specified, using {self.DEFAULT_USER}")
                self.args.user=self.DEFAULT_USER
        return self.args

    def get_free_space_data_part_mb(self):
        return int(self.get_connection().run("df /data/ | awk '{print $4}' | tail -n 1").stdout)/1024

    def get_services_ps(self):
        connection =  self.get_connection()
        services = {}
        with connection.cd('/data/sighthound/services'):
            response = connection.run("./scripts/sh-services ps all").stdout
            for line in response.splitlines():
                fields = line.split()
                if len(fields) >= 2:
                    if fields[1] == 'disabled':
                        services[fields[0]] = { 'enabled': False, 'running': False}
                    elif fields[1] == 'enabled':
                        services[fields[0]] = { 'enabled': True }
                        if len(fields) >= 3:
                            if fields[2] == '(running)':
                                services[fields[0]]['running'] = True
                            else:
                                services[fields[0]]['running'] = False
        return services

    def get_device_name(self):
        return self.get_args().device

    def get_password(self):
        if self.get_args().password is None:
            return self.DEFAULT_PASSWORD
        return self.get_args().password

    def get_connection(self):
        args = self.get_args()
        if args.device is None:
            print("Missing device argument")
            self.get_parser().print_help()
            raise RuntimeError("Must specify device as argument")
        if self.connection is None:
            if args.key is not None:
                print("Connecting with SSH key")
                self.connection = Connection(
                    host=f'{args.user}@{args.device}',
                    connect_kwargs={
                        "key_filename": args.key,
                        "password": args.password
                    })
            elif args.password is not None or self.DEFAULT_PASSWORD is not None:
                password = self.get_password()
                print("Connecting with user/pass")
                self.connection = Connection(
                    host=f'{args.user}@{args.device}',
                    connect_kwargs={
                        "password": password
                    })
            else:
                print("Connecting with no password")
                self.connection = Connection(
                    host=f'{args.user}@{args.device}',
                    connect_kwargs={
                        "password": "",
                        "look_for_keys": False
                    })
        return self.connection

    def get_web_api(self):
        if self.web_api is None:
            self.web_api = DeviceWebAPI({'password' : self.get_password(), 'host' : self.get_args().device })
        return self.web_api

    def write_config(self, service, file, content):
        found = False
        for entry in self.get_web_api().get_response(f'analytics/config/{service}'):
            if entry.get('filename',None) == file:
                found = True
                break
        if not found:
            # If the file isn't there yet we don't currently (afaik) have a way to add it, so use SSH to do this
            print(f"File {file} not yet found on the server for service {service}, adding")
            fd = StringIO(str(content))
            self.get_connection().put(fd,f'/data/sighthound/services/{service}/conf/{file}')
        self.get_web_api().put_request(f'analytics/config/{service}/{file}', json = { 'config' : content })

