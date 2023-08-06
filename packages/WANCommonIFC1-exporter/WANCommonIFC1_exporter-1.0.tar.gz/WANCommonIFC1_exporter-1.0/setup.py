# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='WANCommonIFC1_exporter',
    version='1.0',
    description='Export network data from UPNP devices supporting WANCommonIFC1 to Prometheus',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pboardman/WANCommonIFC1_exporter',
    author='Pascal Boardman',
    author_email='pascalboardman@gmail.com',
    license='MIT',
    scripts=['bin/WANCommonIFC1_exporter'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='prometheus exporter UPNP WANCommonIFC1 grafana',
    install_requires=['upnpclient', 'prometheus_client'],
)
