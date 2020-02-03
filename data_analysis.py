import numpy as np
import pandas as pd
import os
import re
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import Pneumonia_sum_data as psd

plt.rcParams['font.sans-serif']=['SimHei']     #中文显示问题
plt.rcParams['axes.unicode_minus']=False   #符号显示问题

sum_file_name = '\data\sum_data.xlsx'
sheet_name = ['确诊', '死亡', '治愈']
path = os.path.dirname(__file__) #获取脚本当前路径


def data_preprocessing(sum_file_name,sheet_name,path):
    '''
         name:data_preprocessing
         function:删除数据缺失值
         sum_file_name：数据汇总文件名
         sheet_name:excel页标签
    '''
    print('1：确诊  2：死亡  3：治愈')
    i = int(input(':')) -1
    sum_data = pd.read_excel(path + sum_file_name, sheet_name=sheet_name[i])  # 打开数据文件
    # print(sum_data)
    sum_data.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)  # 删除数据缺失行
    # print(sum_data)
    sum_data.to_excel(path + '\data\\' + sheet_name[i] + '.xlsx', header=True, index=False)  # 将当前页面写入
    data_fetch(sum_data)

def data_fetch(data):
    '''
        name:data_fetch
        function:从整理的数据中提取需要的数据并绘图
        data:整理好的数据
    '''
    col_name = [column for column in data]  #提取所有数据列名
    #取出全国增长趋势数据
    growth_trend = data.loc[ (data['省份'] == '全国') & (data['城市'] == '共计'), col_name[2:]]
    #取全国数据行
    growth_trend_x = list(growth_trend)
    growth_trend_y = growth_trend.values.flatten() #将表转置并获取其中的数据，筛掉index与column


    # 取出城市排名前20位数据
    city_ranking = data[['城市',col_name[-1]]][:].loc[ (data['城市'] != '共计')]
    #提取最新的时间，去除统计
    city_ranking.sort_values(col_name[-1], ascending=False, na_position='first', inplace=True)    #排序
    city_ranking=city_ranking[:20][:]  #取前20个城市数据
    city_ranking_x = city_ranking['城市']
    city_ranking_y = city_ranking[col_name[-1]]


    # 取出更新频率数据
    updata_data = pd.DataFrame()  #为方便排序，运算，准备空表，准备载入频率数据
    updata_time = []  #准备载入频率数据
    updata_fre = []   #准备载入频率数据
    for num in range(len(col_name)-1):  #新表为省份，城市，增加人数（当前时刻减去前一时刻）
        if num < 2:
            updata_data[col_name[num]] =data[col_name[num]]
        else:
            updata_data[col_name[num+1]] = data[col_name[num+1]]-data[col_name[num]]
            fre = updata_data.loc[updata_data[col_name[num+1]] > 0, [col_name[num+1]]]
            fre = fre.count()
            # print(fre.values)
            updata_fre.append(fre.values[0])
            ti = re.findall(r"-(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", col_name[num+1])  # 提取列名的时间信息
            updata_time.append(ti[0])

    #对时刻更新频率分析
    updata_fre_data = pd.DataFrame({'更新时间':updata_time,'更新频率':updata_fre})
    updata_fre_data.sort_values('更新频率', ascending=False, na_position='first', inplace=True)  #按频次排序
    updata_fre_data = updata_fre_data[2:12][:] #去除异常值
    #print(updata_fre_data)
    updata_fre_data_x = updata_fre_data['更新时间']
    updata_fre_data_y = updata_fre_data['更新频率']


    city_fre_data =  pd.DataFrame()  #为方便排序，运算，准备空表，准备载入频率数据
    sum_city_name = []  #城市名称列表
    sum_city_fre = []   #城市更新次数列表
    city_fre_data = updata_data.loc[ (data['城市'] != '共计')].T  #转置后方便提取每个城市的数据
    col_city = [column for column in city_fre_data]
    for ind in col_city:
        city_fre = city_fre_data[ind].value_counts() #提取每个城市的统计值，必然0次最多
        city_fre = len(city_fre_data[ind])-2-max(city_fre.values) #长度减去标签占用的两格与统计最大值，为非零个数
        sum_city_fre.append(city_fre)
        city_name = city_fre_data[ind][0]+city_fre_data[ind][1]  # 提取列名的省份，城市
        sum_city_name.append(city_name)

    city_fre_data = pd.DataFrame({'城市名称': sum_city_name, '更新次数': sum_city_fre})
    city_fre_data.sort_values('更新次数', ascending=False, na_position='first', inplace=True)  # 按频次排序
    city_fre_data = city_fre_data[:20][:]  # 去除异常值
    city_fre_data_x = city_fre_data['城市名称']
    city_fre_data_y = city_fre_data['更新次数']

    print('1：全国增长趋势图  2：城市排名图  3：数据更新频率图  4：城市更新频率图')
    i = int(input(':'))
    if i == 1:
        growth_trend_name = '全国增长趋势图'  # 命名
        line_chart(growth_trend_x[::16], growth_trend_y[::16], growth_trend_name)  # 作图
    elif i == 2:
        city_ranking_name = '城市排名图'
        bar_chart(city_ranking_x, city_ranking_y, city_ranking_name)  # 作图
    elif i == 2:
        updata_fre_data_name = '数据更新频率图'
        bar_chart(updata_fre_data_x, updata_fre_data_y, updata_fre_data_name)  # 作图
    elif i == 2:
        city_fre_data_name = '城市更新频率图'
        bar_chart(city_fre_data_x, city_fre_data_y, city_fre_data_name)  # 作图
    else:
        print('输入错误')

def line_chart(x,y,title_name):  #绘图样式:散点折线图
    # 创建x,y轴标签
    plt.style.use('ggplot')  # 设置绘图风格
    fig = plt.figure(figsize=(10, 6))  # 设置图框的大小
    ax1 = fig.add_subplot(1, 1, 1)
    colors1 = '#6D6D6D'
    ax1.plot(x, y,  # x、y坐标
             color='#C42022',  # 折线图颜色为红色
             marker='o', markersize=4  # 标记形状、大小设置
             )
    # ax1.set_xticks(x)  # 设置x轴标签为自然数序列
    ax1.set_xticklabels(x)  # 更改x轴标签值为年份
    plt.xticks(rotation=90)  # 旋转90度，不至太拥挤
    for x, y in zip(x, y):
        plt.text(x, y + 10, '%.0f' % y, ha='center', color=colors1, fontsize=10)
        # '%.0f' %y 设置标签格式不带小数
    # 设置标题及横纵坐标轴标题
    plt.title(title_name, color=colors1, fontsize=18)
    plt.xlabel('时间')
    plt.ylabel('人数')
    # plt.savefig('stock.png',bbox_inches = 'tight',dpi = 300)
    plt.show()

def bar_chart(x,y,title_name):    # 画出柱状图
    plt.bar(x, y)
    # 增加数值
    for x, y in zip(x, y):
        # 标注数值
        # ha='center' 横向居中对齐
        # va='bottom'纵向底部（顶部）对齐
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom')
    plt.title(title_name, fontsize=20)
    plt.show()

file_name = psd.getPathFile(path)#获取所有数据文件全称
psd.select_data(file_name,path)
data_preprocessing(sum_file_name,sheet_name,path)