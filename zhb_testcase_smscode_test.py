from httprunner import HttpRunner, Config, RunTestCase, RunRequest ,Step


class TestSmsCode(HttpRunner):

    config = Config("Sms code").base_url("https://pc.zuihuibao.cn").verify(False).export(*["forsession"])

    teststeps = [
        Step(
            RunRequest("获取smscode")
            .with_variables(
                **{
                    "mobileNum": 10000500005,
                    "uuid": "10000500005",
                    "verify_code": 9421
                }
            )
            .post("/php2/mobile/send_smscode2.php")
            .with_headers(**{
                "Accept": "application / json, text / plain, * / *",
                "Accept - Encoding": "gzip, deflate, br",
                "Accept - Language": "zh - CN, zh;q = 0.9",
                "Cache - Control": "no - cache",
                "Connection": "keep - alive",
                "Content - Length": "55",
                "Content - Type": "application / x - www - form - urlencoded;charset = UTF - 8"
            })
            .with_params(**{"mobileNum":"$mobileNum", "uuid": "$uuid", "verify_code": "$verify_code"})
            .extract()
            .with_jmespath('header."Set-Cookie"', "forsession")
            .validate()
            .assert_equal("status_code", 200)
        )
    ]


if "__name__" == "__main__":
    TestSmsCode().test_start()
