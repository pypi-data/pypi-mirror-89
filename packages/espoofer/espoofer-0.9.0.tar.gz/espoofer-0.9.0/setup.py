#!/usr/bin/env python

"""
Copyright (c) 2006-2020 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from setuptools import setup, find_packages

setup(
    name='espoofer',
    version='0.9.0',
    description='An email spoofing testing tool that aims to bypass SPF/DKIM/DMARC and forge DKIM signatures',
    long_description=open('espoofer/README.md').read(),
    long_description_content_type='text/markdown',
    author='Jianjun Chen',
    author_email= 'whucjj@hotmail.com',
    url='http://github.com/chenjj/espoofer',
    project_urls={  
        'Bug Reports': 'https://github.com/chenjj/espoofer/issues',
        'Source': 'https://github.com/chenjj/espoofer/',
    },
    license='MIT',
    packages=find_packages(),
    install_requires=['colorama', 'simplejson', 'argparse', 'dnspython'],
    include_package_data=True,
    zip_safe=False,
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: Security',
    ],
    python_requires='>=3.5, <4',
    entry_points={
        'console_scripts': [
            'espoofer = espoofer.espoofer:main',
        ],
    },
)
