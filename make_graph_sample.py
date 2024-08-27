import csv
import pprint
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib
from matplotlib import font_manager
import japanize_matplotlib

#ここでフォントを追加しています

font_manager.fontManager.addfont("ipaexg.ttf")

matplotlib.rc('font', family="IPAexGothic")

#成功すれば['IPAexGothic']と表示されます

print(matplotlib.rcParams['font.family'])


def Time_lag(Arrival, Departure):
    if int(Arrival / 100) == int(Departure / 100):
        return Departure - Arrival
    elif int(Arrival / 100) - int(Departure / 100) <= -1:
        return 60 * (int(Departure / 100) - int(Arrival / 100) -
                     1) + (Departure % 100) + 60 - (Arrival % 100)
    else:
        return -1


def analyse_vec(vec):
    count = 0
    for i in vec:
        if i:
            count += 1
    return count


def edit_table(Dh, Dt, Ah, At, x):
    table = []
    for i in range(len(Dh)):
        s = 0
        for j in range(len(x[i])):
            if x[i][j]:
                s = j
                break
        table.append([Dh[i], Dt[i], Ah[i], At[i], s])
    with open('TimeTable1.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)


if __name__ == '__main__':
    Dh = []
    Dt = []
    Ah = []
    At = []
    Ship = int(input('船の数を入力'))    #船の数
    #データの入力
    with open('ShipDate2.csv', encoding="shift_jis") as f:
        ShipDate = csv.reader(f)
        for row in ShipDate:
            Dh.append(row[1])
            Dt.append(int(row[2]))
            Ah.append(row[3])
            At.append(int(row[4]))

    number = 0
    shape = [len(Dh), len(Dh)]
    Graph = np.zeros(shape)
    graph = nx.DiGraph()

    #隣接行列の作成
    for n in range(len(Dh)):
        for i in range(len(Dh)):
            #print(Time_lag(At[n],Dt[i]))
            if (
                Ah[n] == Dh[i] and Time_lag(At[n], Dt[i]) <= 15
                and Time_lag(At[n], Dt[i]) > 0
                ):

                Graph[n][i] += 1

    #解行列（x変数群）の作成
    x = np.zeros([len(Dh), Ship])
    #連続運行期間の作成
    period = [0 for x in range(1, Ship + 1)]
    print(period)

    #始点の探索
    start = []
    for i in range(len(Dh)):
        count = analyse_vec(Graph.T[i])
        if count == 0:
            start.append(i)
    for i in range(len(Dh)):
        count = analyse_vec(Graph[i])
        if count >= 2:
            for j in range(count - 1):
                start.append(i)

    print(start)

    #割り当て
    for s in start:
        #折り返し制約判定
        route = []
        count = analyse_vec(x[s])
        if count == 0:
            print(f'{s} start!')
            route.append(s)
            flag = 1
            k = s
            while flag:
                flag = 0
                j = 0
                for i in Graph[k]:
                    if i and analyse_vec(x[j]) == 0:
                        route.append(j)
                        k = j
                        flag = 1
                        break
                    j += 1

        else:
            print(f'{s} start!')
            flag = 1
            k = s
            while flag:
                flag = 0
                j = 0
                for i in Graph[k]:
                    if i:
                        print(analyse_vec(x[j]))
                    if i and analyse_vec(x[j]) == 0:
                        route.append(j)
                        k = j
                        flag = 1
                        break
                    j += 1
        if route == []:
            print('None')
            continue
        print(route)

        #塗分け制約判定
        exist = False
        i = 0
        for j in period:
            print(type(j))
            if j == 0:
                P = [Dt[route[0]], At[route[-1]]]
                period[i] = [P]
                exist = True
                print(f'farst {i} get!')
                break
            else:
                for n in j:
                    print(f'{n[0]}~{n[1]} {Dt[route[0]]}~{At[route[-1]]}')
                    if (
                        (n[0] <= Dt[route[0]] and n[1] >= Dt[route[0]]) or
                        (n[0] <= At[route[-1]] and n[1] >= At[route[-1]])
                        ) or (
                            (n[0] >= Dt[route[0]] and n[0] <= Dt[route[-1]]) or
                            (n[1] >= Dt[route[0]] and n[1] <= At[route[-1]])
                            ):
                        break
                else:
                    j.append([Dt[route[0]], At[route[-1]]])
                    exist = True
                    print(f'empty {i} get!')
                    break
            print(f'{i} not get...')
            i += 1

        if exist:
            for j in route:
                x[j][i] = 1

    #グラフの描画
    for n in range(len(Dh)):
        graph.add_node(
            str(n) + '\n' + Dh[n] + '\n' + str(Dt[n]) + '\n' + Ah[n] + '\n' +
            str(At[n])
            )

    for n in range(len(Dh)):
        for i in range(len(Dh)):
            if Graph[n][i] >= 1:
                graph.add_edge(
                    str(n) + '\n' + Dh[n] + '\n' + str(Dt[n]) + '\n' + Ah[n] +
                    '\n' + str(At[n]),
                    str(i) + '\n' + Dh[i] + '\n' + str(Dt[i]) + '\n' + Ah[i] +
                    '\n' + str(At[i])
                    )

    nx.draw(graph, with_labels=True, font_family="IPAexGothic")
    np.savetxt('Graph.txt', Graph, fmt='%.1e')
    #print(graph.degree)
    print(x)
    edit_table(Dh, Dt, Ah, At, x)
    print(period)
    plt.show()
