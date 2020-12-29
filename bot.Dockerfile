FROM python:3.9.0-buster
WORKDIR /www
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
ENV PYTHONDONTWRITEBYTECODE 1
EXPOSE 5000
ADD .env .
RUN export $(cat .env | xargs)
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# fr_FR.UTF-8 UTF-8/fr_FR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG fr_FR.UTF-8
ENV LC_ALL fr_FR.UTF-8
CMD python3 bot.py
