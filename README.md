# blimp

[![Build Status](https://travis-ci.org/lchi/blimp.svg?branch=master)](https://travis-ci.org/lchi/blimp)

A lightweight wrapper around `boto` that helps you get to the cloud.

## Installation

Development mode only for now until this gets distributed via pypi.

`python setup.py develop`

You'll also need to follow the [boto credentials setup instructions](http://boto3.readthedocs.io/en/latest/guide/configuration.html) and have appropriate permissions for the actions you'd like to perform.

## Running tests

```bash
pip install -r dev-requirements.txt
nosetests
```
