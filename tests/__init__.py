import json
import os


FIXTURE_DIR = "%s/%s" % (os.path.dirname(os.path.realpath(__file__)), 'fixtures')
OUTPUT_DIR = "%s/%s" % (os.path.dirname(os.path.realpath(__file__)), 'output')


def load_fixture(f, extension='json'):
    with open('%s/%s.%s' % (FIXTURE_DIR, f, extension), 'r') as f:
        content = f.read()
        if extension == 'json':
            return json.loads(content)
        return content
