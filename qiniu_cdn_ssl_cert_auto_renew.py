# -*- coding: utf-8 -*-

'''
脚本使用方式：
python3 qiniu_cdn_ssl_cert_auto_renew.py xxx.yyy.com
'''

from qiniu import Auth
import os
import sys
import requests
import datetime

# 从命令行参数列表中读取cdn域名
cert_domain = sys.argv[1]

access_key = ''
secret_key = ''

if len(sys.argv) < 3:
    #从环境变量中获取 Access Key 和 Secret Key
    access_key = os.getenv('QINIU_ACCESS_KEY')
    secret_key = os.getenv('QINIU_SECRET_KEY')
else:
    access_key = sys.argv[2]
    secret_key = sys.argv[3]

print('QINIU_ACCESS_KEY: ' + access_key)
print('QINIU_SECRET_KEY: ' + secret_key)

# 构建七牛鉴权对象
auth = Auth(access_key, secret_key)

# 上传证书
## 上传 api 地址
sslcertUploadUrl = 'http://api.qiniu.com/sslcert'
## 生成 上传证书 api accesstoken
sslcert_accesstoken = auth.token_of_request(sslcertUploadUrl)
print('上传证书 api accesstoken: ' + sslcert_accesstoken)

## 证书信息
sslcertFolder = '/etc/letsencrypt/live/' + cert_domain
sslcertPriFile = open(sslcertFolder + '/privkey.pem')
sslcertChainFile = open(sslcertFolder + '/fullchain.pem')
sslcertPriStr = sslcertPriFile.read()
sslcertChainStr = sslcertChainFile.read()
nowDate = datetime.date.today().strftime("%Y%m%d")
sslcertData = {
    'name': cert_domain + '-letsencrypt-' + nowDate,
    'common_name': cert_domain,
    'pri': sslcertPriStr,
    'ca': sslcertChainStr
}
sslcertHeaders = {
    'Authorization': 'QBox ' + sslcert_accesstoken,
    'Content-Type': 'application/json'
}
print('证书JSON数据如下：')
print(sslcertData)
## 执行请求
sslcertUploadResponse = requests.post(sslcertUploadUrl, json=sslcertData, headers=sslcertHeaders).json()
print(sslcertUploadResponse)
certID = sslcertUploadResponse['certID']
if certID is None:
    print('证书上传失败！')
    sys.exit()

# 修改 cdn 证书
## 修改证书 api 地址
cdnHttpsconfUrl = 'http://api.qiniu.com/domain/{}/httpsconf'.format(cert_domain)
## 生成 cdn 修改证书 api accesstoken
cdn_httpsconf_accesstoken = auth.token_of_request(cdnHttpsconfUrl)
print('修改证书 api accesstoken: ' + cdn_httpsconf_accesstoken)
## 执行修改请求
httpsconfData = {
    'certId': certID,
    'forceHttps': False,
    'http2Enable': True
}
httpsconfHeaders = {
    'Authorization': 'QBox ' + cdn_httpsconf_accesstoken,
    'Content-Type': 'application/json'
}
httpsconfResponse = requests.put(cdnHttpsconfUrl, json=httpsconfData, headers=httpsconfHeaders).json()
print(httpsconfResponse)
print('修改七牛 CDN SSL 证书完成~')
