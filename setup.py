from pip.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='uwsgi-cloudwatch',
    version='0.0.1',
    packages=find_packages(exclude=('etc')),
    include_package_data=True,
    author='Justin Stewart',
    author_email='jstewart@wdtinc.com',
    description='uwsgi-cloudwatch',
    url='https://github.com/wdtinc/uwsgi-cloudwatch',
    install_requires=reqs,
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    entry_points={
        'console_scripts': [
            'uwsgi-cloudwatch = uwsgi_cloudwatch.main:cli'
        ]
    }
)
