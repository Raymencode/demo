from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase
from .demo_testcase_usr_login_test import TestcaseUsrlogin


class TestCasePriceConfig(HttpRunner):

    config = Config("price config").base_url("https://pc.zuihuibao.cn").verify(False).export("zhbsession")

    teststeps = [
        Step(
            RunTestCase("登录后获取session")
            .call(TestcaseUsrlogin)
            .export("zhbsession")
        ),
        Step(
            RunRequest("Price configration")
            .post('/yiiapp/car-ins/price-configuration-merge')
            .with_headers(**{"Content - Type": "application/x-www-form-urlencoded", "Cookie": "$zhbsession"})
            .with_data({"province": "云南", "city": "昭通", "product_source": "web"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.data.selected_province", "云南")
        )
    ]


if __name__ == '__main__':

    TestCasePriceConfig.test_start()
