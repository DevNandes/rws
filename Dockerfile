FROM python:latest

RUN apt update -y && export DEBIAN_FRONTEND=noninteractive && apt install -y \
  build-essential \
  vim \
  vim-scripts \
  tcsh \
  iputils-ping \
  smbclient \
  && rm -Rf /var/lib/apt/lists/*

# ENTRYPOINT ["/home/renault/rws/docker-entrypoint.sh"]
CMD ["/home/renault/rws/scripts/container/start_app.csh"]
