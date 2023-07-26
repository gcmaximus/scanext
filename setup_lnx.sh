#! /bin/sh

if docker build -t scanext --build-arg UID=$(id -u) --build-arg GID=$(id -u) . && \
    docker run -dit --name scanext_cont -v $(pwd)/SHARED:/scanext/SHARED scanext; then

    echo  
    echo "Done! Docker container scan_cont started. Run this command to start main.py:"
    echo "    docker exec -it scanext_cont python3 main.py"
    echo 
    echo "Use this command to stop the container:"
    echo "    docker container stop scan_cont"
fi
