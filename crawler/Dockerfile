FROM docker.io/bitnami/kafka:3.3.1-debian-11-r11

USER root
WORKDIR /usr/src
RUN apt-get -y update
RUN apt-get install -y wget
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-pip

RUN apt-get install -y python-dev 
RUN apt-get install -y build-essential
RUN apt install unzip  
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN mkdir chrome
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app ./app
CMD ["python3","app/StreetCrawlerFinal.py"]