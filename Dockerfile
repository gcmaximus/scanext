FROM ubuntu:jammy
WORKDIR /tmp
RUN apt-get update && apt-get upgrade -y
COPY requirements-apt.txt .
COPY requirements-pip.txt .
RUN xargs -a requirements-apt.txt apt-get -y install
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb
RUN apt-get install -y -f ./google-chrome*.deb
RUN pip install -r requirements-pip.txt
ARG UID
ARG GID
RUN groupadd -g ${GID} scanuser && useradd --create-home --no-log-init -u ${UID} -g ${GID} scanuser
USER scanuser
WORKDIR /scanext
COPY --chown=scanuser:scanuser . /scanext/

COPY . /scanext/
ARG UID
ARG GID
RUN groupadd -g "${GID}" scanuser \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" scanuser
RUN chown -R scanuser:scanuser /scanext
USER scanuser