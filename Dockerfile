FROM python:3.12

# create new user name app
RUN useradd -ms /bin/bash app

# set the working directory
WORKDIR /home/app

# copy the requirements file
COPY requirements.txt requirements.txt

# install the requirements
RUN pip install -r requirements.txt

WORKDIR /home/app/source