#! /bin/sh

usage="
Usage:
    ./setup_lnx.sh [OPTIONS] DIR

Args:
    DIR     The absolute path to a directory used for docker volume.
            This directory is analogous to a shared folder.
            Refer to the user guide for more info on this directory.
Options:
    -h      Display usage info.
"

finish="
Done! Docker container scan_cont started. Run this command to start main.py:
    docker exec -it scanext_cont python3 main.py

Use this command to stop the container:
    docker container stop scan_cont
"

if test "$1" = "-h" || test $# -eq 0
then
    echo "$usage"
    exit 0
elif ! test -d $1
then
    echo "Directory not found: $1"
    exit 1
else
    if docker build -t scanext --build-arg UID=$(id -u) --build-arg GID=$(id -u) . && \
        docker run -dit --name scanext_cont -v $(cd $1; pwd):/scanext/SHARED scanext
    then
        echo "$finish"
        exit 0
    fi
fi
