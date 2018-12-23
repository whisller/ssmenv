import os

import boto3
import pytest
from moto import mock_ssm

from ssmenv import SSMEnv


@mock_ssm
@pytest.mark.parametrize(
    "ssm_name_prefix,ssm_value,parameter_type",
    [
        ("/service/org.example.microservice", "1", "String"),
        ("/service/ORG.EXAMPLE.MICROSERVICE", "1", "String"),
        ("/service/ORG-EXAMPLE-MICROSERVICE", "1", "String"),
        ("/service/org-EXAMPLE.microservice", "1", "String"),
        ("/service/org.example.microservice", "1", "SecureString"),
        ("/service/ORG.EXAMPLE.MICROSERVICE", "1", "SecureString"),
        ("/service/ORG-EXAMPLE-MICROSERVICE", "1", "SecureString"),
        ("/service/org-EXAMPLE.microservice", "1", "SecureString"),
    ],
)
def test_it_returns_single_parameter(ssm_name_prefix, ssm_value, parameter_type):
    ssm = boto3.client("ssm")
    ssm.put_parameter(
        Name=ssm_name_prefix + "/debug", Value=ssm_value, Type=parameter_type
    )

    ssm_env = SSMEnv((ssm_name_prefix,))
    assert ssm_env["SERVICE_ORG_EXAMPLE_MICROSERVICE_DEBUG"] == "1"

    param = ssm.get_parameter(Name=ssm_name_prefix + "/debug")
    assert param["Parameter"]["Version"] == 1

    ssm.delete_parameter(Name=ssm_name_prefix)


@mock_ssm
def test_it_returns_multiple_parameters_from_different_namespaces():
    ssm = boto3.client("ssm")
    ssm.put_parameter(Name="/service/test-1/debug", Value="1", Type="String")
    ssm.put_parameter(
        Name="/resource/dynamodb/host", Value="https://example.org", Type="String"
    )

    ssm_env = SSMEnv(("/service/test-1", "/resource/dynamodb"))

    assert ssm_env["SERVICE_TEST_1_DEBUG"] == "1"
    assert ssm_env["RESOURCE_DYNAMODB_HOST"] == "https://example.org"


@mock_ssm
def test_it_allows_to_iterate_over_all_parameters():
    ssm = boto3.client("ssm")
    ssm.put_parameter(Name="/service/test-2/first", Value="first-value", Type="String")
    ssm.put_parameter(
        Name="/service/test-2/second", Value="second-value", Type="String"
    )
    ssm.put_parameter(Name="/service/test-3/first", Value="first-value", Type="String")

    ssm_env = SSMEnv(("/service/test-2", "/service/test-3"))

    assert list(ssm_env.keys()) == [
        "SERVICE_TEST_2_FIRST",
        "SERVICE_TEST_2_SECOND",
        "SERVICE_TEST_3_FIRST",
    ]
    assert list(ssm_env.values()) == ["first-value", "second-value", "first-value"]


@mock_ssm
def test_it_allows_to_populate_os_environ():
    ssm = boto3.client("ssm")
    ssm.put_parameter(Name="/service/test-4/first", Value="first-value", Type="String")

    os.environ = {**os.environ, **SSMEnv(("/service/test-4",))}

    assert os.environ["SERVICE_TEST_4_FIRST"] == "first-value"


@mock_ssm
def test_it_removes_prefixes():
    ssm = boto3.client("ssm")
    ssm.put_parameter(Name="/service/test-5/first", Value="first-value", Type="String")

    ssm_env = SSMEnv(("/service/test-5",), prefixes=("/service/test-5",))

    assert ssm_env["FIRST"] == "first-value"
