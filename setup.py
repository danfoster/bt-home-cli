import os
from setuptools import setup, find_packages


setup(
    name = "bt-home-api",
    version = "0.0.1",
    author = "Dan Foster",
    author_email = "dan@zem.org.uk",
    description = "BT Home* API",
    license = "MIT",
    keywords = "bt api",
    packages = find_packages(),
    long_description="""BT Home* API""",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    install_requires=[
        "click",
    ],
    entry_points = {
        'console_scripts': [
            'bthome=bthomeapi.cli:main'
        ],
        
    }
)
