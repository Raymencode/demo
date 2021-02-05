from httprunner import HttpRunner, Step, Config, RunRequest, RunTestCase


class TestcaseUserLogin(HttpRunner):

    config = (
        Config("user pwd login")
        .base_url("https://pc.zuihuibao.cn")
        .export(*["zhbsession", "agency_id"])
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("用户登录")
            .with_variables(
                **{
                    "mobile": 10000500005,
                    "pwd": "fdbc6f40e9e178dd990058bb52888552342a35bb7ed0ca547c9a67eeb2dbb5b6",
                    "password": "fbc48070518afcb58878d596cefbf38c",
                    "login_type": "23",
                    "agency_channel_code": "jpd125",
                }
            )
            .post("/yiiapp/user-pwd/user-pwd-login")
            .with_params(**{"mobile": "$mobile", "pwd": "$pwd", "password": "$password", "login_type": "$login_type", "agency_channel_code": "$agency_channel_code"})
            .with_headers(**{"Content - Type": "application/x-www-form-urlencoded"})
            .extract()
            .with_jmespath('headers."Set-Cookie"', "zhbsession")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.data.user_id", 530938)
        ),

        Step(
            RunRequest("获取用户agency id")
            .post("/yiiapp/system/get-user-agency-id")
            .with_headers(**{"Content - Type": "application/x-www-form-urlencoded", "cookie": "$zhbsession"})
            .extract()
            .with_jmespath('body.data.agency_id', "agency_id")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.data.agency_id", 125)
        )
    ]


if __name__ == "__main__":
    TestcaseUserLogin().test_start()
