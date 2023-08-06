import os
from setuptools import setup, find_packages
import sys


setup(
    name='fb-data-cli',
    version='0.0.1',
    description='Football Data CLI',
    author='Alex Munger',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    keywords="football soccer data api cli",
    author_email='munger.alex@gmail.com',
    url='https://github.com/amunger3/fb-cli',
    packages=find_packages(),
    include_package_data = True,
    install_requires=[
        "click==7.1.2",
        "requests==2.25.1"
    ] + (["colorama==0.4.4"] if "win" in sys.platform else []),
    entry_points={
        'console_scripts': [
            'fb = fb.main:main'
        ],
    }
)