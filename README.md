[![Build Status](https://travis-ci.org/wdtinc/uwsgi-cloudwatch.svg?branch=master)](https://travis-ci.org/wdtinc/uwsgi-cloudwatch)

uwsgi-cloudwatch
================
Store your uWSGI Stats as CloudWatch metrics.

(THIS IS CURRENTLY A WIP AND IS NOT YET FUNCTIONAL)

Prerequisites
-------------
- Python 2.7
- Your EC2 instance MUST be [assigned an IAM role](http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/auth-and-access-control-cw.html) that allows the instance to put CloudWatch metrics into your designated namespace. Supporting other access control methods is a future goal.
- Run uWSGI Stats Server on a network socket. Support for unix sockets is not currently supported, but could be added in the future.

Install
-------
```bash
pip install uwsgi-cloudwatch
```

Run
---
First, run uWSGI as you would normally, but add the `--stats` flag with a target socket along with the `--stats-http` flag to enable serving your stats over HTTP.

```bash
uwsgi --http :9090 --wsgi-file gevent_example.py --stats :9091 --stats-http
```

Then, point `uwsgi-cloudwatch` to your stats server and specify a CloudWatch namespace to use:

```bash
uwsgi-cloudwatch :9091 --namespace "My/Apps/Namespace"
```
