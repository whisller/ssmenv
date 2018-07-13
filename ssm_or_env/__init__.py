import os
import re

import boto3


class SSM(object):
    def __init__(self, ssm=None):
        self._ssm = ssm

    def get_parameters(self, *args, **kwargs):
        if not any((os.environ.get('AWS_ACCESS_KEY_ID'),
                    os.environ.get('AWS_CONTAINER_CREDENTIALS_RELATIVE_URI'))):
            return os.environ

        ssm = self._ssm or boto3.client('ssm')

        parameters = {}
        for namespace in args:
            params = []
            next_token = -1
            while next_token != 0:
                search_params = {'Path': namespace, 'WithDecryption': True, 'Recursive': True}

                if next_token != -1:
                    search_params['NextToken'] = next_token

                current_set = ssm.get_parameters_by_path(**search_params)
                params += current_set.get('Parameters')
                next_token = current_set.get('NextToken', 0)

            for param in params:
                name = SSM._normalize_name(param.get('Name'), kwargs.get('env', True))
                parameters[name] = param if kwargs.get('full') else param.get('Value')

        return parameters

    @staticmethod
    def _normalize_name(name, env):
        if env:
            return re.sub('\W', '_', name).upper().strip('_')

        return name
