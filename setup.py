from setuptools import setup

current_version = '0.9'

# convert from github markdown to rst
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name = 'em73xx',
    packages = [ 'em73xx', 'em73xx.test' ],
    version = current_version,
    description = 'python wrapper for the em73xx series of 4G modems present in recent Lenovo Thinkpads',
    author = 'Sean McLemon',
    author_email = 'sean.mclemon@gmail.com',
    url = 'https://github.com/smcl/py-em73xx',
    download_url = 'https://github.com/smcl/py-em73xx/tarball/%s' % (current_version),
    keywords = ['thinkpad', 'em7345', 'em73xx'],
    classifiers = [],
    test_suite='em73xx.test.all',
    install_requires=[
        'unittest2',
        'pyserial',
        'python-dateutil'
    ],
    setup_requires=[
        'unittest2',
        'pyserial',
        'python-dateutil'
    ],

)
