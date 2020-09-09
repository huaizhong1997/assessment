import socketserver
import json
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest

def initial():
    df = pd.read_csv('data/poor.csv', encoding='utf-8')
    df = df[['证件号码', '人数', '文化程度', '健康状况', '劳动技能', '贫困户属性', '致贫原因1', '人均纯收入']]
    df.columns = ['id', 'family_number', 'education_level', 'physical_condition', 'labor_skill',
                  'poverty_state', 'poverty_cause', 'income']

    df.loc[df.family_number.isnull(), 'family_number'] = -1
    df.loc[df.income.isnull(), 'income'] = -1
    df.loc[df.id.isnull(), 'id'] = -1

    df.loc[df.education_level == "文盲或半文盲", 'education_level'] = 0
    df.loc[df.education_level == "小学", 'education_level'] = 1
    df.loc[df.education_level == "初中", 'education_level'] = 2
    df.loc[df.education_level == "高中", 'education_level'] = 3
    df.loc[df.education_level == "大专", 'education_level'] = 4
    df.loc[df.education_level == "本科及以上", 'education_level'] = 5
    df.loc[df.education_level.isnull(), 'education_level'] = 6

    df.loc[df.physical_condition == "健康", 'physical_condition'] = 0
    df.loc[df.physical_condition == "长期慢性病", 'physical_condition'] = 1
    df.loc[df.physical_condition == "患有大病", 'physical_condition'] = 2
    df.loc[df.physical_condition == "残疾", 'physical_condition'] = 3
    df.loc[df.physical_condition == "残疾,长期慢性病", 'physical_condition'] = 4
    df.loc[df.physical_condition == "长期慢性病,残疾", 'physical_condition'] = 5
    df.loc[df.physical_condition == "患有大病,残疾", 'physical_condition'] = 6
    df.loc[df.physical_condition == "残疾,患有大病", 'physical_condition'] = 7
    df.loc[df.physical_condition.isnull(), 'physical_condition'] = -1

    df.loc[df.labor_skill == "普通劳动力", 'labor_skill'] = 0
    df.loc[df.labor_skill == "技能劳动力", 'labor_skill'] = 1
    df.loc[df.labor_skill == "弱劳动力或半劳动力", 'labor_skill'] = 2
    df.loc[df.labor_skill == "丧失劳动力", 'labor_skill'] = 3
    df.loc[df.labor_skill == "无劳动力", 'labor_skill'] = 4
    df.loc[df.labor_skill.isnull(), 'labor_skill'] = -1

    df.loc[df.poverty_state == "一般脱贫户", 'poverty_state'] = 0
    df.loc[df.poverty_state == "低保脱贫户", 'poverty_state'] = 1
    df.loc[df.poverty_state == "特困供养脱贫户", 'poverty_state'] = 2
    df.loc[df.poverty_state == "低保特困供养贫困户", 'poverty_state'] = 2
    df.loc[df.poverty_state.isnull(), 'poverty_state'] = -1

    df.loc[df.poverty_cause == "缺土地", 'poverty_cause'] = 0
    df.loc[df.poverty_cause == "因灾", 'poverty_cause'] = 1
    df.loc[df.poverty_cause == "交通条件落后", 'poverty_cause'] = 2
    df.loc[df.poverty_cause == "缺技术", 'poverty_cause'] = 3
    df.loc[df.poverty_cause == "因学", 'poverty_cause'] = 4
    df.loc[df.poverty_cause == "因婚", 'poverty_cause'] = 5
    df.loc[df.poverty_cause == "因丧", 'poverty_cause'] = 6
    df.loc[df.poverty_cause == "缺劳力", 'poverty_cause'] = 7
    df.loc[df.poverty_cause == "因残", 'poverty_cause'] = 8
    df.loc[df.poverty_cause == "因病", 'poverty_cause'] = 9
    df.loc[df.poverty_cause == "自身发展动力不足", 'poverty_cause'] = 10
    df.loc[df.poverty_cause.isnull(), 'poverty_cause'] = -1
    return df

def isolation(train_data):

    clf = IsolationForest(contamination=0.1)

    X_cols = ['family_number', 'education_level', 'physical_condition', 'labor_skill',
                  'poverty_state', 'poverty_cause', 'income']
    clf = clf.fit(train_data[X_cols])
    pred = clf.predict(train_data[X_cols])
    train_data["SeriousDlqin2yrs"] = pred
    train_data.loc[train_data.SeriousDlqin2yrs == 1, 'SeriousDlqin2yrs'] = 0
    train_data.loc[train_data.SeriousDlqin2yrs == -1, 'SeriousDlqin2yrs'] = 1
    train_data.to_csv('data/train_data.csv', index=False)


def mono_bin(Y, X, n=10):#连续性变量分箱
    # X为待分箱的变量，Y为target变量,n为分箱数量
    r = 0    #设定斯皮尔曼 初始值
    badnum=Y.sum()    #计算坏样本数
    goodnum=Y.count()-badnum    #计算好样本数
    #下面这段就是分箱的核心 ，就是机器来选择指定最优的分箱节点，代替我们自己来设置
    while np.abs(r) < 1:
        d1 = pd.DataFrame({"X": X, "Y": Y, "Bucket": pd.qcut(X, n)})#用pd.qcut实现最优分箱，Bucket：将X分为n段，n由斯皮尔曼系数决定
        d2 = d1.groupby('Bucket', as_index = True)# 按照分箱结果进行分组聚合
        r, p = stats.spearmanr(d2.mean().X, d2.mean().Y)# 以斯皮尔曼系数作为分箱终止条件
        n = n - 1
    d3 = pd.DataFrame(d2.X.min(), columns = ['min'])
    d3['min']=d2.min().X    #箱体的左边界
    d3['max'] = d2.max().X    #箱体的右边界
    d3['bad'] = d2.sum().Y    #每个箱体中坏样本的数量
    d3['total'] = d2.count().Y    #每个箱体的总样本数
    d3['rate'] = d2.mean().Y
    # print(d3['rate'])
    # print('----------------------')
    d3['woe']=np.log((d3['bad']/badnum)/((d3['total'] - d3['bad'])/goodnum))# 计算每个箱体的woe值
    d3['badattr'] = d3['bad']/badnum  #每个箱体中坏样本所占坏样本总数的比例
    d3['goodattr'] = (d3['total'] - d3['bad'])/goodnum  # 每个箱体中好样本所占好样本总数的比例
    iv = ((d3['badattr']-d3['goodattr'])*d3['woe']).sum()  # 计算变量的iv值
    d4 = (d3.sort_values(by = 'min')).reset_index(drop=True)   # 对箱体从大到小进行排序
    # print('分箱结果：')
    # print(d4)
    # print('IV值为：')
    # print(iv)
    woe=list(d4['woe'].round(3))
    cut=[]    #  cut 存放箱段节点
    cut.append(float('-inf'))    # 在列表前加-inf
    for i in range(1,n+1):        # n是前面的分箱的分割数，所以分成n+1份
        qua=X.quantile(i/(n+1))         #quantile 分为数  得到分箱的节点
        cut.append(round(qua,4))    # 保留4位小数       #返回cut
    cut.append(float('inf'))    # 在列表后加  inf
    return d4,iv,cut,woe


def self_bin(Y,X,cut):#离散型变量分箱
    badnum=Y.sum()    # 坏用户数量
    goodnum=Y.count()-badnum    #好用户数量
    d1 = pd.DataFrame({"X": X, "Y": Y, "Bucket": pd.cut(X, cut)})#建立个数据框 X-- 各个特征变量 ， Y--用户好坏标签 ， Bucket--各个分箱
    d2 = d1.groupby('Bucket', as_index = True)# 按照分箱结果进行分组聚合
    d3 = pd.DataFrame(d2.X.min(), columns = ['min'])    #  添加 min 列 ,不用管里面的 d2.X.min()
    d3['min']=d2.min().X
    d3['max'] = d2.max().X
    d3['bad'] = d2.sum().Y
    d3['total'] = d2.count().Y
    d3['rate'] = d2.mean().Y
    d3['woe']=np.log((d3['bad']/badnum + 0.25)/((d3['total'] - d3['bad'])/goodnum + 0.25))# 修正woe计算公式
    d3['badattr'] = d3['bad']/badnum  #每个箱体中坏样本所占坏样本总数的比例
    d3['goodattr'] = (d3['total'] - d3['bad'])/goodnum  # 每个箱体中好样本所占好样本总数的比例
    iv = ((d3['badattr']-d3['goodattr'])*d3['woe']).sum()  # 计算变量的iv值
    d4 = (d3.sort_values(by = 'min')).reset_index(drop=True)   # 对箱体从大到小进行排序
    # print('分箱结果：')
    # print(d4)
    # print('IV值为：')
    # print(iv)
    woe=list(d4['woe'].round(3))
    return d4, iv, woe


def trans_woe(var,var_name,woe,cut):#将各特征数据替换为woe值
    woe_name=var_name+'_woe'
    for i in range(len(woe)):       # len(woe) 得到woe里 有多少个数值
        if i==0:
            var.loc[(var[var_name]<=cut[i+1]),woe_name]=woe[i]  #将woe的值按 cut分箱的下节点，顺序赋值给var的woe_name 列 ，分箱的第一段
        elif (i>0) and  (i<=len(woe)-2):
            var.loc[((var[var_name]>cut[i])&(var[var_name]<=cut[i+1])),woe_name]=woe[i] #    中间的分箱区间   ，，数手指头就很清楚了
        else:
            var.loc[(var[var_name]>cut[len(woe)-1]),woe_name]=woe[len(woe)-1]   # 大于最后一个分箱区间的 上限值，最后一个值是正无穷
    return var


def compute_score(series,cut,score):
    list = []
    i = 0
    while i < len(series):
        value = int(series.iloc[i])
        j = len(cut) - 2
        m = len(cut) - 2
        while j >= 0:
            if value >= cut[j]:
                j = -1
            else:
                j -= 1
                m -= 1
        list.append(score[m])
        i += 1
    return list

def get_score(coe,woe,factor):#生成各个分箱中woe值的分数
    scores=[]
    for w in woe:
        score=round(coe*w*factor,0)
        scores.append(score)
    return scores



def woe():#数据分箱并生成分数
    train_data = pd.read_csv('data/train_data.csv')

    ninf = float('-inf')  # 负无穷大
    pinf = float('inf')  # 正无穷大
    cutx1 = [ninf, 1, 3, 6, 10, pinf]
    cutx2 = [ninf, 0, 2, 4, 5, pinf]
    cutx3 = [ninf, 0, 1, 2, 3, pinf]
    cutx4 = [ninf, 0, 1, 2, 3, pinf]
    cutx5 = [ninf, 0, 1, pinf]
    cutx6 = [ninf, 2, 4, 6, 9, pinf]
    dfx1, ivx1, woex1 = self_bin(train_data.SeriousDlqin2yrs, train_data['family_number'], cutx1)
    dfx2, ivx2, woex2 = self_bin(train_data.SeriousDlqin2yrs, train_data['education_level'], cutx2)
    dfx3, ivx3, woex3 = self_bin(train_data.SeriousDlqin2yrs, train_data['physical_condition'], cutx3)
    dfx4, ivx4, woex4 = self_bin(train_data.SeriousDlqin2yrs, train_data['labor_skill'], cutx4)
    dfx5, ivx5, woex5 = self_bin(train_data.SeriousDlqin2yrs, train_data['poverty_state'], cutx5)
    dfx6, ivx6, woex6 = self_bin(train_data.SeriousDlqin2yrs, train_data['poverty_cause'], cutx6)
    dfx7, ivx7, cutx7, woex7 = mono_bin(train_data['SeriousDlqin2yrs'], train_data.income)

    x1_name = 'family_number'
    x2_name = 'education_level'
    x3_name = 'physical_condition'
    x4_name = 'labor_skill'
    x5_name = 'poverty_state'
    x6_name = 'poverty_cause'
    x7_name = 'income'
    train_data = trans_woe(train_data, x1_name, woex1, cutx1)
    train_data = trans_woe(train_data, x2_name, woex2, cutx2)
    train_data = trans_woe(train_data, x3_name, woex3, cutx3)
    train_data = trans_woe(train_data, x4_name, woex4, cutx4)
    train_data = trans_woe(train_data, x5_name, woex5, cutx5)
    train_data = trans_woe(train_data, x6_name, woex6, cutx6)
    train_data = trans_woe(train_data, x7_name, woex7, cutx7)

    Y = train_data['SeriousDlqin2yrs']  # 因变量
    X = train_data.iloc[:, -7:]  # 自变量
    clf = LogisticRegression()
    clf.fit(X, Y)
    score_proba = clf.predict_proba(X)
    coe = clf.coef_
    intercept = clf.intercept_


    p = 50 / np.log(2)  # 比例因子
    x_coe = coe[0]

    x1_score = get_score(x_coe[0], woex1, p)
    x2_score = get_score(x_coe[1], woex2, p)
    x3_score = get_score(x_coe[2], woex3, p)
    x4_score = get_score(x_coe[3], woex4, p)
    x5_score = get_score(x_coe[4], woex5, p)
    x6_score = get_score(x_coe[5], woex6, p)
    x7_score = get_score(x_coe[6], woex7, p)

    data = [cutx1, cutx2, cutx3, cutx4, cutx5, cutx6, cutx7]
    df = pd.DataFrame(data).T
    df.columns = ['cutx1', 'cutx2', 'cutx3', 'cutx4', 'cutx5', 'cutx6', 'cutx7']
    df.to_csv('data/param_cut.csv', index=False)
    data = [x1_score, x2_score, x3_score, x4_score, x5_score, x6_score, x7_score]
    df = pd.DataFrame(data).T
    df.columns = ['x1_score', 'x2_score', 'x3_score', 'x4_score', 'x5_score', 'x6_score', 'x7_score']
    df.to_csv('data/param_score.csv', index=False)

def score():
    train_data = pd.read_csv('data/train_data.csv')
    baseScore = 650
    train_data['BaseScore'] = np.zeros(len(train_data)) + baseScore

    df = pd.read_csv('data/param_cut.csv')
    cutx1 = df["cutx1"].dropna().tolist()
    cutx2 = df["cutx2"].dropna().tolist()
    cutx3 = df["cutx3"].dropna().tolist()
    cutx4 = df["cutx4"].dropna().tolist()
    cutx5 = df["cutx5"].dropna().tolist()
    cutx6 = df["cutx6"].dropna().tolist()
    cutx7 = df["cutx7"].dropna().tolist()
    df = pd.read_csv('data/param_score.csv')
    x1_score = df["x1_score"].dropna().tolist()
    x2_score = df["x2_score"].dropna().tolist()
    x3_score = df["x3_score"].dropna().tolist()
    x4_score = df["x4_score"].dropna().tolist()
    x5_score = df["x5_score"].dropna().tolist()
    x6_score = df["x6_score"].dropna().tolist()
    x7_score = df["x7_score"].dropna().tolist()

    train_data['family_number_score'] = compute_score(train_data['family_number'], cutx1, x1_score)
    train_data['education_level_score'] = compute_score(train_data['education_level'], cutx2, x2_score)
    train_data['physical_condition_score'] = compute_score(train_data['physical_condition'], cutx3, x3_score)
    train_data['labor_skill_score'] = compute_score(train_data['labor_skill'], cutx4, x4_score)
    train_data['poverty_state_score'] = compute_score(train_data['poverty_state'], cutx5, x5_score)
    train_data['poverty_cause_score'] = compute_score(train_data['poverty_cause'], cutx6, x6_score)
    train_data['income_score'] = compute_score(train_data['income'], cutx7, x7_score)
    train_data['Score'] = train_data['family_number_score'] + train_data['education_level_score'] + train_data['physical_condition_score'] + train_data['labor_skill_score'] + train_data[
        'poverty_state_score'] + train_data['poverty_cause_score'] + train_data['income_score'] + baseScore

    train_data.to_csv('data/score_poor.csv', index=False)



def scoreCard(data):
    df = pd.read_csv('data/param_cut.csv')
    cutx1 = df["cutx1"].dropna().tolist()
    cutx2 = df["cutx2"].dropna().tolist()
    cutx3 = df["cutx3"].dropna().tolist()
    cutx4 = df["cutx4"].dropna().tolist()
    cutx5 = df["cutx5"].dropna().tolist()
    cutx6 = df["cutx6"].dropna().tolist()
    cutx7 = df["cutx7"].dropna().tolist()
    df = pd.read_csv('data/param_score.csv')
    x1_score = df["x1_score"].dropna().tolist()
    x2_score = df["x2_score"].dropna().tolist()
    x3_score = df["x3_score"].dropna().tolist()
    x4_score = df["x4_score"].dropna().tolist()
    x5_score = df["x5_score"].dropna().tolist()
    x6_score = df["x6_score"].dropna().tolist()
    x7_score = df["x7_score"].dropna().tolist()


    df = pd.DataFrame.from_dict([data])
    df = df[['id', 'family_number', 'education_level', 'physical_condition', 'labor_skill',
             'poverty_state', 'poverty_cause', 'income']]
    df.loc[df.education_level == "文盲或半文盲", 'education_level'] = 0
    df.loc[df.education_level == "小学", 'education_level'] = 1
    df.loc[df.education_level == "初中", 'education_level'] = 2
    df.loc[df.education_level == "高中", 'education_level'] = 3
    df.loc[df.education_level == "大专", 'education_level'] = 4
    df.loc[df.education_level == "本科及以上", 'education_level'] = 5
    df.loc[df.education_level.isnull(), 'education_level'] = 6

    df.loc[df.physical_condition == "健康", 'physical_condition'] = 0
    df.loc[df.physical_condition == "长期慢性病", 'physical_condition'] = 1
    df.loc[df.physical_condition == "患有大病", 'physical_condition'] = 2
    df.loc[df.physical_condition == "残疾", 'physical_condition'] = 3
    df.loc[df.physical_condition == "残疾,长期慢性病", 'physical_condition'] = 4
    df.loc[df.physical_condition == "长期慢性病,残疾", 'physical_condition'] = 5
    df.loc[df.physical_condition == "患有大病,残疾", 'physical_condition'] = 6
    df.loc[df.physical_condition == "残疾,患有大病", 'physical_condition'] = 7
    df.loc[df.physical_condition.isnull(), 'physical_condition'] = -1

    df.loc[df.labor_skill == "普通劳动力", 'labor_skill'] = 0
    df.loc[df.labor_skill == "技能劳动力", 'labor_skill'] = 1
    df.loc[df.labor_skill == "弱劳动力或半劳动力", 'labor_skill'] = 2
    df.loc[df.labor_skill == "丧失劳动力", 'labor_skill'] = 3
    df.loc[df.labor_skill == "无劳动力", 'labor_skill'] = 4
    df.loc[df.labor_skill.isnull(), 'labor_skill'] = -1

    df.loc[df.poverty_state == "一般脱贫户", 'poverty_state'] = 0
    df.loc[df.poverty_state == "低保脱贫户", 'poverty_state'] = 1
    df.loc[df.poverty_state == "特困供养脱贫户", 'poverty_state'] = 2
    df.loc[df.poverty_state == "低保特困供养贫困户", 'poverty_state'] = 2
    df.loc[df.poverty_state.isnull(), 'poverty_state'] = -1

    df.loc[df.poverty_cause == "缺土地", 'poverty_cause'] = 0
    df.loc[df.poverty_cause == "因灾", 'poverty_cause'] = 1
    df.loc[df.poverty_cause == "交通条件落后", 'poverty_cause'] = 2
    df.loc[df.poverty_cause == "缺技术", 'poverty_cause'] = 3
    df.loc[df.poverty_cause == "因学", 'poverty_cause'] = 4
    df.loc[df.poverty_cause == "因婚", 'poverty_cause'] = 5
    df.loc[df.poverty_cause == "因丧", 'poverty_cause'] = 6
    df.loc[df.poverty_cause == "缺劳力", 'poverty_cause'] = 7
    df.loc[df.poverty_cause == "因残", 'poverty_cause'] = 8
    df.loc[df.poverty_cause == "因病", 'poverty_cause'] = 9
    df.loc[df.poverty_cause == "自身发展动力不足", 'poverty_cause'] = 10
    df.loc[df.poverty_cause.isnull(), 'poverty_cause'] = -1

    baseScore = 650
    df['BaseScore'] = baseScore
    df['family_number_score'] = compute_score(df['family_number'], cutx1, x1_score)
    df['education_level_score'] = compute_score(df['education_level'], cutx2, x2_score)
    df['physical_condition_score'] = compute_score(df['physical_condition'], cutx3, x3_score)
    df['labor_skill_score'] = compute_score(df['labor_skill'], cutx4, x4_score)
    df['poverty_state_score'] = compute_score(df['poverty_state'], cutx5, x5_score)
    df['poverty_cause_score'] = compute_score(df['poverty_cause'], cutx6, x6_score)
    df['income_score'] = compute_score(df['income'], cutx7, x7_score)
    df['Score'] = df['family_number_score'] + df['education_level_score'] + df[
        'physical_condition_score'] + df['labor_skill_score'] + df[
                              'poverty_state_score'] + df['poverty_cause_score'] + df[
                              'income_score'] + baseScore
    return df.loc[0, 'Score']
def train():
    df = initial()
    isolation(df)
    woe()
    score()


class myTCPhandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(1024).decode('UTF-8', 'ignore').strip()
            print("------------------")
            print(self.data)
            if self.data == "Train":
                train()
                msg = {'status': "success", 'msg': "模型训练成功"}
                jmsg = json.dumps(msg)
                self.feedback_data = jmsg.encode("utf8")
                self.request.sendall(self.feedback_data)
            else:
                dict = json.loads(self.data)
                score = 100
                score = scoreCard(dict)
                msg = {'status': "success", 'msg': "用户评估完毕", 'score': score}
                jmsg = json.dumps(msg)
                self.feedback_data = jmsg.encode("utf8")
                self.request.sendall(self.feedback_data)

if __name__ == "__main__":
    print("listen 9000")
    HOST, PORT = 'localhost', 9000
    server = socketserver.ThreadingTCPServer((HOST,PORT),myTCPhandler)
    server.serve_forever()