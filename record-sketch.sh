#!/bin/bash

PROCESSING=~/applications/processing3/processing-java
SKETCHES=~/Dropbox/ubi/progfiles/processing3 # no trailing slash!
OUTLOCATION=~/Desktop # no trailing slash!

TMPSTDOUT=/tmp/gifgen_processing_stdout
TMPSTDERR=/tmp/gifgen_processing_stderr

function recordSketch {
    rm -f ${TMPSTDOUT} # -f to be silent if it wasn't created
    rm -f ${TMPSTDERR}
    
    timeout 8s ${PROCESSING} --sketch=${1} --present > ${TMPSTDOUT} 2> ${TMPSTDERR} &

    sleep 2

    byzanz-record -d 5 ${2}

    if [[ -s ${TMPSTDERR} ]]; then
        echo "sketch generated errors, removing gif.."
        rm ${2}
    else
        if [[ -s ${TMPSTDOUT} ]]; then
            echo "sketch generated output"
        fi
    fi

    rm -f ${TMPSTDOUT} # -f to be silent if it wasn't created
    rm -f ${TMPSTDERR}
}

for SKETCH in ${SKETCHES}/*; do
    BASENAME=`basename $SKETCH`
    if [ ! -f ${SKETCH}/${BASENAME}.pde ]; then
        continue
    fi
    echo "#####  RECORDING: ${BASENAME}"
    recordSketch ${SKETCH} ${OUTLOCATION}/${BASENAME}.gif
done

