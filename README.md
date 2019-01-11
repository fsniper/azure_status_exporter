# Azure Status Exporter

This application scrapes metrics from Azure Status Page [https://azure.microsoft.com/en-us/status/] and exposes them as prometheus metrics


## Usage

```
# build docker image
docker build .  -t fsniper/azure_exporter
docker run -p 9999:9999 --rm fsniper/azure_exporter

curl http://localhost:9999/
```
