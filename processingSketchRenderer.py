#!/usr/bin/env python3

# import argparse
import os
import signal
import threading
import subprocess

from xvfbwrapper import Xvfb


PROCESSING = "~/Applications/processing/processing-3.3.6/processing-java"
sketches_folder = "~/Dropbox/ubi/progfiles/processing3/"
OUTPUT_LOCATION = "~/Desktop/"

PROCESSING = os.path.expanduser(PROCESSING)
sketches_folder = os.path.expanduser(sketches_folder)
OUTPUT_LOCATION = os.path.expanduser(OUTPUT_LOCATION)


def parse_arguments():
    pass


def isProcessingSketch(basename, sketchname):
    sketchpath = os.path.join(basename, sketchname)
    mainfile = os.path.join(sketchpath, sketchname+".pde")
    return os.path.isfile(mainfile)


def getSketches(sketches_folder):
    sketches = []
    # gather sketches
    for dirname in os.listdir(sketches_folder):
        # skip known folders
        if dirname in ["tools", "templates", "examples", "libraries", "modes"]:
            continue
        # skip single files
        sketchpath = os.path.join(sketches_folder, dirname)
        if not os.path.isdir(sketchpath):
            continue
        # check if it is a processing sketch
        if not isProcessingSketch(sketches_folder, dirname):
            print("WARNING: "+dirname+" is not a processing sketch")
            continue
        sketches.append(sketchpath)
    return sketches


class SketchRunner(threading.Thread):
    def __init__(self, sketch, timeout=5, mode="present"):
        self.sketch = sketch
        self.command = PROCESSING+" --sketch="+sketch+" --"
        if mode in ["run", "present"]:
            self.command += mode
        else:
            raise ValueError("Mode must be must be run or present.")
        self.timeout = timeout
        threading.Thread.__init__(self)

    def run(self):
        print("Running "+self.sketch)
        with subprocess.Popen(self.command,
                              shell=True,
                              stdout=subprocess.PIPE,
                              preexec_fn=os.setsid) as process:
            try:
                output = process.communicate(timeout=self.timeout)[0]
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGINT)
                output = process.communicate()[0]
        print(output)


def virtualRun(skRunner):
    vdisplay = Xvfb()
    vdisplay.start()
    skRunner.start()
    skRunner.join()
    vdisplay.stop()


def virtualRunRecord(skRunner):
    outfile = os.path.join(OUTPUT_LOCATION, "out.gif")
    vdisplay = Xvfb(width=1000, height=1000)
    vdisplay.start()
    skRunner.start()
    subprocess.run(["byzanz-record", "-d", "2", outfile])
    skRunner.join()
    vdisplay.stop()


def runProcessingSketch(sketch, timeout=None):
    print("running "+sketch)

    command = PROCESSING+" --sketch="+sketch+" --run"

    with subprocess.Popen(command,
                          shell=True,
                          stdout=subprocess.PIPE,
                          preexec_fn=os.setsid) as process:
        try:
            output = process.communicate(timeout=5)[0]
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGINT)
            output = process.communicate()[0]
    print(output)


def main():
    """
    1) parse arguments
        1) location of processing-java
        2) location of sketches
        3) location of output
    2) for each folder in sketches
        1) check if it is a sketch, if not continue
        2) start process to run it
        3) start process to record it
        4) if it generated errors, replace gif with error msg

    todo:
    * logging
    * argparse
    * error handling

    ideas:
    * generate a html gallery that enables browsing
    * try to guess the correct resolution for the sketch
    * save & show outputs (stdout and stderr)
    * general / sketch specific settings
            * resolution
            * length
            * format
            * central save location or in sketch folder?

    """
    sketches = getSketches(sketches_folder)

    for sketch in sketches:
        skRunner = SketchRunner(sketch)
        virtualRunRecord(skRunner)

        # runProcessingSketch(sketch, timeout=5)
        break


if __name__ == "__main__":
    print("hello")
    main()
