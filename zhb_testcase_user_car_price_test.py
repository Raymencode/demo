from httprunner import HttpRunner, Step, Config,  RunRequest, RunTestCase
from ..zhbsuit1.zhb_testcase_user_pwd_login_test import TestcaseUserLogin


class TestcaseUserPrice(HttpRunner):

    config = Config("user price config").base_url("https://pc.zuihuibao.cn").verify(False)

    teststeps = [
        Step(
            RunTestCase("获取登录session")
            .call(TestcaseUserLogin)
            .export("zhbsession")
        ),

        Step(
            RunRequest("获取报价机构")
            .with_variables(
                **{
                    "province": "云南",
                    "city": "邵通",
                    "product_source": "web",
                }
            )
            .post("/yiiapp/car-ins/price-configuration-merge")
            .with_headers(**{"Content - Type": "application/x-www-form-urlencoded"})
            .with_params(**{"province": "$province", "city": "$city", "product_source": "$product_source"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.data.selected_province", "云南")
        ),

        Step(
            RunRequest("车辆报价")
            .post("/yiiapp/car-ins/record-price-info")
            .with_headers(**{"Content - Type": "application/x-www-form-urlencoded", "Accept":"application/json, text/plain, */*", "Cookie":"$zhbsession"})
            .with_data(
                **{

                }
            )
        )
    ]
