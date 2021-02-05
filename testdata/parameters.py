#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
需求：自动读取、执行excel里面的接口测试用例，测试完成后，返回错误结果并发送邮件通知。
一步一步捋清需求：
1、设计excel表格
2、读取excel表格
3、拼接url，发送请求
4、汇总错误结果、发送邮件
'''
import xlrd
import os
import requests
import json
import yaml
import smtplib
import time
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header


def test_cases_in_excel(test_case_file):
    test_case_file = os.path.join(os.getcwd(), test_case_file)
    # 获取测试用例全路径 如：E:\Python\httprunner\interface_excel\testcases.xlsx
    print(test_case_file)
    if not os.path.exists(test_case_file):
        print("测试用例excel文件存在或路径有误！")
        # 找不到指定测试文件，就退出程序 os.system("exit")是用来退出cmd的
        sys.exit()
    # 读取excel文件
    test_case = xlrd.open_workbook(test_case_file)
    # 获取第一个sheet，下标从0开始
    table = test_case.sheet_by_index(0)
    # 记录错误用例
    error_cases = []
    # 一张表格读取下来，其实就像个二维数组，无非是读取第一行的第几列的值，由于下标是从0开始，第一行是标题，所以从第二行开始读取数据
    for i in range(1, table.nrows):
        num = str(int(table.cell(i, 0).value)).replace("\n", "").replace("\r", "")
        api_name = table.cell(i, 1).value.replace("\n", "").replace("\r", "")
        api_host = table.cell(i, 2).value.replace("\n", "").replace("\r", "")
        request_url = table.cell(i, 3).value.replace("\n", "").replace("\r", "")
        method = table.cell(i, 4).value.replace("\n", "").replace("\r", "")
        request_data_type = table.cell(i, 5).value.replace("\n", "").replace("\r", "")
        request_data = table.cell(i, 6).value.replace("\n", "").replace("\r", "")
        check_point = table.cell(i, 7).value.replace("\n", "").replace("\r", "")
        print(num, api_name, api_host, request_url, method, request_data_type, request_data, check_point)
        try:
            # 调用接口请求方法，后面会讲到
            status, resp = interface_test(num, api_name, api_host, request_url, method,
                                            request_data_type, request_data, check_point)
            if status != 200 or check_point not in resp:
                # append只接收一个参数，所以要讲四个参数括在一起，当一个参数来传递
                # 请求失败，则向error_cases中增加一条记录
                error_cases.append((num + " " + api_name, str(status), api_host + request_url))
        except Exception as e:
            print(e)
            print("第{}个接口请求失败，请检查接口是否异常。".format(num))
            # 访问异常，也向error_cases中增加一条记录
            error_cases.append((num + " " + api_name, "请求失败", api_host + request_url))
    return error_cases


def interface_test(num, api_name, api_host, request_url, method,
                    request_data_type, request_data, check_point):
    # 构造请求headers
    headers = {'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                      'X-Requested-With' : 'XMLHttpRequest',
                      'Connection' : 'keep-alive',
                      'Referer' : 'http://' + api_host,
                      'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
                }
    # 判断请求方式，如果是GET，则调用get请求，POST调post请求，都不是，则抛出异常
    if method == "GET":
        r = requests.get(url=api_host+request_url, params=json.loads(request_data), headers=headers)
        # 获取请求状态码
        status = r.status_code
        # 获取返回值
        resp = r.text
        if status == 200:
            # 断言，判断设置的断言值，是否在返回值里面
            if check_point in str(r.text):
                print("第{}条用例'{}'执行成功，状态码为{}，结果返回值为{}.".format(num, api_name, status, r.text))
                return status, resp
            else:
                print("第{}条用例'{}'执行失败！！！状态码为{}，结果返回值为{}.".format(num, api_name, status, r.text))
                return status, resp
        else:
            print("第{}条用例'{}'执行失败！！！状态码为{}，结果返回值为{}.".format(num, api_name, status, r.text))
            return status, resp
    elif method == "POST":
        # 跟GET里面差不多，就不一一注释了
        r = requests.post(url=api_host+request_url, params=json.loads(request_data), headers=headers)
        status = r.status_code
        resp = r.text
        if status == 200:
            if check_point in str(r.text):
                print("第{}条用例'{}'执行成功，状态码为{}，结果返回值为{}.".format(num, api_name, status, r.text))
                return status, resp
            else:
                print("第{}条用例'{}'执行失败！！！状态码为{}，结果返回值为{}.".format(num, api_name, status, r.text))
                return status, resp
        else:
            print("第{}条用例'{}'执行失败！！！状态码为{}，结果返回值为{}.".format(num, api_name, status, r.text))
            return status, resp
    else:
        print("第{}条用例'{}'请求方式有误！！！请确认字段【Method】值是否正确，正确值为大写的GET或POST。".format(num, api_name))
        return 400, "请求方式有误"


def main():
    # 执行所以测试用例，获取错误的用例
    error_cases = test_cases_in_excel("testcases.xlsx")
    # 如果有错误接口，则开始构造html报告
    if len(error_cases) > 0:
        # html = '<html><body>接口自动化扫描，共有 ' + str(len(error_cases)) + ' 个异常接口，列表如下：' + '</p><table><tr><th style="width:100px;text-align:left">接口</th><th style="width:50px;text-align:left">状态</th><th style="width:200px;text-align:left">接口地址</th><th   style="text-align:left">接口返回值</th></tr>'
        html = '<html><body>接口自动化扫描，共有 ' + str(len(error_cases)) + ' 个异常接口，列表如下：' + '</p><table><tr><th style="width:100px;text-align:left">接口</th><th style="width:50px;text-align:left">状态</th><th style="width:200px;text-align:left">接口地址</th></tr>'
        for test in error_cases:
            # html = html + '<tr><td style="text-align:left">' + test[0] + '</td><td style="text-align:left">' + test[1] + '</td><td style="text-align:left">' + test[2] + '</td><td style="text-align:left">' + test[3] + '</td></tr>'
            html = html + '<tr><td style="text-align:left">' + test[0] + '</td><td style="text-align:left">' + test[1] + '</td><td style="text-align:left">' + test[2] + '</td></tr>'
        send_email(html)
        print(html)
        with open ("report.html", "w") as f:
            f.write(html)
    else:
        print("本次测试，所有用例全部通过")
        send_email("本次测试，所有用例全部通过")


def get_conf():
    with open ("config.yml", "r", encoding='utf-8') as f:
        cfg = f.read()
        dic = yaml.load(cfg)
        # print(type(dic))
        # print(dic)
        sender = dic['email']['sender']
        receiver = dic['email']['receiver']
        smtpserver = dic['email']['smtpserver']
        username = dic['email']['username']
        password = dic['email']['password']
        print(sender, receiver, smtpserver, username, password)
        return sender, receiver, smtpserver, username, password


def send_email(text):
    today = time.strftime('%Y.%m.%d',time.localtime(time.time()))
    sender, receiver, smtpserver, username, password = get_conf()
    # subject为邮件主题 text为邮件正文
    subject = "[api_test]接口自动化测试结果通知 {}".format(today)
    msg = MIMEText(text, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = "".join(receiver)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == "__main__":
    # send_email("test")
    main()