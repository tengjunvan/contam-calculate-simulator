import numpy as np
from classes import MainRoom, Elevator
from weatherConstant import *


def pl(a, b, c, n):  # 算流量公式
    if (a-b) >= 0:
        return c*abs(a-b)**n
    elif (a-b) < 0:
        return -c*abs(a-b)**n


def dr(a, b, c, n):  # 算导数公式（正，非主对角线元素）
    return c*n*abs(a-b)**(n-1)


def dr2(a, b, c, n):  # 算导数公式（负，主对角线元素）
    return -c*n*abs(a-b)**(n-1)


def func(z, n=1):  # 该函数接受一个n维向量，返回一个n维向量
    f = np.zeros(MainRoom.number+Elevator.number)
    for i in range(0, MainRoom.h):  # 计算大厅
        f[0] += pl(P-d1*i*h*g, z[0]-d2*i*h*g, MainRoom.d[i], n)  # 外部流入大厅气流量
        for each in Elevator.elevators:
            f[0] += pl(z[MainRoom.number+each.id]-d2*i*h*g, z[0]-d2*i*h*g, each. d[i], n)  # 电梯流入大厅气流量
    for i in range(MainRoom.h, MainRoom.n):  # 计算大厅上层的大空间
        f[i-MainRoom.h+1] += pl(P-d1*i*h*g, z[i-MainRoom.h+1], MainRoom.d[i], n)  # 外部流入大空间气流量
        for each in Elevator.elevators:
            f[i-MainRoom.h+1] += pl(z[MainRoom.number+each.id]-d2*i*h*g, z[i-MainRoom.h+1], each.d[i], n)  # 电梯流入大空间气流量
    for i in range(0, Elevator.number):  # 计算电梯井
        for j in range(MainRoom.h):  # 大厅流入电梯的气流量
            f[MainRoom.number+i] += pl(z[0]-d2*j*h*g, z[MainRoom.number+i]-d2*j*h*g, Elevator.elevators[i].d[j], n)
        for j in range(MainRoom.h, MainRoom.n):  # 上层大空间流入电梯的气流量
            f[MainRoom.number+i] += pl(z[j-MainRoom.h+1], z[MainRoom.number+i]-d2*j*h*g, Elevator.elevators[i].d[j], n)
    return f


def get_ef(z, n=1):  # 该函数与func差不多，每个项取值为正，为了求每个区域的流量总和
    f = np.zeros(MainRoom.number+Elevator.number)
    for i in range(0, MainRoom.h):  # 计算大厅
        f[0] += abs(pl(P-d1*i*h*g, z[0]-d2*i*h*g, MainRoom.d[i], n))  # 外部流入大厅气流量
        for each in Elevator.elevators:
            f[0] += abs(pl(z[MainRoom.number+each.id]-d2*i*h*g, z[0]-d2*i*h*g, each.d[i], n))  # 电梯流入大厅气流量
    for i in range(MainRoom.h, MainRoom.n):  # 计算大厅上层的大空间
        f[i-MainRoom.h+1] += abs(pl(P-d1*i*h*g, z[i-MainRoom.h+1], MainRoom.d[i], n))  # 外部流入大空间气流量
        for each in Elevator.elevators:
            f[i-MainRoom.h+1] += abs(pl(z[MainRoom.number+each.id]-d2*i*h*g,
                                        z[i-MainRoom.h+1], each.d[i], n))  # 电梯流入大空间气流量
    for i in range(0, Elevator.number):  # 计算电梯井
        for j in range(MainRoom.h):  # 大厅流入电梯的气流量
            f[MainRoom.number+i] += abs(pl(z[0]-d2*j*h*g, z[MainRoom.number+i]-d2*j*h*g,
                                           Elevator.elevators[i].d[j], n))
        for j in range(MainRoom.h, MainRoom.n):  # 上层大空间流入电梯的气流量
            f[MainRoom.number+i] += abs(pl(z[j-MainRoom.h+1], z[MainRoom.number+i]-d2*j*h*g,
                                           Elevator.elevators[i].d[j], n))
    f = f/2  # 折半为总流量
    for each in Elevator.elevators:
        each.fa = f[each.id+MainRoom.number]


def get_tf(z, n=1):  # 求解建筑总流量
    for i in range(0, MainRoom.h):  # 计算大厅
        MainRoom.fa += abs(pl(P-d1*i*h*g, z[0]-d2*i*h*g, MainRoom.d[i], n))  # 外部流入大厅气流量
    for i in range(MainRoom.h, MainRoom.n):  # 计算大厅上层的大空间
        MainRoom.fa += abs(pl(P-d1*i*h*g, z[i-MainRoom.h+1], MainRoom.d[i], n))  # 外部流入大空间气流量
    MainRoom.fa = MainRoom.fa/2
    # 下面分别算流入流出，可以启用作为检验
    '''
    for i in range(0,MainRoom.h):#计算大厅
        flow=pl(P-d1*i*h*g,z[0]-d2*i*h*g,MainRoom.d[i],n)#外部流入大厅气流量
        if flow>=0:
            MainRoom.inflow+=flow
        else:
            MainRoom.outflow+=flow
    for i in range(MainRoom.h,MainRoom.n):#计算大厅上层的大空间
        flow=pl(P-d1*i*h*g,z[i-MainRoom.h+1],MainRoom.d[i],n)#外部流入大空间气流量
        if flow>=0:
            MainRoom.inflow+=flow
        else:
            MainRoom.outflow+=flow
    '''


def jacobian(z, n=1):  # 算雅可比矩阵
    j_matrix = np.zeros([MainRoom.number+Elevator.number, MainRoom.number+Elevator.number])
    for i in range(0, MainRoom.h):
        j_matrix[0, 0] += dr2(P-d1*i*h*g, z[0]-d2*i*h*g, MainRoom.d[i], n)  # 大厅函数对大厅变量求导（来自外部）
        for each in Elevator.elevators:
            j_matrix[0, 0] += dr2(z[MainRoom.number+each.id]-d2*i*h*g, z[0]-d2*i*h*g, each.d[i], n)  # 大厅函数对大厅变量求导（来自电梯）
            j_matrix[0, MainRoom.number+each.id] += dr(z[MainRoom.number+each.id]-d2*i*h*g,
                                                       z[0]-d2*i*h*g, each.d[i], n)  # 大厅函数对电梯变量求导
    for each in Elevator.elevators:
        j_matrix[MainRoom.number+each.id, 0] = j_matrix[0, MainRoom.number+each.id]  # 雅可比矩阵的对称性
    for i in range(MainRoom.h, MainRoom.n):  # 计算大厅上层的大空间
        j_matrix[i-MainRoom.h+1, i-MainRoom.h+1] += dr2(P-d1*i*h*g,
                                                        z[i-MainRoom.h+1], MainRoom.d[i], n)  # 大空间函数对大空间变量求导（来自外部）
        for each in Elevator.elevators:
            j_matrix[i-MainRoom.h+1, i-MainRoom.h+1] += dr2(z[MainRoom.number+each.id]-d2*i*h*g,
                                                            z[i-MainRoom.h+1], each.d[i], n)  # 大空间函数对大空间变量求导（来自电梯）
            j_matrix[i-MainRoom.h+1, MainRoom.number+each.id] += dr(
                                                                    z[MainRoom.number+each.id]-d2*i*h*g,
                                                                    z[i-MainRoom.h+1], each.d[i],n
                                                                    )  # 大空间函数对电梯变量求导（来自电梯）
            j_matrix[MainRoom.number+each.id, i-MainRoom.h+1] = j_matrix[i-MainRoom.h+1,
                                                                         MainRoom.number+each.id]  # 雅可比矩阵的对称性
    for i in range(0, Elevator.number):  # 电梯门主对角线元素
        for j in range(MainRoom.h):  # 电梯函数电梯变量求导(大厅)
            j_matrix[MainRoom.number+i, MainRoom.number+i] += dr2(z[0]-d2*j*h*g, z[MainRoom.number+i]-d2*j*h*g,
                                                                  Elevator.elevators[i].d[j], n)
        for j in range(MainRoom.h, MainRoom.n):  # 电梯函数电梯变量求导(上层空间)
            j_matrix[MainRoom.number+i, MainRoom.number+i] += dr2(z[j-MainRoom.h+1], z[MainRoom.number+i]-d2*j*h*g,
                                                                  Elevator.elevators[i].d[j], n)
    return j_matrix


def new_x(z, ji, f):  # n-r迭代公式
    z_new = z-np.dot(ji, f)
    return z_new


def convergence(f):  # 算收敛值
    c = 0
    for i in range(MainRoom.number+Elevator.number):
        c += f[i]**2
    return c
