# Overview

The scripts in this directory may be used to manage Sighthound devices (camera/nodes).

## Setup

Install python requirements with:
```
pip3 install -r requirements.txt
```

### UpdateToTag

The command

```
python3 examples/UpdateDevice/UpdateToTag.py --device deviceip --remote remotename --reference remotetag
```

Will perform commands on the device at `deviceip` which:
* Stop all services.
* Fetch the `remotetag` from the git remote configured as `remotename`.
* Restart all services.

