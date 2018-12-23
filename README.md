# SSMEnv

Simple helper class that allows you to read values either from environment variables or AWS SSM.
Depending what is available at the moment.

If `AWS_ACCESS_KEY_ID` or `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` is set then library will try to read from AWS SSM.

Library reads all all parameters for provided namespace.

## Installation
Library requires `boto3` installed.

`pip install ssm_or_env`

## Usage
```python
from ssm_or_env import SSM

params = SSM()('/resource/mysql', '/service/my-app')
print(params)
# {"RESOURCE_MYSQL_USER": "root", "RESOURCE_MYSQL_PASS: "test123", "SERVICE_MY_APP_DEBUG": True}
```

## Use cases?
Imagine any of your code (lambda, app inside docker container) relies on parameters from SSM.
Now you want to run it locally through e.g. `docker-compose` and want to set some dummy data rather than really connect to AWS SSM.

Library will read from environment variables instead of connecting to AWS SSM.
