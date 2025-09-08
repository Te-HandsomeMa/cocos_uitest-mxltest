import json
import requests

url = "https://oapi.dingtalk.com/robot/send?access_token=564ac7db39fde5a0e45b8713bd8eb901c43920509e34884ccb657218bf0612b8"


def send_dingding(log_file):
    headers = {
        'cache-control': 'no-cache',
        'content-type': 'application/json',
    }
    postdatas = {
        'msgtype': 'markdown',
        'markdown': {
            'title': '自动化测试结果通知',
            'text': f'**自动化测试成功**\n\n日志文件已生成：{log_file}'
        },
        'at': {
            "isAtAll": False
        }
    }
    json_str = json.dumps(postdatas)
    resp = requests.post(url, data=json_str, headers=headers)
    print("钉钉返回：", resp.status_code, resp.text)



def send_dingding_error(log_file):
    headers = {
        'cache-control': 'no-cache',
        'content-type': 'application/json',
    }
    postdatas = {
        'msgtype': 'markdown',
        'markdown': {
            'title': '自动化测试结果通知',
            'text': f'**自动化测试失败**\n\n请检查日志文件：{log_file}'
        },
        'at': {
            "isAtAll": False
        }
    }
    json_str = json.dumps(postdatas)
    requests.post(url, data=json_str, headers=headers)

if __name__ == '__main__':
    send_dingding('log.txt')