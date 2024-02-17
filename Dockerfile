FROM python:3.10-slim
WORKDIR /test_video

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg


COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x /test_video/start.sh

