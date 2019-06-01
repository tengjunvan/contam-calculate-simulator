import numpy as np


class Elevator:                           # 电梯类
    elevators = list()                    # 空列表，用来存储电梯类实例
    number = 0                            # 电梯基数器

    def __init__(self, name, n, detail, level_list):   # 电梯名字，电梯个数，层数与渗透系数，有开口楼层列表
        self.name = name
        self.n = n
        self.d = detail
        self.ll = level_list            # 停留楼层
        self.id = Elevator.number       # 电梯编号，第一个编号为0
        self.fa = 0                     # 初始化流量
        Elevator.elevators.append(self)
        Elevator.number += 1


class MainRoom:         # 大空间类，只有一个实例
    h = 1
    n = 2
    d = np.zeros(2)
    number = n - h + 1
    fa = 0

    def __init__(self, hall, n, detail):      # 输入，大厅楼层，总楼层，层数与渗透系数
        MainRoom.h = hall                     # 大厅楼层
        MainRoom.n = n                        # 总楼层
        MainRoom.d = detail                   # 每层渗透系数，array，长度为总楼层
        MainRoom.number = n - hall + 1        # 大空间个数
        MainRoom.fa = 0                       # 初始化流量
