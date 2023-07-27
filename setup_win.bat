@echo off
setlocal EnableDelayedExpansion

set usage=^

Usage:^
    setup_win.bat [OPTIONS] DIR^

Args:^
    DIR     The absolute path to a directory used for docker volume.^
            This directory is analogous to a shared folder.^
            Refer to the user guide for more info on this directory.^
Options:^
    -h      Display usage info.^


set finish =^

Done! Docker container scan_cont started. Run this command to start main.py:^
    docker exec -it scanext_cont python3 main.py^

Use this command to stop the container:^
    docker container stop scan_cont^


if "%1"=="-h" (
    echo !usage!
    exit /b 0
)
if not exist "%1" (
    echo %1 not found!
    exit /b 1
)


(docker build -t scanext --build-arg UID=1000 --build-arg GID=1000 . && ^
docker run -dit --name scanext_cont -v "%1":/scanext/SHARED scanext) && (
    echo !finish!
)
