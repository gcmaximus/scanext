@echo off


set usage= ^

Usage:^

    setup_win.bat [OPTIONS] DIR^

^

Args:^

    DIR     The absolute path to a directory used for docker volume.^

            This directory is analogous to a shared folder.^

            Refer to the user guide for more info on this directory.^

^

Options:^

    -h      Display usage info.^


set finish= ^

Done! Docker container scan_cont started. Run this command to start main.py:^

    docker exec -it scanext_cont python3 main.py^

^

Use this command to stop the container:^

    docker container stop scan_cont^


setlocal EnableDelayedExpansion

if "%~1"=="" (
    echo !usage!
    exit /b 0
)

if "%~1"=="-h" (
    echo !usage!
    exit /b 0
)

if not exist "%1" (
    echo Directory not found: %1
    exit /b 1
)

(docker build -t scanext --build-arg UID=1000 --build-arg GID=1000 . && ^
docker run -dit --name scanext_cont -v %(cd $1; cd)%:/scanext/SHARED scanext) && (
    echo !finish!
)


