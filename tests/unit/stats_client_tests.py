from unittest import TestCase
from uwsgi_cloudwatch.stats import StatsClient


class StatClientTest(TestCase):

    def test_get(self):
        client = StatsClient('http://my.stats.server:9091')

