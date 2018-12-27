SSMEnv
---
| master  | develop | PyPI | Python | Licence |
| --- | --- | --- | --- | --- |
| [![Build Status](https://travis-ci.org/whisller/ssmenv.svg?branch=master)](https://travis-ci.org/whisller/ssmenv)  | [![Build Status](https://travis-ci.org/whisller/ssmenv.svg?branch=develop)](https://travis-ci.org/whisller/ssmenv)  | [![PyPI](https://img.shields.io/pypi/v/ssmenv.svg)](https://pypi.org/project/ssmenv/) | ![](https://img.shields.io/pypi/pyversions/ssmenv.svg) | ![](https://img.shields.io/pypi/l/ssmenv.svg) |

---
SSMEnv allows you to read parameters from [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html) and operate on results as on dictionary.

## Installation
Only requirement is to have `boto3` installed.
```bash
pip install ssmenv
```

## Reading parameters
Reading parameters is as simple as initialising class object.
```python
from ssmenv import SSMEnv

ssmenv = SSMEnv("/service/my-service")
```

Done!

Now `ssmenv` can be accesses as python `dict` type.

## Interacting with `SSMEnv` instance
As you know by now, instance of `SSMEnv` can be accessed as any `dict` in python which means you can do things like:
```python
from ssmenv import SSMEnv

ssmenv = SSMEnv("/service/my-service")

# 1. Access value directly
debug = ssmenv["SERVICE_MY_SERVICE_DEBUG"]

# 2. Get list of all loaded parameter's names
list(ssmenv.keys())

# 3. Get list of all loaded parameter's values
list(ssmenv.values())

# and so on...
```

## Fetching multiple namespaces at once
In real world most often you will access parameters from different namespaces, you can easily do that with `SSMEnv`
by passing `tuple`
```python
from ssmenv import SSMEnv

ssmenv = SSMEnv(("/service/my-service", "/resource/mysql"))
```
Now `ssmenv` will have all parameters from both `/service/my-service` and `/resource/mysql`.

## AWS Lambda decorator
If you use AWS lambda, you might find handy `ssmenv_lambda` decorator. It behaves same as if you would initialise `SSMEnv` by hand, but additionally it injects instance of `SSMEnv` into `context.params` attribute.

```python
from ssmenv import ssmenv_lambda

@ssmenv_lambda("/service/my-service")
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

ssmenv = SSMEnv("/service/my-service", prefixes=("/service/my-service",))
ssmenv["DEBUG"]
```

## Returning dict in case there is no AWS context
You might want to run your application without AWS, e.g. through docker on your local machine and mock parameters.
For that you can use `no_aws_default` attribute.

```python
import os
from ssmenv import SSMEnv

os.environ["SERVICE_MY_SERVICE_DEBUG"] = "1" # that might be set in docker-compose

ssmenv = SSMEnv("/service/my-service", no_aws_default=os.environ)
```

## Passing your own boto3 client
You can pass your own boto3 client as well.
```python
import boto3
from ssmenv import SSMEnv

ssm_client = boto3.client("ssm")
ssmenv = SSMEnv("/service/my-service", ssm_client=ssm_client)
```
