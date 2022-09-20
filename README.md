# Sighthound docker-compose service

**This project will cease to exist once we release Sighthound artifacts solution**

## Quick start

### Configuration

First create the data dirs
1. `mkdir -p /data/sighthound`
2. `mkdir -p /data/sighthound/media`
3. `mkdir -p /data/sighthound/services`
4. `mkdir -p /data/sighthound/license`
5. Install SIO license in `/data/sighthound/license/sighthound-license.json`
6. Uncompress services tarball into `/data/sighthound/services`

### Deployment

1. `cd core && docker-compose up -d ; cd -`
2. `cd rabbitmq && docker-compose up -d ; cd -`
3. `cd mcp && docker-compose up -d ; cd -`


At this point you can test your deployment by going to:

http://localhost:18672 and http://localhost:8089
