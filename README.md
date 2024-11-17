# EconoNav

## Usage
### 自動生成
1. Excelファイルを作成する

こんな感じで作成する(左から 便番号 出発港 出発時間 到着港 到着時間)

![image](https://github.com/Emmomi/EconoNav/assets/63034349/4750bfd1-a32e-41e4-a92b-6a5fc180e378)

2. 以下を実行する
```
py make_graph_sample.py
```
使用する船の数を入力する

### 最適化
1. Excelファイルを作成する

こんな感じで作成する(左から 便番号 出発港 出発時間 到着港 到着時間)

![image](https://github.com/Emmomi/EconoNav/assets/63034349/4750bfd1-a32e-41e4-a92b-6a5fc180e378)

2. `Search.py`中で目的関数を設定する

3. 以下を実行する
```
py back\app\alg\Search.py
```

## Model
$$
  \begin{cases}
    x_s^n \in {0,1} & \quad n \in N,s \in S\\
    \sum_{s \in S} x_s^n & \quad n \in N\\
    x_s^{n_1} + x_s^{n_2} \leq 1 & \quad AT(n_1) > DT(n_2) \wedge DT(n_1) < AT(n_2),n_1 \in N,n_2 \in N,s \in S\\
    \sum_{s \in S} x_s^{n_1} \times x_s^{n_2} = 1 & \quad \forall n_1 \in N, \forall n_2 \in N,DH(n_2) = AH(n_1),DT(n_2) - AT(n_1) = m
  \end{cases}
$$

## Algorithm
$$
$$