from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

import os

version = os.environ.get('PACKAGE_VERSION', '1.0.0')
setup(
    name="django-app-notifications",
    version=version,
    description="A Django Library to send notifications",
    readme="README.md",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.example.com/",
    author="Hashtrust Technologies Private Limited",
    author_email="support@hashtrust.in",
    license="MIT License",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications :: Chat",
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "Django",
        "channels",
        "daphne",
        "channels-redis",
    ],
)
