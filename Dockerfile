FROM ubuntu:jammy
WORKDIR /tmp
RUN apt-get update && apt-get upgrade -y
COPY requirements-apt.txt .
COPY requirements-pip.txt .
RUN xargs -a requirements-apt.txt apt-get -y install
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y -f ./google-chrome*.deb
RUN apt-get install -y python3-pip
RUN pip install -r requirements-pip.txt
WORKDIR /scanext
COPY . /scanext/
CMD [ "python3", "main.py" ]