# Overview

The scripts in this directory capture video clips corresponding to events segments detected by SIO and processed by MCP.

Clips are captured based on requests to the MCP component based on time regions of interest
corresponding to SIO event segments, where event segments correspond to sequences of video where SIO events are detected.

For now, hack on the MCPEvents.py file to configure/control captures and definition of event sequences. See the comments in `MCPEvents.py` and detail below for tuning parameters.

These scripts all assume they are running on a host with routable IP access to the device/system running MCP.
If MCP is running on a camera/node it's currently assumed the scripts are hosted from an x86 host on the same network.

## Setup

Install python requirements with:
```
pip3 install -r requirements.txt
```

Install these dependencies on Ubuntu platforms
```
sudo apt-get install -y ffmpeg  libx264-dev
```

## Overview

The scripts are used in two phases:
1) Event Capture which records videos and JSON dumps based on interesting regions of
time and associated video.
2) Event Annotation which takes the video and JSON dumps from the previous steps and
overlays bounding boxes, creates annotated video segments to visualize the data
output from the pipeline.

### Event Capture

The command

```
python3 MCPEvents.py 10.1.10.154
```

Will capture events using the instance at 10.1.10.154 and write videos associated with events to
a `video_captures` subdirectory and a json file containing all events captured during the video
to a `video_captures\json` subdirectory.  The video capture format will use .m3u8
which unfortunately [can't be played using VLC](https://superuser.com/questions/1379361/vlc-and-m3u8-file)
but can be played with MPlayer or recent Windows 10 or later version of Windows Media Player.

#### Using Event Generator Output

The command
```
python3 MCPEvents.py --use_events 10.1.10.154
```
Captures events using the Event Analytics module configured on the device with `sensorsConfigFile` SIO
setting referencing a sensor configuration defining events to capture.

#### Filtering based on ROI

The command
```
python3 MCPEvents.py --sensors_json sensors.json 10.1.10.154
```
Will postprocess filter all captures based on regions defined in sensors.json, where the
sensors.json file can be built and exported at http://public-sh-sensor-config-dev.s3-website-us-east-1.amazonaws.com/
using an image captured from an export of one of the images of the videos captured in the step above.

Objects are considered to be in the region of interest if the bottom right corner
of the bounding box is in the region.  This is not (yet) configurable but can be customized
in the ROIFilter class.

### Event Annotation

The command:
```
python3 MCPEventAnnotator.py
```

Will annotate the videos captured in the previous `MCPEvents` capture step, based on the event logs associated with captured videos and the resulting video files.

The command:
```
python3 MCPEventAnnotator.py --sensors_json sensors.json
```

Will include an overlay of the sensors in sensors.json on the annotated videos when
annotating.  This assumes events were captured using the `--use_events` option and a configured Event Analytics
module running in the pipeline.  See the "Postprocessing sensors" section below to run without event analytics

#### Postprocessing Sensors
The command:
```
python3 MCPEventAnnotator.py --postprocess_sensors --sensors_json sensors.json
```

Will include an overlay of the sensors in sensors.json on the annotated videos when
annotating.  Use the `--postprocess_sensors` option when the original MCPEvents capture did not
come from an SIO pipeline with the Event Analytics module enabled (you did not have `sensorsConfigFile` setup
on the pipeline when MCPEvents captured the output data and did not capture events using the --use_events option.)

### Combined event capture and annotation

The command
```
python3 MCPEvents.py --use_events --annotate --sensors_json sensors.json 10.1.10.154
```
will both capture events from 10.1.10.154 and annotate those events using the `sensors.json`
file to draw detailed sensor event information.  The `annotated` subdirectory will contain
annotated videos with names matching the non-annotated .m3u file generated in the base
capture directory.

## Docker Support

The scripts in the [docker](docker) directory support building and running the examples in a docker container.

### Setup
Ensure you have docker installed on your host.

### Building
Run `./docker/build.sh` to build a container which supports running MCPEvents applications.

### Running
Run the commands as directed above, replacing the `python3` reference with `./docker/run.sh`.

For example:
```
./docker/run.sh MCPEvents.py --sensors_json ${sensors_json} --capture_dir ${capture_dir} ${device_ip}
```
All paths specified must be absolute paths for the volume mapping to work within the docker container.
Wrap with $(realpath) as necessary.
When files in capture_dir use symlinks, the symlink must point to the same capture_dir or one directory above.

The MCPEvents container will restart automatically if an error occurs.

Container names will be set to match the application and device IP address.  Use `docker ps` to list
containers, and `docker stop <container_name>` to stop a container.

## Limitations and Future Work

1) The tool only supports region of interest sensors.  Line sensors are not supported.
2) Most tuning parameters are hard coded and not accepted as arguments.