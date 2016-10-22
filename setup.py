from setuptools import setup

current_version = '0.2'

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
        'pyserial'
    ],
    setup_requires=[
        'unittest2',
        'pyserial'
    ],

)
