SSMEnv
---
| master  | develop | PyPI | Python | Licence |
| --- | --- | --- | --- | --- |
| [![Build Status](https://travis-ci.org/whisller/ssmenv.svg?branch=master)](https://travis-ci.org/whisller/ssmenv)  | [![Build Status](https://travis-ci.org/whisller/ssmenv.svg?branch=develop)](https://travis-ci.org/whisller/ssmenv)  | [![PyPI](https://img.shields.io/pypi/v/ssmenv.svg)](https://pypi.org/project/ssmenv/) | ![](https://img.shields.io/pypi/pyversions/ssmenv.svg) | ![](https://img.shields.io/pypi/l/ssmenv.svg) |

---
SSMEnv allows you to read parameters from [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html) and operate on results as on dictionary.

## Installation
```bash
pip install ssmenv
```

## Read parameters
Reading parameters is as simply as initialising class object.

```python
from ssmenv import SSMEnv

ssmenv = SSMEnv(("/service/my-service", "/resource/dynamodb"))

# Accessing parameters
debug = ssmenv["SERVICE_MY_SERVICE_DEBUG"]

# As it's dictionary we can also:

# 1. Get list of all loaded parameter's names
list(ssmenv.keys())

# 2. Get list of all loaded parameter's values
list(ssmenv.values())

# and so on.
```

## Populate `os.environ`
You can hide use of `SSMEnv` by using `os.environ` dict.
```python
import os
from ssmenv import SSMEnv

os.environ = {**os.environ, **SSMEnv("/service/my-service")}
```

## Remove common prefixes
Accessing your parameters through whole namespaces can sometimes be not convenient
especially if you have very long names.

Hence why you can use `prefixes` parameter, to make your code cleaner.

 ```python
from ssmenv import SSMEnv

ssmenv = SSMEnv(("/service/my-service",), prefixes=("/service/my-service",))
ssmenv["DEBUG"]
```
