# -*- coding:utf-8 -*-

from httprunner import HttpRunner, Step, Config, RunRequest, RunTestCase


class TestUserLogin(HttpRunner):

    config = Config("User Login").base_url("https://pc.zuihuibao.cn").export("zhbsession")


