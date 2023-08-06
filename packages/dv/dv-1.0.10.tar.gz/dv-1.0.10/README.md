<center>![logo](img/head.png)</center>

# DV-Python

*A library that to connect a python script to outputs from the dynamic vision system DV. This is used in conjunction with the Dynamic Vision Sensor (DVS).*

## Features
[DV (Dynamic Vision System)](https://inivation.gitlab.io/dv/dv-docs/) is a platform to develop high-performance, embedded, deployable C++ applications. However, for rapid prototyping and experimenting, many developers prefer to use python.

**DV-Python** DV python is a library that helps you:

* Get live (raw or processed) data from DV into your python application
* Open files you recorded with DV
* Open older files, recorded with now obsolete software (such as jaer)

## Installation
Make sure you are using a recent python 3 version.
The easiest way to install the library is via pip

```bash
pip3 install dv
```

## Get live event data from the camera

DV communicates with the outside world by means of your computers network stack. To make DV export your required data to the network, follow these steps:

#### Configure DV

1. Start DV
2. Go to *Structure* tab
3. Add a `Dv net output tcp server` by clicking on *Add module*

   ![add module screenshot](img/1.png)

4. Name the module as you wish, for example "event_server"
5. Connect `events` output of your camera with the input of the added module

   ![connection screenshot](img/2.png)

6. The module assumes port `7777` by default. If you are happy with that, you can start the module by pressing the play button. If not, click on the plus button next to the modules name in the configuration list in the right sidebar.
7. To change the port, change the setting in the window that popped up

   ![connection screenshot](img/3.png)

8. In that same window, you can change the 'Max Data Backlog' configuration if needed. By default the TCP server module discards data if the Python client cannot keep up. To avoid this, change the value to '-1'.

#### Connect in your python program

A sample program that loops over the events in the input:

```python
from dv import NetworkEventInput

with NetworkEventInput(address='127.0.0.1', port=7777) as i:
    for event in i:
        print(event.timestamp)
```

An event has properties `x`, `y`, `polarity` and timestamp. The timestamp is in microseconds.

## Get live frame data from the camera

Configure DV as in the event case, but connect the camera frame output to the network module input.

#### Connect in your python program

A sample program that loops over the events in the input:

```python
from dv import NetworkFrameInput
import cv2

with NetworkFrameInput(address='127.0.0.1', port=7777) as i:
    for frame in i:
        print(frame)
        cv2.imshow('out', frame.image)
        cv2.waitKey(1)
```

`frame.image` is a *numpy* matrix that can directly be used to perform openCV operations on it.

### Get other data from the camera
As with the event and frame case, one can also obtain IMU and Trigger data from the camera the same way.


## Open a recording made with DV

Every `.aedat4` file created with DV, contains all the streams of data that were connected to while recording. To get the names of all the streams in the file, use `.names`.

```python
from dv import AedatFile

with AedatFile(<Path to aedat file>) as f:
    # list all the names of streams in the file
    print(f.names)

    # Access dimensions of the event stream
    height, width = f['events'].size

    # loop through the "events" stream
    for e in f['events']:
        print(e.timestamp)

    # loop through the "frames" stream
    for frame in f['frames']:
        print(frame.timestamp)
        cv2.imshow('out', frame.image)
        cv2.waitKey(1)
```

### Direct numpy access

Iterating over all events in a python loop is pretty slow. In order to improve performance, *dv-python* offers direct *numpy* access.
With numpy access the underlying data is directly interpreted by numpy and no data has to be copied.
Events are accessed in packets of varying size.

```python
from dv import AedatFile

with AedatFile(<Path to aedat file>) as f:
    # list all the names of streams in the file
    print(f.names)

    # loop through the "events" stream as numpy packets
    for e in f['events'].numpy():
        print(e.shape)
```

**Example** Extract all events from a file into a numpy array

```python
from dv import AedatFile
import numpy as np

with AedatFile(<Path to aedat file>) as f:
    # events will be a named numpy array
    events = np.hstack([packet for packet in f['events'].numpy()])

    # Access information of all events by type
    timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']
    # Access individual events information
    event_123_x = events[123]['x']
    # Slice events
    first_100_events = events[:100]
```


## Load an old, legacy .aedat file
dv-python supports loading some (sane) *aedat 2* and *aedat 3* files. However, it only supports reading the event data from these files. Other data, like frames etc. is not supported.

```python
from dv import LegacyAedatFile

with LegacyAedatFile('myFile.aedat') as f:
	for event in f:
		print(event.timestamp)
```

**Note** Reading of the file is done completely in python and is therefore pretty slow. This is not recommended for more than quick tests.

## Experimental: Interfacing with config tree

The configuration of DV at runtime is stored in a tree structure accesible over the network. The config tree is what is altered making changes in the dv gui. *dv-python* offers experimental wrappers for the `dv-control` command line utility to read and change config options at runtime from python.

#### Example

```python
from dv import Control

ctrl = Control(address='127.0.0.1', port=4040)
print(ctrl.get('/mainloop/output_file/', 'file', 'string'))
ctrl.put('/mainloop/accumulator/', 'running', 'bool', True)
```

#### Available functions

* `put(path, attribute, type, value)`
* `get(path, attribute, type)`
* `add_module(name, library)`
* `remove_module(name)`
* `node_exists(path)`
* `attribute_exists(path, attribute, type)`
* `get_children(path)`


## Contribution

This is very new software which can and will contain bugs. Please report any bugs you find, and we'll quickly address them.
