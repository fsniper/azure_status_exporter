FROM python:3-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY azure_status_exporter.py /usr/src/app

EXPOSE 9999

ENTRYPOINT [ "python", "-u", "./azure_status_exporter.py" ]
