FROM python:3.11.5 AS base
WORKDIR /app
COPY app.py requirements.txt ./
COPY templates ./templates/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y default-mysql-client
CMD [ "python", "app.py" ]