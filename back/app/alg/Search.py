from Network import Trans,Node,Network
import csv
import numpy as np

def Time_lag(Arrival,Departure) -> int:
    if int(Arrival/100)==int(Departure/100):
        return Departure-Arrival
    elif int(Arrival/100)-int(Departure/100)<=-1:
        return 60*(int(Departure/100)-int(Arrival/100)-1)+(Departure%100)+60-(Arrival%100)
    else:
        return -1

def st_turnback(node1:Node,node2:Node) -> bool:
    if (node1.trans["harbor"].after==node2.trans["harbor"].befor and Time_lag(node1.trans["time"].after,node2.trans["time"].befor)<=15 and Time_lag(node1.trans["time"].after,node2.trans["time"].befor)>0):
        return True
    else:
        return False

def st_coloring(node1:Node,node2:Node) -> bool:
    pass

def analyse_vec(vec:list) -> int:
    count=0
    for i in vec:
        if i==1:
            count+=1
    return count

def check_route(number:int,routes:list[list[int]]) -> bool:
    for route in routes:
        if number in route:
            return True
    return False


if __name__=="__main__":
    nodes=[]
    Ship=int(input('船の数を入力'))#船の数
    #データの入力
    with open('ShipDate2.csv',encoding="shift-jis") as f:
        ShipDate=csv.reader(f)
        for row in ShipDate:
            node=Node()
            node.add_trans("time",Trans(befor=int(row[2]),after=int(row[4])))
            node.add_trans("harbor",Trans(befor=row[1],after=row[3]))
            nodes.append(node)
    net=Network(nodes)
    net.gen_network(st_turnback)
    routes=[]
    start=[]
    for i in range(len(net.nodes)):
        flag=True
        if analyse_vec(net.A.T[i])==0:
            start.append(i)
    while len(start)>0:
        i=start.pop(0)
        flag=True
        route=[i]
        j=i
        while analyse_vec(net.A[j])==1:
            if analyse_vec(net.A.T[j])>1:
                if not check_route(j,routes):
                    routes.append(route)
                    if route != [j]:
                        routes.append([j])
                    for s in [x for x,y in enumerate(net.A[j]) if y==1]:
                        start.append(s)
                elif not check_route(route[0],routes):
                    routes.append(route)
                flag=False
                break
            if j not in route:
                route.append(j)
            j=np.where(net.A[j]==1)[0][0]
        if analyse_vec(net.A[j])==0:
            if flag:
                if analyse_vec(net.A.T[j])<=1:
                    if j not in route:
                        route.append(j)
                    routes.append(route)
                else:
                    if route!=[j]:
                        routes.append(route)
                        if not check_route(j,routes):
                            routes.append([j])
                    if j in route:
                        if not check_route(j,routes):
                            routes.append([j])
        else:
            if flag:
                if not check_route(j,routes):
                    routes.append(route)
                    if route != [j]:
                        routes.append([j])
                    for s in [x for x,y in enumerate(net.A[j]) if y==1]:
                        if (s not in start) and (not check_route(s,routes)):
                            start.append(s)
                else:
                    if route != [j]:
                        routes.append(route)
    reduce_nodes=[]
    print(routes)
    c=0
    test=[0 for i in range(len(net.A))]
    for i in routes:
        for j in i:
            test[j]+=1
        c+=len(i)
    print(c)
    print(len(net.A))
    print(test)
    for i in [x for x,y in enumerate(test) if y!=1]:
        print(f'{i} {analyse_vec(net.A.T[i])} {analyse_vec(net.A[i])} {test[i]}')
    for route in routes:
        node=Node()
        node.add_trans("harbor",Trans(befor=net.nodes[route[0]].trans["harbor"].befor,after=net.nodes[route[-1]].trans["harbor"].after))
        node.add_trans("time",Trans(befor=net.nodes[route[0]].trans["time"].befor,after=net.nodes[route[-1]].trans["time"].after))
        reduce_nodes.append(node)
    reduce_net=Network(reduce_nodes)
    reduce_net.gen_network(st_turnback)