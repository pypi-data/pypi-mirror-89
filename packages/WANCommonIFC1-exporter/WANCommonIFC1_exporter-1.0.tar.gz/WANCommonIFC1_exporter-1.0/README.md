# WANCommonIFC1_exporter

Export network data from UPNP devices supporting WANCommonIFC1 to Prometheus

## Installation

Require python 3.8+

Installation via pip:
```
pip install WANCommonIFC1_exporter
```

Installation via this repo:
```
git clone https://github.com/pboardman/WANCommonIFC1_exporter
python setup.py install
```

## Usage

Launch it like this:
```
WANCommonIFC1_exporter IP_OF_UPNP_DEVICE PORT_UPNP_IS_RUNNING_ON
```
WANCommonIFC1_exporter will then expose metrics on port **8125** on `/` and `/metrics`

## Metrics

| Metric Name | Description | Data Type
|----------|-------------|------
|bytes_received_total|Number of bytes received since WANCommonIFC1_exporter was started|Counter
|bytes_sent_total|Number of bytes sent since WANCommonIFC1_exporter was started|Counter