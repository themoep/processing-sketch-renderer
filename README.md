# processing-sketch-renderer

Tool to automatically render all sketches to gifs.

Currently just fragile shell scripts that work on xubuntu 17.04. The goal is to have something more robust, with better error handling and cross-plattform.

Since this runs unsupervised, it will not record mouse- and keyboard-interactions and fail if required hardware is not attached.

## requirements

- Xubuntu 17.04
- `xvfb`: runs a program in a virtual X frame-buffer
- `timeout`: terminates a program after a given amount of time if it is still running
- `byzanz`: records the screen to a file

install dependencies with

```
sudo apt-get install xvfb byzanz
```

## usage

1) adjust the variables in record-sketch.sh
2) run virtual-record-sketch.sh
