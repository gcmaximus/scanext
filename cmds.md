cd scanext/
docker build -t scanext --build-arg UID=$(id -u) --build-arg GID=$(id -u) .
docker run -dit --name scanext_cont -u $(id -u) -v $(pwd)/SHARED:/scanext/SHARED scanext
docker exec -it scanext_cont python3 main.py