import requests
import re
import time
import threading
import pandas as pd

def getHTMLText(url):
        '''
            name:getHTMLText
            function:标准request函数请求网页数据
            url:目标网页
        '''
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/" \
                     "537.36 (KHTML, like Gecko) 37abc/2.0.6.16 Chrome/60.0.3112.113 Safari/537.36"
        try:
                r = requests.get(url, timeout=30, headers={'User-Agent': user_agent})
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                return r.text
        except:
                return ''

def getList(list,path):
            '''
                name:getHTMLText
                function:标准request函数请求网页数据
                url:目标网页
            '''
    #提取数据成表格并存储
            list_url  = 'https://news.ifeng.com/c/special/7tPlDSzDgVk?from=groupmessage&isappinstalled=0'
            html = getHTMLText(list_url )
            #print(re.findall(r"{\"siwang\":\".*?\"},",html)) #单条信息样本
            list['省份'] = re.findall(r"\"name1\":\"(.*?)\",", html)
            list['城市'] = re.findall(r"\"name2\":\"(.*?)\",", html)
            list['确诊'] = re.findall(r"\"quezhen\":\"(.*?)\",",html)
            list['治愈'] = re.findall(r"\"zhiyu\":\"(.*?)\",", html)
            list['死亡'] = re.findall(r"\"siwang\":\"(.*?)\",",html)
            list['更新时间'] = re.findall(r"\"sys_publishDateTime\":\"(.*?)\",", html)
            list.loc[list['城市'] == '', '城市'] = '共计'
            list.loc[list['治愈'] == '', '治愈'] =  0
            list.loc[list['死亡'] == '', '死亡'] =  0
            list.to_excel(path,index=True)

def main():
        file_name = str(time.strftime("%Y-%m-%d %H:%M", time.localtime())).replace(' ',"-").replace(':',"-")
        output_file = 'C:\\Users\\Fan\\Desktop\\learnpython\\Pneumonia_map\\'+ file_name +'.xlsx'
        print(output_file)
        list = pd.DataFrame({})
        getList(list, output_file)
        timer = threading.Timer(3600,main) #一小时启动一次
        timer.start()

main()

