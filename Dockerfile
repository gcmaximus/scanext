FROM ubuntu:jammy
WORKDIR /tmp
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libxss1 libappindicator1 libindicator7 xdotool wget xvfb
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y -f ./google-chrome*.deb
RUN apt-get install -y python3-pip
# RUN apt-get install -y tzdata
# ENV TZ=Asia/Singapore
WORKDIR /scanext
COPY . /scanext/
RUN pip install -r requirements.txt
CMD [ "python3", "main.py" ]