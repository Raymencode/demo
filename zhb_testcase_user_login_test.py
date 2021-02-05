from httprunner import HttpRunner, Step, Config, RunRequest, RunTestCase
# from ...ocrimg import ocrimg
# from ...identify import idenimage


class TestcaseLogin(HttpRunner):

    config = (
        Config("user login")
        .base_url("https://pc.zuihuibao.cn")
        .export(*["zhbsession", "agency_id"])
        .verify(False)
        .perform()
    )


    teststeps = [
        Step(
            RunRequest("用户验证码登录")
            .with_variables(
                **{
                    "mobile": 10000500005,
                    "verify_code": 9527,
                    "login_type": "23",
                    "agency_channel_code": "jpd125",
                }
            )
            .post("/yiiapp/system/user-login")
            .with_params(**{"mobile": "$mobile", "verify_code": "$verify_code", "login_type": "$login_type", "agency_channel_code": "$agency_channel_code"})
            .with_headers(**{"Content - Type": "application/x-www-form-urlencoded","Accept": "application/json, text/plain, */*","Cache-Control": "no-cache"
,"Referer": "https://pc.zuihuibao.cn/","Cookie": "_uab_collina=159334398994088306391259; PHPSESSID=4ot32dit2memulfq56j0ihm587; Hm_lvt_79ee0e9f63d4bd87c861f98a6d497993=1611737370,1611740209,1611740211,1611885010; Hm_lpvt_79ee0e9f63d4bd87c861f98a6d497993=1612348459; user_id=530938; ZHBSESSID=eecc77bca75acb3a7cea3c256f1e4df1"
})
            .extract()
            .with_jmespath('headers."Set-Cookie"', "zhbsession")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.data.user_id", 530938)
        ),

        Step(
            RunRequest("获取用户agency id")
            .post("/yiiapp/system/get-user-agency-id")
            .with_headers(**{"Content - Type": "application/x-www-form-urlencoded","Accept": "application/json, text/plain, */*"})
            .extract()
            .with_jmespath('body.data.agency_id', "agency_id")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.data.agency_id", 125)
        ),
    ]


if __name__ == "__main__":
    # idenimage()
    TestcaseLogin().test_start()
