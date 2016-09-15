from unittest import TestCase
from uwsgi_cloudwatch.main import generate_metrics, retrieve_stats
from tests import load_fixture


class AllTests(TestCase):

    def test_generate_metrics(self):

        stats = load_fixture('stats')
        m = generate_metrics(stats)

        self.assertEqual(m['SignalQueueCount'], 0)
        self.assertEqual(m['LoadCount'], 0)

        self.assertEqual(m['LocksUser0Count'], 0)
        self.assertEqual(m['LocksFilemonCount'], 0)
        self.assertEqual(m['LocksTimerCount'], 0)
        self.assertEqual(m['LocksRbTimerCount'], 0)
        self.assertEqual(m['LocksCronCount'], 0)
        self.assertEqual(m['LocksRpcCount'], 0)
        self.assertEqual(m['LocksSnmpCount'], 0)

        self.assertEqual(m['SocketsCount'], 1)

        self.assertEqual(len(m['SocketsQueueCount']), 1)
        self.assertEqual(m['SocketsQueueCount'][0], 0)

        self.assertEqual(len(m['SocketsMaxQueueCount']), 1)
        self.assertEqual(m['SocketsMaxQueueCount'][0], 0)

        self.assertEqual(len(m['SocketsSharedCount']), 1)
        self.assertEqual(m['SocketsSharedCount'][0], 0)

        self.assertEqual(len(m['SocketsCanOffloadCount']), 1)
        self.assertEqual(m['SocketsCanOffloadCount'][0], 0)

        self.assertEqual(m['WorkersCount'], 2)
        self.assertEqual(m['WorkersIdleCount'], 0)
        self.assertEqual(m['WorkersBusyCount'], 2)
        self.assertEqual(m['WorkersAcceptingCount'], 2)

        self.assertEqual(len(m['WorkersRequestsCount']), 2)
        self.assertEqual(m['WorkersRequestsCount'][0], 305)
        self.assertEqual(m['WorkersRequestsCount'][1], 307)

        self.assertEqual(len(m['WorkersDeltaRequestsCount']), 2)
        self.assertEqual(m['WorkersDeltaRequestsCount'][0], 305)
        self.assertEqual(m['WorkersDeltaRequestsCount'][1], 307)

        self.assertEqual(len(m['WorkersAverageResponseTimeMilliseconds']), 2)
        self.assertEqual(m['WorkersAverageResponseTimeMilliseconds'][0], 3017)
        self.assertEqual(m['WorkersAverageResponseTimeMilliseconds'][1], 3017)

        self.assertEqual(len(m['WorkersExceptionsCount']), 2)
        self.assertEqual(m['WorkersExceptionsCount'][0], 0)
        self.assertEqual(m['WorkersExceptionsCount'][1], 0)

        self.assertEqual(len(m['WorkersHarakiriCount']), 2)
        self.assertEqual(m['WorkersHarakiriCount'][0], 0)
        self.assertEqual(m['WorkersHarakiriCount'][1], 0)

        self.assertEqual(len(m['WorkersSignalsCount']), 2)
        self.assertEqual(m['WorkersSignalsCount'][0], 0)
        self.assertEqual(m['WorkersSignalsCount'][1], 0)

        self.assertEqual(len(m['WorkersRssBytes']), 2)
        self.assertEqual(m['WorkersRssBytes'][0], 0)
        self.assertEqual(m['WorkersRssBytes'][1], 0)

        self.assertEqual(len(m['WorkersVszBytes']), 2)
        self.assertEqual(m['WorkersVszBytes'][0], 0)
        self.assertEqual(m['WorkersVszBytes'][1], 0)

        self.assertEqual(len(m['WorkersRunningTimeMilliseconds']), 2)
        self.assertEqual(m['WorkersRunningTimeMilliseconds'][0], 917565)
        self.assertEqual(m['WorkersRunningTimeMilliseconds'][1], 923616)

        self.assertEqual(len(m['WorkerCoresCount']), 2)
        self.assertEqual(m['WorkerCoresCount'][0], 5)
        self.assertEqual(m['WorkerCoresCount'][1], 5)

        self.assertEqual(len(m['WorkerCoresStaticRequestsCount']), 10)
        self.assertEqual(m['WorkerCoresStaticRequestsCount'][0], 0)
        self.assertEqual(m['WorkerCoresStaticRequestsCount'][1], 0)

        self.assertEqual(len(m['WorkerCoresRoutedRequestsCount']), 10)
        self.assertEqual(m['WorkerCoresRoutedRequestsCount'][0], 0)
        self.assertEqual(m['WorkerCoresRoutedRequestsCount'][1], 0)

        self.assertEqual(len(m['WorkerCoresWriteErrorsCount']), 10)
        self.assertEqual(m['WorkerCoresWriteErrorsCount'][0], 0)
        self.assertEqual(m['WorkerCoresWriteErrorsCount'][1], 0)

        self.assertEqual(len(m['WorkerCoresReadErrorsCount']), 10)
        self.assertEqual(m['WorkerCoresReadErrorsCount'][0], 0)
        self.assertEqual(m['WorkerCoresReadErrorsCount'][1], 0)
