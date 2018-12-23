import re
from collections.abc import Mapping

import boto3

__version__ = "1.0.1"


class SSMEnv(Mapping):
    def __init__(self, include, prefixes=None, ssm_client=None):
        self._include = include
        self._prefixes = prefixes
        self._ssm_client = ssm_client
        self._data = {}

    def __getitem__(self, item):
        if not self._data:
            self._data = self._load()

        return self._data[item]

    def __iter__(self):
        if not self._data:
            self._data = self._load()

        yield from self._data

    def __len__(self):
        if not self._data:
            self._data = self._load()

        return len(self._data)

    def _load(self):
        ssm = self._ssm_client or boto3.client("ssm")

        parameters = {}
        for namespace in self._include:
            params = []
            next_token = -1
            while next_token != 0:
                search_params = {
                    "Path": namespace,
                    "WithDecryption": True,
                    "Recursive": True,
                }

                if next_token != -1:
                    search_params["NextToken"] = next_token

                current_set = ssm.get_parameters_by_path(**search_params)
                params += current_set.get("Parameters")
                next_token = current_set.get("NextToken", 0)

            for param in params:
                name = self._normalize_name(self._remove_prefixes(param.get("Name")))
                parameters[name] = param.get("Value")

        return parameters

    def _remove_prefixes(self, name):
        if not self._prefixes:
            return name

        for prefix in self._prefixes:
            if name.startswith(prefix):
                name = name.replace(prefix, "")

        return name

    def _normalize_name(self, name):
        return re.sub(r"\W", "_", name).upper().strip("_")
