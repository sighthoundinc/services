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
7. Modify the `sio.json` file corresponding your sio selected configuration. (Setting the right URL, pipeline parameters...)


#### Pipeline parameters

Some useful pipeline parameters:

```
fpsLimit: Limits the inference fps to a number
recordTo: Path for video storage. Should be: /data/sighthound/media/output/video/${sourceId}/
imageSaveDir: Path for image storage. Should be: /data/sighthound/media/output/image/${sourceId}/
```

For more advanced options visit [VehicleAnalytics Documentation](https://dev.sighthound.com/sio/pipelines/VehicleAnalytics/) and [TrafficAnalytics Documentation](https://dev.sighthound.com/sio/pipelines/TrafficAnalytics/)

### Deployment

1. `cd core && docker-compose up -d ; cd -`
2. `cd rabbitmq && docker-compose up -d ; cd -`
3. `cd mcp && docker-compose up -d ; cd -`


At this point you can test your deployment by going to:

http://localhost:18672 and http://localhost:8089
