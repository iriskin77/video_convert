FROM python:3.10-slim

WORKDIR /test_video

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn


COPY . .

#EXPOSE 8080

RUN chmod a+x /test_video/start.sh

#ENTRYPOINT ["./start.sh"]
