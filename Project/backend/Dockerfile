FROM python:3.6.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /backend/