#!/usr/bin/python
# encoding=utf-8

""" Can only be modified by the administrator. Only fixtures are provided.
"""
import jmespath
import pytest
from faker import Faker
from loguru import logger

from tep.client import request
from tep.dao import mysql_engine


@pytest.fixture(scope="session")
def env_vars(config):
    class Clazz:
        def __init__(self):
            env = config["env"]
            self.mapping = {
                "qa": {
                    "domain": "https://qa.com",
                    "mysql_engine": mysql_engine("127.0.0.1",  # host
                                                 "2306",  # port
                                                 "root",  # username
                                                 "123456",  # password
                                                 "test"),  # db_name
                },
                "release": {
                    "domain": "https://release.com",
                    "mysql_engine": mysql_engine("127.0.0.1",
                                                 "2306",
                                                 "root",
                                                 "123456",
                                                 "release"),
                }
                # Add your env and variables
            }
            self.domain = self.mapping[env]["domain"]
            self.mysql_engine = self.mapping[env]["mysql_engine"]
            # Add properties

        def add(self, key, value):
            self.mapping[config["env"]][key] = value

    return Clazz()


@pytest.fixture(scope="session")
def url(env_vars):
    def domain_and_uri(uri):
        if not uri.startswith("/"):
            uri = "/" + uri
        return env_vars.domain + uri

    return domain_and_uri


@pytest.fixture(scope="session")
def faker_ch():
    return Faker(locale="zh_CN")


@pytest.fixture(scope="session")
def faker_en():
    return Faker()


@pytest.fixture(scope="session")
def pd():
    import pandas
    return pandas


def _jwt_headers(token):
    return {"Content-Type": "application/json", "authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def login():
    # Code your login
    logger.info("Administrator login")
    response = request(
        "post",
        url=url("/api/users/login"),
        headers={"Content-Type": "application/json"},
        json={
            "username": "admin",
            "password": "123456",
        }
    )
    assert response.status_code < 400
    response_token = jmespath.search("token", response.json())

    class Clazz:
        token = response_token
        jwt_headers = _jwt_headers(response_token)

    return Clazz
