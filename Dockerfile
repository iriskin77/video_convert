FROM python:3.10-slim
WORKDIR /test_video

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

COPY . .

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

RUN chmod a+x /test_video/start.sh

#ENTRYPOINT ["./start.sh"]
