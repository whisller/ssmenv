SSMEnv
---
| master  | coverage | PyPI | Python | Licence |
| --- | --- | --- | --- | --- |
| [![Build Status](https://travis-ci.org/whisller/ssmenv.svg?branch=master)](https://travis-ci.org/whisller/ssmenv) | [![Coverage Status](https://coveralls.io/repos/github/whisller/ssmenv/badge.svg?branch=develop)](https://coveralls.io/github/whisller/ssmenv?branch=develop) | [![PyPI](https://img.shields.io/pypi/v/ssmenv.svg)](https://pypi.org/project/ssmenv/) | ![](https://img.shields.io/pypi/pyversions/ssmenv.svg) | ![](https://img.shields.io/pypi/l/ssmenv.svg) |

---
SSMEnv allows you to read parameters from [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html) and operate on results as on dictionary.

## Installation
Only requirement is to have `boto3` installed.
```bash
pip install ssmenv
```

## Reading parameters
Let's assume we have two parameters `token` and `url` under `/service/my-service` namespace.
Reading both parameters is as simple as initialising class object.
```python
from ssmenv import SSMEnv

params = SSMEnv("/service/my-service")
```

Done! Now we can access `/service/my-service/token` and `/service/my-service/url` in `params` variable!

Now `params` can be accesses as python `dict` type.

## Interacting with `SSMEnv` instance
As you know by now, instance of `SSMEnv` can be accessed as any `dict` in python which means you can do things like:
```python
from ssmenv import SSMEnv

params = SSMEnv("/service/my-service")

# 1. Access value directly
token = params["SERVICE_MY_SERVICE_TOKEN"]

# 2. Get list of all loaded parameter's names
list(params.keys())

# 3. Get list of all loaded parameter's values
list(params.values())

# and so on...
```

## Fetching multiple namespaces at once
In real world most often you will access parameters from different namespaces, you can easily do that with `SSMEnv`
by passing `tuple`
```python
from ssmenv import SSMEnv

params = SSMEnv("/service/my-service", "/resource/mysql")
```
Now `params` will have all parameters from both `/service/my-service` and `/resource/mysql`.

## AWS Lambda decorator
If you use AWS lambda, you might find handy `ssmenv` decorator. It behaves same as if you would initialise `SSMEnv` by hand, but additionally it injects instance of `SSMEnv` into `context.params` attribute.

```python
from ssmenv import ssmenv

@ssmenv("/service/my-service")
def handler(event, context):
    return context.params
```

## Populating `os.environ`
You can hide use of `SSMEnv` by using `os.environ` dict.
```python
import os
from ssmenv import SSMEnv

os.environ = {**os.environ, **SSMEnv("/service/my-service")}
```

## Removing common prefixes
Accessing your parameters through whole namespaces can sometimes be not convenient
especially if you have very long names.

Hence why you can use `prefixes` parameter, to make your code cleaner.

 ```python
from ssmenv import SSMEnv

params = SSMEnv("/service/my-service", prefixes=("/service/my-service",))
params["TOKEN"]
```

## Returning dict in case there is no AWS context
You might want to run your application without AWS, e.g. through docker on your local machine and mock parameters.
For that you can use `no_aws_default` attribute.

```python
import os
from ssmenv import SSMEnv

os.environ["SERVICE_MY_SERVICE_TOKEN"] = "mocked-token" # that might be set in docker-compose

params = SSMEnv("/service/my-service", no_aws_default=os.environ)
```

## Passing your own boto3 client
You can pass your own boto3 client as well.
```python
import boto3
from ssmenv import SSMEnv

ssm_client = boto3.client("ssm")
params = SSMEnv("/service/my-service", ssm_client=ssm_client)
```
