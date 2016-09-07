# blimp

[![Build Status](https://travis-ci.org/lchi/blimp.svg?branch=master)](https://travis-ci.org/lchi/blimp)

A lightweight wrapper around `boto` that helps you get to the cloud.

## Installation

Development mode only for now until this gets distributed via pypi.

`python setup.py develop`

You'll also need to follow the [boto credentials setup instructions](http://boto3.readthedocs.io/en/latest/guide/configuration.html) and have appropriate permissions for the actions you'd like to perform.

## Running tests

Check out the [Travis configuration](.travis.yml) for how to run tests.

```bash
pip install -r requirements.txt
nosetests
```

### flake8 setup

This project uses flake8 to perform some static analysis checks. To install you can do the following:

```
pip install flake8
flake8 blimp
```

Additionally, there is a [git hook](git-hooks/pre-commit) that you can [install](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) to run `flake8` prior to committing.
