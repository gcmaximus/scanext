@echo off
(docker build -t scanext --build-arg UID=1000 --build-arg GID=1000 . && ^
docker run -dit --name scanext_cont -v %cd%\SHARED:/scanext/SHARED scanext) && (
    echo.
    echo Done! Docker container scan_cont started. Run this command to start main.py:
    echo     docker exec -it scanext_cont python3 main.py
    echo.
    echo Use this command to stop the container:
    echo     docker container stop scan_cont
)
