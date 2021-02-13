"""PySnoo setup script."""
from setuptools import setup

_VERSION = '0.1.0'


def readme():
    """Pipe README.rst"""
    with open('README.md') as desc:
        return desc.read()


setup(
    name='pysnoo',
    packages=['pysnoo'],
    version=_VERSION,
    description='A Python library and CLI to communicate with'
                ' the Snoo Smart Baby Sleeper and Bassinet from Happiest Baby',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Martin Riedel',
    author_email='web@riedel-it.de',
    url='https://github.com/rado0x54/pysnoo',
    license='MIT',
    python_requires='>=3.7, <4',
    include_package_data=True,
    install_requires=['oauthlib', 'aiohttp', 'pubnub>=5.0.0'],
    test_suite='tests',
    scripts=['scripts/snoo'],
    keywords=[
        'baby',
        'snoo',
        'home automation',
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
