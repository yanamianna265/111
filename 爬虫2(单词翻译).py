import requests
url="https://fanyi.baidu.com/sug"
response=requests.get(url)
s=input("请输入要翻译的单词：")
dat={
    "kw":s
}
result=requests.post(url,data=dat)
print(response.status_code)
print(result.json())
