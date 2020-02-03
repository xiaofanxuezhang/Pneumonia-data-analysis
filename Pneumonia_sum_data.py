import threading
import pandas as pd
import os
from openpyxl import load_workbook

def getPathFile(path):
   '''
   name:getPathFile
   function:获取所给文件夹下所有xlsx文件路径
   path：所给文件夹路径
   '''
   Path = []
   try:
       pathDir = os.listdir(path)
       for allDir in pathDir:
           child = os.path.join('%s/%s' % (path, allDir))
           if os.path.isfile(child) and (".xlsx" in str(allDir)):  # 筛选文件
               Path.append(child)
   except:
       pass
   return Path

def select_data(file_name,path):
    '''
       name:select_data
       function:检查文件，提取需要写入的文件
       file_name:全部数据文件名称
       path：所给文件夹路径
    '''
    saved_data = open(path + '\\data\\saved_data.txt', mode='r')
    data_file_list = saved_data.read()
    #print(data_file_list)
    saved_data.close()
    for i in file_name:  # 判断文件是否已经汇总存储
        new_data_name = []  #本次新写入的文件名列表
        if i in data_file_list:
            print(i+'has saved')
        else:
            print(i)
            sheet_name = ['确诊', '死亡', '治愈']
            path = os.path.dirname(__file__)  # 获取脚本当前路径
            writer_data(i,path,sheet_name)#把未存储的数据写入汇总表
            new_data_name.append(i)
        saved_data = open(path + '\\data\\saved_data.txt', mode='a')
        saved_data.write(','.join(new_data_name))
        saved_data.close()

def writer_data(new_data_name, path, sheet_name):
    '''
           name:writer_data
           function:将数据写入汇总文件多个页面
           new_data_name：要写入的文件名
           path：所给文件夹路径
           sheet_name:excel页标签
    '''
    now_data = pd.ExcelWriter(path + '\\data\\sum_data.xlsx', engine='openpyxl')  #使用openpyxl保持多个sheet不被覆盖
    new_data = pd.read_excel(new_data_name)
    for i in range(len(sheet_name)):
        new_data.rename(columns={sheet_name[i]: max(new_data['更新时间'])}, inplace=True)
        sheet_data = pd.read_excel(path + '\\data\\sum_data.xlsx', sheet_name=sheet_name[i])
        all_data = pd.merge(left=sheet_data, right=new_data[['省份', '城市', max(new_data['更新时间'])]],
                            how='outer', left_on=['省份', '城市'], right_on=['省份', '城市'])
        all_data.to_excel(now_data, sheet_name=sheet_name[i],header=True,index=False)
        new_data.drop([max(new_data['更新时间'])], axis=1, inplace=True)
    now_data.save()
    now_data.close()
