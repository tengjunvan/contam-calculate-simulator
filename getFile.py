import pandas as pd
import numpy as np
from classes import MainRoom, Elevator


def get_file():                    # 读取数据,存入到类属性当中
    df = pd.read_excel('main1.xlsx')  # 读取数据
    counter = 0                   # 计数器，用来计量读取excel的列数
    for each in df.columns:
        if counter == 0:          # 第一次读取是幕墙列
            a = df[each].values   # 读取大厅列的值，转化为array
            a[np.isnan(a)] = 0    # 转化nan数值为0
            hall = a[0]           # 大厅为1-a[0]层分布
            n = a.shape[0]-1      # 总楼层数量（实际总楼层，而不是减去大厅涉及的楼层）
            detail = a[1:]        # 每层的渗透量（array）
            MainRoom(hall, n, detail)
            counter = counter + 1
        elif counter > 0:          # 之后读取的是电梯列
            a = df[each].values   # 读取电梯列的值，转化为array
            a[np.isnan(a)] = 0      # 转化nan数值为0
            n = a[0]              # 某电梯型号个数
            if n > 0:
                detail_each = a[1:]   # 每层的渗透量（array）
                detail = detail_each*n  # 根据电梯型号个数放大每层的渗透率
                level_list = []          # 电梯楼层列表，0代表第一层
                for i in range(MainRoom.n):
                    if detail_each[i] > 0:
                        level_list.append(i)
                Elevator(each, n, detail, level_list)    # 创建电梯实例
