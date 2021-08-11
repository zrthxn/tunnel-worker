FROM python:3
WORKDIR /usr/src/app
COPY ./requirements.txt .
COPY ./tunnel .
RUN pip install -r requirements.txt
RUN apt install -y openssh
CMD [ "python", "./tunnel.py" ]