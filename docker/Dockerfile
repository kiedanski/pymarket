FROM python:3

RUN apt-get update && apt-get install -y vim pandoc

WORKDIR /usr/src/app

RUN git clone https://github.com/gus0k/pymarket.git
# RUN cd pymarket
# RUN make docs
WORKDIR /usr/src/app/pymarket
RUN ls
RUN pip install -r requirements_dev.txt
#CMD ['/bin/sh']