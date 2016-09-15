[![Build Status](https://travis-ci.org/wdtinc/uwsgi-cloudwatch.svg?branch=master)](https://travis-ci.org/wdtinc/uwsgi-cloudwatch)

uwsgi-cloudwatch
================
Store uWSGI stats as CloudWatch metrics.

**This is in early development. There will be bugs.**

Requirements
------------
- Your instance or resource running uwsgi-cloudwatch MUST be [assigned an IAM role](http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/auth-and-access-control-cw.html) that allows you to put CloudWatch metrics into your designated namespace.
- uWSGI Stats Server must run on a network socket over HTTP. Support for unix file sockets is not currently supported, but could be added in the future.

Install
-------
```bash
pip install uwsgi-cloudwatch
```

Run
---
First, run uWSGI as you would normally, but add the `--stats` flag with a target port along with the `--stats-http` flag to enable serving your stats over HTTP.

```bash
uwsgi --http :9090 --wsgi-file foobar.py --stats :9091 --stats-http
```

Then, point `uwsgi-cloudwatch` to your stats server and specify a CloudWatch namespace:

```bash
uwsgi-cloudwatch http://localhost:9091 --namespace "Foo/Bar/Baz"
```

By default, uwsgi-cloudwatch will report metrics every minute. If you wanted to report every 5 minutes:

```bash
uwsgi-cloudwatch http://localhost:9091 --namespace "Foo/Bar/Baz" --frequency 300
```

Metrics
-------
uWSGI Stats Server [exposes stats](http://uwsgi-docs.readthedocs.io/en/latest/StatsServer.html#the-uwsgi-stats-server) that are made available as metrics:

### Workers
- WorkerCount
- WorkerIdleCount
- WorkerBusyCount
- WorkerAcceptingCount
- WorkerRequestsCount
- WorkerDeltaRequestsCount
- WorkerAverageResponseTimeMilliseconds
- WorkerExceptionsCount
- WorkerHarakiriCount
- WorkerSignalsCount
- WorkerRssBytes
- WorkerVszBytes
- WorkerRunningTimeMilliseconds
- WorkerCoreCount
- WorkerCoreInRequestCount
- WorkerCoreStaticRequestsCount
- WorkerCoreRoutedRequestsCount
- WorkerCoreWriteErrorsCount
- WorkerCoreReadErrorsCount

### Locks
- LocksUser0Count
- LocksFilemonCount
- LocksTimerCount
- LocksRbTimerCount
- LocksCronCount
- LocksRpcCount
- LocksSnmpCount

### Sockets
- SocketCount
- SocketQueueCount
- SocketMaxQueueCount
- SocketSharedCount
- SocketCanOffloadCount

### Misc.
- SignalQueueCount
- LoadCount

All metric names are prefixed with "uWSGI" by default, but you can also assign your own prefix:

```bash
uwsgi-cloudwatch http://localhost:9091 --namespace "Foo/Bar/Baz" --metric-prefix "QuxCorge"
```
