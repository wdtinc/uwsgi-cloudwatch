import arrow
import asyncio
import boto3
import click
import logging
import re
import requests
from . import validation

logging.basicConfig(level=logging.INFO)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def run_periodically(func, interval):
    """ Runs a task periodically. """
    _loop = asyncio.get_event_loop()

    def _set():
        _loop.call_later(interval, _run)

    def _run():
        func()
        _set()

    _set()


def put_metrics(metrics, region, namespace, metric_prefix):
    """ Puts metrics in target CloudWatch namespace. """

    timestamp = arrow.get().datetime
    client = boto3.client('cloudwatch', region_name=region)

    # Assemble Metrics
    metric_data = []
    for name, value in metrics.items():

        # Detect Units
        if re.match(".*Bytes", name):
            unit = "Bytes"
        elif re.match(".*Count", name):
            unit = "Count"
        elif re.match(".*Milliseconds", name):
            unit = "Milliseconds"
        else:
            unit = "None"

        if type(value) == list:
            for i in value:
                metric_data.append({
                    'MetricName': metric_prefix + name,
                    'Timestamp': timestamp,
                    'Value': i,
                    'Unit': unit
                })
        else:
            metric_data.append({
                'MetricName': metric_prefix + name,
                'Timestamp': timestamp,
                'Value': value,
                'Unit': unit
            })

    # Put Metrics
    for chunk in chunks(metric_data, 20):
        client.put_metric_data(
            Namespace=namespace,
            MetricData=chunk
        )


def generate_metrics(stats):
    """ Generates metrics from uWSGI stats. """
    m = {}
    m['SignalQueueCount'] = stats['signal_queue']
    m['LoadCount'] = stats['load']

    # Lock Metrics
    locks = {}
    for lock in stats['locks']:
        key = list(lock).pop()
        locks[key] = lock[key]
    m['LocksUser0Count'] = locks['user 0']
    m['LocksSignalCount'] = locks['signal']
    m['LocksFilemonCount'] = locks['filemon']
    m['LocksTimerCount'] = locks['timer']
    m['LocksRbTimerCount'] = locks['rbtimer']
    m['LocksCronCount'] = locks['cron']
    m['LocksRpcCount'] = locks['rpc']
    m['LocksSnmpCount'] = locks['snmp']

    # Socket Metrics
    m['SocketsCount'] = len(stats['sockets'])
    m['SocketsQueueCount'] = []
    m['SocketsMaxQueueCount'] = []
    m['SocketsSharedCount'] = []
    m['SocketsCanOffloadCount'] = []
    for socket in stats['sockets']:
        m['SocketsQueueCount'].append(socket['queue'])
        m['SocketsMaxQueueCount'].append(socket['max_queue'])
        m['SocketsSharedCount'].append(socket['shared'])
        m['SocketsCanOffloadCount'].append(socket['can_offload'])

    # Worker Metrics
    m['WorkersCount'] = len(stats['workers'])
    m['WorkersIdleCount'] = 0
    m['WorkersBusyCount'] = 0
    m['WorkersAcceptingCount'] = 0
    m['WorkersAverageResponseTimeMilliseconds'] = []
    m['WorkersRequestsCount'] = []
    m['WorkersDeltaRequestsCount'] = []
    m['WorkersExceptionsCount'] = []
    m['WorkersHarakiriCount'] = []
    m['WorkersSignalsCount'] = []
    m['WorkersSignalQueueCount'] = []
    m['WorkersRssBytes'] = []
    m['WorkersVszBytes'] = []
    m['WorkersRunningTimeMilliseconds'] = []
    m['WorkersLastSpawnTimestamp'] = []
    m['WorkersRespawnCount'] = []
    for worker in stats['workers']:
        if worker['status'] == 'idle':
            m['WorkersIdleCount'] += 1
        elif worker['status'] == 'busy':
            m['WorkersBusyCount'] += 1
        m['WorkersAcceptingCount'] += worker['accepting']
        m['WorkersRequestsCount'].append(worker['requests'])
        m['WorkersDeltaRequestsCount'].append(worker['delta_requests'])
        m['WorkersExceptionsCount'].append(worker['exceptions'])
        m['WorkersHarakiriCount'].append(worker['harakiri_count'])
        m['WorkersSignalsCount'].append(worker['signals'])
        m['WorkersSignalQueueCount'].append(worker['signal_queue'])
        m['WorkersRssBytes'].append(worker['rss'])
        m['WorkersVszBytes'].append(worker['vsz'])
        m['WorkersAverageResponseTimeMilliseconds'].append(int(worker['avg_rt']/1000))
        m['WorkersRunningTimeMilliseconds'].append(int(worker['running_time']/1000))
        m['WorkersLastSpawnTimestamp'].append(worker['last_spawn'])
        m['WorkersRespawnCount'].append(worker['respawn_count'])

    # Core Metrics
    m['WorkerCoresCount'] = []
    m['WorkerCoresInRequestCount'] = []
    m['WorkerCoresRequestsCount'] = []
    m['WorkerCoresStaticRequestsCount'] = []
    m['WorkerCoresRoutedRequestsCount'] = []
    m['WorkerCoresWriteErrorsCount'] = []
    m['WorkerCoresReadErrorsCount'] = []
    for worker in stats['workers']:
        m['WorkerCoresCount'].append(len(worker['cores']))
        core_in_request_count = 0
        for core in worker['cores']:
            core_in_request_count += core['in_request']
            m['WorkerCoresRequestsCount'].append(core['requests'])
            m['WorkerCoresStaticRequestsCount'].append(core['static_requests'])
            m['WorkerCoresRoutedRequestsCount'].append(core['routed_requests'])
            m['WorkerCoresWriteErrorsCount'].append(core['write_errors'])
            m['WorkerCoresReadErrorsCount'].append(core['read_errors'])
        m['WorkerCoresInRequestCount'].append(core_in_request_count)

    return m


def retrieve_stats(stats_server):
    """ Retrieve latest stats from uWSGI Stats Server. """
    logging.info('Retrieving stats...')
    response = requests.get(stats_server)
    return response.json()


def update_cloudwatch_metrics(stats_server, region, namespace, metric_prefix):
    """ Update a CloudWatch namespace with the latest metrics generated from
        uWSGI Stats Server.
    """
    def f():
        try:
            stats = retrieve_stats(stats_server)
        except Exception as e:
            logging.error("Failed to retrieve uWSGI stats: %s" % e)
        try:
            metrics = generate_metrics(stats)
            put_metrics(metrics, region, namespace, metric_prefix)
        except Exception as e:
            logging.error("Failed to put metrics: %s" % e)

    return f


@click.command()
@click.argument('stats-server')
@click.option('--region', default='us-east-1')
@click.option('--namespace', required=True, callback=validation.namespace)
@click.option('--frequency', default=60, callback=validation.frequency)
@click.option('--metric-prefix', default='uWSGI', callback=validation.prefix)
def cli(stats_server, region, namespace, frequency, metric_prefix):
    run_periodically(update_cloudwatch_metrics(stats_server, region, namespace, metric_prefix), frequency)
    asyncio.get_event_loop().run_forever()
