# FROM prefecthq/prefect:latest-python3.8


# Choose this base image instead to minimize vulnerability risk and image size
FROM python:3.8-slim-buster

WORKDIR /app
ENV PYTHONPATH $PYTHONPATH:/app/

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "prefect", "agent", "kubernetes", "start" ]
