import subprocess
from setuptools import setup, find_packages


def get_long_description():
    cmd = 'pandoc -f markdown_github -t rst README.md --no-wrap'
    try:
        return subprocess.check_output(cmd, shell=True, universal_newlines=True)
    except:
        return ""


VERSION = '0.1.0'


setup(
    name='flunk',
    version=VERSION,
    author='Steve McMaster',
    author_email='mcmaster@hurricanelabs.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    # url='http://hurricanelabs.github.io/flunk/',
    description='Flunk - A Splunk Fact Collector',
    long_description=get_long_description(),
    install_requires=[
        'libweb==1.0',
        'pyyaml',
    ],
    dependency_links=[
        'https://github.com/HurricaneLabs/python-libweb/archive/master.zip#egg=libweb-1.0'
    ],
    entry_points={
        'console_scripts': [
            'flunk = flunk.cli:main',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 5 - Production/Stable',
    ],
    bugtrack_url='https://github.com/HurricaneLabs/flunk/issues',
)
