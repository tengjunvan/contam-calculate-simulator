from solveFunctionsTools import *
from getFile import get_file
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']   # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号


def get_ans():  # 调用该函数来得到结果,返回解和迭代次数
    t = MainRoom.number+Elevator.number
    z_list = []  # 解记录列表，从初试（线性）解开始
    j_matrix_list = []  # 雅可比矩阵记录列表，同上
    d_list = []  # 雅可比矩阵行列式记录列表，同上
    f_list = []  # 函数值列表，同上
    c_list = []  # 收敛值列表，同上

    z_initial = new_x(np. zeros(t), np.linalg.inv(jacobian(np. zeros(t))), func(np.zeros(t)))
    # 来算初始（线性）解
    z_list.append(z_initial)
    n = 0.67
    i = 0  # 迭代次数计数器
    while i < 10000:    # 迭代次数不超过10000次
        z = z_list[i]
        f = func(z, n)  # 函数值
        f_list.append(f)
        c = convergence(f)
        c_list.append(c)
        if c < 0.005:
            get_ef(z, n)  # 计算收敛后求得各个区域总流量
            get_tf(z, n)  # 计算建筑总流量
            break
        j = jacobian(z, n)
        j_matrix_list.append(j)
        if np.linalg.det(j) != 0:
            d_list.append(np.linalg.det(j))
            ji = np.linalg.inv(j)
            z_new = new_x(z, ji, f)
            z_list.append(z_new)
            i = i + 1
        else:
            print('第'+str(i)+'次迭代的'+'雅可比矩阵的行列式为0')
            break
    return z_list, i, j_matrix_list, f_list, c_list


def get_gap(z):  # 输出每一个电梯压差值以及每层表面的压差值
    for each in Elevator.elevators:
        each.gm = [0, 0]  # 最大压差初始化，一个list值，第一个是楼层，第二个是压差值
        for i in each.ll:  # 遍历该电梯楼层
            if i < MainRoom.h:  # 在大厅内的楼层
                if abs(z[0]-z[MainRoom.number+each.id]) >= abs(each.gm[1]):
                    each.gm[0] = i
                    each.gm[1] = abs(z[0]-z[MainRoom.number+each.id])
            elif i >= MainRoom.h:  # 非大厅内的楼层
                if abs(z[i-MainRoom.h+1]-(z[MainRoom.number+each.id]-d2*i*h*g)) >= abs(each.gm[1]):
                    each.gm[0] = i
                    each.gm[1] = abs(z[i-MainRoom.h+1]-(z[MainRoom.number+each.id]-d2*i*h*g))
        # 底部压差值
        if each.ll[0] < MainRoom.h:
            each.b = z[0]-z[MainRoom.number+each.id]
        elif each.ll[0] >= MainRoom.h:
            each.b = z[each.ll[0]-MainRoom.h+1]-z[MainRoom.number+each.id]+d2*each.ll[0]*h*g
        # 顶部压差值
        if each.ll[-1] < MainRoom.h:
            each.t = z[0]-z[MainRoom.number+each.id]
        elif each.ll[-1] >= MainRoom.h:
            each.t = z[each.ll[-1]-MainRoom.h+1]-z[MainRoom.number+each.id]+d2*each.ll[-1]*h*g
        # 每个开口层的压差值
        each.lg = []
        for i in each.ll:
            if i < MainRoom.h:
                each.lg.append((z[0]-z[MainRoom.number+each.id]))
            elif i >= MainRoom.h:
                each.lg.append(z[i-MainRoom.h+1]-(z[MainRoom.number+each.id]-d2*i*h*g))
    MainRoom.lg = []  # 初始化表面压差，列表
    for i in range(MainRoom.n):  # 求每层外表面的压差
        if i < MainRoom.h:  # 在大厅内
            MainRoom.lg.append(P-d1*i*h*g-(z[0]-d2*i*h*g))
        elif i >= MainRoom.h:
            MainRoom.lg.append(P-d1*i*h*g-z[i-MainRoom.h+1])


get_file()  # 读取excel文件，创建类
answers_list, iter_times, matrix_list, func_list, convergence_list = get_ans()  # 计算非线性方程组
get_gap(answers_list[-1])  # 解的后处理，得到压差值

for each in Elevator.elevators:
    print(each.name, ':', '底部压差:', each.ll[0]+1, '层',each.b, '顶部压差', each.ll[-1]+1,
          '层', each.t, '最大压差', each.gm[0]+1, '层', each.gm[1])

for each in Elevator.elevators:
    print(each.name, ':', '总流量', each.fa)
